# -*- coding: utf-8 -*-
"""
ARCHI-AI — Dataset A Builder (Phase 4 Controlled Unimodal Micro-Pilot)
=====================================================================
Générateur déterministe et reproductible pour Dataset A :
- Small : 800 exemples (200 / tâche)
- Medium : 2 400 exemples (600 / tâche)
- Full : 6 000 exemples (1 500 / tâche)

Sanctuarisation absolue du Gold Set V3 (interdiction stricte des IDs et des projets Gold).
Découpage étanche 80/10/10 scellé par project_group_id (DeterministicSplitter seed=42).
Emboîtement strict : Small ⊂ Medium ⊂ Full.
"""

import os
import sys
import json
import math
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple, Optional
from collections import defaultdict, Counter
from datetime import datetime, timezone

import numpy as np
from PIL import Image
from scipy.ndimage import label

from .target_validators import TargetContractValidator, TargetValidationStatus
from ..master_pipeline.split_manager import DeterministicSplitter

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MASTER_MANIFEST = BASE_DIR / "dataset" / "master" / "v2" / "manifests" / "MASTER_MANIFEST.jsonl"
RAW_EXTERNAL_DIR = BASE_DIR / "dataset" / "raw" / "external"
GOLD_MANIFEST = BASE_DIR / "dataset" / "supervision" / "v1" / "manifests" / "GOLD_V3_MANIFEST.jsonl"

TARGET_BASE_DIR = BASE_DIR / "dataset" / "experiments" / "phase4_micro_pilot" / "dataset_a"


