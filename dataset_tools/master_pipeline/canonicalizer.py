# -*- coding: utf-8 -*-
"""
ARCHI-AI — STEP 8: Canonical Record Builder
===========================================
Génère les enregistrements canoniques normalisés conformément au schéma officiel.
Assure la conformité exacte des champs requis et l'immuabilité des identifiants.
"""

from typing import Dict, Any, List
from .schema import RawAssetRecord, CanonicalAssetRecord, QualityDimensions


def build_canonical_record(
    raw_record: RawAssetRecord,
    metadata: Dict[str, Any],
    quality_scores: QualityDimensions,
    transformations: List[Dict[str, Any]],
    project_group_id: str,
) -> CanonicalAssetRecord:
    """Construit un CanonicalAssetRecord unifié à partir des analyses amont."""
    return CanonicalAssetRecord(
        asset_id=raw_record.asset_id,
        source_path=raw_record.relative_path,
        sha256=raw_record.sha256,
        asset_type=raw_record.category.value,
        asset_subtype=raw_record.subtype.value,
        source_dataset=raw_record.source_dataset,
        license=raw_record.license,
        legal_status=raw_record.legal_status,
        quality_status=raw_record.quality_status,
        classification_status="CANONICAL_CONFIRMED" if raw_record.canonical else "SECONDARY_DUPLICATE",
        provenance_status=raw_record.provenance_status,
        duplicate_group_id=raw_record.duplicate_group_id,
        canonical=raw_record.canonical,
        derived_from=[raw_record.asset_id],
        transformations=transformations,
        project_group_id=project_group_id,
        quality_scores=quality_scores,
        metadata=metadata,
    )
