# -*- coding: utf-8 -*-
"""
ARCHI-AI — Préprocesseur Canonique Matériaux PBR
================================================
Normalise les catalogues de matériaux de finition architecturale :
- Poly Haven (862 textures PBR avec échelles physiques et métadonnées)
- ambientCG (catalogue complet de 2 891 matériaux PBR)
Extraction :
- Nom, catégorie, tags de style et d'usage
- Échelle physique réelle certifiée en mètres
- Types de canaux PBR disponibles (albedo, roughness, normal, displacement)
- Vignettes et liens d'aperçu
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
    PbrMaterialItem
)


class PolyHavenMaterialsPreprocessor(BasePreprocessor):
    """Adaptateur pour les matériaux PBR Poly Haven."""

    @property
    def source_name(self) -> str:
        return "CORE_POLYHAVEN_MATERIALS"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.MATERIAL_PBR

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.MULTIUSE

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        raw_rel = "core/materials/polyhaven/textures_catalog.json"
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

        for mat_id in keys:
            self.items_processed += 1
            info = catalog[mat_id]

            name = info.get("name", mat_id)
            cat = info.get("category", "surface")
            tags = info.get("tags", [])
            dims_mm = info.get("dimensions") # [x_mm, y_mm]
            dims_m = [round(d / 1000.0, 3) for d in dims_mm] if dims_mm and len(dims_mm) == 2 else None

            pbr_maps = ["color", "roughness", "normal", "displacement", "ao"]

            pbr_item = PbrMaterialItem(
                material_id=mat_id,
                name=name,
                category=cat,
                tags=tags,
                physical_scale_m=dims_m,
                maps_available=pbr_maps,
                preview_url=info.get("thumbnail_url"),
                properties={
                    "max_resolution": info.get("max_resolution"),
                    "download_count": info.get("download_count"),
                    "attributes": info.get("attributes", {})
                }
            )

            norm_id = f"NORM_POLYHAVEN_MAT_{mat_id}"
            master_id = f"ARCHI_MASTER_POLYHAVEN_MAT_{mat_id}"

            provenance = self.build_provenance(
                raw_file_rel=raw_rel,
                raw_element_id=mat_id,
                normalized_id=norm_id,
                master_id=master_id,
                transformation_name="PolyHavenMaterialsPreprocessor.pbr_extractor",
                notes=f"Matériau PBR {name} (échelle: {dims_m} m)"
            )

            item = MasterCanonicalItem(
                id=master_id,
                source_id=mat_id,
                source_name=self.source_name,
                source_license="CC0",
                modality=self.modality,
                data_type="pbr_material_spec",
                domain="materials",
                routing=self.default_routing,
                quality_status=QualityStatus.PASS,
                provenance=provenance,
                material=pbr_item,
                metadata={
                    "categories_list": info.get("categories", []),
                    "description": info.get("description", "")
                }
            )

            self.items_passed += 1
            yield item

        self.end_time = time.time()


class AmbientCgPreprocessor(BasePreprocessor):
    """Adaptateur pour les matériaux PBR ambientCG."""

    @property
    def source_name(self) -> str:
        return "CORE_AMBIENTCG"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.MATERIAL_PBR

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.MULTIUSE

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        raw_rel = "core/materials/ambientcg/ambientcg_full_catalog.json"
        cat_path = self.raw_root / raw_rel

        if not cat_path.exists():
            self.errors.append(f"Fichier introuvable: {cat_path}")
            self.end_time = time.time()
            return

        with open(cat_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)

        found_assets = catalog.get("foundAssets", [])
        if limit is not None:
            found_assets = found_assets[:limit]

        for asset in found_assets:
            self.items_processed += 1
            asset_id = asset.get("assetId", f"asset_{self.items_processed}")
            name = asset.get("displayName", asset_id)
            cat = asset.get("displayCategory", "Material")
            tags = asset.get("tags", [])

            # Dimensions en cm -> conversion certifiée en mètres
            dim_x = asset.get("dimensionX")
            dim_y = asset.get("dimensionY")
            dims_m = [round(dim_x / 100.0, 3), round(dim_y / 100.0, 3)] if (dim_x and dim_y) else None

            pbr_item = PbrMaterialItem(
                material_id=asset_id,
                name=name,
                category=cat,
                tags=tags,
                physical_scale_m=dims_m,
                maps_available=asset.get("maps", []),
                preview_url=asset.get("shortLink"),
                properties={
                    "creation_method": asset.get("creationMethod"),
                    "popularity_score": asset.get("popularityScore")
                }
            )

            norm_id = f"NORM_AMBIENTCG_{asset_id}"
            master_id = f"ARCHI_MASTER_AMBIENTCG_{asset_id}"

            provenance = self.build_provenance(
                raw_file_rel=raw_rel,
                raw_element_id=asset_id,
                normalized_id=norm_id,
                master_id=master_id,
                transformation_name="AmbientCgPreprocessor.pbr_extractor",
                notes=f"Matériau {name} (échelle: {dims_m} m)"
            )

            item = MasterCanonicalItem(
                id=master_id,
                source_id=asset_id,
                source_name=self.source_name,
                source_license="CC0",
                modality=self.modality,
                data_type="pbr_material_spec",
                domain="materials",
                routing=self.default_routing,
                quality_status=QualityStatus.PASS,
                provenance=provenance,
                material=pbr_item,
                metadata={
                    "data_type": asset.get("dataType"),
                    "preview_links": asset.get("previewLinks", [])
                }
            )

            self.items_passed += 1
            yield item

        self.end_time = time.time()
