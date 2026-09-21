# -*- coding: utf-8 -*-
"""
test_independent_audit.py — Unit tests for the Independent Red-Team Audit Suite
==============================================================================
Tests the independent auditing algorithms without modifying any production datasets:
- Stratified sampling coverage
- Grounding claim breakdown & source ablation
- Specificity scoring & adversarial transfer detection
- Multimodal ablation & fake modal dependency detection
- 3D spatial coordinate recalculation & axis confusion detection
- Floorplan pixel-area anomaly detection
- L6 multi-constraint authenticity test
- Diversity & structural duplication detection
"""

import os
import sys
from pathlib import Path
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dataset_tools.supervision.independent_audit.sampling import AuditSampler
from dataset_tools.supervision.independent_audit.grounding_audit import GroundingAuditor
from dataset_tools.supervision.independent_audit.specificity_audit import SpecificityAuditor
from dataset_tools.supervision.independent_audit.multimodal_audit import MultimodalAuditor
from dataset_tools.supervision.independent_audit.reasoning_audit import ReasoningAuditor
from dataset_tools.supervision.independent_audit.difficulty_audit import DifficultyAuditor
from dataset_tools.supervision.independent_audit.diversity_audit import DiversityAuditor

BASE_DIR = Path(__file__).resolve().parent.parent


def test_sampling_stratification():
    sampler = AuditSampler(seed=42)
    wave1_path = BASE_DIR / "dataset" / "master" / "v1" / "supervision" / "wave1_repaired" / "wave1_dataset.jsonl"
    review_path = BASE_DIR / "dataset" / "master" / "v1" / "supervision" / "wave1_repaired" / "review_queue.jsonl"
    gold_v2_path = BASE_DIR / "dataset" / "master" / "v1" / "supervision" / "gold_set" / "v2" / "gold_set_v2.jsonl"

    res = sampler.sample_datasets(wave1_path, review_path, gold_v2_path, min_wave1_fraction=0.20)
    stats = res["strata_stats"]

    assert stats["total_wave1_sampled"] >= int(stats["total_wave1_available"] * 0.20)
    assert stats["wave1_warnings_sampled"] == stats["wave1_warnings_count"]
    assert stats["wave1_l6_sampled"] == stats["wave1_l6_count"]
    assert stats["gold_v2_sampled"] == stats["total_gold_v2"]
    assert stats["review_queue_sampled"] == stats["total_review_queue"]
    assert res["total_unique_audited"] > 200


def test_grounding_claims_and_ablation():
    auditor = GroundingAuditor()
    record = {
        "id": "TEST_GROUNDING_1",
        "task_type": "CLEARANCE_CHECK",
        "question": "Quelle est la largeur de couloir requise ?",
        "answer": (
            "**Observation factuelle :**\n"
            "La largeur minimale est de 0.90 m selon la norme.\n\n"
            "**Analyse spatiale :**\n"
            "Ces prescriptions imposent des gabarits incompressibles (passage utile minimal, ressaut de seuil ≤ 2 cm, cercle de giration Ø 1,50 m).\n\n"
            "**Raisonnement architectural :**\n"
            "En architecture intérieure, les contraintes réglementaires priment sur le choix esthétique et s'imposent à l'implantation générale."
        ),
        "inputs": {"text_contexts": [{"normalized_value": 0.9, "normalized_unit": "m"}]},
        "evidence": {"source": "Légifrance", "value_m": 0.9},
        "ground_truth": {"value_m": 0.9},
    }

    audit_res = auditor.audit_record_grounding(record)
    assert audit_res["total_claims"] >= 2
    assert audit_res["grounding_ratio"] > 0.0
    # The second paragraph is a generic filler -> should trigger ablation vulnerability
    assert audit_res["source_ablation"]["is_vulnerable_to_ablation"] is True


def test_specificity_auditor():
    auditor = SpecificityAuditor()
    # High specificity example
    high_spec_rec = {
        "answer": "La cloison IfcWallStandardCase (GUID: 2O2$TG2TX4G8) de 15 cm sépare le séjour (living, 24.5 m²) de la cuisine (kitchen, 12.0 m²) avec un passage libre de 0.90 m."
    }
    res_high = auditor.compute_specificity_score(high_spec_rec)
    assert res_high["score"] >= 0.50
    assert res_high["level"] == "HIGH_SPECIFICITY"

    # Generic boilerplate example
    boilerplate_rec = {
        "answer": "L'organisation actuelle sépare déjà clairement les pièces. La lecture croisée plan-programme arbitre l'adéquation entre l'enveloppe bâtie disponible et les modes de vie. Nécessite la vérification des cloisons abattables."
    }
    res_generic = auditor.compute_specificity_score(boilerplate_rec)
    assert res_generic["score"] < 0.40
    assert res_generic["level"] == "GENERIC_BOILERPLATE"


