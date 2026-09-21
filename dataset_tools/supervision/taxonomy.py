# -*- coding: utf-8 -*-
"""
ARCHI-AI — Taxonomie des Compétences & Vocabulaire Contrôlé
===========================================================
Taxonomie unifiée pour le Supervision Engine :
- Compétences métier spécialisées (Skills)
- Types d'apprentissage cognitif (Learning Types dont MAIEUTIC_GUIDANCE)
- Niveaux de difficulté (L1 à L6)
- Domaines d'application
- Lexique bilingue Français / Anglais d'architecture intérieure
"""

from enum import Enum
from typing import Dict, List, Set, Optional


class SupervisionSkill(str, Enum):
    """Compétences métier ciblées par ARCHI-AI."""
    SPATIAL_REASONING = "spatial_reasoning"
    PLAN_READING = "plan_reading"
    TOPOLOGY = "topology"
    CIRCULATION = "circulation"
    ERGONOMICS = "ergonomics"
    MATERIALS = "materials"
    LIGHTING = "lighting"
    FURNITURE = "furniture"
    STYLE = "style"
    ARCHITECTURE_HISTORY = "architecture_history"
    DESIGN_HISTORY = "design_history"
    BIM = "BIM"
    IFC = "IFC"
    CONSTRUCTION = "construction"
    REGULATION = "regulation"
    CRITIQUE = "critique"
    PROBLEM_SOLVING = "problem_solving"
    VISUAL_REASONING = "visual_reasoning"
    MULTIMODAL_REASONING = "multimodal_reasoning"
    PEDAGOGICAL_EXPLANATION = "pedagogical_explanation"


class SupervisionLearningType(str, Enum):
    """Types d'apprentissage cognitif."""
    OBSERVATION = "observation"
    ANALYSIS = "analysis"
    CRITIQUE = "critique"
    ERROR_DETECTION = "error_detection"
    IMPROVEMENT = "improvement"
    ALTERNATIVES = "alternatives"
    COMPARISON = "comparison"
    CONSTRAINT_REASONING = "constraint_reasoning"
    PEDAGOGY = "pedagogy"
    MAIEUTIC_GUIDANCE = "maieutic_guidance"
    STUDIO_CRITIQUE = "studio_critique"
    METHODOLOGY = "methodology"
    DEDUCTIVE_REASONING = "deductive_reasoning"


class SupervisionDomain(str, Enum):
    """Domaines de spécialité."""
    INTERIOR_DESIGN = "interior_design"
    ARCHITECTURE = "architecture"
    ERGONOMICS = "ergonomics"
    HERITAGE_DESIGN = "heritage_design"
    MATERIALS_LIGHTING = "materials_lighting"
    BIM_CONSTRUCTION = "bim_construction"
    REGULATION_SAFETY = "regulation_safety"


# Lexique bilingue certifié pour l'architecture d'intérieur
ARCHI_BILINGUAL_LEXICON: Dict[str, Dict[str, str]] = {
    "circulation": {
        "fr": "circulation",
        "en": "circulation / traffic flow",
        "definition_fr": "Axe de déplacement des usagers au sein de l'espace bâti reliant les différentes fonctions.",
        "definition_en": "Pathway of user movement through the built environment connecting different functions.",
    },
    "degagement": {
        "fr": "dégagement / passage utile",
        "en": "clearance / clear width",
        "definition_fr": "Largeur minimale libre d'obstacle nécessaire au passage d'une personne ou d'un fauteuil roulant.",
        "definition_en": "Minimum unobstructed width required for a person or wheelchair to pass.",
    },
    "triangle_activite": {
        "fr": "triangle d'activité",
        "en": "work triangle",
        "definition_fr": "Disposition ergonomique en cuisine reliant la zone de cuisson, de lavage et de stockage réfrigéré.",
        "definition_en": "Ergonomic kitchen layout linking cooking, sink, and cold storage zones.",
    },
    "giration": {
        "fr": "espace de giration (Ø 1,50 m)",
        "en": "turning circle (Ø 1.50 m)",
        "definition_fr": "Espace libre de tout obstacle permettant à un utilisateur en fauteuil roulant d'effectuer un demi-tour.",
        "definition_en": "Clear circular area allowing a wheelchair user to perform a 180-degree turn.",
    },
    "allege": {
        "fr": "allège",
        "en": "sill wall / parapet",
        "definition_fr": "Partie de mur située entre le sol fini et l'appui de fenêtre.",
        "definition_en": "Wall section located between finished floor and window sill.",
    },
    "refend": {
        "fr": "mur de refend",
        "en": "load-bearing partition / shear wall",
        "definition_fr": "Mur porteur intérieur participant à la structure et reprenant les charges des planchers.",
        "definition_en": "Interior structural load-bearing wall supporting floors and ceilings.",
    },
    "flj": {
        "fr": "facteur de lumière du jour (FLJ)",
        "en": "daylight factor (DF)",
        "definition_fr": "Rapport entre l'éclairement naturel intérieur et l'éclairement extérieur sur surface horizontale.",
        "definition_en": "Ratio of internal illuminance to outdoor unobstructed horizontal illuminance.",
    },
    "rugosite": {
        "fr": "rugosité (roughness PBR)",
        "en": "roughness",
        "definition_fr": "Micro-relief d'une surface déterminant le caractère spéculaire ou diffus de la réflexion lumineuse.",
        "definition_en": "Micro-facet surface texture governing specular vs diffuse light reflection.",
    },
    "haussmannien": {
        "fr": "style haussmannien",
        "en": "Haussmann style",
        "definition_fr": "Vocabulaire d'appartement bourgeois parisien : moulures en stuc, parquet point de Hongrie, cheminée marbre et trumeau.",
        "definition_en": "Parisian bourgeois apartment aesthetic: plaster moldings, herringbone parquet, marble fireplace, and pier glass mirror.",
    },
    "maieutique": {
        "fr": "guidage maïeutique",
        "en": "maieutic / Socratic guidance",
        "definition_fr": "Méthode pédagogique stimulant la réflexion autonome de l'étudiant par un questionnement ciblé sans révéler immédiatement la solution.",
        "definition_en": "Pedagogical tutoring method stimulating independent student problem-solving via guided questioning without prematurely spoiling answers.",
    },
}
