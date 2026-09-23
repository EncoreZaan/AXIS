# AXIS Phase 6A — Journal Complet d'Ingénierie & Reproduction (`WALKTHROUGH.md`)

> **Phase Identifier:** AXIS PHASE 6A — Spatial Supervision Engineering & Training Gate  
> **Date:** 2026-09-23  
> **Auteur:** Agent d'Ingénierie Dataset & de Préparation Scientifique AXIS  
> **Statut Invariant:** `TRAINING_ALLOWED: NO` | `TRAINING_EXECUTED: NO`  
> **Répertoire d'Artefacts:** `RUN-021-SPATIAL-SUPERVISION/`

---

## 1. Contexte & Problématique Scientifique

Lors des Phases 4 et 5 (`RUN-019` et `RUN-020`), l'évaluation de généralisation a révélé que le modèle fine-tuné sur `REAL_DATA_PILOT` n'utilisait pratiquement pas l'information visuelle :
- **Similarité avec image noire :** 92.0 % (vs 4.3 % pour le modèle de base).
- **Similarité en mode Text-Only :** 95.7 %.
- **Adhérence au template :** 80.2 % de réponses calquées sur la critique canonique en 5 rubriques.
- **Hallucination d'identifiants :** 100 % d'identifiants inventés.

La Phase 6A a reçu le mandat exclusif de refondre intégralement la supervision pour contraindre le conditionnement visuel et spatial, sous la règle absolue : **AUCUN ENTRAÎNEMENT**.

---

## 2. Déroulement Chronologique & Décisions Techniques

### Étape 1 : Audit Forensique des Données Physiques Disponibles
- **Sources inspectées :**
  - `CORE_RPLAN` (`metindeder/rplan-floorplan-edited`, archive `rplan_dataset.zip` de 23,5 Mo).
  - `CORE_RESBIM_PAIRED` (`tsesterh/ResBIM-IFC`, 10 unités 2D JPEG + 3D OpenBIM IFC).
  - Documents de référence : `configs/training_corpus_cleared.json`, `docs/datasets/DATASET_RAW_FORENSIC_AUDIT.md`, `experiments/runpod_2026-09-22/REAL_DATA_PILOT/manifest.jsonl`.
- **Découvertes critiques :**
  1. Dans `metindeder/rplan-floorplan-edited`, les métadonnées textuelles amont sont composées d'une unique phrase de conditionnement ControlNet répétée 15 000 fois. **Aucun nom sémantique de pièce (salon, chambre, cuisine) n'est disponible.**
  2. C'est cette absence de pièces textuelles qui avait forcé l'ancien script `floorplan_gen.py` (ligne 40) à utiliser un fallback textuel statique pour 100 % des plans RPLAN.
  3. L'inspection des maquettes OpenBIM de ResBIM via `ifcopenshell` a révélé : **0 entité `IfcSpace`**, mais la présence exacte d'`IfcWall` (12-18), `IfcDoor` (5-6) et `IfcWindow` (4) avec cotes millimétriques réelles.
  4. L'absence de calibration affine métrique entre les rasters 2D et les mètres physiques interdit formellement d'inventer des cotes métriques sur RPLAN ou sur les dessins 2D de ResBIM.
