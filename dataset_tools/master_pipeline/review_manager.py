# -*- coding: utf-8 -*-
"""
ARCHI-AI — STEP 9: Review Queues Manager
========================================
Gère les 8 files d'attente d'arbitrage :
1. REVIEW_CLASSIFICATION
2. REVIEW_LICENSE
3. REVIEW_DUPLICATE
4. REVIEW_OCR
5. REVIEW_PLAN_TYPE
6. REVIEW_IFC
7. REVIEW_QUALITY
8. REVIEW_PROVENANCE

Génère REVIEW_MANIFEST.jsonl et les fichiers JSONL par file.
"""

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

from .config import REVIEW_DIR, MANIFEST_REVIEW
from .schema import ReviewQueueItem


class ReviewQueueManager:
    """Gestionnaire des files de révision humaine et IA."""

    QUEUES = [
        "REVIEW_CLASSIFICATION",
        "REVIEW_LICENSE",
        "REVIEW_DUPLICATE",
        "REVIEW_OCR",
        "REVIEW_PLAN_TYPE",
        "REVIEW_IFC",
        "REVIEW_QUALITY",
        "REVIEW_PROVENANCE",
    ]

    def __init__(self, review_root: Optional[Path] = None):
        self.review_root = review_root or REVIEW_DIR
        self.review_root.mkdir(parents=True, exist_ok=True)
        self.items: Dict[str, List[ReviewQueueItem]] = {q: [] for q in self.QUEUES}

    def add_to_queue(
        self,
        queue_name: str,
        asset_id: str,
        source_path: str,
        problem: str,
        evidence: Optional[Dict[str, Any]] = None,
        confidence: float = 0.5,
        suggested_action: str = "MANUAL_REVIEW_REQUIRED",
    ) -> ReviewQueueItem:
        """Ajoute une entrée typée dans une file d'arbitrage."""
        if queue_name not in self.items:
            self.items[queue_name] = []

        item = ReviewQueueItem(
            queue_name=queue_name,
            asset_id=asset_id,
            source_path=source_path,
            problem=problem,
            evidence=evidence or {},
            confidence=confidence,
            suggested_action=suggested_action,
            current_status="PENDING_REVIEW",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )
        self.items[queue_name].append(item)
        return item

    def save_all_queues(self) -> Dict[str, Any]:
        """Sauvegarde les 8 files individuelles et le REVIEW_MANIFEST.jsonl global."""
        total_items = 0
        queue_counts = {}

        MANIFEST_REVIEW.parent.mkdir(parents=True, exist_ok=True)
        with open(MANIFEST_REVIEW, "w", encoding="utf-8") as f_manifest:
            for q_name, items in self.items.items():
                queue_file = self.review_root / f"{q_name}.jsonl"
                with open(queue_file, "w", encoding="utf-8") as f_q:
                    for it in items:
                        line = it.model_dump_json()
                        f_q.write(line + "\n")
                        f_manifest.write(line + "\n")
                queue_counts[q_name] = len(items)
                total_items += len(items)

        return {
            "total_review_items": total_items,
            "queue_counts": queue_counts,
            "manifest_review_path": str(MANIFEST_REVIEW),
        }
