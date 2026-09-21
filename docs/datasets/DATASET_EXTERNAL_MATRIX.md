# ARCHI-AI — Matrice Comparative des Datasets Externes

Ce tableau synthétise les 34 datasets audités ainsi que les candidats clés issus des répertoires spécialisés.

---

## Tableau Comparatif Synthétique

| # | Dataset | Type | Modalités | Annotations Principales | Licence | Vision | Plans | Spatial | Design | RAG | Benchmark | Difficulté | Statut Recommandé |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Structured3D** | Synthétique 3D | Panoramas, Perspectives, RGB-D, 2D Plans | Primitives 3D, BBox 3D, Layouts, Vide/Meublé | Propriétaire Non-Commercial | Élevée | Élevée | Majeure | Bonne | Faible | Excellente | Moyenne | `RELEVANT WITH PREPROCESSING` |
| **2** | **InternScenes** | Mixte 3D EAI | Maillages USD/GLB, Multi-vues, Simulation | Classes d'objets, Poses 3D, Physique | CC BY-NC-SA 4.0 | Bonne | Faible | Forte | Moyenne | Nulle | Moyenne | Très élevée | `SECONDARY` |
| **3** | **IL3D** | Synthétique 3D | Multi-vues RGB, Depth, Normales, BBox 3D | Texte en langage naturel, Boîtes 3D, Sémantique | **Apache-2.0** | Élevée | Bonne | **Exceptionnelle** | Bonne | Forte | **Idéal** | Faible à modérée | `DIRECTLY RELEVANT` |
| **4** | **M3DLayout** | Mixte 3D | Layouts 3D, Vecteurs, Textes | Texte structuré hiérarchique, Boîtes 3D | CC BY-NC 4.0 | Bonne | Forte | **Majeure** | Bonne | Élevée | Excellente | Modérée | `RELEVANT WITH PREPROCESSING` |
| **5** | **InteriorGS** | Synthétique 3DGS | 3D Gaussian Splatting (PLY), JSON | BBox 3D instances, Occupancy maps | Manycore Terms (Gated) | Excellente* | Moyenne | Forte | Bonne | Nulle | Bonne | Très élevée | `LOW PRIORITY` |
| **6** | **SpatialGen** | Synthétique 3D | Multi-vues RGB, Normales, Depth, Masques | Layouts 3D sémantiques, Géométrie de surface | CC BY-NC-SA 4.0 | **Exceptionnelle** | Bonne | **Majeure** | Excellente | Moyenne | **Idéal (SpatialGen-Bench)** | Modérée (Bench) / Élevée (Full) | `BENCHMARK ONLY` / `SECONDARY` |
| **7** | **HomeWorld** | Mixte 3D/2D | Plans K-D tree, 3D Interactif | Découpage spatial K-D, Objets interactifs | `ACCESS UNCLEAR` | Forte | **Colossale** | **Révolutionnaire** | Bonne | Bonne | Majeur futur | Modérée | `ACCESS UNCLEAR` (Veille V2) |
| **8** | **InteriorNet** | Synthétique 3D | RGB, Depth, Normales, Trajectoires vidéo | Labels d'objets, Sémantique pixel | Propriétaire Accord tripartite | Bonne (datée) | Faible | Moyenne | Faible | Nulle | Dépassé | Maximale | `NOT RECOMMENDED` |
| **9** | **OpenRooms** | Mixte Inverse Rend. | Rendus HDR, BRDF, Luminaires, Normales | Albédo, Rugosité, Composants de lumière | ScanNet + Adobe Stock | Excellente | Nulle | Moyenne | Moyenne | Faible | Très bon | Élevée | `SECONDARY` |
| **10** | **Matterport3D** | Réel Scan 3D | Panoramas RGB-D, Maillages OBJ | 40 classes sémantiques, BBox 3D, Pièces | Matterport Academic EULA | Forte | Moyenne | Forte | Bonne | Nulle | Standard académique | Élevée | `RESEARCH ONLY` |
| **11** | **HM3D** | Réel Scan 3D | Scans 3D haute fidélité (OBJ), Navigation | Découpage pièces, Top-down maps | Matterport Academic EULA | Excellente | Moyenne | Majeure | Bonne | Nulle | Référence EAI | Très élevée | `SECONDARY` / `RESEARCH ONLY` |
| **12** | **HM3D Semantics** | Réel Scan 3D | Maillages sémantiques GLB | 142k instances, 40 classes unifiées | Matterport Academic EULA | Forte | Moyenne | Très forte | Bonne | Faible | Très bon | Très élevée | `BENCHMARK ONLY` |
| **13** | **StructScan3D** | Réel RGB-D | RGB, Depth calibré, Masques sémantiques | 6 éléments structurels (murs, sols, portes...) | **CC BY 4.0** | **Excellente** | Moyenne | Forte | Faible | Nulle | **Idéal structure** | Très faible | `DIRECTLY RELEVANT` |
| **14** | **ARKit LabelMaker** | Réel iPad LIDAR | Vidéos RGB, Nuages de points, Masques 3D | Pseudo-ground truth ScanNet200 dense | Apple EULA + BSD/CC | Bonne | Faible | Bonne | Bonne | Nulle | Bon | Moyenne à élevée | `SECONDARY` |
| **15** | **SmartScenes** | Répertoire / Outils | Visualiseur Three.js, Parsers, Scènes | Divers selon sous-datasets | MIT (Code) / Divers | N/A | N/A | N/A | N/A | Faible | N/A | N/A | `NOT RECOMMENDED AS DATASET` |
| **16** | **ResPlan** | Réel Vectoriel | Géométrie vectorielle, Graphes de pièces | 17 classes (murs, portes, fenêtres, pièces) | **CC BY 4.0** | Excellente | **Majeure** | **Exceptionnelle** | Moyenne | Bonne | **Pilier 2D** | Très faible | `DIRECTLY RELEVANT` |
| **17** | **MSD** | Réel Collectif | Raster, Polygones vectoriels, Graphes d'accès | Logements collectifs, paliers, gaines, pièces | **CC BY 4.0** | Excellente | **Majeure** | **Exceptionnelle** | Bonne | Bonne | **Idéal hiérarchie** | Faible à modérée | `DIRECTLY RELEVANT` |
| **18** | **RPLAN** | Réel Matriciel | Images PNG multi-canaux (80k plans) | Masques de pièces, murs, portes, fenêtres | **CC BY 4.0** (Zenodo) | Bonne | Forte | Bonne | Faible | Faible | Classique | Faible | `RELEVANT WITH PREPROCESSING` |
| **19** | **CubiCasa5K** | Réel Scan/SVG | Scans raster réels, SVG hiérarchiques | >80 classes d'équipements, murs, pièces | CC BY-NC 4.0 | **Incomparable** | **Majeure** | Très forte | Bonne | Moyenne | **Indispensable** | Faible à modérée | `DIRECTLY RELEVANT` |
| **20** | **BRIDGE** | Réel Web + Texte | Images de plans, Paragraphes textuels | Symboles, Descriptions textuelles par zone | `LICENSE UNCLEAR` | Bonne | Forte | Très forte | Moyenne | **Élevée** | Bon captioning | Moyenne | `RAG ONLY` / `SECONDARY` |
| **21** | **FloorPlanCAD** | Réel CAD SVG | Primitives vectorielles (lignes, arcs) | 30 classes d'éléments CAD et symboles | `RESEARCH ONLY` (Abandon) | Excellente | Très forte | Forte | Faible | Nulle | Bon symboles | Moyenne | `SECONDARY` |
| **22** | **MLSTRUCT-FP** | Réel Structurel | PNG ultra-haute résolution (9000px) | Murs porteurs et dalles béton parasismiques | Non commercial recherche | Bonne | Forte (Gros œuvre) | Bonne | Faible | Faible | Bon structure | Moyenne | `SECONDARY` |
| **23** | **HomeWorld FP** | Réel Normalisé | Arbres K-D normalisés (300k plans) | Découpage spatial binaire, connectivité | `ACCESS UNCLEAR` | Forte | **Majeure** | Exceptionnelle | Bonne | Bonne | Majeur futur | Modérée | `ACCESS UNCLEAR` (Veille V2) |
| **24** | **CHOrD** | Synthétique 3D | Floorplans 2D, Scènes 3D, Graphes | Graphes hiérarchiques, non-collision | Recherche académique | Bonne | Très bonne | **Excellente** | Bonne | Bonne | Bon ergonomie | Modérée | `RELEVANT WITH PREPROCESSING` |
| **25** | **MetaScenes** | Mixte EAI | Assets 3D détaillés, Poses 6D | Micro-objets de table/étagère, relations pose | Recherche non commerciale | Excellente* | Faible | Forte (micro) | Bonne | Faible | Spécialisé robotique | Élevée | `LOW PRIORITY` |
| **26** | **HSSD** | Synthétique Manuel | Modèles GLB d'artistes, Floorplans d'archi | Proportions humaines réelles, gabarits | CC BY-NC 4.0 | Excellente | Très bonne | **Majeure** | Très bonne | Faible | Excellent spatial | Modérée | `RELEVANT WITH PREPROCESSING` |
| **27** | **iDesigner** | Inconnu | Paires texte-image (non publiées) | Prompts d'ambiances intérieures | Propriétaire fermé | N/A | Nulle | N/A | N/A | Faible | N/A | Impossible | `NOT RECOMMENDED` |
| **28** | **MMIS** | Réel Photo + Texte | 160k images photos, descriptions texte | **40 styles d'intérieur**, 5 types de pièces | **CC BY-SA 4.0** | **Excellente** | Nulle | Moyenne | **Majeure** | **Très forte** | **Idéal style/mat.** | Faible | `DIRECTLY RELEVANT` |
| **29** | **Rooms-with-Text** | Réel Photo OCR | Images d'intérieurs avec filigranes | Boîtes englobantes de texte/logos incrustés | Recherche académique | Hors sujet | Nulle | Nulle | Nulle | Nulle | N/A | N/A | `NOT RECOMMENDED` (Watermark OCR) |
| **30** | **360SpatialAI** | Prototype Web | Panoramas 360 découpés, Sorties ComfyUI | 1 600 paires de test interne | Propriétaire recherche | Conceptuelle | Nulle | Moyenne | Moyenne | Faible | N/A | Impossible | `NOT RECOMMENDED` (Pas de dataset) |
| **31** | **Kaggle interior** | Réel Scrapé | 4 147 vignettes 256x256 px | **Aucune annotation, aucun texte** | `LICENSE UNCLEAR` | Très faible | Nulle | Faible | Non annoté | Nulle | Inadapté | Nulle valeur | `NOT RECOMMENDED` |
| **32** | **architecture2022** | Mixte Diffusion | 2 415 images Parquet (ext/int) | Prompts courts non structurés | `LICENSE UNCLEAR` | Moyenne | Nulle | Faible | Hétéroclite | Nulle | Inadapté | Faible | `LOW PRIORITY` / `NOT RECOMMENDED` |
| **33a**| **ZInD (Candidat)** | Réel Photo/Panos | 71k panoramas, Plans 2D et 3D alignés | Vues réelles non meublées alignées sur plan | Zillow Research Non-com. | Très forte | Excellente | Majeure | Moyenne | Faible | Excellent vide/plan | Moyenne | `SECONDARY CANDIDATE` |
| **33b**| **BIM/IFC QA (Cand.)** | Texte Normatif | 13 485 paires QA textuelles spécialisées | Normes IFC, règles de construction, BIM | Open-access recherche | Nulle | Faible | Moyenne | Bonne | **Majeure** | Idéal normes | Très faible | `DIRECTLY RELEVANT (RAG ONLY)` |
| **34** | **Trends 2026** | Enquête Métier | Fichier CSV léger (74 répondants) | Pourcentages d'opinions et attentes clients | Citation libre MyArchitectAI | Nulle | Nulle | Nulle | Anecdotique | **Bonne (contexte)** | Nulle | Très faible | `RAG ONLY` (Pas d'entraînement) |

