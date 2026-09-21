# ARCHI-AI — Plan de Téléchargement Progressif

Ce document détaille la feuille de route technique pour le téléchargement progressif et sécurisé des datasets sélectionnés pour ARCHI-AI.

> [!CAUTION]
> **RÈGLE ABSOLUE : AUCUN TÉLÉCHARGEMENT MASSIF N'EST EXÉCUTÉ PENDANT LA PHASE D'AUDIT.**
> Ce plan constitue un protocole d'exécution prêt à l'emploi qui ne sera enclenché qu'après validation explicite de l'utilisateur.

---

## 1. Vue d'Ensemble & Empreinte de Stockage

Pour éviter de saturer l'espace disque de la station de travail, le téléchargement est ordonné par **vagues de priorité** (P0 -> P1 -> P2 -> P3) et s'effectue dans le répertoire standardisé :

`C:\Users\encor\Documents\Devs\AEON-RWKV\ARCHI_AI\dataset\raw\`

### Bilan Prévisionnel d'Espace Disque

| Vague | Datasets Inclus | Volume Brut Estimé | Volume Après Filtrage V1 | Destination `dataset/raw/` |
| :--- | :--- | :--- | :--- | :--- |
| **Vague P0 (Socle Libre Prioritaire)** | ResPlan, StructScan3D, MSD, IL3D (sous-ensemble) | ~35 GB | ~8 GB | `dataset/raw/p0_core_free/` |
| **Vague P1 (Styles & Plans Réels)** | MMIS, CubiCasa5K (échantillon) | ~45 GB | ~12 GB | `dataset/raw/p1_styles_plans/` |
| **Vague P2 (Raisonnement Spatial)** | M3DLayout, Structured3D (pack léger), HSSD | ~65 GB | ~15 GB | `dataset/raw/p2_spatial/` |
| **Vague P3 (Benchmarks Holdout & RAG)** | SpatialGen-Bench, BIM/IFC QA, Trends 2026 | ~15 GB | ~5 GB | `dataset/raw/p3_bench_rag/` |
| **TOTAL TOUTES VAGUES** | **11 sources ciblées** | **~160 GB** | **~40 GB** | — |

---

## 2. Protocole par Source Recommandée

### 2.1 ResPlan (Priorité P0 — Plans 2D Vectoriels)
- **Taille estimée :** 297,2 MB.
- **Espace nécessaire :** 1 GB (archive + décompression).
- **Priorité :** `P0 (Immédiate)`
- **Source :** Kaggle (`resplan/resplan`)
- **Méthode recommandée :**
  ```powershell
  # Utilisation de l'API kagglehub en Python ou CLI
  kaggle datasets download -d resplan/resplan -p dataset/raw/resplan --unzip
  ```
- **Destination :** `ARCHI_AI/dataset/raw/resplan/`
- **Licence :** CC BY 4.0 (vérifiée).
- **Validation nécessaire :** Vérification de la présence de `ResPlan_dataset.json` et test de lecture via `resplan_utils.py`.

---

### 2.2 StructScan3D (Priorité P0 — Enveloppe Bâtie Réelle)
- **Taille estimée :** ~4,5 GB.
- **Espace nécessaire :** 8 GB.
- **Priorité :** `P0 (Immédiate)`
- **Source :** GitHub / Zenodo MDPI Sensors (`ishraqrc/StructScan3D`)
- **Méthode recommandée :**
  ```powershell
  git clone --depth 1 https://github.com/ishraqrc/StructScan3D.git dataset/raw/structscan3d
  # Téléchargement des archives RGB-D calibrées via les liens officiels du dépôt
  ```
- **Destination :** `ARCHI_AI/dataset/raw/structscan3d/`
- **Licence :** CC BY 4.0.
- **Validation nécessaire :** Contrôle de l'alignement RGB/Depth sur 10 images échantillon.

---

### 2.3 Modified Swiss Dwellings — MSD (Priorité P0 — Bâtiments Collectifs)
- **Taille estimée :** ~1,2 GB.
- **Espace nécessaire :** 3 GB.
- **Priorité :** `P0 (Immédiate)`
- **Source :** GitHub / Kaggle (`caspervanengelenburg/msd-eccv24`)
- **Méthode recommandée :**
  ```powershell
  kaggle datasets download -d wassimjabi/modified-swiss-dwellings-01-json -p dataset/raw/msd --unzip
  ```
- **Destination :** `ARCHI_AI/dataset/raw/msd/`
- **Licence :** CC BY 4.0.
- **Validation nécessaire :** Chargement des graphes d'accessibilité avec `networkx` pour valider l'intégrité des structures.

---

### 2.4 IL3D (Priorité P0 — Raisonnement Spatial en Langage Naturel)
- **Taille estimée :** ~30 GB (pour le package images et descriptions textuelles).
- **Espace nécessaire :** 45 GB.
- **Priorité :** `P0 (Immédiate)`
- **Source :** Hugging Face (`WenxuZhou/IL3D`)
- **Méthode recommandée :**
  ```powershell
  # Téléchargement sélectif des descriptions et rendus (sans les gros nuages de points bruts)
  huggingface-cli download WenxuZhou/IL3D --include "descriptions/*" "images/*" "layouts/*" --local-dir dataset/raw/il3d --repo-type dataset
  ```
- **Destination :** `ARCHI_AI/dataset/raw/il3d/`
- **Licence :** Apache-2.0.
- **Validation nécessaire :** Vérification de l'encodage UTF-8 des descriptions textuelles et intégrité JSON.

---

### 2.5 MMIS (Priorité P1 — 40 Styles d'Intérieur & Matériaux)
- **Taille estimée :** ~35 GB (images seules, sans les fichiers audio WAV).
- **Espace nécessaire :** 50 GB.
- **Priorité :** `P1 (Haute)`
- **Source :** GitHub / Dépôt officiel (`AhmedMahmoudMostafa/MMIS`)
- **Méthode recommandée :**
  ```powershell
  git clone --depth 1 https://github.com/AhmedMahmoudMostafa/MMIS.git dataset/raw/mmis_repo
  # Exécution du script de téléchargement filtré pour exclure l'audio (*.wav)
  python dataset/raw/mmis_repo/download_images_only.py --target dataset/raw/mmis
  ```
- **Destination :** `ARCHI_AI/dataset/raw/mmis/`
- **Licence :** CC BY-SA 4.0.
- **Validation nécessaire :** Contrôle de la répartition par dossier des 40 styles et des 5 types de pièces.

---

### 2.6 CubiCasa5K (Priorité P1 — Plans Scannés Réels)
- **Taille estimée :** ~20 GB.
- **Espace nécessaire :** 30 GB.
- **Priorité :** `P1 (Haute)`
- **Source :** Zenodo (`DOI: 10.5281/zenodo.2613548`)
- **Méthode recommandée :**
  ```powershell
  # Téléchargement via curl / wget direct ou kagglehub
  kaggle datasets download -d qmarva/cubicasa5k -p dataset/raw/cubicasa5k --unzip
  ```
- **Destination :** `ARCHI_AI/dataset/raw/cubicasa5k/`
- **Licence :** CC BY-NC 4.0.
- **Validation nécessaire :** Vérification de la présence des fichiers `model.svg` et des images d'origine `original.png`.

---

### 2.7 M3DLayout (Priorité P2 — Agencements Hiérarchiques)
- **Taille estimée :** ~25 GB.
- **Espace nécessaire :** 35 GB.
- **Priorité :** `P2 (Moyenne)`
- **Source :** Hugging Face (`Metaverse-AI-Lab/M3DLayout`)
- **Méthode recommandée :**
  ```powershell
  huggingface-cli download Metaverse-AI-Lab/M3DLayout --local-dir dataset/raw/m3dlayout --repo-type dataset
  ```
- **Destination :** `ARCHI_AI/dataset/raw/m3dlayout/`
- **Licence :** CC BY-NC 4.0.
- **Validation nécessaire :** Test d'intégrité des dictionnaires d'agencement JSON.

---

### 2.8 Structured3D (Priorité P2 — Sous-ensemble Vide/Meublé)
- **Taille estimée :** ~25 GB (uniquement le pack d'annotations + rendus perspectives sélectionnées).
- **Espace nécessaire :** 40 GB.
- **Priorité :** `P2 (Moyenne)`
- **Source :** Formulaire officiel `structured3d-dataset.org` ou Hugging Face `Pointcept/structured3d-compressed`.
- **Méthode recommandée :** Téléchargement ciblé des maisons sélectionnées après validation des conditions d'utilisation.
- **Destination :** `ARCHI_AI/dataset/raw/structured3d/`
- **Licence :** Non-commercial academic.
- **Validation nécessaire :** Vérification de la correspondance exacte entre vue vide et vue meublée.

---

### 2.9 SpatialGen-Bench (Priorité P3 — Benchmark d'Évaluation)
- **Taille estimée :** ~8 GB.
- **Espace nécessaire :** 12 GB.
- **Priorité :** `P3 (Benchmark)`
- **Source :** Hugging Face (`wx91726/SpatialGen-Bench`)
- **Méthode recommandée :**
  ```powershell
  huggingface-cli download wx91726/SpatialGen-Bench --local-dir evaluation/benchmark/spatialgen_bench --repo-type dataset
  ```
- **Destination :** `ARCHI_AI/evaluation/benchmark/spatialgen_bench/`
- **Licence :** CC BY-NC-SA 4.0.
- **Validation nécessaire :** Contrôle de la non-présence dans les répertoires d'entraînement.

---

### 2.10 BIM/IFC Domain QA & Trends 2026 (Priorité P3 — RAG)
- **Taille estimée :** ~50 MB.
- **Espace nécessaire :** 100 MB.
- **Priorité :** `P3 (RAG)`
- **Source :** Dépôt DataDrivenAEC / MyArchitectAI.
- **Méthode recommandée :** Téléchargement des fichiers JSON/CSV textuels légers.
- **Destination :** `ARCHI_AI/dataset/raw/rag_corpus/`
- **Licence :** Open research / Citation autorisée.
- **Validation nécessaire :** Parsing CSV/JSON sans erreur d'encodage.

---

## 3. Procédure de Vérification d'Intégrité Automatisée

À l'issue de chaque vague, un script de vérification cryptographique sera exécuté :

```powershell
# Commande de vérification de l'intégrité (à exécuter lors de la Phase B)
python -m dataset_tools.validation.verify_raw_checksums --input-dir dataset/raw
```

Toute archive corrompue ou incomplète sera purgée et ré-téléchargée avant la phase de normalisation.
