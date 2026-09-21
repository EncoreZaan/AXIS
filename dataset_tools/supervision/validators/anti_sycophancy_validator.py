# -*- coding: utf-8 -*-
"""
ARCHI-AI — AntiSycophancyValidator (Rejet de la Complaisance Décorative)
========================================================================
Interdit les flatteries superficielles non fondées et exige des diagnostics
objectifs, argumentés et équilibrés pour l'architecture d'intérieur.
"""

import re
from typing import Set, List
from .base_validator import BaseValidator
from ..schema import SupervisedExample, QualityStatus, QualityCheckResult


class AntiSycophancyValidator(BaseValidator):
    """Détecte les tournures sycophantes et creuses."""

    @property
    def name(self) -> str:
        return "AntiSycophancyValidator"

    # Expressions complaisantes proscrites
    FORBIDDEN_SYCOPHANTIC_PHRASES = [
        "très beau projet",
        "tres beau projet",
        "super ambiance",
        "c'est parfait",
        "tout est parfait",
        "magnifique projet",
        "rien à redire",
        "rien a redire",
        "absolument parfait",
        "bravo pour ce projet sans défaut",
    ]

    def validate(self, example: SupervisedExample) -> QualityCheckResult:
        """
        Vérifie l'absence de flagornerie et l'exigence d'esprit critique.
        """
        answer_lower = example.answer.lower()

        # 1. Vérification des phrases interdites
        for phrase in self.FORBIDDEN_SYCOPHANTIC_PHRASES:
            if phrase in answer_lower:
                return QualityCheckResult(
                    validator_name=self.name,
                    status=QualityStatus.FAIL,
                    message=f"Sycophantie détectée : présence de la formule complaisante proscrite '{phrase}'",
                    details={"matched_phrase": phrase},
                )

        # 2. Si c'est une tâche de type CRITIQUE ou ERROR_DETECTION
        if example.task_type in ("PROJECT_CRITIQUE", "WEAKNESS_IDENTIFICATION", "PLAN_ERROR_DETECTION", "STUDIO_CRITIQUE"):
            # Exiger des arguments concrets de point de vigilance ou de friction
            critical_markers = [
                "vigilance", "conflit", "faiblesse", "attention", "limite",
                "point noir", "perte", "goulot", "dégagement insuffisant",
                "manque", "incohérence", "obstacle", "réserve", "arbitrage", "toutefois", "cependant"
            ]
            has_critical_marker = any(marker in answer_lower for marker in critical_markers)
            if not has_critical_marker:
                return QualityCheckResult(
                    validator_name=self.name,
                    status=QualityStatus.WARNING,
                    message="Critique studio sans point de vigilance ou faiblesse identifiée (risque de complaisance)",
                    details={"task_type": example.task_type},
                )

        return QualityCheckResult(
            validator_name=self.name,
            status=QualityStatus.PASS,
            message="Ton professionnel, objectif et sans complaisance",
            details={},
        )
