# -*- coding: utf-8 -*-
"""
ARCHI-AI — SupervisionEngine (Moteur d'Orchestration Principal)
===============================================================
Orchestre la génération, la validation déterministe, le contrôle qualité,
le partitionnement étanche et la production des rapports du Dataset V1.

Usage CLI :
    python -m dataset_tools.supervision.engine --wave 1 --max-examples 1000
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

from .schema import SupervisedExample, QualityStatus, SplitName, RoutingDestination
from .task_catalogue import TASK_CATALOGUE, TaskGroup
from .generators import ALL_GENERATORS
from .quality_gate import QualityGate
from .split_manager import SplitManager
from .reporter import SupervisionReporter

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MASTER_RECORDS_PATH = BASE_DIR / "dataset" / "master" / "v1" / "master_records.jsonl"
PROCESSED_DIR = BASE_DIR / "dataset" / "processed"
OUTPUT_BASE_DIR = BASE_DIR / "dataset" / "master" / "v1" / "supervision"


class SupervisionEngine:
    """Moteur central de supervision ARCHI-AI."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or (OUTPUT_BASE_DIR / "wave1")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "splits").mkdir(parents=True, exist_ok=True)

        self.quality_gate = QualityGate()
        self.split_manager = SplitManager()
        self.generators = ALL_GENERATORS

    def run_wave1_repaired(self, max_examples: int = 800) -> Dict[str, Any]:
        """
        Exécute la génération et la certification de la Wave 1 Repaired.
        Direction vers 'dataset/master/v1/supervision/wave1_repaired/'.
        """
        self.output_dir = OUTPUT_BASE_DIR / "wave1_repaired"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "splits").mkdir(parents=True, exist_ok=True)
        return self.run_wave1(max_examples=max_examples, is_repaired=True)

    def run_wave1(self, max_examples: int = 1000, is_repaired: bool = False) -> Dict[str, Any]:
        """
        Exécute la génération et la certification de la Vague 1.
        Garantit la représentativité multi-sources et multi-tâches sans dépassement.
        """
        mode_label = "WAVE 1 REPAIRED (RECONSTRUCTION PROPRE)" if is_repaired else "WAVE 1 PILOTE"
        print("=" * 70)
        print(f"ARCHI-AI — DÉMARRAGE DU SUPERVISION ENGINE ({mode_label})")
        print("=" * 70)
        print(f"Répertoire de sortie : {self.output_dir}")
        print(f"Plafond cible : {max_examples} exemples supervisés certifiés")

        all_examples: List[SupervisedExample] = []
        rejected_examples: List[SupervisedExample] = []
        review_queue: List[SupervisedExample] = []
        seen_ids = set()

        # Sources cibles équilibrées et quotas d'exemples par source
        source_targets = [
            ("CORE_RESPLAN", PROCESSED_DIR / "floorplan_2d_resplan.jsonl", 110),
            ("CORE_RPLAN", PROCESSED_DIR / "floorplan_2d_rplan.jsonl", 40),
            ("CORE_RESBIM_PAIRED", PROCESSED_DIR / "floorplan_2d_resbim_2d.jsonl", 20),
            ("CORE_IL3D", PROCESSED_DIR / "spatial_3d_il3d.jsonl", 80),
            ("CORE_STRUCTSCAN3D", PROCESSED_DIR / "spatial_3d_structscan3d.jsonl", 40),
            ("CORE_BUILDINGSMART_IFC", PROCESSED_DIR / "bim_ifc_buildingsmart.jsonl", 30),
            ("CORE_IFC_BENCH_MODELS", PROCESSED_DIR / "bim_ifc_ifc_bench_models.jsonl", 30),
            ("CORE_IFC_BENCH_QA", PROCESSED_DIR / "multimodal_qa_ifc_bench_qa.jsonl", 40),
            ("CORE_MMMU_ARCHITECTURE", PROCESSED_DIR / "multimodal_qa_mmmu.jsonl", 50),
            ("CORE_AMBIENTCG", PROCESSED_DIR / "material_pbr_ambientcg.jsonl", 40),
            ("CORE_POLYHAVEN_MATERIALS", PROCESSED_DIR / "material_pbr_polyhaven_materials.jsonl", 50),
            ("CORE_POLYHAVEN_LIGHTING", PROCESSED_DIR / "lighting_hdri_polyhaven_lighting.jsonl", 60),
            ("CORE_ERGONOMIE", PROCESSED_DIR / "ergonomics_ergonomie.jsonl", 50),
            ("CORE_NORMES_FR", PROCESSED_DIR / "regulatory_text_normes_fr.jsonl", 40),
            ("CORE_MOMA_COLLECTION", PROCESSED_DIR / "historical_design_moma.jsonl", 50),
            ("CORE_MET_OPENACCESS", PROCESSED_DIR / "historical_design_met.jsonl", 40),
        ]

        for src_name, src_file, target_quota in source_targets:
            if not src_file.exists():
                print(f"[WARN] Fichier source introuvable : {src_file.name}")
                continue

            current_src_count = 0
            with open(src_file, "r", encoding="utf-8") as f:
                for line in f:
                    if current_src_count >= target_quota or len(all_examples) >= max_examples:
                        break

                    line_str = line.strip()
                    if not line_str:
                        continue

                    record = json.loads(line_str)
                    record["source_name"] = src_name

                    # Déterminer les générateurs compatibles
                    for gen in self.generators:
                        if src_name in gen.supported_sources:
                            gen_exs = gen.generate(record, max_examples=2)
                            for ex in gen_exs:
                                # 1. Évaluation par le Quality Gate
                                evaluated_ex = self.quality_gate.evaluate(ex)

                                # 2. Gestion selon le statut
                                if evaluated_ex.quality_status == QualityStatus.FAIL:
                                    rejected_examples.append(evaluated_ex)
                                    continue
                                elif evaluated_ex.quality_status == QualityStatus.REVIEW:
                                    review_queue.append(evaluated_ex)
                                    continue

                                # 3. Déduplication stricte par identifiant
                                if evaluated_ex.id in seen_ids:
                                    continue
                                seen_ids.add(evaluated_ex.id)

                                # 4. Affectation d'une partition étanche
                                self.split_manager.assign_split(evaluated_ex)

                                all_examples.append(evaluated_ex)
                                current_src_count += 1

                                if current_src_count >= target_quota or len(all_examples) >= max_examples:
                                    break

                        if current_src_count >= target_quota or len(all_examples) >= max_examples:
                            break

        print(f"\n[OK] Génération brute achevée : {len(all_examples)} exemples supervisés certifiés.")
        print(f"Rejets (FAIL) : {len(rejected_examples)} | File de revue (REVIEW) : {len(review_queue)}")

        # Audit anti-fuite
        leak_audit = self.split_manager.check_leakage(all_examples)
        print(f"Audit de non-contamination (Leakage Check) : {'SUCCÈS (Zéro fuite)' if leak_audit['is_leak_free'] else 'ÉCHEC (Fuite détectée)'}")

        # Sérialisation des résultats
        self._write_outputs(all_examples, rejected_examples, review_queue)

        # Calcul des statistiques de distribution
        stats = self._compute_statistics(all_examples, rejected_examples, review_queue, leak_audit)

        # Production des rapports Markdown officiels
        engine_report_path = BASE_DIR / "SUPERVISION_ENGINE_REPORT.md"
        if is_repaired:
            wave1_report_path = BASE_DIR / "WAVE1_REPAIRED_REPORT.md"
        else:
            wave1_report_path = BASE_DIR / "DATASET_V1_WAVE1_REPORT.md"
        SupervisionReporter.generate_engine_report(stats, engine_report_path)
        SupervisionReporter.generate_wave1_report(stats, wave1_report_path)
        print(f"[OK] Rapport d'ingénierie généré : {engine_report_path.name}")
        print(f"[OK] Rapport métrique généré : {wave1_report_path.name}")

        return stats

    def _write_outputs(
        self,
        examples: List[SupervisedExample],
        rejected: List[SupervisedExample],
        review_queue: List[SupervisedExample],
    ) -> None:
        """Sérialise les fichiers de données supervisées."""
        main_file = self.output_dir / "wave1_dataset.jsonl"
        with open(main_file, "w", encoding="utf-8") as f:
            for ex in examples:
                f.write(ex.model_dump_json() + "\n")

        # Partitions
        split_files = {
            SplitName.TRAIN: self.output_dir / "splits" / "train.jsonl",
            SplitName.VALIDATION: self.output_dir / "splits" / "validation.jsonl",
            SplitName.BENCHMARK: self.output_dir / "splits" / "benchmark.jsonl",
            SplitName.HOLDOUT: self.output_dir / "splits" / "holdout.jsonl",
        }
        for split_enum, path in split_files.items():
            with open(path, "w", encoding="utf-8") as f:
                for ex in examples:
                    if ex.split == split_enum:
                        f.write(ex.model_dump_json() + "\n")

        # Files spéciales
        if rejected:
            with open(self.output_dir / "rejected.jsonl", "w", encoding="utf-8") as f:
                for ex in rejected:
                    f.write(ex.model_dump_json() + "\n")

        if review_queue:
            with open(self.output_dir / "review_queue.jsonl", "w", encoding="utf-8") as f:
                for ex in review_queue:
                    f.write(ex.model_dump_json() + "\n")

    def _compute_statistics(
        self,
        examples: List[SupervisedExample],
        rejected: List[SupervisedExample],
        review: List[SupervisedExample],
        leak_audit: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Calcule les indicateurs statistiques pour les rapports."""
        total = len(examples)
        skills_count: Dict[str, int] = {}
        groups_count: Dict[str, int] = {}
        diff_count: Dict[str, int] = {}
        splits_count: Dict[str, int] = {}
        quality_count: Dict[str, int] = {"PASS": 0, "WARNING": 0, "REVIEW": len(review), "FAIL": len(rejected)}

        for ex in examples:
            skills_count[ex.skill] = skills_count.get(ex.skill, 0) + 1
            groups_count[ex.task_group] = groups_count.get(ex.task_group, 0) + 1
            diff_count[ex.difficulty.value] = diff_count.get(ex.difficulty.value, 0) + 1
            splits_count[ex.split.value] = splits_count.get(ex.split.value, 0) + 1
            quality_count[ex.quality_status.value] = quality_count.get(ex.quality_status.value, 0) + 1

        # Formatage texte pour les compétences
        skills_lines = []
        for s, c in sorted(skills_count.items(), key=lambda x: x[1], reverse=True):
            pct = (c / max(total, 1)) * 100
            skills_lines.append(f"├── {s.ljust(25)} : {c:>4} exemples ({pct:>5.1f} %)")
        skills_text = "\n".join(skills_lines)

        # Lignes Markdown pour le tableau des groupes
        group_rows = []
        for g, c in sorted(groups_count.items(), key=lambda x: x[0]):
            pct = (c / max(total, 1)) * 100
            group_rows.append(f"| **{g}** | `{g}` | **{c}** | {pct:.1f} % |")
        groups_table = "\n".join(group_rows)

        # Taille sur disque
        main_file = self.output_dir / "wave1_dataset.jsonl"
        disk_size_mb = main_file.stat().st_size / (1024 * 1024) if main_file.exists() else 0.0

        return {
            "total_examples": total,
            "quality_pass": quality_count.get("PASS", 0),
            "quality_warning": quality_count.get("WARNING", 0),
            "quality_review": len(review),
            "quality_fail": len(rejected),
            "pct_pass": f"{(quality_count.get('PASS', 0) / max(total, 1)) * 100:.1f} %",
            "leakage_status": "ZÉRO FUITE (Audit étanche certifié)" if leak_audit["is_leak_free"] else "FUITE DÉTECTÉE",
            "disk_size_mb": disk_size_mb,
            "skills_breakdown_text": skills_text,
            "groups_table_rows": groups_table,
            "diff_l1": diff_count.get("L1_RECONNAISSANCE", 0),
            "diff_l2": diff_count.get("L2_COMPREHENSION", 0),
            "diff_l3": diff_count.get("L3_ANALYSE", 0),
            "diff_l4": diff_count.get("L4_RAISONNEMENT", 0),
            "diff_l5": diff_count.get("L5_EXPERT", 0),
            "diff_l6": diff_count.get("L6_MULTICONTRAINTE", 0),
            "split_train": splits_count.get("train", 0),
            "split_val": splits_count.get("validation", 0),
            "split_bench": splits_count.get("benchmark", 0),
            "split_holdout": splits_count.get("holdout", 0),
            "split_train_pct": f"{(splits_count.get('train', 0) / max(total, 1)) * 100:.1f} %",
            "split_val_pct": f"{(splits_count.get('validation', 0) / max(total, 1)) * 100:.1f} %",
            "split_bench_pct": f"{(splits_count.get('benchmark', 0) / max(total, 1)) * 100:.1f} %",
        }


def main():
    parser = argparse.ArgumentParser(description="ARCHI-AI Supervision Engine")
    parser.add_argument("--wave", type=int, default=1, help="Numéro de vague (défaut: 1)")
    parser.add_argument("--repaired", action="store_true", help="Générer la Wave 1 Repaired propre")
    parser.add_argument("--max-examples", type=int, default=800, help="Nombre max d'exemples (défaut: 800)")
    args = parser.parse_args()

    engine = SupervisionEngine()
    if args.repaired:
        engine.run_wave1_repaired(max_examples=args.max_examples)
    elif args.wave == 1:
        engine.run_wave1(max_examples=args.max_examples)
    else:
        print(f"Vague {args.wave} non autorisée : la consigne exige de s'arrêter après la Wave 1.")


if __name__ == "__main__":
    main()
