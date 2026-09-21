# -*- coding: utf-8 -*-
"""
tests/test_master_pipeline.py — Tests unitaires et d'intégration du Master Pipeline v0.2.0
"""

import pytest
from pathlib import Path

from dataset_tools.master_pipeline.config import RAW_DIR, CORE_RAW_DIR
from dataset_tools.master_pipeline.schema import (
    RawAssetRecord,
    AssetCategory,
    AssetSubtype,
    LegalStatus,
    QualityStatus,
)
from dataset_tools.master_pipeline.classification import classify_asset
from dataset_tools.master_pipeline.metadata_extractor import (
    extract_image_metadata,
    extract_ifc_metadata,
    extract_floorplan_metadata,
)
from dataset_tools.master_pipeline.deduplicator import MultiLevelDeduplicator
from dataset_tools.master_pipeline.legal_filter import LegalFilter
from dataset_tools.master_pipeline.quality_scorer import QualityScorer
from dataset_tools.master_pipeline.provenance_tracker import ProvenanceTracker
from dataset_tools.master_pipeline.split_manager import DeterministicSplitter, extract_project_group_id
from dataset_tools.master_pipeline.canonicalizer import build_canonical_record


def test_classify_asset_deterministic():
    """Vérifie la précision de la taxonomie déterministe."""
    rec_ifc = RawAssetRecord(
        asset_id="dummy_ifc",
        absolute_path="dummy/path/model.ifc",
        relative_path="core/bim_ifc/buildingsmart/model.ifc",
        filename="model.ifc",
        extension=".ifc",
        file_size_bytes=1000,
        sha256="dummy_ifc",
        mtime_utc="2026-09-21T00:00:00Z",
        parent_dir="buildingsmart",
        source_dataset="CORE_BUILDINGSMART_IFC",
    )
    cat, sub, status = classify_asset(rec_ifc)
    assert cat == AssetCategory.ARCHITECTURE_3D
    assert sub == AssetSubtype.IFC
    assert status == "CLASSIFIED_DETERMINISTIC"


def test_legal_filter_floorplancad():
    """Garantit que FloorPlanCAD (CC BY-NC 4.0) est obligatoirement filtré."""
    rec_fpc = RawAssetRecord(
        asset_id="dummy_fpc",
        absolute_path="dummy/path/001.png",
        relative_path="core/floorplancad/001.png",
        filename="001.png",
        extension=".png",
        file_size_bytes=2000,
        sha256="dummy_fpc",
        mtime_utc="2026-09-21T00:00:00Z",
        parent_dir="floorplancad",
        source_dataset="CORE_FLOORPLANCAD",
    )
    lf = LegalFilter()
    app, rest, stats = lf.apply_filter([rec_fpc])
    assert len(rest) == 1
    assert len(app) == 0
    assert rest[0].legal_status == LegalStatus.LEGAL_REVIEW_REQUIRED
    assert stats["hard_stop_check"] == "PASS"


def test_provenance_dag_integrity():
    """Vérifie la détection de cycles et l'intégrité acyclique du DAG."""
    pt = ProvenanceTracker()
    pt.record_transformation("A", "B", "norm")
    pt.record_transformation("B", "C", "norm")
    is_dag, err = pt.verify_dag_integrity()
    assert is_dag is True
    assert err is None

    # Injection d'un cycle
    pt.record_transformation("C", "A", "cycle_bug")
    is_dag_corrupt, err_corrupt = pt.verify_dag_integrity()
    assert is_dag_corrupt is False
    assert "Cycle" in str(err_corrupt)


def test_quality_scorer_dimensions():
    """Vérifie que les 8 dimensions qualité sont calculées de façon explicable."""
    rec = RawAssetRecord(
        asset_id="dummy_rec",
        absolute_path="dummy/path/plan.png",
        relative_path="core/rplan/plan.png",
        filename="plan.png",
        extension=".png",
        file_size_bytes=50000,
        sha256="dummy_rec",
        mtime_utc="2026-09-21T00:00:00Z",
        parent_dir="rplan",
        source_dataset="CORE_RPLAN",
        category=AssetCategory.ARCHITECTURE_2D,
        subtype=AssetSubtype.FLOOR_PLAN,
        legal_status=LegalStatus.APPROVED,
        canonical=True,
    )
    meta = {"width": 1024, "height": 1024, "parse_success": True}
    qs = QualityScorer()
    scores = qs.score_asset(rec, meta)

    assert scores.visual_quality == 1.0
    assert scores.legal_quality == 1.0
    assert scores.duplication_quality == 1.0
    assert scores.overall_quality_score >= 0.85
    assert qs.determine_status(scores) == QualityStatus.PASS


def test_split_deterministic_anti_leakage():
    """Vérifie l'étanchéité absolue du découpage par project_group_id."""
    splitter = DeterministicSplitter(seed=42)

    c1 = build_canonical_record(
        raw_record=RawAssetRecord(
            asset_id="asset_1",
            absolute_path="dummy",
            relative_path="core/ifc_bench/projects/P1/model.ifc",
            filename="model.ifc",
            extension=".ifc",
            file_size_bytes=10,
            sha256="h1",
            mtime_utc="",
            parent_dir="",
            source_dataset="CORE_IFC_BENCH",
            legal_status=LegalStatus.APPROVED,
            canonical=True,
        ),
        metadata={},
        quality_scores=None,
        transformations=[],
        project_group_id="PROJECT_P1",
    )
    c2 = build_canonical_record(
        raw_record=RawAssetRecord(
            asset_id="asset_2",
            absolute_path="dummy",
            relative_path="core/ifc_bench/projects/P1/drawing.png",
            filename="drawing.png",
            extension=".png",
            file_size_bytes=10,
            sha256="h2",
            mtime_utc="",
            parent_dir="",
            source_dataset="CORE_IFC_BENCH",
            legal_status=LegalStatus.APPROVED,
            canonical=True,
        ),
        metadata={},
        quality_scores=None,
        transformations=[],
        project_group_id="PROJECT_P1",
    )

    splits, stats = splitter.partition_records([c1, c2])
    assert stats["leakage_test_passed"] is True
    # c1 et c2 doivent impérativement être dans la même partition !
    assigned_splits = [s for s, group in splits.items() if len(group) > 0]
    assert len(assigned_splits) == 1
    assert len(splits[assigned_splits[0]]) == 2
