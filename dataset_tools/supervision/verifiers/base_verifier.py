# -*- coding: utf-8 -*-
"""
ARCHI-AI — Classe Abstraite BaseVerifier
========================================
Interface de base pour les vérificateurs déterministes.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple


class BaseVerifier(ABC):
    """Classe de base pour tout vérificateur déterministe."""

    @abstractmethod
    def verify(self, claim: Any, ground_truth_context: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Vérifie une assertion face au contexte déterministe réel.
        Retourne : (is_valid: bool, reason: str, verified_metrics: dict)
        """
        pass
