#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Outil de découpage et de sanctuarisation des splits
============================================================
Génère ou met à jour les splits (train / val / test) à partir du Master Dataset.
Applique la vérification stricte de non-contamination via SplitLeakageDetector.
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from dataset_tools.splitting.leak_detector import SplitLeakageDetector, save_split_manifests


def run_splitting_pipeline(base_dir: str):
    """Génère les splits officiels à partir de master_annotations.jsonl."""
    master_path = os.path.join(base_dir, "dataset", "master", "annotations", "master_annotations.jsonl")
    splits_dir = os.path.join(base_dir, "dataset", "splits")
    
    if not os.path.exists(master_path):
        raise FileNotFoundError(f"Master annotations introuvables : {master_path}")
        
    with open(master_path, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]
        
    train_set = [r for r in records if r.get("assigned_split") == "train"]
    val_set = [r for r in records if r.get("assigned_split") == "validation"]
    test_set = [r for r in records if r.get("assigned_split") == "test"]
    
    print(f"--- SPLITTING PIPELINE ---")
    print(f"Total master: {len(records)}")
    print(f"Train: {len(train_set)}, Validation: {len(val_set)}, Test: {len(test_set)}")
    
    detector = SplitLeakageDetector()
    leak_report = detector.check_splits(train_set, val_set, test_set)
    
    if not leak_report["is_clean"]:
        print("[ALERTE] Contamination détectée entre les splits !")
        for leak in leak_report["leakages"]:
            print(f"  - {leak}")
        raise ValueError("Échec de la validation de non-contamination des splits.")
    else:
        print("[OK] Séparation étanche vérifiée : aucune fuite d'image, de hash, de scène ou de consigne.")
        
    saved = save_split_manifests(records, splits_dir)
    print(f"Splits sauvegardés dans {splits_dir} :")
    for s, p in saved.items():
        print(f"  - {s}: {p}")


if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    run_splitting_pipeline(base_dir)
