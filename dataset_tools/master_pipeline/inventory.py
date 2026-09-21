# -*- coding: utf-8 -*-
"""
ARCHI-AI — STEP 1: Forensic Inventory
=====================================
Établit un inventaire exhaustif, déterministe et reprenable (cache SQLite)
de chaque fichier physique présent dans dataset/raw/external/ (résolu via RAW_DIR, relatif à la racine du dépôt).
"""

import os
import sys
import json
import sqlite3
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Generator, Any

from .config import (
    RAW_DIR,
    CORE_RAW_DIR,
    MANIFEST_RAW,
    INVENTORY_CACHE,
    CACHE_DIR,
    HASH_CHUNK_SIZE,
    RAW_MANIFEST_PATH,
)
from .schema import RawAssetRecord, AssetCategory, AssetSubtype, LegalStatus, QualityStatus


def init_cache(cache_path: Path) -> sqlite3.Connection:
    """Initialise la table SQLite de cache d'inventaire optimisée WAL."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(cache_path))
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS file_cache (
            rel_path TEXT PRIMARY KEY,
            mtime REAL,
            size INTEGER,
            sha256 TEXT,
            mime TEXT
        )
    """)
    conn.commit()
    return conn


def compute_sha256(file_path: Path) -> str:
    """Calcul SHA-256 streaming par blocs de 1 Mo."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(HASH_CHUNK_SIZE):
            h.update(chunk)
    return h.hexdigest()


def detect_source_dataset(rel_path: Path) -> str:
    """Identifie la source officielle selon l'arborescence."""
    parts = rel_path.parts
    if not parts:
        return "ROOT"
    if parts[0] == "research_isolated":
        return "RESEARCH_ISOLATED"
    if parts[0] == "core" and len(parts) > 1:
        c1 = parts[1].lower()
        if c1 == "bim_ifc" and len(parts) > 2:
            sub = parts[2].lower()
            if "buildingsmart" in sub:
                return "CORE_BUILDINGSMART_IFC"
            elif "ifc_bench" in sub:
                return "CORE_IFC_BENCH"
            return "CORE_BIM_IFC"
        elif c1 == "design_history" and len(parts) > 2:
            sub = parts[2].lower()
            if "moma" in sub:
                return "CORE_MOMA_COLLECTION"
            elif "met" in sub:
                return "CORE_MET_OPENACCESS"
            return "CORE_DESIGN_HISTORY"
        elif c1 == "lighting" and len(parts) > 2:
            return "CORE_POLYHAVEN_LIGHTING"
        elif c1 == "materials" and len(parts) > 2:
            sub = parts[2].lower()
            if "polyhaven" in sub:
                return "CORE_POLYHAVEN_MATERIALS"
            elif "ambientcg" in sub:
                return "CORE_AMBIENTCG"
            return "CORE_MATERIALS"
        elif c1 == "multimodal_reasoning":
            return "CORE_MMMU_ARCHITECTURE"
        elif c1 == "resplan":
            return "CORE_RESPLAN"
        elif c1 == "rplan":
            return "CORE_RPLAN"
        elif c1 == "resbim":
            return "CORE_RESBIM_PAIRED"
        elif c1 == "il3d":
            return "CORE_IL3D"
        elif c1 == "structscan3d":
            return "CORE_STRUCTSCAN3D"
        elif c1 == "normes_fr":
            return "CORE_NORMES_FR"
        elif c1 == "ergonomie":
            return "CORE_ERGONOMIE"
        elif c1 == "trends":
            return "CORE_TRENDS_2026"
        elif c1 == "floorplancad":
            return "CORE_FLOORPLANCAD"
        return f"CORE_{c1.upper()}"
    return "UNKNOWN_SOURCE"


