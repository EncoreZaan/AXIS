# -*- coding: utf-8 -*-
"""
ARCHI-AI — STEP 11: Deterministic Split Engine (Anti-Leakage)
============================================================
Répartit les assets canoniques en train (80%), validation (10%) et test (10%)
en groupant strictement par project_group_id.
Empêche toute fuite d'information intra-projet. Enregistre le seed = 42.
Vérifie la non-contamination via SplitLeakageDetector.
"""

import json
import hashlib
from typing import Dict, List, Any, Tuple
from collections import defaultdict

from .config import SPLIT_RATIOS, RANDOM_SEED, SPLITS_DIR, MANIFEST_SPLIT
from .schema import CanonicalAssetRecord, SplitType
from ..splitting.leak_detector import SplitLeakageDetector


def extract_project_group_id(record: Any) -> str:
    """Extrait ou calcule un identifiant de projet/scène pour sceller les groupes insécables."""
    raw_rel = getattr(record, "source_path", None) or getattr(record, "relative_path", "")
    rel = str(raw_rel).replace("\\", "/")
    parts = rel.split("/")

    # 1. IFC-Bench (groupement par projet réel)
    if "ifc_bench/projects" in rel:
        idx = parts.index("projects")
        if len(parts) > idx + 1:
            return f"PROJECT_IFCBENCH_{parts[idx + 1]}"

    # 2. ResBIM (groupement par paire 2D/3D)
    if "resbim" in rel:
        fname = parts[-1]
        base_id = fname.split(".")[0].replace("_plan", "").replace("_ifc", "")
        return f"PROJECT_RESBIM_{base_id}"

    # 3. StructScan3D (groupement par scène de scan)
    if "structscan3d" in rel:
        fname = parts[-1]
        scene_prefix = fname.split("_")[0] if "_" in fname else fname
        return f"PROJECT_STRUCTSCAN_{scene_prefix}"

    # 4. IL3D (groupement par scène 3D)
    if "il3d" in rel:
        fname = parts[-1]
        scene_name = fname.split(".")[0]
        return f"PROJECT_IL3D_{scene_name}"

    # 5. RPlan & ResPlan (groupement par identifiant de plan)
    if "resplan" in rel:
        return f"PROJECT_RESPLAN_{parts[-1]}"
    if "rplan" in rel:
        fname = parts[-1]
        plan_id = fname.split(".")[0].split("_")[0]
        return f"PROJECT_RPLAN_{plan_id}"

    # Par défaut, groupe par dossier parent
    parent = parts[-2] if len(parts) > 1 else "ROOT"
    return f"GROUP_{record.source_dataset}_{parent}"


class DeterministicSplitter:
    """Gestionnaire de découpage expérimental sans fuite."""

    def __init__(self, seed: int = RANDOM_SEED):
        self.seed = seed

    def assign_split(self, project_id: str) -> SplitType:
        """Assigne un split de façon pseudo-aléatoire mais 100% déterministe via seed et SHA-256."""
        h_input = f"{project_id}_{self.seed}".encode("utf-8")
        h_val = int(hashlib.sha256(h_input).hexdigest()[:8], 16) / 0xFFFFFFFF

        if h_val < SPLIT_RATIOS["train"]:
            return SplitType.TRAIN
        elif h_val < SPLIT_RATIOS["train"] + SPLIT_RATIOS["validation"]:
            return SplitType.VALIDATION
        else:
            return SplitType.TEST

    def partition_records(
        self, records: List[CanonicalAssetRecord]
    ) -> Tuple[Dict[str, List[CanonicalAssetRecord]], Dict[str, Any]]:
        """Découpe les enregistrements et applique la vérification de non-contamination."""
        splits: Dict[str, List[CanonicalAssetRecord]] = {
            SplitType.TRAIN.value: [],
            SplitType.VALIDATION.value: [],
            SplitType.TEST.value: [],
        }

        # 1. Regroupement préalable par project_group_id
        project_map: Dict[str, List[CanonicalAssetRecord]] = defaultdict(list)
        for r in records:
            p_id = r.project_group_id or extract_project_group_id(r)
            r.project_group_id = p_id
            project_map[p_id].append(r)

        # 2. Attribution du split par projet
        for p_id, group in project_map.items():
            target_split = self.assign_split(p_id)
            splits[target_split.value].extend(group)

        # 3. Sauvegarde des partitions
        SPLITS_DIR.mkdir(parents=True, exist_ok=True)
        split_counts = {}
        for s_name, s_records in splits.items():
            s_file = SPLITS_DIR / f"{s_name}.jsonl"
            with open(s_file, "w", encoding="utf-8") as f:
                for r in s_records:
                    f.write(r.model_dump_json() + "\n")
            split_counts[s_name] = len(s_records)

        # 4. Sauvegarde SPLIT_MANIFEST.jsonl
        MANIFEST_SPLIT.parent.mkdir(parents=True, exist_ok=True)
        with open(MANIFEST_SPLIT, "w", encoding="utf-8") as f_split:
            for s_name, s_records in splits.items():
                for r in s_records:
                    entry = {
                        "asset_id": r.asset_id,
                        "split": s_name,
                        "project_group_id": r.project_group_id,
                        "source_dataset": r.source_dataset,
                    }
                    f_split.write(json.dumps(entry) + "\n")

        # 5. Vérification d'étanchéité (Leakage Check)
        train_shas = {r.sha256 for r in splits[SplitType.TRAIN.value]}
        val_shas = {r.sha256 for r in splits[SplitType.VALIDATION.value]}
        test_shas = {r.sha256 for r in splits[SplitType.TEST.value]}

        train_projects = {r.project_group_id for r in splits[SplitType.TRAIN.value]}
        val_projects = {r.project_group_id for r in splits[SplitType.VALIDATION.value]}
        test_projects = {r.project_group_id for r in splits[SplitType.TEST.value]}

        sha_leak = len(train_shas.intersection(val_shas)) + len(train_shas.intersection(test_shas)) + len(val_shas.intersection(test_shas))
        project_leak = len(train_projects.intersection(val_projects)) + len(train_projects.intersection(test_projects)) + len(val_projects.intersection(test_projects))

        leak_check_passed = (sha_leak == 0) and (project_leak == 0)

        stats = {
            "total_canonical_records": len(records),
            "split_counts": split_counts,
            "distinct_projects_count": len(project_map),
            "seed_used": self.seed,
            "sha_leak_count": sha_leak,
            "project_leak_count": project_leak,
            "leakage_test_passed": leak_check_passed,
            "manifest_split_path": str(MANIFEST_SPLIT),
        }
        return splits, stats
