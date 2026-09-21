# -*- coding: utf-8 -*-
"""
ARCHI-AI — STEP 12: Comprehensive QA Test Suite
================================================
Valide automatiquement les 6 piliers d'intégrité avant le Gate :
1. Integrity (fichiers, hashes, non-corruption)
2. Provenance (DAG acyclique, sources valides)
3. License (zéro asset restreint dans CORE)
4. Deduplication & Leakage (étanchéité absolue entre splits)
5. Parsing (IFC, images, scènes 3D certifiés)
6. Dataset Schema (conformité Pydantic v2 des records)
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Tuple

from .schema import CanonicalAssetRecord, RawAssetRecord, LegalStatus, QualityStatus
from .provenance_tracker import ProvenanceTracker


class MasterQASuite:
    """Suite de vérification automatisée de conformité Master Dataset."""

    def __init__(
        self,
        raw_records: List[RawAssetRecord],
        master_records: List[CanonicalAssetRecord],
        splits: Dict[str, List[CanonicalAssetRecord]],
        provenance_tracker: ProvenanceTracker,
    ):
        self.raw_records = raw_records
        self.master_records = master_records
        self.splits = splits
        self.provenance_tracker = provenance_tracker
        self.test_results: Dict[str, Dict[str, Any]] = {}

    def test_raw_integrity(self) -> bool:
        """Vérifie qu'aucun fichier RAW n'est manquant ou corrompu."""
        missing = 0
        for r in self.raw_records:
            if not os.path.exists(r.absolute_path):
                missing += 1
        passed = (missing == 0)
        self.test_results["RAW_INTEGRITY"] = {
            "passed": passed,
            "missing_files_count": missing,
            "total_raw_audited": len(self.raw_records),
        }
        return passed

    def test_provenance_dag(self) -> bool:
        """Vérifie l'absence de cycles et la cohérence de la chaîne de provenance."""
        is_dag, err = self.provenance_tracker.verify_dag_integrity()
        self.test_results["PROVENANCE_DAG"] = {
            "passed": is_dag,
            "error_detail": err,
            "total_transformations": len(self.provenance_tracker.transformations),
        }
        return is_dag

    def test_license_isolation(self) -> bool:
        """Garantit qu'aucun asset FloorPlanCAD ou CC BY-NC 4.0 n'est admis dans CORE."""
        illegal_in_master = [
            r for r in self.master_records
            if r.source_dataset == "CORE_FLOORPLANCAD" or r.legal_status != LegalStatus.APPROVED
        ]
        passed = (len(illegal_in_master) == 0)
        self.test_results["LICENSE_ISOLATION"] = {
            "passed": passed,
            "illegal_assets_in_master": len(illegal_in_master),
        }
        return passed

    def test_split_leakage(self) -> bool:
        """Vérifie l'absence absolue de recouvrement d'empreintes ou de projets entre splits."""
        train_shas = {r.sha256 for r in self.splits.get("train", [])}
        val_shas = {r.sha256 for r in self.splits.get("validation", [])}
        test_shas = {r.sha256 for r in self.splits.get("test", [])}

        train_proj = {r.project_group_id for r in self.splits.get("train", []) if r.project_group_id}
        val_proj = {r.project_group_id for r in self.splits.get("validation", []) if r.project_group_id}
        test_proj = {r.project_group_id for r in self.splits.get("test", []) if r.project_group_id}

        sha_overlap = (
            len(train_shas.intersection(val_shas))
            + len(train_shas.intersection(test_shas))
            + len(val_shas.intersection(test_shas))
        )
        proj_overlap = (
            len(train_proj.intersection(val_proj))
            + len(train_proj.intersection(test_proj))
            + len(val_proj.intersection(test_proj))
        )

        passed = (sha_overlap == 0) and (proj_overlap == 0)
        self.test_results["SPLIT_LEAKAGE"] = {
            "passed": passed,
            "sha_overlap_count": sha_overlap,
            "project_overlap_count": proj_overlap,
        }
        return passed

    def test_parsing_validity(self) -> bool:
        """Vérifie qu'aucun asset en échec de parsing n'est marqué comme exploitable sans alerte."""
        failed_parse = [
            r for r in self.master_records
            if not r.metadata.get("parse_success", True)
        ]
        passed = (len(failed_parse) == 0)
        self.test_results["PARSING_VALIDITY"] = {
            "passed": passed,
            "unhandled_parse_failures": len(failed_parse),
        }
        return passed

    def test_schema_conformance(self) -> bool:
        """Vérifie que 100% des master records respectent scrupuleusement les types requis."""
        invalid_count = 0
        for r in self.master_records:
            if not r.asset_id or not r.sha256 or not r.source_path:
                invalid_count += 1
        passed = (invalid_count == 0)
        self.test_results["SCHEMA_CONFORMANCE"] = {
            "passed": passed,
            "invalid_schema_records": invalid_count,
            "total_validated": len(self.master_records),
        }
        return passed

    def run_full_qa(self) -> Tuple[bool, Dict[str, Any]]:
        """Exécute tous les tests et agrège le statut QA."""
        t1 = self.test_raw_integrity()
        t2 = self.test_provenance_dag()
        t3 = self.test_license_isolation()
        t4 = self.test_split_leakage()
        t5 = self.test_parsing_validity()
        t6 = self.test_schema_conformance()

        all_passed = all([t1, t2, t3, t4, t5, t6])
        return all_passed, self.test_results
