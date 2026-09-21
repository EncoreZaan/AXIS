# Architecture du Dataset ARCHI-AI

## 1. Vue d'ensemble et Philosophie

L'infrastructure du dataset ARCHI-AI est conçue pour passer de façon fiable et rigoureuse de **25 exemples expérimentaux** à **5 000, 10 000 et 50 000+ exemples** d'architecture et de design spatial de haute qualité.

Elle repose sur 5 piliers fondamentaux :
1. **Traçabilité & Provenance :** Chaque exemple est associé à une source, une licence, un projet et une scène clairement identifiés.
2. **Sanctuarisation des Évaluations :** Les splits `validation` et `test` sont strictement étanches vis-à-vis du `train` (aucun partage d'image, de hash, de scène ou de projet).
3. **Master Schema Extensible :** Séparation du stockage de vérité terrain (`MasterAnnotation`) et des formats d'export d'entraînement (`Qwen2-VL JSONL`).
4. **Assurance Qualité Déterministe :** Validation schématique (Pydantic + JSON Schema), intégrité des fichiers images, contrôle anti-hallucination gradué (`PASS`, `WARNING`, `REVIEW`, `FAIL`).
5. **Taxonomie Métier Découplée :** 14 compétences architecturales (`Skill`), 12 modes d'apprentissage cognitif (`LearningType`) et 10 types de documents (`DocumentType`).

---

## 2. Arborescence du Système

```
ARCHI_AI/
├── dataset/
│   ├── raw/                              # Fichiers bruts ingérés et non traités
│   ├── master/
│   │   ├── annotations/
│   │   │   └── master_annotations.jsonl  # Fichier unique de vérité terrain (Master)
│   │   └── schema/
│   │       ├── models.py                 # Modèles Pydantic v2
│   │       └── master_schema.json        # Schéma JSON exporté
│   ├── images/                           # Dépôt d'images source
│   ├── splits/                           # Partitions étanches (train, validation, test)
│   │   ├── train.jsonl
│   │   ├── validation.jsonl
│   │   └── test.jsonl
│   ├── versions/                         # Instantanés figés et reproductibles
│   │   └── v0.1-micro-baseline/
│   └── export_qwen/                      # Exports conversationnels prêts pour Qwen2-VL
│
├── dataset_tools/
│   ├── validation/
│   │   ├── taxonomy.py                   # Enums et taxonomies métier
│   │   ├── qa_validator.py               # Moteur QA multicritères & anti-hallucination
│   │   └── migrate_historical.py         # Script de migration vers le schéma master
│   ├── deduplication/
│   │   ├── hasher.py                     # Algorithmes SHA-256 et pHash (perceptuel)
│   │   └── dedup_detector.py             # Détecteur de doublons et near-duplicates
│   ├── splitting/
│   │   ├── leak_detector.py              # Détection de fuite (image/scène/projet/question)
│   │   └── make_splits.py                # Découpage et vérification d'étanchéité
│   ├── export/
│   │   └── export_qwen_vl.py             # Export vers le format d'entraînement
│   └── reporting/
│       └── dataset_reporter.py           # Génération de rapports statistiques complets
│
├── evaluation/
│   ├── baseline/                         # Résultats immuables de la baseline historique
│   ├── benchmark/                        # Définition des 13 axes d'évaluation
│   ├── runners/                          # Moteurs de benchmark et d'évaluation
│   └── reports/                          # Rapports de benchmark générés
│
├── tests/                                # Suite de tests automatisés (pytest)
├── config/                               # Configurations YAML d'entraînement et d'inférence
└── docs/                                 # Documentation technique exhaustive
```

---

## 3. Flux de Données (Data Pipeline)

```
       [ Nouvelles données / Ingestion ]
                       │
                       ▼
            [ Master Dataset Schema ]
            (dataset/master/schema/)
                       │
                       ▼
            [ Contrôle Qualité (QA) ]
            (Images, Taxonomie, Prudence épistémique)
                       │
                       ▼
         [ Déduplication (Exact & pHash) ]
                       │
                       ▼
       [ Sanctuarisation & Splits étanches ]
       (Train / Validation / Test sans fuite de scène)
                       │
                       ▼
     [ Exportateur Dédié (Qwen2-VL JSONL) ]
                       │
                       ▼
          [ Entraînement QLoRA / PEFT ]
             (train_qlora.py)
```
