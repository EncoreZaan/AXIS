#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AXIS Phase 6B — Independent Pre-Flight Cryptographic Gate Verification
"""

import sys
import json
import hashlib
from pathlib import Path

RUN021_DIR = Path("/workspace/AXIS/RUN-021-SPATIAL-SUPERVISION")
HASHES_JSON_PATH = RUN021_DIR / "hashes.json"

REQUIRED_FILES = [
    "DATASET_LOCK.md",
    "hashes.json",
    "FINAL_GATE.md",
    "dataset_config.json",
    "training_config_proposal.yaml",
    "train.jsonl",
    "validation.jsonl",
    "test.jsonl"
]

ALL_LOCKED_FILES = [
    "manifest.jsonl",
    "dataset_manifest.jsonl",
    "train.jsonl",
    "validation.jsonl",
    "test.jsonl",
    "dataset_config.json",
    "DATA_CAPABILITY_AUDIT.md",
    "SPATIAL_RELATION_DEFINITIONS.md",
    "SPLIT_REPORT.md",
    "LEAKAGE_REPORT.md",
    "DATA_QUALITY_REPORT.md",
    "MANUAL_AUDIT.md"
]

def main():
    print("=" * 60)
    print("AXIS PHASE 6B — INDEPENDENT PRE-FLIGHT CRYPTOGRAPHIC GATE")
    print("=" * 60)

    if not HASHES_JSON_PATH.exists():
        print(f"ERROR: hashes.json missing at {HASHES_JSON_PATH}")
        sys.exit(1)

    hashes_data = json.loads(HASHES_JSON_PATH.read_text(encoding="utf-8"))
    
    all_matched = True
    results = {}

    print("\n--- Verifying hashes.json certified entries ---")
    for fname in ALL_LOCKED_FILES:
        fpath = RUN021_DIR / fname
        if not fpath.exists():
            print(f"FAILED: {fname} does not exist!")
            all_matched = False
            continue
        
        content = fpath.read_bytes()
        calculated_sha = hashlib.sha256(content).hexdigest()
        expected_sha = hashes_data[fname]["sha256"]
        expected_size = hashes_data[fname]["size_bytes"]
        
        match = (calculated_sha == expected_sha and len(content) == expected_size)
        results[fname] = {
            "calculated_sha256": calculated_sha,
            "expected_sha256": expected_sha,
            "size": len(content),
            "match": match
        }
        status_str = "PASS" if match else "FAIL"
        print(f"[{status_str}] {fname}: {calculated_sha} (size: {len(content)})")
        if not match:
            all_matched = False

    print("\n--- Additional Required Pre-Flight Files ---")
    extra_files = ["DATASET_LOCK.md", "FINAL_GATE.md", "training_config_proposal.yaml", "hashes.json"]
    for fname in extra_files:
        fpath = RUN021_DIR / fname
        if not fpath.exists():
            print(f"FAILED: {fname} does not exist!")
            all_matched = False
            continue
        content = fpath.read_bytes()
        calculated_sha = hashlib.sha256(content).hexdigest()
        results[fname] = {
            "calculated_sha256": calculated_sha,
            "size": len(content)
        }
        print(f"[VERIFIED] {fname}: {calculated_sha} (size: {len(content)})")

    print("\n" + "=" * 60)
    if all_matched:
        print("PRE-FLIGHT GATE VERDICT: PASS")
        print("TRAINING_PRE_FLIGHT_PASSED = YES")
    else:
        print("PRE-FLIGHT GATE VERDICT: FAIL")
        print("TRAINING_ALLOWED = NO")
        print("STOP")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()
