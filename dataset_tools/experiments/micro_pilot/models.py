# -*- coding: utf-8 -*-
"""
ARCHI-AI — Experimental Minimal Models for Phase 4 Micro-Pilot
==============================================================
Minimal, fast, interpretable, deterministic neural architectures:
1. SpatialRelationMLP: 3D spatial distance regression (6D -> 1D)
2. ClearanceMLP: 3D clearance & compliance verification (7D -> 2D: distance + logit)
3. PlanVisionCNN: 2D floorplan reading (256x256 -> 4D counts & areas)
4. TopologyVisionCNN: 2D room topology partition (256x256 -> 3D)
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any, Tuple


class SpatialRelationMLP(nn.Module):
    """
    Minimal MLP for 3D Euclidean distance estimation.
    Inputs: 6D coordinates [x_a, y_a, z_a, x_b, y_b, z_b]
    Outputs: predicted continuous distance (meters)
    """
    def __init__(self, in_features: int = 6, hidden_dim: int = 64, dropout: float = 0.0):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 32),
            nn.GELU(),
            nn.Linear(32, 1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(-1)

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


class ClearanceMLP(nn.Module):
    """
    Minimal multi-task MLP for clearance check & compliance classification.
    Inputs: 7D [x_a, y_a, z_a, x_b, y_b, z_b, threshold_m]
    Outputs:
      - distance: predicted continuous distance
      - compliance_logits: binary classification logit (>= threshold)
    """
    def __init__(self, in_features: int = 7, hidden_dim: int = 64, dropout: float = 0.0):
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
        )
        self.distance_head = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.GELU(),
            nn.Linear(32, 1)
        )
        self.compliance_head = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.GELU(),
            nn.Linear(32, 1)
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        feat = self.backbone(x)
        dist = self.distance_head(feat).squeeze(-1)
        logit = self.compliance_head(feat).squeeze(-1)
        return dist, logit

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


class PlanVisionCNN(nn.Module):
    """
    Lightweight CNN for 2D floorplan reading on 256x256 plans.
    Outputs: [rooms_count, doors_count, habitable_pixels, wall_pixels]
    """
    def __init__(self, out_features: int = 4):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 128x128

            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 64x64

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 32x32

            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((4, 4))  # 64 x 4 x 4 = 1024
        )
        self.head = nn.Sequential(
            nn.Linear(1024, 128),
            nn.ReLU(),
            nn.Linear(128, out_features),
            nn.ReLU()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        f = self.conv(x)
        f = f.view(f.size(0), -1)
        return self.head(f)

    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def build_model(task_id: str, ablation_mode: str = "full") -> nn.Module:
    """Builds appropriate minimal model for task and ablation mode."""
    if task_id == "OBJECT_RELATION":
        # In ablation mode B (metadata stripped), we keep 6D coordinates
        # In ablation mode C (target-related fields masked), pos_b could be masked or zeroed
        return SpatialRelationMLP(in_features=6, hidden_dim=64)
    elif task_id == "CLEARANCE_CHECK":
        return ClearanceMLP(in_features=7, hidden_dim=64)
    elif task_id in ["FLOORPLAN_READING", "ROOM_TOPOLOGY"]:
        out_dim = 4 if task_id == "FLOORPLAN_READING" else 3
        return PlanVisionCNN(out_features=out_dim)
    else:
        raise ValueError(f"Unknown task_id: {task_id}")
