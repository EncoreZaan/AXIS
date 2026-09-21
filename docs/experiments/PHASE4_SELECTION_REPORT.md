# ARCHI-AI — Rapport de Sélection des Tâches Phase 4 (`PHASE4_SELECTION_REPORT.md`)
## Controlled Unimodal Micro-Pilot — Task Selection & Feasibility

> **Date d'émission :** 21 Septembre 2026  
> **Auteur :** Assistant Spécialiste ARCHI-AI  
> **Statut de l'Étape :** STEP 2 & 3 COMPLÉTÉS — EN ATTENTE DE VALIDATION UTILISATEUR  
> **Règle Fondamentale :** `TRAINING_ALLOWED: NO` (Aucun entraînement n'est lancé à ce stade).

---

## 1. Synthèse de la Sélection

Conformément au mandat de la **Phase 4 — Controlled Unimodal Micro-Pilot**, l'objectif n'est pas de réaliser un entraînement généraliste ni de couvrir les 69 tâches du catalogue, mais de prouver expérimentalement sur un périmètre restreint, falsifiable et reproductible :
1. Que les données canoniques sont apprenables ;
2. Que les cibles déterministes produisent un signal réel (au-delà des shortcuts) ;
3. Que la chaîne de traitement `Data → Loader → Modèle → Métriques → Gold Set V3` est rigoureuse et exempte de fuite.

Quatre (4) tâches ont été sélectionnées, réparties équitablement sur deux pistes unimodales complémentaires :
- **Piste 1 : Vision 2D / Lecture & Topologie de Plans** (`PLAN_ONLY` via `CORE_RPLAN`)
- **Piste 2 : Géométrie 3D & Raisonnement Normatif** (`3D` via `CORE_IL3D` + `CORE_NORMES_FR`)

---

## 2. Tableau Récapitulatif des Tâches Sélectionnées

| Tâche | Pourquoi retenue | Volume Supervision v1 / Master v2 | Target | Métrique | Risque & Shortcut Identifié |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`FLOORPLAN_READING`** | Perception 2D pure ; décodage de code graphique architectural ; cibles numériques déterministes issues de la segmentation. | 100 ex (v1)<br>29 278 assets (Master v2) | Décompte pièces (`rooms_count`), portes (`doors_count`), surfaces pixels habitables et murs. | MAE & Exact Match sur les comptages ; Erreur relative $\le 5\%$ sur les pixels. | Présence d'identifiants hash d'assets dans les textes bruts v1 (à expurger formellement en Ablation B). |
| **`ROOM_TOPOLOGY`** | Raisonnement spatial & partitionnement topologique 2D ; alignement direct avec le **Gold Set V3** (100 cas). | 100 ex (Gold Set V3)<br>29 278 assets (Master v2) | Nombre de pièces distinctes, surface min/max, distribution des volumes intérieurs. | Exact Match sur `room_count` ; MAE sur pixels extrêmes ; F1-score topologique de connectivité. | Les 100 cas de v1 sont intégralement dans le Gold Set V3 : interdiction absolue de les utiliser en Train/Val (quarantaine stricte). |
| **`OBJECT_RELATION`** | Géométrie 3D pure ; calcul euclidien exact sans hallucination ; base fondamentale de la spatialité 3D. | 100 ex (v1)<br>27 820 assets (Master v2) | Distance euclidienne 3D $d_E = \sqrt{\Delta x^2 + \Delta y^2 + \Delta z^2}$ et gisement relatif. | MAE, RMSE, et Taux de Succès sous tolérance stricte ($\pm 0.05$ m). | Risque de shortcut par mémorisation de distances moyennes par paire de catégories meublantes. |
| **`CLEARANCE_CHECK`** | Décision normative professionnelle binaire (Pass/Fail) basée sur standards ergonomiques officiels (Neufert/PMR) ; alignement direct avec le **Gold Set V3** (100 cas + 100 contre-exemples). | 100 ex (Gold Set V3)<br>100 contre-exemples<br>27 820 assets (Master v2) | Verdict de conformité (`compliance_verdict`: True/False), distance mesurée vs seuil réglementaire. | Accuracy binaire, F1-Score macro, F1-Score sur classe critique (non-conforme). | Déséquilibre de classe naturel si l'échantillonnage n'est pas stratifié (surreprésentation des passages conformes). |

---

## 3. Détail Approfondi des Tâches Sélectionnées

### 3.1. Tâche 1 : `FLOORPLAN_READING`
- **Domaine :** Architecture 2D / Lecture de plans d'étage.
- **Modalité d'entrée :** `PLAN_ONLY` — Image matricielle raster 256x256 px (3 canaux RGB).
- **Encodage graphique :** Fond noir = extérieur, pixels rouges = murs porteurs / cloisons, pixels verts = portes et baies, aplats blancs = pièces intérieures habitables.
- **Formulation du prompt :** Question standardisée interrogeant le nombre de pièces, de portes et les emprises de matière sans aucune mention d'échelle métrique physique inventée.
- **Target Contract :**
  ```json
  {
    "rooms_count": 6,
    "doors_count": 7,
    "habitable_pixels": 28450,
    "wall_pixels": 11200,
    "metric_scale": null
  }
  ```
- **Métrique d'évaluation :**
  - $\text{Acc}_{\text{exact}}(\text{rooms}) = \mathbb{I}(\hat{N}_{\text{rooms}} = N_{\text{rooms}})$
  - $\text{MAE}(\text{doors}) = \frac{1}{N}\sum |\hat{N}_{\text{doors}} - N_{\text{doors}}|$
  - $\text{RelErr}(\text{pixels}) = \frac{|\hat{A} - A|}{A} \le 0.05$
- **Baseline 0 Recommandée :**
  - Comptage majoritaire du corpus train (ex: mode = 5 pièces, 6 portes).
  - Surface moyenne empirique des aplats habitables.

### 3.2. Tâche 2 : `ROOM_TOPOLOGY`
- **Domaine :** Topologie spatiale & Connectivité intérieure.
- **Modalité d'entrée :** `PLAN_ONLY` — Image raster 256x256 px.
- **Formulation du prompt :** Identification de la partition topologique et calcul des tailles relatives des cellules habitables.
- **Target Contract :**
  ```json
  {
    "room_count": 6,
    "largest_room_pixels": 7678,
    "smallest_room_pixels": 874,
    "room_sizes_pixels": [7678, 2970, 2622, 2254, 920]
  }
  ```
- **Métrique d'évaluation :**
  - Exact Match sur le décompte de composants connexes habitables.
  - $\text{MAE}$ sur les pixels de la plus grande et de la plus petite pièce.
  - Vérificateur automatique : `dataset_tools/supervision/verifiers/geometry_verifier.py`.
- **Règle d'isolation stricte Gold Set V3 :**
  - Les 100 exemples actuels de Supervision v1 constituent le Gold Set V3 officiel.
  - **Interdiction formelle** de les inclure dans le set d'entraînement ou de validation du Dataset A.
  - Les exemples Train et Val du Dataset A seront extraits de projets `CORE_RPLAN` disjoints du Master Dataset v2 (Train split).
- **Baseline 0 Recommandée :**
  - Médiane des pièces observées sur le split d'entraînement.
  - Prédicteur basé sur la proportion globale de blanc divisée par la taille médiane.

### 3.3. Tâche 3 : `OBJECT_RELATION`
- **Domaine :** Géométrie 3D spatiale intérieure.
- **Modalité d'entrée :** `3D` — Coordonnées cartésiennes 3D $[x, y, z]$ des centroïdes d'objets meublants issus des scènes `CORE_IL3D`.
- **Formulation du prompt :** Requête de la distance métrique réelle et de la position relative entre l'objet A et l'objet B.
- **Target Contract :**
  ```json
  {
    "distance_m": 1.30,
    "object_a_pos": [6.80, 0.00, 5.78],
    "object_b_pos": [7.66, 0.00, 4.80],
    "room": "RecreationRoom"
  }
  ```
- **Métrique d'évaluation :**
  - $\text{MAE} = \frac{1}{N}\sum |\hat{d} - d_E|$ en mètres.
  - Tolérance de succès : $|\hat{d} - d_E| \le 0.05\text{ m}$.
  - Vérificateur automatique : `dataset_tools/supervision/verifiers/scene_graph_verifier.py`.
- **Baseline 0 Recommandée :**
  - Distance moyenne globale du jeu d'entraînement ($\approx 2.45\text{ m}$).
  - Distance moyenne par couple d'objets fréquent (ex: table-chaise).

### 3.4. Tâche 4 : `CLEARANCE_CHECK`
- **Domaine :** Ergonomie spatiale, Accessibilité & Conformité aux normes.
- **Modalité d'entrée :** `3D` + Contexte textuel normatif (`CORE_NORMES_FR` / Neufert).
- **Formulation du prompt :** Détermination de la conformité du passage utile séparant deux éléments par rapport au seuil minimal réglementaire (ex: passage PMR $\ge 0.90\text{ m}$, passage d'usage $\ge 0.80\text{ m}$).
- **Target Contract :**
  ```json
  {
    "measured_distance_m": 1.30,
    "threshold_m": 0.90,
    "compliance_verdict": true
  }
  ```
- **Métrique d'évaluation :**
  - Classification Accuracy : $\frac{TP + TN}{TP + TN + FP + FN}$.
  - F1-score binaire (accent sur la détection des non-conformités, $verdict = \text{False}$).
  - Vérificateur automatique : `dataset_tools/supervision/verifiers/ergonomics_verifier.py`.
- **Règle d'isolation stricte Gold Set V3 :**
  - 100 exemples de référence certifiés et 100 contre-exemples adversariaux (distances critiques à $\pm 0.02\text{ m}$ du seuil) composent le Gold Set V3.
  - Ces 200 cas sont sanctuarisés en **EVALUATION ONLY**.
  - Le Dataset A Train/Val générera des cas déterministes sur des scènes `CORE_IL3D` indépendantes.
- **Baseline 0 Recommandée :**
  - Prédicteur majoritaire (prédit toujours `True`).
  - Prédicteur aléatoire uniforme (50/50).

---

## 4. Tâches Écartées et Justification Complète des Rejets

Sur les 69 tâches du catalogue architectural officiel, 65 tâches ont été formellement écartées du micro-pilote pour des raisons scientifiques et réglementaires rigoureuses :

| Catégorie de Rejet | Nombre de Tâches | Tâches Concernées (Exemples Phares) | Motif Scientifique & Technique Incompressible |
| :--- | :---: | :--- | :--- |
| **`NOT_SUPPORTED` (RAW Absent)** | 18 | `SPATIAL_RELATION_ANALYSIS`, `FURNITURE_LAYOUT_ANALYSIS`, `ARTIFICIAL_LIGHTING_REASONING`, `ALTERNATIVE_DESIGN`, `OPTION_COMPARISON`, `IMAGE_PLUS_PLAN_PLUS_TEXT` | Aucune donnée source correspondante n'est présente dans le RAW corpus. Toute tentative d'apprentissage relèverait de l'affabulation ou de la génération synthétique non ancrée. |
| **Interdiction Multimodale Croisée** | 7 | `BIM_PLUS_PLAN`, `PLAN_PLUS_3D`, `IMAGE_PLUS_PLAN`, `IMAGE_PLUS_TEXT`, `MULTIMODAL_PROJECT_REASONING`, etc. | **Phase 4 = Micro-Pilote Unimodal**. Seulement 10 paires réelles 2D/3D existent dans tout le corpus. L'entraînement multimodal généraliste est explicitement interdit par la règle fondamentale 2. |
| **Quarantaine Métrique ResPlan** | 3 | `PLAN_SUMMARY`, `METRIC_SURFACE_CALCULATION`, etc. | Échec de calibration métrique de ResPlan documenté en Phase 3. Interdiction formelle d'inventer des conversions pixel $\rightarrow \text{m}^2$. |
| **Risque Juridique FloorPlanCAD** | 1 | `FLOORPLANCAD_VECTOR_READING` | Statut juridique `LEGAL_REVIEW_REQUIRED`. Strictement proscrit de tout jeu d'entraînement. |
| **Volume Insuffisant (< 5 ex en v1)** | 5 | `MATERIAL_IDENTIFICATION` (4 ex), `DESIGN_HISTORY` (4 ex), `VISUAL_LIGHTING_ANALYSIS` (3 ex), `CIRCULATION_CHECK` (1 ex), `ACCESSIBILITY_ANALYSIS` (1 ex) | Effectifs statistiquement insignifiants pour alimenter des partitions train/val/test rigoureuses. |
| **Shortcut / Fuite dans les Métadonnées** | 1 | `IFC_ENTITY_IDENTIFICATION` (85 ex) | **Audit critique :** Dans le Supervision v1 actuel, le champ `inputs["ifc_entities"][0]["top_classes"]` contient déjà le décompte exact des classes IFC recherchées ! Le modèle apprendrait un shortcut trivial de recopie JSON et non une lecture STEP du fichier BIM. |
| **Cible Subjective ou Faiblement Déterministe** | 6 | `STYLE_ANALYSIS`, `INTERIOR_ANALYSIS`, `STYLE_CLASSIFICATION`, `STYLE_COMPARISON`, `PROJECT_CRITIQUE`, etc. | Absence d'étiquettes de vérité terrain objectives dans le Master Dataset v2. Évaluation non falsifiable, risque majeur de faux pass par sycophancie. |
| **Redondance / Doublons** | 11 | `SPATIAL_LAYOUT_ANALYSIS`, `3D_TO_TEXT`, `PLAN_TO_TEXT`, `ROOM_IDENTIFICATION`, `DOOR_WINDOW_ANALYSIS`, etc. | Couvertes plus rigoureusement par les tâches sélectionnées (`ROOM_TOPOLOGY`, `FLOORPLAN_READING`, `OBJECT_RELATION`). |
| **Autres Tâches Spécialisées non prioritaires** | 13 | PBR/Shaders, Pédagogie d'atelier, Analyse programmatique non contrainte. | Hors du périmètre d'un micro-pilote minimaliste, stable et falsifiable. |

---

## 5. Spécification des Niveaux de Taille de Dataset A

Pour tester la scalabilité et l'apprentissage sans saturer la machine locale (NVIDIA RTX 4060 Ti 8 Go VRAM, Windows 11), trois niveaux d'échelle contrôlés sont définis :

```text
=============================================================================
NIVEAU                  TOTAL EXEMPLES      EXEMPLES / TÂCHE (4 tâches)     TRAIN / VAL / TEST (80% / 10% / 10%)
=============================================================================
Dataset A-Small         800                 200                             640 / 80 / 80
Dataset A-Medium        2 400               600                             1 920 / 240 / 240
Dataset A-Full          6 000               1 500                           4 800 / 600 / 600
=============================================================================
```

### Règles Incompressibles de Constitution :
1. **Unité de séparation :** Groupement strict par `project_group_id` (aucun asset d'un même plan RPLAN ou d'une même scène IL3D ne peut se retrouver à la fois dans train et validation/test).
2. **Graine scellée :** `seed = 42`.
3. **Étanchéité Gold Set V3 :**
   $$\text{Gold Set V3} \cap \text{Dataset A (Train)} = \emptyset$$
   $$\text{Gold Set V3} \cap \text{Dataset A (Val)} = \emptyset$$
   $$\text{ProjectGroup}(\text{Gold Set V3}) \cap \text{ProjectGroup}(\text{Dataset A Train}) = \emptyset$$

---

## 6. Protocole de Baselines Minimales

Avant tout entraînement de modèle, les performances seront calibrées sur les baselines suivantes :

1. **Baseline 0.1 — Random / Stochastic :**
   - Tirage aléatoire uniforme dans l'intervalle empirique des cibles d'entraînement.
2. **Baseline 0.2 — Majority / Empirical Constant :**
   - Classe majoritaire pour `CLEARANCE_CHECK` (`True`).
   - Médiane / moyenne pour les comptages et distances (`FLOORPLAN_READING`, `OBJECT_RELATION`).
3. **Baseline 1 — Modèle Heuristique Déterministe / Règle Géométrique :**
   - Heuristique basée sur la densité des pixels ou la moyenne de boîte englobante.
4. **Modèle Minimal Expérimental :**
   - Modèle léger, rapide, reproductible et inspectable (ex: MLP / Ridge / Régresseur léger pour les features géométriques 3D ; CNN minimaliste ou extracteur de traits pour les images 2D).

---

## 7. Plan d'Ablation & Audit de Shortcuts

Chaque tâche retenue fera l'objet d'un audit à 3 conditions d'ablation :
- **Ablation A (Complète) :** Entrées brutes saines sans identifiants ni chemins divulguants.
- **Ablation B (Sanitisation des Métadonnées) :** Suppression intégrale des noms de fichiers, hash d'assets, mentions de source ou métadonnées textuelles secondaires.
- **Ablation C (Perturbation / Shuffling) :** Entrées permutées ou bruitées (ex: inversion aléatoire des coordonnées pour `OBJECT_RELATION`, permutation des masques couleur pour `FLOORPLAN_READING`) afin de prouver que la performance s'effondre sans le signal spatial authentique.

---

## 8. Conclusion et Demande d'Approbation

L'inspection technique et l'audit forensic confirment que :
- Les 4 tâches sélectionnées disposent d'un gisement de dizaines de milliers d'assets dans le Master Dataset v2 (`CORE_RPLAN` et `CORE_IL3D`) ;
- Les cibles sont 100% déterministes et évaluables automatiquement ;
- L'intégrité du Gold Set V3 est garantie par une séparation stricte des projets ;
- Aucun composant à risque juridique (FloorPlanCAD) ou métrique faussé (ResPlan pixel->m²) n'est mobilisé.

**L'agent s'arrête ici conformément à la section 28.**  
La Phase 4 (construction de Dataset A, baselines, pipeline d'entraînement et overfit test) ne débutera qu'après votre validation formelle de cette proposition de sélection.
