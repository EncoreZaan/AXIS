# -*- coding: utf-8 -*-
"""
ARCHI-AI — CritiqueEngine (Moteur de Critique de Studio & Pédagogie Maïeutique)
=============================================================================
Implémente le cœur de l'expertise critique d'ARCHI-AI :
- Diagnostic argumenté sans flatterie sycophante
- Détection des points de friction et conflits d'agencement
- Séparation explicite faits tangibles (Observation) vs jugement de composition
- Recommandations d'arbitrage et alternatives concrètes
- Posturation pédagogique de tuteur d'atelier (maïeutique guidée)
"""

from typing import Dict, Any, List, Optional, Tuple
from ..schema import EpistemicTag


class CritiqueEngine:
    """Moteur de diagnostic critique et pédagogique pour projets d'architecture intérieure."""

    @staticmethod
    def format_structured_response(
        observation: str,
        analyse: str,
        raisonnement: str,
        probleme: Optional[str] = None,
        recommandation: Optional[str] = None,
        limites: Optional[str] = None,
    ) -> str:
        """
        Formate une réponse experte selon la structure canonique recommandée :
        Observation → Analyse → Raisonnement → Problème éventuel → Recommandation → Limites / vérification.
        """
        sections = [
            f"**Observation factuelle :**\n{observation}",
            f"**Analyse spatiale :**\n{analyse}",
            f"**Raisonnement architectural :**\n{raisonnement}",
        ]
        if probleme:
            sections.append(f"**Point de friction / Faiblesse identifiée :**\n{probleme}")
        if recommandation:
            sections.append(f"**Recommandation / Piste d'optimisation :**\n{recommandation}")
        if limites:
            sections.append(f"**Limites & Éléments à vérifier in situ :**\n{limites}")

        return "\n\n".join(sections)

    @staticmethod
    def build_maieutic_dialogue(
        observed_friction: str,
        clue_question: str,
        guiding_principle: str,
        follow_up_step: str,
    ) -> str:
        """
        Génère une réponse maïeutique guidée (STUDIO TUTOR) qui stimule l'étudiant
        sans donner immédiatement la solution clé en main.
        """
        return (
            f"**Constat d'atelier :**\n{observed_friction}\n\n"
            f"**Piste de réflexion guidée :**\n{clue_question}\n\n"
            f"**Principe fondamental à mobiliser :**\n{guiding_principle}\n\n"
            f"**Exercice recommandé :**\n{follow_up_step}"
        )

    @staticmethod
    def build_epistemic_breakdown(
        observations: List[str],
        interpretations: List[str],
        inferences: Optional[List[str]] = None,
        unknowns: Optional[List[str]] = None,
        to_verifys: Optional[List[str]] = None,
    ) -> Dict[str, List[str]]:
        """Construit le dictionnaire de ventilation épistémique rigoureux."""
        breakdown: Dict[str, List[str]] = {
            EpistemicTag.OBSERVATION.value: observations,
            EpistemicTag.INTERPRETATION.value: interpretations,
        }
        if inferences:
            breakdown[EpistemicTag.INFERENCE.value] = inferences
        if unknowns:
            breakdown[EpistemicTag.UNKNOWN.value] = unknowns
        if to_verifys:
            breakdown[EpistemicTag.TO_VERIFY.value] = to_verifys
        return breakdown
