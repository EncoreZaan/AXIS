# -*- coding: utf-8 -*-
"""
ARCHI-AI — Préprocesseur Canonique Éclairage & Panoramas HDRI
============================================================
Normalise les 997 ambiances lumineuses calibrées Poly Haven :
- Température de couleur (Kelvin / balance des blancs)
- Capacité dynamique (EV - Exposure Value)
- Typologie d'environnement (intérieur, extérieur, studio, ciel)
- Résolution maximale et aperçus visuels
- Routage : MULTIUSE (FINETUNE + RAG)
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
    HdriLightingItem
)


class PolyHavenLightingPreprocessor(BasePreprocessor):
    """Adaptateur de normalisation pour CORE_POLYHAVEN_LIGHTING."""

    @property
    def source_name(self) -> str:
        return "CORE_POLYHAVEN_LIGHTING"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.LIGHTING_HDRI

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.MULTIUSE

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        raw_rel = "core/lighting/polyhaven/hdris_catalog.json"
        cat_path = self.raw_root / raw_rel

        if not cat_path.exists():
            self.errors.append(f"Fichier introuvable: {cat_path}")
            self.end_time = time.time()
            return

        with open(cat_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)

        keys = list(catalog.keys())
        if limit is not None:
            keys = keys[:limit]

        for hdri_id in keys:
            self.items_processed += 1
            info = catalog[hdri_id]

            name = info.get("name", hdri_id)
            attrs = info.get("attributes", {})
            env_type = attrs.get("environment", "unknown")
            time_of_day = attrs.get("time_of_day")
            kelvin = info.get("whitebalance")
            ev = float(info.get("evs_cap")) if info.get("evs_cap") is not None else None
            max_res = info.get("max_resolution")

            hdri_item = HdriLightingItem(
                hdri_id=hdri_id,
                name=name,
                environment_type=env_type,
                kelvin_temperature=kelvin,
                ev=ev,
                max_resolution=max_res,
                time_of_day=time_of_day,
                preview_path=info.get("thumbnail_url"),
                attributes=attrs
            )

            norm_id = f"NORM_HDRI_{hdri_id}"
            master_id = f"ARCHI_MASTER_HDRI_{hdri_id}"

            provenance = self.build_provenance(
                raw_file_rel=raw_rel,
                raw_element_id=hdri_id,
                normalized_id=norm_id,
                master_id=master_id,
                transformation_name="PolyHavenLightingPreprocessor.hdri_extractor",
                notes=f"HDRI {name} ({kelvin}K, EV {ev}, {env_type})"
            )

            item = MasterCanonicalItem(
                id=master_id,
                source_id=hdri_id,
                source_name=self.source_name,
                source_license="CC0",
                modality=self.modality,
                data_type="hdri_lighting_spec",
                domain="lighting",
                routing=self.default_routing,
                quality_status=QualityStatus.PASS,
                provenance=provenance,
                lighting=hdri_item,
                metadata={
                    "tags": info.get("tags", []),
                    "categories": info.get("categories", []),
                    "coords": info.get("coords")
                }
            )

            self.items_passed += 1
            yield item

        self.end_time = time.time()
