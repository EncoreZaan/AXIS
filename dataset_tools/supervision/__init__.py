# -*- coding: utf-8 -*-
"""
ARCHI-AI — Supervision Engine Module
====================================
Ce module gère la transformation du Master Dataset en données supervisées
de haute qualité pour le fine-tuning multimodal, l'indexation RAG, et les outils déterministes.
"""

from .schema import SupervisedExample, EpistemicTag, DifficultyLevel, QualityStatus, RoutingType
from .task_catalogue import TASK_CATALOGUE, TaskDefinition, TaskGroup
from .mapping_matrix import SOURCE_CAPABILITY_TASK_MATRIX, resolve_tasks_for_record

__all__ = [
    "SupervisedExample",
    "EpistemicTag",
    "DifficultyLevel",
    "QualityStatus",
    "RoutingType",
    "TASK_CATALOGUE",
    "TaskDefinition",
    "TaskGroup",
    "SOURCE_CAPABILITY_TASK_MATRIX",
    "resolve_tasks_for_record",
]
