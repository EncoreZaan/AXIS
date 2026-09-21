# -*- coding: utf-8 -*-
"""
ARCHI-AI — Gestionnaire FloorPlanCAD (GELÉ / LEGAL_REVIEW_REQUIRED)
===================================================================
Conformément aux directives de l'audit forensic et aux règles absolues :
FloorPlanCAD est GELÉ en raison de la clause NonCommercial découverte dans sa documentation.
Ce module documente l'exclusion formelle de FloorPlanCAD du pipeline CORE V1.
Aucun élément ne doit entrer dans le Master Dataset V1 commercial.
"""

from typing import Iterator, Optional
import time

from dataset_tools.preprocessing.base import BasePreprocessor
from dataset_tools.preprocessing.schema import (
    MasterCanonicalItem,
    ModalityType,
    RoutingType,
    QualityStatus
)


class FloorPlanCadFrozenHandler(BasePreprocessor):
    """Gestionnaire de gel légal pour CORE_FLOORPLANCAD."""

    @property
    def source_name(self) -> str:
        return "CORE_FLOORPLANCAD"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.FLOORPLAN_2D

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.HOLDOUT

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0
        self.items_warning = 1

        # Alerte formelle de gel légal
        warning_msg = (
            "SOURCE GELÉE — LEGAL_REVIEW_REQUIRED : "
            "CORE_FLOORPLANCAD contient une clause restrictive NonCommercial (Voxel51/Alibaba). "
            "Exclusion absolue du pool commercial CORE V1. 0 élément normalisé généré."
        )
        self.warnings.append(warning_msg)
        self.end_time = time.time()
        
        # Rend un générateur vide : aucun item n'entre dans CORE V1
        if False:
            yield None
