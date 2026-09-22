"""
test_phase3_scientific_readiness.py — Comprehensive Scientific Readiness Test Suite
ARCHI-AI — Phase 3: Corpus Expansion & Scientific Readiness
"""

import os
import json
import pytest
from dataset_tools.pairing.pairing_detector import MultiLevelPairingDetector
from dataset_tools.resplan.resplan_forensic_auditor import ResPlanForensicAuditor


def _resolve_candidate_path(rel_parts):
    root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(root, *rel_parts)


@pytest.fixture(scope="module")
def core_dir():
    return _resolve_candidate_path(["dataset", "raw", "external", "core"])


@pytest.fixture(scope="module")
def pairing_audit(core_dir):
    detector = MultiLevelPairingDetector(core_dir)
    return detector.run_full_audit()


@pytest.fixture(scope="module")
def resplan_audit(core_dir):
    pkl_file = os.path.join(core_dir, "resplan", "extracted", "ResPlan.pkl")
    auditor = ResPlanForensicAuditor(pkl_file)
    auditor.load_data(max_samples=200)
    return auditor


# -------------------------------------------------------------
# 1. PAIRING TESTS
# -------------------------------------------------------------

def test_no_arbitrary_pairing(pairing_audit):
    """Verify that arbitrary / cross-dataset pairing without ground truth is strictly REJECTED."""
    rejected = pairing_audit["rejected_candidates"]
    assert len(rejected) > 0, "Expected rejected arbitrary pairing candidates to be tracked."
    for r in rejected:
        assert r["confidence"] == "REJECTED"
        assert r["validation_status"] == "REJECTED"


def test_pairing_confidence_consistency(pairing_audit):
    """Verify confidence levels: CERTIFIED pairs must be EXACT; never turn LOW into CERTIFIED."""
    for p in pairing_audit["resbim_pairs"]:
        assert p["confidence"] == "EXACT"
        assert p["validation_status"] == "CERTIFIED"
        assert len(p["match_methods"]) >= 1

    for p in pairing_audit["ifc_bench_pairs"]:
        assert p["confidence"] == "EXACT"
        assert p["validation_status"] == "CERTIFIED"
        assert len(p["match_methods"]) >= 1


def test_pairing_provenance_completeness(pairing_audit):
    """Verify that every certified pair has full provenance: paths, sha256, source IDs."""
    raw_ext = _resolve_candidate_path(["dataset", "raw", "external"])
    for p in pairing_audit["resbim_pairs"]:
        assert p["asset_a"]["sha256"] != ""
        assert p["asset_b"]["sha256"] != ""
        assert os.path.exists(os.path.join(raw_ext, p["asset_a"]["rel_path"]))
        assert os.path.exists(os.path.join(raw_ext, p["asset_b"]["rel_path"]))


def test_exact_count_of_floorplan_bim_pairs(pairing_audit):
    """Verify that exactly 10 2D floorplan to 3D BIM pairs exist in the current RAW corpus."""
    assert pairing_audit["summary"]["certified_2d_floorplan_3d_bim_pairs"] == 10
    assert pairing_audit["summary"]["new_2d_floorplan_3d_bim_pairs_in_raw"] == 0


# -------------------------------------------------------------
# 2. RESPLAN AUDIT & CALIBRATION TESTS
# -------------------------------------------------------------

def test_resplan_metric_calibration_fails(resplan_audit):
    """Verify that ResPlan metric calibration fails and is quarantined."""
    res = resplan_audit.audit_metric_calibration(sample_size=100)
    assert res["forensic_calibration_status"] == "FAIL"
    assert res["metric_supervision_decision"] == "QUARANTINED"
    assert res["canvas_normalization"]["is_strictly_normalized_to_256"] is True


def test_no_uncalibrated_metric_calculation_allowed(resplan_audit):
    """Verify that ratio std is high, proving absence of a deterministic scale factor."""
    res = resplan_audit.audit_metric_calibration(sample_size=100)
    assert res["scale_ratio_variance"]["is_deterministic_scale"] is False
    assert res["scale_ratio_variance"]["geom_area_over_gross_area_std"] > 10.0


def test_resplan_safe_capabilities_identified(resplan_audit):
    """Verify that non-metric safe capabilities are rigorously identified."""
    safe_info = resplan_audit.audit_safe_non_metric_capabilities(sample_size=50)
    caps = safe_info["safe_capabilities"]
    metric_caps = [c for c in caps if c["is_metric"]]
    non_metric_caps = [c for c in caps if not c["is_metric"]]

    assert len(non_metric_caps) >= 4
    for c in non_metric_caps:
        assert c["status"] == "VALID_SAFE"

    for c in metric_caps:
        assert c["status"] == "QUARANTINED_PROHIBITED"


@pytest.fixture(scope="module")
def sup_manifest():
    return _resolve_candidate_path(["dataset", "supervision", "v1", "manifests", "SUPERVISION_MANIFEST.jsonl"])


def test_resplan_not_in_supervision_metric_tasks(sup_manifest):
    """Verify that no ResPlan asset is used for metric calculation tasks in supervision v1."""
    with open(sup_manifest, "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            # PLAN_SUMMARY is invalid and was excluded from supervision
            assert d.get("task_id") != "PLAN_SUMMARY"
            # Ensure no ResPlan asset is used in supervision with m2 claims
            for inp_plan in d.get("inputs", {}).get("plans", []):
                assert "resplan" not in inp_plan.get("path", "").lower()


# -------------------------------------------------------------
# 3. MULTIMODAL INTEGRITY & NECESSITY TESTS
# -------------------------------------------------------------

def test_no_fake_multimodal_in_supervision(sup_manifest):
    """Verify that all MULTIMODAL examples in supervision v1 pass multimodal necessity (fake_multimodal == 0)."""
    multimodal_examples = []
    with open(sup_manifest, "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            if d.get("modality") == "MULTIMODAL":
                multimodal_examples.append(d)

    assert len(multimodal_examples) == 10
    for ex in multimodal_examples:
        assert ex["task_id"] == "BIM_PLUS_PLAN"
        assert "plans" in ex["inputs"]
        assert "ifc_entities" in ex["inputs"]
        assert len(ex["inputs"]["plans"]) > 0
        assert len(ex["inputs"]["ifc_entities"]) > 0


# -------------------------------------------------------------
# 4. LEAKAGE & SPLIT GROUPING TESTS
# -------------------------------------------------------------

def test_pairing_does_not_cross_splits(sup_manifest):
    """Verify that paired assets share the exact same project_group_id and are never split across train/val/test."""
    group_to_splits = {}
    with open(sup_manifest, "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            pg = d.get("project_group_id")
            s = d.get("split")
            if pg:
                group_to_splits.setdefault(pg, set()).add(s)

    for pg, splits in group_to_splits.items():
        assert len(splits) == 1, f"Data leakage detected! Project group {pg} crosses multiple splits: {splits}"


# -------------------------------------------------------------
# 5. SCIENTIFIC READINESS GATE PRECONDITIONS
# -------------------------------------------------------------

def test_floorplancad_remains_quarantined(sup_manifest):
    """Verify that FloorPlanCAD remains under LEGAL_REVIEW_REQUIRED and not in certified supervision."""
    with open(sup_manifest, "r", encoding="utf-8") as f:
        for line in f:
            text = line.lower()
            assert "floorplancad" not in text
