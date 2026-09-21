# -*- coding: utf-8 -*-
"""
ARCHI-AI — Assembleur du Master Dataset Intermédiaire V1
=========================================================
Coordonne le flux complet :
RAW -> NORMALISATION PAR SOURCE -> PROCESSED -> MASTER INTERMÉDIAIRE V1
- Sérialisation progressive en streaming JSON Lines
- Traçabilité totale de provenance dans provenance.jsonl
- Indexation par routage cognitif (FINETUNE, RAG, TOOL, BENCHMARK, HOLDOUT)
- Partitions étanches (Train, Val, Benchmark Test, Holdout)
- Contrôles automatiques de déduplication et de non-contamination (Leakage)
- Manifeste d'exécution PREPROCESSING_MANIFEST.json
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import time
from collections import defaultdict

from dataset_tools.preprocessing.registry import PREPROCESSOR_REGISTRY, list_available_sources
from dataset_tools.preprocessing.schema import MasterCanonicalItem, RoutingType, QualityStatus
from dataset_tools.splitting.leak_detector import SplitLeakageDetector


class MasterDatasetAssembler:
    """Orchestrateur de normalisation et d'assemblage du Master Dataset."""

    def __init__(self, raw_root: Path, processed_root: Path, master_root: Path):
        self.raw_root = Path(raw_root)
        self.processed_root = Path(processed_root)
        self.master_root = Path(master_root)

        # Création des sous-répertoires cibles
        self.processed_root.mkdir(parents=True, exist_ok=True)
        (self.processed_root / "metadata").mkdir(parents=True, exist_ok=True)
        (self.processed_root / "plans").mkdir(parents=True, exist_ok=True)
        (self.processed_root / "spatial").mkdir(parents=True, exist_ok=True)
        (self.processed_root / "bim").mkdir(parents=True, exist_ok=True)
        (self.processed_root / "materials").mkdir(parents=True, exist_ok=True)
        (self.processed_root / "lighting").mkdir(parents=True, exist_ok=True)
        (self.processed_root / "text" / "regulatory").mkdir(parents=True, exist_ok=True)
        (self.processed_root / "text" / "ergonomie").mkdir(parents=True, exist_ok=True)
        (self.processed_root / "text" / "museum").mkdir(parents=True, exist_ok=True)
        (self.processed_root / "text" / "trends").mkdir(parents=True, exist_ok=True)
        (self.processed_root / "multimodal").mkdir(parents=True, exist_ok=True)
        (self.processed_root / "images").mkdir(parents=True, exist_ok=True)

        self.master_root.mkdir(parents=True, exist_ok=True)
        (self.master_root / "splits").mkdir(parents=True, exist_ok=True)

        self.provenance_path = self.processed_root / "metadata" / "provenance.jsonl"
        self.master_records_path = self.master_root / "master_records.jsonl"
        self.routing_index_path = self.master_root / "routing_index.json"
        self.manifest_path = self.processed_root / "metadata" / "PREPROCESSING_MANIFEST.json"

    def run(
        self,
        sources: Optional[List[str]] = None,
        limits: Optional[Dict[str, int]] = None,
        default_limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Exécute la normalisation complète ou ciblée.
        """
        start_time = time.time()
        target_sources = sources or list_available_sources()
        limits = limits or {}

        all_stats = {}
        total_items_generated = 0
        routing_counts = defaultdict(int)
        routing_index = defaultdict(list)
        modality_counts = defaultdict(int)
        quality_counts = defaultdict(int)
        source_counts = defaultdict(int)

        split_train_items = []
        split_val_items = []
        split_test_items = []
        split_holdout_items = []

        # Ouvrir les fichiers de sortie en écriture
        with open(self.provenance_path, "w", encoding="utf-8") as f_prov, \
             open(self.master_records_path, "w", encoding="utf-8") as f_master:

            for s_key in target_sources:
                if s_key not in PREPROCESSOR_REGISTRY:
                    continue

                prep_cls = PREPROCESSOR_REGISTRY[s_key]
                preprocessor = prep_cls(self.raw_root, self.processed_root)
                limit_val = limits.get(s_key, default_limit)

                print(f"  -> Traitement de la source: {s_key}...", flush=True)

                # Fichier spécifique de modalité
                modality_file = self.processed_root / f"{preprocessor.modality.value}_{s_key}.jsonl"
                source_item_count = 0

                with open(modality_file, "w", encoding="utf-8") as f_mod:
                    for item in preprocessor.process(limit=limit_val):
                        if item is None:
                            continue

                        source_item_count += 1
                        total_items_generated += 1
                        routing_counts[item.routing.value] += 1
                        routing_index[item.routing.value].append(item.id)
                        modality_counts[item.modality.value] += 1
                        quality_counts[item.quality_status.value] += 1
                        source_counts[item.source_name] += 1

                        # Sérialisation dict Pydantic
                        item_dict = item.model_dump(exclude_none=True)
                        prov_dict = item.provenance.model_dump(exclude_none=True)

                        # Écriture progressive (streaming)
                        line_item = json.dumps(item_dict, ensure_ascii=False) + "\n"
                        line_prov = json.dumps(prov_dict, ensure_ascii=False) + "\n"

                        f_master.write(line_item)
                        f_prov.write(line_prov)
                        f_mod.write(line_item)

                        # Affectation de partition étanche
                        if item.routing == RoutingType.BENCHMARK:
                            split_test_items.append(item_dict)
                        elif item.routing == RoutingType.HOLDOUT:
                            split_holdout_items.append(item_dict)
                        else:
                            # 90% train, 10% validation déterministe
                            if total_items_generated % 10 == 0:
                                split_val_items.append(item_dict)
                            else:
                                split_train_items.append(item_dict)

                stats = preprocessor.get_stats()
                stats["items_written"] = source_item_count
                all_stats[s_key] = stats
                print(f"     [OK] {s_key}: {source_item_count:,} items émis en {stats['duration_seconds']}s", flush=True)

        # Écriture des partitions étanches
        splits_dir = self.master_root / "splits"
        for s_name, s_items in [
            ("train.jsonl", split_train_items),
            ("validation.jsonl", split_val_items),
            ("benchmark_test.jsonl", split_test_items),
            ("holdout.jsonl", split_holdout_items)
        ]:
            with open(splits_dir / s_name, "w", encoding="utf-8") as f_sp:
                for it in s_items:
                    f_sp.write(json.dumps(it, ensure_ascii=False) + "\n")

        # Écriture de l'index de routage
        with open(self.routing_index_path, "w", encoding="utf-8") as f_ri:
            json.dump({
                "routing_counts": dict(routing_counts),
                "indices": dict(routing_index)
            }, f_ri, indent=2, ensure_ascii=False)

        # Contrôle anti-contamination / Leakage
        leak_detector = SplitLeakageDetector()
        leak_report = leak_detector.check_splits(
            train_samples=split_train_items[:1000],
            val_samples=split_val_items[:500],
            test_samples=split_test_items[:500]
        )

        total_duration = time.time() - start_time

        # Calcul stockage réel utilisé
        total_storage_bytes = sum(
            f.stat().st_size for f in self.processed_root.rglob("*") if f.is_file()
        ) + sum(
            f.stat().st_size for f in self.master_root.rglob("*") if f.is_file()
        )

        manifest = {
            "version": "1.0.0-canonical-master",
            "generation_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_duration_seconds": round(total_duration, 2),
            "total_items": total_items_generated,
            "modality_breakdown": dict(modality_counts),
            "routing_breakdown": dict(routing_counts),
            "quality_breakdown": dict(quality_counts),
            "source_breakdown": dict(source_counts),
            "splits": {
                "train_count": len(split_train_items),
                "validation_count": len(split_val_items),
                "benchmark_test_count": len(split_test_items),
                "holdout_count": len(split_holdout_items)
            },
            "leakage_check": leak_report,
            "storage_used_bytes": total_storage_bytes,
            "storage_used_mb": round(total_storage_bytes / (1024 * 1024), 2),
            "sources_processed": all_stats
        }

        with open(self.manifest_path, "w", encoding="utf-8") as f_man:
            json.dump(manifest, f_man, indent=2, ensure_ascii=False)

        return manifest
