# ARCHI-AI — Matrice de Preprocessing & Normalisation (`DATASET_PREPROCESSING_MATRIX`)

> **Date :** 21 septembre 2026  
> **Statut :** MATRICE EXHAUSTIVE DE TRANSFORMATION DU CORPUS RAW  
> **Pipeline :** [`ARCHI_AI/dataset_tools/preprocessing/`](file:///c:/Users/encor/Documents/Devs/AEON-RWKV/ARCHI_AI/dataset_tools/preprocessing/)  
> **Master Dataset :** `ARCHI_AI/dataset/master/v1/`  
> **Manifeste :** [`dataset/processed/metadata/PREPROCESSING_MANIFEST.json`](file:///c:/Users/encor/Documents/Devs/AEON-RWKV/ARCHI_AI/dataset/processed/metadata/PREPROCESSING_MANIFEST.json)

---

## 1. Matrice Exhaustive des Sources Traitées

| # | Identifiant Source | Modalité RAW | Formats RAW | Éléments Normalisés | Statut Juridique | Destination Cognitive | Conservation d'Information | Statut Pipeline |
| :- | :--- | :--- | :--- | :---: | :--- | :--- | :---: | :---: |
| **01** | `CORE_RESPLAN` | Plans 2D Vectoriels | `.pkl` (Shapely) | 17 000 | CC-BY-4.0 | `MULTIUSE` (FINETUNE + TOOL) | 100% (Polygones & graphes réels) | **PASS** |
| **02** | `CORE_RPLAN` | Plans 2D Matriciels | `.png`, `.jsonl` | 15 000 | Open Research | `FINETUNE` | 100% (Paires image/masque) | **PASS** |
| **03** | `CORE_RESBIM_PAIRED` (2D) | Plans 2D Appariés | `.jpg` | 10 | MIT | `MULTIUSE` (FINETUNE + TOOL) | 100% (Plans appariés au BIM) | **PASS** |
| **04** | `CORE_FLOORPLANCAD` | Polylignes CAD | `.png`, `.lock` | **0 (GELÉ)** | **LEGAL_REVIEW_REQUIRED** | `HOLDOUT` (Exclu CORE V1) | 0% (Gel conservatoire) | **GELÉ** |
| **05** | `CORE_IL3D` | Scènes 3D Intérieur | `.json` | 27 816 | Apache-2.0 | `FINETUNE` | 100% (Poses, BBox, Scene Graphs) | **PASS** |
| **06** | `CORE_STRUCTSCAN3D` | Scans RGB-D | `.jpg`, `.png`, `.txt` | 2 594 | CC-BY-4.0 | `FINETUNE` | 100% (Triplets RGB+Depth+Masks) | **PASS** |
| **07** | `CORE_BUILDINGSMART_IFC` | Maquettes BIM IFC | `.ifc` (2x3, 4, 4.3) | 35 | CC-BY-4.0 | `MULTIUSE` (FINETUNE + TOOL + RAG) | 100% (Arborescence spatiale) | **PASS** |
| **08** | `CORE_IFC_BENCH_MODELS` | Maquettes BIM IFC | `.ifc` | 50 | CC-BY-4.0 | `MULTIUSE` (FINETUNE + TOOL + RAG) | 100% (21 projets réels) | **PASS** |
| **09** | `CORE_RESBIM_IFC` | Maquettes BIM IFC | `.ifc` | 10 | MIT | `MULTIUSE` (FINETUNE + TOOL + RAG) | 100% (10 unités résidentielles) | **PASS** |
| **10** | `CORE_POLYHAVEN_MATERIALS`| Matériaux PBR | `.json`, `.png` | 862 | CC0-1.0 | `MULTIUSE` (FINETUNE + RAG) | 100% (Échelles physiques métriques) | **PASS** |
| **11** | `CORE_AMBIENTCG` | Matériaux PBR | `.json` | 100 | CC0-1.0 | `MULTIUSE` (FINETUNE + RAG) | 100% (Profils profonds PBR) | **PASS** |
| **12** | `CORE_POLYHAVEN_LIGHTING` | Panoramas HDRI | `.json`, `.png` | 997 | CC0-1.0 | `MULTIUSE` (FINETUNE + RAG) | 100% (Kelvin, EV, environnements) | **PASS** |
| **13** | `CORE_NORMES_FR` | Textes Réglementaires | `.md` | 12 | Licence Ouverte v2.0 | `RAG` | 100% (Textes officiels inaltérés) | **PASS** |
| **14** | `CORE_ERGONOMIE` | Cotes Anthropométrie | `.json` | 18 | CC0-1.0 / Factuel | `MULTIUSE` (TOOL + RAG) | 100% (Unités cm + SI mètres) | **PASS** |
| **15** | `CORE_MOMA_COLLECTION` | Histoire Architecture | `.csv` | 34 539 | CC0-1.0 | `RAG` | 100% (Département A&D filtré) | **PASS** |
| **16** | `CORE_MET_OPENACCESS` | Arts Décoratifs & Mobilier| `.csv` | 2 458 | CC0-1.0 | `RAG` | 100% (Mobilier d'art filtré) | **PASS** |
| **17** | `CORE_TRENDS_2026` | Enquête prospective | `.csv` | 1 | Interne Recherche | `RAG` | 100% (Tendances contemporaines) | **PASS** |
| **18** | `CORE_IFC_BENCH_QA` (Train)| QA Raisonnement BIM | `.csv` | 512 | CC-BY-4.0 | `FINETUNE` | 100% (Vérité terrain certifiée) | **PASS** |
| **19** | `CORE_IFC_BENCH_QA` (Test) | QA Benchmark BIM | `.csv` | 514 | CC-BY-4.0 | `BENCHMARK` (Sanctuarisé) | 100% (Holdout aveugle garanti) | **PASS** |
| **20** | `CORE_MMMU_ARCHITECTURE` | QA Multimodale Supérieure| `.parquet` | 586 | Apache-2.0 | `BENCHMARK` (Sanctuarisé) | 100% (Diagrammes & vérité terrain) | **PASS** |

---

## 2. Synthèse Globale par Destination Cognitive

| Destination Cognitive | Rôle Système ARCHI-AI | Sources Principales | Volume d'Items |
| :--- | :--- | :--- | :---: |
| **`FINETUNE`** | Entraînement des poids VLM (perception, flux, agencement) | IL3D, RPLAN, StructScan3D, IFC-Bench QA train | ~45 922 items |
| **`MULTIUSE`** | Exploitation conjointe (Fine-Tuning VLM + Outils déterministes / RAG) | ResPlan (17k), 95 maquettes IFC, Matériaux PBR, HDRIs, Ergonomie | ~18 994 items |
| **`RAG`** | Indexation vectorielle / BM25 (lois, monographies, fiches techniques) | MoMA A&D, The Met, Normes FR (CCH, PMR, ERP), Tendances 2026 | ~37 010 items |
| **`BENCHMARK`** | Sanctuarisé pour évaluation aveugle (0 contamination d'apprentissage) | MMMU Architecture (586), IFC-Bench QA test (514) | **1 100 items** |
| **`HOLDOUT`** | Isolé pour revue juridique ou recherche | FloorPlanCAD (359 images CAD) | **359 items** |

---

## 3. Conformité aux Règles Absolues

1. **Aucun RAW modifié ni supprimé** : 100% des fichiers dans `dataset/raw/` sont strictement identiques à leur état d'acquisition.
2. **Aucune dimension inventée** : les échelles inconnues restent `null`.
3. **Aucune règle artificielle fabriquée** : les textes réglementaires sont repris in extenso sans interprétation biaisée.
4. **Conservation intégrale de la provenance** : chaque entité possède son enregistrement dans `provenance.jsonl`.
5. **Sanctuarisation de FloorPlanCAD** : 0 élément admis dans le pool CORE V1.
6. **Étanchéité Benchmarks** : MMMU et IFC-Bench test sont isolés avec `is_benchmark_holdout = True`.
