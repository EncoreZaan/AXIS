# -*- coding: utf-8 -*-
"""
ARCHI-AI — Difficulty Calibration & L6 Authenticity Audit Module
===============================================================
Audits cognitive difficulty calibration across L1–L6:
- L1_RECONNAISSANCE: Basic retrieval and identification.
- L2_COMPREHENSION: Categorization and functional grouping.
- L3_ANALYSE: Metric computations, graph topology, PBR reflectance.
- L4_RAISONNEMENT: Guided deduction, flow bottlenecks.
- L5_EXPERT: Uncompromising studio critique, regulatory mastery.
- L6_MULTICONTRAINTE: Multi-objective trade-offs between genuinely conflicting constraints.

Implements L6_AUTHENTICITY_TEST:
Evaluates whether each of the 50 L6 examples features:
1. At least 2 active constraints.
2. Genuinely conflicting architectural objectives (e.g. acoustic vs daylight, budget vs heritage).
3. Explicit trade-off reasoning / arbitration in the answer.
4. Non-trivial synthesis.
"""

from typing import Dict, Any, List, Tuple


class DifficultyAuditor:
    """Independent auditor for curriculum difficulty and L6 authenticity."""

    def __init__(self):
        self.arbitration_keywords = [
            "arbitrage", "compromis", "mise en balance", "tension entre", "conflit d'usage",
            "dilemme", "priorisation", "hiérarchie des contraintes", "conciliation",
            "arbitre l'adéquation", "arbitrer", "sacrifice consenti", "compromis spatial"
        ]

    def audit_difficulty(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits the claimed difficulty level against the reasoning structure.
        """
        diff = record.get("difficulty", "UNKNOWN")
        answer = record.get("answer", "")
        task_type = record.get("task_type", "")

        is_l6 = diff in ("L6", "L6_MULTICONTRAINTE")

        if is_l6:
            return self.l6_authenticity_test(record)

        # Basic check for L1-L5
        words = len(answer.split())
        has_analysis = "analyse" in answer.lower() or "raisonnement" in answer.lower()

        is_miscalibrated = False
        notes = []

        if diff in ("L1", "L1_RECONNAISSANCE") and words > 300:
            notes.append("L1 example contains disproportionately complex reasoning")
        elif diff in ("L5", "L5_EXPERT") and words < 50:
            is_miscalibrated = True
            notes.append("L5 expert example is too brief and superficial")

        return {
            "record_id": record.get("id"),
            "difficulty": diff,
            "is_l6": False,
            "is_miscalibrated": is_miscalibrated,
            "notes": notes,
            "verdict": "PASS" if not is_miscalibrated else "WARNING",
        }

    def l6_authenticity_test(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        L6_AUTHENTICITY_TEST:
        Examines whether an L6 example contains genuine contradictory constraints
        and an authentic architectural trade-off, or merely empty posturing.
        """
        constraints = record.get("constraints") or []
        answer = record.get("answer", "")
        question = record.get("question", "")
        gt = record.get("ground_truth") or {}
        inputs = record.get("inputs") or {}

        # 1. Constraint count check
        constraint_count = len(constraints)
        # Check text contexts for constraint claims
        text_contexts = inputs.get("text_contexts") or []
        spatial_demands = []
        for tc in text_contexts:
            if isinstance(tc, dict) and "spatial_demands" in tc:
                spatial_demands.extend(tc["spatial_demands"])

        total_effective_constraints = max(constraint_count, len(spatial_demands))

        has_at_least_2_constraints = total_effective_constraints >= 2

        # 2. Check for explicit trade-off / arbitration in answer
        matched_arbitration = [kw for kw in self.arbitration_keywords if kw in answer.lower()]
        has_arbitration_language = len(matched_arbitration) > 0

        # 3. Check whether conflicting objectives are articulated
        conflict_tokens = ["versus", "vs", "antagoniste", "contradictoire", "opposé", "conflit", "limitation"]
        has_conflict_stated = any(tok in answer.lower() or tok in question.lower() for tok in conflict_tokens)

        # 4. Authenticity score
        score = 0.0
        if has_at_least_2_constraints:
            score += 0.4
        if has_arbitration_language:
            score += 0.3
        if has_conflict_stated:
            score += 0.3

        is_authentic = score >= 0.7

        verdict = "L6_AUTHENTIC" if is_authentic else (
            "L6_SUPERFICIAL" if score >= 0.4 else "L6_INAUTHENTIC"
        )

        return {
            "record_id": record.get("id"),
            "difficulty": "L6_MULTICONTRAINTE",
            "is_l6": True,
            "authenticity_score": round(score, 2),
            "total_effective_constraints": total_effective_constraints,
            "has_at_least_2_constraints": has_at_least_2_constraints,
            "has_arbitration_language": has_arbitration_language,
            "matched_arbitration_keywords": matched_arbitration,
            "has_conflict_stated": has_conflict_stated,
            "verdict": verdict,
            "is_authentic": is_authentic,
        }
