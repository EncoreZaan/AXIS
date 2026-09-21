# -*- coding: utf-8 -*-
"""
ARCHI-AI — EpistemicValidator (Contrôle de Séparation Faits / Déductions)
=========================================================================
Garantit qu'une hypothèse n'est jamais présentée comme un fait certain.
Vérifie la présence et la cohérence de la décomposition épistémique :
OBSERVATION, INTERPRETATION, INFERENCE, UNKNOWN, TO_VERIFY.
"""

from typing import Dict, Any, List
from .base_validator import BaseValidator
from ..schema import SupervisedExample, QualityStatus, QualityCheckResult, EpistemicTag


class EpistemicValidator(BaseValidator):
    """Validateur de qualification épistémique."""

    @property
    def name(self) -> str:
        return "EpistemicValidator"

    def validate(self, example: SupervisedExample) -> QualityCheckResult:
        """
        Vérifie que l'exemple qualifie clairement ses assertions.
        """
        breakdown = example.epistemic_breakdown
        if not breakdown:
            # Si aucune décomposition épistémique n'est renseignée
            return QualityCheckResult(
                validator_name=self.name,
                status=QualityStatus.WARNING,
                message="Décomposition épistémique absente ou vide",
                details={},
            )

        # Contrôler les clés valides
        valid_tags = {tag.value for tag in EpistemicTag}
        for k in breakdown.keys():
            if k not in valid_tags:
                return QualityCheckResult(
                    validator_name=self.name,
                    status=QualityStatus.FAIL,
                    message=f"Tag épistémique inconnu: '{k}'. Doit être parmi {list(valid_tags)}",
                    details={"invalid_tag": k},
                )

        # Si l'exemple déclare une incertitude ou information manquante, vérifier la présence d'un tag UNKNOWN ou TO_VERIFY
        uncertainty = example.uncertainty
        if uncertainty and uncertainty.strip():
            has_unknown = bool(breakdown.get(EpistemicTag.UNKNOWN.value) or breakdown.get(EpistemicTag.TO_VERIFY.value))
            if not has_unknown:
                return QualityCheckResult(
                    validator_name=self.name,
                    status=QualityStatus.WARNING,
                    message="Une incertitude est déclarée sans tag UNKNOWN ou TO_VERIFY associé",
                    details={"uncertainty": uncertainty},
                )

        return QualityCheckResult(
            validator_name=self.name,
            status=QualityStatus.PASS,
            message="Qualification épistémique valide et respectée",
            details={"active_tags": list(breakdown.keys())},
        )
