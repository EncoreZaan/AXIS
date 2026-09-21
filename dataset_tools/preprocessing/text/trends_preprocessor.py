# -*- coding: utf-8 -*-
"""
ARCHI-AI — Préprocesseur Enquête Tendances 2026
===============================================
Normalise les données prospectives de tendances d'aménagement intérieur 2026 :
- Typologies de matériaux montants, palettes et styles
- Destiné au RAG et à la contextualisation contemporaine
- Routage : RAG
"""

from typing import Iterator, Dict, Any, List, Optional
from pathlib import Path
import csv
import time

from dataset_tools.preprocessing.base import BasePreprocessor
from dataset_tools.preprocessing.schema import (
    MasterCanonicalItem,
    ModalityType,
    RoutingType,
    QualityStatus
)


class Trends2026Preprocessor(BasePreprocessor):
    """Adaptateur de normalisation pour CORE_TRENDS_2026."""

    @property
    def source_name(self) -> str:
        return "CORE_TRENDS_2026"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.TRENDS

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.RAG

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        raw_rel = "core/trends/trends_2026_survey.csv"
        csv_path = self.raw_root / raw_rel

        if not csv_path.exists():
            self.errors.append(f"Fichier introuvable: {csv_path}")
            self.end_time = time.time()
            return

        with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row_idx, row in enumerate(reader):
                if limit is not None and self.items_processed >= limit:
                    break

                self.items_processed += 1
                trend_id = str(row.get("id", f"trend_{row_idx+1}"))
                theme = row.get("theme", "Design Tendances 2026")
                content_desc = row.get("description", str(row))

                norm_id = f"NORM_TREND_{trend_id}"
                master_id = f"ARCHI_MASTER_TREND_{trend_id}"

                provenance = self.build_provenance(
                    raw_file_rel=raw_rel,
                    raw_element_id=trend_id,
                    normalized_id=norm_id,
                    master_id=master_id,
                    transformation_name="Trends2026Preprocessor.row_standardizer",
                    notes=f"Tendance 2026: {theme}"
                )

                item = MasterCanonicalItem(
                    id=master_id,
                    source_id=trend_id,
                    source_name=self.source_name,
                    source_license="Internal ARCHI-AI Research",
                    modality=self.modality,
                    data_type="trend_survey_record",
                    domain="interior_design",
                    routing=self.default_routing,
                    quality_status=QualityStatus.PASS,
                    provenance=provenance,
                    metadata={
                        "theme": theme,
                        "content": content_desc,
                        "raw_row": row
                    }
                )

                self.items_passed += 1
                yield item

        self.end_time = time.time()
