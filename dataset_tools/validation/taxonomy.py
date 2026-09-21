#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Définitions des taxonomies, compétences et types d'apprentissage
==========================================================================
Vocabulaire contrôlé et taxonomies extensibles pour l'analyse d'architecture.
"""

from enum import Enum
from typing import List, Set


class DocumentType(str, Enum):
    """Types de documents visuels acceptés."""
    PHOTOGRAPHY = "photography"
    RENDER_3D = "render_3d"
    PLAN_2D = "plan_2d"
    SECTION_2D = "section_2d"
    ELEVATION_2D = "elevation_2d"
    AXONOMETRY = "axonometry"
    SKETCH = "sketch"
    MOODBOARD = "moodboard"
    TECHNICAL_DETAIL = "technical_detail"
    DIAGRAM = "diagram"


class Domain(str, Enum):
    """Domaine d'application principal."""
    ARCHITECTURE = "architecture"
    INTERIOR_DESIGN = "interior_design"
    URBANISM = "urbanism"
    LANDSCAPE = "landscape"
    HERITAGE = "heritage"


class DifficultyLevel(str, Enum):
    """Niveau de complexité de l'exemple."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class LearningType(str, Enum):
    """
    Types d'apprentissage cognitif ciblés (Phase 8).
    Chaque exemple possède un learning_type principal.
    """
    OBSERVATION = "observation"
    ANALYSIS = "analysis"
    UNKNOWN = "unknown"
    CRITIQUE = "critique"
    ERROR_DETECTION = "error_detection"
    IMPROVEMENT = "improvement"
    ALTERNATIVES = "alternatives"
    COMPARISON = "comparison"
    CONSTRAINT_REASONING = "constraint_reasoning"
    PEDAGOGY = "pedagogy"
    COUNTEREXAMPLE = "counterexample"
    REASONING = "reasoning"


class Skill(str, Enum):
    """
    Taxonomie métier des compétences d'architecture (Phase 7).
    Un exemple peut mobiliser plusieurs compétences.
    """
    VISION = "VISION"
    ESPACE = "ESPACE"
    ERGONOMIE = "ERGONOMIE"
    CIRCULATION = "CIRCULATION"
    MATERIAUX = "MATERIAUX"
    COULEUR = "COULEUR"
    LUMIERE = "LUMIERE"
    MOBILIER = "MOBILIER"
    STYLE = "STYLE"
    COMPOSITION = "COMPOSITION"
    CRITIQUE = "CRITIQUE"
    RECOMMANDATION = "RECOMMANDATION"
    PEDAGOGIE = "PEDAGOGIE"
    PLANS_2D = "PLANS_2D"


class QAStatus(str, Enum):
    """Statut QA pour le contrôle qualité et la validation humaine."""
    PASS_STATUS = "PASS"
    WARNING = "WARNING"
    REVIEW = "REVIEW"
    FAIL = "FAIL"


class SplitName(str, Enum):
    """Identifiants des partitions de données."""
    TRAIN = "train"
    VALIDATION = "validation"
    TEST = "test"


# Mappings d'aide pour les rétro-compatibilités et inférences
LEGACY_CATEGORY_TO_SKILLS = {
    "ANALYSE D'ESPACE": [Skill.ESPACE, Skill.CIRCULATION, Skill.VISION, Skill.COMPOSITION],
    "CRITIQUE ARCHITECTURALE": [Skill.CRITIQUE, Skill.RECOMMANDATION, Skill.VISION],
    "ERGONOMIE / USAGE": [Skill.ERGONOMIE, Skill.ESPACE, Skill.CIRCULATION],
    "STYLE / MATERIAUX / AMBIANCE": [Skill.STYLE, Skill.MATERIAUX, Skill.COULEUR, Skill.LUMIERE],
    "PLANS & DIAGRAMMES": [Skill.PLANS_2D, Skill.ESPACE, Skill.CIRCULATION],
    "PEDAGOGIE": [Skill.PEDAGOGIE, Skill.CRITIQUE, Skill.RECOMMANDATION],
}

BENCHMARK_AXES = [
    "Vision",
    "Spatial",
    "Ergonomie",
    "Matériaux",
    "Lumière",
    "Couleur",
    "Style",
    "Circulation",
    "Critique",
    "Recommandation",
    "Plan 2D",
    "Pédagogie",
    "Anti-hallucination"
]
