# -*- coding: utf-8 -*-
"""
ARCHI-AI — STEP 7: Multidimensional Quality Scoring Engine
==========================================================
Évalue chaque asset selon 8 dimensions explicables :
1. visual_quality (résolution, mode couleur, lisibilité)
2. structural_quality (cohérence géométrique, validité syntaxique)
3. metadata_quality (exhaustivité des métadonnées requises)
4. semantic_quality (cohérence sens/étiquette, détection d'anomalies de cotes)
5. provenance_quality (lignage jusqu'à l'archive RAW source)
6. legal_quality (licence libre / absence de restriction NC)
7. duplication_quality (unicité ou statut canonique confirmé)
8. parse_quality (absence d'erreur au chargement)

Calcule overall_quality_score de façon pondérée et explicite.
"""

from typing import Dict, Any, Tuple
from .config import QUALITY_PASS_THRESHOLD, QUALITY_CRITICAL_DIM_MIN
from .schema import RawAssetRecord, QualityDimensions, QualityStatus, LegalStatus


class QualityScorer:
    """Calculateur de scores qualité multidimensionnels."""

    # Poids des dimensions pour le score composite global
    WEIGHTS = {
        "visual_quality": 0.15,
        "structural_quality": 0.15,
        "metadata_quality": 0.15,
        "semantic_quality": 0.15,
        "provenance_quality": 0.10,
        "legal_quality": 0.15,
        "duplication_quality": 0.10,
        "parse_quality": 0.05,
    }

    def score_asset(self, record: RawAssetRecord, metadata: Dict[str, Any]) -> QualityDimensions:
        """Calcule les 8 scores dimensionnels pour un asset."""
        notes = []

        # 1. Visual Quality
        visual = 1.0
        if record.category.value in ["images", "architecture_2d"]:
            w = metadata.get("width", 0) or 0
            h = metadata.get("height", 0) or 0
            if w < 256 or h < 256:
                visual = 0.50
                notes.append("Basse résolution (< 256px)")
            elif w >= 1024 and h >= 768:
                visual = 1.0
            else:
                visual = 0.85
        elif record.category.value in ["architecture_3d"]:
            visual = 0.95
        else:
            visual = 1.0

        # 2. Structural Quality
        structural = 1.0
        if record.category.value == "architecture_3d" and record.extension == ".ifc":
            counts = metadata.get("elements_count", {})
            total_elements = sum(counts.values()) if isinstance(counts, dict) else 0
            if total_elements == 0:
                structural = 0.50
                notes.append("Maquette IFC sans entités reconnues")
            else:
                structural = 1.0
        elif record.category.value == "architecture_2d":
            if metadata.get("unscaled_pixel_anomaly", False):
                structural = 0.60
                notes.append("Anomalie critique : surfaces en pixels bruts non calibrées en m²")
            else:
                structural = 0.95

        # 3. Metadata Quality
        meta_score = 1.0
        if not metadata.get("parse_success", False):
            meta_score = 0.40
            notes.append("Échec de parsing des métadonnées")
        elif record.category.value in ["images", "architecture_2d"] and not metadata.get("width"):
            meta_score = 0.60
            notes.append("Dimensions absentes des métadonnées")

        # 4. Semantic Quality
        semantic = 1.0
        if metadata.get("unscaled_pixel_anomaly", False):
            semantic = 0.50
            notes.append("Déficit sémantique : risque d'hallucination d'ordre de grandeur")

        # 5. Provenance Quality
        provenance = 1.0 if record.provenance_status == "VERIFIED" else 0.50

        # 6. Legal Quality
        if record.legal_status == LegalStatus.APPROVED:
            legal = 1.0
        elif record.legal_status in [LegalStatus.LEGAL_REVIEW_REQUIRED, LegalStatus.RESTRICTED]:
            legal = 0.20
            notes.append(f"Statut juridique restrictif ({record.license})")
        else:
            legal = 0.50
            notes.append("Licence non formellement confirmée")

        # 7. Duplication Quality
        if record.canonical:
            duplication = 1.0
        else:
            duplication = 0.60
            notes.append(f"Asset marqué comme doublon secondaire (groupe: {record.duplicate_group_id})")

        # 8. Parse Quality
        parse_q = 1.0 if metadata.get("parse_success", True) else 0.20

        # Score global pondéré
        overall = (
            visual * self.WEIGHTS["visual_quality"]
            + structural * self.WEIGHTS["structural_quality"]
            + meta_score * self.WEIGHTS["metadata_quality"]
            + semantic * self.WEIGHTS["semantic_quality"]
            + provenance * self.WEIGHTS["provenance_quality"]
            + legal * self.WEIGHTS["legal_quality"]
            + duplication * self.WEIGHTS["duplication_quality"]
            + parse_q * self.WEIGHTS["parse_quality"]
        )

        return QualityDimensions(
            visual_quality=round(visual, 3),
            structural_quality=round(structural, 3),
            metadata_quality=round(meta_score, 3),
            semantic_quality=round(semantic, 3),
            provenance_quality=round(provenance, 3),
            legal_quality=round(legal, 3),
            duplication_quality=round(duplication, 3),
            parse_quality=round(parse_q, 3),
            overall_quality_score=round(overall, 3),
            evaluation_notes=notes,
        )

    def determine_status(self, scores: QualityDimensions) -> QualityStatus:
        """Détermine le statut qualité final selon les seuils stricts."""
        # Seuil critique bloquant
        min_dim = min([
            scores.visual_quality,
            scores.structural_quality,
            scores.metadata_quality,
            scores.semantic_quality,
            scores.provenance_quality,
            scores.legal_quality,
            scores.duplication_quality,
            scores.parse_quality,
        ])
        if scores.legal_quality < 0.30:
            return QualityStatus.REVIEW
        if min_dim < QUALITY_CRITICAL_DIM_MIN:
            return QualityStatus.WARNING
        if scores.overall_quality_score >= QUALITY_PASS_THRESHOLD:
            return QualityStatus.PASS
        return QualityStatus.REVIEW
