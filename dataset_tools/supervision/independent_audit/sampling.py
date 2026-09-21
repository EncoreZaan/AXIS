# -*- coding: utf-8 -*-
"""
ARCHI-AI — Sampling Module for Independent Audit
================================================
Deterministic, stratified sampling ensuring rigorous coverage across:
- 100% of Gold Set V2 (73 examples)
- 100% of Wave 1 Repaired WARNINGs (33 examples)
- 100% of Wave 1 Repaired Review Queue (21 examples)
- 100% of L6 Multicontrainte examples (50 examples)
- 100% of Multimodal tasks (PLAN_PLUS_3D, IMAGE_PLUS_TEXT, PLAN_PLUS_TEXT, MULTIMODAL_PROJECT_REASONING, etc.)
- 100% of Critical tasks:
  - circulation (CIRCULATION_ANALYSIS, CIRCULATION_CHECK)
  - ergonomie (CLEARANCE_CHECK, ERGONOMIC_ANALYSIS, ACCESSIBILITY_ANALYSIS, FURNITURE_DIMENSION_REASONING)
  - critique (PROJECT_CRITIQUE, GUIDED_REASONING)
  - BIM (IFC_ENTITY_IDENTIFICATION, IFC_PROPERTY_REASONING, BIM_SPATIAL_HIERARCHY, BIM_OBJECT_QUERY, BIM_REASONING, IFC_QA)
  - OBJECT_RELATION
  - PLAN_PLUS_3D
  - IMAGE_PLUS_TEXT
- At least 20% of all other Wave 1 Repaired examples stratified by task group.
"""

import json
import random
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple

CRITICAL_TASKS = {
    "CIRCULATION_ANALYSIS",
    "CIRCULATION_CHECK",
    "CLEARANCE_CHECK",
    "ERGONOMIC_ANALYSIS",
    "ACCESSIBILITY_ANALYSIS",
    "FURNITURE_DIMENSION_REASONING",
    "PROJECT_CRITIQUE",
    "GUIDED_REASONING",
    "IFC_ENTITY_IDENTIFICATION",
    "IFC_PROPERTY_REASONING",
    "BIM_SPATIAL_HIERARCHY",
    "BIM_OBJECT_QUERY",
    "BIM_REASONING",
    "IFC_QA",
    "OBJECT_RELATION",
    "PLAN_PLUS_3D",
    "IMAGE_PLUS_TEXT",
    "PLAN_PLUS_TEXT",
    "MULTIMODAL_PROJECT_REASONING",
}

MULTIMODAL_GROUPS = {"L_MULTIMODAL"}
MULTIMODAL_TASKS = {
    "PLAN_PLUS_3D",
    "IMAGE_PLUS_TEXT",
    "PLAN_PLUS_TEXT",
    "MULTIMODAL_PROJECT_REASONING",
    "MATERIAL_AND_STYLE_RELATION",
}


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    """Loads a JSONL file into a list of dictionaries."""
    records = []
    if not path.exists():
        return records
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


