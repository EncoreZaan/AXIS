# -*- coding: utf-8 -*-
"""
ARCHI-AI — Environment Inspector & Fingerprinter
================================================
Gathers precise hardware and software execution environment details:
- OS & Architecture
- Python, Torch, CUDA, CuDNN
- GPU name, VRAM total / available
- CPU info & RAM total / available
- Installed package versions
Outputs a certified environment.json.
"""

import sys
import os
import json
import platform
import psutil

def get_installed_version(package_name: str) -> str:
    try:
        if package_name == "python":
            return sys.version.split()[0]
        mod = __import__(package_name)
        return getattr(mod, "__version__", "unknown")
    except ImportError:
        return "missing"

def inspect_environment(output_path: str = None) -> dict:
    import torch

    cuda_avail = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if cuda_avail else "None"
    gpu_memory = (
        torch.cuda.get_device_properties(0).total_memory if cuda_avail else 0
    )
    gpu_memory_gb = round(gpu_memory / (1024 ** 3), 2) if cuda_avail else 0.0

    ram = psutil.virtual_memory()
    total_ram_gb = round(ram.total / (1024 ** 3), 2)
    avail_ram_gb = round(ram.available / (1024 ** 3), 2)

    env_data = {
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
        },
        "hardware": {
            "gpu_name": gpu_name,
            "cuda_available": cuda_avail,
            "cuda_version": torch.version.cuda if cuda_avail else None,
            "cudnn_version": torch.backends.cudnn.version() if cuda_avail and torch.backends.cudnn.is_available() else None,
            "gpu_memory_bytes": gpu_memory,
            "gpu_memory_gb": gpu_memory_gb,
            "cpu_physical_cores": psutil.cpu_count(logical=False),
            "cpu_logical_cores": psutil.cpu_count(logical=True),
            "ram_total_gb": total_ram_gb,
            "ram_available_gb": avail_ram_gb,
        },
        "python": sys.version,
        "packages": {
            "python": sys.version.split()[0],
            "torch": get_installed_version("torch"),
            "torchvision": get_installed_version("torchvision"),
            "numpy": get_installed_version("numpy"),
            "scipy": get_installed_version("scipy"),
            "transformers": get_installed_version("transformers"),
            "datasets": get_installed_version("datasets"),
            "sklearn": get_installed_version("sklearn"),
            "peft": get_installed_version("peft"),
            "accelerate": get_installed_version("accelerate"),
            "bitsandbytes": get_installed_version("bitsandbytes"),
            "pillow": get_installed_version("PIL"),
        },
        "cuda": torch.version.cuda if cuda_avail else None,
        "cuda_available": cuda_avail,
        "gpu_name": gpu_name,
        "gpu_memory": f"{gpu_memory_gb} GB",
    }

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(env_data, f, indent=2)

    return env_data

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "environment.json"
    data = inspect_environment(out)
    print(f"[OK] Environment fingerprinted to {out}")
    print(json.dumps(data, indent=2))
