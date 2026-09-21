# -*- coding: utf-8 -*-
"""
ARCHI-AI — Préprocesseur Canonique MMMU Architecture
=====================================================
Normalise les 586 questions/réponses expertes de MMMU Architecture :
- Raisonnement universitaire et diagrammes architecturaux haute résolution
- Sanctuarisation absolue en BENCHMARK (0 contamination de l'apprentissage)
- Extraction propre des diagrammes visuels dans dataset/processed/images/mmmu/
- Routage : BENCHMARK (is_benchmark_holdout = True)
"""

from typing import Iterator, Dict, Any, List, Optional
from pathlib import Path
import time
import pyarrow.parquet as pq

from dataset_tools.preprocessing.base import BasePreprocessor
from dataset_tools.preprocessing.schema import (
    MasterCanonicalItem,
    ModalityType,
    RoutingType,
    QualityStatus,
    MultimodalQAPair,
    VisualMetadata
)


class MmmuArchitecturePreprocessor(BasePreprocessor):
    """Adaptateur de normalisation pour CORE_MMMU_ARCHITECTURE."""

    PARQUET_SPLITS = [
        ("dev-00000-of-00001.parquet", "validation"),
        ("validation-00000-of-00001.parquet", "validation"),
        ("test-00000-of-00001.parquet", "test")
    ]

    @property
    def source_name(self) -> str:
        return "CORE_MMMU_ARCHITECTURE"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.MULTIMODAL_QA

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.BENCHMARK

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        raw_base = self.raw_root / "core/multimodal_reasoning/mmmu_architecture"
        if not raw_base.exists():
            self.errors.append(f"Répertoire introuvable: {raw_base}")
            self.end_time = time.time()
            return

        img_out_dir = self.processed_root / "images/mmmu"
        img_out_dir.mkdir(parents=True, exist_ok=True)

        for p_file, split_name in self.PARQUET_SPLITS:
            parquet_path = raw_base / p_file
            if not parquet_path.exists():
                self.warnings.append(f"Fichier Parquet manquant: {p_file}")
                continue

            try:
                table = pq.read_table(parquet_path)
            except Exception as e:
                self.errors.append(f"Erreur lecture {p_file}: {e}")
                continue

            pydict = table.to_pydict()
            num_rows = table.num_rows

            for r_idx in range(num_rows):
                if limit is not None and self.items_processed >= limit:
                    break

                self.items_processed += 1
                qa_id = str(pydict["id"][r_idx])
                question_text = str(pydict["question"][r_idx] or "").strip()
                options_val = pydict["options"][r_idx]
                if isinstance(options_val, str):
                    # Essayer de désérialiser ou convertir
                    try:
                        import ast
                        options_list = ast.literal_eval(options_val)
                    except Exception:
                        options_list = [options_val]
                elif isinstance(options_val, list):
                    options_list = [str(o) for o in options_val]
                else:
                    options_list = None

                answer_val = str(pydict["answer"][r_idx] or "").strip()
                explanation_val = str(pydict["explanation"][r_idx] or "") if "explanation" in pydict else None
                diff_val = str(pydict.get("topic_difficulty", [None])[r_idx] or "advanced")
                subfield_val = str(pydict.get("subfield", [None])[r_idx] or "Architecture")

                # Extraction du diagramme visuel si présent
                extracted_img_rel = None
                img1_data = pydict["image_1"][r_idx]
                if isinstance(img1_data, dict) and img1_data.get("bytes"):
                    img_bytes = img1_data["bytes"]
                    target_img = img_out_dir / f"{qa_id}.png"
                    if not target_img.exists():
                        with open(target_img, "wb") as f_img:
                            f_img.write(img_bytes)
                    extracted_img_rel = f"dataset/processed/images/mmmu/{qa_id}.png"

                qa_pair = MultimodalQAPair(
                    qa_id=qa_id,
                    question=question_text,
                    answer=answer_val,
                    options=options_list,
                    ground_truth=answer_val,
                    explanation=explanation_val,
                    image_path=extracted_img_rel,
                    category=subfield_val,
                    difficulty=diff_val,
                    source_benchmark="MMMU Architecture",
                    split_assignment=split_name,
                    is_benchmark_holdout=True
                )

                visual_meta = None
                if extracted_img_rel:
                    visual_meta = VisualMetadata(
                        path=extracted_img_rel,
                        role="diagram",
                        caption=f"Diagramme architectural MMMU {qa_id}"
                    )

                norm_id = f"NORM_MMMU_{qa_id}"
                master_id = f"ARCHI_MASTER_MMMU_{qa_id}"

                provenance = self.build_provenance(
                    raw_file_rel=f"core/multimodal_reasoning/mmmu_architecture/{p_file}",
                    raw_element_id=qa_id,
                    normalized_id=norm_id,
                    master_id=master_id,
                    transformation_name="MmmuArchitecturePreprocessor.benchmark_sanctuary_extractor",
                    notes=f"MMMU QA ({subfield_val}, split: {split_name})"
                )

                item = MasterCanonicalItem(
                    id=master_id,
                    source_id=qa_id,
                    source_name=self.source_name,
                    source_license="Apache-2.0",
                    modality=self.modality,
                    data_type="multimodal_benchmark_qa",
                    domain="architecture",
                    routing=self.default_routing,
                    quality_status=QualityStatus.PASS,
                    provenance=provenance,
                    qa=qa_pair,
                    visual=visual_meta,
                    metadata={
                        "subfield": subfield_val,
                        "question_type": pydict.get("question_type", [None])[r_idx],
                        "source_split": split_name,
                        "is_benchmark_strict": True
                    }
                )

                self.items_passed += 1
                yield item

        self.end_time = time.time()
