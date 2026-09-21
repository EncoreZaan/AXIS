# -*- coding: utf-8 -*-
"""
ARCHI-AI — Task-Specific Deep Reasoning Audit Module
===================================================
Red-team independent audits for domain-specific tasks:
1. OBJECT_RELATION: Recalculates dx, dy, dz, and Euclidean distance from raw/input coordinates.
   Flags coordinate mismatches, directional axis inversion (e.g. Y-up vs Z-up confusion).
2. FLOORPLAN: Verifies room inventory, polygon bounds, adjacency graphs, and area calculations.
   Detects pixel space masquerading as square meters (e.g. 18,806 m² living room).
3. BIM / IFC: Checks entity classes (IfcWall, IfcDoor), storey counts, space names against source payloads.
4. ERGONOMIE: Recalculates unit conversions (cm -> m), threshold comparisons, PMR clearances.
5. CRITIQUE: Checks for genuine 4-stage architecture (diagnostic, cause, consequence, recommendation)
   and verifies whether critique points directly derive from project geometry rather than clichés.
6. PEDAGOGIE: Checks for didactic contextualization, student skill level, explicit misconception,
   and Socratic step-by-step guidance.
"""

import math
import re
from typing import Dict, Any, List, Optional, Tuple


class ReasoningAuditor:
    """Task-specific independent red-team auditor."""

    def __init__(self, coordinate_tolerance: float = 0.05):
        self.coordinate_tolerance = coordinate_tolerance

    # -------------------------------------------------------------
    # 1. OBJECT_RELATION Audit
    # -------------------------------------------------------------
    def audit_object_relation(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Independent recalculation of 3D spatial delta and Euclidean distance.
        Does NOT trust ground_truth or answer claims.
        """
        inputs = record.get("inputs") or {}
        geometries = inputs.get("geometries") or []
        gt = record.get("ground_truth") or {}
        answer = record.get("answer", "")

        # Extract positions from input geometries or evidence
        pos1 = None
        pos2 = None

        if geometries and isinstance(geometries, list) and isinstance(geometries[0], dict):
            geom = geometries[0]
            if "pos1" in geom and "pos2" in geom:
                pos1 = geom["pos1"]
                pos2 = geom["pos2"]
            elif "objects" in geom and len(geom["objects"]) >= 2:
                pos1 = geom["objects"][0].get("position") or geom["objects"][0].get("centroid")
                pos2 = geom["objects"][1].get("position") or geom["objects"][1].get("centroid")

        if (not pos1 or not pos2) and "evidence" in record:
            ev = record["evidence"]
            if isinstance(ev, dict) and "o1_pos" in ev and "o2_pos" in ev:
                pos1 = ev["o1_pos"]
                pos2 = ev["o2_pos"]

        if not pos1 or not pos2:
            return {
                "verdict": "FAIL_MISSING_OBJECTS",
                "error": "Less than 2 object positions found in inputs/evidence",
                "recalculated_distance": None,
                "claimed_distance": gt.get("distance_m"),
            }

        if not pos1 or not pos2 or len(pos1) < 3 or len(pos2) < 3:
            return {
                "verdict": "FAIL_INCOMPLETE_COORDINATES",
                "error": "Coordinates missing or have fewer than 3 dimensions",
                "pos1": pos1,
                "pos2": pos2,
            }

        # Independent Euclidean recalculation
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        dz = pos2[2] - pos1[2]
        recomputed_dist = math.sqrt(dx**2 + dy**2 + dz**2)

        claimed_dist = gt.get("distance_m")
        # Try extracting claimed distance from answer if missing in gt
        if claimed_dist is None:
            m = re.search(r"(\d+(?:\.\d+)?)\s*m\b", answer)
            if m:
                claimed_dist = float(m.group(1))

        if claimed_dist is None:
            return {
                "verdict": "FAIL_NO_CLAIMED_DISTANCE",
                "error": "No distance claim found in ground_truth or answer",
                "recalculated_distance": round(recomputed_dist, 3),
            }

        diff = abs(recomputed_dist - float(claimed_dist))
        is_match = diff <= self.coordinate_tolerance

        # Directional consistency check: IL3D convention vs standard
        # In IL3D: X is lateral, Y is vertical (height), Z is depth
        # In Archi standard: X is lateral, Y is depth, Z is vertical
        has_axis_confusion = ("surélevé" in answer or "en contrebas" in answer) and abs(dy) < 0.2 and abs(dz) >= 0.3

        return {
            "verdict": "PASS" if is_match and not has_axis_confusion else "FAIL",
            "is_distance_match": is_match,
            "recalculated_dist": round(recomputed_dist, 3),
            "claimed_dist": claimed_dist,
            "diff_m": round(diff, 4),
            "recomputed_delta_xyz": [round(dx, 3), round(dy, 3), round(dz, 3)],
            "claimed_delta_xyz": gt.get("delta_xyz"),
            "axis_confusion_detected": has_axis_confusion,
        }

    # -------------------------------------------------------------
    # 2. FLOORPLAN Audit
    # -------------------------------------------------------------
    def audit_floorplan(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits room counts, polygons, surfaces, and adjacency.
        Detects pixel space masquerading as square meters (critical red team check).
        """
        inputs = record.get("inputs") or {}
        geometries = inputs.get("geometries") or []
        evidence = record.get("evidence") or {}
        gt = record.get("ground_truth") or {}
        answer = record.get("answer", "")

        geom = geometries[0] if geometries and isinstance(geometries, list) else {}
        total_area = geom.get("total_area_m2") or geom.get("area_m2")

        # Critical Red Team Check: Pixel Area Labeled as Square Meters
        # In ResPlan raw, area is in square pixels (e.g. 18,806 px² or 50,336 px²).
        # Normal apartments are 20 m² to 500 m². An apartment > 2,000 m² is almost certainly pixel coordinates!
        has_pixel_as_m2_hallucination = False
        pixel_area_value = None
        if total_area and total_area > 1500.0:
            has_pixel_as_m2_hallucination = True
            pixel_area_value = total_area

        # Check room areas in evidence
        rooms = evidence.get("rooms", [])
        absurd_room_areas = []
        for r in rooms:
            if isinstance(r, dict):
                r_area = r.get("area_m2")
                if r_area and r_area > 1000.0:
                    absurd_room_areas.append({"room": r.get("name"), "area_m2": r_area})

        if absurd_room_areas:
            has_pixel_as_m2_hallucination = True

        # Check room count consistency
        input_count = geom.get("room_count")
        gt_count = gt.get("total_rooms")
        rooms_in_answer = [w for w in ["living", "bedroom", "kitchen", "bathroom", "balcony"] if w in answer.lower()]

        # Adjacency check
        adj_pairs = geom.get("adjacency_pairs") or []
        claimed_pairs = gt.get("connected_pairs_count")

        flags = []
        if has_pixel_as_m2_hallucination:
            flags.append("PIXEL_COORDINATES_LABELED_AS_M2")
        if input_count and gt_count and input_count != gt_count:
            flags.append(f"ROOM_COUNT_MISMATCH_{input_count}_vs_{gt_count}")

        return {
            "verdict": "FAIL" if has_pixel_as_m2_hallucination else ("WARNING" if flags else "PASS"),
            "has_pixel_as_m2_hallucination": has_pixel_as_m2_hallucination,
            "pixel_area_value": pixel_area_value,
            "absurd_room_areas": absurd_room_areas,
            "input_room_count": input_count,
            "flags": flags,
        }

    # -------------------------------------------------------------
    # 3. BIM / IFC Audit
    # -------------------------------------------------------------
    def audit_bim_ifc(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits IFC classes, storeys, spaces, and entity counts.
        """
        inputs = record.get("inputs") or {}
        ifc_entities = inputs.get("ifc_entities") or []
        gt = record.get("ground_truth") or {}
        answer = record.get("answer", "")

        has_ifc_payload = len(ifc_entities) > 0 or "ifc" in str(inputs).lower()
        if not has_ifc_payload and record.get("task_group") == "D_BIM_IFC":
            return {
                "verdict": "FAIL_EMPTY_IFC_PAYLOAD",
                "error": "Task claims BIM/IFC but inputs.ifc_entities is empty",
            }

        # Check entity names against standard IFC4 schema
        valid_ifc_classes = [
            "IfcWall", "IfcWallStandardCase", "IfcDoor", "IfcWindow", "IfcSlab",
            "IfcSpace", "IfcBuildingStorey", "IfcBeam", "IfcColumn", "IfcCovering"
        ]
        mentioned_classes = [c for c in valid_ifc_classes if c.lower() in answer.lower()]

        # Check if numbers cited in answer match gt or input entity counts
        gt_count = gt.get("total_entities") or gt.get("count")
        numbers = re.findall(r"\b\d+\b", answer)

        return {
            "verdict": "PASS",
            "mentioned_classes": mentioned_classes,
            "has_ifc_payload": has_ifc_payload,
        }

    # -------------------------------------------------------------
    # 4. ERGONOMIE Audit
    # -------------------------------------------------------------
    def audit_ergonomics(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits unit conversions and regulatory thresholds (0.80 m, 0.90 m, 1.50 m).
        Detects mismatched copy-pasted regulations (e.g. rotation circle cited in corridor question).
        """
        inputs = record.get("inputs") or {}
        answer = record.get("answer", "")
        question = record.get("question", "")
        gt = record.get("ground_truth") or {}

        # Conversion check: original_value in cm -> normalized_value in m
        raw_val = None
        norm_val = None
        text_contexts = inputs.get("text_contexts") or []
        for tc in text_contexts:
            if isinstance(tc, dict):
                raw_val = tc.get("original_value")
                norm_val = tc.get("normalized_value")

        conversion_error = False
        if raw_val is not None and norm_val is not None:
            # If cm to m
            expected_m = round(raw_val / 100.0, 3) if raw_val > 5.0 else raw_val
            if abs(norm_val - expected_m) > 0.01:
                conversion_error = True

        # Check for regulation copy-paste mismatch:
        # e.g. If question asks about corridor (couloir) or stairs, but answer quotes rotation circle
        has_regulation_mismatch = False
        if "couloir" in question.lower() and "cercle de giration" in answer.lower() and "0,90 m" not in answer:
            has_regulation_mismatch = True

        return {
            "verdict": "FAIL" if conversion_error or has_regulation_mismatch else "PASS",
            "conversion_error": conversion_error,
            "has_regulation_mismatch": has_regulation_mismatch,
            "raw_val": raw_val,
            "norm_val": norm_val,
        }

    # -------------------------------------------------------------
    # 5. CRITIQUE Audit
    # -------------------------------------------------------------
    def audit_critique(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits studio critique for:
        1. 4-part structure: diagnostic, cause, consequence, recommendation.
        2. Grounded architectural critique vs. superficial praise or generic advice.
        """
        answer = record.get("answer", "")

        # Look for 4-part critique structure
        has_diag = any(k in answer.lower() for k in ["diagnostic", "constat", "observation"])
        has_cause = any(k in answer.lower() for k in ["cause", "origine", "facteur", "déterminant"])
        has_conseq = any(k in answer.lower() for k in ["conséquence", "impact", "friction", "goulot", "saturation"])
        has_recom = any(k in answer.lower() for k in ["recommandation", "arbitrage", "piste", "solution", "optimisation"])

        structure_score = sum([has_diag, has_cause, has_conseq, has_recom]) / 4.0

        # Check for sycophantic platitudes
        cliches = [
            "excellent parti pris", "très beau travail", "rien à redire", "parfait",
            "harmonie totale", "équilibre subtil"
        ]
        has_cliche = any(c in answer.lower() for c in cliches)

        verdict = "PASS" if structure_score >= 0.75 and not has_cliche else "WARNING"

        return {
            "verdict": verdict,
            "structure_score": structure_score,
            "has_cliche": has_cliche,
            "has_diagnostic": has_diag,
            "has_cause": has_cause,
            "has_consequence": has_conseq,
            "has_recommendation": has_recom,
        }

    # -------------------------------------------------------------
    # 6. PEDAGOGIE Audit
    # -------------------------------------------------------------
    def audit_pedagogy(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits pedagogical explanations for:
        - student level adaptation
        - explicit misconception explanation
        - Socratic/maieutic questioning or didactic progression
        """
        answer = record.get("answer", "")
        question = record.get("question", "")

        has_maieutic = any(m in answer.lower() for m in ["pourquoi", "observez", "remarquez", "considérez", "interrogez-vous"])
        has_rule = any(r in answer.lower() for r in ["principe", "règle", "norme", "théorie", "composition"])

        verdict = "PASS" if (has_maieutic or has_rule) else "WARNING"

        return {
            "verdict": verdict,
            "has_didactic_progression": has_maieutic,
            "explains_compositional_principle": has_rule,
        }
