# AXIS — Rôles Métier & Affectation Fonctionnelle des Datasets

Ce document attribue à chaque dataset audité ses rôles précis au sein de l'architecture d'intelligence spatiale et architecturale d'**AXIS**.

---

## 1. Cartographie des Rôles Métier AXIS

Dans AXIS, chaque compétence mobilisée doit reposer sur des sources de vérité supervisées adaptées. Les 13 rôles fonctionnels sont définis comme suit :

1. **`PERCEPTION` :** Capacité à identifier les éléments physiques dans une image (parois, ouvertures, meubles, volumes).
2. **`PLAN UNDERSTANDING` :** Capacité à lire, interpréter et extraire la sémantique d'un plan 2D technique d'architecte.
3. **`SPATIAL REASONING` :** Raisonnement sur les relations spatiales 3D, proximités, alignements, vis-à-vis et contiguïtés.
4. **`INTERIOR DESIGN` :** Agencement harmonieux, compositions spatiales, cohérence d'ambiance et aménagement d'habitat.
5. **`MATERIALS` :** Identification précise des matériaux (bois massifs, placages, marbres, bétons, laques, textiles, métaux).
6. **`LIGHTING` :** Analyse de la lumière naturelle (orientation, baies, apports solaires) et artificielle (directe, indirecte, température de couleur).
7. **`STYLE` :** Reconnaissance et qualification formelle des mouvements stylistiques et époques décoratives (40+ styles).
8. **`ERGONOMICS` :** Respect des normes dimensionnelles humaines, hauteurs d'usage, plans de travail, espaces de dégagement.
9. **`CIRCULATION` :** Fluidité des flux de déplacement, couloirs, zones de croisement, accès aux issues et sanitaires.
10. **`CRITIQUE` :** Capacité à poser un diagnostic architectural impartial (relever les défauts d'agencement, inconforts, aberrations de plan).
11. **`PEDAGOGY` :** Explication didactique et structurée des choix de conception, formulation de recommandations argumentées.
12. **`RAG` :** Données documentaires, connaissances normatives, fiches techniques et références textuelles d'architectes.
13. **`BENCHMARK` :** Jeux d'évaluation fermés et indépendants pour mesurer la progression sans contamination d'entraînement.

---

## 2. Matrice d'Affectation par Dataset

| Dataset | Rôles Métier Principaux | Rôles Secondaires | Justification Fonctionnelle AXIS |
| :--- | :--- | :--- | :--- |
| **Structured3D** | `SPATIAL REASONING`, `PLAN UNDERSTANDING`, `PERCEPTION` | `INTERIOR DESIGN`, `BENCHMARK` | Seul dataset reliant directement un plan 2D à une version 3D vide ET meublée d'une même pièce. |
| **IL3D** | `SPATIAL REASONING`, `INTERIOR DESIGN`, `PEDAGOGY` | `PERCEPTION`, `BENCHMARK` | Alignement natif entre description en langage naturel et placement tridimensionnel des objets (Apache-2.0). |
| **M3DLayout** | `SPATIAL REASONING`, `CIRCULATION`, `ERGONOMICS` | `CRITIQUE`, `PEDAGOGY` | Structuration hiérarchique du texte (scène globale -> grands meubles -> accessoires de circulation). |
| **ResPlan** | `PLAN UNDERSTANDING`, `SPATIAL REASONING`, `CIRCULATION` | `ERGONOMICS`, `BENCHMARK` | Dualité vecteur + graphe de connectivité de pièces mathématiquement infaillible pour les plans 2D. |
| **Modified Swiss Dwellings (MSD)** | `PLAN UNDERSTANDING`, `CIRCULATION`, `PEDAGOGY` | `CRITIQUE`, `BENCHMARK` | Introduit la hiérarchie du logement collectif, la cage d'escalier, l'ascenseur et la rigueur de plan suisse. |
| **CubiCasa5K** | `PLAN UNDERSTANDING`, `PERCEPTION`, `BENCHMARK` | `ERGONOMICS`, `CRITIQUE` | Confrontation aux graphismes de plans réels (hachures, boussoles, cotations, styles agences). |
| **MMIS** | `STYLE`, `MATERIALS`, `INTERIOR DESIGN` | `LIGHTING`, `PEDAGOGY` | Corpus d'autorité pour les 40 styles d'architecture d'intérieur et la caractérisation des matériaux. |
| **StructScan3D** | `PERCEPTION`, `CRITIQUE` | `SPATIAL REASONING`, `BENCHMARK` | Reconnaissance rigoureuse de l'enveloppe bâtie réelle (murs porteurs, cloisons, sols, plafonds, fenêtres). |
| **SpatialGen (Bench)**| `BENCHMARK`, `LIGHTING`, `PERCEPTION` | `SPATIAL REASONING` | Réservé comme banc de test d'évaluation de la cohérence multi-vues et de l'éclairage. |
| **HSSD** | `ERGONOMICS`, `SPATIAL REASONING` | `INTERIOR DESIGN`, `BENCHMARK` | Données créées par des artistes respectant les gabarits réels du mobilier et de l'anatomie humaine. |
| **CHOrD** | `CIRCULATION`, `ERGONOMICS` | `SPATIAL REASONING` | Algorithmes garantissant l'absence de collisions et la continuité des couloirs de circulation. |
| **OpenRooms** | `LIGHTING`, `MATERIALS` | `PERCEPTION`, `RESEARCH` | Vérité terrain physique sur l'albédo, la rugosité et les composantes d'éclairage direct/indirect. |
| **RPLAN (Sous-ensemble)** | `PLAN UNDERSTANDING`, `AUXILIARY` | `PERCEPTION` | Volume d'appoint pour consolider la segmentation de pièces standards d'appartements. |
| **BRIDGE** | `RAG`, `PEDAGOGY` | `PLAN UNDERSTANDING` | Paragraphes explicatifs décrivant des plans pour enrichir la base de connaissances et les prompts. |
| **BIM/IFC QA (DataDrivenAEC)** | `RAG`, `PEDAGOGY` | `CRITIQUE` | Connaissances techniques normatives, réglementation, vocabulaire IFC pour le RAG. |
| **Trends 2026 (Survey)** | `RAG` | `AUXILIARY` | Veille sociologique et tendances déclarées du marché (à citer sans entraîner). |
| **HM3D Semantics** | `BENCHMARK`, `PERCEPTION` | `SPATIAL REASONING` | Évaluation comparative externe sur la reconnaissance fine d'objets du monde réel. |
| **ARKit LabelMaker** | `AUXILIARY`, `PERCEPTION` | `BENCHMARK` | Test de robustesse sur des images d'intérieur capturées au smartphone/tablette. |

---

## 3. Répartition des Rôles pour AXIS Dataset V1

Pour la construction concrète du Dataset V1, chaque rôle est alloué à une source primaire dominante :

### A. Rôle `PLAN UNDERSTANDING` (Compréhension de Plans 2D)
- **Source primaire d'entraînement :** `ResPlan` (17 000 plans vectoriels/graphes, CC BY 4.0) + `MSD` (5 372 plans collectifs, CC BY 4.0).
- **Source d'évaluation de robustesse graphique :** Split Test de `CubiCasa5K`.
- **Compétences Master Schema :** `Skill.PLANS_2D`, `Skill.ESPACE`, `Skill.CIRCULATION`.

### B. Rôle `SPATIAL REASONING` & `CIRCULATION` (Raisonnement Spatial)
- **Source primaire d'entraînement :** `IL3D` (27 816 scènes avec descriptions naturelles, Apache-2.0) + `M3DLayout` (descriptions hiérarchiques).
- **Appui géométrique :** `Structured3D` (comparaison systématique pièce vide vs pièce meublée).
- **Compétences Master Schema :** `Skill.ESPACE`, `Skill.CIRCULATION`, `Skill.ERGONOMIE`, `Skill.MOBILIER`.

### C. Rôle `STYLE`, `MATERIALS`, `LIGHTING` (Esthétique & Matière)
- **Source primaire d'entraînement :** `MMIS` (160 000 images, 40 styles d'intérieur, CC BY-SA 4.0).
- **Appui photométrique :** Échantillon de scènes éclairage de `OpenRooms` (en recherche interne).
- **Compétences Master Schema :** `Skill.STYLE`, `Skill.MATERIAUX`, `Skill.LUMIERE`, `Skill.COULEUR`.

