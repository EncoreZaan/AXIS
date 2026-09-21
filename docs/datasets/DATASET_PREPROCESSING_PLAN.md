# ARCHI-AI — Plan de Prétraitement & Chaîne de Transformation V1

Ce document définit la chaîne industrielle de prétraitement (*preprocessing pipeline*) permettant de transformer les données brutes hétérogènes en annotations conformes au **Master Schema Pydantic** d'ARCHI-AI et directement exportables vers **Qwen2-VL**.

---

## 1. Vue Globale de la Chaîne de Traitement

Chaque dataset brut entrant suit rigoureusement les 9 étapes du pipeline :

```text
       ┌───────────────────────┐
       │      1. RAW IN        │ Archives brutes (SVG, PNG, JSON, K-D, PLY)
       └──────────┬────────────┘
                  │
       ┌──────────▼────────────┐
       │   2. NORMALIZATION    │ Redimensionnement, conversion RGB, vector -> raster
       └──────────┬────────────┘
                  │
       ┌──────────▼────────────┐
       │   3. QUALITY CHECK    │ Filtrage résolution min, flou, corruption, contraste
       └──────────┬────────────┘
                  │
       ┌──────────▼────────────┐
       │       4. DEDUP        │ SHA-256 (doublons parfaits) + pHash (similarité >0.92)
       └──────────┬────────────┘
                  │
       ┌──────────▼────────────┐
       │ 5. ANNOTATION MAPPING │ Traduction des labels en compétences, question/réponse
       └──────────┬────────────┘
                  │
       ┌──────────▼────────────┐
       │   6. MASTER SCHEMA    │ Validation stricte Pydantic (MasterAnnotation)
       └──────────┬────────────┘
                  │
       ┌──────────▼────────────┐
       │     7. LEAK CHECK     │ Contrôle étanchéité par scene_id, building_id, pHash
       └──────────┬────────────┘
                  │
       ┌──────────▼────────────┐
       │       8. SPLIT        │ Répartition Train (80%) / Val (10%) / Test (10%)
       └──────────┬────────────┘
                  │
       ┌──────────▼────────────┐
       │    9. QWEN EXPORT     │ Conversion messages conversationnels Qwen2-VL
       └───────────────────────┘
```

---

## 2. Spécifications Détaillées par Étape

### Étape 1 : Ingestion des Données Brutes (RAW IN)
- Lecture depuis `ARCHI_AI/dataset/raw/<source_name>/`.
- Décompression sécurisée et indexation des fichiers d'annotations associés.

