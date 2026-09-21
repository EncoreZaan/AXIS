"""
test_audit_raw_corpus.py — Unit and integration tests for RAW corpus forensic audit.
"""

import os
import sys
from pathlib import Path
import json
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dataset_tools.validation.audit_raw_corpus import (
    audit_corpus,
    verify_zip_integrity,
    classify_file,
    compute_sha256,
    RAW_DIR,
    CORE_DIR,
    MANIFEST_PATH,
)


@pytest.fixture(scope="module")
def audit_report():
    """Run the raw corpus audit once for the test module."""
    return audit_corpus(verify_all_hashes=False)


def test_audit_corpus_runs_successfully(audit_report):
    """Verify that the forensic audit function executes and returns comprehensive results."""
    assert audit_report is not None
    assert audit_report["total_files"] > 60000
    assert audit_report["total_size_bytes"] > 3 * 1024 * 1024 * 1024  # > 3 GB
    assert len(audit_report["archives"]) == 3
    assert all(a["is_valid"] for a in audit_report["archives"]), "All ZIP archives must be valid"


def test_archives_integrity():
    """Test every raw ZIP archive for corruption and validity."""
    archives = [
        CORE_DIR / "resplan" / "ResPlan.zip",
        CORE_DIR / "il3d" / "layout.zip",
        CORE_DIR / "rplan" / "rplan_dataset.zip",
    ]
    for arch in archives:
        assert arch.exists(), f"Archive {arch} must exist"
        is_valid, err, count = verify_zip_integrity(arch)
        assert is_valid is True, f"Archive {arch.name} failed integrity check: {err}"
        assert err is None
        assert count > 0


def test_zero_byte_files_isolation(audit_report):
    """Ensure zero-byte files are strictly restricted to huggingface cache/lock files."""
    zero_files = audit_report["zero_byte_files"]
    assert len(zero_files) > 0, "Expected lock/incomplete zero-byte cache files"
    for zf in zero_files:
        p_str = zf.lower()
        # Must be in .cache or be a lock/incomplete file
        assert (
            ".cache" in p_str or p_str.endswith(".lock") or p_str.endswith(".incomplete")
        ), f"Found non-temporary zero-byte file in data: {zf}"


def test_modality_counts_ground_truth(audit_report):
    """Verify ground truth counts for primary architectural modalities."""
    m = audit_report["modalities"]

    assert m["ifc_models"] == 95, "Expected exactly 95 IFC models"
    assert m["raster_images"] == 38179, "Expected 38,179 raster images on disk"
    assert m["total_floorplans"] == 32369, "Expected 32,369 floorplans"
    assert m["total_3d_scenes"] == 27911, "Expected 27,911 3D scenes (27,816 IL3D + 95 IFC)"
    assert m["total_expert_qa"] == 1612, "Expected 1,612 expert QA pairs"
    assert m["total_notices"] == 661589, "Expected 661,589 museum notices"
    assert m["total_materials"] == 3753, "Expected 3,753 materials cataloged"


def test_floorplancad_legal_flag(audit_report):
    """Ensure FloorPlanCAD is detected and flagged as LEGAL_REVIEW_REQUIRED due to NC clause."""
    sources = audit_report["sources"]
    assert "CORE_FLOORPLANCAD" in sources
    fpc_data = sources["CORE_FLOORPLANCAD"]
    assert fpc_data["legal_status"] == "LEGAL_REVIEW_REQUIRED"
    assert "noncommercial" in fpc_data["legal_notes"].lower()


def test_no_architectural_assets_in_cross_duplicates(audit_report):
    """Ensure cross-dataset duplicates contain no architectural models, plans, or images."""
    cross_dups = audit_report["duplicates"]["cross_dataset_items"]
    for dup in cross_dups:
        for f in dup["files"]:
            ext = Path(f).suffix.lower()
            assert ext not in [
                ".ifc",
                ".pkl",
                ".parquet",
                ".jsonl",
            ], f"Architectural file {f} duplicated across datasets"


def test_file_classification_validity(audit_report):
    """Verify that file classification categorizes the vast majority as USEFUL."""
    cls_summary = audit_report["file_classification"]
    useful_count = cls_summary["USEFUL"]["count"]
    total_count = audit_report["total_files"]
    useful_ratio = useful_count / total_count
    assert useful_ratio > 0.95, f"Expected >95% useful files, got {useful_ratio:.2%}"
