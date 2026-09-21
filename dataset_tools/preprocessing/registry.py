# -*- coding: utf-8 -*-
"""
ARCHI-AI — Registre des Préprocesseurs de Sources RAW
=====================================================
Permet la découverte, l'instanciation et l'exécution modulaire
de chaque préprocesseur par nom de source ou globalement (`--source all`).
"""

from typing import Dict, Type, List, Optional
from pathlib import Path

from dataset_tools.preprocessing.base import BasePreprocessor
from dataset_tools.preprocessing.floorplans.resplan_preprocessor import ResPlanPreprocessor
from dataset_tools.preprocessing.floorplans.rplan_preprocessor import RPlanPreprocessor
from dataset_tools.preprocessing.floorplans.resbim_2d_preprocessor import ResBim2DPreprocessor
from dataset_tools.preprocessing.floorplans.floorplancad_handler import FloorPlanCadFrozenHandler
from dataset_tools.preprocessing.spatial.il3d_preprocessor import IL3DPreprocessor
from dataset_tools.preprocessing.spatial.structscan3d_preprocessor import StructScan3DPreprocessor
from dataset_tools.preprocessing.bim.ifc_preprocessor import (
    BuildingSmartIfcPreprocessor,
    IfcBenchModelsPreprocessor,
    ResBimIfcPreprocessor
)
from dataset_tools.preprocessing.materials.materials_preprocessor import (
    PolyHavenMaterialsPreprocessor,
    AmbientCgPreprocessor
)
from dataset_tools.preprocessing.lighting.lighting_preprocessor import PolyHavenLightingPreprocessor
from dataset_tools.preprocessing.text.regulatory_preprocessor import RegulatoryPreprocessor
from dataset_tools.preprocessing.text.ergonomie_preprocessor import ErgonomiePreprocessor
from dataset_tools.preprocessing.text.museum_preprocessor import (
    MoMaCollectionPreprocessor,
    MetOpenAccessPreprocessor
)
from dataset_tools.preprocessing.text.trends_preprocessor import Trends2026Preprocessor
from dataset_tools.preprocessing.multimodal.ifc_bench_qa_preprocessor import IfcBenchQAPreprocessor
from dataset_tools.preprocessing.multimodal.mmmu_architecture_preprocessor import MmmuArchitecturePreprocessor


PREPROCESSOR_REGISTRY: Dict[str, Type[BasePreprocessor]] = {
    # Floorplans 2D
    "resplan": ResPlanPreprocessor,
    "rplan": RPlanPreprocessor,
    "resbim_2d": ResBim2DPreprocessor,
    "floorplancad": FloorPlanCadFrozenHandler,

    # Spatial 3D
    "il3d": IL3DPreprocessor,
    "structscan3d": StructScan3DPreprocessor,

    # BIM / IFC
    "buildingsmart": BuildingSmartIfcPreprocessor,
    "ifc_bench_models": IfcBenchModelsPreprocessor,
    "resbim_ifc": ResBimIfcPreprocessor,

    # Matériaux & Lumière
    "polyhaven_materials": PolyHavenMaterialsPreprocessor,
    "ambientcg": AmbientCgPreprocessor,
    "polyhaven_lighting": PolyHavenLightingPreprocessor,

    # Textes & Réglementation
    "normes_fr": RegulatoryPreprocessor,
    "ergonomie": ErgonomiePreprocessor,
    "moma": MoMaCollectionPreprocessor,
    "met": MetOpenAccessPreprocessor,
    "trends": Trends2026Preprocessor,

    # Multimodal & QA
    "ifc_bench_qa": IfcBenchQAPreprocessor,
    "mmmu": MmmuArchitecturePreprocessor,
}


def get_preprocessor_class(key: str) -> Optional[Type[BasePreprocessor]]:
    """Retourne la classe du préprocesseur associée à la clé."""
    return PREPROCESSOR_REGISTRY.get(key.lower())


def list_available_sources() -> List[str]:
    """Liste l'ensemble des clés sources enregistrées."""
    return sorted(list(PREPROCESSOR_REGISTRY.keys()))
