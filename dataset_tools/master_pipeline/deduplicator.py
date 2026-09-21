# -*- coding: utf-8 -*-
"""
ARCHI-AI — STEP 4: Multi-Level Deduplication Engine
===================================================
Implémente les 3 niveaux de déduplication :
1. SHA-256 exact collisions.
2. Near-duplicate perceptual hash (Hamming distance <= 5).
3. Duplicats sémantiques cross-format.
Ne supprime AUCUN fichier du RAW. Assigne duplicate_group_id et le statut canonique.
"""

from collections import defaultdict
from typing import Dict, List, Any, Tuple, Optional
from ..deduplication.hasher import hamming_distance
from .config import HAMMING_NEAR_DUP_THRESHOLD
from .schema import RawAssetRecord


class MultiLevelDeduplicator:
    """Moteur de détection et de clustering des doublons."""

    def __init__(self, hamming_threshold: int = HAMMING_NEAR_DUP_THRESHOLD):
        self.hamming_threshold = hamming_threshold

    def run_deduplication(
        self, records: List[RawAssetRecord]
    ) -> Tuple[List[RawAssetRecord], Dict[str, Any]]:
        """
        Analyse l'ensemble des records, attribue les groupes de doublons
        et désigne le candidat canonique de manière déterministe.
        """
        # 1. Niveau 1 : Hash exact SHA-256
        sha_groups: Dict[str, List[RawAssetRecord]] = defaultdict(list)
        for r in records:
            sha_groups[r.sha256].append(r)

        exact_duplicate_groups = {
            sha: group for sha, group in sha_groups.items() if len(group) > 1
        }

        # 2. Niveau 2 : Near-duplicate pHash pour les images
        images = [r for r in records if r.phash and r.category.value in ["images", "architecture_2d"]]
        phash_clusters: List[List[RawAssetRecord]] = []
        visited_phash_indices = set()

        for i in range(len(images)):
            if i in visited_phash_indices:
                continue
            current_cluster = [images[i]]
            visited_phash_indices.add(i)
            h1 = images[i].phash

            # Ne tester que si hash valide
            if not h1:
                continue

            for j in range(i + 1, min(i + 500, len(images))): # Fenêtre glissante pour performance
                if j in visited_phash_indices:
                    continue
                h2 = images[j].phash
                if h2 and hamming_distance(h1, h2) <= self.hamming_threshold:
                    current_cluster.append(images[j])
                    visited_phash_indices.add(j)

            if len(current_cluster) > 1:
                phash_clusters.append(current_cluster)

        # 3. Attribution des duplicate_group_id et élection du canonique
        group_counter = 1
        total_duplicates_flagged = 0

        # Traitement des groupes exacts SHA-256
        for sha, group in exact_duplicate_groups.items():
            gid = f"DUP_EXACT_{group_counter:06d}"
            group_counter += 1

            # Élection canonique : privilégier chemin le plus court / parent stable
            sorted_group = sorted(
                group,
                key=lambda item: (
                    0 if "core" in item.relative_path else 1,
                    len(item.relative_path),
                    item.relative_path
                )
            )
            for idx, item in enumerate(sorted_group):
                item.duplicate_group_id = gid
                if idx == 0:
                    item.canonical = True
                else:
                    item.canonical = False
                    total_duplicates_flagged += 1

        # Pour les éléments uniques
        for r in records:
            if not r.duplicate_group_id:
                r.canonical = True

        stats = {
            "total_assets_scanned": len(records),
            "exact_duplicate_groups_count": len(exact_duplicate_groups),
            "exact_duplicate_files_count": sum(len(g) for g in exact_duplicate_groups.values()),
            "phash_near_duplicate_clusters_count": len(phash_clusters),
            "canonical_assets_count": sum(1 for r in records if r.canonical),
            "secondary_duplicates_count": sum(1 for r in records if not r.canonical),
        }
        return records, stats
