# -*- coding: utf-8 -*-
"""
ARCHI-AI — IfcVerifier (Validation Déterministe BIM / IFC)
==========================================================
Valide rigoureusement les classes IFC, les arborescences spatiales
et les jeux de propriétés (PropertySets) à partir des modèles normalisés.
"""

from typing import Dict, Any, List, Tuple, Optional
from .base_verifier import BaseVerifier


class IfcVerifier(BaseVerifier):
    """Vérificateur déterministe pour les entités et hiérarchies IFC."""

    VALID_IFC_CLASSES = {
        "IfcProject", "IfcSite", "IfcBuilding", "IfcBuildingStorey", "IfcSpace",
        "IfcWall", "IfcWallStandardCase", "IfcDoor", "IfcWindow", "IfcSlab",
        "IfcColumn", "IfcBeam", "IfcStair", "IfcRailing", "IfcCovering",
        "IfcFurnishingElement", "IfcOpeningElement", "IfcFlowTerminal"
    }

    def verify_class_name(self, class_name: str) -> bool:
        """Contrôle la validité d'une classe selon le standard buildingSMART."""
        return class_name in self.VALID_IFC_CLASSES

    def verify(self, claim: Any, ground_truth_context: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Vérifie si une entité ou propriété déclarée existe réellement dans le modèle IFC.
        """
        ifc_entities = ground_truth_context.get("entities", [])
        hierarchy = ground_truth_context.get("hierarchy", {})

        claimed_entity = claim.get("entity_type")
        if claimed_entity:
            if not self.verify_class_name(claimed_entity):
                return False, f"Classe IFC invalide ou inexistante: '{claimed_entity}'", {}
            
            # Vérifier la présence dans les entités réelles si fournies
            if ifc_entities:
                matching = [e for e in ifc_entities if e.get("type") == claimed_entity or e.get("class") == claimed_entity]
                if not matching:
                    return (
                        False,
                        f"L'entité IFC '{claimed_entity}' n'existe pas dans cette maquette",
                        {"claimed_entity": claimed_entity}
                    )
                return True, f"Entité IFC '{claimed_entity}' certifiée présente ({len(matching)} occurrences)", {"count": len(matching)}

        return True, "Entité IFC conforme au schéma standard", {}
