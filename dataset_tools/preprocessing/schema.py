# -*- coding: utf-8 -*-
"""
ARCHI-AI — Master Schema Canonique & Modèles de Normalisation
=============================================================
Définit le format pivot unifié pour toutes les modalités architecturales :
- Plans 2D & topologie spatiale
- Agencements 3D & scene graphs
- Maquettes BIM IFC
- Matériaux PBR & textures physiques
- Ambiances lumineuses HDRIs
- Réglementation & normes CCH/ERP/PMR (RAG)
- Ergonomie & cotes anthropométriques (Outils / Déterministe)
- Notices d'histoire de l'architecture & design
- Benchmark et questions/réponses multimodales
- Traçabilité complète de provenance
"""

from enum import Enum
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class RoutingType(str, Enum):
    """Destination cognitive de la donnée dans l'écosystème ARCHI-AI."""
    FINETUNE = "FINETUNE"          # Pour entraînement VLM des poids (perception, critique, agencement)
    RAG = "RAG"                    # Pour indexation documentaire BM25 / vectorielle (lois, monographies)
    TOOL = "TOOL"                  # Pour solveurs déterministes (calculs métriques, graphes, cotes)
    BENCHMARK = "BENCHMARK"        # Sanctuarisé pour évaluation aveugle (MMMU, test sets)
    HOLDOUT = "HOLDOUT"            # Jeu de réserve inaccessible en apprentissage
    MULTIUSE = "MULTIUSE"          # Exploitable simultanément (ex: FINETUNE + TOOL)


class ModalityType(str, Enum):
    """Modalité technique de la donnée normalisée."""
    FLOORPLAN_2D = "floorplan_2d"
    SPATIAL_3D = "spatial_3d"
    BIM_IFC = "bim_ifc"
    MATERIAL_PBR = "material_pbr"
    LIGHTING_HDRI = "lighting_hdri"
    REGULATORY_TEXT = "regulatory_text"
    ERGONOMICS = "ergonomics"
    HISTORICAL_DESIGN = "historical_design"
    MULTIMODAL_QA = "multimodal_qa"
    TRENDS = "trends"


class QualityStatus(str, Enum):
    """Statut de certification qualité de la donnée."""
    PASS = "PASS"
    WARNING = "WARNING"
    REVIEW = "REVIEW"
    FAIL = "FAIL"


class ProvenanceRecord(BaseModel):
    """Traçabilité immuable remontant jusqu'à la source RAW originale."""
    source_name: str = Field(..., description="Nom officiel de la source (ex: CORE_RESPLAN)")
    dataset_name: str = Field(..., description="Sous-ensemble ou dataset (ex: ResPlan)")
    raw_file: str = Field(..., description="Chemin relatif vers le fichier RAW source")
    raw_element_id: str = Field(..., description="Identifiant natif d'origine dans le fichier RAW")
    transformation: str = Field(..., description="Nom de la transformation / adaptateur appliqué")
    normalized_id: str = Field(..., description="Identifiant unique normalisé")
    master_id: str = Field(..., description="Identifiant assigné dans le Master Dataset")
    raw_sha256: Optional[str] = Field(default=None, description="SHA-256 du fichier RAW parent")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    notes: Optional[str] = Field(default=None)


class VisualMetadata(BaseModel):
    """Métadonnées associées à un fichier image ou document visuel."""
    path: str = Field(..., description="Chemin relatif vers l'image dans ARCHI_AI")
    width: Optional[int] = Field(default=None)
    height: Optional[int] = Field(default=None)
    format: Optional[str] = Field(default=None)
    sha256: Optional[str] = Field(default=None)
    phash: Optional[str] = Field(default=None)
    caption: Optional[str] = Field(default=None)
    role: str = Field(default="primary")


class PlanRoom(BaseModel):
    """Description structurée d'une pièce dans un plan 2D."""
    name: str = Field(..., description="Label de la pièce (ex: bedroom, living, kitchen)")
    category: Optional[str] = Field(default=None)
    polygon: Optional[List[List[float]]] = Field(default=None, description="Coordonnées 2D [[x1, y1], [x2, y2], ...]")
    area_m2: Optional[float] = Field(default=None, description="Surface réelle métrique en m2 (non inventée)")
    bounds: Optional[List[float]] = Field(default=None, description="[minx, miny, maxx, maxy]")
    connected_rooms: List[str] = Field(default_factory=list, description="Pièces adjacentes ou connectées")


