# -*- coding: utf-8 -*-
"""
ARCHI-AI — Préprocesseur Canonique Questions/Réponses IFC-Bench V2
==================================================================
Normalise les 1 026 questions/réponses expertes de raisonnement BIM :
- Métadonnées BIM, métrés, requêtes topologiques
- Respect strict du split hellin2026 :
    * train (512 QA) -> FINETUNE
    * test (514 QA)  -> BENCHMARK (Sanctuarisé hors entraînement)
- Conservation intégrale de la vérité terrain (ground_truth)
- Aucun QA inventé ou modifié
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
    MultimodalQAPair
)


class IfcBenchQAPreprocessor(BasePreprocessor):
    """Adaptateur de normalisation pour les QA de CORE_IFC_BENCH."""

    @property
    def source_name(self) -> str:
        return "CORE_IFC_BENCH_QA"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.MULTIMODAL_QA

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.MULTIUSE

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        raw_rel_v2 = "core/bim_ifc/ifc_bench/questions/ifc-bench-v2.csv"
        raw_rel_split = "core/bim_ifc/ifc_bench/questions/eval-split-hellin2026.csv"

        csv_v2 = self.raw_root / raw_rel_v2
        csv_split = self.raw_root / raw_rel_split

        if not csv_v2.exists() or not csv_split.exists():
            self.errors.append(f"Fichiers manquants dans IFC-Bench QA")
            self.end_time = time.time()
            return

        # 1. Charger le split officiel (hellin2026)
        split_assignments = {}
        with open(csv_split, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                split_assignments[row["id"]] = row["split"]

        # 2. Charger les questions V2
        with open(csv_v2, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if limit is not None and self.items_processed >= limit:
                    break

                self.items_processed += 1
                qa_id = row["id"]
                assigned_split = split_assignments.get(qa_id, "train")
                
                # Distinction stricte Trainable vs Benchmark
                is_benchmark = (assigned_split == "test")
                routing = RoutingType.BENCHMARK if is_benchmark else RoutingType.FINETUNE

                question_text = row.get("question", "").strip()
                ground_truth = row.get("ground_truth", "").strip()
                category = row.get("category", "bim_reasoning")
                ifc_model = row.get("ifc_model")
                project = row.get("project")

                qa_pair = MultimodalQAPair(
                    qa_id=qa_id,
                    question=question_text,
                    answer=ground_truth,
                    options=None,
                    ground_truth=ground_truth,
                    explanation=None,
                    image_path=None,
                    category=category,
                    difficulty="advanced",
                    source_benchmark="IFC-Bench V2",
                    split_assignment=assigned_split,
                    is_benchmark_holdout=is_benchmark
                )

                norm_id = f"NORM_IFC_BENCH_QA_{qa_id}"
                master_id = f"ARCHI_MASTER_IFC_QA_{qa_id}"

                provenance = self.build_provenance(
                    raw_file_rel=raw_rel_v2,
                    raw_element_id=qa_id,
                    normalized_id=norm_id,
                    master_id=master_id,
                    transformation_name="IfcBenchQAPreprocessor.split_sanctuary_extractor",
                    notes=f"QA BIM V2 liée au projet {project}, modèle {ifc_model} (Split: {assigned_split})"
                )

                item = MasterCanonicalItem(
                    id=master_id,
                    source_id=qa_id,
                    source_name=self.source_name,
                    source_license="CC-BY-4.0",
                    modality=self.modality,
                    data_type="multimodal_bim_qa",
                    domain="bim",
                    routing=routing,
                    quality_status=QualityStatus.PASS,
                    provenance=provenance,
                    qa=qa_pair,
                    metadata={
                        "project": project,
                        "ifc_model": ifc_model,
                        "is_benchmark_strict": is_benchmark
                    }
                )

                self.items_passed += 1
                yield item

        self.end_time = time.time()
