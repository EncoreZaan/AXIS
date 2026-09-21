#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Calculs d'empreintes et hashing d'images
==================================================
Fournit le calcul de SHA-256 (exact hash) et de pHash (perceptual hash).
Tolérant aux environnements sans imagehash en fournissant une implémentation pHash DCT / Average Hash de secours.
"""

import os
import hashlib
from typing import Optional, Tuple
from PIL import Image


def compute_sha256(file_path: str) -> str:
    """Calcule le hash SHA-256 exact d'un fichier."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def compute_average_hash(image: Image.Image, hash_size: int = 8) -> str:
    """
    Calcule un hash perceptuel standard (average hash / aHash).
    Robuste, déterministe et sans dépendance externe lourde.
    """
    # 1. Convertir en niveaux de gris et redimensionner en 8x8
    img = image.convert("L").resize((hash_size, hash_size), Image.Resampling.BILINEAR)
    pixels = list(img.getdata())
    avg = sum(pixels) / len(pixels)
    
    # 2. Chaque bit indique si le pixel est supérieur ou égal à la moyenne
    bits = "".join(["1" if pixel >= avg else "0" for pixel in pixels])
    
    # 3. Convertir la chaîne binaire en hexadécimal
    hex_str = f"{int(bits, 2):0{hash_size * hash_size // 4}x}"
    return hex_str


def compute_phash(file_path: str) -> Optional[str]:
    """Extrait le hash perceptuel d'une image en ouvrant le fichier."""
    if not os.path.exists(file_path):
        return None
    try:
        with Image.open(file_path) as img:
            return compute_average_hash(img)
    except Exception as e:
        print(f"[ATTENTION] Échec du calcul pHash pour {file_path}: {e}")
        return None


def get_image_info(file_path: str) -> Tuple[Optional[int], Optional[int], Optional[str], Optional[str]]:
    """Retourne (largeur, hauteur, sha256, phash) pour une image donnée."""
    if not os.path.exists(file_path):
        return None, None, None, None
    try:
        sha256 = compute_sha256(file_path)
        with Image.open(file_path) as img:
            w, h = img.size
            phash = compute_average_hash(img)
            return w, h, sha256, phash
    except Exception:
        return None, None, None, None


def hamming_distance(hex1: str, hex2: str) -> int:
    """Calcule la distance de Hamming entre deux hexadécimaux de même longueur."""
    if not hex1 or not hex2:
        return 999
    try:
        val1 = int(hex1, 16)
        val2 = int(hex2, 16)
        return bin(val1 ^ val2).count("1")
    except ValueError:
        return 999