- **Artefact produit :** [`DATA_CAPABILITY_AUDIT.md`](file:///c:/Users/teoba/Documents/Devs/AXIS/RUN-021-SPATIAL-SUPERVISION/DATA_CAPABILITY_AUDIT.md).

### Étape 2 : Spécification Formelle des Relations Spatiales
- **Décision d'ancrage :** Remplacer les noms textuels de pièces par un ancrage par boîtes englobantes $[ymin, xmin, ymax, xmax]$, centroïdes $(cx, cy)$, surfaces et positions extrémales.
- **Définitions mathématiques strictes sans seuil arbitraire :**
  - `LEFT_OF` / `RIGHT_OF` : Dominance horizontale ($|\Delta x| > |\Delta y|$) et écart normalisé $\Delta x \ge 0.4 \times \bar{w}$.
  - `ABOVE` / `BELOW` : Dominance verticale ($|\Delta y| > |\Delta x|$) et écart normalisé $\Delta y \ge 0.4 \times \bar{h}$.
  - `CONNECTED_TO` : Intersection de la dilatation morphologique $r=2$ px d'une porte verte avec les deux pièces blanches mitoyennes.
  - `NOT_CONNECTED_TO` : Exemple négatif contrastif rigoureusement certifié (absence de porte entre les pièces).
  - `ADJACENT_TO` : Partage d'une cloison rouge mitoyenne (dilatation $r=3$ px).
  - `LARGEST_ROOM` / `SMALLEST_ROOM` : Extrema d'aire en pixels.
  - `SHORTEST_PATH_LENGTH` : Plus court chemin en nombre de portes via l'algorithme BFS sur le graphe de pièces $G_P$.
  - `CIRCULATION_HUB` : Nœud de degré maximal dans $G_P$.
- **Artefact produit :** [`SPATIAL_RELATION_DEFINITIONS.md`](file:///c:/Users/teoba/Documents/Devs/AXIS/RUN-021-SPATIAL-SUPERVISION/SPATIAL_RELATION_DEFINITIONS.md).

### Étape 3 : Implémentation du Générateur de Supervision Spatiale
- **Script créé :** [`dataset_tools/supervision/spatial_supervision_builder.py`](file:///c:/Users/teoba/Documents/Devs/AXIS/dataset_tools/supervision/spatial_supervision_builder.py).
- **Extraction physique :**
  - Extraction et copie des 1 000 images d'origine (990 RPLAN PNG 256x256, 10 ResBIM JPEG 7572x4189) vers `RUN-021-SPATIAL-SUPERVISION/dataset/images/`.
  - Vérification cryptographique : 100 % des empreintes SHA-256 correspondent au manifeste canonique certifié en Phase 3.
- **Génération supervisée :**
  - 7 950 exemples supervisés générés au format conversationnel Qwen2-VL.
  - Réponses courtes et ciblées (moyenne : 12.3 mots), éradiquant tout template verbeux.
  - Découpage étanche préservé (Seed 42) :
    - Train : 6 160 exemples (77.5 %)
    - Validation : 784 exemples (9.9 %)
    - Test : 1 006 exemples (12.7 %)

### Étape 4 : Audits d'Étanchéité et de Qualité
- **Audit de Fuite (`LEAKAGE_REPORT.md`) :**
  - Intersections d'identifiants d'exemples : Train $\cap$ Val = 0, Train $\cap$ Test = 0, Val $\cap$ Test = 0.
  - Intersections d'assets : 0.
  - Intersections de hash SHA-256 d'images : 0.
  - Chevauchement Gold Set V3 : 0.
  - Contamination FloorPlanCAD : 0.
- **Audit de Qualité (`DATA_QUALITY_REPORT.md`) :**
  - Schéma JSON valide : 7 950 / 7 950 (100.0 %).
  - Images lisibles par PIL : 1 000 / 1 000 (100.0 %).
  - Questions et réponses non-vides : 100.0 %.
  - Dépendance visuelle `VISUAL_REQUIRED` : 100.0 %.
- **Audit Manuel Déterministe (`MANUAL_AUDIT.md`) :**
  - 50 exemples échantillonnés (Graine = 42).
  - Inspection visuelle et géométrique individuelle : 50/50 validés (100 % PASS).

### Étape 5 : Scellement Cryptographique du Jeu de Données
- Calcul des empreintes SHA-256 de tous les fichiers critiques du répertoire `RUN-021-SPATIAL-SUPERVISION/`.
- Fichiers scellés : `manifest.jsonl`, `dataset_manifest.jsonl`, `train.jsonl`, `validation.jsonl`, `test.jsonl`, `dataset_config.json`, rapports markdown.
- Artefacts produits : [`hashes.json`](file:///c:/Users/teoba/Documents/Devs/AXIS/RUN-021-SPATIAL-SUPERVISION/hashes.json) et [`DATASET_LOCK.md`](file:///c:/Users/teoba/Documents/Devs/AXIS/RUN-021-SPATIAL-SUPERVISION/DATASET_LOCK.md).

### Étape 6 : Configuration Candidate & Validation par Dry Run
- **Configuration candidate :**
  - Création de [`training_config_proposal.yaml`](file:///c:/Users/teoba/Documents/Devs/AXIS/RUN-021-SPATIAL-SUPERVISION/training_config_proposal.yaml).
  - Mention explicite : `STATUS: PROPOSAL`, `TRAINING_ALLOWED: NO`.
- **Dry Run de Collation et Passage Avant :**
  - Script créé : [`scripts/dry_run_spatial.py`](file:///c:/Users/teoba/Documents/Devs/AXIS/scripts/dry_run_spatial.py).
  - 8 pas de passage avant exécutés avec un batch size de 2 sur `train.jsonl`.
  - Invariant vérifié : `optimizer.step()` strictement désactivé.
  - Invariance des poids : Empreinte SHA-256 avant et après run = `69d0872fa01b1144596e80a3c61ad3fea7f976d80f698dec553440c92a73018f` (Strictement identique).
  - Artefacts produits : [`dry_run_metrics.json`](file:///c:/Users/teoba/Documents/Devs/AXIS/RUN-021-SPATIAL-SUPERVISION/dry_run_metrics.json) et [`DRY_RUN_REPORT.md`](file:///c:/Users/teoba/Documents/Devs/AXIS/RUN-021-SPATIAL-SUPERVISION/DRY_RUN_REPORT.md).

### Étape 7 : Rapport Scientifique et Porte Finale
- **Rapport Scientifique :** [`SCIENTIFIC_DESIGN_REPORT.md`](file:///c:/Users/teoba/Documents/Devs/AXIS/RUN-021-SPATIAL-SUPERVISION/SCIENTIFIC_DESIGN_REPORT.md) apportant des réponses complètes aux 12 questions formelles du protocole.
- **Porte Finale :** [`FINAL_GATE.md`](file:///c:/Users/teoba/Documents/Devs/AXIS/RUN-021-SPATIAL-SUPERVISION/FINAL_GATE.md) attestant de l'état `COMPLETE` et de `TRAINING_ALLOWED: NO`.

---

## 3. Inventaire des Fichiers et Empreintes SHA-256

| Fichier | Emplacement | Statut |
| :--- | :--- | :---: |
| `DATA_CAPABILITY_AUDIT.md` | `RUN-021-SPATIAL-SUPERVISION/DATA_CAPABILITY_AUDIT.md` | SCELLÉ |
| `SPATIAL_RELATION_DEFINITIONS.md` | `RUN-021-SPATIAL-SUPERVISION/SPATIAL_RELATION_DEFINITIONS.md` | SCELLÉ |
| `SPLIT_REPORT.md` | `RUN-021-SPATIAL-SUPERVISION/SPLIT_REPORT.md` | SCELLÉ |
| `LEAKAGE_REPORT.md` | `RUN-021-SPATIAL-SUPERVISION/LEAKAGE_REPORT.md` | SCELLÉ |
| `DATA_QUALITY_REPORT.md` | `RUN-021-SPATIAL-SUPERVISION/DATA_QUALITY_REPORT.md` | SCELLÉ |
| `MANUAL_AUDIT.md` | `RUN-021-SPATIAL-SUPERVISION/MANUAL_AUDIT.md` | SCELLÉ |
| `DATASET_LOCK.md` | `RUN-021-SPATIAL-SUPERVISION/DATASET_LOCK.md` | SCELLÉ |
| `manifest.jsonl` | `RUN-021-SPATIAL-SUPERVISION/manifest.jsonl` | SCELLÉ |
| `dataset_manifest.jsonl` | `RUN-021-SPATIAL-SUPERVISION/dataset_manifest.jsonl` | SCELLÉ |
| `train.jsonl` | `RUN-021-SPATIAL-SUPERVISION/train.jsonl` | SCELLÉ |
| `validation.jsonl` | `RUN-021-SPATIAL-SUPERVISION/validation.jsonl` | SCELLÉ |
| `test.jsonl` | `RUN-021-SPATIAL-SUPERVISION/test.jsonl` | SCELLÉ |
| `dataset_config.json` | `RUN-021-SPATIAL-SUPERVISION/dataset_config.json` | SCELLÉ |
| `hashes.json` | `RUN-021-SPATIAL-SUPERVISION/hashes.json` | SCELLÉ |
| `training_config_proposal.yaml` | `RUN-021-SPATIAL-SUPERVISION/training_config_proposal.yaml` | SCELLÉ |
| `dry_run_metrics.json` | `RUN-021-SPATIAL-SUPERVISION/dry_run_metrics.json` | SCELLÉ |
| `DRY_RUN_REPORT.md` | `RUN-021-SPATIAL-SUPERVISION/DRY_RUN_REPORT.md` | SCELLÉ |
| `FINAL_GATE.md` | `RUN-021-SPATIAL-SUPERVISION/FINAL_GATE.md` | SCELLÉ |
| `SCIENTIFIC_DESIGN_REPORT.md` | `RUN-021-SPATIAL-SUPERVISION/SCIENTIFIC_DESIGN_REPORT.md` | SCELLÉ |
| `WALKTHROUGH.md` | `RUN-021-SPATIAL-SUPERVISION/WALKTHROUGH.md` | SCELLÉ |

---

## 4. Instructions de Reproduction Intégrale

Pour reproduire l'intégralité de la Phase 6A sur une machine neuve :
```bash
# 1. Vérifier l'environnement Python
python --version  # Python >= 3.10

# 2. Exécuter le générateur de supervision spatiale
python dataset_tools/supervision/spatial_supervision_builder.py

# 3. Exécuter le dry-run sans mise à jour de poids
python scripts/dry_run_spatial.py

# 4. Vérifier l'intégrité des hashes SHA-256
python -c "import json, hashlib; [print(f, hashlib.sha256(open('RUN-021-SPATIAL-SUPERVISION/'+f,'rb').read()).hexdigest()) for f in json.load(open('RUN-021-SPATIAL-SUPERVISION/hashes.json'))]"
```
