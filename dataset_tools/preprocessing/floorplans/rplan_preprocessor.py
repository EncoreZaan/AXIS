# -*- coding: utf-8 -*-
"""
ARCHI-AI — Préprocesseur Canonique RPLAN
=======================================
Normalise les 15 000 plans d'étage matriciels segmentés de RPLAN :
- Paires image de synthèse / masque de conditionnement
- Métadonnées textuelles de segmentation
- Empreintes visuelles
- Routage : FINETUNE
"""

from typing import Iterator, Dict, Any, List, Optional
from pathlib import Path
import json
import time

from dataset_tools.preprocessing.base import BasePreprocessor
from dataset_tools.preprocessing.schema import (
    MasterCanonicalItem,
    ModalityType,
    RoutingType,
    QualityStatus,
    VisualMetadata
)


class RPlanPreprocessor(BasePreprocessor):
    """Adaptateur de normalisation pour CORE_RPLAN."""

    @property
    def source_name(self) -> str:
        return "CORE_RPLAN"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.FLOORPLAN_2D

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.FINETUNE

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        raw_rel = "core/rplan/extracted/metadata.jsonl"
        meta_path = self.raw_root / raw_rel

        if not meta_path.exists():
            self.errors.append(f"Fichier introuvable: {meta_path}")
            self.end_time = time.time()
            return

        with open(meta_path, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f):
                if limit is not None and self.items_processed >= limit:
                    break
                line = line.strip()
                if not line:
                    continue

                self.items_processed += 1
                record = json.loads(line)

                img_rel = record.get("image", "")
                cond_rel = record.get("conditioning_image", "")
                caption = record.get("text", "")
                
                # Récupérer l'identifiant numérique depuis le chemin d'image (ex: 42007)
                plan_id = Path(img_rel).stem if img_rel else str(line_idx)

                norm_id = f"NORM_RPLAN_{plan_id}"
                master_id = f"ARCHI_MASTER_RPLAN_{plan_id}"

                provenance = self.build_provenance(
                    raw_file_rel=f"core/rplan/extracted/{img_rel}",
                    raw_element_id=plan_id,
                    normalized_id=norm_id,
                    master_id=master_id,
                    transformation_name="RPlanPreprocessor.raster_plan_extractor",
                    notes="Plan matriciel segmenté 256x256 avec masque sémantique"
                )

                visual = VisualMetadata(
                    path=f"dataset/raw/external/core/rplan/extracted/{img_rel}",
                    width=256,
                    height=256,
                    format="png",
                    caption=caption,
                    role="primary_raster"
                )

                item = MasterCanonicalItem(
                    id=master_id,
                    source_id=plan_id,
                    source_name=self.source_name,
                    source_license="Open Research License",
                    modality=self.modality,
                    data_type="raster_floorplan_pair",
                    domain="architecture",
                    routing=self.default_routing,
                    quality_status=QualityStatus.PASS,
                    provenance=provenance,
                    visual=visual,
                    metadata={
                        "conditioning_image_path": f"dataset/raw/external/core/rplan/extracted/{cond_rel}",
                        "segmentation_classes": ["doors_green", "walls_red", "rooms_white", "background_gray"]
                    }
                )

                self.items_passed += 1
                yield item

        self.end_time = time.time()
