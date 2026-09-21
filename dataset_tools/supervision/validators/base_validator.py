# -*- coding: utf-8 -*-
"""
ARCHI-AI — Classe Abstraite BaseValidator
==========================================
Interface de base pour les validateurs de contrôle qualité de supervision.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..schema import SupervisedExample, QualityStatus, QualityCheckResult


class BaseValidator(ABC):
    """Classe de base pour un validateur de qualité."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nom unique du validateur."""
        pass

    @abstractmethod
    def validate(self, example: SupervisedExample) -> QualityCheckResult:
        """
        Valide un exemple supervisé et retourne un QualityCheckResult.
        """
        pass
