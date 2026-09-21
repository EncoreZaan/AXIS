#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Définitions des axes du Benchmark
===========================================
Framework d'évaluation modulaire sur les 13 axes d'architecture.
Permet d'évaluer séparément et objectivement les capacités d'un modèle VLM.
"""

from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class BenchmarkAxis(str, Enum):
    """Les 13 axes d'évaluation du Benchmark ARCHI-AI."""
    VISION = "Vision"
    SPATIAL = "Spatial"
    ERGONOMIE = "Ergonomie"
    MATERIAUX = "Matériaux"
    LUMIERE = "Lumière"
    COULEUR = "Couleur"
    STYLE = "Style"
    CIRCULATION = "Circulation"
    CRITIQUE = "Critique"
    RECOMMANDATION = "Recommandation"
    PLAN_2D = "Plan 2D"
    PEDAGOGIE = "Pédagogie"
    ANTI_HALLUCINATION = "Anti-hallucination"


class BenchmarkEvaluationMetric(BaseModel):
    """Métrique d'évaluation unitaire pour un axe."""
    axis: BenchmarkAxis
    score: float = Field(..., ge=0.0, le=10.0, description="Note sur 10")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    epistemic_caution_detected: bool = Field(default=False)
    notes: Optional[str] = None


class BenchmarkResult(BaseModel):
    """Résultat consolidé du benchmark pour un modèle ou une baseline."""
    model_name: str
    checkpoint_or_tag: str
    dataset_version: str = "v0.1-micro-baseline"
    axis_scores: Dict[str, float] = Field(default_factory=dict)
    global_score: float = Field(default=0.0)
    sample_evaluations: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
