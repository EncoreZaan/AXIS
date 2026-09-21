# -*- coding: utf-8 -*-
"""
ARCHI-AI — Master Pipeline Configuration
=========================================
Centralise les chemins, seuils, constantes et schémas du pipeline Master Dataset v0.2.0.
"""

from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "dataset" / "raw" / "external"
CORE_RAW_DIR = RAW_DIR / "core"
RAW_MANIFEST_PATH = RAW_DIR / "ACQUISITION_MANIFEST.json"

# Sorties Master v2
MASTER_V2_DIR = BASE_DIR / "dataset" / "master" / "v2"
ASSETS_DIR = MASTER_V2_DIR / "assets"
IMAGES_DIR = MASTER_V2_DIR / "images"
PLANS_DIR = MASTER_V2_DIR / "plans"
IFC_DIR = MASTER_V2_DIR / "ifc"
SCENES_DIR = MASTER_V2_DIR / "scenes"
MATERIALS_DIR = MASTER_V2_DIR / "materials"
TEXT_DIR = MASTER_V2_DIR / "text"
QA_DIR = MASTER_V2_DIR / "qa"
METADATA_DIR = MASTER_V2_DIR / "metadata"
PROVENANCE_DIR = MASTER_V2_DIR / "provenance"
MANIFESTS_DIR = MASTER_V2_DIR / "manifests"
REPORTS_DIR = MASTER_V2_DIR / "reports"
RESTRICTED_DIR = MASTER_V2_DIR / "restricted"
REVIEW_DIR = MASTER_V2_DIR / "review"
SPLITS_DIR = MASTER_V2_DIR / "splits"

# Manifestes
MANIFEST_RAW = MANIFESTS_DIR / "RAW_MANIFEST.jsonl"
MANIFEST_MASTER = MANIFESTS_DIR / "MASTER_MANIFEST.jsonl"
MANIFEST_REVIEW = MANIFESTS_DIR / "REVIEW_MANIFEST.jsonl"
MANIFEST_RESTRICTED = MANIFESTS_DIR / "RESTRICTED_MANIFEST.jsonl"
MANIFEST_SPLIT = MANIFESTS_DIR / "SPLIT_MANIFEST.jsonl"
MANIFEST_TRANSFORMATION = MANIFESTS_DIR / "TRANSFORMATION_MANIFEST.jsonl"
PIPELINE_RUN_MANIFEST = MANIFESTS_DIR / "PIPELINE_RUN_MANIFEST.json"

# Cache intermédiaire pour reprise (checkpoint)
CACHE_DIR = MASTER_V2_DIR / ".cache"
INVENTORY_CACHE = CACHE_DIR / "inventory_cache.sqlite"

# Paramètres généraux
PIPELINE_VERSION = "v0.2.0-master"
RANDOM_SEED = 42
HASH_CHUNK_SIZE = 1024 * 1024  # 1 Mo streaming

# Seuils Déduplication
HAMMING_NEAR_DUP_THRESHOLD = 5

# Seuils Qualité
QUALITY_PASS_THRESHOLD = 0.80
QUALITY_CRITICAL_DIM_MIN = 0.65

# Ratios de splits
SPLIT_RATIOS = {
    "train": 0.80,
    "validation": 0.10,
    "test": 0.10,
}

# Licences reconnues et autorisations
LICENSE_PERMISSIONS = {
    "CC0-1.0": {"commercial": True, "derivative": True, "attribution": False, "status": "APPROVED"},
    "CC0-1.0 Factual": {"commercial": True, "derivative": True, "attribution": False, "status": "APPROVED"},
    "CC-BY-4.0": {"commercial": True, "derivative": True, "attribution": True, "status": "APPROVED"},
    "CC BY 4.0 / MIT": {"commercial": True, "derivative": True, "attribution": True, "status": "APPROVED"},
    "Apache-2.0": {"commercial": True, "derivative": True, "attribution": True, "status": "APPROVED"},
    "MIT": {"commercial": True, "derivative": True, "attribution": True, "status": "APPROVED"},
    "Licence Ouverte": {"commercial": True, "derivative": True, "attribution": True, "status": "APPROVED"},
    "Open Research": {"commercial": True, "derivative": True, "attribution": True, "status": "APPROVED"},
    "Propriété ARCHI-AI": {"commercial": True, "derivative": True, "attribution": False, "status": "APPROVED"},
    "Curation Interne": {"commercial": True, "derivative": True, "attribution": False, "status": "APPROVED"},
    "CC-BY-NC 4.0": {"commercial": False, "derivative": True, "attribution": True, "status": "RESTRICTED"},
}
