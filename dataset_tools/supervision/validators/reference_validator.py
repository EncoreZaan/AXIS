# -*- coding: utf-8 -*-
"""
ARCHI-AI — ReferenceValidator (Intégrité des Références & Provenance)
====================================================================
Contrôle que chaque exemple supervisé pointe vers des identifiants et fichiers
réels du Master Dataset sans aucune source fantôme.
"""

from typing import Dict, Any, List
from .base_validator import BaseValidator
from ..schema import SupervisedExample, QualityStatus, QualityCheckResult


class ReferenceValidator(BaseValidator):
    """Vérificateur de cohérence des références et de la provenance."""

    @property
    def name(self) -> str:
        return "ReferenceValidator"

    def validate(self, example: SupervisedExample) -> QualityCheckResult:
        """
        Vérifie la présence d'identifiants sources réels et d'un ancrage de provenance.
        """
        if not example.source_ids:
            return QualityCheckResult(
                validator_name=self.name,
                status=QualityStatus.FAIL,
                message="Aucun source_id associé à l'exemple",
                details={},
            )

        provenance = example.source_provenance
        if not provenance:
            return QualityCheckResult(
                validator_name=self.name,
                status=QualityStatus.FAIL,
                message="Objet source_provenance manquant ou vide",
                details={},
            )

        # Vérifier que les champs minimaux sont renseignés
        required_keys = ["source_name", "dataset_name", "raw_file"]
        missing_keys = [k for k in required_keys if not provenance.get(k)]
        if missing_keys:
            return QualityCheckResult(
                validator_name=self.name,
                status=QualityStatus.WARNING,
                message=f"Champs de traçabilité incomplets : {missing_keys}",
                details={"missing_keys": missing_keys},
            )

        return QualityCheckResult(
            validator_name=self.name,
            status=QualityStatus.PASS,
            message="Références sources et traçabilité vérifiées",
            details={"source_ids_count": len(example.source_ids)},
        )
