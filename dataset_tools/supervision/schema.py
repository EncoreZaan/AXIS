# -*- coding: utf-8 -*-
"""
ARCHI-AI — Schéma Strict de Donnée Supervisée (Supervision Schema V1)
=====================================================================
Définit le standard formel pour tout exemple supervisé généré par le moteur.
Garantit la traçabilité complète, le statut épistémique, la séparation
observation/interprétation/inférence, l'ancrage déterministe et l'absence d'hallucination.
"""

from enum import Enum
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class EpistemicTag(str, Enum):
    """
    Qualification épistémique rigoureuse de chaque assertion dans la supervision ARCHI-AI.
    Interdit formellement de faire passer une hypothèse pour un fait avéré.
    """
    OBSERVATION = "OBSERVATION"      # Directement visible ou mesurable sur le document (factuel)
    INTERPRETATION = "INTERPRETATION"# Déduction qualitative selon les règles de l'art
    INFERENCE = "INFERENCE"          # Déduction combinatoire croisant plusieurs éléments
    UNKNOWN = "UNKNOWN"              # Information absente / non disponible dans la source
    TO_VERIFY = "TO_VERIFY"          # Requiert un calcul d'outil externe ou une vérification in situ


class DifficultyLevel(str, Enum):
    """Échelle de difficulté progressive L1 à L6 (curriculum d'apprentissage)."""
    L1 = "L1_RECONNAISSANCE"      # Qu'est-ce qui est visible ?
    L2 = "L2_COMPREHENSION"       # Organisation générale de l'espace
    L3 = "L3_ANALYSE"             # Analyse des flux, matières, ouvertures
    L4 = "L4_RAISONNEMENT"        # Pourquoi cette disposition crée-t-elle un conflit ?
    L5 = "L5_EXPERT"              # Amélioration conjointe ergonomie + lumière + matérialité
    L6 = "L6_MULTICONTRAINTE"     # Arbitrage sous faisceau de contraintes (surfaces, PMR, esthétique)


class QualityStatus(str, Enum):
    """Statut attribué par le Quality Gate."""
    PASS = "PASS"
    WARNING = "WARNING"
    REVIEW = "REVIEW"
    FAIL = "FAIL"


class RoutingDestination(str, Enum):
    """Destination cognitive de l'exemple supervisé."""
    FINETUNE = "FINETUNE"
    RAG = "RAG"
    TOOL = "TOOL"
    BENCHMARK = "BENCHMARK"
    HOLDOUT = "HOLDOUT"
    MULTIUSE = "MULTIUSE"
    SKIP = "SKIP"


RoutingType = RoutingDestination


class SplitName(str, Enum):
    """Partitions étanches de données."""
    TRAIN = "train"
    VALIDATION = "validation"
    BENCHMARK = "benchmark"
    HOLDOUT = "holdout"


class ModalInputs(BaseModel):
    """
    Conteneur d'entrées multimodales avec pointeurs précis et vérifiables.
    """
    images: List[Dict[str, Any]] = Field(default_factory=list, description="Références images réelles (path, dimensions, sha256)")
    plans: List[Dict[str, Any]] = Field(default_factory=list, description="Références plans 2D (path, dimensions, format)")
    geometries: List[Dict[str, Any]] = Field(default_factory=list, description="Géométries vectorielles réelles (polygones, cotes)")
    ifc_entities: List[Dict[str, Any]] = Field(default_factory=list, description="Entités IFC réelles (GlobalId, Class, Type)")
    materials: List[Dict[str, Any]] = Field(default_factory=list, description="Spécifications PBR réelles (maps, échelles physiques)")
    lighting: List[Dict[str, Any]] = Field(default_factory=list, description="Données d'éclairage réelles (Kelvin, EV, HDRI)")
    text_contexts: List[Dict[str, Any]] = Field(default_factory=list, description="Citations textuelles réelles (extraits, articles)")
    custom_metadata: Dict[str, Any] = Field(default_factory=dict, description="Métadonnées d'entrée additionnelles")


