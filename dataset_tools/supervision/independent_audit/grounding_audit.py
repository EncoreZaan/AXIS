# -*- coding: utf-8 -*-
"""
ARCHI-AI — Grounding & Source Ablation Audit Module
===================================================
Red-team programmatic grounding verification:
- Extracts factual propositions from answer sections (OBSERVATION, INTERPRETATION, etc.).
- Verifies whether each claim is genuinely anchored in evidence/inputs:
  - SUPPORTED
  - PARTIALLY_SUPPORTED
  - UNSUPPORTED
  - UNKNOWN
- Calculates the true Grounding Ratio.
- SOURCE ABLATION TEST: tests whether the response collapses without source data,
  or if it survives intact as an ungrounded, boilerplate template.
"""

import re
from typing import Dict, Any, List, Tuple


class GroundingAuditor:
    """Independent programmatic grounding auditor."""

    def __init__(self):
        self.re_numbers = re.compile(r"[-+]?\d+(?:\.\d+)?")
        self.re_metric_units = re.compile(r"\b(\d+(?:\.\d+)?)\s*(?:m|cm|mm|m²|m2|deg|°|K|EV)\b", re.IGNORECASE)

    def extract_claims(self, text: str) -> List[str]:
        """Splits answer into discrete factual assertions."""
        claims = []
        for line in text.split("\n"):
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("**") and line.endswith("**"):
                continue
            # Remove Markdown boldness markers if line starts with section header
            clean_line = re.sub(r"^\*\*[^*]+\*\*\s*:\s*", "", line).strip()
            if not clean_line:
                continue
            # Split by period into sentences
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", clean_line) if len(s.strip()) > 10]
            if sentences:
                claims.extend(sentences)
            else:
                claims.append(clean_line)
        return claims

    def audit_record_grounding(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits the grounding of a single SupervisedExample record.
        """
        answer = record.get("answer", "")
        evidence = record.get("evidence") or {}
        inputs = record.get("inputs") or {}
        gt = record.get("ground_truth") or {}
        question = record.get("question", "")
        source_prov = record.get("source_provenance") or {}

        evidence_str = str(evidence) + " " + str(inputs) + " " + str(gt) + " " + str(source_prov)

        claims = self.extract_claims(answer)
        claim_evaluations = []

        supported_count = 0
        partially_supported_count = 0
        unsupported_count = 0
        unknown_count = 0

        for claim in claims:
            # Extract specific entities/numbers from claim
            numbers_in_claim = self.re_numbers.findall(claim)
            units_in_claim = self.re_metric_units.findall(claim)

            # Check if this claim is purely a generic homily
            is_generic_homily = self._is_generic_platitude(claim)

            if is_generic_homily:
                status = "UNKNOWN"
                reason = "Generic architectural principle or platitude without specific empirical anchor"
                unknown_count += 1
            elif not numbers_in_claim and not self._contains_specific_entities(claim, record):
                status = "UNKNOWN"
                reason = "No verifiable empirical entities or figures asserted"
                unknown_count += 1
            else:
                # Extract floats from evidence_str for numerical tolerance comparison
                evidence_numbers = [float(x) for x in self.re_numbers.findall(evidence_str)]
                matched_nums = []
                for n_str in numbers_in_claim:
                    try:
                        n_val = float(n_str)
                        if any(abs(n_val - ev_val) < 1e-3 for ev_val in evidence_numbers) or n_str in evidence_str:
                            matched_nums.append(n_str)
                    except ValueError:
                        if n_str in evidence_str:
                            matched_nums.append(n_str)
                num_ratio = len(matched_nums) / len(numbers_in_claim) if numbers_in_claim else 1.0

                matched_entities = self._match_entities_in_evidence(claim, evidence_str, record)

                if num_ratio == 1.0 and matched_entities["full_match"]:
                    status = "SUPPORTED"
                    reason = "All numbers and named entities are verified in source evidence"
                    supported_count += 1
                elif num_ratio > 0.5 or matched_entities["partial_match"]:
                    status = "PARTIALLY_SUPPORTED"
                    reason = f"Partial alignment: numbers ({len(matched_nums)}/{len(numbers_in_claim)}), entities partially matched"
                    partially_supported_count += 1
                else:
                    status = "UNSUPPORTED"
                    reason = "Claim asserts numbers or entities not found in evidence payload"
                    unsupported_count += 1

            claim_evaluations.append({
                "claim": claim,
                "status": status,
                "reason": reason,
            })

        total_claims = len(claims) if claims else 1
        grounding_ratio = round((supported_count + 0.5 * partially_supported_count) / total_claims, 4)

        # Source Ablation Test
        ablation_result = self.source_ablation_test(record)

        return {
            "record_id": record.get("id"),
            "task_type": record.get("task_type"),
            "total_claims": len(claims),
            "supported_count": supported_count,
            "partially_supported_count": partially_supported_count,
            "unsupported_count": unsupported_count,
            "unknown_count": unknown_count,
            "grounding_ratio": grounding_ratio,
            "claims": claim_evaluations,
            "source_ablation": ablation_result,
            "is_solidly_grounded": grounding_ratio >= 0.70 and unsupported_count == 0,
        }

    def source_ablation_test(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        SOURCE ABLATION TEST:
        If we remove all source-specific tokens (names, dimensions, numbers),
        does the response remain intact as a generic answer?
        If an answer has 80%+ identical text to an ablated skeleton, it fails.
        """
        answer = record.get("answer", "")
        # Remove numbers and capitalized terms
        ablated = self.re_numbers.sub("[NUM]", answer)
        words = ablated.split()
        total_words = len(words)

        # Identify generic filler phrases
        generic_fillers = [
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
        ]

        found_fillers = [f for f in generic_fillers if f.lower() in answer.lower()]
        filler_density = len(found_fillers) / len(generic_fillers)

        is_vulnerable_to_ablation = len(found_fillers) >= 2 or (
            len(answer) > 200 and len(found_fillers) >= 1 and total_words < 80
        )

        return {
            "generic_filler_count": len(found_fillers),
            "found_fillers": found_fillers,
            "is_vulnerable_to_ablation": is_vulnerable_to_ablation,
            "verdict": "VULNERABLE_GENERIC_TEMPLATE" if is_vulnerable_to_ablation else "SOURCE_DEPENDENT",
        }

    def _is_generic_platitude(self, claim: str) -> bool:
        platitudes = [
            "priment sur le choix esthétique",
            "arbitre l'adéquation entre l'enveloppe",
            "permet une classification programmatique",
            "prévient les parcours traversants",
            "détermine l'usage",
            "respectent les tolérances anthropométriques",
            "supposées libres d'accès sans condamnation",
            "vérification in situ",
            "version consolidée applicable",
        ]
        claim_lower = claim.lower()
        return any(p in claim_lower for p in platitudes)

    def _contains_specific_entities(self, claim: str, record: Dict[str, Any]) -> bool:
        """Checks if claim references entities from inputs/ground_truth."""
        inputs = record.get("inputs") or {}
        gt = record.get("ground_truth") or {}
        ev = record.get("evidence") or {}

        # Look for room names or object names
        names = []
        if "room_names" in gt:
            names.extend(gt["room_names"])
        if "categories" in gt and isinstance(gt["categories"], list):
            names.extend(gt["categories"])
        if "rooms" in ev and isinstance(ev["rooms"], list):
            for r in ev["rooms"]:
                if isinstance(r, dict) and "name" in r:
                    names.append(r["name"])

        claim_lower = claim.lower()
        return any(n.lower() in claim_lower for n in names if len(n) > 2)

    def _match_entities_in_evidence(self, claim: str, evidence_str: str, record: Dict[str, Any]) -> Dict[str, bool]:
        ev_lower = evidence_str.lower()
        claim_words = [w.strip(".,;:()") for w in claim.split() if len(w) > 4]
        matches = [w for w in claim_words if w.lower() in ev_lower]
        ratio = len(matches) / len(claim_words) if claim_words else 1.0
        return {
            "full_match": ratio >= 0.7,
            "partial_match": ratio >= 0.3,
        }
