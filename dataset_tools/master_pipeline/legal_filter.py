# -*- coding: utf-8 -*-
"""
ARCHI-AI — STEP 6: Legal Filter & Restriction Isolation
========================================================
Isole formellement FloorPlanCAD (CC BY-NC 4.0) dans :
dataset/master/v2/restricted/legal_review/floorplancad/
Garantit qu'aucun élément restreint n'entre dans le Master CORE.
Produit RESTRICTED_MANIFEST.jsonl et le dossier juridique complet.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from .config import RESTRICTED_DIR, MANIFEST_RESTRICTED, LICENSE_PERMISSIONS
from .schema import RawAssetRecord, LegalStatus


class LegalFilter:
    """Filtre légal strict et ségrégation des licences non commerciales."""

    def __init__(self, restricted_root: Optional[Path] = None):
        self.restricted_root = restricted_root or (RESTRICTED_DIR / "legal_review" / "floorplancad")
        self.restricted_root.mkdir(parents=True, exist_ok=True)
        self.restricted_records: List[RawAssetRecord] = []
        self.approved_records: List[RawAssetRecord] = []

    def evaluate_asset_license(self, record: RawAssetRecord) -> LegalStatus:
        """Détermine le statut légal en fonction de la source et des termes."""
        source = record.source_dataset

        if source == "CORE_FLOORPLANCAD":
            record.license = "CC-BY-NC 4.0"
            record.legal_status = LegalStatus.LEGAL_REVIEW_REQUIRED
            return LegalStatus.LEGAL_REVIEW_REQUIRED

        # Sources libres approuvées
        if source in ["CORE_MOMA_COLLECTION", "CORE_MET_OPENACCESS", "CORE_POLYHAVEN_MATERIALS", "CORE_POLYHAVEN_LIGHTING", "CORE_AMBIENTCG", "CORE_ERGONOMIE"]:
            record.license = "CC0-1.0"
            record.legal_status = LegalStatus.APPROVED
            return LegalStatus.APPROVED

        if source in ["CORE_BUILDINGSMART_IFC", "CORE_STRUCTSCAN3D", "CORE_IFC_BENCH"]:
            record.license = "CC-BY-4.0"
            record.legal_status = LegalStatus.APPROVED
            return LegalStatus.APPROVED

        if source in ["CORE_RESPLAN"]:
            record.license = "CC BY 4.0 / MIT"
            record.legal_status = LegalStatus.APPROVED
            return LegalStatus.APPROVED

        if source in ["CORE_IL3D", "CORE_MMMU_ARCHITECTURE"]:
            record.license = "Apache-2.0"
            record.legal_status = LegalStatus.APPROVED
            return LegalStatus.APPROVED

        if source in ["CORE_RESBIM_PAIRED"]:
            record.license = "MIT"
            record.legal_status = LegalStatus.APPROVED
            return LegalStatus.APPROVED

        if source in ["CORE_NORMES_FR"]:
            record.license = "Licence Ouverte"
            record.legal_status = LegalStatus.APPROVED
            return LegalStatus.APPROVED

        if source in ["CORE_RPLAN"]:
            record.license = "Open Research"
            record.legal_status = LegalStatus.APPROVED
            return LegalStatus.APPROVED

        if source in ["CORE_TRENDS_2026"]:
            record.license = "Curation Interne"
            record.legal_status = LegalStatus.APPROVED
            return LegalStatus.APPROVED

        record.license = "UNKNOWN"
        record.legal_status = LegalStatus.UNKNOWN
        return LegalStatus.UNKNOWN

    def apply_filter(self, records: List[RawAssetRecord]) -> Tuple[List[RawAssetRecord], List[RawAssetRecord], Dict[str, Any]]:
        """Sépare strictement les assets approuvés des assets restreints."""
        self.approved_records = []
        self.restricted_records = []

        for r in records:
            st = self.evaluate_asset_license(r)
            if st in [LegalStatus.RESTRICTED, LegalStatus.LEGAL_REVIEW_REQUIRED, LegalStatus.PROHIBITED]:
                self.restricted_records.append(r)
            else:
                self.approved_records.append(r)

        # 1. Sauvegarde du manifest des données restreintes
        MANIFEST_RESTRICTED.parent.mkdir(parents=True, exist_ok=True)
        with open(MANIFEST_RESTRICTED, "w", encoding="utf-8") as f:
            for r in self.restricted_records:
                f.write(r.model_dump_json() + "\n")

        # 2. Génération du dossier juridique FloorPlanCAD
        dossier_path = self.restricted_root / "FLOORPLANCAD_LEGAL_DOSSIER.md"
        with open(dossier_path, "w", encoding="utf-8") as f_dossier:
            f_dossier.write(f"""# Dossier de Révision Juridique : FloorPlanCAD (`LEGAL_REVIEW_REQUIRED`)

> **Date d'évaluation :** 21 septembre 2026  
> **Statut formel :** `LEGAL_REVIEW_REQUIRED` (Ségrégation étanche)  
> **Nombre d'assets isolés :** {len(self.restricted_records)} fichiers  
> **Décision immédiate :** **EXCLUSION STRICTE DU MASTER DATASET CORE**

---

## 1. Motifs Juridiques
- **Licence d'origine :** Creative Commons Attribution-NonCommercial 4.0 International (`CC BY-NC 4.0`).
- **Clause bloquante :** Clause non-commerciale (`NC`) interdisant l'exploitation commerciale directe ou dérivée sans contrat d'exemption explicite.
- **Règle ARCHI-AI :** Aucun asset grevé d'une clause restrictive ne doit être incorporé silencieusement au dataset principal de pré-entraînement ou de fine-tuning.

---

## 2. Inventaire des Fichiers Isolés
- Répertoire RAW source : `dataset/raw/external/core/floorplancad/` (conservé intact et immuable).
- Répertoire de confinement : `dataset/master/v2/restricted/legal_review/floorplancad/`.
- Manifeste dédié : `dataset/master/v2/manifests/RESTRICTED_MANIFEST.jsonl`.

---

## 3. Conditions pour Réintégration Future
Pour qu'un asset FloorPlanCAD puisse quitter l'espace restreint :
1. Une analyse juridique écrite concluant à la compatibilité de l'usage prévu (ex: exemption recherche pure, fair use ou accord bilatéral).
2. Un avis conforme du Lead Juridique / Équipe ARCHI-AI.
3. Une mise à jour explicite du statut vers `APPROVED`.
""")

        stats = {
            "total_evaluated": len(records),
            "approved_count": len(self.approved_records),
            "restricted_count": len(self.restricted_records),
            "floorplancad_isolated_count": sum(1 for r in self.restricted_records if r.source_dataset == "CORE_FLOORPLANCAD"),
            "manifest_restricted_path": str(MANIFEST_RESTRICTED),
            "dossier_path": str(dossier_path),
            "hard_stop_check": "PASS" if len(self.restricted_records) > 0 and all(r.source_dataset != "CORE_FLOORPLANCAD" for r in self.approved_records) else "FAIL",
        }
        return self.approved_records, self.restricted_records, stats
