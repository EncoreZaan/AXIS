# -*- coding: utf-8 -*-
"""
ARCHI-AI — Classe Abstraite BaseGenerator
==========================================
Interface pour les générateurs de tâches de supervision.
Chaque générateur transforme des données réelles normalisées en exemples supervisés.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..schema import SupervisedExample, ModalInputs, QualityStatus, RoutingDestination, SplitName, DifficultyLevel
from ..task_catalogue import get_task_definition


class BaseGenerator(ABC):
    """Classe abstraite pour les générateurs de tâches."""

    @property
    @abstractmethod
    def supported_sources(self) -> List[str]:
        """Sources Master traitées par ce générateur."""
        pass

    @abstractmethod
    def generate(self, record: Dict[str, Any], max_examples: int = 5) -> List[SupervisedExample]:
        """
        Génère une liste d'exemples supervisés sémantiquement distincts à partir d'un record réel.
        """
        pass