class AuditSampler:
    """Stratified deterministic sampler for independent audit."""

    def __init__(self, seed: int = 42):
        self.seed = seed

    def sample_datasets(
        self,
        wave1_repaired_path: Path,
        review_queue_path: Path,
        gold_set_v2_path: Path,
        min_wave1_fraction: float = 0.20,
    ) -> Dict[str, Any]:
        """
        Executes stratified sampling meeting all user criteria.
        Returns:
            {
                "sampled_wave1": List[Dict],
                "sampled_gold_v2": List[Dict],
                "sampled_review": List[Dict],
                "total_unique_audited": int,
                "all_audited_records": List[Dict],
                "strata_stats": Dict[str, Any],
            }
        """
        rng = random.Random(self.seed)

        wave1_all = load_jsonl(wave1_repaired_path)
        review_all = load_jsonl(review_queue_path)
        gold_v2_all = load_jsonl(gold_set_v2_path)

        # 1. 100% of Gold Set V2
        sampled_gold_ids = {ex["id"] for ex in gold_v2_all}

        # 2. 100% of Review Queue
        sampled_review_ids = {ex["id"] for ex in review_all}

        # 3. Mandatory Wave 1 subsets
        wave1_warnings = [ex for ex in wave1_all if ex.get("quality_status") == "WARNING"]
        wave1_l6 = [ex for ex in wave1_all if ex.get("difficulty") in ("L6", "L6_MULTICONTRAINTE")]
        wave1_multimodal = [
            ex for ex in wave1_all
            if ex.get("task_group") in MULTIMODAL_GROUPS or ex.get("task_type") in MULTIMODAL_TASKS
        ]
        wave1_critical = [
            ex for ex in wave1_all
            if ex.get("task_type") in CRITICAL_TASKS or ex.get("skill") in ("circulation", "ergonomics", "critique", "BIM", "IFC")
        ]

        mandatory_wave1_ids: Set[str] = set()
        for group in (wave1_warnings, wave1_l6, wave1_multimodal, wave1_critical):
            for ex in group:
                mandatory_wave1_ids.add(ex["id"])

        # Remaining Wave 1 records stratified by task_group
        remaining_wave1_by_group: Dict[str, List[Dict[str, Any]]] = {}
        for ex in wave1_all:
            if ex["id"] not in mandatory_wave1_ids:
                grp = ex.get("task_group", "UNKNOWN")
                remaining_wave1_by_group.setdefault(grp, []).append(ex)

        additional_wave1_ids: Set[str] = set()
        # Stratified sampling of remaining to achieve >= 20% total Wave 1 and good coverage of all groups
        for grp, items in remaining_wave1_by_group.items():
            k = max(1, int(len(items) * min_wave1_fraction)) if items else 0
            selected = rng.sample(items, min(k, len(items)))
            for ex in selected:
                additional_wave1_ids.add(ex["id"])

        all_sampled_wave1_ids = mandatory_wave1_ids.union(additional_wave1_ids)

        sampled_wave1 = [ex for ex in wave1_all if ex["id"] in all_sampled_wave1_ids]

        # Tag origin metadata
        for ex in sampled_wave1:
            ex["_audit_origin"] = "wave1_repaired"
        for ex in review_all:
            ex["_audit_origin"] = "review_queue"
        for ex in gold_v2_all:
            ex["_audit_origin"] = "gold_set_v2"

        # Construct unified audited list (keyed by ID, preserving provenance)
        id_to_record: Dict[str, Dict[str, Any]] = {}
        for ex in sampled_wave1:
            id_to_record[ex["id"]] = ex
        for ex in review_all:
            id_to_record[ex["id"]] = ex
        for ex in gold_v2_all:
            # If in both, note it for contamination check
            if ex["id"] in id_to_record:
                id_to_record[ex["id"]]["_in_gold_v2"] = True
            else:
                id_to_record[ex["id"]] = ex

        strata_stats = {
            "total_wave1_available": len(wave1_all),
            "total_wave1_sampled": len(sampled_wave1),
            "wave1_sample_percentage": round((len(sampled_wave1) / len(wave1_all)) * 100, 2) if wave1_all else 0,
            "wave1_warnings_count": len(wave1_warnings),
            "wave1_warnings_sampled": len([ex for ex in sampled_wave1 if ex.get("quality_status") == "WARNING"]),
            "wave1_l6_count": len(wave1_l6),
            "wave1_l6_sampled": len([ex for ex in sampled_wave1 if ex.get("difficulty") in ("L6", "L6_MULTICONTRAINTE")]),
            "wave1_multimodal_count": len(wave1_multimodal),
            "wave1_multimodal_sampled": len([ex for ex in sampled_wave1 if ex.get("task_group") in MULTIMODAL_GROUPS or ex.get("task_type") in MULTIMODAL_TASKS]),
            "wave1_critical_count": len(wave1_critical),
            "wave1_critical_sampled": len([ex for ex in sampled_wave1 if ex.get("task_type") in CRITICAL_TASKS]),
            "total_review_queue": len(review_all),
            "review_queue_sampled": len(review_all),
            "total_gold_v2": len(gold_v2_all),
            "gold_v2_sampled": len(gold_v2_all),
            "total_unique_records_audited": len(id_to_record),
        }

        return {
            "sampled_wave1": sampled_wave1,
            "sampled_gold_v2": gold_v2_all,
            "sampled_review": review_all,
            "total_unique_audited": len(id_to_record),
            "all_audited_records": list(id_to_record.values()),
            "strata_stats": strata_stats,
        }
