#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Script de diagnostic et validation de l'environnement distant
========================================================================
Vérifie rigoureusement la disponibilité des dépendances matérielles et logicielles
pour l'entraînement QLoRA 4-bit de Qwen2-VL-7B-Instruct sur GPU 24 Go.
"""

import sys
import os
import importlib
import importlib.metadata
import argparse
from pathlib import Path


def check_python() -> bool:
    v = sys.version_info
    print(f"[*] Python Version         : {v.major}.{v.minor}.{v.micro} (Build {sys.platform})")
    if (v.major, v.minor) < (3, 10):
        print("    [!] ERREUR : Python 3.10+ est requis (recommandé: 3.11).")
        return False
    return True


def check_pytorch() -> tuple[bool, bool, float, str]:
    """Vérifie PyTorch, CUDA, nom du GPU et VRAM totale."""
    try:
        import torch
        print(f"[*] PyTorch Version        : {torch.__version__}")
    except ImportError:
        print("    [!] ERREUR : PyTorch n'est pas installé.")
        return False, False, 0.0, "None"

    cuda_available = torch.cuda.is_available()
    print(f"[*] CUDA Disponible        : {'OUI' if cuda_available else 'NON'}")

    if not cuda_available:
        print("    [!] ERREUR : Aucun GPU CUDA détecté par PyTorch.")
        return True, False, 0.0, "None"

    cuda_version = torch.version.cuda
    device_count = torch.cuda.device_count()
    device_name = torch.cuda.get_device_name(0)
    total_mem_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)

    print(f"[*] CUDA Runtime Version   : {cuda_version}")
    print(f"[*] Nombre de GPU CUDA     : {device_count}")
    print(f"[*] GPU Principal (Dev 0)  : {device_name}")
    print(f"[*] VRAM Totale Détectée   : {total_mem_gb:.2f} Go")

    return True, True, total_mem_gb, device_name


def check_library(name: str, min_version: str = None) -> tuple[bool, str]:
    """Vérifie la présence et la version d'une bibliothèque Python."""
    try:
        mod = importlib.import_module(name)
        version = getattr(mod, "__version__", None)
        if not version:
            try:
                clean_name = name.replace("_", "-")
                version = importlib.metadata.version(clean_name)
            except Exception:
                version = "Installé (version non exposée)"
        return True, str(version)
    except ImportError:
        return False, "NON INSTALLÉ"


def test_bitsandbytes_cuda() -> bool:
    """Vérifie le chargement des extensions CUDA de bitsandbytes."""
    try:
        import bitsandbytes as bnb
        import torch
        if torch.cuda.is_available():
            # Test simple d'allocation 4-bit
            linear = bnb.nn.Linear4bit(16, 16, bias=False).cuda()
            x = torch.randn(1, 16, device="cuda")
            _ = linear(x)
            print("    -> Extension CUDA BitsAndBytes 4-bit : FONCTIONNELLE")
            return True
        else:
            print("    -> BitsAndBytes importé (test CUDA omis : aucun GPU CUDA actif)")
            return True
    except Exception as e:
        print(f"    [!] AVERTISSEMENT BitsAndBytes CUDA : {e}")
        return False