class QualityCheckResult(BaseModel):
    """Résultat unitaire d'un validateur de qualité."""
    validator_name: str
    status: QualityStatus
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)


class SupervisedExample(BaseModel):
    """
    Schéma canonique d'un exemple supervisé dans ARCHI-AI Dataset V1.
    Chaque instance satisfait l'ensemble des 31 exigences de supervision.
    """
    id: str = Field(..., description="Identifiant unique de l'exemple (ex: ARCHI_SUP_V1_W1_0001)")
    task_type: str = Field(..., description="Type de tâche formel du catalogue ARCHI-AI")
    task_group: str = Field(..., description="Groupe de tâches (A à L)")
    domain: str = Field(..., description="Domaine architectural principal")
    skill: str = Field(..., description="Compétence métier mobilisée")
    learning_type: str = Field(..., description="Type d'apprentissage cognitif")
    difficulty: DifficultyLevel = Field(..., description="Niveau de complexité L1 à L6")
    
    # Traçabilité et provenance (règle absolue : zéro source inconnue)
    source_ids: List[str] = Field(..., description="Identifiants des items du Master Dataset d'origine")
    source_provenance: Dict[str, Any] = Field(..., description="Détails de provenance (dataset, raw_file, sha256)")
    
    # Entrées multimodales
    inputs: ModalInputs = Field(default_factory=ModalInputs, description="Références d'entrées réelles")
    question: str = Field(..., description="Question formulée pour l'utilisateur/modèle")
    language: str = Field(default="fr", description="Langue de l'exemple ('fr' ou 'en')")
    
    # Réponse supervisée et décomposition épistémique
    answer: str = Field(..., description="Réponse experte complète, non sycophante et justifiée")
    epistemic_breakdown: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Répartition des assertions : OBSERVATION, INTERPRETATION, INFERENCE, UNKNOWN, TO_VERIFY"
    )
    expected_reasoning_type: str = Field(
        default="structured_observation_analysis",
        description="Type de structure de raisonnement attendu (ex: studio_critique, deductive, maieutic)"
    )
    
    # Vérité terrain déterministe et contraintes (règle absolue : zéro hallucination)
    ground_truth: Dict[str, Any] = Field(
        default_factory=dict,
        description="Faits mesurables certifiés par vérificateurs déterministes (surfaces m2, distances, counts)"
    )
    constraints: List[str] = Field(
        default_factory=list,
        description="Contraintes actives (PMR, ERP, triangle d'activité, passage utile)"
    )
    evidence: Dict[str, Any] = Field(
        default_factory=dict,
        description="Preuves et ancrages tangibles (polygones, propriétés IFC, références RAG)"
    )
    uncertainty: Optional[str] = Field(
        default=None,
        description="Explicitation obligatoire des limites, incertitudes ou données non observées"
    )
    
    # Validation Qualité et Audit
    quality_status: QualityStatus = Field(default=QualityStatus.PASS, description="Statut de certification")
    review_status: str = Field(default="APPROVED_AUTOMATED", description="APPROVED_AUTOMATED, REVIEW_QUEUE, REJECTED")
    quality_checks: List[QualityCheckResult] = Field(default_factory=list, description="Résultats détaillés des validateurs")
    
    # Partitionnement étanche et routage cognitif
    split: SplitName = Field(default=SplitName.TRAIN, description="train, validation, benchmark, holdout")
    destination: RoutingDestination = Field(default=RoutingDestination.FINETUNE, description="FINETUNE, RAG, TOOL, BENCHMARK, MULTIUSE, etc.")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    @field_validator("answer")
    @classmethod
    def validate_non_empty_answer(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("SupervisedExample answer cannot be empty")
        return v

    @field_validator("question")
    @classmethod
    def validate_non_empty_question(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("SupervisedExample question cannot be empty")
        return v
