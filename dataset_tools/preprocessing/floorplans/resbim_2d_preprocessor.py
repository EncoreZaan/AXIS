# -*- coding: utf-8 -*-
"""
ARCHI-AI — Préprocesseur ResBIM 2D
==================================
Normalise les 10 plans architecturaux 2D appariés aux maquettes 3D IFC de ResBIM :
- Plans matriciels JPG haute résolution
- Lien explicite vers la maquette numérique 3D appariée
- Routage : MULTIUSE (FINETUNE + TOOL)
"""

from typing import Iterator, Dict, Any, List, Optional
from pathlib import Path
import time
from PIL import Image

from dataset_tools.preprocessing.base import BasePreprocessor
from dataset_tools.preprocessing.schema import (
    MasterCanonicalItem,
    ModalityType,
    RoutingType,
    QualityStatus,
    VisualMetadata
)


class ResBim2DPreprocessor(BasePreprocessor):
    """Adaptateur pour les plans 2D appariés de CORE_RESBIM_PAIRED."""

    @property
    def source_name(self) -> str:
        return "CORE_RESBIM_PAIRED"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.FLOORPLAN_2D

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.MULTIUSE

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        resbim_dir = self.raw_root / "core/resbim"
        if not resbim_dir.exists():
            self.errors.append(f"Répertoire introuvable: {resbim_dir}")
            self.end_time = time.time()
            return

        jpg_files = sorted(list(resbim_dir.glob("*.jpg")))
        if limit is not None:
            jpg_files = jpg_files[:limit]

        for jpg_path in jpg_files:
            self.items_processed += 1
            unit_id = jpg_path.stem
            ifc_path = resbim_dir / f"{unit_id}.ifc"

            width, height = None, None
            try:
                with Image.open(jpg_path) as img:
                    width, height = img.size
            except Exception as e:
                self.warnings.append(f"Erreur lecture image {jpg_path.name}: {e}")

            norm_id = f"NORM_RESBIM_2D_{unit_id}"
            master_id = f"ARCHI_MASTER_RESBIM_2D_{unit_id}"

            provenance = self.build_provenance(
                raw_file_rel=f"core/resbim/{jpg_path.name}",
                raw_element_id=unit_id,
                normalized_id=norm_id,
                master_id=master_id,
                transformation_name="ResBim2DPreprocessor.plan_extractor",
                notes=f"Plan 2D apparié à la maquette 3D {unit_id}.ifc"
            )

            visual = VisualMetadata(
                path=f"dataset/raw/external/core/resbim/{jpg_path.name}",
                width=width,
                height=height,
                format="jpg",
                caption=f"Plan d'architecte résidentiel 2D apparié {unit_id}",
                role="primary_plan_2d"
            )

            item = MasterCanonicalItem(
                id=master_id,
                source_id=unit_id,
                source_name=self.source_name,
                source_license="MIT",
                modality=self.modality,
                data_type="paired_plan_2d",
                domain="architecture",
                routing=self.default_routing,
                quality_status=QualityStatus.PASS,
                provenance=provenance,
                visual=visual,
                metadata={
                    "paired_ifc_model": f"dataset/raw/external/core/resbim/{unit_id}.ifc" if ifc_path.exists() else None,
                    "unit_name": unit_id
                }
            )

            self.items_passed += 1
            yield item

        self.end_time = time.time()
