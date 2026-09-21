#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Tests automatisés de l'infrastructure Dataset & Benchmark
===================================================================
Vérifie :
1. La validité du Master Dataset après migration des 25 exemples historiques.
2. La conformité au schéma Pydantic et JSON Schema.
3. L'étanchéité absolue des splits (non-contamination).
4. Le fonctionnement des algorithmes de déduplication (SHA-256 et pHash).
5. La conformité exacte de l'export Qwen2-VL et sa rétro-compatibilité avec train_qlora.py.
6. Le bon fonctionnement du Benchmark Runner sur les 13 axes.
"""

import os
import sys
import json
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from dataset.master.schema.models import MasterAnnotation
except ModuleNotFoundError:
    # `dataset/master/schema/models.py` is part of the original author's local
    # dataset construction workspace (the `dataset/` tree itself is gitignored
    # and not redistributed — see DATASET.md, "Data Access Policy"). This
    # module was never migrated into the published `dataset_tools` package, so
    # this entire test file cannot run against a fresh public clone. See
    # REPRODUCIBILITY.md, "Reproducibility Limitations" for details instead of
    # failing with an opaque ImportError at collection time.
    pytest.skip(
        "test_dataset_infra.py requires the private `dataset/master/schema/models.py` "
        "module, which is not part of this public repository. See REPRODUCIBILITY.md.",
        allow_module_level=True,
    )

from dataset_tools.validation.taxonomy import SplitName, Skill, LearningType, QAStatus
from dataset_tools.validation.qa_validator import QAValidator
from dataset_tools.deduplication.hasher import compute_sha256, compute_average_hash, hamming_distance
from dataset_tools.deduplication.dedup_detector import DeduplicationAnalyzer
from dataset_tools.splitting.leak_detector import SplitLeakageDetector
from dataset_tools.export.export_qwen_vl import export_master_to_qwen_vl
from evaluation.runners.benchmark_runner import ArchiBenchmarkRunner


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MASTER_FILE = os.path.join(BASE_DIR, "dataset", "master", "annotations", "master_annotations.jsonl")


@pytest.fixture
def master_records():
    """Fixture chargeant les 25 exemples du Master Dataset."""
    assert os.path.exists(MASTER_FILE), f"Master file introuvable: {MASTER_FILE}"
    records = []
    with open(MASTER_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def test_master_dataset_count_and_invariants(master_records):
    """Vérifie que les 25 exemples historiques sont intégralement préservés."""
    assert len(master_records) == 25, f"Le master dataset doit contenir exactement 25 exemples, trouvé {len(master_records)}"
    
    # Vérification unicité des ID
    ids = [r["id"] for r in master_records]
    assert len(ids) == len(set(ids)), "Collision d'identifiants détectée dans le Master Dataset"
    
    # Vérification répartition train / validation
    train_count = sum(1 for r in master_records if r.get("assigned_split") == "train")
    val_count = sum(1 for r in master_records if r.get("assigned_split") == "validation")
    assert train_count == 20, f"Le split train doit contenir 20 exemples, trouvé {train_count}"
    assert val_count == 5, f"Le split val doit contenir 5 exemples, trouvé {val_count}"


def test_pydantic_and_schema_validation(master_records):
    """Vérifie que chaque enregistrement master instancie sans erreur MasterAnnotation."""
    for record in master_records:
        model = MasterAnnotation(**record)
        assert model.id
        assert len(model.images) >= 1
        assert model.images[0].path
        assert model.learning_type in LearningType
        assert model.qa_status in QAStatus


def test_split_leakage_detector(master_records):
    """Vérifie qu'aucune fuite n'existe entre le train et la validation."""
    train_samples = [r for r in master_records if r.get("assigned_split") == "train"]
    val_samples = [r for r in master_records if r.get("assigned_split") == "validation"]
    
    detector = SplitLeakageDetector()
    report = detector.check_splits(train_samples, val_samples)
    
    assert report["is_clean"] is True, f"Fuite détectée entre les splits : {report['leakages']}"
    assert len(report["leakages"]) == 0


def test_deduplication_analyzer(master_records):
    """Vérifie que l'analyseur de doublons ne détecte aucune collision anormale."""
    analyzer = DeduplicationAnalyzer(hamming_threshold=3)
    results = analyzer.analyze(master_records)
    
    assert len(results["id_collisions"]) == 0
    assert len(results["exact_image_duplicates"]) == 0
    assert len(results["exact_text_duplicates"]) == 0


def test_qa_validator_full(master_records):
    """Vérifie que le validateur QA certifie le master dataset."""
    validator = QAValidator(BASE_DIR)
    qa_report = validator.validate_dataset_file(MASTER_FILE)
    
    assert qa_report["is_valid"] is True
    assert qa_report["status_distribution"]["FAIL"] == 0


def test_export_qwen_vl_compatibility(tmp_path, master_records):
    """Vérifie que l'exporteur produit un format compatible avec train_qlora.py."""
    export_out = str(tmp_path / "exported_test.jsonl")
    count = export_master_to_qwen_vl(MASTER_FILE, export_out)
    
    assert count == 25
    assert os.path.exists(export_out)
    
    with open(export_out, "r", encoding="utf-8") as f:
        first_line = json.loads(f.readline())
        assert "id" in first_line
        assert "image" in first_line
        assert "conversations" in first_line
        assert len(first_line["conversations"]) == 2
        assert first_line["conversations"][0]["role"] == "user"
        assert first_line["conversations"][1]["role"] == "assistant"


def test_benchmark_runner_on_baseline():
    """Vérifie que le benchmark runner s'exécute correctement sur la baseline."""
    baseline_path = os.path.join(BASE_DIR, "evaluation", "baseline", "baseline_results.json")
    assert os.path.exists(baseline_path), "Fichier baseline_results.json introuvable"
    
    runner = ArchiBenchmarkRunner()
    result = runner.evaluate_baseline_file(baseline_path)
    
    assert result.global_score > 0.0
    assert len(result.axis_scores) == 13
    assert "Vision" in result.axis_scores
    assert "Anti-hallucination" in result.axis_scores