def test_multimodal_ablation_fake_detection():
    auditor = MultimodalAuditor()
    fake_record = {
        "id": "TEST_FAKE_MODAL",
        "task_type": "PLAN_PLUS_TEXT",
        "inputs": {
            "images": [],
            "plans": [],  # Empty plan!
            "geometries": [{"rooms": ["living", "bedroom"]}],
            "text_contexts": [{"program": "Famille 2 enfants"}],
        },
        "answer": "L'organisation actuelle sépare déjà clairement les pièces d'eau et de repos du séjour. Le télétravail peut être aménagé dans une chambre secondaire.",
    }
    res = auditor.audit_multimodal_record(fake_record)
    assert res["is_fake_modal"] is True
    assert "DEGRADED_PLAN_TO_VECTOR_GEOMETRY_ONLY" in res["flags"]


def test_reasoning_object_relation():
    auditor = ReasoningAuditor(coordinate_tolerance=0.05)
    # Authentic match: (0,0,0) and (1, 2, 2) -> dist = 3.0
    valid_rec = {
        "inputs": {
            "geometries": [{
                "objects": [
                    {"label": "table", "position": [0.0, 0.0, 0.0]},
                    {"label": "chair", "position": [1.0, 2.0, 2.0]},
                ]
            }]
        },
        "ground_truth": {"distance_m": 3.0, "delta_xyz": [1.0, 2.0, 2.0]},
        "answer": "L'élément 'chair' est situé à une distance euclidienne calculée de 3.00 m de 'table'.",
    }
    res_valid = auditor.audit_object_relation(valid_rec)
    assert res_valid["verdict"] == "PASS"
    assert res_valid["is_distance_match"] is True
    assert res_valid["recalculated_dist"] == 3.0

    # Mismatched claim
    bad_rec = {
        "inputs": {
            "geometries": [{
                "objects": [
                    {"label": "table", "position": [0.0, 0.0, 0.0]},
                    {"label": "chair", "position": [1.0, 2.0, 2.0]},
                ]
            }]
        },
        "ground_truth": {"distance_m": 1.20},  # False distance claim
        "answer": "Distance de 1.20 m",
    }
    res_bad = auditor.audit_object_relation(bad_rec)
    assert res_bad["verdict"] == "FAIL"
    assert res_bad["is_distance_match"] is False


def test_floorplan_pixel_area_anomaly():
    auditor = ReasoningAuditor()
    # Hallucinated pixel area labeled as m2
    bad_fp = {
        "task_type": "ROOM_IDENTIFICATION",
        "task_group": "B_FLOORPLAN",
        "inputs": {
            "geometries": [{"room_count": 10, "total_area_m2": 50336.89}]
        },
        "evidence": {
            "rooms": [{"name": "living", "area_m2": 18806.48}]
        },
        "answer": "Le plan comprend 10 pièces.",
    }
    res = auditor.audit_floorplan(bad_fp)
    assert res["verdict"] == "FAIL"
    assert res["has_pixel_as_m2_hallucination"] is True
    assert "PIXEL_COORDINATES_LABELED_AS_M2" in res["flags"]


def test_l6_authenticity():
    auditor = DifficultyAuditor()
    # Authentic L6
    auth_rec = {
        "difficulty": "L6_MULTICONTRAINTE",
        "constraints": [
            {"type": "acoustic", "target": "Rw >= 45dB"},
            {"type": "daylight", "target": "FLJ >= 2.0%"},
        ],
        "question": "Arbitrez la tension acoustique versus apport solaire.",
        "answer": "Un arbitrage s'impose : la mise en balance de l'isolation phonique et de la surface vitrée nécessite un compromis de double vitrage asymétrique.",
    }
    res_auth = auditor.l6_authenticity_test(auth_rec)
    assert res_auth["is_authentic"] is True
    assert res_auth["verdict"] == "L6_AUTHENTIC"

    # Inauthentic L6
    fake_rec = {
        "difficulty": "L6_MULTICONTRAINTE",
        "constraints": [],
        "question": "Décrivez la couleur des murs.",
        "answer": "Les murs sont peints en blanc cassé.",
    }
    res_fake = auditor.l6_authenticity_test(fake_rec)
    assert res_fake["is_authentic"] is False
    assert res_fake["verdict"] == "L6_INAUTHENTIC"


def test_diversity_auditor():
    auditor = DiversityAuditor(near_dup_threshold=0.80)
    records = [
        {"id": "A1", "question": "Q1", "answer": "L'organisation actuelle sépare déjà clairement les pièces.", "source_ids": ["S1"]},
        {"id": "A2", "question": "Q2", "answer": "L'organisation actuelle sépare déjà clairement les pièces.", "source_ids": ["S2"]},
        {"id": "A3", "question": "Q3", "answer": "L'organisation actuelle sépare déjà clairement les pièces.", "source_ids": ["S3"]},
        {"id": "A4", "question": "Q4", "answer": "Une réponse totalement distincte et originale sans aucun rapport.", "source_ids": ["S4"]},
    ]
    res = auditor.audit_diversity(records)
    assert res["exact_duplicate_answers"] >= 2
    assert res["structural_duplicate_examples"] >= 3
    assert res["unique_sources"] == 4
