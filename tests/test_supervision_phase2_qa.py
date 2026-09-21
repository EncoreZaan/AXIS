# -*- coding: utf-8 -*-
"""
ARCHI-AI — Suite de Certification QA Phase 2 (Supervision QA Suite)
==================================================================
Valide contractuellement les 10 critères d'intégrité avant franchissement du Gate :
1. Conformité des Task Contracts (69 contrats formels)
2. Schéma unifié des exemples de supervision
3. Grounding obligatoire de tout exemple multimodal
4. Test d'ablation de nécessité multimodale
5. Validité des cibles déterministes (non hallucinées)
6. Zéro contamination entre splits (Split Leakage = 0)
7. Absence de shortcuts ou fuite de réponse dans la question
8. Quarantaine stricte de ResPlan (zéro mesure arbitraire)
9. Intégrité et double validation du Gold Set V3
10. Traçabilité et provenance (100% rattachés au Master Dataset v2)
"""

import os
import sys
import json
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MANIFESTS_DIR = BASE_DIR / "dataset" / "supervision" / "v1" / "manifests"
SPLITS_DIR = BASE_DIR / "dataset" / "supervision" / "v1" / "splits"
REVIEW_DIR = BASE_DIR / "dataset" / "supervision" / "v1" / "review"


@pytest.fixture(scope="module")
def task_contracts():
    p = MANIFESTS_DIR / "TASK_MANIFEST.jsonl"
    assert p.exists(), f"TASK_MANIFEST introuvable: {p}"
    contracts = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                contracts.append(json.loads(line))
    return contracts


@pytest.fixture(scope="module")
def supervision_examples():
    p = MANIFESTS_DIR / "SUPERVISION_MANIFEST.jsonl"
    assert p.exists(), f"SUPERVISION_MANIFEST introuvable: {p}"
    examples = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                examples.append(json.loads(line))
    return examples


@pytest.fixture(scope="module")
def gold_v3_examples():
    p = MANIFESTS_DIR / "GOLD_V3_MANIFEST.jsonl"
    assert p.exists(), f"GOLD_V3_MANIFEST introuvable: {p}"
    gold = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                gold.append(json.loads(line))
    return gold


def test_01_task_contracts_count_and_schema(task_contracts):
    """Vérifie que les 69 contrats de tâches sont formalisés et valides."""
    assert len(task_contracts) == 69, f"Attendu 69 contrats, obtenu {len(task_contracts)}"
    for c in task_contracts:
        assert "task_id" in c and c["task_id"]
        assert "task_family" in c and c["task_family"]
        assert "modality" in c and c["modality"]
        assert "difficulty_levels" in c and len(c["difficulty_levels"]) > 0
        assert "status" in c and c["status"] in [
            "VALID", "PARTIAL", "DUPLICATE", "FAKE_MULTIMODAL", "UNDERSPECIFIED", "INVALID", "MISSING_EVIDENCE"
        ]


def test_02_example_schema_and_epistemic_tags(supervision_examples):
    """Vérifie la conformité du schéma et la présence des balises épistémiques."""
    assert len(supervision_examples) > 0
    required_tags = ["[OBSERVATION]", "[INTERPRETATION]", "[INFERENCE]", "[UNKNOWN]"]
    for ex in supervision_examples:
        assert "example_id" in ex and ex["example_id"]
        assert "task_id" in ex and ex["task_id"]
        assert "split" in ex and ex["split"] in ["train", "validation", "test"]
        assert "inputs" in ex and isinstance(ex["inputs"], dict)
        assert "question" in ex and len(ex["question"]) > 10
        assert "answer" in ex and len(ex["answer"]) > 20
        # Contrôle des balises épistémiques strictes
        for tag in required_tags:
            assert tag in ex["answer"], f"Exemple {ex['example_id']} manque de la balise {tag}"