class DatasetABuilder:
    """Constructeur officiel du Dataset A pour la Phase 4."""

    def __init__(self, seed: int = 42, output_dir: Optional[Path] = None):
        self.seed = seed
        self.splitter = DeterministicSplitter(seed=seed)
        self.output_dir = output_dir or TARGET_BASE_DIR

        # Dossiers cibles
        self.dirs = {
            "small": self.output_dir / "small",
            "medium": self.output_dir / "medium",
            "full": self.output_dir / "full",
            "manifests": self.output_dir / "manifests",
            "statistics": self.output_dir / "statistics",
            "reports": self.output_dir / "reports",
        }
        for d in self.dirs.values():
            d.mkdir(parents=True, exist_ok=True)

        self.gold_ids: Set[str] = set()
        self.gold_projects: Set[str] = set()
        self.gold_sources: Set[str] = set()
        self._load_gold_manifest()

    def _load_gold_manifest(self) -> None:
        """Charge et indexe les identifiants et projets du Gold Set V3."""
        if not GOLD_MANIFEST.exists():
            raise FileNotFoundError(f"Gold manifest introuvable : {GOLD_MANIFEST}")

        with open(GOLD_MANIFEST, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                rec = json.loads(line)
                self.gold_ids.add(rec["example_id"])
                self.gold_projects.add(rec["project_group_id"])
                for s in rec.get("source_ids", []):
                    self.gold_sources.add(s)

        print(f"[BUILDER] Gold Set V3 chargé : {len(self.gold_ids)} IDs, {len(self.gold_projects)} projets sanctuarisés.")

    def _load_canonical_assets(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Charge les assets canoniques sains de RPLAN et IL3D depuis MASTER_MANIFEST."""
        rplan_records = []
        il3d_records = []

        with open(MASTER_MANIFEST, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                rec = json.loads(line)
                if not rec.get("canonical", True):
                    continue

                proj = rec.get("project_group_id", "")
                asset_id = rec.get("asset_id", "")

                # Quarantaine stricte : exclusion si projet ou asset présent dans le Gold Set V3
                if proj in self.gold_projects or asset_id in self.gold_sources or asset_id in self.gold_ids:
                    continue

                src = rec.get("source_dataset")
                spath = rec.get("source_path", "")

                if src == "CORE_RPLAN" and spath.startswith("core/rplan/extracted/image/"):
                    rplan_records.append(rec)
                elif src == "CORE_IL3D" and spath.startswith("core/il3d/extracted/layout/"):
                    il3d_records.append(rec)

        print(f"[BUILDER] Assets éligibles (hors Gold) : {len(rplan_records)} RPLAN, {len(il3d_records)} IL3D.")
        return rplan_records, il3d_records

    def generate_all_tasks(self) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        Génère les exemples pour les 4 tâches, organisés par tâche et par split.
        Retourne : {task_id: {"train": [...], "validation": [...], "test": [...]}}
        """
        rplan_records, il3d_records = self._load_canonical_assets()

        # Quotas pour FULL (1500 par tâche : 1200 train, 150 val, 150 test)
        quotas = {"train": 1200, "validation": 150, "test": 150}

        tasks_data = {
            "FLOORPLAN_READING": {"train": [], "validation": [], "test": []},
            "ROOM_TOPOLOGY": {"train": [], "validation": [], "test": []},
            "OBJECT_RELATION": {"train": [], "validation": [], "test": []},
            "CLEARANCE_CHECK": {"train": [], "validation": [], "test": []},
        }

        used_projects: Set[str] = set()

        # -------------------------------------------------------------
        # 1. FLOORPLAN_READING & 2. ROOM_TOPOLOGY (RPLAN)
        # -------------------------------------------------------------
        print("[BUILDER] Génération FLOORPLAN_READING et ROOM_TOPOLOGY...")
        for rec in rplan_records:
            proj = rec.get("project_group_id", f"PROJECT_RPLAN_{rec['asset_id'][:8]}")
            if proj in used_projects:
                continue

            split = self.splitter.assign_split(proj).value
            spath = rec.get("source_path", "")
            img_path = RAW_EXTERNAL_DIR / spath
            if not img_path.exists():
                continue

            # Vérifier si on a besoin de ce split pour FLOORPLAN_READING ou ROOM_TOPOLOGY
            need_reading = len(tasks_data["FLOORPLAN_READING"][split]) < quotas[split]
            need_topology = len(tasks_data["ROOM_TOPOLOGY"][split]) < quotas[split]

            if not need_reading and not need_topology:
                continue

            try:
                im = Image.open(img_path).convert("RGB")
                arr = np.array(im)
                w, h = im.size

                is_green = (arr[:, :, 0] < 50) & (arr[:, :, 1] > 200) & (arr[:, :, 2] < 50)
                is_red = (arr[:, :, 0] > 200) & (arr[:, :, 1] < 50) & (arr[:, :, 2] < 50)
                is_white = (arr[:, :, 0] > 230) & (arr[:, :, 1] > 230) & (arr[:, :, 2] > 230)

                door_pixel_count = int(np.sum(is_green))
                wall_pixel_count = int(np.sum(is_red))
                habitable_pixel_count = int(np.sum(is_white))

                labeled_rooms, num_rooms = label(is_white)
                labeled_doors, num_doors = label(is_green)

                if num_rooms < 2 or wall_pixel_count < 100 or habitable_pixel_count < 100:
                    continue

                room_sizes = []
                for r_idx in range(1, num_rooms + 1):
                    room_sizes.append(int(np.sum(labeled_rooms == r_idx)))
                room_sizes.sort(reverse=True)

                asset_id = rec["asset_id"]
                sha = rec.get("sha256", "")

                # Attribution exclusive du projet pour éviter tout partage de projet entre tâches
                if need_reading:
                    ex_id = f"DATASET_A_RPLAN_{asset_id[:12]}_READING"
                    ex = {
                        "example_id": ex_id,
                        "task_id": "FLOORPLAN_READING",
                        "project_group_id": proj,
                        "source_dataset": "CORE_RPLAN",
                        "source_ids": [asset_id],
                        "inputs": {
                            "plans": [{"path": spath, "width": w, "height": h}],
                            "prompt": f"Identifiez le code graphique et les entités architecturales matérialisées sur ce plan 2D ({w}x{h} px)."
                        },
                        "targets": {
                            "rooms_count": int(num_rooms),
                            "doors_count": int(num_doors),
                            "habitable_pixels": int(habitable_pixel_count),
                            "wall_pixels": int(wall_pixel_count),
                            "metric_scale": None
                        },
                        "target_contract": "EXACT_DISCRETE_PIXEL_COUNTS",
                        "modality": "PLAN_ONLY",
                        "difficulty": "L1",
                        "split": split,
                        "validation_status": "VALID",
                        "provenance": {
                            "source_dataset": "CORE_RPLAN",
                            "source_asset": spath,
                            "source_record": asset_id,
                            "source_sha256": sha,
                            "transformation_chain": ["MASTER_CANONICAL_V2", "DETERMINISTIC_EXTRACTION_V4"]
                        }
                    }
                    st, msg = TargetContractValidator.validate_example(ex)
                    if st == TargetValidationStatus.VALID:
                        tasks_data["FLOORPLAN_READING"][split].append(ex)
                        used_projects.add(proj)
                        continue

                if need_topology and num_rooms >= 3:
                    ex_id = f"DATASET_A_RPLAN_{asset_id[:12]}_TOPO"
                    ex = {
                        "example_id": ex_id,
                        "task_id": "ROOM_TOPOLOGY",
                        "project_group_id": proj,
                        "source_dataset": "CORE_RPLAN",
                        "source_ids": [asset_id],
                        "inputs": {
                            "plans": [{"path": spath, "width": w, "height": h}],
                            "prompt": "Combien de pièces distinctes sont délimitées sur ce plan et quelle est la distribution des volumes intérieurs ?"
                        },
                        "targets": {
                            "room_count": int(num_rooms),
                            "largest_room_pixels": int(room_sizes[0]),
                            "smallest_room_pixels": int(room_sizes[-1]),
                            "room_sizes_pixels": [int(s) for s in room_sizes]
                        },
                        "target_contract": "ORDERED_PARTITION_COMPONENTS",
                        "modality": "PLAN_ONLY",
                        "difficulty": "L3",
                        "split": split,
                        "validation_status": "VALID",
                        "provenance": {
                            "source_dataset": "CORE_RPLAN",
                            "source_asset": spath,
                            "source_record": asset_id,
                            "source_sha256": sha,
                            "transformation_chain": ["MASTER_CANONICAL_V2", "DETERMINISTIC_EXTRACTION_V4"]
                        }
                    }
                    st, msg = TargetContractValidator.validate_example(ex)
                    if st == TargetValidationStatus.VALID:
                        tasks_data["ROOM_TOPOLOGY"][split].append(ex)
                        used_projects.add(proj)
                        continue

            except Exception:
                continue

        # -------------------------------------------------------------
        # 3. OBJECT_RELATION & 4. CLEARANCE_CHECK (IL3D)
        # -------------------------------------------------------------
        print("[BUILDER] Génération OBJECT_RELATION et CLEARANCE_CHECK...")
        # Pour équilibrer CLEARANCE_CHECK : suivi du ratio Pass/Fail
        clearance_verdicts = {"train": Counter(), "validation": Counter(), "test": Counter()}

        for rec in il3d_records:
            proj = rec.get("project_group_id", f"PROJECT_IL3D_{rec['asset_id'][:8]}")
            if proj in used_projects:
                continue

            split = self.splitter.assign_split(proj).value
            spath = rec.get("source_path", "")
            json_path = RAW_EXTERNAL_DIR / spath
            if not json_path.exists():
                continue

            need_objrel = len(tasks_data["OBJECT_RELATION"][split]) < quotas[split]
            need_clearance = len(tasks_data["CLEARANCE_CHECK"][split]) < quotas[split]

            if not need_objrel and not need_clearance:
                continue

            try:
                with open(json_path, "r", encoding="utf-8") as jf:
                    layout_data = json.load(jf)

                objects = layout_data.get("objects", [])
                if len(objects) < 2:
                    continue

                asset_id = rec["asset_id"]
                sha = rec.get("sha256", "")

                # Extraction pour OBJECT_RELATION
                if need_objrel:
                    obj_a = objects[0]
                    obj_b = objects[1]
                    name_a = obj_a.get("category") or obj_a.get("label") or "element_A"
                    name_b = obj_b.get("category") or obj_b.get("label") or "element_B"
                    pos_a = [round(float(v), 2) for v in obj_a.get("position", [0, 0, 0])]
                    pos_b = [round(float(v), 2) for v in obj_b.get("position", [0, 0, 0])]
                    room_name = obj_a.get("roomId", "LivingArea")

                    dx = pos_a[0] - pos_b[0]
                    dy = pos_a[1] - pos_b[1]
                    dz = pos_a[2] - pos_b[2]
                    dist_m = round(math.sqrt(dx * dx + dy * dy + dz * dz), 2)

                    ex_id = f"DATASET_A_IL3D_{asset_id[:12]}_OBJREL"
                    ex = {
                        "example_id": ex_id,
                        "task_id": "OBJECT_RELATION",
                        "project_group_id": proj,
                        "source_dataset": "CORE_IL3D",
                        "source_ids": [asset_id],
                        "inputs": {
                            "geometries": [{
                                "object_a": name_a,
                                "pos_a": pos_a,
                                "object_b": name_b,
                                "pos_b": pos_b,
                                "room": room_name
                            }],
                            "prompt": f"Quelle est la distance spatiale tridimensionnelle entre '{name_a}' et '{name_b}' dans l'espace '{room_name}' ?"
                        },
                        "targets": {
                            "distance_m": dist_m,
                            "object_a_pos": pos_a,
                            "object_b_pos": pos_b,
                            "room": room_name
                        },
                        "target_contract": "EUCLIDEAN_3D_METRIC_DISTANCE",
                        "modality": "3D",
                        "difficulty": "L2",
                        "split": split,
                        "validation_status": "VALID",
                        "provenance": {
                            "source_dataset": "CORE_IL3D",
                            "source_asset": spath,
                            "source_record": asset_id,
                            "source_sha256": sha,
                            "transformation_chain": ["MASTER_CANONICAL_V2", "DETERMINISTIC_EXTRACTION_V4"]
                        }
                    }
                    st, msg = TargetContractValidator.validate_example(ex)
                    if st == TargetValidationStatus.VALID:
                        tasks_data["OBJECT_RELATION"][split].append(ex)
                        used_projects.add(proj)
                        continue

                # Extraction pour CLEARANCE_CHECK (avec équilibrage équitable Pass/Fail)
                if need_clearance:
                    # Recherche de paires avec alternance pour assurer un équilibre
                    want_fail = clearance_verdicts[split][False] < clearance_verdicts[split][True]
                    chosen_pair = None

                    all_pairs = []
                    for i in range(len(objects)):
                        for j in range(i + 1, len(objects)):
                            oa = objects[i]
                            ob = objects[j]
                            pa = [round(float(v), 2) for v in oa.get("position", [0, 0, 0])]
                            pb = [round(float(v), 2) for v in ob.get("position", [0, 0, 0])]
                            d = round(math.sqrt(sum((a - b) ** 2 for a, b in zip(pa, pb))), 2)
                            if 0.2 <= d <= 3.5:
                                all_pairs.append((oa, ob, pa, pb, d))

                    if not all_pairs:
                        continue

                    # Filtrer selon besoin d'équilibrage
                    threshold_neufert = 0.90
                    target_pairs = [p for p in all_pairs if (p[4] < threshold_neufert) == want_fail]
                    if target_pairs:
                        chosen_pair = target_pairs[0]
                    else:
                        chosen_pair = all_pairs[0]

                    oa, ob, pa, pb, dist_m = chosen_pair
                    na = oa.get("category") or oa.get("label") or "element_A"
                    nb = ob.get("category") or ob.get("label") or "element_B"
                    is_ok = bool(dist_m >= threshold_neufert)

                    ex_id = f"DATASET_A_IL3D_{asset_id[:12]}_CLEARANCE"
                    ex = {
                        "example_id": ex_id,
                        "task_id": "CLEARANCE_CHECK",
                        "project_group_id": proj,
                        "source_dataset": "CORE_IL3D",
                        "source_ids": [asset_id, "CORE_NORMES_FR_NEUFERT"],
                        "inputs": {
                            "geometries": [{
                                "object_a": na,
                                "pos_a": pa,
                                "object_b": nb,
                                "pos_b": pb
                            }],
                            "text_contexts": [{
                                "standard": "Neufert / Panero",
                                "threshold_m": threshold_neufert
                            }],
                            "prompt": f"Le dégagement spatial séparant '{na}' et '{nb}' permet-il un passage d'usage confortable selon les standards d'ergonomie ? Évaluez la distance par rapport au seuil réglementaire."
                        },
                        "targets": {
                            "measured_distance_m": dist_m,
                            "threshold_m": threshold_neufert,
                            "compliance_verdict": is_ok
                        },
                        "target_contract": "BINARY_REGULATORY_COMPLIANCE",
                        "modality": "3D + regulatory text",
                        "difficulty": "L3",
                        "split": split,
                        "validation_status": "VALID",
                        "provenance": {
                            "source_dataset": "CORE_IL3D",
                            "source_asset": spath,
                            "source_record": asset_id,
                            "source_sha256": sha,
                            "transformation_chain": ["MASTER_CANONICAL_V2", "DETERMINISTIC_EXTRACTION_V4"]
                        }
                    }
                    st, msg = TargetContractValidator.validate_example(ex)
                    if st == TargetValidationStatus.VALID:
                        tasks_data["CLEARANCE_CHECK"][split].append(ex)
                        clearance_verdicts[split][is_ok] += 1
                        used_projects.add(proj)
                        continue

            except Exception:
                continue

        # Vérification des quotas atteints
        print("[BUILDER] Synthèse des extractions par tâche :")
        for tid, s_dict in tasks_data.items():
            counts = {s: len(l) for s, l in s_dict.items()}
            print(f"  - {tid}: {counts} (total={sum(counts.values())})")

        return tasks_data

    def construct_variants(self) -> Dict[str, Any]:
        """Construit les 3 variantes Small, Medium, Full et leurs manifests."""
        tasks_data = self.generate_all_tasks()

        # Construction ordonnée des ensembles
        subsets = {
            "small": {"train": [], "validation": [], "test": []},
            "medium": {"train": [], "validation": [], "test": []},
            "full": {"train": [], "validation": [], "test": []}
        }

        # Quotas par variante et par tâche
        variant_quotas = {
            "small": {"train": 160, "validation": 20, "test": 20},      # 200 / tâche -> 800 total
            "medium": {"train": 480, "validation": 60, "test": 60},    # 600 / tâche -> 2400 total
            "full": {"train": 1200, "validation": 150, "test": 150}     # 1500 / tâche -> 6000 total
        }

        for var_name, quotas in variant_quotas.items():
            for task_id, splits in tasks_data.items():
                for s in ["train", "validation", "test"]:
                    needed = quotas[s]
                    available = splits[s][:needed]
                    if len(available) < needed:
                        raise ValueError(f"Déficit critique pour {var_name} {task_id} {s}: {len(available)} < {needed}")
                    subsets[var_name][s].extend(available)

        manifests_info = {}

        for var_name in ["small", "medium", "full"]:
            var_dir = self.dirs[var_name]
            all_examples = []

            for s in ["train", "validation", "test"]:
                split_file = var_dir / f"{s}.jsonl"
                examples = subsets[var_name][s]
                # Tri déterministe pour chaque split
                examples.sort(key=lambda x: (x["task_id"], x["project_group_id"], x["example_id"]))
                with open(split_file, "w", encoding="utf-8", newline="\n") as f:
                    for ex in examples:
                        f.write(json.dumps(ex, ensure_ascii=False) + "\n")
                all_examples.extend(examples)

            # Création du manifest global trié déterministement
            all_examples.sort(key=lambda x: (x["task_id"], x["project_group_id"], x["example_id"]))
            manifest_file = self.dirs["manifests"] / f"DATASET_A_{var_name.upper()}_MANIFEST.jsonl"
            hasher = hashlib.sha256()

            with open(manifest_file, "w", encoding="utf-8", newline="\n") as f:
                for ex in all_examples:
                    line = json.dumps(ex, ensure_ascii=False) + "\n"
                    f.write(line)
                    hasher.update(line.encode("utf-8"))

            m_hash = hasher.hexdigest()

            # Calcul des statistiques détaillées
            stats = self._compute_variant_statistics(all_examples, var_name, m_hash)
            stats_file = self.dirs["statistics"] / f"{var_name.upper()}_STATS.json"
            with open(stats_file, "w", encoding="utf-8") as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)

            manifests_info[var_name] = {
                "manifest_path": str(manifest_file),
                "manifest_hash": m_hash,
                "stats": stats
            }
            print(f"[BUILDER] Variante '{var_name.upper()}' finalisée : {len(all_examples)} exemples, SHA256={m_hash[:16]}...")

        return manifests_info

    def _compute_variant_statistics(self, examples: List[Dict[str, Any]], var_name: str, manifest_hash: str) -> Dict[str, Any]:
        """Calcule les métriques et métadonnées de synthèse d'une variante."""
        tasks = Counter()
        splits = Counter()
        modalities = Counter()
        sources = Counter()
        difficulties = Counter()
        projects = set()
        gold_overlap = 0
        gold_proj_overlap = 0

        for ex in examples:
            tasks[ex["task_id"]] += 1
            splits[ex["split"]] += 1
            modalities[ex["modality"]] += 1
            sources[ex["source_dataset"]] += 1
            difficulties[ex["difficulty"]] += 1
            proj = ex["project_group_id"]
            projects.add(proj)

            if ex["example_id"] in self.gold_ids:
                gold_overlap += 1
            if proj in self.gold_projects:
                gold_proj_overlap += 1

        return {
            "variant": var_name.upper(),
            "total_examples": len(examples),
            "train_examples": splits["train"],
            "validation_examples": splits["validation"],
            "test_examples": splits["test"],
            "unique_projects": len(projects),
            "tasks": dict(tasks),
            "modalities": dict(modalities),
            "sources": dict(sources),
            "difficulty_distribution": dict(difficulties),
            "gold_overlap": gold_overlap,
            "gold_project_overlap": gold_proj_overlap,
            "duplicate_count": len(examples) - len({e["example_id"] for e in examples}),
            "provenance_coverage": 1.0,
            "manifest_sha256": manifest_hash,
            "build_seed": self.seed,
            "build_timestamp": datetime.now(timezone.utc).isoformat()
        }


def run_build(seed: int = 42, output_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Point d'entrée pour la construction de Dataset A."""
    builder = DatasetABuilder(seed=seed, output_dir=output_dir)
    return builder.construct_variants()


if __name__ == "__main__":
    run_build()
