# -*- coding: utf-8 -*-
"""
ARCHI-AI — DifficultyValidator (Calibration de la Complexité Cognitive L1 à L6)
==============================================================================
Contrôle la cohérence entre le niveau de difficulté déclaré (L1 à L6) et les exigences
cognitives réelles de la tâche :
- L1 : consultation / lookup unitaire
- L2 : compréhension / inventaire direct
- L3 : analyse de relation
- L4 : raisonnement multi-étapes / pédagogie
- L5 : expertise / critique argumentée
- L6 : arbitrage de plusieurs contraintes réelles contradictoires
Toute incohérence majeure est orientée vers REVIEW.
"""

from .base_validator import BaseValidator
from ..schema import SupervisedExample, QualityStatus, QualityCheckResult, DifficultyLevel


class DifficultyValidator(BaseValidator):
    """Vérificateur de calibration du niveau de difficulté."""

    @property
    def name(self) -> str:
        return "DifficultyValidator"

    def validate(self, example: SupervisedExample) -> QualityCheckResult:
        ttype = example.task_type
        diff = example.difficulty

        # 1. CLEARANCE_CHECK : consultation unitaire d'un standard -> surcoté si > L2
        if ttype == "CLEARANCE_CHECK" and diff in (DifficultyLevel.L3, DifficultyLevel.L4, DifficultyLevel.L5, DifficultyLevel.L6):
            return QualityCheckResult(
                validator_name=self.name,
                status=QualityStatus.WARNING,
                message=f"Surévaluation de difficulté : '{ttype}' est une requête de cote unitaire (L1/L2), mais étiqueté {diff.value}",
                details={"declared_difficulty": diff.value, "expected_range": ["L1_RECONNAISSANCE", "L2_COMPREHENSION"]},
            )

        # 2. Tâche L6 multicontrainte sans contraintes explicites
        if diff == DifficultyLevel.L6:
            has_constraints = bool(example.constraints and len(example.constraints) >= 2)
            has_tradeoff_axes = bool(example.ground_truth.get("tradeoff_axes") and len(example.ground_truth.get("tradeoff_axes", [])) >= 2)
            if not (has_constraints or has_tradeoff_axes):
                return QualityCheckResult(
                    validator_name=self.name,
                    status=QualityStatus.WARNING,
                    message="Difficulté L6 déclarée sans matrice de contraintes réelles contradictoires (au moins 2 requises)",
                    details={"declared_difficulty": diff.value, "has_constraints": has_constraints, "has_tradeoff_axes": has_tradeoff_axes},
                )

        return QualityCheckResult(
            validator_name=self.name,
            status=QualityStatus.PASS,
            message="Niveau de difficulté cohérent avec la structure cognitive de la tâche",
            details={"difficulty": diff.value},
        )