### Étape 2 : Normalisation Visuelle & Géométrique (NORMALIZATION)
- **Images photographiques & rendus 3D :**
  - Redimensionnement adaptatif : max 1 280 px sur le grand côté (maintien strict du ratio d'aspect).
  - Suppression des profils de couleur aberrants, conversion standard `RGB` (JPEG qualité 92 ou PNG optimisé).
- **Plans 2D vectoriels (ResPlan, MSD, CubiCasa5K) :**
  - Rendu rasterisé haute netteté : fond blanc neutre, épaisseur de trait calibrée (murs porteurs 3 px, cloisons 1.5 px, symboles 1 px).
  - Élimination des artefacts d'échelle et génération d'une version avec cotations nettoyées.
- **Stockage intermédiaire :** `ARCHI_AI/dataset/images/<source_name>/`.

### Étape 3 : Contrôle Qualité Visuel (QUALITY CHECK)
- Seuil minimal de résolution : largeur et hauteur >= 512 px.
- Détection du flou par variance du laplacien : exclusion des images avec variance < 100.
- Vérification du contraste et rejet des images uniformes (fonds blancs vides ou noirs).

### Étape 4 : Déduplication Exacte & Perceptuelle (DEDUP)
- Calcul de l'empreinte cryptographique **SHA-256** sur chaque fichier image normalisé.
- Calcul de l'empreinte perceptuelle **pHash (Average Hash 64-bit)**.
- Rejet immédiat de tout doublon exact (SHA-256 identique).
- Regroupement des doublons quasi identiques (distance de Hamming pHash <= 4) pour n'en conserver qu'une seule variante représentative.

### Étape 5 : Cartographie Métier & Synthèse Conversationnelle (ANNOTATION MAPPING)
- Mapping de la typologie source vers la taxonomie contrôlée ARCHI-AI :
  - `Domain` : `architecture` ou `interior_design`.
  - `DocumentType` : `photography`, `render_3d`, `plan_2d`.
  - `DifficultyLevel` : assigné selon la complexité spatiale (`beginner` à `expert`).
  - `LearningType` : `analysis`, `observation`, `critique`, `constraint_reasoning`, `pedagogy`.
  - `Skills` : assignation multi-labels parmi les 13 compétences ARCHI-AI.
- Génération de paires question/réponse expertes :
  - Formulation de consignes d'architecte variées (pas de formulation mécanique répétitive).
  - Structuration de la réponse experte avec extraction explicite des `observables`, `interpretations`, `unknowns`, et `constraints`.

### Étape 6 : Validation Pydantic & QA (MASTER SCHEMA)
- Instanciation de l'objet `MasterAnnotation` via `dataset/master/schema/models.py`.
- Validation automatique des invariants :
  - Validité des chemins d'images relatifs existants sur disque.
  - Longueur minimale de la question (>= 5 caractères) et de la réponse (>= 10 caractères).
  - Présence d'au moins une compétence (`skills`).
  - Traçabilité complète de la provenance (`source_name`, `license`, `scene_id`).
- Écriture dans `dataset/master/annotations/v1_<source_name>.json`.

### Étape 7 : Détection Anti-Fuite (LEAK CHECK)
- Utilisation de `dataset_tools.validation.split_leak_detector` :
  - Vérification qu'aucune image n'est présente dans deux splits.
  - **Verrouillage par `scene_id` / `building_id` :** toutes les vues, pièces ou plans d'un même bâtiment doivent être assignés au **même split** (aucun bâtiment ne peut être à la fois en train et en test).
  - Détection de fuite perceptuelle par pHash : aucune image de test ne doit avoir une distance pHash < 8 avec une image d'entraînement.

### Étape 8 : Partitionnement Déterministe (SPLIT)
- Split déterministe basé sur un hachage SHA-256 de l'identifiant de projet/scène avec graine aléatoire fixée (`seed=42`).
- Ratios : **80% Train, 10% Validation, 10% Test**.

### Étape 9 : Export Formaté Qwen2-VL (QWEN EXPORT)
- Utilisation de `dataset_tools.export.export_qwen_vl` :
  - Conversion au schéma JSON conversationnel natif de Qwen2-VL :
    ```json
    {
      "id": "archi_resplan_00142",
      "conversations": [
        {
          "from": "user",
          "value": "<image>\nEn tant qu'architecte, analysez la circulation de ce plan..."
        },
        {
          "from": "assistant",
          "value": "OBSERVATION : Le plan présente une distribution en étoile..."
        }
      ]
    }
    ```
  - Validation que le token `<image>` correspond exactement au nombre d'images déclarées dans l'exemple.

---

## 3. Matrice de Transformation Spécifique par Dataset Retenu

### 3.1 ResPlan
- **Format brut :** Fichier JSON unique contenant 17 000 entrées vectorielles.
- **Script de transformation :** `dataset_tools/preprocessing/convert_resplan.py`
  - Rendu raster des géométries polygonales via `matplotlib`/`Pillow` à 1024x1024 px.
  - Extraction du graphe `networkx` de connectivité des pièces.
  - Génération de questions ciblées : contiguïté de pièces, détection de pièces aveugles, calcul de ratios de surfaces habitables.
  - Ingestion de 1 800 exemples dans le Master Schema.

### 3.2 StructScan3D
- **Format brut :** Images PNG RGB + depth maps 16-bit Kinect.
- **Script de transformation :** `dataset_tools/preprocessing/convert_structscan.py`
  - Sous-échantillonnage temporel : sélection d'une trame toutes les 3 secondes pour éliminer les doublons vidéo.
  - Normalisation des masques de segmentation en 6 classes d'enveloppe bâtie.
  - Génération de questions d'identification structurelle : repérage des baies vitrées, franchissements de portes et jonctions mur/plafond.
  - Ingestion de 500 exemples dans le Master Schema.

### 3.3 Modified Swiss Dwellings (MSD)
- **Format brut :** Plans d'étage d'immeubles collectifs (JSON + PNG).
- **Script de transformation :** `dataset_tools/preprocessing/convert_msd.py`
  - Recadrage et mise à l'échelle des étages d'immeubles.
  - Cartographie des distributions de paliers et d'accès aux logements.
  - Génération de questions sur la distribution collective : accès pompiers, compacité des circulations verticales, double orientation.
  - Ingestion de 800 exemples dans le Master Schema.

### 3.4 IL3D
- **Format brut :** Rendus multi-vues et fichiers JSON de descriptions d'agencement.
- **Script de transformation :** `dataset_tools/preprocessing/convert_il3d.py`
  - Sélection de la vue perspective principale de chaque agencement.
  - Extraction des descriptions d'agencement en langage naturel (relations de mobilier).
  - Transformation en dialogue d'analyse spatiale : explication des choix de placement du mobilier par rapport aux axes de vue.
  - Ingestion de 1 500 exemples dans le Master Schema.

### 3.5 MMIS
- **Format brut :** 160 000 images réparties dans 40 dossiers de styles et 5 sous-dossiers de pièces.
- **Script de transformation :** `dataset_tools/preprocessing/convert_mmis.py`
  - Échantillonnage stratifié : sélection de 75 images par style (40 styles x 75 = 3 000 images).
  - Contrôle de contraste et de résolution minimale.
  - Exploitation des descriptions textuelles d'ambiance fournies dans le dataset.
  - Génération de questions de qualification esthétique : identification du style, analyse des accords de teintes et des textures de surface.
  - Ingestion de 3 000 exemples dans le Master Schema.

---

## 4. Tests Automatisés & Validation Continue

Chaque composant de ce pipeline est couvert par un test unitaire automatisé dans `tests/` :
- `test_pydantic_and_schema_validation`
- `test_deduplication_analyzer`
- `test_split_leakage_detector`
- `test_qa_validator_full`
- `test_export_qwen_vl_compatibility`

Aucun exemple n'entre dans les versions figées de production sans avoir validé **100%** de ces contrôles qualité.
