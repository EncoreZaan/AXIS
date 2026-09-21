# ARCHI-AI — Proposition d'Architecture Dataset V1

Ce document formalise la proposition stratégique d'architecture pour la version **V1** du dataset d'entraînement et d'évaluation d'**ARCHI-AI**.

---

## 1. Principes Fondateurs de la Stratégie V1

Une erreur classique en vision-langage consiste à accumuler des téraoctets de données hétérogènes ("tout télécharger en masse"), provoquant :
- Une saturation immédiate du stockage et des dépassements de coûts GPU ;
- Une dilution de l'expertise métier dans du bruit visuel non labellisé ;
- Des risques juridiques fatals pour la pérennité du projet ;
- Une contamination des bancs de test par fuite d'apprentissage (*data leakage*).

La stratégie d'ARCHI-AI V1 repose au contraire sur une **sélection chirurgicale**, **hautement équilibrée**, **légalement sécurisée** et **nativement compatible avec notre Master Schema Pydantic**.

---

## 2. Structure Cible du Dataset ARCHI-AI V1

Le dataset V1 est structuré en **7 blocs modulaires** totalisant un volume cible de **12 500 exemples supervisés d'excellence** :

```text
ARCHI-AI Dataset V1 (12 500 exemples)
│
├── 1. CORE VISUAL (1 500 ex.)
│   ├── Enveloppe bâtie réelle (murs, ouvertures, sols) [StructScan3D]
│   └── Perspectives d'espaces réalistes [Structured3D sous-échantillonné]
│
├── 2. CORE INTERIOR DESIGN & STYLE (3 000 ex.)
│   ├── Reconnaissance de 40 styles d'intérieurs [MMIS]
│   ├── Matériaux, finitions et textures [MMIS]
│   └── Harmonie colorimétrique et mobilier [MMIS]
│
├── 3. CORE FLOORPLAN (3 000 ex.)
│   ├── Plans résidentiels unitaires vectoriels + graphes [ResPlan]
│   ├── Plans de logements collectifs et circulations [MSD]
│   └── Plans réels complexes et bruits d'agences [CubiCasa5K filtré]
│
├── 4. CORE SPATIAL REASONING (2 500 ex.)
│   ├── Relations spatiales 3D en langage naturel [IL3D]
│   ├── Agencements hiérarchiques de mobilier [M3DLayout]
│   └── Comparaisons pièce vide vs pièce meublée [Structured3D]
│
├── 5. SPECIALIZED SKILLS (1 000 ex.)
│   ├── Ergonomie dimensionnelle et gabarits [HSSD / CHOrD synthétisé]
│   ├── Critique de défauts d'agencement et diagnostic [ARCHI-AI Expert Curated]
│   └── Pédagogie et recommandations spatiales [ARCHI-AI Expert Curated]
│
├── 6. INDEPENDENT BENCHMARK (1 000 ex. - STRICTEMENT ISOLÉ)
│   ├── Test lecture de plans aveugles [ResPlan Holdout + CubiCasa5K Holdout]
│   ├── Test cohérence multi-vues et lumière [SpatialGen-Bench]
│   └── Test identification d'enveloppe et matériaux [StructScan3D Holdout]
│
└── 7. RAG KNOWLEDGE CORPUS (Ressource Textuelle Hors-Poids ML)
    ├── Normes IFC et réglementation constructive [BIM/IFC QA]
    ├── Corpus d'analyses textuelles de plans [BRIDGE]
    └── Données de tendances datées [Trends 2026 Survey]
```

---

## 3. Détail des Blocs & Sources Retenues

### Bloc 1 : Core Visual — Perception de l'Enveloppe Bâtie (1 500 exemples)
- **Objectif :** Apprendre au modèle à discerner immédiatement l'enveloppe architecturale (murs porteurs, cloisons, sols, plafonds, portes, fenêtres) sans la confondre avec le mobilier.
- **Sources :**
  - `StructScan3D` : 500 images réelles RGB-D de haute qualité (CC BY 4.0).
  - `Structured3D` : 1 000 perspectives photoréalistes de scènes vides (*unfurnished*) et semi-meublées.
- **Learning Type dominant :** `LearningType.OBSERVATION`, `LearningType.ANALYSIS`.
- **Compétences clés :** `Skill.VISION`, `Skill.ESPACE`.

### Bloc 2 : Core Interior Design — Styles, Couleurs & Matières (3 000 exemples)
- **Objectif :** Établir une maîtrise impeccable des styles décoratifs, des palettes de matériaux (chêne massif, travertin, laiton brossé, béton ciré) et de l'éclairage.
- **Sources :**
  - `MMIS` : 3 000 photographies sélectionnées couvrant de manière strictement équilibrée les 40 styles majeurs sur les 5 typologies de pièces (salon, cuisine, chambre, bain, repas).
- **Learning Type dominant :** `LearningType.ANALYSIS`, `LearningType.COMPARISON`.
- **Compétences clés :** `Skill.STYLE`, `Skill.MATERIAUX`, `Skill.COULEUR`, `Skill.LUMIERE`.