class PlanOpening(BaseModel):
    """Ouverture (porte, fenêtre) dans une paroi."""
    type: str = Field(..., description="door, front_door, window")
    coordinates: Optional[List[List[float]]] = Field(default=None)
    connects: List[str] = Field(default_factory=list, description="Labels des pièces reliées")
    width_m: Optional[float] = Field(default=None)


class PlanGeometry(BaseModel):
    """Représentation géométrique canonique d'un plan d'étage."""
    plan_id: str
    rooms: List[PlanRoom] = Field(default_factory=list)
    walls: List[Dict[str, Any]] = Field(default_factory=list)
    openings: List[PlanOpening] = Field(default_factory=list)
    total_area_m2: Optional[float] = Field(default=None)
    net_area_m2: Optional[float] = Field(default=None)
    scale: Optional[str] = Field(default=None, description="Échelle du plan si connue, sinon null")
    coordinate_unit: str = Field(default="meter", description="Unité des coordonnées (meter, pixel, uncalibrated)")
    room_adjacency_graph: Dict[str, List[str]] = Field(default_factory=dict, description="Graphe topologique de circulation")
    unknown_fields: List[str] = Field(default_factory=list, description="Champs manquants dans le RAW documentés")


class SpatialObject(BaseModel):
    """Objet 3D dans un agencement spatial."""
    object_id: str
    category: str
    label: Optional[str] = None
    position: List[float] = Field(..., description="[x, y, z] en mètres")
    rotation: List[float] = Field(..., description="[rx, ry, rz] en degrés ou radians")
    dimensions: List[float] = Field(..., description="[dx, dy, dz] bounding box en mètres")
    room_id: Optional[str] = None
    kinematic: Optional[bool] = None
    asset_id: Optional[str] = None


class SpatialScene(BaseModel):
    """Scène 3D complète avec scene graph relationnel."""
    scene_id: str
    rooms: List[str] = Field(default_factory=list)
    objects: List[SpatialObject] = Field(default_factory=list)
    scene_graph: Dict[str, Any] = Field(default_factory=dict, description="Relations spatiales (contains, adjacent, on_top_of)")
    total_objects: int = 0
    coordinate_convention: str = Field(default="Y-up, right-handed", description="Convention du repère 3D")


class BimModelSummary(BaseModel):
    """Résumé canonique d'une maquette numérique BIM / IFC."""
    model_id: str
    ifc_schema: str = Field(..., description="IFC2X3, IFC4, IFC4X3")
    project_name: Optional[str] = None
    site_name: Optional[str] = None
    building_name: Optional[str] = None
    storeys: List[str] = Field(default_factory=list)
    spaces: List[str] = Field(default_factory=list)
    element_counts: Dict[str, int] = Field(default_factory=dict, description="Décompte par classe IfcWall, IfcDoor, etc.")
    walls_count: int = 0
    doors_count: int = 0
    windows_count: int = 0
    slabs_count: int = 0
    columns_count: int = 0
    furnishing_count: int = 0
    materials_declared: List[str] = Field(default_factory=list)
    properties_extracted: Dict[str, Any] = Field(default_factory=dict)


class PbrMaterialItem(BaseModel):
    """Matériau PBR physique et texture."""
    material_id: str
    name: str
    category: str
    tags: List[str] = Field(default_factory=list)
    physical_scale_m: Optional[List[float]] = Field(default=None, description="Dimensions réelles [largeur, hauteur] en mètres")
    maps_available: List[str] = Field(default_factory=list, description="color, normal, roughness, displacement, etc.")
    preview_url: Optional[str] = None
    thumbnail_path: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)


class HdriLightingItem(BaseModel):
    """Panorama d'ambiance lumineuse calibrée HDRI."""
    hdri_id: str
    name: str
    environment_type: str = Field(..., description="indoor, outdoor, studio, nature")
    kelvin_temperature: Optional[int] = Field(default=None, description="Température de couleur en Kelvin (balance des blancs)")
    ev: Optional[float] = Field(default=None, description="Exposure Value de la scène")
    max_resolution: Optional[List[int]] = Field(default=None, description="[width, height] px")
    time_of_day: Optional[str] = None
    preview_path: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)


