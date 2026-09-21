"""
Unit tests for ARCHI-AI Raw Dataset Acquisition & Isolation
"""

import json
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_EXTERNAL_DIR = BASE_DIR / "dataset" / "raw" / "external"
CORE_DIR = RAW_EXTERNAL_DIR / "core"
MANIFEST_PATH = RAW_EXTERNAL_DIR / "ACQUISITION_MANIFEST.json"


def test_manifest_exists_and_valid():
    assert MANIFEST_PATH.exists(), "ACQUISITION_MANIFEST.json must exist"
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert "records" in manifest
    assert len(manifest["records"]) >= 14, "At least 14 core datasets should be registered"
    assert manifest["total_size_bytes"] > 100 * 1024 * 1024, "Total size should exceed 100 MB"


def test_core_datasets_exist():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    for key, record in manifest["records"].items():
        rel_path = record.get("local_path", "")
        abs_path = BASE_DIR / rel_path
        assert abs_path.exists(), f"Path for {key} does not exist: {abs_path}"


def test_legal_isolation_integrity():
    """Ensure no tainted or non-commercial files infiltrated the core pool."""
    tainted = ["cubicasa", "archcad", "structured3d", "interiornet", "suncg"]
    for p in CORE_DIR.rglob("*"):
        for word in tainted:
            assert word not in p.name.lower(), f"Tainted source '{word}' found in CORE: {p}"


def test_raw_archives_preserved():
    """Ensure immutable archives (ZIP) are preserved alongside extractions."""
    resplan_zip = CORE_DIR / "resplan" / "ResPlan.zip"
    assert resplan_zip.exists(), "Original ResPlan.zip must be preserved"
    assert resplan_zip.stat().st_size > 90 * 1024 * 1024

    il3d_zip = CORE_DIR / "il3d" / "layout.zip"
    assert il3d_zip.exists(), "Original IL3D layout.zip must be preserved"
    assert il3d_zip.stat().st_size > 40 * 1024 * 1024
