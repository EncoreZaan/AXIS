# -*- coding: utf-8 -*-
"""
ARCHI-AI — STEP 10: Master Dataset Assembly Engine
==================================================
Assemble le Master Dataset intermédiaire en filtrant :
- Les données juridiquement restreintes (ex: FloorPlanCAD CC BY-NC 4.0).
- Les doublons secondaires (seul le représentant canonique est admis).
- Les données en statut de rejet ou avec échec critique.
Émet MASTER_MANIFEST.jsonl et indexe les répertoires par modalité.
"""

from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from .config import (
    MASTER_V2_DIR,
    MANIFEST_MASTER,
    ASSETS_DIR,
    IMAGES_DIR,
    PLANS_DIR,
    IFC_DIR,
    SCENES_DIR,
    MATERIALS_DIR,
    TEXT_DIR,
    QA_DIR,
)
from .schema import CanonicalAssetRecord, QualityStatus, LegalStatus


class MasterDatasetBuilder:
    """Assembleur final du Master Dataset Intermédiaire v2."""

    def __init__(self, master_dir: Optional[Path] = None):
        self.master_dir = master_dir or MASTER_V2_DIR
        self.ensure_directories()

    def ensure_directories(self):
        """Crée l'architecture complète des répertoires du Master Dataset."""
        dirs = [
            self.master_dir,
            ASSETS_DIR,
            IMAGES_DIR,
            PLANS_DIR,
            IFC_DIR,
            SCENES_DIR,
            MATERIALS_DIR,
            TEXT_DIR,
            QA_DIR,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    def assemble_master(
        self, canonical_records: List[CanonicalAssetRecord]
    ) -> Tuple[List[CanonicalAssetRecord], List[CanonicalAssetRecord], Dict[str, Any]]:
        """
        Sélectionne les éléments validés pour le Master Dataset.
        Retourne (master_records, rejected_records, stats).
        """
        master_records: List[CanonicalAssetRecord] = []
        rejected_records: List[CanonicalAssetRecord] = []
        exclusion_reasons: Dict[str, int] = {}

        for r in canonical_records:
            # 1. Filtre Légal Absolu
            if r.legal_status != LegalStatus.APPROVED:
                rejected_records.append(r)
                exclusion_reasons["RESTRICTED_LICENSE"] = exclusion_reasons.get("RESTRICTED_LICENSE", 0) + 1
                continue

            # 2. Filtre Doublon : Seul le canonique est admis
            if not r.canonical:
                rejected_records.append(r)
                exclusion_reasons["SECONDARY_DUPLICATE"] = exclusion_reasons.get("SECONDARY_DUPLICATE", 0) + 1
                continue

            # 3. Filtre Qualité
            if r.quality_status == QualityStatus.FAIL:
                rejected_records.append(r)
                exclusion_reasons["QUALITY_FAIL"] = exclusion_reasons.get("QUALITY_FAIL", 0) + 1
                continue

            # 4. Filtre d'intégrité
            if r.quality_scores and r.quality_scores.overall_quality_score < 0.65:
                rejected_records.append(r)
                exclusion_reasons["LOW_OVERALL_SCORE"] = exclusion_reasons.get("LOW_OVERALL_SCORE", 0) + 1
                continue

            master_records.append(r)

        # Sauvegarde du MASTER_MANIFEST.jsonl
        MANIFEST_MASTER.parent.mkdir(parents=True, exist_ok=True)
        modalities_distribution = {}
        with open(MANIFEST_MASTER, "w", encoding="utf-8") as f_master:
            for r in master_records:
                f_master.write(r.model_dump_json() + "\n")
                modalities_distribution[r.asset_type] = modalities_distribution.get(r.asset_type, 0) + 1

        stats = {
            "total_candidates": len(canonical_records),
            "master_admitted_count": len(master_records),
            "master_rejected_count": len(rejected_records),
            "exclusion_reasons": exclusion_reasons,
            "modalities_distribution": modalities_distribution,
            "manifest_master_path": str(MANIFEST_MASTER),
        }
        return master_records, rejected_records, stats
