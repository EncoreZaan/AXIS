# -*- coding: utf-8 -*-
"""
ARCHI-AI — Dataset A Loader for Controlled Training Micro-Pilot
==============================================================
Loads JSONL records, constructs PyTorch tensors, extracts targets,
and applies controlled ablations (Full, Metadata-Stripped, Target-Field-Masked).
"""

import os
import json
import torch
from torch.utils.data import Dataset
from typing import List, Dict, Any, Optional
from PIL import Image
import torchvision.transforms as T

class DatasetASubset(Dataset):
    """
    PyTorch Dataset for Dataset A unimodal tasks.
    Supports task filtering, micro-subsets, and ablations.
    """
    def __init__(
        self,
        jsonl_path: str,
        task_id: Optional[str] = None,
        ablation_mode: str = "full",  # "full", "metadata_stripped", "target_masked"
        limit: Optional[int] = None,
        image_base_dir: str = "ARCHI_AI/dataset/raw/external"
    ):
        self.jsonl_path = jsonl_path
        self.task_id = task_id
        self.ablation_mode = ablation_mode
        self.image_base_dir = image_base_dir

        if not os.path.exists(jsonl_path):
            raise FileNotFoundError(f"Dataset file not found: {jsonl_path}")

        self.examples = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                item = json.loads(line)
                if task_id is None or item.get("task_id") == task_id:
                    self.examples.append(item)

        if limit is not None and limit > 0:
            self.examples = self.examples[:limit]

        self.img_transform = T.Compose([
            T.Resize((256, 256)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        item = self.examples[idx]
        task = item["task_id"]
        inputs = item.get("inputs", {})
        targets = item.get("targets", {})

        meta = {
            "example_id": item.get("example_id"),
            "task_id": task,
            "project_group_id": item.get("project_group_id"),
            "difficulty": item.get("difficulty", "L2"),
            "source_dataset": item.get("source_dataset", "CORE_IL3D")
        }

        # 1. 3D Spatial Relation Task
        if task == "OBJECT_RELATION":
            geom = inputs.get("geometries", [{}])[0]
            pos_a = geom.get("pos_a", [0.0, 0.0, 0.0])
            pos_b = geom.get("pos_b", [0.0, 0.0, 0.0])

            if self.ablation_mode == "target_masked":
                # Mask object B's position entirely (zero it out)
                pos_b = [0.0, 0.0, 0.0]

            feat = torch.tensor(pos_a + pos_b, dtype=torch.float32)
            target_dist = torch.tensor(float(targets["distance_m"]), dtype=torch.float32)
            return {
                "inputs": feat,
                "targets": target_dist,
                "metadata": meta
            }

        # 2. 3D Clearance Check Task
        elif task == "CLEARANCE_CHECK":
            geom = inputs.get("geometries", [{}])[0]
            pos_a = geom.get("pos_a", [0.0, 0.0, 0.0])
            pos_b = geom.get("pos_b", [0.0, 0.0, 0.0])
            txt = inputs.get("text_contexts", [{}])[0]
            thresh = float(txt.get("threshold_m", 0.9))

            if self.ablation_mode == "target_masked":
                pos_b = [0.0, 0.0, 0.0]

            feat = torch.tensor(pos_a + pos_b + [thresh], dtype=torch.float32)
            target_dist = torch.tensor(float(targets["measured_distance_m"]), dtype=torch.float32)
            target_verdict = torch.tensor(1.0 if targets["compliance_verdict"] else 0.0, dtype=torch.float32)
            return {
                "inputs": feat,
                "targets_dist": target_dist,
                "targets_verdict": target_verdict,
                "metadata": meta
            }

        # 3. 2D Floorplan Reading Task
        elif task == "FLOORPLAN_READING":
            plans = inputs.get("plans", [{}])[0]
            rel_path = plans.get("path", "")
            img_full_path = os.path.join(self.image_base_dir, rel_path)

            if os.path.exists(img_full_path):
                img = Image.open(img_full_path).convert("RGB")
            else:
                img = Image.new("RGB", (256, 256), color=(0, 0, 0))

            if self.ablation_mode == "target_masked":
                # Mask central image content
                img = Image.new("RGB", (256, 256), color=(0, 0, 0))

            img_tensor = self.img_transform(img)

            # Targets: rooms_count, doors_count, habitable_pixels, wall_pixels
            target_vec = torch.tensor([
                float(targets["rooms_count"]),
                float(targets["doors_count"]),
                float(targets["habitable_pixels"]) / 1000.0,  # Scaled for stable loss
                float(targets["wall_pixels"]) / 1000.0
            ], dtype=torch.float32)

            return {
                "inputs": img_tensor,
                "targets": target_vec,
                "metadata": meta
            }

        # 4. 2D Room Topology Task
        elif task == "ROOM_TOPOLOGY":
            plans = inputs.get("plans", [{}])[0]
            rel_path = plans.get("path", "")
            img_full_path = os.path.join(self.image_base_dir, rel_path)

            if os.path.exists(img_full_path):
                img = Image.open(img_full_path).convert("RGB")
            else:
                img = Image.new("RGB", (256, 256), color=(0, 0, 0))

            if self.ablation_mode == "target_masked":
                img = Image.new("RGB", (256, 256), color=(0, 0, 0))

            img_tensor = self.img_transform(img)

            target_vec = torch.tensor([
                float(targets["room_count"]),
                float(targets["largest_room_pixels"]) / 1000.0,
                float(targets["smallest_room_pixels"]) / 1000.0
            ], dtype=torch.float32)

            return {
                "inputs": img_tensor,
                "targets": target_vec,
                "metadata": meta
            }

        else:
            raise ValueError(f"Unknown task {task}")