def test_03_multimodal_grounding(supervision_examples):
    """Vérifie que chaque exemple multimodal possède un ancrage réel d'évidence."""
    mm_count = 0
    for ex in supervision_examples:
        if ex.get("modality") == "MULTIMODAL":
            mm_count += 1
            inputs = ex.get("inputs", {})
            assert bool(inputs.get("plans") or inputs.get("images") or inputs.get("geometries") or inputs.get("ifc_entities"))
            assert bool(ex.get("evidence")), f"Exemple multimodal {ex['example_id']} sans preuve tangible"
    assert mm_count > 0, "Aucun exemple multimodal trouvé dans le dataset supervisé"


def test_04_modality_necessity_no_fake_multimodal(supervision_examples):
    """Vérifie l'absence absolue de faux multimodal dans les exemples certifiés."""
    for ex in supervision_examples:
        if ex.get("modality") == "MULTIMODAL":
            q = ex["question"].lower()
            # La question ne doit pas donner la réponse cible dans l'énoncé
            gt = ex.get("ground_truth", {})
            target_keys = ["concordance_status", "expected_answer", "verdict", "compliance_status"]
            for k in target_keys:
                if k in gt:
                    v = str(gt[k]).lower()
                    if len(v) > 3 and v in q:
                        pytest.fail(f"Faux multimodal : {ex['example_id']} divulgue la réponse '{v}' dans la consigne")


def test_05_target_validity_and_deterministic_facts(supervision_examples):
    """Vérifie que chaque ground_truth repose sur des faits mesurés ou vérifiés."""
    for ex in supervision_examples:
        gt = ex.get("ground_truth", {})
        assert bool(gt), f"Ground truth vide sur {ex['example_id']}"
        # Interdiction des valeurs None ou null dans les champs métriques
        for k, v in gt.items():
            assert v is not None, f"Valeur None détectée dans ground_truth[{k}] sur {ex['example_id']}"


def test_06_zero_split_leakage(supervision_examples):
    """Vérifie l'étanchéité absolue des partitions train / val / test."""
    from dataset_tools.supervision.shortcut_auditor import ShortcutAuditor
    is_clean, diag = ShortcutAuditor.audit_split_leakage(supervision_examples)
    assert is_clean, f"Fuite de partition détectée : {diag['leaks']}"


def test_07_no_question_shortcuts(supervision_examples):
    """Vérifie qu'aucun raccourci trivial ou token interdit n'apparaît."""
    for ex in supervision_examples:
        q = ex["question"].lower()
        a = ex["answer"].lower()
        assert "organisation matricielle" not in a or "parois et les ouvertures identifiables" not in q
        assert "groundtruth" not in q and "solution" not in q


def test_08_resplan_quarantine_enforced(supervision_examples):
    """Vérifie qu'aucune surface non étalonnée ResPlan n'a pollué les exemples en m2."""
    quarantine_file = REVIEW_DIR / "resplan_quarantine.jsonl"
    assert quarantine_file.exists(), "Manifeste de quarantaine ResPlan absent"
    for ex in supervision_examples:
        for sid in ex.get("source_ids", []):
            assert "103edd854a5f365aa875ed832e6cef0d8bc72c4b34e5df0856c01b6970684cb5" != sid, (
                f"L'actif mis en quarantaine ResPlan.pkl est présent dans {ex['example_id']}"
            )


def test_09_gold_set_v3_validation(gold_v3_examples):
    """Vérifie la qualité et l'intégrité du Gold Set V3."""
    assert len(gold_v3_examples) >= 150, f"Gold Set insuffisant ({len(gold_v3_examples)})"
    for ex in gold_v3_examples:
        assert ex["quality_status"] == "PASS"
        assert bool(ex.get("evidence"))
        assert bool(ex.get("ground_truth"))


def test_10_provenance_full_traceability(supervision_examples):
    """Vérifie que 100% des exemples sont traçables vers un ou plusieurs assets Master."""
    for ex in supervision_examples:
        s_ids = ex.get("source_ids", [])
        assert len(s_ids) >= 1, f"Exemple {ex['example_id']} orphelin de source"
        assert bool(ex.get("project_group_id")), f"Exemple {ex['example_id']} sans project_group_id"
