# -*- coding: utf-8 -*-
"""
ARCHI-AI — GenericAnswerValidator (Détection de Réponses Génériques & Placeholders)
==================================================================================
Identifie les réponses stéréotypées interchangeables, les placeholders non résolus
(ex: 'None m', 'NaN', 'inf'), et les clichés architecturaux appliqués sans ancrage source.
Toute réponse présentant un placeholder ou un cliché est orientée vers REVIEW ou FAIL.
"""

import re
from typing import List
from .base_validator import BaseValidator
from ..schema import SupervisedExample, QualityStatus, QualityCheckResult


class GenericAnswerValidator(BaseValidator):
    """Vérificateur d'originalité et d'ancrage spécifique des réponses."""

    CRITICAL_PLACEHOLDERS = [
        ("PLACEHOLDER_NONE", re.compile(r"\bNone\b", re.IGNORECASE)),
        ("PLACEHOLDER_NAN", re.compile(r"\bnan\b|\binf\b", re.IGNORECASE)),
        ("PLACEHOLDER_NONE_M", re.compile(r"None\s*m\b", re.IGNORECASE)),
    ]

    GENERIC_PATTERNS = [
        ("GENERIC_PLAN_READING", re.compile(r"Plan matriciel segmenté\s*:\s*parois,\s*baies et espaces délimités", re.IGNORECASE)),
        ("GENERIC_CRITIQUE_FILTER", re.compile(r"transition entre l['’]entrée et l['’]espace de vie manque de filtre spatial", re.IGNORECASE)),
        ("GENERIC_CLAUSTRA", re.compile(r"claustra ajouré ou un meuble double-face faisant office de sas", re.IGNORECASE)),
        ("GENERIC_CATHEDRAL_SALON", re.compile(r"salon cathédrale baigné de lumière", re.IGNORECASE)),
        ("GENERIC_VIS_A_VIS", re.compile(r"sont positionnés en vis-à-vis / proximité dans la même zone d'usage", re.IGNORECASE)),
        ("GENERIC_CANONIC_IFC", re.compile(r"séquence canonique\s*:\s*IfcProject\s*→\s*IfcSite\s*→\s*IfcBuilding", re.IGNORECASE)),
        ("GENERIC_GOULOT", re.compile(r"croisent simultanément au niveau du goulot central", re.IGNORECASE)),
        ("GENERIC_MATERIAL_CONTRAST", re.compile(r"L['’]association avec des matériaux lisses en contrepoint crée un contraste tactile recherché", re.IGNORECASE)),
        ("GENERIC_LIGHTING_SHADOWS", re.compile(r"L['’]apport lumineux génère des ombres nettes ou diffuses adaptées à la mise en scène spatiale", re.IGNORECASE)),
    ]

    @property
    def name(self) -> str:
        return "GenericAnswerValidator"

    def validate(self, example: SupervisedExample) -> QualityCheckResult:
        answer = example.answer
        question = example.question
        full_text = f"{question}\n{answer}"

        # 1. Détection de placeholders non résolus (critique -> REVIEW/FAIL)
        crit_matches: List[str] = []
        for label, pat in self.CRITICAL_PLACEHOLDERS:
            if pat.search(full_text):
                crit_matches.append(label)

        if crit_matches:
            return QualityCheckResult(
                validator_name=self.name,
                status=QualityStatus.REVIEW,
                message=f"Valeur placeholder non résolue détectée dans la réponse : {crit_matches}",
                details={"critical_placeholders": crit_matches},
            )

        # 2. Détection de templates stéréotypés et clichés textuels
        generic_matches: List[str] = []
        for label, pat in self.GENERIC_PATTERNS:
            if pat.search(answer):
                generic_matches.append(label)

        if generic_matches:
            return QualityCheckResult(
                validator_name=self.name,
                status=QualityStatus.WARNING,
                message=f"Formulation générique ou template répétitif détecté : {generic_matches}",
                details={"patterns_matched": generic_matches},
            )

        return QualityCheckResult(
            validator_name=self.name,
            status=QualityStatus.PASS,
            message="Réponse spécifique et ancrée, exempte de template générique",
            details={},
        )