class ForensicInventory:
    """Scanne et produit l'inventaire unitaire du RAW."""

    def __init__(self, raw_root: Optional[Path] = None):
        self.raw_root = raw_root or RAW_DIR
        self.cache_conn = init_cache(INVENTORY_CACHE)

    def scan_all_files(self) -> List[Path]:
        """Collecte la liste exhaustive des fichiers récursifs sans altération."""
        file_list = []
        for root, _, files in os.walk(self.raw_root):
            for f in files:
                file_list.append(Path(root) / f)
        # Tri déterministe par chemin relatif
        file_list.sort(key=lambda p: str(p.relative_to(self.raw_root)))
        return file_list

    def process_file(self, file_path: Path) -> RawAssetRecord:
        """Traite un fichier unitaire en exploitant le cache pour performance et reprise."""
        rel_path = file_path.relative_to(self.raw_root)
        rel_str = str(rel_path).replace("\\", "/")
        stat = file_path.stat()
        mtime = stat.st_mtime
        size = stat.st_size

        # Vérification cache
        cur = self.cache_conn.cursor()
        cur.execute("SELECT sha256, mime FROM file_cache WHERE rel_path = ? AND mtime = ? AND size = ?",
                    (rel_str, mtime, size))
        row = cur.fetchone()

        if row:
            sha256, mime = row
        else:
            sha256 = compute_sha256(file_path)
            mime, _ = mimetypes.guess_type(file_path.name)
            mime = mime or "application/octet-stream"
            cur.execute("""
                INSERT OR REPLACE INTO file_cache (rel_path, mtime, size, sha256, mime)
                VALUES (?, ?, ?, ?, ?)
            """, (rel_str, mtime, size, sha256, mime))

        mtime_iso = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
        ext = file_path.suffix.lower()
        source = detect_source_dataset(rel_path)

        record = RawAssetRecord(
            asset_id=sha256,
            absolute_path=str(file_path.resolve()),
            relative_path=rel_str,
            filename=file_path.name,
            extension=ext,
            mime_type=mime,
            file_size_bytes=size,
            sha256=sha256,
            mtime_utc=mtime_iso,
            parent_dir=file_path.parent.name,
            source_dataset=source,
            category=AssetCategory.UNKNOWN,
            subtype=AssetSubtype.UNKNOWN,
            extraction_status="SUCCESS",
            parse_status="PENDING",
            quality_status=QualityStatus.REVIEW,
            provenance_status="VERIFIED",
            legal_status=LegalStatus.UNKNOWN,
            license="UNKNOWN",
            duplicate_group_id=None,
            canonical=False,
        )
        return record

    def run_inventory(self, progress_callback=None) -> Tuple[List[RawAssetRecord], Dict[str, Any]]:
        """Exécute l'inventaire complet et génère RAW_MANIFEST.jsonl."""
        files = self.scan_all_files()
        total_files = len(files)
        total_bytes = 0
        records: List[RawAssetRecord] = []
        zero_byte_files: List[str] = []
        sources_counts: Dict[str, int] = {}
        ext_counts: Dict[str, int] = {}

        MANIFEST_RAW.parent.mkdir(parents=True, exist_ok=True)
        with open(MANIFEST_RAW, "w", encoding="utf-8") as f_out:
            for idx, p in enumerate(files):
                rec = self.process_file(p)
                records.append(rec)
                total_bytes += rec.file_size_bytes

                if rec.file_size_bytes == 0:
                    zero_byte_files.append(rec.relative_path)

                sources_counts[rec.source_dataset] = sources_counts.get(rec.source_dataset, 0) + 1
                ext_counts[rec.extension] = ext_counts.get(rec.extension, 0) + 1

                # Écriture JSON Lines
                f_out.write(rec.model_dump_json() + "\n")

                if (idx + 1) % 2000 == 0:
                    self.cache_conn.commit()

                if progress_callback and (idx + 1) % 5000 == 0:
                    progress_callback(idx + 1, total_files)

        self.cache_conn.commit()

        summary = {
            "total_files": total_files,
            "total_size_bytes": total_bytes,
            "total_size_gb": round(total_bytes / (1024 ** 3), 4),
            "zero_byte_count": len(zero_byte_files),
            "zero_byte_files": zero_byte_files,
            "sources_count": len(sources_counts),
            "sources_distribution": sources_counts,
            "extensions_distribution": ext_counts,
            "manifest_path": str(MANIFEST_RAW),
        }
        return records, summary
