# AXIS — Developer & Engineering Guide

This guide is intended for engineers and developers working on the AXIS codebase.

---

## 1. Environment Requirements

- **Operating System:** Windows 10/11, Ubuntu 20.04+, or macOS
- **Python Version:** `3.10` or `3.11` (Python 3.11.9 recommended)
- **CUDA Runtime (optional):** CUDA 12.1+ / 12.4 for GPU-accelerated training and inference
- **Disk Space:** ~5 GB for code, configs, and dependencies; ~15 GB if local RAW datasets are mirrored.

---

## 2. Installation & Quickstart

```bash
# 1. Clone repository
git clone https://github.com/EncoreZaan/AXIS.git
cd AXIS

# 2. Virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1

# 3. Dependencies
pip install -r requirements.txt
pip install -e .

# 4. Verify test suite
pytest tests
```

---

## 3. Directory Layout & Module Overview

```text
AXIS/
├── dataset_tools/             # Data processing & verification suite
│   ├── acquisition/           # Ingestion scripts for 19 physical sources
│   ├── experiments/           # Dataset A builders, validators, and auditors
│   ├── master_pipeline/       # Master Dataset v2 orchestrator & config
│   ├── preprocessing/         # Rasterization, CAD cleaning, schema normalization
│   ├── resplan/               # ResPlan forensic auditor and topological validator
│   ├── splitting/             # Zero-leakage project group splitter
│   └── supervision/           # Question/answer generators & multi-dimensional verifiers
├── evaluation/                # Evaluation harness, benchmark runners, metrics
├── experiments/               # Experiment configs, metrics, and JSON run summaries
├── scripts/                   # CLI entrypoints (build, evaluate, validate, train)
├── configs/                   # Configuration files (YAML / JSON)
├── tests/                     # 99 pytest test cases
└── docs/                      # Extensive research, forensic, and historical reports
```

---

## 4. Running Code Quality & Tests

The project uses `pytest` for all unit and integration testing.

```bash
# Run all tests
pytest tests

# Run specific test modules
pytest tests/test_phase4_dataset_a.py
pytest tests/test_phase3_scientific_readiness.py
pytest tests/test_supervision_engine.py

# Run with verbose output and timing
pytest tests -v --durations=10
```

---

## 5. Coding & Integrity Guidelines

- **Deterministic Randomness:** Always pass explicit seeds (`seed=42`) to NumPy, PyTorch, and random split generators.
- **Path Resolution:** Always resolve paths relative to `Path(__file__).resolve()` or root configuration. Never hardcode absolute user directories.
- **Contract Enforcement:** All supervised tasks must enforce typed target schemas using `pydantic` or dataclasses.
