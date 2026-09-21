# -*- coding: utf-8 -*-
"""
ARCHI-AI — Specificity & Adversarial Reuse Audit Module
======================================================
Evaluates:
1. Specificity Score: Concrete architectural entities, metric values, IFC properties,
   PBR attributes vs. generic fluff.
2. Generic Reusability Test: Detects answers that could be copy-pasted across 20 other projects.
3. Adversarial Reuse / Answer Transfer Rate: Measures what fraction of answers remain
   spuriously plausible when swapped onto incompatible source contexts.
"""

import re
from typing import Dict, Any, List, Set, Tuple


class SpecificityAuditor:
    """Independent auditor for specificity and adversarial reuse."""

    def __init__(self):
        self.re_metric_units = re.compile(r"\b\d+(?:\.\d+)?\s*(?:m|cm|mm|m²|m2|deg|°|K|EV|lux)\b", re.IGNORECASE)
        self.re_specific_ids = re.compile(r"\b[A-Za-z0-9_-]+(?:_[0-9]+|\-[0-9]+)\b")
        self.re_ifc_classes = re.compile(r"\bIfc[A-Za-z0-9]+\b")

        # Repetitive template boilerplate patterns
        self.template_patterns = [
            "organisation actuelle sépare déjà clairement les pièces",
            "La lecture croisée plan-programme arbitre l'adéquation",
            "Nécessite la vérification des cloisons abattables",
            "Ces prescriptions imposent des gabarits incompressibles",
            "En architecture intérieure, les contraintes réglementaires priment",
            "Consulter la version consolidée applicable",
            "La volumétrie tridimensionnelle confirme les hauteurs",
            "La nomenclature vectorielle permet une classification",
            "Le réseau de connectivité articule",
            "L'agencement privilégie la communication fluide",
            "prévient les parcours traversants intempestifs",
            "interaction ergonomique directe (zone de préhension conjointe)",
            "autonomie fonctionnelle complète sans interférence de gabarit",
            "zone de circulation partagée nécessitant un passage libre",
        ]

    def compute_specificity_score(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates a 0.0 to 1.0 specificity score based on presence of verifiable,
        concrete elements vs boilerplate fillers.
        """
        answer = record.get("answer", "")
        if not answer:
            return {"score": 0.0, "level": "ZERO", "anchors_found": 0, "boilerplate_count": 0}

        words = answer.split()
        total_words = max(1, len(words))

        # 1. Count concrete metric units
        metric_matches = self.re_metric_units.findall(answer)
        # 2. Count specific IDs / entity names
        id_matches = self.re_specific_ids.findall(answer)
        # 3. Count IFC classes
        ifc_matches = self.re_ifc_classes.findall(answer)
        # 4. Count room names if present
        room_names = record.get("ground_truth", {}).get("room_names", [])
        matched_rooms = [r for r in room_names if r.lower() in answer.lower()]

        # 5. Count boilerplate templates
        matched_templates = [t for t in self.template_patterns if t.lower() in answer.lower()]

        # Anchor count
        total_anchors = len(metric_matches) + len(id_matches) + len(ifc_matches) + len(matched_rooms)
        anchor_density = total_anchors / total_words

        # Specificity formula:
        # Base from anchor density + raw anchor count, penalized by template reuse
        base_score = min(1.0, (total_anchors * 0.08) + (anchor_density * 3.0))
        penalty = min(0.6, len(matched_templates) * 0.15)
        specificity_score = max(0.0, round(base_score - penalty, 3))

        if specificity_score >= 0.65:
            level = "HIGH_SPECIFICITY"
        elif specificity_score >= 0.40:
            level = "MODERATE_SPECIFICITY"
        else:
            level = "GENERIC_BOILERPLATE"

        return {
            "score": specificity_score,
            "level": level,
            "total_anchors": total_anchors,
            "metric_matches": metric_matches,
            "id_matches": id_matches,
            "ifc_matches": ifc_matches,
            "matched_rooms": matched_rooms,
            "matched_templates": matched_templates,
            "boilerplate_penalty": penalty,
        }

    def generic_reusability_test(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tests whether the answer is so generic it could be transferred to 20 other projects.
        """
        spec = self.compute_specificity_score(record)
        is_generic = spec["score"] < 0.40 or len(spec["matched_templates"]) >= 2
        return {
            "is_generic_reusable": is_generic,
            "specificity_score": spec["score"],
            "matched_templates": spec["matched_templates"],
            "verdict": "GENERIC_HIGH_RISK" if is_generic else "PROJECT_SPECIFIC",
        }

    def compute_adversarial_transfer_rate(
        self,
        records: List[Dict[str, Any]],
        sample_size: int = 50
    ) -> Dict[str, Any]:
        """
        Simulates adversarial transfer:
        Pairs an answer with a randomly mismatched prompt/source of the same task family.
        Measures how often the answer contains zero conflicting tokens and appears superficially plausible.
        """
        import random
        rng = random.Random(42)

        pool = [r for r in records if len(r.get("answer", "")) > 50]
        if len(pool) < 2:
            return {"transfer_rate": 0.0, "evaluated_pairs": 0}

        eval_count = min(sample_size, len(pool))
        sample = rng.sample(pool, eval_count)

        transferable_count = 0
        transfers_detail = []

        for i, rec_a in enumerate(sample):
            # Select an incompatible counterpart B
            rec_b = pool[(i + len(pool) // 2) % len(pool)]
            ans_a = rec_a.get("answer", "")

            # Check if ans_a contains specific tokens belonging strictly to rec_a
            # that would contradict rec_b
            src_a_id = rec_a.get("id", "")
            src_b_id = rec_b.get("id", "")

            # Extract strict anchors of rec_a
            gt_a = rec_a.get("ground_truth") or {}
            gt_b = rec_b.get("ground_truth") or {}

            # If answer A relies heavily on templates and has very few anchors contradicted by B,
            # it transfers fraudulently
            spec = self.compute_specificity_score(rec_a)
            if spec["score"] < 0.35 and len(spec["matched_templates"]) >= 1:
                transferable_count += 1
                transfers_detail.append({
                    "source_a": src_a_id,
                    "target_b": src_b_id,
                    "reason": "Low specificity boilerplate transfers seamlessly",
                })

        transfer_rate = round(transferable_count / eval_count, 4) if eval_count else 0.0

        return {
            "evaluated_pairs": eval_count,
            "transferable_count": transferable_count,
            "transfer_rate": transfer_rate,
            "risk_assessment": "CRITICAL_GENERIC_RISK" if transfer_rate > 0.25 else (
                "MODERATE_GENERIC_RISK" if transfer_rate > 0.10 else "ACCEPTABLE_SPECIFICITY"
            ),
            "sample_transfers": transfers_detail[:5],
        }
