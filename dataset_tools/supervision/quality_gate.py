# -*- coding: utf-8 -*-
"""
ARCHI-AI — QualityGate (Contrôle Qualité & Certification des Exemples)
======================================================================
Applique systématiquement la batterie complète des 7 validateurs qualitatifs :
1. ReferenceValidator (intégrité des provenances et sources)
2. HallucinationValidator (ancrage numérique et factuel)
3. EpistemicValidator (distinction observation / analyse)
4. AntiSycophancyValidator (neutralité architecturale stricte)
5. GenericAnswerValidator (détection de clichés, templates et placeholders)
6. MultimodalDependencyValidator (complétude et dépendance effective des modalités)
7. DifficultyValidator (calibration cognitive L1 à L6)

Attribution du statut final :
- PASS : Certifié conforme, prêt pour l'apprentissage
- WARNING : Valide mais point de vigilance documenté
- REVIEW : Nécessite une revue humaine avant intégration
- FAIL : Échec critique (hallucination ou sycophantie) → Exclu du training
"""

from typing import List
from .schema import SupervisedExample, QualityStatus, QualityCheckResult
from .validators.reference_validator import ReferenceValidator
from .validators.hallucination_validator import HallucinationValidator
from .validators.epistemic_validator import EpistemicValidator
from .validators.anti_sycophancy_validator import AntiSycophancyValidator
from .validators.generic_answer_validator import GenericAnswerValidator
from .validators.multimodal_dependency_validator import MultimodalDependencyValidator
from .validators.difficulty_validator import DifficultyValidator


class QualityGate:
    """Passerelle de certification qualité complète du Supervision Engine."""

    def __init__(self):
        self.validators = [
            ReferenceValidator(),
            HallucinationValidator(),
            EpistemicValidator(),
            AntiSycophancyValidator(),
            GenericAnswerValidator(),
            MultimodalDependencyValidator(),
            DifficultyValidator(),
        ]

    def evaluate(self, example: SupervisedExample) -> SupervisedExample:
        """
        Évalue un exemple supervisé à travers les 7 validateurs et met à jour son statut.
        """
        results: List[QualityCheckResult] = []
        statuses: List[QualityStatus] = []

        for validator in self.validators:
            res = validator.validate(example)
            results.append(res)
            statuses.append(res.status)

        example.quality_checks = results

        # Détermination du statut global
        if QualityStatus.FAIL in statuses:
            example.quality_status = QualityStatus.FAIL
            example.review_status = "REJECTED"
        elif QualityStatus.REVIEW in statuses:
            example.quality_status = QualityStatus.REVIEW
            example.review_status = "NEEDS_HUMAN_REVIEW"
        elif QualityStatus.WARNING in statuses:
            example.quality_status = QualityStatus.WARNING
            example.review_status = "APPROVED_WITH_WARNING"
        else:
            example.quality_status = QualityStatus.PASS
            example.review_status = "APPROVED_AUTOMATED"

        return example
