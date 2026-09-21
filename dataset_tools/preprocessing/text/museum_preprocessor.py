# -*- coding: utf-8 -*-
"""
ARCHI-AI — Préprocesseur Histoire du Design & Architecture (MoMA & The Met)
===========================================================================
Normalise les notices patrimoniales et muséales pour le corpus RAG :
- MoMA Architecture & Design (34 539 notices d'édifices, mobilier, maquettes, dessins)
- The Met Open Access (Arts décoratifs, mobilier et éléments d'architecture)
RÈGLES STRICTES APPLIQUÉES :
- Ne génère pas de fausses paires QA artificielles
- Destiné prioritairement au RAG, à la culture d'atelier et à l'enrichissement sémantique
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
    QualityStatus,
    MuseumArtworkRecord
)


class MoMaCollectionPreprocessor(BasePreprocessor):
    """Adaptateur de normalisation pour CORE_MOMA_COLLECTION (Architecture & Design)."""

    @property
    def source_name(self) -> str:
        return "CORE_MOMA_COLLECTION"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.HISTORICAL_DESIGN

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.RAG

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        raw_rel = "core/design_history/moma/Artworks.csv"
        csv_path = self.raw_root / raw_rel

        if not csv_path.exists():
            self.errors.append(f"Fichier introuvable: {csv_path}")
            self.end_time = time.time()
            return

        with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Filtrage strict sur le département Architecture & Design
                if row.get("Department") != "Architecture & Design":
                    continue

                if limit is not None and self.items_processed >= limit:
                    break

                self.items_processed += 1
                obj_id = str(row.get("ObjectID", f"moma_{self.items_processed}"))
                title = row.get("Title") or row.get("\ufeffTitle") or "Untitled"
                artist = row.get("Artist")
                date_str = row.get("Date")
                medium = row.get("Medium")
                dims = row.get("Dimensions")
                classification = row.get("Classification")
                url = row.get("URL")
                img_url = row.get("ImageURL")

                rec = MuseumArtworkRecord(
                    record_id=obj_id,
                    institution="MoMA (The Museum of Modern Art)",
                    title=title,
                    artist_or_designer=artist,
                    artist_bio=row.get("ArtistBio"),
                    nationality=row.get("Nationality"),
                    creation_date=date_str,
                    medium=medium,
                    dimensions_raw=dims,
                    classification=classification,
                    department="Architecture & Design",
                    image_url=img_url,
                    object_url=url,
                    language="en"
                )

                norm_id = f"NORM_MOMA_{obj_id}"
                master_id = f"ARCHI_MASTER_MOMA_{obj_id}"

                provenance = self.build_provenance(
                    raw_file_rel=raw_rel,
                    raw_element_id=obj_id,
                    normalized_id=norm_id,
                    master_id=master_id,
                    transformation_name="MoMaCollectionPreprocessor.architecture_filter",
                    notes=f"Notice MoMA A&D: {title} par {artist} ({date_str})"
                )

                item = MasterCanonicalItem(
                    id=master_id,
                    source_id=obj_id,
                    source_name=self.source_name,
                    source_license="CC0-1.0 Domaine Public",
                    modality=self.modality,
                    data_type="museum_catalog_record",
                    domain="heritage",
                    routing=self.default_routing,
                    quality_status=QualityStatus.PASS,
                    provenance=provenance,
                    museum=rec,
                    metadata={
                        "cataloged": row.get("Cataloged"),
                        "on_view": row.get("OnView")
                    }
                )

                self.items_passed += 1
                yield item

        self.end_time = time.time()


class MetOpenAccessPreprocessor(BasePreprocessor):
    """Adaptateur de normalisation pour CORE_MET_OPENACCESS (Mobilier & Arts Décoratifs)."""

    DECORATIVE_DEPARTMENTS = [
        "European Sculpture and Decorative Arts",
        "The American Wing",
        "Asian Art"
    ]

    ARCHI_KEYWORDS = [
        "furniture", "chair", "table", "cabinet", "woodwork", "armchair",
        "desk", "bed", "sofa", "door", "window", "paneling", "commode",
        "credenza", "architectural"
    ]

    @property
    def source_name(self) -> str:
        return "CORE_MET_OPENACCESS"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.HISTORICAL_DESIGN

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.RAG

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        raw_rel = "core/design_history/met/MetObjects.csv"
        csv_path = self.raw_root / raw_rel

        if not csv_path.exists():
            self.errors.append(f"Fichier introuvable: {csv_path}")
            self.end_time = time.time()
            return

        with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dep = row.get("Department", "")
                name = (row.get("Object Name") or "").lower()
                title = (row.get("Title") or "").lower()
                classification = (row.get("Classification") or "").lower()

                # Filtrer les pièces d'arts décoratifs, mobilier et architecture
                is_target = any(dep == d for d in self.DECORATIVE_DEPARTMENTS) and any(
                    k in name or k in title or k in classification for k in self.ARCHI_KEYWORDS
                )
                if not is_target:
                    continue

                if limit is not None and self.items_processed >= limit:
                    break

                self.items_processed += 1
                obj_id = str(row.get("Object ID", f"met_{self.items_processed}"))
                obj_title = row.get("Title") or row.get("Object Name") or "Untitled"

                rec = MuseumArtworkRecord(
                    record_id=obj_id,
                    institution="The Metropolitan Museum of Art",
                    title=obj_title,
                    artist_or_designer=row.get("Artist Display Name"),
                    artist_bio=row.get("Artist Display Bio"),
                    nationality=row.get("Artist Nationality"),
                    creation_date=row.get("Object Date"),
                    medium=row.get("Medium"),
                    dimensions_raw=row.get("Dimensions"),
                    classification=row.get("Classification"),
                    department=dep,
                    image_url=None,
                    object_url=row.get("Link Resource"),
                    language="en"
                )

                norm_id = f"NORM_MET_{obj_id}"
                master_id = f"ARCHI_MASTER_MET_{obj_id}"

                provenance = self.build_provenance(
                    raw_file_rel=raw_rel,
                    raw_element_id=obj_id,
                    normalized_id=norm_id,
                    master_id=master_id,
                    transformation_name="MetOpenAccessPreprocessor.furniture_architecture_filter",
                    notes=f"Notice Met: {obj_title} ({dep})"
                )

                item = MasterCanonicalItem(
                    id=master_id,
                    source_id=obj_id,
                    source_name=self.source_name,
                    source_license="CC0-1.0 Domaine Public",
                    modality=self.modality,
                    data_type="museum_catalog_record",
                    domain="heritage",
                    routing=self.default_routing,
                    quality_status=QualityStatus.PASS,
                    provenance=provenance,
                    museum=rec,
                    metadata={
                        "period": row.get("Period"),
                        "culture": row.get("Culture"),
                        "country": row.get("Country")
                    }
                )

                self.items_passed += 1
                yield item

        self.end_time = time.time()
