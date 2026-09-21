# ARCHI-AI — Cartographie de Couverture des Données

Ce document détaille la projection exhaustive entre les **compétences requises**, les **sources primaires identifiées**, les **datasets associés**, le **type de supervision technique** et la **destination système** au sein de l'architecture ARCHI-AI.

---

## 1. Vue d'Ensemble de la Chaîne d'Affectation

Chaque bloc de données est tracé selon la chaîne formelle :

$$\text{Compétence Métier} \longrightarrow \text{Sources Primaires} \longrightarrow \text{Datasets / Corpus} \longrightarrow \text{Format de Supervision} \longrightarrow \text{Destination Système}$$

Les destinations système sont définies par :
- **`FINE-TUNE`** : Injection directe dans les poids du modèle multimodal (LoRA / QLoRA).
- **`RAG`** : Indexation documentaire pour interrogation et citation contextuelle en cours d'inférence.
- **`TOOL`** : Algorithme ou moteur de calcul déterministe (parseurs géométriques, graphes, tables).
- **`BENCHMARK`** : Évaluation aveugle isolée (Zéro fuite dans le Fine-Tuning).
- **`HYBRIDE`** : Combinaison de plusieurs composantes (ex. VLM pour l'interprétation visuelle + RAG pour la norme).

---

## 2. Tableau de Correspondance par Compétence et Domaine

| # | Compétence Métier | Sources Primaires | Datasets Retenus | Type de Supervision | Destination |
|---|---|---|---|---|---|
| **01** | **Architecture Intérieure** (Espaces, pièces, aménagement) | Kujiale, Alibaba, Stanford, CVPR/ECCV | `Structured3D`, `IL3D`, `M3DLayout`, `InteriorGS` | Paires Image ↔ Description d'aménagement, Relations spatiales de pièces | `FINE-TUNE` (Weights) |
| **02** | **Plans 2D : Parois & Baies** (Murs, cloisons, portes, fenêtres) | CubiCasa, ResPlan, MSD, EPFL | `CubiCasa5K`, `ResPlan`, `Modified Swiss Dwellings` | Masques sémantiques, polylignes SVG, boucles de cloisons | `FINE-TUNE` + `TOOL` |
| **03** | **Plans 2D : Topologie & Flux** (Graphes de connectivité, circulations) | ResPlan, RPLAN, Space Syntax | `ResPlan-Graph`, `RPLAN` | Graphes de connectivité de pièces, matrices d'adjacence | `FINE-TUNE` + `TOOL` |
| **04** | **Plans 2D : CAD & Cotations** (Symboles architecturaux, cotes) | ArchiCAD, AutoCAD, Kaggle | `FloorPlanCAD`, `ArchCAD-400K` | Panoptic symbol spotting, détection de blocs vectoriels | `FINE-TUNE` + `TOOL` |
| **05** | **BIM / IFC : Éléments Bâtis** (Murs porteurs, dalles, cloisons) | buildingSMART, RWTH Aachen | `IFC-Bench`, `IFCNet`, `ResBIM` | Graphes d'entités STEP/IFC (IfcWall, IfcDoor, IfcWindow) | `RAG` + `TOOL` + `FINE-TUNE` |
| **06** | **BIM / IFC : Raisonnement** (Interrogation de maquette numérique) | IFC-Bench, ResBIM | `IFC-Bench (Q/A)` | Paires Question technique ↔ Propriété IFC extraite | `FINE-TUNE` + `RAG` |
| **07** | **Matériaux : Perception** (Textures, finitions, aspect de surface) | Hugging Face, ambientCG, Cornell | `MatSynth`, `ambientCG`, `MINC`, `OpenSurfaces` | Patch image ↔ Classification minéral/bois/métal/tissu/verre | `FINE-TUNE` |
| **08** | **Matériaux : Technique & PBR** (Propriétés physiques, calepinage, DTU) | MatSynth, CSTB, DTU | `MatSynth (Metadata)`, `DTU 52.1 / 51.11` | Fiches techniques (albédo, rugosité, résistance, pose) | `RAG` |
| **09** | **Lumière : Perception Visuelle** (Ombres, baies, contrastes) | OpenRooms, Laval University | `Laval Photometric Indoor HDR`, `OpenRooms` | Panoramas HDR, masques d'exposition, sources naturelles/artificielles | `FINE-TUNE` |
| **10** | **Lumière : Photométrie & Confort** (Niveaux d'éclairement, lux, FLJ) | CSTB, RE2020, AFNOR | `Laval Photometric Groundtruth`, `RE2020 Factsheets` | Calculs de facteur lumière jour (FLJ) et seuils lux requis | `TOOL` + `RAG` |
| **11** | **Ergonomie : Cotes & Gabarits** (Hauteurs de plan, passages, assises) | Neufert, Panero & Zelnik | `Anthropometric Data Extracts`, `CHOrD` | Gabarits d'encombrement 3D, règles de dégagement minimal | `TOOL` + `FINE-TUNE` |
| **12** | **Ergonomie : PMR & Accessibilité** (Aires de rotation, largeurs de portes) | Légifrance, Cerema, Arrêté 2015 | `Réglementation PMR consolidée`, `A11YBench` | Règles déterministes (Ø 150 cm, porte 90 cm, pente 5%) | `RAG` + `TOOL` |
| **13** | **Mobilier : Typologies & Volumes** (Modèles 3D, boîtes d'encombrement) | ShapeNet, 3D-FUTURE, Amazon | `3D-FUTURE`, `ABO`, `PartNet` | Bounding boxes 3D, métadonnées dimensionnelles standard | `FINE-TUNE` + `RAG` |
| **14** | **Histoire de l'Architecture** (Mouvements, ordres, typologies) | The Met, Archnet, RIBA | `Met Open Access`, `Archnet Corpus`, `WikiArt Architecture` | Notions stylistiques, chronologie, œuvres et édifices emblématiques | `RAG` + `FINE-TUNE` |
| **15** | **Histoire du Design** (Mobilier culte, écoles, créateurs) | Cooper Hewitt, Vitra Museum, MoMA | `Cooper Hewitt Open Collection`, `Design History Monographies` | Fiches œuvres, filiations stylistiques (Bauhaus, Memphis, etc.) | `RAG` + `FINE-TUNE` |
| **16** | **Styles Décoratifs & Ambiance** (Identification et discrimination de styles) | MMIS, iDesigner, Houzz | `MMIS`, `iDesigner`, `Kaggle Interior Design` | 40 taxonomies de styles annotées par pièce | `FINE-TUNE` |
| **17** | **Critique de Projet : Diagnostic** (Repérage de faiblesses, dysfonctionnements) | Écoles d'architecture, jurys | `ARCHI-AI Expert Curated`, `Synthetic Counterexamples` | Image / Plan ↔ Diagnostic critique structuré et justifié | `FINE-TUNE` |
| **18** | **Critique de Projet : Recommandation** (Arbitrages et solutions alternatives) | Écoles d'architecture, jurys | `ARCHI-AI Expert Curated`, `IL3D Improvement Prompts` | Paires Problème spatial ↔ Proposition d'aménagement optimisée | `FINE-TUNE` |
| **19** | **Pédagogie & Tutorat** (Explication didactique, maïeutique) | Architecture Education Repositories | `ARCHI-AI Socratic Dialogues`, `Design Studio QA` | Dialogues d'explication pas-à-pas avec questions guidées | `FINE-TUNE` |
| **20** | **Construction & Technique** (Cloisonnement, faux-plafonds, fluides) | CSTB, DTU, Fabricants | `DTU 25.41 (Plâtre)`, `Guides Techniques Second Œuvre` | Détails de jonctions, épaisseurs de cloisons, gaines techniques | `RAG` |
| **21** | **Normes & Réglementation ERP** (Issues de secours, dégagements, escaliers) | Légifrance, Ministère Intérieur | `Règlement Sécurité ERP consolidé` | Articles CO, GN, PE (unités de passage, largeurs minimales) | `RAG` + `TOOL` |
| **22** | **Physique du Bâtiment** (Acoustique, thermique, ventilation) | ADEME, Cerema, RE2020 | `Guides Acoustique Qualitel`, `RE2020 Bâtiment` | Performances isolantes d'éléments, affaiblissement acoustique (Rw) | `RAG` |
| **23** | **Représentation Graphique** (Coupes, axonométries, croquis) | ETH Zurich, Harvard GSD | `Drawing Matter Collection`, `BRIDGE CAD/Sketches` | Détection de types de projection et correspondances volumétriques | `FINE-TUNE` |
| **24** | **Multimodalité Croisée** (Cohérence Plan ↔ 3D ↔ Moodboard) | Structured3D, ResBIM, IL3D | `Structured3D (Plan+Rendu)`, `ResBIM Paired` | Analyse croisée multi-images : détection des incohérences plan/vue | `FINE-TUNE` |
| **25** | **Données de Projets Réels** (Dossiers complets et notices architecturales) | DataDrivenAEC, Concours publics | `DataDrivenAEC Open Projects`, `Mies Crown Hall Archive` | Notices de projet, contraintes de programme et livrables finaux | `RAG` + `BENCHMARK` |
| **26** | **Banc de Test Indépendant** (Évaluation aveugle de performance) | Holdouts stricts | `ResPlan Test`, `CubiCasa5K Test`, `SpatialGen-Bench`, `StructScan3D Test` | Questions fermées et ouvertes sur scènes jamais vues | `BENCHMARK` |

---

## 3. Matrice de Distribution par Destination Système

```text
TOTAL DES SOURCES & CORPUS
├── FINE-TUNING DES POIDS (VLM) : ~60% de l'effort multimodal
│   ├── Structured3D (Sous-échantillonné haute qualité)
│   ├── IL3D (Relations spatiales en langage naturel)
│   ├── M3DLayout (Hiérarchie spatiale)
│   ├── StructScan3D (Enveloppe bâtie réelle)
│   ├── MMIS (40 styles d'intérieurs)
│   ├── ResPlan & Modified Swiss Dwellings (Plans 2D vectoriels)
│   ├── FloorPlanCAD & ArchCAD-400K (Symboles et blocs techniques)
│   ├── MatSynth & ambientCG (Reconnaissance de matières)
│   └── ARCHI-AI Expert Curated (Critique, diagnostic, pédagogie studio)
│
├── RAG DOCUMENTAIRE DYNAMIQUE : ~25% de la couverture de connaissances
│   ├── Textes officiels (CCH, Arrêtés PMR 2015/2017, Règlement ERP)
│   ├── Recueils des DTU (25.41 cloisons, 52.1 carrelage, 51 parquets)
│   ├── Données encyclopédiques (Histoire de l'architecture & du design)
│   ├── Fiches techniques PBR & matériaux fabricants
│   ├── IFC-Bench (Base de connaissances d'entités IFC)
│   └── Corpus de notices de projets d'architecture réels
│
├── OUTILS DÉTERMINISTES (ENGINES & TOOLS) : ~10% de la fiabilité d'analyse
│   ├── Parseur géométrique SVG / DXF (Calcul automatique de surfaces)
│   ├── Analyseur de graphes de circulation (Algorithme A* et dégagements)
│   ├── Vérificateur déterministe de gabarits PMR (Cercle de 150 cm, portes >= 90 cm)
│   ├── Extracteur de propriétés IFC via IfcOpenShell
│   └── Moteur de calcul d'éclairement (Ratios surface vitrée / surface plancher)
│
└── BENCHMARK STRICTEMENT HOLD-OUT : 5% des volumes certifiés
    ├── Splits tests verrouillés (ResPlan, CubiCasa5K, StructScan3D)
    ├── SpatialGen-Bench (Cohérence multi-vues et perception volumique)
    └── Jeux d'évaluation critique conçus par des enseignants d'atelier
```
