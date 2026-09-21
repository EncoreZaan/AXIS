# ARCHI-AI — Architecture du Pipeline de Preprocessing & Normalisation

## 1. Vue d'Ensemble

Le pipeline de preprocessing d'ARCHI-AI assure la transition industrielle et reproductible entre le corpus brut et les couches exploitables du système :

```text
       ┌────────────────────────────────────────────────────────┐
       │                1. RAW CORPUS (IMMUTABLE)               │
       │  3,48 Go • 66 847 fichiers • 16 sources vérifiées      │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │         2. ADAPTATEURS CANONIQUES SPÉCIALISÉS          │
       │  dataset_tools/preprocessing/{floorplans,spatial,bim,  │
       │                               materials,lighting,text, │
       │                               multimodal}/             │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │          3. COUCHE PROCESSED / NORMALISÉE              │
       │  dataset/processed/                                    │
       │  ├── plans/      ├── spatial/   ├── bim/               │
       │  ├── materials/  ├── lighting/  ├── text/              │
       │  ├── multimodal/ └── metadata/ (provenance.jsonl)      │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │         4. MASTER DATASET INTERMÉDIAIRE V1             │
       │  dataset/master/v1/                                    │
       │  ├── master_records.jsonl                              │
       │  ├── splits/ (train, validation, benchmark_test)       │
       │  └── routing_index.json (FINETUNE, RAG, TOOL, BENCH)   │
       └────────────────────────────────────────────────────────┘
```

---

## 2. Responsabilités des Couches

### A. Couche RAW (`dataset/raw/external/core/`)
- **Règle absolue : Immutabilité totale.**
- Fichiers sources intouchables : aucune écriture, aucune modification, aucune suppression.
- Comprend les archives originales (`.zip`), les données extraites, les catalogues JSON, les maquettes IFC, les fichiers Parquet et les notices CSV.

### B. Couche PROCESSED (`dataset/processed/`)
- Données nettoyées, standardisées et représentées selon le schéma canonique pivot.
- Stockage structuré par modalité :
  - `plans/` : plans vectoriels avec polygones métriques, masques matriciels et graphes d'adjacence.
  - `spatial/` : agencements 3D avec boîtes englobantes, orientations, coordonnées réelles et *scene graphs*.
  - `bim/` : résumés structurés des maquettes IFC extraits avec `ifcopenshell`.
  - `materials/` : textures PBR avec dimensions physiques certifiées en mètres.
  - `lighting/` : panoramas HDRI avec balance des blancs Kelvin et valeurs d'exposition (EV).
  - `text/` :
    - `regulatory/` : textes réglementaires découpés fidèlement pour le RAG.
    - `ergonomie/` : cotes anthropométriques (unités originales + normalisation SI).
    - `museum/` : monographies d'architecture et de design (MoMA, The Met).
    - `trends/` : enquêtes prospectives d'agencement.
  - `multimodal/` : questions/réponses expertes IFC-Bench et MMMU.
  - `metadata/` : `provenance.jsonl` consignant chaque chaîne `source -> RAW -> id -> transformation -> master_id`.

### C. Couche MASTER INTERMÉDIAIRE (`dataset/master/v1/`)
- Enregistrements prêts à alimenter la future phase de génération de supervision.
- **Routage cognitif explicite** :
  - `FINETUNE` : perception visuelle, orientation 3D, agencement, critique architecturale.
  - `RAG` : articles réglementaires, histoire du design, propriétés techniques des matériaux.
  - `TOOL` : cotes déterministes, calculs de surfaces, graphes topologiques de circulation.
  - `BENCHMARK` : ensembles sanctuarisés étanches (MMMU Architecture, IFC-Bench test split).
  - `HOLDOUT` : données isolées ou nécessitant revue (FloorPlanCAD).
- **Partitions étanches** : séparation physique et logique dans `splits/`.

---

## 3. Gestion de la Mémoire et Scalabilité

Pour traiter sereinement plus de 60 000 entités sans risque de saturation RAM (`OutOfMemoryError`) :
- **Architecture en streaming (générateurs `yield`)** : chaque préprocesseur émet ses enregistrements un à un.
- **Écriture progressive en JSON Lines (`.jsonl`)** : pas de structure globale en mémoire tampon.
- **Traitement sélectif ou global** : possibilité de normaliser une seule source (`--source resplan`) ou l'ensemble (`--source all`).
