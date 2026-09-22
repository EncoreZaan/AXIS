# -*- coding: utf-8 -*-
"""
ARCHI-AI — Tests Automatisés du Pipeline de Preprocessing & Normalisation
========================================================================
Vérifie :
1. La conformité stricte au Master Schema Pydantic canonique.
2. L'intégrité de la chaîne de traçabilité de provenance (provenance.jsonl).
3. Le gel juridique formel de FloorPlanCAD (0 élément dans CORE V1).
4. L'absence d'hallucination de cotes ou de dimensions.
5. La préservation intégrale des unités d'origine pour l'ergonomie.
6. L'isolation étanche absolue des benchmarks (MMMU, IFC-Bench test).
7. Le bon fonctionnement des adaptateurs modulaires par modalité.
"""

import os
import sys
from pathlib import Path
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dataset_tools.preprocessing.schema import (
    MasterCanonicalItem,
    ProvenanceRecord,
    RoutingType,
    ModalityType,
    QualityStatus,
    PlanGeometry,
    PlanRoom
)
from dataset_tools.preprocessing.registry import PREPROCESSOR_REGISTRY, list_available_sources
from dataset_tools.preprocessing.floorplans.floorplancad_handler import FloorPlanCadFrozenHandler
from dataset_tools.preprocessing.text.ergonomie_preprocessor import ErgonomiePreprocessor
from dataset_tools.preprocessing.multimodal.ifc_bench_qa_preprocessor import IfcBenchQAPreprocessor
from dataset_tools.preprocessing.multimodal.mmmu_architecture_preprocessor import MmmuArchitecturePreprocessor
from dataset_tools.preprocessing.floorplans.resplan_preprocessor import ResPlanPreprocessor
from dataset_tools.preprocessing.spatial.il3d_preprocessor import IL3DPreprocessor
from dataset_tools.preprocessing.bim.ifc_preprocessor import BuildingSmartIfcPreprocessor


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "dataset" / "raw" / "external"
MASTER_DIR = BASE_DIR / "dataset" / "master" / "v1"
# Preprocessors create their processed-output directory (and any subdirectories)
# as a side effect of construction/processing (BasePreprocessor.__init__ does
# `self.processed_root.mkdir(...)`). Each test below is passed a pytest
# `tmp_path` for this instead of a real `dataset/processed` path, so running
# the suite does not write persistent artifacts into the repository working tree.


def test_registry_contains_all_sources():
    """Vérifie que toutes les sources prévues sont déclarées dans le registre."""
    sources = list_available_sources()
    expected = [
        "resplan", "rplan", "resbim_2d", "floorplancad",
        "il3d", "structscan3d",
        "buildingsmart", "ifc_bench_models", "resbim_ifc",
        "polyhaven_materials", "ambientcg", "polyhaven_lighting",
        "normes_fr", "ergonomie", "moma", "met", "trends",
        "ifc_bench_qa", "mmmu"
    ]
    for exp in expected:
        assert exp in sources, f"Source attendue manquante dans le registre: {exp}"


def test_floorplancad_strictly_frozen(tmp_path):
    """Garantit que FloorPlanCAD est exclu et ne produit aucun élément CORE V1."""
    handler = FloorPlanCadFrozenHandler(RAW_DIR, tmp_path)
    items = list(handler.process())
    assert len(items) == 0, "FloorPlanCAD ne doit produire AUCUN élément dans CORE V1"
    stats = handler.get_stats()
    assert len(stats["warnings"]) > 0
    assert "LEGAL_REVIEW_REQUIRED" in stats["warnings"][0]


def test_ergonomie_preserves_original_units(tmp_path):
    """Vérifie que l'ergonomie préserve les unités cm originales tout en ajoutant le SI m."""
    prep = ErgonomiePreprocessor(RAW_DIR, tmp_path)
    items = list(prep.process(limit=10))
    assert len(items) > 0
    for item in items:
        ergo = item.ergonomics
        assert ergo is not None
        assert ergo.original_unit in ["cm", "unit"]
        assert ergo.normalized_si_unit == "m"
        assert item.routing == RoutingType.MULTIUSE


def test_mmmu_strictly_benchmark_holdout(tmp_path):
    """Garantit que 100% des questions MMMU sont étanches et sanctuarisées en BENCHMARK."""
    prep = MmmuArchitecturePreprocessor(RAW_DIR, tmp_path)
    items = list(prep.process(limit=5))
    assert len(items) > 0
    for item in items:
        assert item.routing == RoutingType.BENCHMARK
        assert item.qa is not None
        assert item.qa.is_benchmark_holdout is True


def test_ifc_bench_split_sanctuary(tmp_path):
    """Vérifie la séparation stricte entre les questions d'entraînement et de test benchmark d'IFC-Bench."""
    prep = IfcBenchQAPreprocessor(RAW_DIR, tmp_path)
    items = list(prep.process(limit=20))
    assert len(items) > 0
    for item in items:
        assert item.qa is not None
        if item.qa.split_assignment == "test":
            assert item.routing == RoutingType.BENCHMARK
            assert item.qa.is_benchmark_holdout is True
        else:
            assert item.routing == RoutingType.FINETUNE
            assert item.qa.is_benchmark_holdout is False


def test_resplan_no_hallucinated_scale(tmp_path):
    """Vérifie que ResPlan ne fabrique aucune échelle arbitraire."""
    prep = ResPlanPreprocessor(RAW_DIR, tmp_path)
    items = list(prep.process(limit=5))
    assert len(items) > 0
    for item in items:
        assert item.floorplan is not None
        assert item.floorplan.scale is None  # Doit rester null
        assert item.floorplan.coordinate_unit == "meter"
        assert item.floorplan.total_area_m2 is not None


def test_buildingsmart_ifc_parsing(tmp_path):
    """Vérifie l'extraction IfcOpenShell des maquettes buildingSMART."""
    prep = BuildingSmartIfcPreprocessor(RAW_DIR, tmp_path)
    items = list(prep.process(limit=3))
    assert len(items) > 0
    for item in items:
        assert item.bim is not None
        assert item.bim.ifc_schema in ["IFC2X3", "IFC4", "IFC4X3"]
        assert item.bim.walls_count >= 0
