# -*- coding: utf-8 -*-
"""
ARCHI-AI — STEP 5: Provenance Tracker & DAG Lineage
===================================================
Garantit la traçabilité intégrale de chaque dérivé jusqu'au RAW.
Aucune transformation opaque. Vérifie l'intégrité du graphe (zéro cycle).
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone

from .config import MANIFEST_TRANSFORMATION, PIPELINE_VERSION
from .schema import TransformationRecord


class ProvenanceTracker:
    """Gestionnaire de provenance et de lignage déterministe."""

    def __init__(self, manifest_path: Optional[Path] = None):
        self.manifest_path = manifest_path or MANIFEST_TRANSFORMATION
        self.transformations: List[TransformationRecord] = []
        self.edges: Dict[str, List[str]] = {}

    def record_transformation(
        self,
        source_id: str,
        target_id: str,
        operation: str,
        parameters: Optional[Dict[str, Any]] = None,
        tool_name: str = "archi_master_pipeline",
        tool_version: str = PIPELINE_VERSION,
    ) -> TransformationRecord:
        """Enregistre un événement de dérivation ou de normalisation."""
        rec = TransformationRecord(
            source_asset_id=source_id,
            target_asset_id=target_id,
            operation=operation,
            tool_name=tool_name,
            tool_version=tool_version,
            parameters=parameters or {},
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )
        self.transformations.append(rec)
        self.edges.setdefault(source_id, []).append(target_id)
        return rec

    def save_manifest(self) -> Path:
        """Sauvegarde les enregistrements dans TRANSFORMATION_MANIFEST.jsonl."""
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            for t in self.transformations:
                f.write(t.model_dump_json() + "\n")
        return self.manifest_path

    def verify_dag_integrity(self) -> Tuple[bool, Optional[str]]:
        """Vérifie l'absence de cycles (DAG valide) par parcours en profondeur."""
        visited = set()
        recursion_stack = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            recursion_stack.add(node)
            for neighbor in self.edges.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in recursion_stack:
                    return True
            recursion_stack.remove(node)
            return False

        for node in list(self.edges.keys()):
            if node not in visited:
                if dfs(node):
                    return False, f"Cycle de provenance détecté impliquant {node}"
        return True, None
