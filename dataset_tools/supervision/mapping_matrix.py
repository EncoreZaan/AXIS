# -*- coding: utf-8 -*-
"""
ARCHI-AI — Matrice Source → Compétence → Tâches (Mapping Matrix V1)
===================================================================
Définit la matrice canonique qui lie chaque source du Master Dataset
à ses capacités spécifiques et aux types de tâches éligibles,
en assignant la destination cognitive appropriée (FINETUNE, RAG, TOOL, etc.).
"""

from typing import Dict, List, Any, Optional
from .schema import RoutingDestination
from .task_catalogue import TASK_CATALOGUE


# Matrice officielle : source_name -> spécifications de capacités et tâches
SOURCE_CAPABILITY_TASK_MATRIX: Dict[str, Dict[str, Any]] = {
    "CORE_RESPLAN": {
        "modality": "floorplan_2d",
        "primary_destination": RoutingDestination.MULTIUSE,
        "capabilities": ["plan_reading", "topology", "circulation", "ergonomics", "critique"],
        "eligible_tasks": [
            "FLOORPLAN_READING",
            "ROOM_IDENTIFICATION",
            "ROOM_TOPOLOGY",
            "CIRCULATION_ANALYSIS",
            "DOOR_WINDOW_ANALYSIS",
            "FURNITURE_LAYOUT_ANALYSIS",
            "PLAN_ERROR_DETECTION",
            "PLAN_SUMMARY",
            "PLAN_TO_TEXT",
            "CLEARANCE_CHECK",
            "PROJECT_CRITIQUE",
            "WEAKNESS_IDENTIFICATION",
            "IMPROVEMENT_PROPOSAL",
            "GUIDED_REASONING",
        ],
        "default_difficulty": "L3_ANALYSE",
    },
    "CORE_RPLAN": {
        "modality": "floorplan_2d",
        "primary_destination": RoutingDestination.FINETUNE,
        "capabilities": ["plan_reading", "room_identification", "circulation"],
        "eligible_tasks": [
            "FLOORPLAN_READING",
            "ROOM_IDENTIFICATION",
            "ROOM_TOPOLOGY",
            "CIRCULATION_ANALYSIS",
            "DOOR_WINDOW_ANALYSIS",
            "PLAN_SUMMARY",
        ],
        "default_difficulty": "L2_COMPREHENSION",
    },
    "CORE_RESBIM_2D": {
        "modality": "floorplan_2d",
        "primary_destination": RoutingDestination.MULTIUSE,
        "capabilities": ["plan_reading", "topology", "paired_3d"],
        "eligible_tasks": [
            "FLOORPLAN_READING",
            "ROOM_TOPOLOGY",
            "PLAN_PLUS_3D",
            "BIM_PLUS_PLAN",
            "CIRCULATION_ANALYSIS",
        ],
        "default_difficulty": "L4_RAISONNEMENT",
    },
    "CORE_RESBIM_IFC": {
        "modality": "bim_ifc",
        "primary_destination": RoutingDestination.MULTIUSE,
        "capabilities": ["bim_reasoning", "ifc_entities", "paired_2d"],
        "eligible_tasks": [
            "IFC_ENTITY_IDENTIFICATION",
            "BIM_SPATIAL_HIERARCHY",
            "PLAN_PLUS_3D",
            "BIM_PLUS_PLAN",
            "BIM_REASONING",
        ],
        "default_difficulty": "L4_RAISONNEMENT",
    },
    "CORE_IL3D": {
        "modality": "spatial_3d",
        "primary_destination": RoutingDestination.FINETUNE,
        "capabilities": ["spatial_reasoning", "scene_graphs", "furniture_layout", "3d_relations"],
        "eligible_tasks": [
            "SCENE_GRAPH_REASONING",
            "OBJECT_RELATION",
            "ROOM_OBJECT_REASONING",
            "SPATIAL_LAYOUT_ANALYSIS",
            "3D_TO_TEXT",
            "FURNITURE_IDENTIFICATION",
            "SPATIAL_RELATION_ANALYSIS",
        ],
        "default_difficulty": "L3_ANALYSE",
    },
    "CORE_STRUCTSCAN3D": {
        "modality": "spatial_3d",
        "primary_destination": RoutingDestination.FINETUNE,
        "capabilities": ["visual_reasoning", "depth_analysis", "interior_analysis"],
        "eligible_tasks": [
            "IMAGE_ANALYSIS",
            "INTERIOR_ANALYSIS",
            "SPATIAL_RELATION_ANALYSIS",
            "SPATIAL_LAYOUT_ANALYSIS",
        ],
        "default_difficulty": "L2_COMPREHENSION",
    },
    "CORE_BUILDINGSMART": {
        "modality": "bim_ifc",
        "primary_destination": RoutingDestination.TOOL,
        "capabilities": ["ifc_entities", "ifc_properties", "spatial_hierarchy"],
        "eligible_tasks": [
            "IFC_ENTITY_IDENTIFICATION",
            "IFC_PROPERTY_REASONING",
            "BIM_SPATIAL_HIERARCHY",
            "BIM_OBJECT_QUERY",
        ],
        "default_difficulty": "L3_ANALYSE",
    },
    "CORE_IFC_BENCH_MODELS": {
        "modality": "bim_ifc",
        "primary_destination": RoutingDestination.MULTIUSE,
        "capabilities": ["bim_reasoning", "spatial_hierarchy", "ifc_qa"],
        "eligible_tasks": [
            "IFC_ENTITY_IDENTIFICATION",
            "BIM_SPATIAL_HIERARCHY",
            "BIM_REASONING",
            "IFC_QA",
        ],
        "default_difficulty": "L4_RAISONNEMENT",
    },
    "CORE_IFC_BENCH_QA": {
        "modality": "multimodal_qa",
        "primary_destination": RoutingDestination.MULTIUSE,
        "capabilities": ["ifc_qa", "bim_reasoning"],
        "eligible_tasks": [
            "IFC_QA",
            "BIM_REASONING",
        ],
        "default_difficulty": "L3_ANALYSE",
    },
    "CORE_MMMU_ARCHITECTURE": {
        "modality": "multimodal_qa",
        "primary_destination": RoutingDestination.BENCHMARK,
        "capabilities": ["academic_benchmark_evaluation"],
        "eligible_tasks": [
            "IMAGE_ANALYSIS",
            "ARCHITECTURE_HISTORY",
            "DESIGN_DECISION",
        ],
        "default_difficulty": "L5_EXPERT",
    },
    "CORE_AMBIENTCG": {
        "modality": "material_pbr",
        "primary_destination": RoutingDestination.MULTIUSE,
        "capabilities": ["materials", "pbr_reasoning", "tactile_perception"],
        "eligible_tasks": [
            "MATERIAL_ANALYSIS",
            "MATERIAL_COMPARISON",
            "MATERIAL_APPLICATION",
            "PBR_REASONING",
        ],
        "default_difficulty": "L2_COMPREHENSION",
    },
    "CORE_POLYHAVEN_MATERIALS": {
        "modality": "material_pbr",
        "primary_destination": RoutingDestination.MULTIUSE,
        "capabilities": ["materials", "pbr_reasoning", "scale_reasoning"],
        "eligible_tasks": [
            "MATERIAL_ANALYSIS",
            "MATERIAL_COMPARISON",
            "MATERIAL_APPLICATION",
            "PBR_REASONING",
        ],
        "default_difficulty": "L3_ANALYSE",
    },
    "CORE_POLYHAVEN_LIGHTING": {
        "modality": "lighting_hdri",
        "primary_destination": RoutingDestination.FINETUNE,
        "capabilities": ["lighting", "daylight", "kelvin_photometry"],
        "eligible_tasks": [
            "LIGHTING_ANALYSIS",
            "LIGHTING_SCENARIO",
            "DAYLIGHT_REASONING",
            "ARTIFICIAL_LIGHTING_REASONING",
        ],
        "default_difficulty": "L3_ANALYSE",
    },
    "CORE_ERGONOMIE": {
        "modality": "ergonomics",
        "primary_destination": RoutingDestination.TOOL,
        "capabilities": ["ergonomics", "clearances", "anthropometry", "accessibility"],
        "eligible_tasks": [
            "ERGONOMIC_ANALYSIS",
            "CLEARANCE_CHECK",
            "CIRCULATION_CHECK",
            "FURNITURE_DIMENSION_REASONING",
            "ACCESSIBILITY_ANALYSIS",
        ],
        "default_difficulty": "L4_RAISONNEMENT",
    },
    "CORE_NORMES_FR": {
        "modality": "regulatory_text",
        "primary_destination": RoutingDestination.RAG,
        "capabilities": ["accessibility_pmr", "fire_safety_erp", "habitability_cch"],
        "eligible_tasks": [
            "ACCESSIBILITY_ANALYSIS",
            "CONSTRAINT_REASONING",
            "FEASIBILITY_ANALYSIS",
        ],
        "default_difficulty": "L5_EXPERT",
    },
    "CORE_MOMA": {
        "modality": "historical_design",
        "primary_destination": RoutingDestination.RAG,
        "capabilities": ["design_history", "modern_movement", "iconic_furniture"],
        "eligible_tasks": [
            "DESIGN_HISTORY",
            "ARCHITECTURE_HISTORY",
            "STYLE_CLASSIFICATION",
            "STYLE_COMPARISON",
            "MATERIAL_AND_STYLE_RELATION",
        ],
        "default_difficulty": "L2_COMPREHENSION",
    },
    "CORE_MET": {
        "modality": "historical_design",
        "primary_destination": RoutingDestination.RAG,
        "capabilities": ["woodwork", "decorative_arts", "period_furniture"],
        "eligible_tasks": [
            "DESIGN_HISTORY",
            "ARCHITECTURE_HISTORY",
            "STYLE_CLASSIFICATION",
            "MATERIAL_AND_STYLE_RELATION",
        ],
        "default_difficulty": "L2_COMPREHENSION",
    },
    "CORE_FLOORPLANCAD": {
        "modality": "floorplan_2d",
        "primary_destination": RoutingDestination.HOLDOUT,
        "capabilities": ["frozen_legal_review"],
        "eligible_tasks": [],
        "default_difficulty": "L1_RECONNAISSANCE",
    },
    "CORE_TRENDS": {
        "modality": "trends",
        "primary_destination": RoutingDestination.RAG,
        "capabilities": ["contemporary_trends", "color_palettes"],
        "eligible_tasks": [
            "STYLE_CLASSIFICATION",
            "STYLE_ANALYSIS",
        ],
        "default_difficulty": "L2_COMPREHENSION",
    },
}