### Bloc 3 : Core Floorplan — Lecture & Compréhension de Plans (3 000 exemples)
- **Objectif :** Transformer Qwen2-VL en un lecteur de plans chevronné, capable d'identifier les pièces, les liaisons, les portes, les orientations et les surfaces.
- **Sources :**
  - `ResPlan` : 1 800 plans vectoriels avec questions/réponses alignées sur le graphe de connectivité (CC BY 4.0).
  - `Modified Swiss Dwellings (MSD)` : 800 plans d'immeubles collectifs suisses (CC BY 4.0).
  - `CubiCasa5K` : 400 plans scannés réels avec cotations et graphismes d'agences.
- **Learning Type dominant :** `LearningType.ANALYSIS`, `LearningType.CONSTRAINT_REASONING`.
- **Compétences clés :** `Skill.PLANS_2D`, `Skill.CIRCULATION`, `Skill.ESPACE`.

### Bloc 4 : Core Spatial Reasoning — Agencement & Volumes 3D (2 500 exemples)
- **Objectif :** Développer la capacité à raisonner en trois dimensions sur la disposition du mobilier par rapport aux baies, aux circulations et aux points focaux.
- **Sources :**
  - `IL3D` : 1 500 paires multi-vues + dialogues d'agencement en langage naturel (Apache-2.0).
  - `M3DLayout` : 600 descriptions hiérarchiques de relations spatiales (CC BY-NC 4.0).
  - `Structured3D` : 400 paires comparatives pièce vide vs pièce meublée sous le même angle de vue.
- **Learning Type dominant :** `LearningType.REASONING`, `LearningType.ANALYSIS`.
- **Compétences clés :** `Skill.ESPACE`, `Skill.MOBILIER`, `Skill.CIRCULATION`.

### Bloc 5 : Specialized Skills — Ergonomie, Critique & Pédagogie (1 000 exemples)
- **Objectif :** La signature distinctive d'ARCHI-AI. Sortir de la simple description passive pour poser un diagnostic critique d'expert (identifier les erreurs d'ergonomie, les vis-à-vis gênants, les passages trop étroits, et formuler des recommandations d'amélioration).
- **Sources :**
  - `HSSD` / `CHOrD` : 300 exemples illustrant des gabarits stricts et des règles de non-collision.
  - `ARCHI-AI Curated & Synthetic Augmentation` : 700 exemples hautement supervisés formulés par des architectes (incluant contre-exemples et corrections).
- **Learning Type dominant :** `LearningType.CRITIQUE`, `LearningType.ERROR_DETECTION`, `LearningType.IMPROVEMENT`, `LearningType.PEDAGOGY`.
- **Compétences clés :** `Skill.CRITIQUE`, `Skill.RECOMMANDATION`, `Skill.PEDAGOGIE`, `Skill.ERGONOMIE`.

### Bloc 6 : Benchmark Indépendant (1 000 exemples — Strictly Holdout)
- **Objectif :** Banc de test unifié et inviolable.
- **Sources :**
  - 300 plans de `ResPlan` (split test non vu).
  - 200 plans réels de `CubiCasa5K` (split test non vu).
  - 300 scènes de `SpatialGen-Bench` (évaluation multi-vues / lumière).
  - 200 images de `StructScan3D` (évaluation enveloppe bâtie).
- **Règle :** Zéro présence dans le split `train`.

### Bloc 7 : RAG Knowledge Corpus (Système Documentaire)
- **Objectif :** Fournir des connaissances factuelles exactes au moment de l'inférence sans alourdir le modèle.
- **Sources :**
  - `BIM/IFC QA` : 13 485 paires de questions techniques sur la maquette numérique et les normes.
  - Extraits textuels de `BRIDGE` : descriptions de typologies spatiales.
  - Synthèse `Interior Design Trends 2026` : contexte d'opinion daté.

---

## 4. Équilibre des Compétences & Distribution des Splits

### Répartition par Split
- **Train Split (80%) :** 9 200 exemples
- **Validation Split (10%) :** 1 150 exemples
- **Internal Test Split (10%) :** 1 150 exemples
- **Independent Holdout Benchmark :** 1 000 exemples (évalués séparément)

### Répartition Cible des Compétences (Skills)
- `VISION` : ~35%
- `ESPACE` : ~45%
- `PLANS_2D` : ~25%
- `CIRCULATION` : ~25%
- `ERGONOMIE` : ~20%
- `STYLE` : ~25%
- `MATERIAUX` : ~20%
- `LUMIERE` : ~18%
- `COULEUR` : ~18%
- `MOBILIER` : ~25%
- `CRITIQUE` : ~15%
- `RECOMMANDATION` : ~15%
- `PEDAGOGIE` : ~12%

*(Note : Un exemple mobilisant généralement 2 à 4 compétences simultanément, la somme des pourcentages dépasse 100%).*

---

## 5. Faisabilité Technique & Budgétaire sur RTX 3090 / RunPod

| Paramètre | Estimation V1 (12 500 exemples) |
| :--- | :--- |
| **Poids des images stockées (sélectionnées)** | **~35 à 45 GB** (compatible avec le disque local NVMe) |
| **Tokens texte estimés** | ~6,5 millions de tokens (prompt + réponse experte) |
| **Temps d'entraînement QLoRA (RTX 3090 24 GB)** | ~8 à 12 heures pour 3 époques (LoRA rank 16 / alpha 32) |
| **Coût estimé RunPod (si GPU loué ultérieurement)** | **< 15 $** (1 machine RTX 4090 ou A5000 pendant une nuit) |

Cette architecture confère à ARCHI-AI une assise d'expertise incomparable, tout en restant parfaitement agile, légère et totalement maîtrisée.
