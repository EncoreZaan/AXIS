# -*- coding: utf-8 -*-
"""
ARCHI-AI — Provenance & Traceability Audit Module
================================================
Verifies end-to-end data provenance:
- Checks presence of required source_provenance fields.
- Verifies physical file existence on disk where available.
- Validates master_id and source_ids consistency.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple


class ProvenanceAuditor:
    """Independent auditor for provenance traceability."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def audit_provenance(self, record: Dict[str, Any]) -> Dict[str, Any]:
        prov = record.get("source_provenance")
        source_ids = record.get("source_ids", [])

        if not prov or not isinstance(prov, dict):
            return {
                "verdict": "FAIL_NO_PROVENANCE",
                "has_provenance": False,
                "missing_fields": ["source_provenance"],
            }

        required_fields = ["source_name", "raw_file", "transformation", "master_id"]
        missing = [f for f in required_fields if not prov.get(f)]

        # Check raw file path
        raw_rel = prov.get("raw_file")
        raw_exists = False
        if raw_rel:
            # Check relative to base_dir or raw data folders
            p1 = self.base_dir / raw_rel
            p2 = self.base_dir / "dataset" / "raw" / raw_rel
            p3 = self.base_dir / "dataset" / "core" / raw_rel
            raw_exists = p1.exists() or p2.exists() or p3.exists()

        # Consistency between master_id and source_ids
        master_id = prov.get("master_id")
        id_consistent = master_id in source_ids if (master_id and source_ids) else True

        has_issues = bool(missing) or not id_consistent
        verdict = "WARNING" if not raw_exists else ("FAIL" if missing else "PASS")

        return {
            "verdict": verdict,
            "has_provenance": True,
            "missing_fields": missing,
            "raw_file": raw_rel,
            "raw_file_exists_on_disk": raw_exists,
            "id_consistent": id_consistent,
        }