# Alias pour correspondre aux identifiants exacts du Master Dataset
SOURCE_CAPABILITY_TASK_MATRIX["CORE_BUILDINGSMART_IFC"] = SOURCE_CAPABILITY_TASK_MATRIX["CORE_BUILDINGSMART"]
SOURCE_CAPABILITY_TASK_MATRIX["CORE_MOMA_COLLECTION"] = SOURCE_CAPABILITY_TASK_MATRIX["CORE_MOMA"]
SOURCE_CAPABILITY_TASK_MATRIX["CORE_MET_OPENACCESS"] = SOURCE_CAPABILITY_TASK_MATRIX["CORE_MET"]
SOURCE_CAPABILITY_TASK_MATRIX["CORE_RESBIM_PAIRED"] = SOURCE_CAPABILITY_TASK_MATRIX["CORE_RESBIM_2D"]
SOURCE_CAPABILITY_TASK_MATRIX["CORE_TRENDS_2026"] = SOURCE_CAPABILITY_TASK_MATRIX["CORE_TRENDS"]



def resolve_tasks_for_record(record: Dict[str, Any]) -> List[str]:
    """
    Détermine les types de tâches éligibles pour un item du Master Dataset.
    Ne force jamais un item à devenir un exemple de fine-tuning.
    """
    source_name = record.get("source_name", "")
    entry = SOURCE_CAPABILITY_TASK_MATRIX.get(source_name)
    if not entry:
        return []
    
    # Si la source est gelée ou marquée SKIP/HOLDOUT
    if entry["primary_destination"] in (RoutingDestination.HOLDOUT, RoutingDestination.SKIP):
        return []
        
    return entry["eligible_tasks"]
