# -*- coding: utf-8 -*-
"""
ARCHI-AI — Target Contract Validators for Dataset A
===================================================
Vérificateurs formels des contrats de cibles pour les 4 tâches de la Phase 4 :
1. FLOORPLAN_READING
2. ROOM_TOPOLOGY
3. OBJECT_RELATION
4. CLEARANCE_CHECK

Catégories d'évaluation :
- VALID
- INVALID
- AMBIGUOUS
- MISSING
"""

import math
from typing import Dict, Any, Tuple
from enum import Enum


class TargetValidationStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    AMBIGUOUS = "AMBIGUOUS"
    MISSING = "MISSING"


class TargetContractValidator:
    """Valide les cibles et vérifie l'absence de fuite dans les entrées."""

    @staticmethod
    def validate_floorplan_reading(example: Dict[str, Any]) -> Tuple[TargetValidationStatus, str]:
        targets = example.get("targets") or example.get("ground_truth")
        if not targets:
            return TargetValidationStatus.MISSING, "Targets dict is missing"

        required_keys = ["rooms_count", "doors_count", "habitable_pixels", "wall_pixels"]
        for k in required_keys:
            if k not in targets:
                return TargetValidationStatus.MISSING, f"Missing key '{k}' in targets"
            if not isinstance(targets[k], int) or targets[k] < 0:
                return TargetValidationStatus.INVALID, f"Invalid value for '{k}': {targets[k]}"

        if targets["rooms_count"] < 1:
            return TargetValidationStatus.INVALID, "rooms_count must be at least 1"

        # Interdiction absolue de calibrations métriques physiques
        if "metric_scale" in targets and targets["metric_scale"] not in [None, "UNKNOWN"]:
            return TargetValidationStatus.INVALID, "Metric calibration scale is forbidden in FLOORPLAN_READING"

        # Vérification anti-shortcut dans les données d'inputs (hors prompt textuel)
        input_data = {k: v for k, v in example.get("inputs", {}).items() if k != "prompt"}
        input_str = str(input_data).lower()
        for forbidden in ["rooms_count", "doors_count", "habitable_pixels", "wall_pixels"]:
            if forbidden in input_str:
                return TargetValidationStatus.INVALID, f"Target shortcut leak in inputs: {forbidden}"

        return TargetValidationStatus.VALID, "Target contract verified"

    @staticmethod
    def validate_room_topology(example: Dict[str, Any]) -> Tuple[TargetValidationStatus, str]:
        targets = example.get("targets") or example.get("ground_truth")
        if not targets:
            return TargetValidationStatus.MISSING, "Targets dict is missing"

        required_keys = ["room_count", "largest_room_pixels", "smallest_room_pixels", "room_sizes_pixels"]
        for k in required_keys:
            if k not in targets:
                return TargetValidationStatus.MISSING, f"Missing key '{k}' in targets"

        room_count = targets["room_count"]
        room_sizes = targets["room_sizes_pixels"]

        if not isinstance(room_count, int) or room_count < 2:
            return TargetValidationStatus.INVALID, f"Invalid room_count: {room_count}"

        if not isinstance(room_sizes, list) or len(room_sizes) != room_count:
            return TargetValidationStatus.INVALID, f"room_sizes_pixels length ({len(room_sizes)}) != room_count ({room_count})"

        # Vérifier l'ordre décroissant
        if room_sizes != sorted(room_sizes, reverse=True):
            return TargetValidationStatus.INVALID, "room_sizes_pixels is not sorted descending"

        if targets["largest_room_pixels"] != room_sizes[0]:
            return TargetValidationStatus.INVALID, f"largest_room_pixels mismatch: {targets['largest_room_pixels']} vs {room_sizes[0]}"

        if targets["smallest_room_pixels"] != room_sizes[-1]:
            return TargetValidationStatus.INVALID, f"smallest_room_pixels mismatch: {targets['smallest_room_pixels']} vs {room_sizes[-1]}"

        # Vérification anti-shortcut dans inputs (hors prompt)
        input_data = {k: v for k, v in example.get("inputs", {}).items() if k != "prompt"}
        input_str = str(input_data).lower()
        for forbidden in ["room_count", "largest_room_pixels", "smallest_room_pixels", "room_sizes"]:
            if forbidden in input_str:
                return TargetValidationStatus.INVALID, f"Target shortcut leak in inputs: {forbidden}"

        return TargetValidationStatus.VALID, "Target contract verified"

    @staticmethod
    def validate_object_relation(example: Dict[str, Any]) -> Tuple[TargetValidationStatus, str]:
        targets = example.get("targets") or example.get("ground_truth")
        if not targets:
            return TargetValidationStatus.MISSING, "Targets dict is missing"

        required_keys = ["distance_m", "object_a_pos", "object_b_pos", "room"]
        for k in required_keys:
            if k not in targets:
                return TargetValidationStatus.MISSING, f"Missing key '{k}' in targets"

        pos_a = targets["object_a_pos"]
        pos_b = targets["object_b_pos"]
        if not (isinstance(pos_a, (list, tuple)) and len(pos_a) == 3):
            return TargetValidationStatus.INVALID, f"Invalid object_a_pos: {pos_a}"
        if not (isinstance(pos_b, (list, tuple)) and len(pos_b) == 3):
            return TargetValidationStatus.INVALID, f"Invalid object_b_pos: {pos_b}"

        dx = pos_a[0] - pos_b[0]
        dy = pos_a[1] - pos_b[1]
        dz = pos_a[2] - pos_b[2]
        expected_dist = round(math.sqrt(dx * dx + dy * dy + dz * dz), 2)
        dist_m = round(float(targets["distance_m"]), 2)

        if abs(expected_dist - dist_m) > 0.02:
            return TargetValidationStatus.INVALID, f"Distance calculation mismatch: {dist_m} vs {expected_dist}"

        # Vérification anti-shortcut : les données de géométrie ne doivent jamais contenir de distance calculée
        input_data = {k: v for k, v in example.get("inputs", {}).items() if k != "prompt"}
        input_str = str(input_data).lower()
        for forbidden in ["distance_m", "distance", "euclidean", "dist_m", "bearing"]:
            if forbidden in input_str:
                return TargetValidationStatus.INVALID, f"Distance shortcut leak in inputs data: {forbidden}"

        return TargetValidationStatus.VALID, "Target contract verified"

    @staticmethod
    def validate_clearance_check(example: Dict[str, Any]) -> Tuple[TargetValidationStatus, str]:
        targets = example.get("targets") or example.get("ground_truth")
        if not targets:
            return TargetValidationStatus.MISSING, "Targets dict is missing"

        required_keys = ["measured_distance_m", "threshold_m", "compliance_verdict"]
        for k in required_keys:
            if k not in targets:
                return TargetValidationStatus.MISSING, f"Missing key '{k}' in targets"

        dist = float(targets["measured_distance_m"])
        thresh = float(targets["threshold_m"])
        verdict = targets["compliance_verdict"]

        if not isinstance(verdict, bool):
            return TargetValidationStatus.INVALID, f"compliance_verdict must be boolean, got {type(verdict)}"

        expected_verdict = (dist >= thresh)
        if verdict != expected_verdict:
            return TargetValidationStatus.INVALID, f"Verdict mismatch: {verdict} vs expected {expected_verdict} (dist={dist}, thresh={thresh})"

        # Vérification anti-shortcut : inputs ne doit contenir AUCUN indice sur le verdict
        input_data = {k: v for k, v in example.get("inputs", {}).items() if k != "prompt"}
        input_str = str(input_data).lower()
        for leak_word in ["compliance_verdict", "verdict", "compliant", "conforme", "insuffisant", "pass", "fail"]:
            if leak_word in input_str:
                return TargetValidationStatus.INVALID, f"Verdict shortcut leak in inputs: '{leak_word}'"

        return TargetValidationStatus.VALID, "Target contract verified"

    @classmethod
    def validate_example(cls, example: Dict[str, Any]) -> Tuple[TargetValidationStatus, str]:
        """Routeur de validation contractuelle par tâche."""
        task_id = example.get("task_id")
        if not task_id:
            return TargetValidationStatus.MISSING, "example has no task_id"

        if task_id == "FLOORPLAN_READING":
            return cls.validate_floorplan_reading(example)
        elif task_id == "ROOM_TOPOLOGY":
            return cls.validate_room_topology(example)
        elif task_id == "OBJECT_RELATION":
            return cls.validate_object_relation(example)
        elif task_id == "CLEARANCE_CHECK":
            return cls.validate_clearance_check(example)
        else:
            return TargetValidationStatus.INVALID, f"Unsupported task_id: {task_id}"
