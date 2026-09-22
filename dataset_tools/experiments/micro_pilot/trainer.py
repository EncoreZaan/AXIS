# -*- coding: utf-8 -*-
"""
ARCHI-AI — Controlled Training Micro-Pilot Engine
=================================================
Manages:
- Deterministic seeding (torch, numpy, random, cudnn)
- Training & validation loops
- Checkpoint management with SHA-256 integrity
- Metrics logging (metrics.jsonl) & error collection
- Plot / ASCII curve generation
- Diagnostic classification (LEARNING, NO_LEARNING, OVERFIT, etc.)
"""

import os
import sys
import json
import time
import math
import random
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Repository root, resolved from this file's location (this used to be reached
# via a local `ARCHI_AI/` directory junction — see DATASET.md §6 for history).
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from dataset_tools.experiments.micro_pilot.models import (
    SpatialRelationMLP,
    ClearanceMLP,
    PlanVisionCNN,
    build_model
)
from dataset_tools.experiments.micro_pilot.dataset_loader import DatasetASubset


def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def compute_sha256(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


class Trainer:
    def __init__(self, config: Dict[str, Any], run_dir: str):
        self.config = config
        self.run_dir = run_dir
        self.run_id = config.get("run_id", "ARCHI-AI-P4-EXP")
        self.task_id = config.get("task_id", "OBJECT_RELATION")
        self.seed = config.get("seed", 42)
        self.device = torch.device(config.get("device", "cuda" if torch.cuda.is_available() else "cpu"))

        os.makedirs(self.run_dir, exist_ok=True)
        self.checkpoint_dir = os.path.join(self.run_dir, "checkpoint")
        os.makedirs(self.checkpoint_dir, exist_ok=True)

        set_seed(self.seed)

        # Build model
        ablation_mode = config.get("ablation_mode", "full")
        self.model = build_model(self.task_id, ablation_mode=ablation_mode).to(self.device)

        # Optimizer & Scheduler
        lr = config.get("learning_rate", 1e-3)
        weight_decay = config.get("weight_decay", 1e-4)
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=lr, weight_decay=weight_decay)

        epochs = config.get("epochs", 50)
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=epochs, eta_min=lr * 0.05)

        # Loss functions
        self.reg_loss_fn = nn.SmoothL1Loss()
        self.cls_loss_fn = nn.BCEWithLogitsLoss()

        # Metrics log
        self.metrics_log_path = os.path.join(self.run_dir, "metrics.jsonl")
        self.stdout_log_path = os.path.join(self.run_dir, "stdout.log")

    def _log(self, msg: str):
        print(msg)
        with open(self.stdout_log_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")

    def train_epoch(self, dataloader: DataLoader) -> Tuple[float, float, float]:
        self.model.train()
        total_loss = 0.0
        metric_sum = 0.0
        grad_norm_sum = 0.0
        count = 0

        for batch in dataloader:
            self.optimizer.zero_grad()
            inputs = batch["inputs"].to(self.device)

            if self.task_id == "OBJECT_RELATION":
                targets = batch["targets"].to(self.device)
                preds = self.model(inputs)
                loss = self.reg_loss_fn(preds, targets)
                metric = torch.abs(preds - targets).mean().item()  # MAE

            elif self.task_id == "CLEARANCE_CHECK":
                targets_dist = batch["targets_dist"].to(self.device)
                targets_verdict = batch["targets_verdict"].to(self.device)
                pred_dist, pred_logits = self.model(inputs)
                loss_dist = self.reg_loss_fn(pred_dist, targets_dist)
                loss_cls = self.cls_loss_fn(pred_logits, targets_verdict)
                loss = loss_dist + 2.0 * loss_cls
                # Metric: classification accuracy
                pred_verdict = (torch.sigmoid(pred_logits) >= 0.5).float()
                metric = (pred_verdict == targets_verdict).float().mean().item()

            elif self.task_id in ["FLOORPLAN_READING", "ROOM_TOPOLOGY"]:
                targets = batch["targets"].to(self.device)
                preds = self.model(inputs)
                loss = self.reg_loss_fn(preds, targets)
                # Metric: Room count MAE
                metric = torch.abs(preds[:, 0] - targets[:, 0]).mean().item()

            loss.backward()
            max_grad_norm = self.config.get("max_grad_norm", 1.0)
            grad_norm = nn.utils.clip_grad_norm_(self.model.parameters(), max_grad_norm).item()
            self.optimizer.step()

            bs = inputs.size(0)
            total_loss += loss.item() * bs
            metric_sum += metric * bs
            grad_norm_sum += grad_norm * bs
            count += bs

        self.scheduler.step()
        return total_loss / count, metric_sum / count, grad_norm_sum / count

    def evaluate(self, dataloader: DataLoader) -> Tuple[float, float, List[Dict[str, Any]]]:
        self.model.eval()
        total_loss = 0.0
        metric_sum = 0.0
        count = 0
        errors = []

        with torch.no_grad():
            for batch in dataloader:
                inputs = batch["inputs"].to(self.device)
                meta = batch["metadata"]
                bs = inputs.size(0)

                if self.task_id == "OBJECT_RELATION":
                    targets = batch["targets"].to(self.device)
                    preds = self.model(inputs)
                    loss = self.reg_loss_fn(preds, targets)
                    metric = torch.abs(preds - targets).mean().item()
                    for i in range(bs):
                        err = abs(preds[i].item() - targets[i].item())
                        if err > 0.10:  # error sample
                            errors.append({
                                "example_id": meta["example_id"][i],
                                "prediction": round(preds[i].item(), 3),
                                "target": round(targets[i].item(), 3),
                                "task": self.task_id,
                                "project_group_id": meta["project_group_id"][i],
                                "difficulty": meta["difficulty"][i],
                                "source": meta["source_dataset"][i],
                                "abs_error": round(err, 3)
                            })

                elif self.task_id == "CLEARANCE_CHECK":
                    targets_dist = batch["targets_dist"].to(self.device)
                    targets_verdict = batch["targets_verdict"].to(self.device)
                    pred_dist, pred_logits = self.model(inputs)
                    loss_dist = self.reg_loss_fn(pred_dist, targets_dist)
                    loss_cls = self.cls_loss_fn(pred_logits, targets_verdict)
                    loss = loss_dist + 2.0 * loss_cls
                    pred_verdict = (torch.sigmoid(pred_logits) >= 0.5).float()
                    metric = (pred_verdict == targets_verdict).float().mean().item()
                    for i in range(bs):
                        pv = bool(pred_verdict[i].item() == 1.0)
                        tv = bool(targets_verdict[i].item() == 1.0)
                        if pv != tv:
                            errors.append({
                                "example_id": meta["example_id"][i],
                                "prediction": pv,
                                "target": tv,
                                "predicted_dist": round(pred_dist[i].item(), 3),
                                "target_dist": round(targets_dist[i].item(), 3),
                                "task": self.task_id,
                                "project_group_id": meta["project_group_id"][i],
                                "difficulty": meta["difficulty"][i],
                                "source": meta["source_dataset"][i]
                            })

                elif self.task_id in ["FLOORPLAN_READING", "ROOM_TOPOLOGY"]:
                    targets = batch["targets"].to(self.device)
                    preds = self.model(inputs)
                    loss = self.reg_loss_fn(preds, targets)
                    metric = torch.abs(preds[:, 0] - targets[:, 0]).mean().item()
                    for i in range(bs):
                        diff = abs(preds[i, 0].item() - targets[i, 0].item())
                        if diff >= 1.0:
                            errors.append({
                                "example_id": meta["example_id"][i],
                                "prediction": round(preds[i, 0].item(), 2),
                                "target": round(targets[i, 0].item(), 2),
                                "task": self.task_id,
                                "project_group_id": meta["project_group_id"][i],
                                "difficulty": meta["difficulty"][i],
                                "source": meta["source_dataset"][i]
                            })

                total_loss += loss.item() * bs
                metric_sum += metric * bs
                count += bs

        return total_loss / count, metric_sum / count, errors

    def save_checkpoint(self, tag: str, epoch: int, score: float) -> Dict[str, Any]:
        ckpt_filename = f"checkpoint_{tag}.pt"
        ckpt_path = os.path.join(self.checkpoint_dir, ckpt_filename)
        state = {
            "epoch": epoch,
            "score": score,
            "task_id": self.task_id,
            "run_id": self.run_id,
            "model_state": self.model.state_dict(),
            "optimizer_state": self.optimizer.state_dict(),
            "config": self.config
        }
        torch.save(state, ckpt_path)
        sha = compute_sha256(ckpt_path)
        meta_filename = f"checkpoint_{tag}.json"
        meta_path = os.path.join(self.checkpoint_dir, meta_filename)
        ckpt_meta = {
            "checkpoint_file": ckpt_filename,
            "sha256": sha,
            "epoch": epoch,
            "validation_score": score,
            "model_class": self.model.__class__.__name__,
            "param_count": self.model.count_parameters(),
            "run_id": self.run_id,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(ckpt_meta, f, indent=2)
        return ckpt_meta

    def run(self, train_loader: DataLoader, val_loader: DataLoader) -> Dict[str, Any]:
        epochs = self.config.get("epochs", 50)
        best_val_score = float("inf") if self.task_id != "CLEARANCE_CHECK" else 0.0
        best_epoch = 0
        history = []
        all_errors = []

        self._log(f"[{self.run_id}] Starting training on {self.task_id} (Seed: {self.seed}, Device: {self.device})")
        self._log(f"[{self.run_id}] Model: {self.model.__class__.__name__} ({self.model.count_parameters():,} parameters)")

        for epoch in range(1, epochs + 1):
            t_loss, t_metric, g_norm = self.train_epoch(train_loader)
            v_loss, v_metric, errors = self.evaluate(val_loader)
            current_lr = self.optimizer.param_groups[0]["lr"]

            rec = {
                "epoch": epoch,
                "train_loss": round(t_loss, 5),
                "validation_loss": round(v_loss, 5),
                "training_metric": round(t_metric, 5),
                "validation_metric": round(v_metric, 5),
                "learning_rate": round(current_lr, 7),
                "gradient_norm": round(g_norm, 5),
                "step": epoch * len(train_loader)
            }
            history.append(rec)
            with open(self.metrics_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")

            # Check best score
            is_better = (v_metric > best_val_score) if self.task_id == "CLEARANCE_CHECK" else (v_metric < best_val_score)
            if is_better:
                best_val_score = v_metric
                best_epoch = epoch
                self.save_checkpoint("best_validation", epoch, v_metric)
                all_errors = errors

            if epoch % 10 == 0 or epoch == epochs:
                self._log(f"Epoch {epoch:02d}/{epochs:02d} | Train Loss: {t_loss:.4f} | Val Loss: {v_loss:.4f} | Train Metric: {t_metric:.4f} | Val Metric: {v_metric:.4f}")

        # Save last epoch
        self.save_checkpoint("last_epoch", epochs, history[-1]["validation_metric"])

        # Write error collection
        err_path = os.path.join(self.run_dir, "errors.json")
        with open(err_path, "w", encoding="utf-8") as f:
            json.dump(all_errors[:50], f, indent=2)

        # Generate text/ascii curve representation for training dynamics
        self.export_curves(history)

        return {
            "run_id": self.run_id,
            "task_id": self.task_id,
            "seed": self.seed,
            "best_epoch": best_epoch,
            "best_validation_metric": round(best_val_score, 4),
            "final_validation_metric": round(history[-1]["validation_metric"], 4),
            "final_train_metric": round(history[-1]["training_metric"], 4),
            "initial_train_loss": history[0]["train_loss"],
            "final_train_loss": history[-1]["train_loss"],
            "loss_reduction_pct": round((1.0 - history[-1]["train_loss"] / max(history[0]["train_loss"], 1e-6)) * 100, 2),
            "history": history
        }

    def export_curves(self, history: List[Dict[str, Any]]):
        curves_dir = os.path.join(self.run_dir, "training_curves")
        os.makedirs(curves_dir, exist_ok=True)
        # Export json curves
        with open(os.path.join(curves_dir, "curves.json"), "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

        # Export ASCII plots
        def make_ascii_curve(title: str, values: List[float]) -> str:
            lines = [f"=== {title} ==="]
            min_v, max_v = min(values), max(values)
            lines.append(f"Min: {min_v:.4f} | Max: {max_v:.4f} | Final: {values[-1]:.4f}")
            width = 40
            for idx, val in enumerate(values):
                if len(values) > 20 and idx % max(1, len(values) // 20) != 0 and idx != len(values)-1:
                    continue
                ratio = (val - min_v) / (max_v - min_v + 1e-9)
                bar = "#" * int(ratio * width)
                lines.append(f"Ep {idx+1:02d} | {val:8.4f} | {bar}")
            return "\n".join(lines)

        t_losses = [h["train_loss"] for h in history]
        v_losses = [h["validation_loss"] for h in history]
        v_metrics = [h["validation_metric"] for h in history]
        lrs = [h["learning_rate"] for h in history]

        with open(os.path.join(curves_dir, "loss_curve.txt"), "w", encoding="utf-8") as f:
            f.write(make_ascii_curve("Train Loss Curve", t_losses))
        with open(os.path.join(curves_dir, "validation_curve.txt"), "w", encoding="utf-8") as f:
            f.write(make_ascii_curve("Validation Loss Curve", v_losses))
        with open(os.path.join(curves_dir, "metric_curve.txt"), "w", encoding="utf-8") as f:
            f.write(make_ascii_curve("Validation Metric Curve", v_metrics))
        with open(os.path.join(curves_dir, "learning_rate_curve.txt"), "w", encoding="utf-8") as f:
            f.write(make_ascii_curve("Learning Rate Curve", lrs))
