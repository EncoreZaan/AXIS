# -*- coding: utf-8 -*-
"""
ARCHI-AI — Point d'Entrée CLI du Pipeline de Prétraitement
==========================================================
Exécute la normalisation canonique du corpus brut ARCHI-AI vers :
- ARCHI_AI/dataset/processed/
- ARCHI_AI/dataset/master/v1/

Usage :
    python -m dataset_tools.preprocessing.run --source all
    python -m dataset_tools.preprocessing.run --source resplan --limit 100
    python -m dataset_tools.preprocessing.run --source ifc_bench_qa
"""

import argparse
from pathlib import Path
import sys
import json

# Définir le path pour importer ARCHI_AI
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from dataset_tools.preprocessing.assembler import MasterDatasetAssembler
from dataset_tools.preprocessing.registry import list_available_sources


def main():
    parser = argparse.ArgumentParser(description="Pipeline de normalisation canonique ARCHI-AI")
    parser.add_argument(
        "--source",
        type=str,
        default="all",
        help="Source à traiter ('all' pour toutes les sources, ou clé spécifique ex: resplan, il3d, mmmu...)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limite d'éléments par source (optionnel, pour tests ou exécutions partielles)"
    )
    parser.add_argument(
        "--raw-dir",
        type=str,
        default=str(BASE_DIR / "dataset" / "raw" / "external"),
        help="Répertoire racine des données RAW externes"
    )
    parser.add_argument(
        "--processed-dir",
        type=str,
        default=str(BASE_DIR / "dataset" / "processed"),
        help="Répertoire racine des données normalisées (processed)"
    )
    parser.add_argument(
        "--master-dir",
        type=str,
        default=str(BASE_DIR / "dataset" / "master" / "v1"),
        help="Répertoire du Master Dataset V1"
    )

    args = parser.parse_args()

    raw_root = Path(args.raw_dir)
    processed_root = Path(args.processed_dir)
    master_root = Path(args.master_dir)

    print("=" * 70)
    print("ARCHI-AI — NORMALISATION DU CORPUS & MASTER DATASET INTERMÉDIAIRE V1")
    print("=" * 70)
    print(f"Racine RAW       : {raw_root}")
    print(f"Sortie Processed : {processed_root}")
    print(f"Sortie Master V1 : {master_root}")
    print(f"Source demandée  : {args.source}")
    print(f"Limite par source: {args.limit or 'Illimité'}")
    print("-" * 70)

    if args.source == "all":
        sources_to_run = list_available_sources()
    else:
        req_sources = [s.strip().lower() for s in args.source.split(",")]
        sources_to_run = [s for s in req_sources if s in list_available_sources()]
        if not sources_to_run:
            print(f"Erreur : Aucune source valide trouvée parmi {req_sources}")
            print(f"Sources disponibles : {list_available_sources()}")
            sys.exit(1)

    assembler = MasterDatasetAssembler(
        raw_root=raw_root,
        processed_root=processed_root,
        master_root=master_root
    )

    manifest = assembler.run(
        sources=sources_to_run,
        default_limit=args.limit
    )

    print("\n" + "=" * 70)
    print("RÉSULTAT DE LA NORMALISATION DU MASTER DATASET V1")
    print("=" * 70)
    print(f"Éléments normalisés totaux : {manifest['total_items']:,}")
    print(f"Durée totale d'exécution   : {manifest['total_duration_seconds']}s")
    print(f"Stockage utilisé sur disque: {manifest['storage_used_mb']} Mo")
    print("\nRépartition par Modalité :")
    for mod, count in manifest["modality_breakdown"].items():
        print(f"  - {mod:<22}: {count:,}")
    print("\nRépartition par Routage Cognitif :")
    for r, count in manifest["routing_breakdown"].items():
        print(f"  - {r:<22}: {count:,}")
    print("\nPartitions Étanches (Splits) :")
    for s_name, count in manifest["splits"].items():
        print(f"  - {s_name:<24}: {count:,}")
    print("\nManifeste sauvegardé dans :")
    print(f"  {assembler.manifest_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