### D. Rôle `PERCEPTION` (Enveloppe Bâtie Réelle)
- **Source primaire :** `StructScan3D` (2 594 paires RGB-D nettoyées, segmentation murs/sols/ouvertures, CC BY 4.0).
- **Compétences Master Schema :** `Skill.VISION`, `Skill.ESPACE`.

### E. Rôle `CRITIQUE` & `PEDAGOGY` (Intelligence Cognitive & Conseil)
- **Stratégie :** Synthèse croisée de questions/réponses avancées générées à partir des paires (Plan 2D + Scène 3D) de `Structured3D` et des contraintes de circulation de `CHOrD`/`HSSD`.
- **Learning Types Master Schema :** `LearningType.CRITIQUE`, `LearningType.ERROR_DETECTION`, `LearningType.IMPROVEMENT`, `LearningType.PEDAGOGY`.

### F. Rôle `RAG` (Système Documentaire & Réglementaire)
- **Bases textuelles :** `BIM/IFC Domain QA` (13k paires), extraits textuels de `BRIDGE`, synthèses de tendances datées (`Trends 2026`).
- **Absence d'images :** Aucune contamination des poids visuels du modèle.

### G. Rôle `BENCHMARK` (Évaluation Indépendante Impartiale)
- **Bancs de test isolés :** `SpatialGen-Bench` (cohérence visuelle et lumière), Split Test holdout de `CubiCasa5K` (lecture de plans complexes), Split Test holdout de `ResPlan` (graphes spatiaux).
- **Règle absolue :** Zéro contamination avec les données de fine-tuning.
