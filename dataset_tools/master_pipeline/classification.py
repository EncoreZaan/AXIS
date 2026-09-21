# -*- coding: utf-8 -*-
"""
ARCHI-AI — STEP 2: Asset Classification & Taxonomy
===================================================
Applique la taxonomie hiérarchique à 4 branches (2D, 3D, Images, Text).
Principe : Déterministe lorsque possible -> Review Queue lorsque ambigu.
Ne force JAMAIS une classification incertaine.
"""

from pathlib import Path
from typing import Tuple, Optional
from .schema import RawAssetRecord, AssetCategory, AssetSubtype, QualityStatus


def classify_asset(record: RawAssetRecord) -> Tuple[AssetCategory, AssetSubtype, str]:
    """
    Classifie un asset selon sa source, son extension, son chemin et son contenu.
    Retourne (category, subtype, classification_status).
    """
    ext = record.extension.lower()
    rel = record.relative_path.lower()
    filename = record.filename.lower()
    source = record.source_dataset

    # 1. Fichiers temporaires ou git/cache (Hors périmètre d'entraînement)
    if (
        ".git" in rel
        or ".cache" in rel
        or ext in [".lock", ".incomplete", ".tmp"]
        or "cachedir.tag" in filename
    ):
        return AssetCategory.TEMPORARY, AssetSubtype.UNKNOWN, "CLASSIFIED_DETERMINISTIC"

    # 2. Code source et scripts
    if ext in [".py", ".sh", ".bat", ".cmd"]:
        return AssetCategory.CODE, AssetSubtype.UNKNOWN, "CLASSIFIED_DETERMINISTIC"

    # 3. Documentation pure
    if ext in [".md", ".rst"] and "normes_fr" not in rel:
        return AssetCategory.DOCUMENTATION, AssetSubtype.DOCUMENTATION_TXT, "CLASSIFIED_DETERMINISTIC"

    # 4. Architecture 3D & BIM
    if ext == ".ifc":
        return AssetCategory.ARCHITECTURE_3D, AssetSubtype.IFC, "CLASSIFIED_DETERMINISTIC"

    if source == "CORE_IL3D":
        if ext == ".json" and "extracted/layout/" in rel:
            return AssetCategory.ARCHITECTURE_3D, AssetSubtype.SCENE_3D, "CLASSIFIED_DETERMINISTIC"
        if filename in ["assets.json", "labels.json"]:
            return AssetCategory.TEXT, AssetSubtype.METADATA_TXT, "CLASSIFIED_DETERMINISTIC"

    if source == "CORE_STRUCTSCAN3D":
        if ext == ".jpg":
            return AssetCategory.IMAGES, AssetSubtype.INTERIOR, "CLASSIFIED_DETERMINISTIC"
        if ext == ".png":
            return AssetCategory.IMAGES, AssetSubtype.TEXTURE, "CLASSIFIED_DETERMINISTIC"
        if ext == ".txt":
            return AssetCategory.TEXT, AssetSubtype.METADATA_TXT, "CLASSIFIED_DETERMINISTIC"

    # 5. Architecture 2D (Plans)
    if source == "CORE_RESPLAN":
        if ext == ".pkl":
            return AssetCategory.ARCHITECTURE_2D, AssetSubtype.FLOOR_PLAN, "CLASSIFIED_DETERMINISTIC"

    if source == "CORE_RPLAN":
        if ext == ".png":
            return AssetCategory.ARCHITECTURE_2D, AssetSubtype.FLOOR_PLAN, "CLASSIFIED_DETERMINISTIC"
        if ext == ".jsonl":
            return AssetCategory.TEXT, AssetSubtype.METADATA_TXT, "CLASSIFIED_DETERMINISTIC"

    if source == "CORE_RESBIM_PAIRED":
        if ext in [".jpg", ".png"]:
            return AssetCategory.ARCHITECTURE_2D, AssetSubtype.FLOOR_PLAN, "CLASSIFIED_DETERMINISTIC"
        if ext == ".ifc":
            return AssetCategory.ARCHITECTURE_3D, AssetSubtype.IFC, "CLASSIFIED_DETERMINISTIC"

    if source == "CORE_FLOORPLANCAD":
        if ext == ".png":
            return AssetCategory.ARCHITECTURE_2D, AssetSubtype.TECHNICAL_DRAWING, "CLASSIFIED_DETERMINISTIC"

    # 6. Matériaux & Éclairage (PBR & HDRI)
    if source in ["CORE_POLYHAVEN_MATERIALS", "CORE_AMBIENTCG"]:
        if ext == ".json":
            return AssetCategory.ARCHITECTURE_3D, AssetSubtype.MATERIAL_PBR, "CLASSIFIED_DETERMINISTIC"
        if ext in [".png", ".jpg"]:
            return AssetCategory.IMAGES, AssetSubtype.PRODUCT_MATERIAL, "CLASSIFIED_DETERMINISTIC"

    if source == "CORE_POLYHAVEN_LIGHTING":
        if ext == ".json":
            return AssetCategory.ARCHITECTURE_3D, AssetSubtype.HDRI, "CLASSIFIED_DETERMINISTIC"
        if ext in [".png", ".jpg"]:
            return AssetCategory.IMAGES, AssetSubtype.PRODUCT_MATERIAL, "CLASSIFIED_DETERMINISTIC"

    # 7. Textes réglementaires & Ergonomie
    if source == "CORE_NORMES_FR":
        return AssetCategory.TEXT, AssetSubtype.SPECIFICATION, "CLASSIFIED_DETERMINISTIC"

    if source == "CORE_ERGONOMIE":
        return AssetCategory.TEXT, AssetSubtype.SPECIFICATION, "CLASSIFIED_DETERMINISTIC"

    if source == "CORE_TRENDS_2026":
        return AssetCategory.TEXT, AssetSubtype.ARCHITECTURAL_DESCRIPTION, "CLASSIFIED_DETERMINISTIC"

    # 8. QA et Benchmark
    if source == "CORE_IFC_BENCH":
        if ext == ".csv" and "qa" in filename:
            return AssetCategory.TEXT, AssetSubtype.QA, "CLASSIFIED_DETERMINISTIC"
        if ext == ".pdf":
            return AssetCategory.TEXT, AssetSubtype.DOCUMENTATION_TXT, "CLASSIFIED_DETERMINISTIC"
        if ext in [".xlsx", ".xls"]:
            return AssetCategory.TEXT, AssetSubtype.SPECIFICATION, "CLASSIFIED_DETERMINISTIC"
        if ext == ".png":
            return AssetCategory.IMAGES, AssetSubtype.SCREENSHOT, "CLASSIFIED_DETERMINISTIC"
        if ext == ".ifc":
            return AssetCategory.ARCHITECTURE_3D, AssetSubtype.IFC, "CLASSIFIED_DETERMINISTIC"

    if source == "CORE_MMMU_ARCHITECTURE":
        if ext == ".parquet":
            return AssetCategory.TEXT, AssetSubtype.QA, "CLASSIFIED_DETERMINISTIC"

    # 9. Collections & Musées (MoMA, Met)
    if source in ["CORE_MOMA_COLLECTION", "CORE_MET_OPENACCESS"]:
        if ext == ".csv":
            return AssetCategory.TEXT, AssetSubtype.METADATA_TXT, "CLASSIFIED_DETERMINISTIC"

    # 10. Archives zip
    if ext == ".zip":
        return AssetCategory.METADATA, AssetSubtype.UNKNOWN, "CLASSIFIED_DETERMINISTIC"

    # Cas non résolu avec certitude -> REVIEW_CLASSIFICATION
    return AssetCategory.UNKNOWN, AssetSubtype.UNKNOWN, "REVIEW_REQUIRED"