def check_dataset_integrity(pkg_dir: Path) -> bool:
    """Vérifie que les fichiers de dataset du package existent et sont intègres."""
    train_path = pkg_dir / "dataset" / "train.jsonl"
    val_path = pkg_dir / "dataset" / "validation.jsonl"
    images_dir = pkg_dir / "dataset" / "images"

    ok = True
    if not train_path.exists():
        print(f"    [!] ERREUR : train.jsonl manquant ({train_path})")
        ok = False
    else:
        with open(train_path, "r", encoding="utf-8") as f:
            t_count = sum(1 for line in f if line.strip())
        print(f"[*] Dataset Train          : {train_path.name} ({t_count} exemples)")

    if not val_path.exists():
        print(f"    [!] ERREUR : validation.jsonl manquant ({val_path})")
        ok = False
    else:
        with open(val_path, "r", encoding="utf-8") as f:
            v_count = sum(1 for line in f if line.strip())
        print(f"[*] Dataset Validation     : {val_path.name} ({v_count} exemples)")

    if not images_dir.exists():
        print(f"    [!] ERREUR : Dossier images manquant ({images_dir})")
        ok = False
    else:
        img_count = len(list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.png")))
        print(f"[*] Dossier Images         : {img_count} images présentes")
        if img_count < 25:
            print("    [!] AVERTISSEMENT : Au moins 25 images attendues.")
            ok = False

    return ok


def main():
    parser = argparse.ArgumentParser(description="Vérification environnement ARCHI-AI")
    parser.add_argument(
        "--target-vram-gb",
        type=float,
        default=22.0,
        help="VRAM minimale requise pour déclarer READY FOR TRAINING (défaut : 22.0 Go pour GPU 24 Go)"
    )
    args = parser.parse_args()

    print("=" * 65)
    print("ARCHI-AI: DIAGNOSTIC ENVIRONNEMENT D'ENTRAÎNEMENT DISTANT")
    print("=" * 65)

    pkg_dir = Path(__file__).resolve().parent

    failures = []
    warnings = []

    # 1. Python
    if not check_python():
        failures.append("Version Python incompatible")

    # 2. PyTorch & CUDA & VRAM
    torch_ok, cuda_ok, total_vram, gpu_name = check_pytorch()
    if not torch_ok:
        failures.append("PyTorch manquant")
    elif not cuda_ok:
        failures.append("CUDA non détecté (GPU absent ou driver non lié)")
    else:
        if total_vram < args.target_vram_gb:
            warnings.append(
                f"VRAM détectée ({total_vram:.1f} Go) inférieure au seuil de production cible ({args.target_vram_gb} Go)."
            )

    # 3. Stack Hugging Face & QLoRA
    libs = [
        ("transformers", "5.17.0"),
        ("peft", "0.21.0"),
        ("bitsandbytes", "0.50.2"),
        ("accelerate", "1.15.0"),
        ("qwen_vl_utils", "0.0.14"),
        ("PIL", "12.3.0"),
        ("yaml", "6.0.3"),
    ]

    for lib_name, expected_ver in libs:
        ok, ver = check_library(lib_name)
        display_name = "pillow" if lib_name == "PIL" else ("PyYAML" if lib_name == "yaml" else lib_name)
        print(f"[*] {display_name:<22} : {ver}")
        if not ok:
            failures.append(f"Bibliothèque manquante : {display_name}")

    # 4. Test d'exécution BitsAndBytes CUDA
    if cuda_ok:
        bnb_tested = test_bitsandbytes_cuda()
        if not bnb_tested:
            failures.append("Erreur lors de l'appel du kernel CUDA BitsAndBytes 4-bit")

    # 5. Intégrité des données du package
    print("-" * 65)
    print("Vérification des données locales du package :")
    dataset_ok = check_dataset_integrity(pkg_dir)
    if not dataset_ok:
        failures.append("Incohérence ou fichiers manquants dans le dataset")

    # 6. Conclusion et Verdict
    print("=" * 65)
    if not failures and (cuda_ok and total_vram >= args.target_vram_gb):
        print(">> VERDICT : READY FOR TRAINING")
        print("Toutes les conditions matérielles (GPU 24 Go) et logicielles sont réunies.")
        print("=" * 65)
        sys.exit(0)
    elif not failures and cuda_ok:
        print(">> VERDICT : NOT READY (VRAM INSUFFISANTE POUR GPU CIBLE 24 Go)")
        print(f"Toutes les dépendances logicielles sont validées, mais la VRAM détectée")
        print(f"({total_vram:.1f} Go) est inférieure aux {args.target_vram_gb} Go requis pour l'entraînement distant.")
        for w in warnings:
            print(f"  - {w}")
        print("=" * 65)
        sys.exit(1)
    else:
        print(">> VERDICT : NOT READY")
        print("Des prérequis obligatoires ne sont pas satisfaits :")
        for f in failures:
            print(f"  - [MANQUE] {f}")
        for w in warnings:
            print(f"  - [ATTENTION] {w}")
        print("=" * 65)
        sys.exit(1)


if __name__ == "__main__":
    main()
