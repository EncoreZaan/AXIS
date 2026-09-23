#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AXIS Phase 6B — Environment Snapshot Generator
"""

import sys
import os
import json
import subprocess
import platform
import importlib.metadata
from pathlib import Path

def main():
    import torch
    import transformers
    import peft
    import bitsandbytes
    import qwen_vl_utils
    import PIL
    import numpy

    workspace = Path("/workspace/AXIS")
    output_dir = workspace / "RUN-022-SPATIAL-GROUNDING-PILOT"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Git info
    git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=workspace).decode().strip()
    git_status = subprocess.check_output(["git", "status", "--short"], cwd=workspace).decode().strip()
    git_diff = subprocess.check_output(["git", "diff"], cwd=workspace).decode().strip()

    # nvidia-smi
    try:
        nvidia_smi = subprocess.check_output(["nvidia-smi"], cwd=workspace).decode()
    except Exception as e:
        nvidia_smi = str(e)

    # pip freeze
    pip_freeze = subprocess.check_output([sys.executable, "-m", "pip", "freeze"]).decode().strip().splitlines()

    # Driver & GPU
    cuda_available = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if cuda_available else "None"
    gpu_vram_total_mib = (torch.cuda.get_device_properties(0).total_memory / (1024**2)) if cuda_available else 0

    try:
        qwen_vl_utils_ver = importlib.metadata.version("qwen-vl-utils")
    except Exception:
        qwen_vl_utils_ver = getattr(qwen_vl_utils, "__version__", "unknown")

    snapshot = {
        "run_id": "RUN-022-SPATIAL-GROUNDING-PILOT",
        "os": platform.platform(),
        "python_version": sys.version,
        "pytorch_version": torch.__version__,
        "cuda_version": torch.version.cuda,
        "cuda_available": cuda_available,
        "nvidia_driver": "580.159.04",
        "gpu_name": gpu_name,
        "gpu_vram_total_mib": gpu_vram_total_mib,
        "transformers_version": transformers.__version__,
        "peft_version": peft.__version__,
        "bitsandbytes_version": bitsandbytes.__version__,
        "qwen_vl_utils_version": qwen_vl_utils_ver,
        "pillow_version": PIL.__version__,
        "numpy_version": numpy.__version__,
        "git_commit": git_commit,
        "git_status": git_status,
        "git_diff": git_diff,
        "nvidia_smi": nvidia_smi,
        "pip_freeze": pip_freeze
    }

    out_file = output_dir / "environment_snapshot.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    print(f"Environment snapshot captured successfully to {out_file}")

if __name__ == "__main__":
    main()
