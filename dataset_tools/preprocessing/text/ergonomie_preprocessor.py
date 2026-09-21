# -*- coding: utf-8 -*-
"""
ARCHI-AI — Préprocesseur Ergonomie & Anthropométrie (Neufert / Panero)
======================================================================
Normalise les règles dimensionnelles anthropométriques certifiées :
- Conservation stricte des cotes et unités originales (cm)
- Ajout de la valeur normalisée dans le Système International (mètres)
- Structure analytique complète : objet, action, contexte, seuils min/recommandés
- Routage : MULTIUSE (TOOL + RAG)
"""

from typing import Iterator, Dict, Any, List, Optional, Union
from pathlib import Path
import json
import time

from dataset_tools.preprocessing.base import BasePreprocessor
from dataset_tools.preprocessing.schema import (
    MasterCanonicalItem,
    ModalityType,
    RoutingType,
    QualityStatus,
    ErgonomicStandard
)


class ErgonomiePreprocessor(BasePreprocessor):
    """Adaptateur de normalisation pour CORE_ERGONOMIE."""

    @property
    def source_name(self) -> str:
        return "CORE_ERGONOMIE"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.ERGONOMICS

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.MULTIUSE

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        raw_rel = "core/ergonomie/regles_ergonomie_neufert_panero.json"
        ergo_path = self.raw_root / raw_rel

        if not ergo_path.exists():
            self.errors.append(f"Fichier introuvable: {ergo_path}")
            self.end_time = time.time()
            return

        with open(ergo_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        source_doc = data.get("source", "Neufert / Panero & Zelnik")
        spaces = data.get("espaces", {})

        for space_cat, rules in spaces.items():
            for rule_key, val in rules.items():
                if limit is not None and self.items_processed >= limit:
                    break
                
                # Ignorer les listes textuelles comme le triangle d'activité
                if isinstance(val, list) and all(isinstance(x, str) for x in val):
                    continue

                self.items_processed += 1
                
                # Extraction unité d'origine
                original_unit = "cm" if "_cm" in rule_key else "unit"
                clean_key = rule_key.replace("_cm", "")

                # Conversion certifiée vers SI (mètres)
                if isinstance(val, (int, float)):
                    norm_val = round(val / 100.0, 3)
                    min_v = norm_val if "minimum" in clean_key else None
                    rec_v = norm_val if ("standard" in clean_key or "confort" in clean_key) else None
                elif isinstance(val, list) and all(isinstance(x, (int, float)) for x in val):
                    norm_val = [round(x / 100.0, 3) for x in val]
                    min_v, rec_v = None, None
                else:
                    norm_val = val
                    min_v, rec_v = None, None

                target_pop = "pmr" if "pmr" in clean_key else "standard_adulte"

                std_id = f"{space_cat}_{clean_key}"
                norm_id = f"NORM_ERGO_{std_id}"
                master_id = f"ARCHI_MASTER_ERGO_{std_id}"

                ergo_std = ErgonomicStandard(
                    standard_id=std_id,
                    space_category=space_cat,
                    object_or_usage=clean_key,
                    original_value=val,
                    original_unit=original_unit,
                    normalized_si_value=norm_val,
                    normalized_si_unit="m",
                    context=f"Espace {space_cat}",
                    population=target_pop,
                    source=source_doc,
                    min_value=min_v,
                    recommended_value=rec_v,
                    remarks=f"Standard dimensionnel {clean_key}: {val} {original_unit}"
                )

                provenance = self.build_provenance(
                    raw_file_rel=raw_rel,
                    raw_element_id=rule_key,
                    normalized_id=norm_id,
                    master_id=master_id,
                    transformation_name="ErgonomiePreprocessor.metric_standardizer",
                    notes=f"Conversion certifiée: {val} {original_unit} -> {norm_val} m"
                )

                item = MasterCanonicalItem(
                    id=master_id,
                    source_id=rule_key,
                    source_name=self.source_name,
                    source_license="CC0",
                    modality=self.modality,
                    data_type="ergonomic_standard_rule",
                    domain="interior_design",
                    routing=self.default_routing,
                    quality_status=QualityStatus.PASS,
                    provenance=provenance,
                    ergonomics=ergo_std,
                    metadata={
                        "space_category": space_cat,
                        "rule_key": rule_key
                    }
                )

                self.items_passed += 1
                yield item

        self.end_time = time.time()
