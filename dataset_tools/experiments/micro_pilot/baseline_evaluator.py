# -*- coding: utf-8 -*-
"""
ARCHI-AI — Baseline 0 Trivial Evaluator
=======================================
Computes deterministic trivial baselines (majority class, mean, median, constant heuristics)
on the training split of Dataset A and evaluates on the validation split.
Produces BASELINE_RESULTS.md and baseline_0.json.
"""

import os
import json
import statistics
from pathlib import Path
from typing import Dict, List, Any
from collections import Counter

# Repository root, resolved from this file's location (this used to be reached
# via a local `ARCHI_AI/` directory junction — see DATASET.md §6 for history).
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data

def compute_baselines(train_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    tasks = {}
    for ex in train_data:
        t = ex["task_id"]
        tasks.setdefault(t, []).append(ex)

    baselines = {}

    # 1. CLEARANCE_CHECK
    clearance_exs = tasks.get("CLEARANCE_CHECK", [])
    verdicts = [x["targets"]["compliance_verdict"] for x in clearance_exs]
    distances = [x["targets"]["measured_distance_m"] for x in clearance_exs]
    majority_verdict = Counter(verdicts).most_common(1)[0][0]
    median_dist = statistics.median(distances)
    mean_dist = statistics.mean(distances)
    baselines["CLEARANCE_CHECK"] = {
        "strategy": "Majority class for verdict, median for distance",
        "predicted_verdict": majority_verdict,
        "predicted_distance": round(median_dist, 2),
        "majority_class_freq_train": Counter(verdicts)[majority_verdict] / len(verdicts),
    }

    # 2. OBJECT_RELATION
    obj_exs = tasks.get("OBJECT_RELATION", [])
    obj_dists = [x["targets"]["distance_m"] for x in obj_exs]
    baselines["OBJECT_RELATION"] = {
        "strategy": "Median distance of train set",
        "predicted_distance": round(statistics.median(obj_dists), 2),
        "mean_distance": round(statistics.mean(obj_dists), 2),
    }

    # 3. FLOORPLAN_READING
    plan_exs = tasks.get("FLOORPLAN_READING", [])
    rooms = [x["targets"]["rooms_count"] for x in plan_exs]
    doors = [x["targets"]["doors_count"] for x in plan_exs]
    hab_pixels = [x["targets"]["habitable_pixels"] for x in plan_exs]
    wall_pixels = [x["targets"]["wall_pixels"] for x in plan_exs]
    baselines["FLOORPLAN_READING"] = {
        "strategy": "Mode for discrete counts, median for pixel areas",
        "predicted_rooms_count": Counter(rooms).most_common(1)[0][0],
        "predicted_doors_count": Counter(doors).most_common(1)[0][0],
        "predicted_habitable_pixels": int(statistics.median(hab_pixels)),
        "predicted_wall_pixels": int(statistics.median(wall_pixels)),
    }

    # 4. ROOM_TOPOLOGY
    topo_exs = tasks.get("ROOM_TOPOLOGY", [])
    topo_rooms = [x["targets"]["room_count"] for x in topo_exs]
    largest = [x["targets"]["largest_room_pixels"] for x in topo_exs]
    smallest = [x["targets"]["smallest_room_pixels"] for x in topo_exs]
    baselines["ROOM_TOPOLOGY"] = {
        "strategy": "Mode for room_count, median for partition extremes",
        "predicted_room_count": Counter(topo_rooms).most_common(1)[0][0],
        "predicted_largest_room_pixels": int(statistics.median(largest)),
        "predicted_smallest_room_pixels": int(statistics.median(smallest)),
    }

    return baselines

def evaluate_baselines(baselines: Dict[str, Any], val_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    tasks = {}
    for ex in val_data:
        t = ex["task_id"]
        tasks.setdefault(t, []).append(ex)

    results = {}

    # CLEARANCE_CHECK evaluation
    cc_val = tasks.get("CLEARANCE_CHECK", [])
    cc_base = baselines["CLEARANCE_CHECK"]
    tp = sum(1 for x in cc_val if x["targets"]["compliance_verdict"] is True and cc_base["predicted_verdict"] is True)
    fp = sum(1 for x in cc_val if x["targets"]["compliance_verdict"] is False and cc_base["predicted_verdict"] is True)
    tn = sum(1 for x in cc_val if x["targets"]["compliance_verdict"] is False and cc_base["predicted_verdict"] is False)
    fn = sum(1 for x in cc_val if x["targets"]["compliance_verdict"] is True and cc_base["predicted_verdict"] is False)
    acc = (tp + tn) / len(cc_val) if cc_val else 0.0
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    mae_dist = sum(abs(x["targets"]["measured_distance_m"] - cc_base["predicted_distance"]) for x in cc_val) / len(cc_val)
    results["CLEARANCE_CHECK"] = {
        "sample_count": len(cc_val),
        "accuracy": round(acc, 4),
        "f1_score": round(f1, 4),
        "mae_distance_m": round(mae_dist, 4),
        "baseline_summary": f"Predicts constant verdict={cc_base['predicted_verdict']}, dist={cc_base['predicted_distance']}m",
    }

    # OBJECT_RELATION evaluation
    obj_val = tasks.get("OBJECT_RELATION", [])
    obj_base = baselines["OBJECT_RELATION"]
    pred_d = obj_base["predicted_distance"]
    mae_obj = sum(abs(x["targets"]["distance_m"] - pred_d) for x in obj_val) / len(obj_val)
    within_5cm = sum(1 for x in obj_val if abs(x["targets"]["distance_m"] - pred_d) <= 0.05) / len(obj_val)
    results["OBJECT_RELATION"] = {
        "sample_count": len(obj_val),
        "mae_m": round(mae_obj, 4),
        "success_rate_5cm": round(within_5cm, 4),
        "baseline_summary": f"Predicts constant dist={pred_d}m",
    }

    # FLOORPLAN_READING evaluation
    plan_val = tasks.get("FLOORPLAN_READING", [])
    plan_base = baselines["FLOORPLAN_READING"]
    exact_rooms = sum(1 for x in plan_val if x["targets"]["rooms_count"] == plan_base["predicted_rooms_count"]) / len(plan_val)
    mae_doors = sum(abs(x["targets"]["doors_count"] - plan_base["predicted_doors_count"]) for x in plan_val) / len(plan_val)
    mae_hab = sum(abs(x["targets"]["habitable_pixels"] - plan_base["predicted_habitable_pixels"]) for x in plan_val) / len(plan_val)
    results["FLOORPLAN_READING"] = {
        "sample_count": len(plan_val),
        "exact_rooms_acc": round(exact_rooms, 4),
        "doors_mae": round(mae_doors, 4),
        "habitable_pixels_mae": round(mae_hab, 2),
        "baseline_summary": f"Predicts rooms={plan_base['predicted_rooms_count']}, doors={plan_base['predicted_doors_count']}",
    }

    # ROOM_TOPOLOGY evaluation
    topo_val = tasks.get("ROOM_TOPOLOGY", [])
    topo_base = baselines["ROOM_TOPOLOGY"]
    exact_topo_rooms = sum(1 for x in topo_val if x["targets"]["room_count"] == topo_base["predicted_room_count"]) / len(topo_val)
    mae_largest = sum(abs(x["targets"]["largest_room_pixels"] - topo_base["predicted_largest_room_pixels"]) for x in topo_val) / len(topo_val)
    results["ROOM_TOPOLOGY"] = {
        "sample_count": len(topo_val),
        "exact_room_count_acc": round(exact_topo_rooms, 4),
        "largest_room_pixels_mae": round(mae_largest, 2),
        "baseline_summary": f"Predicts room_count={topo_base['predicted_room_count']}",
    }

    return results

def run_and_report(
    train_path: str,
    val_path: str,
    out_dir: str
) -> Dict[str, Any]:
    os.makedirs(out_dir, exist_ok=True)
    baselines_dir = os.path.join(out_dir, "baselines")
    reports_dir = os.path.join(out_dir, "reports")
    os.makedirs(baselines_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    train_data = load_jsonl(train_path)
    val_data = load_jsonl(val_path)

    baselines = compute_baselines(train_data)
    eval_results = evaluate_baselines(baselines, val_data)

    # Save JSON
    baseline_payload = {
        "baselines_train": baselines,
        "evaluation_val": eval_results
    }
    with open(os.path.join(baselines_dir, "baseline_0.json"), "w", encoding="utf-8") as f:
        json.dump(baseline_payload, f, indent=2)

    # Generate BASELINE_RESULTS.md
    report_md = f"""# ARCHI-AI — Baseline 0 Results (`BASELINE_RESULTS.md`)
## Controlled Training Micro-Pilot — Phase 4

> **Date :** 2026-09-21  
> **Source Split :** Dataset A-Small Train (640 exemples)  
> **Evaluation Split :** Dataset A-Small Validation (80 exemples)  
> **Test Set Status :** LOCKED (HELD OUT)  
> **Gold Set Status :** LOCKED (HELD OUT)  

---

### 1. Synthèse des Baselines Triviaux par Tâche

| Task ID | Stratégie Baseline | Métrique Primaire | Score Validation | Seuil à Battre |
| :--- | :--- | :--- | :---: | :--- |
| **`CLEARANCE_CHECK`** | Majority Class (`verdict = {baselines['CLEARANCE_CHECK']['predicted_verdict']}`) | Accuracy / F1 | **{eval_results['CLEARANCE_CHECK']['accuracy']*100:.1f}%** (F1: {eval_results['CLEARANCE_CHECK']['f1_score']:.4f}) | > {eval_results['CLEARANCE_CHECK']['accuracy']*100:.1f}% |
| **`OBJECT_RELATION`** | Médiane d'entraînement ({baselines['OBJECT_RELATION']['predicted_distance']} m) | MAE (mètres) | **{eval_results['OBJECT_RELATION']['mae_m']:.3f} m** | < {eval_results['OBJECT_RELATION']['mae_m']:.3f} m |
| **`FLOORPLAN_READING`** | Mode d'entraînement ({baselines['FLOORPLAN_READING']['predicted_rooms_count']} pièces) | Exact Match Rooms | **{eval_results['FLOORPLAN_READING']['exact_rooms_acc']*100:.1f}%** | > {eval_results['FLOORPLAN_READING']['exact_rooms_acc']*100:.1f}% |
| **`ROOM_TOPOLOGY`** | Mode d'entraînement ({baselines['ROOM_TOPOLOGY']['predicted_room_count']} pièces) | Exact Match Count | **{eval_results['ROOM_TOPOLOGY']['exact_room_count_acc']*100:.1f}%** | > {eval_results['ROOM_TOPOLOGY']['exact_room_count_acc']*100:.1f}% |

---

### 2. Détail par Tâche

#### A. `CLEARANCE_CHECK`
- **Règle Baseline :** {baselines['CLEARANCE_CHECK']['strategy']}
- **Verdict constant prédit :** `{baselines['CLEARANCE_CHECK']['predicted_verdict']}`
- **Distance médiane constante :** `{baselines['CLEARANCE_CHECK']['predicted_distance']} m`
- **Performance sur Validation (N={eval_results['CLEARANCE_CHECK']['sample_count']}) :**
  - Accuracy : **{eval_results['CLEARANCE_CHECK']['accuracy']*100:.2f}%**
  - F1-Score : **{eval_results['CLEARANCE_CHECK']['f1_score']:.4f}**
  - MAE Distance : **{eval_results['CLEARANCE_CHECK']['mae_distance_m']:.3f} m**

#### B. `OBJECT_RELATION`
- **Règle Baseline :** {baselines['OBJECT_RELATION']['strategy']}
- **Distance médiane constante prédite :** `{baselines['OBJECT_RELATION']['predicted_distance']} m` (Moyenne : `{baselines['OBJECT_RELATION']['mean_distance']} m`)
- **Performance sur Validation (N={eval_results['OBJECT_RELATION']['sample_count']}) :**
  - MAE : **{eval_results['OBJECT_RELATION']['mae_m']:.4f} m**
  - Taux de succès ($\\le 0.05$ m) : **{eval_results['OBJECT_RELATION']['success_rate_5cm']*100:.1f}%**

#### C. `FLOORPLAN_READING`
- **Règle Baseline :** {baselines['FLOORPLAN_READING']['strategy']}
- **Valeurs prédites :** `{baselines['FLOORPLAN_READING']['predicted_rooms_count']} rooms`, `{baselines['FLOORPLAN_READING']['predicted_doors_count']} doors`, `{baselines['FLOORPLAN_READING']['predicted_habitable_pixels']} habitable px`
- **Performance sur Validation (N={eval_results['FLOORPLAN_READING']['sample_count']}) :**
  - Exact Match (Rooms) : **{eval_results['FLOORPLAN_READING']['exact_rooms_acc']*100:.2f}%**
  - MAE Doors : **{eval_results['FLOORPLAN_READING']['doors_mae']:.2f}**
  - MAE Habitable Pixels : **{eval_results['FLOORPLAN_READING']['habitable_pixels_mae']:.1f} px**

#### D. `ROOM_TOPOLOGY`
- **Règle Baseline :** {baselines['ROOM_TOPOLOGY']['strategy']}
- **Valeurs prédites :** `{baselines['ROOM_TOPOLOGY']['predicted_room_count']} rooms`, `{baselines['ROOM_TOPOLOGY']['predicted_largest_room_pixels']} px (max)`, `{baselines['ROOM_TOPOLOGY']['predicted_smallest_room_pixels']} px (min)`
- **Performance sur Validation (N={eval_results['ROOM_TOPOLOGY']['sample_count']}) :**
  - Exact Match (Rooms) : **{eval_results['ROOM_TOPOLOGY']['exact_room_count_acc']*100:.2f}%**
  - MAE Largest Room : **{eval_results['ROOM_TOPOLOGY']['largest_room_pixels_mae']:.1f} px**

---

### 3. Statut Gate Baseline 0
```text
BASELINE_GATE = PASS
```
Toutes les tâches disposent d'un baseline trivial déterministe certifié comme niveau de référence incompressible à surpasser.
"""
    report_path = os.path.join(reports_dir, "BASELINE_RESULTS.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)

    return baseline_payload

if __name__ == "__main__":
    train_p = str(REPO_ROOT / "dataset" / "experiments" / "phase4_micro_pilot" / "dataset_a" / "small" / "train.jsonl")
    val_p = str(REPO_ROOT / "dataset" / "experiments" / "phase4_micro_pilot" / "dataset_a" / "small" / "validation.jsonl")
    out_p = str(REPO_ROOT / "experiments" / "phase4_micro_pilot")
    res = run_and_report(train_p, val_p, out_p)
    print(json.dumps(res, indent=2))
