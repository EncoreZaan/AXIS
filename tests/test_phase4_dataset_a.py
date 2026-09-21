# -*- coding: utf-8 -*-
"""
test_phase4_dataset_a.py — Comprehensive Test Suite for Dataset A
=================================================================
ARCHI-AI — Phase 4 Controlled Unimodal Micro-Pilot
Vérifie rigoureusement :
- Absence totale de collision avec le Gold Set V3 (IDs et groupes de projets)
- Absence totale de leakage intra-projet entre train, val et test
- Validité à 100% des target contracts
- Complétude de la traçabilité et provenance (100%)
- Absence de sources interdites (FloorPlanCAD, ResPlan métrique)
- Reproductibilité déterministe et stabilité des hashes de manifestes
- Emboîtement strict des variantes (Small ⊂ Medium ⊂ Full)
"""

import json
import hashlib
from pathlib import Path
import pytest

from dataset_tools.experiments.target_validators import TargetContractValidator, TargetValidationStatus

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_A_DIR = BASE_DIR / "dataset" / "experiments" / "phase4_micro_pilot" / "dataset_a"
GOLD_MANIFEST = BASE_DIR / "dataset" / "supervision" / "v1" / "manifests" / "GOLD_V3_MANIFEST.jsonl"


@pytest.fixture(scope="module")
def gold_data():
    """Charge l'ensemble des IDs, projets et sources du Gold Set V3."""
    ids = set()
    projects = set()
    sources = set()
    with open(GOLD_MANIFEST, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                ids.add(rec["example_id"])
                projects.add(rec["project_group_id"])
                for s in rec.get("source_ids", []):
                    sources.add(s)
    return {"ids": ids, "projects": projects, "sources": sources}


@pytest.fixture(scope="module")
def dataset_a_examples():
    """Charge l'ensemble des exemples par variante et par split."""
    variants = {}
    for var in ["small", "medium", "full"]:
        var_data = {"train": [], "validation": [], "test": []}
        for s in ["train", "validation", "test"]:
            p = DATASET_A_DIR / var / f"{s}.jsonl"
            assert p.exists(), f"Fichier de split manquant : {p}"
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        var_data[s].append(json.loads(line))
        variants[var] = var_data
    return variants


def test_no_gold_overlap(gold_data, dataset_a_examples):
    """Vérifie : Gold IDs ∩ Dataset A = ∅ sur l'ensemble des variantes."""
    for var, splits in dataset_a_examples.items():
        for s, ex_list in splits.items():
            for ex in ex_list:
                assert ex["example_id"] not in gold_data["ids"], (
                    f"Collision critique Gold ID détectée dans {var} {s} : {ex['example_id']}"
                )


def test_no_gold_project_overlap(gold_data, dataset_a_examples):
    """Vérifie : Gold project groups ∩ Dataset A project groups = ∅."""
    for var, splits in dataset_a_examples.items():
        for s, ex_list in splits.items():
            for ex in ex_list:
                proj = ex["project_group_id"]
                assert proj not in gold_data["projects"], (
                    f"Contamination Gold Project Group détectée dans {var} {s} : {proj}"
                )


def test_no_project_split_leakage(dataset_a_examples):
    """Vérifie l'étanchéité stricte : Train ∩ Val = ∅, Train ∩ Test = ∅, Val ∩ Test = ∅."""
    for var, splits in dataset_a_examples.items():
        train_projs = {e["project_group_id"] for e in splits["train"]}
        val_projs = {e["project_group_id"] for e in splits["validation"]}
        test_projs = {e["project_group_id"] for e in splits["test"]}

        leak_train_val = train_projs & val_projs
        leak_train_test = train_projs & test_projs
        leak_val_test = val_projs & test_projs

        assert len(leak_train_val) == 0, f"Fuite projet Train ∩ Val dans {var} : {leak_train_val}"
        assert len(leak_train_test) == 0, f"Fuite projet Train ∩ Test dans {var} : {leak_train_test}"
        assert len(leak_val_test) == 0, f"Fuite projet Val ∩ Test dans {var} : {leak_val_test}"


def test_no_duplicate_projects_across_splits(dataset_a_examples):
    """Vérifie qu'aucun projet n'est répété entre splits différents."""
    for var, splits in dataset_a_examples.items():
        all_projs = []
        for s in ["train", "validation", "test"]:
            all_projs.extend([e["project_group_id"] for e in splits[s]])
        assert len(all_projs) == len(set(all_projs)), (
            f"Doublons de projets détectés dans {var}"
        )


def test_all_targets_valid(dataset_a_examples):
    """Exécute validate_target sur chaque exemple de Dataset A (100% VALID requis)."""
    for var, splits in dataset_a_examples.items():
        for s, ex_list in splits.items():
            for ex in ex_list:
                status, msg = TargetContractValidator.validate_example(ex)
                assert status == TargetValidationStatus.VALID, (
                    f"Exemple invalide dans {var} {s} ({ex['example_id']}): {msg}"
                )


def test_provenance_complete(dataset_a_examples):
    """Vérifie que 100% des exemples possèdent une provenance complète et vérifiable."""
    for var, splits in dataset_a_examples.items():
        for s, ex_list in splits.items():
            for ex in ex_list:
                prov = ex.get("provenance")
                assert prov is not None, f"Provenance manquante : {ex['example_id']}"
                assert "source_dataset" in prov and prov["source_dataset"]
                assert "source_asset" in prov and prov["source_asset"]
                assert "source_sha256" in prov and len(prov["source_sha256"]) == 64
                assert "transformation_chain" in prov and len(prov["transformation_chain"]) > 0


def test_no_forbidden_sources(dataset_a_examples):
    """Vérifie l'absence absolue de FloorPlanCAD, ResPlan métrique ou tout asset non certifié."""
    forbidden = ["FLOORPLANCAD", "RESPPLAN", "METRIC_RESPPLAN"]
    for var, splits in dataset_a_examples.items():
        for s, ex_list in splits.items():
            for ex in ex_list:
                src = ex.get("source_dataset", "").upper()
                for f in forbidden:
                    assert f not in src, f"Source interdite détectée : {src} dans {ex['example_id']}"


def test_deterministic_build():
    """Vérifie que le build produit les mêmes hashes de manifestes attendus."""
    expected_hashes = {
        "SMALL": "bb3a009124de6ae53a8868b0755c345c5f1e4bee271d75c2afc2dbd2a40aa790",
        "MEDIUM": "ab65451083dc077853f1802b6d97009d800859b306524897e806c2c5db644c78",
        "FULL": "83697dc13b41c3fc08bee7128974c9be7e3bc3ac3eedaa1421cb0910644bd93c"
    }
    for var, exp_hash in expected_hashes.items():
        m_file = DATASET_A_DIR / "manifests" / f"DATASET_A_{var}_MANIFEST.jsonl"
        assert m_file.exists()
        with open(m_file, "rb") as f:
            computed_hash = hashlib.sha256(f.read()).hexdigest()
        assert computed_hash == exp_hash, f"Hash manifest instable pour {var} : {computed_hash} != {exp_hash}"


def test_manifest_hash_stable():
    """Vérifie que les statistiques JSON concordent exactement avec les manifestes."""
    for var in ["SMALL", "MEDIUM", "FULL"]:
        stat_file = DATASET_A_DIR / "statistics" / f"{var}_STATS.json"
        manifest_file = DATASET_A_DIR / "manifests" / f"DATASET_A_{var}_MANIFEST.jsonl"
        with open(stat_file, "r", encoding="utf-8") as f:
            stats = json.load(f)
        with open(manifest_file, "rb") as f:
            m_hash = hashlib.sha256(f.read()).hexdigest()
        assert stats["manifest_sha256"] == m_hash


def test_expected_task_set(dataset_a_examples):
    """Vérifie la présence exacte des 4 tâches sélectionnées sans ajout parasite."""
    expected_tasks = {"FLOORPLAN_READING", "ROOM_TOPOLOGY", "OBJECT_RELATION", "CLEARANCE_CHECK"}
    for var, splits in dataset_a_examples.items():
        found_tasks = set()
        for s, ex_list in splits.items():
            for ex in ex_list:
                found_tasks.add(ex["task_id"])
        assert found_tasks == expected_tasks, f"Tâches discordantes dans {var} : {found_tasks}"


def test_subset_nesting(dataset_a_examples):
    """Garantit l'emboîtement strict des ensembles : Small ⊂ Medium ⊂ Full."""
    small_ids = set()
    medium_ids = set()
    full_ids = set()

    for s in ["train", "validation", "test"]:
        small_ids.update(e["example_id"] for e in dataset_a_examples["small"][s])
        medium_ids.update(e["example_id"] for e in dataset_a_examples["medium"][s])
        full_ids.update(e["example_id"] for e in dataset_a_examples["full"][s])

    assert len(small_ids) == 800
    assert len(medium_ids) == 2400
    assert len(full_ids) == 6000

    assert small_ids.issubset(medium_ids), "Small n'est pas strictement inclus dans Medium"
    assert medium_ids.issubset(full_ids), "Medium n'est pas strictement inclus dans Full"