*\* Nécessite une étape intermédiaire de rasterisation 3D/3DGS.*

---

## Synthèse par Catégorie de Statut

- **`DIRECTLY RELEVANT` (7 datasets fondamentaux) :**
  1. `IL3D` (Spatial, Apache-2.0)
  2. `ResPlan` (Plans 2D vectoriels et graphes, CC BY 4.0)
  3. `Modified Swiss Dwellings` (Plans d'immeubles collectifs, CC BY 4.0)
  4. `CubiCasa5K` (Plans d'architectes réels annotés, CC BY-NC 4.0)
  5. `MMIS` (40 styles d'intérieurs et matériaux, CC BY-SA 4.0)
  6. `StructScan3D` (Reconnaissance de l'enveloppe bâtie réelle, CC BY 4.0)
  7. `BIM/IFC Domain QA` (Candidat RAG expert bâtiment)

- **`RELEVANT WITH PREPROCESSING` (4 datasets de haute valeur) :**
  1. `Structured3D` (Ancrage vide vs meublé et vue vs plan)
  2. `M3DLayout` (Descriptions spatiales hiérarchiques)
  3. `RPLAN` (Sous-échantillon filtré de 5 000 plans dédupliqués)
  4. `CHOrD` / `HSSD` (Proportions réalistes et circulation sans collision)

- **`BENCHMARK ONLY` (2 benchmarks d'évaluation indépendante) :**
  1. `SpatialGen-Bench` (Évaluation de la vision multi-vues et de l'éclairage)
  2. `HM3D Semantics` (Grounding sémantique fin d'objets intérieurs)

- **`RAG ONLY` (2 ressources textuelles sans image ML) :**
  1. `BRIDGE` (Paragraphes d'analyse de plans)
  2. `Interior Design Trends 2026` (Contexte temporel et sociologique, échantillon 74)

- **`NOT RECOMMENDED` (7 datasets écartés factuellement) :**
  1. `InteriorNet` (Obsolète, liens inaccessibles, pétaoctets non gérables)
  2. `Rooms-with-Text` (Hors sujet architectural : détection de logos et watermarks)
  3. `360SpatialAI` (Prototype d'application web, aucun dataset public)
  4. `iDesigner` (Dataset propriétaire interne non publié)
  5. `Kaggle interior_design` (256x256 px, non annoté, qualité indigne)
  6. `SmartScenes` (Annuaire/toolkit, pas un dataset ; SUNCG illégal)
  7. `rrustom/architecture2022clean` (Mélange non trié, prompts vagues)

- **`ACCESS UNCLEAR` (1 veille stratégique) :**
  1. `HomeWorld` (300k plans et 5k maisons, statut "Coming Soon" au dépôt officiel)
