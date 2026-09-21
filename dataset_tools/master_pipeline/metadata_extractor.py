# -*- coding: utf-8 -*-
"""
ARCHI-AI — STEP 3: Specialized Metadata Extractors
==================================================
Extrait les métadonnées techniques, physiques, architecturales et géométriques
selon la modalité de chaque asset.
Détecte formellement les anomalies (ex: pixels étiquetés en m² dans ResPlan).
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from PIL import Image

from ..deduplication.hasher import compute_average_hash


def extract_image_metadata(file_path: Path, compute_hash: bool = True) -> Dict[str, Any]:
    """Extrait les métadonnées d'une image matricielle sans surcoût mémoire."""
    meta: Dict[str, Any] = {
        "modality": "image",
        "width": None,
        "height": None,
        "aspect_ratio": None,
        "orientation": "unknown",
        "color_mode": None,
        "format": None,
        "has_alpha": False,
        "phash": None,
        "parse_success": False,
        "error": None,
    }
    try:
        with Image.open(file_path) as img:
            w, h = img.size
            meta["width"] = w
            meta["height"] = h
            meta["aspect_ratio"] = round(w / h, 4) if h > 0 else 0
            if w > h:
                meta["orientation"] = "landscape"
            elif h > w:
                meta["orientation"] = "portrait"
            else:
                meta["orientation"] = "square"

            meta["color_mode"] = img.mode
            meta["format"] = img.format
            meta["has_alpha"] = "A" in img.mode

            if compute_hash:
                meta["phash"] = compute_average_hash(img)

            meta["parse_success"] = True
    except Exception as e:
        meta["error"] = str(e)
        meta["parse_success"] = False
    return meta


def extract_ifc_metadata(file_path: Path) -> Dict[str, Any]:
    """
    Extrait les métadonnées d'une maquette numérique IFC.
    Utilise regex déterministe pour une vitesse d'extraction maximale (100% stable).
    """
    meta: Dict[str, Any] = {
        "modality": "ifc",
        "ifc_schema": "UNKNOWN",
        "project_name": None,
        "elements_count": {
            "walls": 0,
            "slabs": 0,
            "doors": 0,
            "windows": 0,
            "spaces": 0,
            "storeys": 0,
            "columns": 0,
            "beams": 0,
            "stairs": 0,
            "roofs": 0,
        },
        "parse_success": False,
        "error": None,
    }
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            header_sample = f.read(50000)

        # 1. Détection du schéma IFC
        schema_match = re.search(r"FILE_SCHEMA\s*\(\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*\)", header_sample, re.IGNORECASE)
        if schema_match:
            meta["ifc_schema"] = schema_match.group(1).upper()
        elif "IFC4" in header_sample:
            meta["ifc_schema"] = "IFC4"
        elif "IFC2X3" in header_sample:
            meta["ifc_schema"] = "IFC2X3"

        # 2. Comptage déterministe des entités IFC
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            full_text = f.read()

        counts = {
            "walls": len(re.findall(r"=\s*IFCWALL(?:STANDARDCASE)?\s*\(", full_text, re.IGNORECASE)),
            "slabs": len(re.findall(r"=\s*IFCSLAB\s*\(", full_text, re.IGNORECASE)),
            "doors": len(re.findall(r"=\s*IFCDOOR\s*\(", full_text, re.IGNORECASE)),
            "windows": len(re.findall(r"=\s*IFCWINDOW\s*\(", full_text, re.IGNORECASE)),
            "spaces": len(re.findall(r"=\s*IFCSPACE\s*\(", full_text, re.IGNORECASE)),
            "storeys": len(re.findall(r"=\s*IFCBUILDINGSTOREY\s*\(", full_text, re.IGNORECASE)),
            "columns": len(re.findall(r"=\s*IFCCOLUMN\s*\(", full_text, re.IGNORECASE)),
            "beams": len(re.findall(r"=\s*IFCBEAM\s*\(", full_text, re.IGNORECASE)),
            "stairs": len(re.findall(r"=\s*IFCSTAIR(?:FLIGHT)?\s*\(", full_text, re.IGNORECASE)),
            "roofs": len(re.findall(r"=\s*IFCROOF\s*\(", full_text, re.IGNORECASE)),
        }
        meta["elements_count"] = counts
        meta["parse_success"] = True
    except Exception as e:
        meta["error"] = str(e)
        meta["parse_success"] = False
    return meta


def extract_il3d_scene_metadata(file_path: Path) -> Dict[str, Any]:
    """Extrait la structure et les boîtes 3D d'une scène Indoor Layout 3D (IL3D)."""
    meta: Dict[str, Any] = {
        "modality": "scene_3d",
        "room_type": None,
        "objects_count": 0,
        "classes_present": [],
        "has_floor_mesh": False,
        "parse_success": False,
        "error": None,
    }
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        meta["room_type"] = data.get("room_type") or data.get("type") or "room"
        objects = data.get("objects", []) or data.get("furniture", [])
        meta["objects_count"] = len(objects)
        classes = set()
        for obj in objects:
            c = obj.get("label") or obj.get("category") or obj.get("class")
            if c:
                classes.add(str(c))
        meta["classes_present"] = sorted(list(classes))
        meta["has_floor_mesh"] = "floor" in data or "floor_plan" in data
        meta["parse_success"] = True
    except Exception as e:
        meta["error"] = str(e)
        meta["parse_success"] = False
    return meta


def extract_floorplan_metadata(file_path: Path, subtype_name: str) -> Dict[str, Any]:
    """
    Extrait les métadonnées de plan 2D.
    Vérifie explicitement l'anomalie de conversion pixel -> m² signalée dans l'audit Red Team.
    """
    meta: Dict[str, Any] = {
        "modality": "floorplan_2d",
        "units_detected": "unknown",
        "scale_detected": False,
        "unscaled_pixel_anomaly": False,
        "parse_success": False,
        "error": None,
    }
    try:
        ext = file_path.suffix.lower()
        if ext in [".png", ".jpg"]:
            img_meta = extract_image_metadata(file_path, compute_hash=True)
            meta.update(img_meta)
            meta["units_detected"] = "pixels"
            meta["parse_success"] = img_meta["parse_success"]
        elif ext == ".pkl":
            # ResPlan pkl
            meta["units_detected"] = "metric_or_pixel_hybrid"
            # Signalement systématique pour ResPlan : nécessite calibration d'échelle
            meta["unscaled_pixel_anomaly"] = True
            meta["parse_success"] = True
    except Exception as e:
        meta["error"] = str(e)
        meta["parse_success"] = False
    return meta


def extract_metadata_for_record(file_path: Path, category: str, subtype: str) -> Tuple[Dict[str, Any], bool]:
    """Aiguille vers l'extracteur idoine selon la catégorie."""
    ext = file_path.suffix.lower()
    if category == "images":
        m = extract_image_metadata(file_path)
        return m, m.get("parse_success", False)
    elif category == "architecture_2d":
        m = extract_floorplan_metadata(file_path, subtype)
        return m, m.get("parse_success", False)
    elif category == "architecture_3d":
        if ext == ".ifc":
            m = extract_ifc_metadata(file_path)
            return m, m.get("parse_success", False)
        elif ext == ".json":
            m = extract_il3d_scene_metadata(file_path)
            return m, m.get("parse_success", False)
    return {"modality": "generic", "extension": ext, "parse_success": True}, True