class RegulatoryArticle(BaseModel):
    """Article ou section réglementaire consolidée (RAG)."""
    article_id: str
    document: str = Field(..., description="Nom de l'arrêté, loi ou code (CCH, Arrêté PMR, Arrêté ERP)")
    theme: str = Field(..., description="Accessibilité PMR, Dégagements ERP, Habitabilité CCH")
    jurisdiction: str = Field(default="France")
    section: Optional[str] = None
    article_number: Optional[str] = None
    official_source: str = Field(default="Journal Officiel / Légifrance")
    version_date: Optional[str] = None
    text: str = Field(..., description="Texte officiel exact inaltéré")
    references: List[str] = Field(default_factory=list)
    language: str = Field(default="fr")


class ErgonomicStandard(BaseModel):
    """Règle dimensionnelle anthropométrique certifiée (TOOL / RAG)."""
    standard_id: str
    space_category: str = Field(..., description="circulations, cuisine, chambre, salle_de_bain, mobilier")
    object_or_usage: str = Field(..., description="Élément mesuré (ex: couloir_personne_seule)")
    original_value: Union[float, int, List[Union[float, int]]] = Field(..., description="Valeur originale inaltérée")
    original_unit: str = Field(..., description="cm, m, mm")
    normalized_si_value: Union[float, List[float]] = Field(..., description="Valeur normalisée en mètres (SI certifié)")
    normalized_si_unit: str = Field(default="m")
    context: Optional[str] = None
    population: str = Field(default="adulte_standard_et_pmr")
    source: str = Field(default="Neufert / Panero & Zelnik")
    min_value: Optional[float] = None
    recommended_value: Optional[float] = None
    remarks: Optional[str] = None


class MuseumArtworkRecord(BaseModel):
    """Notice patrimoniale d'architecture et design (RAG)."""
    record_id: str
    institution: str = Field(..., description="MoMA ou The Met")
    title: str
    artist_or_designer: Optional[str] = None
    artist_bio: Optional[str] = None
    nationality: Optional[str] = None
    creation_date: Optional[str] = None
    medium: Optional[str] = None
    dimensions_raw: Optional[str] = None
    classification: Optional[str] = None
    department: Optional[str] = None
    image_url: Optional[str] = None
    object_url: Optional[str] = None
    language: str = Field(default="en")


class MultimodalQAPair(BaseModel):
    """Paire question/réponse multimodale experte (Benchmark ou Train)."""
    qa_id: str
    question: str
    answer: str
    options: Optional[List[str]] = None
    ground_truth: Optional[str] = None
    explanation: Optional[str] = None
    image_path: Optional[str] = None
    category: str
    difficulty: str = Field(default="intermediate")
    source_benchmark: str = Field(..., description="IFC-Bench, MMMU Architecture")
    split_assignment: str = Field(default="train", description="train, validation, test")
    is_benchmark_holdout: bool = Field(default=False, description="True si sanctuarisé hors entraînement")


class MasterCanonicalItem(BaseModel):
    """
    Conteneur pivot universel d'ARCHI-AI.
    Chaque enregistrement du Master Dataset Intermédiaire instancie ce schéma.
    """
    id: str = Field(..., description="Identifiant unique pivot ARCHI-AI (ex: ARCHI_NORM_RESPLAN_00001)")
    source_id: str = Field(..., description="Identifiant dans la source d'origine")
    source_name: str = Field(..., description="Nom de la source originale")
    source_license: str = Field(..., description="Licence d'utilisation vérifiée")
    modality: ModalityType = Field(..., description="Modalité principale")
    data_type: str = Field(..., description="Type de données (vector, mesh, text, qa, material...)")
    domain: str = Field(default="architecture", description="architecture, interior_design, bim, heritage...")
    routing: RoutingType = Field(..., description="Destination cognitive principale (FINETUNE, RAG, TOOL, BENCHMARK...)")
    quality_status: QualityStatus = Field(default=QualityStatus.PASS)
    provenance: ProvenanceRecord = Field(..., description="Chaîne complète de provenance RAW")
    
    # Données spécialisées selon la modalité (optionnelles, une seule est peuplée par item)
    visual: Optional[VisualMetadata] = None
    floorplan: Optional[PlanGeometry] = None
    spatial: Optional[SpatialScene] = None
    bim: Optional[BimModelSummary] = None
    material: Optional[PbrMaterialItem] = None
    lighting: Optional[HdriLightingItem] = None
    regulatory: Optional[RegulatoryArticle] = None
    ergonomics: Optional[ErgonomicStandard] = None
    museum: Optional[MuseumArtworkRecord] = None
    qa: Optional[MultimodalQAPair] = None
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Métadonnées libres additionnelles")
    
    @field_validator("id")
    @classmethod
    def check_id_non_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("L'identifiant id ne peut être vide.")
        return v
