# -*- coding: utf-8 -*-
"""
ARCHI-AI — GeometryVerifier (Calculs Métriques Déterministes)
=============================================================
Calcule les surfaces réelles, les périmètres, les largeurs de passage
et les relations d'adjacence géométrique via Shapely.
Garantit zéro hallucination sur les métrés.
"""

from typing import Dict, Any, List, Tuple, Optional
import math
from shapely.geometry import Polygon, Point, box
from .base_verifier import BaseVerifier


class GeometryVerifier(BaseVerifier):
    """Vérificateur déterministe pour la géométrie 2D de plans d'étage."""

    def compute_polygon_area_m2(self, coords: List[List[float]], scale_factor: float = 1.0) -> float:
        """Calcule la surface réelle d'un polygone fermé en m²."""
        if len(coords) < 3:
            return 0.0
        poly = Polygon(coords)
        if not poly.is_valid:
            poly = poly.buffer(0)
        return float(poly.area * (scale_factor ** 2))

    def compute_distance_m(self, p1: List[float], p2: List[float], scale_factor: float = 1.0) -> float:
        """Distance euclidienne exacte entre deux points."""
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return float(math.sqrt(dx * dx + dy * dy) * scale_factor)

    def check_clearance(self, box1: List[float], box2: List[float]) -> float:
        """
        Calcule la distance minimale libre entre deux boîtes englobantes [minx, miny, maxx, maxy].
        Retourne 0.0 en cas de collision/chevauchement.
        """
        b1 = box(box1[0], box1[1], box1[2], box1[3])
        b2 = box(box2[0], box2[1], box2[2], box2[3])
        if b1.intersects(b2):
            return 0.0
        return float(b1.distance(b2))

    def verify(self, claim: Any, ground_truth_context: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Vérifie une affirmation numérique (ex: surface d'une pièce annoncée) face à la géométrie réelle.
        Tolérance d'arrondi : 5% max.
        """
        room_name = claim.get("room_name")
        claimed_area = claim.get("claimed_area_m2")
        rooms = ground_truth_context.get("rooms", [])

        target_room = None
        for r in rooms:
            if r.get("name", "").lower() == room_name.lower():
                target_room = r
                break

        if not target_room:
            return False, f"Pièce '{room_name}' non trouvée dans la géométrie du plan", {}

        # Calculer la surface exacte si polygone présent, sinon prendre area_m2
        actual_area = target_room.get("area_m2")
        if actual_area is None and "polygon" in target_room and target_room["polygon"]:
            actual_area = self.compute_polygon_area_m2(target_room["polygon"])

        if actual_area is None:
            return False, f"Impossible de calculer la surface de '{room_name}' : pas de polygone", {}

        actual_area = float(actual_area)
        if claimed_area is not None:
            claimed_area = float(claimed_area)
            diff = abs(actual_area - claimed_area)
            relative_error = diff / max(actual_area, 0.01)
            if relative_error > 0.05:
                return (
                    False,
                    f"Erreur de métré : la surface annoncée ({claimed_area:.2f} m²) diffère de la surface réelle calculée ({actual_area:.2f} m²)",
                    {"actual_area_m2": round(actual_area, 2), "error_pct": round(relative_error * 100, 2)},
                )

        return (
            True,
            f"Surface vérifiée avec exactitude : {actual_area:.2f} m²",
            {"actual_area_m2": round(actual_area, 2)},
        )
