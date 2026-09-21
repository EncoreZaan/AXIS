# -*- coding: utf-8 -*-
"""
ARCHI-AI — Schémas Canoniques du Master Dataset (Pydantic v2)
============================================================
Définit les structures de données typées et validées pour toutes les étapes
du pipeline RAW -> MASTER DATASET.
"""

from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator


class AssetCategory(str, Enum):
    ARCHITECTURE_2D = "architecture_2d"
    ARCHITECTURE_3D = "architecture_3d"
    IMAGES = "images"
    TEXT = "text"
    METADATA = "metadata"
    CODE = "code"
    DOCUMENTATION = "documentation"
    TEMPORARY = "temporary"
    UNKNOWN = "unknown"


class AssetSubtype(str, Enum):
    # 2D
    FLOOR_PLAN = "floor_plan"
    SECTION = "section"
    ELEVATION = "elevation"
    TECHNICAL_DRAWING = "technical_drawing"
    DETAIL_DRAWING = "detail_drawing"
    DIAGRAM_2D = "diagram_2d"
    SKETCH = "sketch"

    # 3D
    BIM = "bim"
    IFC = "ifc"
    SCENE_3D = "scene_3d"
    MODEL = "model"
    OBJECT_3D = "object_3d"
    FURNITURE = "furniture"
    MATERIAL_PBR = "material_pbr"
    ENVIRONMENT = "environment"
    HDRI = "hdri"

    # Images
    INTERIOR = "interior"
    EXTERIOR = "exterior"
    FACADE = "facade"
    ARCHITECTURAL_PHOTOGRAPHY = "architectural_photography"
    PRODUCT_MATERIAL = "product_material"
    TEXTURE = "texture"
    DRAWING_SCAN = "drawing_scan"
    SCREENSHOT = "screenshot"

    # Text
    ARCHITECTURAL_DESCRIPTION = "architectural_description"
    SPECIFICATION = "specification"
    QA = "qa"
    DOCUMENTATION_TXT = "documentation"
    METADATA_TXT = "metadata"
    OCR = "ocr"

    UNKNOWN = "unknown"


class LegalStatus(str, Enum):
    APPROVED = "APPROVED"
    RESTRICTED = "RESTRICTED"
    LEGAL_REVIEW_REQUIRED = "LEGAL_REVIEW_REQUIRED"
    PROHIBITED = "PROHIBITED"
    UNKNOWN = "UNKNOWN"


class QualityStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    REVIEW = "REVIEW"
    FAIL = "FAIL"


class SplitType(str, Enum):
    TRAIN = "train"
    VALIDATION = "validation"
    TEST = "test"
    HOLDOUT = "holdout"


class RawAssetRecord(BaseModel):
    """Enregistrement unitaire d'un asset physique dans le RAW."""
    asset_id: str = Field(..., description="Hash SHA-256 déterministe du fichier")
    absolute_path: str = Field(..., description="Chemin absolu du fichier")
    relative_path: str = Field(..., description="Chemin relatif par rapport à dataset/raw/external/")
    filename: str = Field(..., description="Nom de base du fichier")
    extension: str = Field(..., description="Extension en minuscules avec point")
    mime_type: Optional[str] = Field(default=None, description="MIME type détecté")
    file_size_bytes: int = Field(..., description="Taille exacte en octets")
    sha256: str = Field(..., description="Empreinte SHA-256")
    mtime_utc: str = Field(..., description="Horodatage ISO de dernière modification")
    parent_dir: str = Field(..., description="Répertoire parent immédiat")
    source_dataset: str = Field(..., description="Identifiant officiel de la source")
    category: AssetCategory = Field(default=AssetCategory.UNKNOWN)
    subtype: AssetSubtype = Field(default=AssetSubtype.UNKNOWN)
    extraction_status: str = Field(default="PENDING")
    parse_status: str = Field(default="PENDING")
    quality_status: QualityStatus = Field(default=QualityStatus.REVIEW)
    provenance_status: str = Field(default="VERIFIED")
    legal_status: LegalStatus = Field(default=LegalStatus.UNKNOWN)
    license: str = Field(default="UNKNOWN")
    duplicate_group_id: Optional[str] = Field(default=None)
    canonical: bool = Field(default=False)
    phash: Optional[str] = Field(default=None)


class TransformationRecord(BaseModel):
    """Traçabilité formelle de chaque transformation appliquée."""
    source_asset_id: str
    target_asset_id: str
    operation: str
    tool_name: str
    tool_version: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    timestamp_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class QualityDimensions(BaseModel):
    visual_quality: float = Field(default=1.0, ge=0.0, le=1.0)
    structural_quality: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata_quality: float = Field(default=1.0, ge=0.0, le=1.0)
    semantic_quality: float = Field(default=1.0, ge=0.0, le=1.0)
    provenance_quality: float = Field(default=1.0, ge=0.0, le=1.0)
    legal_quality: float = Field(default=1.0, ge=0.0, le=1.0)
    duplication_quality: float = Field(default=1.0, ge=0.0, le=1.0)
    parse_quality: float = Field(default=1.0, ge=0.0, le=1.0)
    overall_quality_score: float = Field(default=1.0, ge=0.0, le=1.0)
    evaluation_notes: List[str] = Field(default_factory=list)


class ReviewQueueItem(BaseModel):
    """Élément consigné dans une file d'arbitrage."""
    queue_name: str
    asset_id: str
    source_path: str
    problem: str
    evidence: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    suggested_action: str
    current_status: str = Field(default="PENDING_REVIEW")
    timestamp_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CanonicalAssetRecord(BaseModel):
    """Enregistrement canonique officiel d'un asset pour le Master Dataset."""
    asset_id: str
    source_path: str
    sha256: str
    asset_type: str
    asset_subtype: str
    source_dataset: str
    license: str
    legal_status: LegalStatus
    quality_status: QualityStatus
    classification_status: str
    provenance_status: str
    duplicate_group_id: Optional[str] = None
    canonical: bool = False
    derived_from: List[str] = Field(default_factory=list)
    transformations: List[Dict[str, Any]] = Field(default_factory=list)
    project_group_id: Optional[str] = None
    quality_scores: Optional[QualityDimensions] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MasterExampleRecord(BaseModel):
    """Enregistrement canonique d'un exemple Master pour entraînement ou benchmark."""
    example_id: str
    source_assets: List[str] = Field(default_factory=list)
    project_group_id: str
    input: Dict[str, Any] = Field(default_factory=dict)
    target: Dict[str, Any] = Field(default_factory=dict)
    task: str
    difficulty: str
    quality: Dict[str, Any] = Field(default_factory=dict)
    provenance: Dict[str, Any] = Field(default_factory=dict)
    license: Dict[str, Any] = Field(default_factory=dict)
    split: SplitType = SplitType.TRAIN
    validation: Dict[str, Any] = Field(default_factory=dict)
