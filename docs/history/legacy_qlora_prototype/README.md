# Legacy QLoRA Prototype (Superseded, Archived for Traceability)

> **Status:** HISTORICAL / NON-CANONICAL. Do not use for reproduction.
> **Canonical replacement:** [`experiment_package/`](../../../experiment_package/) at the repository root.

## Why this exists

Two divergent implementations of a QLoRA training script for
`Qwen2-VL-7B-Instruct` existed in the repository:

1. `scripts/train_qlora.py` + `configs/qlora_experiment.yaml` (this archive) —
   an earlier prototype that resolved dataset paths by joining them with a
   hardcoded, machine-specific base directory (`ARCHI_AI/dataset/`,
   `ARCHI_AI/outputs/`). Run from the repository root, this only worked on
   the original author's local checkout and could not be reproduced by an
   external researcher without manually recreating that exact folder layout.
2. `experiment_package/train_qlora.py` + `experiment_package/config/qlora_experiment.yaml`
   — a self-contained, portable package whose script resolves every path
   relative to its own package root (`PACKAGE_ROOT = Path(__file__).resolve().parent`),
   independent of the machine or working directory it is run from.

The software stack pinned in `experiment_package/requirements.txt`
(`torch==2.6.0`, `transformers==5.17.0`, `peft==0.21.0`, `bitsandbytes==0.50.2`)
matches exactly the stack reported for the VLM QLoRA proof-of-concept in
[`EXPERIMENTS.md`](../../../EXPERIMENTS.md) and [`REPRODUCIBILITY.md`](../../../REPRODUCIBILITY.md#configuration-2-remote--cluster-node).
This confirms `experiment_package/` is the script that actually produced the
published proof-of-concept results, not the prototype archived here.

## What was fixed for this archive

The hardcoded `ARCHI_AI/dataset/` and `ARCHI_AI/outputs/` paths in
`qlora_experiment.yaml` here have been left as originally written — this
snapshot is preserved as-is for historical accuracy, not corrected in place,
since it is no longer meant to be run. If you need a working, path-portable
QLoRA training entry point, use `experiment_package/train_qlora.py` with
`experiment_package/config/qlora_experiment.yaml`, and see
`experiment_package/README.md` for the exact commands.

## Traceability note

Nothing here was deleted. This move only relocates the two files so the
repository has a single canonical, working reproduction path
(`experiment_package/`) while preserving the earlier prototype for scientific
traceability, per the project's history-preservation policy
(see [`docs/history/project-history.md`](../project-history.md)).
