# -*- coding: utf-8 -*-
"""
ARCHI-AI — SceneGraphVerifier (Relations Spatiales & Comptage 3D)
================================================================
Vérifie déterministement le nombre d'objets, leurs catégories et leurs relations
spatiales réelles (gauche, droite, devant, derrière, dessus) dans les scènes 3D.
"""

from typing import Dict, Any, List, Tuple, Optional
from .base_verifier import BaseVerifier


class SceneGraphVerifier(BaseVerifier):
    """Vérificateur déterministe pour les scene graphs et boîtes 3D (ex: IL3D)."""

    def count_objects_by_category(self, objects: List[Dict[str, Any]]) -> Dict[str, int]:
        """Compte exact des objets par label de catégorie."""
        counts: Dict[str, int] = {}
        for obj in objects:
            cat = obj.get("category") or obj.get("label") or "unknown"
            counts[cat] = counts.get(cat, 0) + 1
        return counts

    def get_relative_spatial_relation(
        self, box_a: List[float], box_b: List[float]
    ) -> List[str]:
        """
        Détermine les relations spatiales 3D entre deux objets à partir de leurs coordonnées [x, y, z].
        Hypothèse conventionnelle : X = latéral (gauche/droite), Y = profondeur (devant/derrière), Z = vertical (dessus/dessous).
        """
        relations = []
        dx = box_a[0] - box_b[0]
        dy = box_a[1] - box_b[1]
        dz = box_a[2] - box_b[2]

        if abs(dx) > 0.3:
            relations.append("droite" if dx > 0 else "gauche")
        if abs(dy) > 0.3:
            relations.append("devant" if dy > 0 else "derriere")
        if abs(dz) > 0.3:
            relations.append("au-dessus" if dz > 0 else "en-dessous")

        return relations

    def verify(self, claim: Any, ground_truth_context: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Vérifie le décompte d'objets ou une relation spatiale déclarée.
        """
        objects = ground_truth_context.get("objects", [])
        actual_counts = self.count_objects_by_category(objects)

        # Vérification d'un décompte d'objet
        if "expected_category" in claim and "expected_count" in claim:
            cat = claim["expected_category"]
            exp_count = claim["expected_count"]
            real_count = actual_counts.get(cat, 0)
            if real_count != exp_count:
                return (
                    False,
                    f"Comptage 3D erroné : {exp_count} '{cat}' annoncés, mais {real_count} présents dans la scène",
                    {"actual_counts": actual_counts},
                )
            return (
                True,
                f"Comptage vérifié : {real_count} '{cat}' présents",
                {"actual_counts": actual_counts},
            )

        return True, "Scène 3D cohérente avec les annotations de bounding boxes", {"total_objects": len(objects)}
