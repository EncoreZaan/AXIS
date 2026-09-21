# ARCHI-AI — Rapport de Preprocessing & Normalisation du Corpus (`DATASET_PREPROCESSING_REPORT`)

> **Date de génération :** 21 septembre 2026  
> **Statut :** NORMALISATION DU MASTER DATASET V1 COMPLÈTE & CERTIFIÉE  
> **Pipeline reproductible :** `python -m dataset_tools.preprocessing.run --source all` (durée : 81,6s)  
> **Suite de tests :** 25 tests automatisés validés sur 25 (100% vert, 0 régression)  
> **Manifeste d'exécution :** [`dataset/processed/metadata/PREPROCESSING_MANIFEST.json`](file:///c:/Users/encor/Documents/Devs/AEON-RWKV/ARCHI_AI/dataset/processed/metadata/PREPROCESSING_MANIFEST.json)  
> **Traçabilité immuable :** [`dataset/processed/metadata/provenance.jsonl`](file:///c:/Users/encor/Documents/Devs/AEON-RWKV/ARCHI_AI/dataset/processed/metadata/provenance.jsonl) (105 441 entrées)

---

## 1. Vue d'Ensemble & Bilan Métrique Réel

La phase de preprocessing a transformé l'ensemble des sources RAW hétérogènes en représentations canoniques normalisées, prêtes pour les futurs pipelines de génération et d'outils, sans perte d'information utile.

### Chiffres Clés du Master Dataset Intermédiaire V1

| Indicateur | Mesure Réelle | Commentaire Forensic |
| :--- | :---: | :--- |
| **Nombre total d'éléments normalisés** | **105 441 items** | 100% instanciés et validés selon le Master Schema canonique |
| **Durée totale d'exécution du pipeline**| **81,6 secondes** | Traitement streaming optimisé en mémoire (< 500 Mo RAM) |
| **Stockage utilisé sur disque** | **990,12 Mo** | Couche `processed/` + partitions `master/v1/` |
| **Sources CORE traitées avec succès** | **15 sources** | 19 sous-référentiels fonctionnels |
| **Sources gelées (exclusion légale)** | **1 source** | `CORE_FLOORPLANCAD` (motif : clause NonCommercial) |
| **Taux de conservation d'information** | **100%** | Aucune géométrie, surface, cote ou métadonnée utile perdue |
| **Traçabilité de provenance** | **100%** | 105 441 lignes d'ancrage dans `provenance.jsonl` |
| **Suite de tests automatisés** | **25 / 25 PASS** | 18 tests historiques + 7 nouveaux tests d'intégration |

---

## 2. Décomposition par Modalité Architecturale

```text
RÉPARTITION FORENSIC DES MODALITÉS NORMALISÉES (TOTAL : 105 441)
├── Plans d'étage architecturaux (2D)   : 32 010 plans complets
│   ├── ResPlan vectoriels métriques   : 17 000 plans d'architecte (polygones, pièces, adjacence)
│   ├── RPLAN matriciels segmentés    : 15 000 paires (dessin de synthèse + masque sémantique)
│   └── ResBIM paires 2D               :     10 plans 2D d'architecte appariés
│
├── Scènes et agencements spatiaux (3D) : 30 410 scènes complètes
│   ├── IL3D (Indoor Layout 3D)        : 27 816 scènes avec boîtes 3D, poses et scene graphs
│   └── StructScan3D                   :  2 594 scans physiques réels (triplets RGB + Depth + Masks)
│
├── Maquettes numériques BIM / IFC      : 95 maquettes 3D complètes
│   ├── buildingSMART certifiés        :     35 modèles (IFC 2x3, IFC 4, IFC 4.3)
│   ├── IFC-Bench V2                   :     50 modèles (21 projets réels, arborescence spatiale)
│   └── ResBIM unités 3D               :     10 maquettes résidentielles
│
├── Questions / Réponses Expertes (QA) : 1 612 paires de benchmark multimodal
│   ├── IFC-Bench V2 (BIM QA)          :  1 026 questions (512 train + 514 benchmark test)
│   └── MMMU Architecture (VLM QA)     :    586 questions universitaires sanctuarisées (holdout)
│
├── Notices patrimoniales & Design      : 39 313 notices structurées (RAG)
│   ├── MoMA Architecture & Design     : 34 539 notices d'édifices, mobilier, dessins et maquettes
│   └── The Met (Arts Déco & Mobilier) :  4 774 notices filtrées de menuiserie, boiserie et mobilier
│
├── Matériaux PBR & Ambiances Lumière   : 1 959 spécifications physiques
│   ├── Poly Haven Matériaux PBR       :    862 revêtements avec cotes physiques réelles en mètres
│   ├── ambientCG                      :    100 profils complets PBR (dimensions métriques certifiées)
│   └── Poly Haven Panoramas HDRI      :    997 environnements avec température Kelvin et EV
│
├── Réglementation Française & Textes   : 12 sections consolidées (RAG)
│   ├── Arrêté PMR du 20 avril 2017    :      4 sections inaltérées (dégagements, giration Ø150)
│   ├── Arrêté ERP du 25 juin 1980     :      3 sections inaltérées (Unités de Passage, évacuation)
│   └── CCH (Surfaces & Habitabilité)  :      2 sections inaltérées (Art. R. 156-1, ouvertures 1/6)
│
├── Ergonomie & Cotes Anthropométriques : 25 règles dimensionnelles (TOOL / RAG)
│   └── Standards Neufert & Panero     :     25 règles (cotes cm d'origine + conversion SI certifiée en m)
│
└── Enquête Tendances Déco 2026         : 5 enregistrements de prospective contemporaine
```

---

## 3. Répartition par Destination Cognitive (Routage)

Conformément à la feuille de route ARCHI-AI, chaque donnée normalisée se voit affecter un rôle cognitif précis pour éviter l'erreur d'injecter aveuglément toute information dans les poids du modèle :

| Destination Cognitive | Volume d'Items | % du Total | Sources Principales | Rôle dans ARCHI-AI |
| :--- | :---: | :---: | :--- | :--- |
| **`FINETUNE`** | **45 922** | 43,55 % | IL3D (27,8k), RPLAN (15k), StructScan3D (2,6k), IFC-Bench Train (512) | Ajustement des poids VLM : intuition spatiale, agencement, perception de parois |
| **`MULTIUSE`** | **19 089** | 18,10 % | ResPlan (17k), 95 IFC, Poly Haven (862 mat. + 997 HDRIs), ambientCG (100), Ergonomie (25) | Double usage : Fine-Tuning de perception + Outils déterministes (surfaces, graphes, collisions) |
| **`RAG`** | **39 330** | 37,30 % | MoMA A&D (34,5k), The Met (4,8k), Normes FR (12), Tendances (5) | Recherche documentaire et injection de contexte : textes de lois, culture, monographies |
| **`BENCHMARK`** | **1 100** | 1,04 % | MMMU Architecture (586), IFC-Bench Test (514) | **Évaluation aveugle sanctuarisée** : strictement inaccessible lors de l'entraînement |
| **`HOLDOUT`** | **0** (359 bruts) | 0,00 % | FloorPlanCAD | Exclu de CORE V1 suite au signalement juridique NonCommercial |

---

## 4. Partitions Étanches (Splits)

| Partition | Fichier Produit | Nombre d'Items | Usage Système |
| :--- | :--- | :---: | :--- |
| **`train`** | `dataset/master/v1/splits/train.jsonl` | **93 908** | Apprentissage supervisé & bases d'indexation |
| **`validation`** | `dataset/master/v1/splits/validation.jsonl` | **10 433** | Contrôle de convergence et réglage d'hyperparamètres |
| **`benchmark_test`** | `dataset/master/v1/splits/benchmark_test.jsonl` | **1 100** | Évaluation finale aveugle certifiée sans fuite (Zero Contamination) |
| **`holdout`** | `dataset/master/v1/splits/holdout.jsonl` | **0** | Données mises en réserve |

---

## 5. Audit de Non-Contamination (Leakage Check)

Le détecteur de fuite (`SplitLeakageDetector`) a été exécuté sur les partitions produites :
- **ID Overlap Train ↔ Test :** 0 collision.
- **Image Overlap Train ↔ Test :** 0 collision.
- **Scene/Project Overlap Train ↔ Test :** 0 collision.
- **Questions Overlap Train ↔ Test :** 0 collision.
- **Statut de propreté :** **IS_CLEAN = TRUE**.

---

## 6. Traçabilité de Provenance (Provenance Chain)

Chaque entité du Master Dataset V1 est enregistrée dans `dataset/processed/metadata/provenance.jsonl` avec le schéma suivant :
```json
{
  "source_name": "CORE_RESPLAN",
  "dataset_name": "resplan",
  "raw_file": "core/resplan/extracted/ResPlan.pkl",
  "raw_element_id": "004281",
  "transformation": "ResPlanPreprocessor.vector_topology_extractor",
  "normalized_id": "NORM_RESPLAN_004281",
  "master_id": "ARCHI_MASTER_RESPLAN_004281",
  "raw_sha256": "4b68e...",
  "timestamp": "2026-09-21T13:52:45Z"
}
```
**Résultat : 100% des 105 441 éléments peuvent être tracés jusqu'à leur octet d'origine dans le répertoire RAW.**

---

## 7. Respect des Règles Absolues

1. **Aucun RAW modifié ni supprimé :** Vérification SHA-256 et timestamps confirmée.
2. **Aucune dimension inventée :**
   - ResPlan : échelle conservée à `null`.
   - RPLAN : pas d'échelle métrique extrapolée.
   - Textes : aucune règle ajoutée aux arrêtés officiels.
3. **Unités originales conservées :**
   - Ergonomie : cotes en `cm` conservées, conversion en mètres ajoutée sous le champ `normalized_si_value`.
4. **FloorPlanCAD sanctuarisé :** 0 élément dans CORE V1.
5. **Micro-dataset historique v0.1 préservé :** Les 25 exemples d'origine (`train.jsonl` et `validation.jsonl`) demeurent intacts et valident la totalité de la suite de tests historique.
