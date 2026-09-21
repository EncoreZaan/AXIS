# ARCHI-AI — Audit Externe des Datasets (V1)

Ce document présente l'audit factuel, critique et sourcé des 34 datasets et répertoires identifiés pour le projet **ARCHI-AI**, complété par les candidats découverts dans les répertoires spécialisés.

---

## Sommaire

1. [Méthodologie d'Audit & Critères](#méthodologie-daudit--critères)
2. [Section A : Scènes Indoor 3D & Layouts (1 à 15)](#section-a--scènes-indoor-3d--layouts)
   - [1. Structured3D](#1-structured3d)
   - [2. InternScenes](#2-internscenes)
   - [3. IL3D — Indoor Layout 3D](#3-il3d--indoor-layout-3d)
   - [4. M3DLayout](#4-m3dlayout)
   - [5. InteriorGS](#5-interiorgs)
   - [6. SpatialGen](#6-spatialgen)
   - [7. HomeWorld](#7-homeworld)
   - [8. InteriorNet](#8-interiornet)
   - [9. OpenRooms](#9-openrooms)
   - [10. Matterport3D](#10-matterport3d)
   - [11. Habitat-Matterport 3D (HM3D)](#11-habitat-matterport-3d-hm3d)
   - [12. HM3D Semantics](#12-hm3d-semantics)
   - [13. StructScan3D](#13-structscan3d)
   - [14. ARKit LabelMaker](#14-arkit-labelmaker)
   - [15. SmartScenes (Répertoire / SSTK)](#15-smartscenes)
3. [Section B : Floorplans & Plans Résidentiels (16 à 23)](#section-b--floorplans--plans-résidentiels)
   - [16. ResPlan](#16-resplan)
   - [17. Modified Swiss Dwellings (MSD)](#17-modified-swiss-dwellings-msd)
   - [18. RPLAN](#18-rplan)
   - [19. CubiCasa5K](#19-cubicasa5k)
   - [20. BRIDGE](#20-bridge)
   - [21. FloorPlanCAD](#21-floorplancad)
   - [22. MLSTRUCT-FP](#22-mlstruct-fp)
   - [23. HomeWorld Floorplans (Analyse Plans 2D)](#23-homeworld-floorplans)
4. [Section C : Scènes Synthétiques & Simulation (24 à 26)](#section-c--scènes-synthétiques--simulation)
   - [24. CHOrD](#24-chord)
   - [25. MetaScenes](#25-metascenes)
   - [26. HSSD — House Scaled Scene Dataset](#26-hssd--house-scaled-scene-dataset)
5. [Section D : Image + Texte & Interior Design (27 à 32)](#section-d--image--texte--interior-design)
   - [27. iDesigner](#27-idesigner)
   - [28. MMIS — Multimodal Interior Scenes](#28-mmis--multimodal-interior-scenes)
   - [29. Rooms-with-Text](#29-rooms-with-text)
   - [30. 360SpatialAI](#30-360spatialai)
   - [31. Kaggle interior_design](#31-kaggle-interior_design)
   - [32. rrustom/architecture2022clean](#32-rrustomarchitecture2022clean)
6. [Section E : Répertoires & Candidats Additionnels (33)](#section-e--répertoires--candidats-additionnels)
   - [33. DataDrivenAEC & Additional Candidates](#33-datadrivenaec--additional-candidates)
7. [Section F : Données Métier (34)](#section-f--données-métier)
   - [34. Interior Design Trends 2026](#34-interior-design-trends-2026)

---

## Méthodologie d'Audit & Critères

Conformément aux directives de recherche :
- Les données ont été vérifiées à partir des **sources primaires** (papiers de recherche, dépôts GitHub officiels, pages Hugging Face officielles, formulaires de licence).
- Aucun score global arbitraire n'est attribué.
- Les statuts de recommandation utilisés sont strictement :
  - `DIRECTLY RELEVANT` : Pertinence immédiate, haute qualité, intégration prioritaire.
  - `RELEVANT WITH PREPROCESSING` : Très pertinent mais nécessite conversion/filtrage substantiel.
  - `SECONDARY` : Utile pour expansion future ou compléments spécialisés.
  - `BENCHMARK ONLY` : Réservé exclusivement à l'évaluation indépendante (zéro contamination train).
  - `RAG ONLY` : Données documentaires/connaissances textuelles sans modalité visuelle directe.
  - `RESEARCH ONLY` : Licence ou format restreignant l'usage à de l'expérimentation académique fermée.
  - `LOW PRIORITY` : Qualité faible, résolution inadéquate ou valeur marginale par rapport aux alternatives.
  - `NOT RECOMMENDED` : Inadapté au domaine, projet fermé, doublon redondant ou biais bloquant.
  - `LICENSE UNCLEAR` : Risque juridique sur l'entraînement ou la redistribution.
  - `ACCESS UNCLEAR` : Données non encore publiées ou liens inaccessibles.

---

## Section A : Scènes Indoor 3D & Layouts

### 1. Structured3D

- **Nom :** Structured3D
- **Catégorie :** Scènes 3D Synthétiques / Layouts Photoréalistes
- **Source primaire :** https://structured3d-dataset.org/
- **Paper :** *"Structured3D: A Large Photo-realistic Dataset for Structured 3D Modeling"*, Zheng et al., ECCV 2020 (arXiv:1908.00222).
- **Repository :** https://github.com/bertjiazheng/Structured3D
- **Page téléchargement :** Formulaire de demande sur le site officiel + miroirs Hugging Face (`Pointcept/structured3d-compressed`, `Gen3DF/Structured3D`).
- **Licence :** Licence propriétaire académique non commerciale (Structured3D Terms of Use). Code sous licence MIT.
- **Statut de licence :** Utilisable sous conditions de recherche non commerciale. Redistribution publique interdite sans accord.
- **Taille :** ~15 GB compressé (version light/annotations), ~150-250 GB pour les rendus photoréalistes complets haute résolution.
- **Nombre d'exemples/scènes :** 3 500 maisons complètes modélisées par des designers professionnels, >21 800 pièces/panoramas, ~196k vues perspectives.
- **Modalités :** Panoramas équirectangulaires, vues perspectives, depth maps, surface normals, segmentation sémantique, wireframes 3D, floorplans 2D alignés.
- **Annotations :** Primitives géométriques (lignes, plans, jonctions), bounding boxes orientées 3D d'objets, masques sémantiques, agencement de pièces.
- **Formats :** PNG/JPG (images/rendus), TXT/JSON (annotations géométriques et labels), OBJ/PLY (maillages 3D).
- **Réel / synthétique / mixte :** Synthétique photoréaliste (conçu par des designers d'intérieur professionnels via Kujiale).
- **Texte :** Métadonnées de pièces, types de pièces (salon, chambre, cuisine...), noms d'objets. Pas de descriptions en langage naturel denses d'origine.
- **Images :** Oui (panoramiques et perspectives multi-vues).
- **Plans :** Oui (plans d'étage 2D vectoriels et matriciels alignés avec la géométrie 3D).
- **3D :** Oui (maillages OBJ, wireframes 3D).
- **RGB-D :** Oui (RGB + Depth parfaitement alignés).
- **Segmentation :** Oui (instance et sémantique au niveau pixel et géométrique).
- **Depth :** Oui (profondeur exacte issue du moteur de rendu).
- **Graphes :** Graphe de connectivité déductible du floorplan et des jonctions de pièces.
- **Métadonnées :** Configuration de la scène : version vide (*unfurnished*), version meublée simple (*simple*), version meublée complète (*full*).
- **Disponibilité :** Accessible après signature de formulaire ou acceptation des termes Hugging Face.
- **Restrictions :** Usage strictement non commercial. Pas de redistribution directe des fichiers bruts.
- **Préprocessing nécessaire :** Extraction des vues perspectives, recadrage architectural, génération de questions/réponses VLM sur la spatialité et l'ameublement, alignement avec le Master Schema.
- **Coût stockage estimé :** ~25 à 50 GB pour un sous-ensemble haute qualité sélectionné.
- **Pertinence vision :** Excellente (photoréalisme, éclairage réaliste, vues multiples).
- **Pertinence plan 2D :** Élevée (floorplans directement connectés aux scènes 3D).
- **Pertinence spatial :** Majeure (rapport direct entre pièce vide et pièce meublée, relations de volumes).
- **Pertinence ergonomie :** Moyenne à élevée (agencement standard de mobilier).
- **Pertinence matériaux :** Bonne (textures réalistes, mais absence d'annotations textuelles de matériaux).
- **Pertinence lumière :** Bonne (rendus avec illumination globale).
- **Pertinence couleur :** Bonne.
- **Pertinence style :** Moyenne (styles résidentiels contemporains variés mais non annotés stylistiquement).
- **Pertinence critique :** Faible dans les données brutes (nécessite prompting synthétique).
- **Pertinence pédagogie :** Forte pour illustrer la transition plan 2D -> volume vide -> volume meublé.
- **Pertinence RAG :** Faible (peu de texte descriptif métier).
- **Pertinence benchmark :** Excellente pour le test de raisonnement spatial 2D-3D.
- **Compatibilité Master Schema :** Excellente (support multi-images, plan_2d + render_3d).
- **Risque leakage :** Scènes complètes : isoler par `scene_id` (maison) pour éviter d'avoir deux pièces de la même maison réparties entre train et test.
- **Risque doublons :** Multiples vues d'une même pièce ; déduplication spatiale requise.
- **Risques licence :** Restreint au non-commercial.
- **Risques qualité :** Très faible (synthèse professionnelle propre, pas d'artefacts de scan LIDAR).
- **Difficulté intégration :** Moyenne (nécessite pipeline de conversion d'annotations JSON -> Q/A).
- **Recommandation d'utilisation :** `RELEVANT WITH PREPROCESSING` (Candidat de premier choix pour l'ancrage spatial et la comparaison vide/meublé).

---

### 2. InternScenes

- **Nom :** InternScenes
- **Catégorie :** Scènes Indoor 3D Simulables pour Embodied AI
- **Source primaire :** https://github.com/InternRobotics/InternScenes
- **Paper :** *"InternScenes: A Large-Scale Simulatable 3D Indoor Scene Dataset for Embodied AI"*, NeurIPS 2025 / arXiv:2509.10813.
- **Repository :** https://github.com/InternRobotics/InternScenes
- **Page téléchargement :** https://huggingface.co/datasets/OpenRobotLab/InternScenes
- **Licence :** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0).
- **Statut de licence :** Utilisable sous conditions non commerciales avec obligation de partage à l'identique (ShareAlike).
- **Taille :** Très volumineux (~300 à 600 GB selon les modalités téléchargées).
- **Nombre d'exemples/scènes :** ~40 000 scènes, 1,96 million d'objets 3D, 15 types de scènes intérieures, 288 classes d'objets.
- **Modalités :** Scènes 3D interactives, maillages, physical simulation properties, multi-vues RGB, bounding boxes.
- **Annotations :** Classes d'objets, positions 3D, relations physiques, densité d'objets (41,5 objets par zone en moyenne).
- **Formats :** USD/GLB/OBJ, JSON pour les agencements et métadonnées.
- **Réel / synthétique / mixte :** Mixte : Real2Sim (scans réels réhabilités), Gen (génération procédurale), Synthetic (conception par designers).
- **Texte :** Labels sémantiques de classes, métadonnées de simulation. Peu de prose descriptive.
- **Images :** Rendus extractibles via simulateur (Habitat ou Isaac Lab).
- **Plans :** Top-down occupancy maps et layouts déductibles.
- **3D :** Oui, scènes 3D complètes.
- **RGB-D :** Générable par rendu.
- **Segmentation :** Oui (instances d'objets 3D).
- **Depth :** Générable par moteur de simulation.
- **Graphes :** Graphe spatial d'objets dérivable.
- **Métadonnées :** Physique (collisions résolues, masse, friction).
- **Disponibilité :** Active sur Hugging Face.
- **Restrictions :** CC BY-NC-SA 4.0 (interdit l'exploitation commerciale directe, ShareAlike sur modèles dérivés redistribués).
- **Préprocessing nécessaire :** Très lourd : nécessite d'exécuter un pipeline de rendu (ex. Isaac Sim ou Blender) pour convertir les scènes 3D en paires images + questions.
- **Coût stockage estimé :** 200 à 400 GB.
- **Pertinence vision :** Bonne, mais orientée robotique mobile / interaction physique.
- **Pertinence plan 2D :** Faible (pas de plans d'architecte formels, seulement des top-down maps).
- **Pertinence spatial :** Forte (placement réaliste de petits objets, encombrement réel).
- **Pertinence ergonomie :** Forte pour les micro-dégagements et les encombrements de table/cuisine.
- **Pertinence matériaux :** Moyenne.
- **Pertinence lumière :** Moyenne (rendus de simulateur souvent moins photoréalistes qu'architecturaux).
- **Pertinence couleur :** Moyenne.
- **Pertinence style :** Faible à moyenne (hétérogène, orienté interaction).
- **Pertinence critique :** Faible nativement.
- **Pertinence pédagogie :** Moyenne.
- **Pertinence RAG :** Très faible.
- **Pertinence benchmark :** Secondaire (axé navigation robotique).
- **Compatibilité Master Schema :** Moyenne (nécessite beaucoup d'inférence pour devenir une annotation d'architecture).
- **Risque leakage :** Regroupement par scène obligatoire.
- **Risque doublons :** Redondance des micro-objets.
- **Risques licence :** Contrainte ShareAlike (SA).
- **Risques qualité :** Scènes parfois visuellement encombrées ("cluttered") de manière non réaliste pour un projet d'architecture.
- **Difficulté intégration :** Très élevée (ingénierie 3D lourde requise).
- **Recommandation d'utilisation :** `SECONDARY` (Trop lourd pour la phase V1 ; à réserver pour des tâches d'encombrement spatial fin ultérieures).

---

### 3. IL3D — Indoor Layout 3D

- **Nom :** IL3D (Indoor Layout 3D)
- **Catégorie :** Dataset Multimodal pour Génération de Scènes Guidée par LLM
- **Source primaire :** https://openreview.net/forum?id=0oxkxG9cCo
- **Paper :** *"IL3D: A Large-Scale Indoor Layout Dataset for LLM-Driven 3D Scene Generation"*, Zhou et al., 2024/2025.
- **Repository :** https://github.com/ (référencé dans la publication)
- **Page téléchargement :** https://huggingface.co/datasets/WenxuZhou/IL3D
- **Licence :** **Apache-2.0** (confirmée sur la page officielle Hugging Face).
- **Statut de licence :** **Clairement utilisable**, y compris pour le fine-tuning commercial et la redistribution avec attribution.
- **Taille :** ~30 à 60 GB selon les modalités.
- **Nombre d'exemples/scènes :** 27 816 layouts intérieurs à travers 18 types de pièces ; 29 215 modèles d'objets 3D haute fidélité.
- **Modalités :** Multi-vues RGB, depth maps, normal maps, nuages de points, 3D bounding boxes, masques sémantiques, annotations en langage naturel.
- **Annotations :** Descriptions textuelles par instance et globales au niveau scène, bounding boxes orientées 3D, étiquettes sémantiques.
- **Formats :** Images PNG, annotations JSON, maillages OBJ/GLB.
- **Réel / synthétique / mixte :** Synthétique haute qualité.
- **Texte :** **Oui, descriptions détaillées en langage naturel** reliant la disposition des objets au prompt textuel d'aménagement.
- **Images :** Oui, rendus multi-vues de chaque pièce.
- **Plans :** Layouts 2D/3D avec coordonnées métriques.
- **3D :** Oui (assets et scènes).
- **RGB-D :** Oui.
- **Segmentation :** Oui (masques sémantiques par instance).
- **Depth :** Oui.
- **Graphes :** Relations de proximité et agencement formulées en langage structuré.
- **Métadonnées :** Typologie de pièce, identifiants d'objets, dimensions physiques.
- **Disponibilité :** Active et téléchargeable sur Hugging Face.
- **Restrictions :** Aucune restriction commerciale (licence permissive Apache-2.0).
- **Préprocessing nécessaire :** Extraction des paires (rendu vue principale, description d'aménagement), formulation de questions VLM de raisonnement spatial ("Explique l'implantation des assises par rapport aux ouvertures").
- **Coût stockage estimé :** ~35 GB.
- **Pertinence vision :** Très forte.
- **Pertinence plan 2D :** Bonne (plans de masse de pièces déductibles des boîtes 3D).
- **Pertinence spatial :** **Exceptionnelle** (alignement natif texte ↔ relations spatiales 3D).
- **Pertinence ergonomie :** Élevée (circulation entre meubles, dégagements).
- **Pertinence matériaux :** Moyenne.
- **Pertinence lumière :** Bonne.
- **Pertinence couleur :** Bonne.
- **Pertinence style :** Moyenne à bonne.
- **Pertinence critique :** Forte pour la détection d'erreurs de placement.
- **Pertinence pédagogie :** Très forte.
- **Pertinence RAG :** Forte (descriptions textuelles d'aménagements intérieurs exploitables).
- **Pertinence benchmark :** Idéal pour évaluer la compréhension spatiale d'un VLM.
- **Compatibilité Master Schema :** Excellente (adéquation directe avec `observables`, `interpretations`, `skills: [ESPACE, MOBILIER, CIRCULATION]`).
- **Risque leakage :** Faible si séparation par layout ID.
- **Risque doublons :** Faible.
- **Risques licence :** **Nul** (Apache-2.0).
- **Risques qualité :** Faible (validation géométrique rigoureuse dans le papier).
- **Difficulté intégration :** Faible à modérée.
- **Recommandation d'utilisation :** `DIRECTLY RELEVANT` (Candidat prioritaire absolu en raison de sa licence Apache-2.0 et de ses annotations en langage naturel).

---

### 4. M3DLayout

- **Nom :** M3DLayout
- **Catégorie :** Layouts 3D Multi-sources & Descriptions Textuelles Structurées
- **Source primaire :** https://graphic-kiliani.github.io/M3DLayout/
- **Paper :** *"M3DLayout: A Multi-source Dataset for Text-driven 3D Indoor Scene Generation"*, CVPR 2025/2026 Highlight (arXiv:2509.23728).
- **Repository :** https://github.com/Graphic-Kiliani/M3DLayout-code
- **Page téléchargement :** https://huggingface.co/datasets/Metaverse-AI-Lab/M3DLayout
- **Licence :** Creative Commons Attribution-NonCommercial 4.0 International (CC-BY-NC-4.0).
- **Statut de licence :** Utilisable sous conditions académiques/non commerciales. Les sous-composants 3D-FRONT conservent leurs termes respectifs.
- **Taille :** ~25 à 45 GB.
- **Nombre d'exemples/scènes :** 21 367 layouts, >433 000 instances d'objets.
- **Modalités :** Layouts 3D, représentations vectorielles, texte descriptif hiérarchique, rendus de scènes.
- **Annotations :** Résumés globaux de scènes, relations de placement de mobilier majeur, agencements fins de petits objets.
- **Formats :** JSON (descriptions et géométries), NPY, PNG.
- **Réel / synthétique / mixte :** Mixte : scans réels réalignés, modèles CAO professionnels (3D-FRONT) et génération procédurale.
- **Texte :** **Oui, descriptions textuelles hiérarchiques de haute qualité** (structure globale -> grands meubles -> petits éléments).
- **Images :** Rendus 2D disponibles ou générables.
- **Plans :** Layouts 2D au sol précis avec orientation.
- **3D :** Boîtes englobantes 3D et matrices de pose.
- **RGB-D :** Partiel.
- **Segmentation :** Oui (instances d'objets annotées).
- **Depth :** Dérivable.
- **Graphes :** Graphes de relations spatiales intégrés.
- **Métadonnées :** Type de pièce, dimensions, styles.
- **Disponibilité :** Active sur Hugging Face.
- **Restrictions :** Non commercial (CC-BY-NC-4.0).
- **Préprocessing nécessaire :** Conversion des hiérarchies textuelles en dialogues structurés question/réponse.
- **Coût stockage estimé :** ~25 GB.
- **Pertinence vision :** Bonne.
- **Pertinence plan 2D :** Très bonne.
- **Pertinence spatial :** **Majeure** (description explicite des relations : "en face de", "à gauche de", "aligné avec").
- **Pertinence ergonomie :** Élevée (composition spatiale, hiérarchie de circulation).
- **Pertinence matériaux :** Faible à moyenne.
- **Pertinence lumière :** Faible.
- **Pertinence couleur :** Moyenne.
- **Pertinence style :** Bonne.
- **Pertinence critique :** Bonne.
- **Pertinence pédagogie :** Excellente pour enseigner la structuration d'un espace.
- **Pertinence RAG :** Élevée pour le corpus de descriptions spatiales.
- **Pertinence benchmark :** Excellente pour le spatial reasoning.
- **Compatibilité Master Schema :** Excellente.
- **Risque leakage :** Partitionnement strict par scène ID requis.
- **Risque doublons :** Faible.
- **Risques licence :** Non commercial strict.
- **Risques qualité :** Très faible.
- **Difficulté intégration :** Modérée.
- **Recommandation d'utilisation :** `RELEVANT WITH PREPROCESSING` (Excellente source de raisonnement spatial et d'agencement).

---

### 5. InteriorGS

- **Nom :** InteriorGS
- **Catégorie :** 3D Gaussian Splatting Indoor avec Sémantique
- **Source primaire :** https://github.com/manycore-research/InteriorGS
- **Paper :** Associated with Manycore Tech (Kujiale) Research, 2025/2026.
- **Repository :** https://github.com/manycore-research/InteriorGS
- **Page téléchargement :** https://huggingface.co/datasets/spatialverse/InteriorGS
- **Licence :** Licence propriétaire spécifique "InteriorGS Terms of Use" (Manycore Tech). Accès restreint ("Gated dataset").
- **Statut de licence :** Recherche non commerciale uniquement, nécessite approbation individuelle sur Hugging Face.
- **Taille :** ~35 à 60 GB (fichiers `.ply` compressés par scène, ~35 MB par scène pour 1 000 scènes).
- **Nombre d'exemples/scènes :** 1 000 scènes 3D complètes réparties sur >80 typologies d'environnements intérieurs (résidentiel, musée, commerce...).
- **Modalités :** 3D Gaussian Splatting (`3dgs_compressed.ply`), boîtes sémantiques 3D (`labels.json`), cartes d'occupance.
- **Annotations :** Bounding boxes orientées par instance, structure hiérarchique de scène, occupance de sol.
- **Formats :** PLY (Gaussians 3D), JSON (labels), PNG (occupancy).
- **Réel / synthétique / mixte :** Synthétique haute fidélité (moteur Manycore/Kujiale).
- **Texte :** Labels sémantiques d'instances.
- **Images :** Non fournies sous forme de banque d'images plates JPEG traditionnelles ; nécessite un rasterizer 3DGS pour synthétiser des images de caméras.
- **Plans :** Occupancy maps 2D au sol.
- **3D :** Oui, représentations volumiques par gaussiennes.
- **RGB-D :** Rendu temps réel possible.
- **Segmentation :** Oui (au niveau 3DGS).
- **Depth :** Dérivable par rasterisation.
- **Graphes :** Hiérarchies de scène dans le JSON.
- **Métadonnées :** Typologies de pièces détaillées.
- **Disponibilité :** Gated sur Hugging Face (accord préalable obligatoire).
- **Restrictions :** Non commercial, interdiction de décompilation pour concurrence directe.
- **Préprocessing nécessaire :** Très lourd : nécessite un moteur de rendu 3D Gaussian Splatting (CUDA/C++) pour générer les images d'entraînement de Qwen2-VL.
- **Coût stockage estimé :** ~40 GB.
- **Pertinence vision :** Excellente une fois rendue, mais nulle sous forme de fichiers PLY bruts pour un VLM.
- **Pertinence plan 2D :** Moyenne.
- **Pertinence spatial :** Forte.
- **Pertinence ergonomie :** Bonne.
- **Pertinence matériaux :** Excellente (reflets spéculaires et transmission lumineuse gérés par 3DGS).
- **Pertinence lumière :** Très bonne.
- **Pertinence couleur :** Excellente.
- **Pertinence style :** Bonne.
- **Pertinence critique :** Faible nativement.
- **Pertinence pédagogie :** Moyenne.
- **Pertinence RAG :** Nulle.
- **Pertinence benchmark :** Intéressant pour évaluer la vision multi-angles continue.
- **Compatibilité Master Schema :** Faible sans pipeline de rendu intermédiaire.
- **Risque leakage :** Par scène.
- **Risque doublons :** Faible.
- **Risques licence :** Gated, contrôle Manycore.
- **Risques qualité :** Faible (données très propres).
- **Difficulté intégration :** Très élevée (infrastructure de rendu 3DGS indispensable).
- **Recommandation d'utilisation :** `LOW PRIORITY` (Complexité de rendu disproportionnée par rapport aux bénéfices VLM immédiats).

---

### 6. SpatialGen

- **Nom :** SpatialGen
- **Catégorie :** Dataset Photoréaliste Multi-vues Guidé par Layout
- **Source primaire :** https://manycore-research.github.io/SpatialGen
- **Paper :** *"SpatialGen: Layout-guided 3D Indoor Scene Generation"*, Fang et al. (HKUST / Manycore), arXiv:2509.14981.
- **Repository :** https://github.com/manycore-research/SpatialGen
- **Page téléchargement :** https://huggingface.co/datasets/wx91726/SpatialGen-Bench (Benchmark), testset sur GitHub.
- **Licence :** **CC BY-NC-SA 4.0** pour les données du projet.
- **Statut de licence :** Utilisable sous conditions non commerciales et partage à l'identique.
- **Taille :** Dataset complet annoncé à >1 To (4,7 millions d'images). Testset de 48 pièces (~5 à 10 GB).
- **Nombre d'exemples/scènes :** 12 328 scènes structurées, 57 440 pièces, 4,7 millions de rendus 2D photoréalistes.
- **Modalités :** Images RGB multi-vues, cartes de coordonnées de scène (geometry), cartes de segmentation sémantique, depth maps, normales.
- **Annotations :** Layouts 3D sémantiques, masques de segmentation, poses caméras cohérentes.
- **Formats :** PNG, EXR, JSON.
- **Réel / synthétique / mixte :** Synthétique photoréaliste professionnel.
- **Texte :** Prompts de conditionnement textuel de styles et d'ambiances.
- **Images :** Oui, 4,7M de rendus à cohérence multi-vues stricte.
- **Plans :** Layouts 2D/3D associés aux pièces.
- **3D :** Coordonnées spatiales de surface 3D.
- **RGB-D :** Oui.
- **Segmentation :** Oui (masques sémantiques pixel-perfect).
- **Depth :** Oui.
- **Graphes :** Relations d'agencement.
- **Métadonnées :** Styles, types de pièces, paramètres d'éclairage.
- **Disponibilité :** Benchmark et testset immédiatement disponibles ; release complète du corpus 4.7M annoncée progressivement.
- **Restrictions :** Non commercial (CC BY-NC-SA 4.0).
- **Préprocessing nécessaire :** Sous-échantillonnage impératif (impossible de stocker 4,7M d'images localement).
- **Coût stockage estimé :** 15 GB pour le sous-ensemble de test/benchmark et un échantillon sélectionné.
- **Pertinence vision :** **Exceptionnelle** (qualité photoréaliste haut de gamme).
- **Pertinence plan 2D :** Bonne.
- **Pertinence spatial :** **Majeure** (cohérence géométrique multi-vues absolue).
- **Pertinence ergonomie :** Élevée.
- **Pertinence matériaux :** Très bonne.
- **Pertinence lumière :** Excellente (rendus avec illumination globale et variations lumineuses).
- **Pertinence couleur :** Très bonne.
- **Pertinence style :** Excellente (grand éventail de styles d'intérieur).
- **Pertinence critique :** Bonne.
- **Pertinence pédagogie :** Excellente.
- **Pertinence RAG :** Moyenne.
- **Pertinence benchmark :** **Idéal pour ARCHI-AI Benchmark** (SpatialGen-Bench existe déjà sur Hugging Face).
- **Compatibilité Master Schema :** Excellente.
- **Risque leakage :** Filtrer strictement par scène ID.
- **Risque doublons :** Vues très rapprochées d'une même pièce à filtrer.
- **Risques licence :** ShareAlike (SA).
- **Risques qualité :** Nul (SOTA actuel).
- **Difficulté intégration :** Modérée pour le sous-ensemble/benchmark, impossible pour le corpus complet sans stockage cloud massif.
- **Recommandation d'utilisation :** `BENCHMARK ONLY` pour le sous-ensemble de test (`SpatialGen-Bench`), `SECONDARY` pour l'entraînement complet ultérieur.

---

### 7. HomeWorld

- **Nom :** HomeWorld (Kairos-HomeWorld)
- **Catégorie :** Framework Multi-pièces & Génération Totale d'Habitation
- **Source primaire :** https://kairos-homeworld.github.io/
- **Paper :** *"HomeWorld: A Unified Floorplan-to-Furnished Framework for Generating Controllable, Densely Interactive Whole-Home Scenes"*, Li et al., Juin 2026 (arXiv:2606.06390).
- **Repository :** https://github.com/Kairos-HomeWorld/HomeWorld
- **Page téléchargement :** Dépôt GitHub (statut "Coming Soon" pour les poids et données complètes).
- **Licence :** En attente de confirmation formelle lors de la release (prévu recherche open-source).
- **Statut de licence :** `ACCESS UNCLEAR` / À vérifier lors de la libération publique.
- **Taille :** Non finalisée (estimée à >100 GB pour l'ensemble des scènes 3D et 300k plans).
- **Nombre d'exemples/scènes :** 300 000 plans d'étage résidentiels réels, 5 000 habitations complètes meublées et interactives, 50 000 objets interactifs.
- **Modalités :** Plans 2D nettoyés (arbre K-D), agencements 3D, scènes multi-pièces complètes, assets interactifs.
- **Annotations :** Arbres de découpage spatial K-D, bounding boxes 3D, graphes d'interactivité.
- **Formats :** JSON (K-D trees, layouts), GLB/USD, PNG.
- **Réel / synthétique / mixte :** Mixte : plans réels collectés et nettoyés, ameublement synthétique guidé par modèles de diffusion et VLMs.
- **Texte :** Prompts de génération globale d'habitation.
- **Images :** Rendus 2D de validation.
- **Plans :** 300 000 plans d'étage résidentiels structurés.
- **3D :** Oui, maisons complètes.
- **RGB-D :** Générable.
- **Segmentation :** Oui.
- **Depth :** Dérivable.
- **Graphes :** Graphes hiérarchiques de maison entière (K-D tree).
- **Métadonnées :** Nombre de pièces, distributions, surfaces.
- **Disponibilité :** **Non téléchargeable immédiatement** (le dépôt affiche "coming soon").
- **Restrictions :** Inconnues à ce jour.
- **Préprocessing nécessaire :** Parsing des K-D trees et sélection d'un échantillon représentatif.
- **Coût stockage estimé :** Variable.
- **Pertinence vision :** Forte.
- **Pertinence plan 2D :** **Colossale** (300k plans résidentiels nettoyés).
- **Pertinence spatial :** **Révolutionnaire** (couvre la maison entière et la cohérence inter-pièces, pas seulement une pièce isolée).
- **Pertinence ergonomie :** Forte (circulations globales, corridors, accès).
- **Pertinence matériaux :** Moyenne.
- **Pertinence lumière :** Moyenne.
- **Pertinence couleur :** Moyenne.
- **Pertinence style :** Bonne.
- **Pertinence critique :** Forte.
- **Pertinence pédagogie :** Majeure.
- **Pertinence RAG :** Bonne.
- **Pertinence benchmark :** Futur benchmark de référence pour la cohérence globale d'un plan.
- **Compatibilité Master Schema :** Excellente.
- **Risque leakage :** Nécessitera un audit d'empreintes pHash strict lors de la release.
- **Risque doublons :** Inconnu.
- **Risques licence :** Inconnu.
- **Risques qualité :** Élevée selon les résultats du papier.
- **Difficulté intégration :** Modérée dès parution.
- **Recommandation d'utilisation :** `ACCESS UNCLEAR` (À surveiller activement pour V2 ; ne peut pas être intégré dans le sprint V1 immédiat).

---

### 8. InteriorNet

- **Nom :** InteriorNet
- **Catégorie :** Dataset Synthétique Méga-échelle pour l'Intérieur
- **Source primaire :** https://interiornet.org/
- **Paper :** *"InteriorNet: Mega-scale Multi-sensor Photo-realistic Indoor Scenes Dataset"*, Li et al. (Imperial College London & Kujiale), BMVC 2018.
- **Repository :** Scripts d'outils sur GitHub / Imperial College.
- **Page téléchargement :** Formulaire de demande d'accès sur `interiornet.org`.
- **Licence :** Licence propriétaire académique non commerciale (accord tripartite Imperial College / Kujiale).
- **Statut de licence :** Restrictive, recherche uniquement, formulaires souvent non répondus ou liens FTP expirés.
- **Taille :** Gigantesque (>20 To théorique complet, plusieurs centaines de Go par sous-dossier).
- **Nombre d'exemples/scènes :** Annoncé à 20 millions d'images, 5,3 millions de configurations d'aménagement, 22 millions de keyframes.
- **Modalités :** RGB, depth, normal, segmentation sémantique, trajectories caméra, optical flow, illuminations variables.
- **Annotations :** Sémantique fine, étiquettes de mobilier, trajectoires inertielles (IMU).
- **Formats :** PNG, TXT, binaires propriétaires.
- **Réel / synthétique / mixte :** Synthétique (modèles CAO Kujiale).
- **Texte :** Labels sémantiques basiques.
- **Images :** Oui, des millions.
- **Plans :** Layouts 2D sous-jacents mais difficilement dissociables.
- **3D :** Données brutes souvent non fournies (uniquement rendus vidéo/trajectoires).
- **RGB-D :** Oui.
- **Segmentation :** Oui.
- **Depth :** Oui.
- **Graphes :** Non.
- **Métadonnées :** Poses caméras.
- **Disponibilité :** **Très problématique.** De nombreux chercheurs rapportent des liens de téléchargement morts ou des délais d'attente indéfinis depuis 2022-2024.
- **Restrictions :** Strictement non commercial, interdiction de partage de liens.
- **Préprocessing nécessaire :** Titanesque (filtrage, extraction d'images statiques, purge de vidéos floues).
- **Coût stockage estimé :** Ingérable pour une station locale (>500 GB au minimum).
- **Pertinence vision :** Bonne sur le papier, mais datée (rendus 2018 inférieurs à Structured3D ou SpatialGen).
- **Pertinence plan 2D :** Faible (orienté SLAM et robotique visuelle).
- **Pertinence spatial :** Moyenne.
- **Pertinence ergonomie :** Faible.
- **Pertinence matériaux :** Moyenne.
- **Pertinence lumière :** Bonne (variations jour/nuit).
- **Pertinence couleur :** Moyenne.
- **Pertinence style :** Faible.
- **Pertinence critique :** Nulle.
- **Pertinence pédagogie :** Faible.
- **Pertinence RAG :** Nulle.
- **Pertinence benchmark :** Dépassé par des benchmarks plus récents.
- **Compatibilité Master Schema :** Faible.
- **Risque leakage :** Élevé (séquences vidéo successives avec 99% de similarité visuelle).
- **Risque doublons :** Extrême.
- **Risques licence :** Propriétaire contraignant.
- **Risques qualité :** Trop redondant (keyframes vidéo rapprochées).
- **Difficulté intégration :** Maximale.
- **Recommandation d'utilisation :** `NOT RECOMMENDED` (Obsolète, accès verrouillé, rapport coût de stockage / valeur pédagogique très défavorable face à Structured3D).

---

### 9. OpenRooms

- **Nom :** OpenRooms
- **Catégorie :** Dataset Photométrique & Inverse Rendering pour Scènes Intérieures
- **Source primaire :** https://ucsd-openrooms.github.io/
- **Paper :** *"OpenRooms: An Open Framework for Photorealistic Indoor Scene Datasets"*, Li, Sunkavalli, Chandraker et al., CVPR 2021.
- **Repository :** https://github.com/ViLab-UCSD/OpenRooms
- **Page téléchargement :** Téléchargement via scripts Python dans le dépôt officiel.
- **Licence :** Dépôt sous licence recherche, **mais dépendances de licences tierces complexes** : nécessite la licence ScanNet, et certaines textures exigent une licence Adobe Stock séparée.
- **Statut de licence :** `LICENSE UNCLEAR` / Complexe : risque juridique si redistribution de modèles entraînés sur des assets protégés Adobe Stock.
- **Taille :** ~100 à 250 GB.
- **Nombre d'exemples/scènes :** 1 200 scènes d'intérieur photoréalistes, ~87 000 images haute résolution, multiples variations d'éclairage.
- **Modalités :** HDR radiance, albedo BRDF (spatially-varying), surface normals, depth, masques de sources lumineuses, masques d'objets.
- **Annotations :** Paramètres photométriques complets (rugosité, spécularité, transmission), types de lampes, fenêtres, éclairage naturel.
- **Formats :** HDR, PNG, EXR, XML (fichiers de scène Mitsuba / OptiX).
- **Réel / synthétique / mixte :** Mixte : géométrie dérivée de scans réels (ScanNet/Scan2CAD) texturée avec des matériaux haute fidélité et simulée par ray tracing physique.
- **Texte :** Métadonnées physiques de matériaux et luminaires.
- **Images :** Oui (rendus HDR et LDR).
- **Plans :** Non (pas de plan d'architecte 2D).
- **3D :** Oui (maillages CAD assemblés).
- **RGB-D :** Oui.
- **Segmentation :** Oui (par matériau et par objet).
- **Depth :** Oui.
- **Graphes :** Non.
- **Métadonnées :** Spécifications optiques et géométrie des luminaires.
- **Disponibilité :** Téléchargeable via les scripts du dépôt.
- **Restrictions :** Non commercial, restrictions ScanNet et Adobe Stock.
- **Préprocessing nécessaire :** Conversion HDR -> SDR (tonemapping), formulation de questions d'analyse de lumière et de matériaux.
- **Coût stockage estimé :** ~80 GB.
- **Pertinence vision :** Excellente pour la compréhension de la lumière physique.
- **Pertinence plan 2D :** Quasi nulle.
- **Pertinence spatial :** Moyenne.
- **Pertinence ergonomie :** Faible.
- **Pertinence matériaux :** **Majeure** (ground truth physique d'albédo et rugosité).
- **Pertinence lumière :** **Exceptionnelle** (décomposition éclairage direct / indirect / environnemental).
- **Pertinence couleur :** Très bonne.
- **Pertinence style :** Moyenne.
- **Pertinence critique :** Faible.
- **Pertinence pédagogie :** Excellente pour expliquer la physique de l'éclairage intérieur.
- **Pertinence RAG :** Faible.
- **Pertinence benchmark :** Très bon pour tester les capacités de décomposition de lumière d'un VLM.
- **Compatibilité Master Schema :** Bonne (`skills: [LUMIERE, MATERIAUX]`).
- **Risque leakage :** Découpage par scène ScanNet.
- **Risque doublons :** Multiples variations d'éclairage d'une même caméra (excellente opportunité de contrastive learning).
- **Risques licence :** Élevés en raison des droits Adobe Stock sur les textures.
- **Risques qualité :** Faible (rendu Mitsuba de très haut niveau).
- **Difficulté intégration :** Élevée.
- **Recommandation d'utilisation :** `SECONDARY` (À exploiter ultérieurement pour un module spécialisé en éclairage, mais à écarter du socle V1 pour éviter l'intrication de licences ScanNet/Adobe).

---

### 10. Matterport3D

- **Nom :** Matterport3D
- **Catégorie :** Scans 3D Réels de Bâtiments Complets
- **Source primaire :** https://niessner.github.io/Matterport/
- **Paper :** *"Matterport3D: Learning from RGB-D Data in Indoor Environments"*, Chang et al., 3DV 2017 (arXiv:1709.06158).
- **Repository :** https://github.com/niessner/Matterport
- **Page téléchargement :** Formulaire formel d'accord de licence Matterport EULA envoyé par email.
- **Licence :** **Matterport End User License Agreement for Academic Use of Model Data.**
- **Statut de licence :** **Très restrictive.** Strictement non commerciale, interdiction formelle de créer des services concurrents de visualisation 3D, interdiction de géolocalisation des biens, interdiction de redistribution des données brutes.
- **Taille :** ~1,3 To au total (textures haute définition, maillages, panoramas). Version réduite ~150-200 GB.
- **Nombre d'exemples/scènes :** 90 bâtiments complets, 10 800 panoramas, 194 400 vues RGB-D.
- **Modalités :** Panoramas équirectangulaires RGB, depth maps, maillages 3D texturés (`.obj`), segmentations sémantiques 2D et 3D.
- **Annotations :** 50 811 objets annotés en 3D avec 40 catégories sémantiques, découpage par pièces, normales de surface.
- **Formats :** JPG/PNG, OBJ, PLY, JSON.
- **Réel / synthétique / mixte :** **100% Réel** (scans lidar/photométrie Matterport Pro).
- **Texte :** Labels sémantiques de pièces et d'objets.
- **Images :** Oui, prises de vue photographiques réelles.
- **Plans :** Layouts de pièces et maillages de sol déductibles.
- **3D :** Oui, maillages d'immeubles complets multi-étages.
- **RGB-D :** Oui.
- **Segmentation :** Oui (instance et sémantique 2D/3D).
- **Depth :** Oui (capteur réel).
- **Graphes :** Graphe de connectivité entre points de vue panoramiques.
- **Métadonnées :** Types d'espaces, surface des bâtiments.
- **Disponibilité :** Accessible uniquement après approbation formelle de la demande académique.
- **Restrictions :** Interdiction totale d'utilisation commerciale directe ou indirecte. Risque juridique majeur si le modèle final est déployé en SaaS.
- **Préprocessing nécessaire :** Extraction de vues perspectives à partir des panoramas, correction des trous de maillage et artéfacts de scan.
- **Coût stockage estimé :** >150 GB minimum pour un sous-ensemble utilisable.
- **Pertinence vision :** Forte pour le réalisme des scènes vécues (désordre réel, usure, textures réelles).
- **Pertinence plan 2D :** Moyenne.
- **Pertinence spatial :** Forte.
- **Pertinence ergonomie :** Élevée (bâtiments réels avec circulation humaine réelle).
- **Pertinence matériaux :** Moyenne (artefacts de reprojection de textures fréquents).
- **Pertinence lumière :** Bonne (lumière réelle ambiante).
- **Pertinence couleur :** Bonne.
- **Pertinence style :** Forte (résidences réelles typiquement américaines).
- **Pertinence critique :** Bonne.
- **Pertinence pédagogie :** Moyenne.
- **Pertinence RAG :** Nulle.
- **Pertinence benchmark :** Classique en recherche universitaire, mais contraignant en produit.
- **Compatibilité Master Schema :** Bonne.
- **Risque leakage :** Bâtiments multi-pièces : partitionner strictement par bâtiment (`scene_id`).
- **Risque doublons :** Nombreux panoramas distants de seulement 1 à 2 mètres.
- **Risques licence :** **Critiques** (EULA Matterport menaçante pour toute commercialisation future).
- **Risques qualité :** Maillages bruités, miroirs non réfléchissants déformés.
- **Difficulté intégration :** Élevée.
- **Recommandation d'utilisation :** `RESEARCH ONLY` / `NOT RECOMMENDED FOR V1 CORE` (Le verrouillage juridique de Matterport est antinomique avec une solution pérenne).

---

### 11. Habitat-Matterport 3D (HM3D)

- **Nom :** HM3D (Habitat-Matterport 3D Research Dataset)
- **Catégorie :** Scans Réels Haute Résolution pour Embodied AI
- **Source primaire :** https://aihabitat.org/datasets/hm3d/
- **Paper :** *"Habitat-Matterport 3D Dataset (HM3D): Next-Generation 3D Datasets for Embodied AI"*, Ramakrishnan et al., NeurIPS 2021.
- **Repository :** https://github.com/facebookresearch/habitat-matterport3d-dataset
- **Page téléchargement :** Formulaire sur ai-habitat / Matterport.
- **Licence :** Matterport EULA for Academic Use of Model Data.
- **Statut de licence :** Restrictive (identique à Matterport3D).
- **Taille :** ~400 GB à plus de 2 To selon la résolution de maillage.
- **Nombre d'exemples/scènes :** 1 000 bâtiments complets haute résolution (800 train, 100 val, 100 test), 112 371 pièces réelles.
- **Modalités :** Maillages 3D OBJ texturés, textures 2K/4K, trajectoires de navigation, top-down maps.
- **Annotations :** Découpage de pièces, bounding boxes, sémantique d'espaces (complétée par HM3DSem).
- **Formats :** OBJ, GLB, JSON.
- **Réel / synthétique / mixte :** Réel (scans Matterport Pro2).
- **Texte :** Métadonnées d'espaces.
- **Images :** Générées par rendu dans Habitat-Sim.
- **Plans :** Top-down semantic maps.
- **3D :** Oui, scans 3D denses complets.
- **RGB-D :** Générable via Habitat-Sim.
- **Segmentation :** Oui (avec HM3D Semantics).
- **Depth :** Oui.
- **Graphes :** Graphe de navigation navigable.
- **Métadonnées :** Type d'architecture, surface, volume.
- **Disponibilité :** Requiert approbation d'accord de licence.
- **Restrictions :** Strictly non-commercial research.
- **Préprocessing nécessaire :** Installation obligatoire de Habitat-Sim pour extraire des images utilisables par Qwen2-VL.
- **Coût stockage estimé :** >300 GB.
- **Pertinence vision :** Excellente.
- **Pertinence plan 2D :** Moyenne.
- **Pertinence spatial :** Majeure.
- **Pertinence ergonomie :** Élevée.
- **Pertinence matériaux :** Bonne.
- **Pertinence lumière :** Réelle mais figée au moment du scan.
- **Pertinence couleur :** Bonne.
- **Pertinence style :** Excellente diversité d'habitats réels.
- **Pertinence critique :** Moyenne.
- **Pertinence pédagogie :** Moyenne.
- **Pertinence RAG :** Nulle.
- **Pertinence benchmark :** Référence standard en embodied AI.
- **Compatibilité Master Schema :** Moyenne (nécessite tooling Habitat).
- **Risque leakage :** Bâtiments complets : split par bâtiment impératif.
- **Risque doublons :** Élevé lors des rendus de trajectoire.
- **Risques licence :** Élevés (Matterport EULA).
- **Risques qualité :** Faible (bien plus propre que Matterport3D 2017).
- **Difficulté intégration :** Très élevée (nécessite pipeline de simulation).
- **Recommandation d'utilisation :** `SECONDARY` / `RESEARCH ONLY`.

---

### 12. HM3D Semantics

- **Nom :** HM3D Semantics (HM3D-Sem / HM3DSem)
- **Catégorie :** Extension Sémantique Dense de HM3D
- **Source primaire :** https://aihabitat.org/datasets/hm3d-semantics/
- **Paper :** *"Habitat-Matterport 3D Semantics Dataset (HM3D-Sem)"*, Yadav et al., CVPR 2023 (arXiv:2210.05633v3).
- **Repository :** https://github.com/facebookresearch/habitat-matterport3d-dataset
- **Page téléchargement :** Via AI Habitat après signature EULA.
- **Licence :** Matterport EULA + Habitat research terms.
- **Statut de licence :** Non commercial strict.
- **Taille :** ~50 à 150 GB (annotations et maillages ré-étiquetés).
- **Nombre d'exemples/scènes :** 202 scènes annotées en v0.1 (étendu à >400 scènes en v0.2), 142 646 instances d'objets annotées manuellement, 1 600+ classes du vocabulaire d'intérieur regroupées en 40 catégories majeures.
- **Modalités :** Maillages 3D segmentés par instance (`.semantic.glb`), fichiers de correspondances sémantiques.
- **Annotations :** Identification manuelle rigoureuse des objets d'intérieur, des éléments architecturaux (murs, fenêtres, portes, escaliers), et des zones fonctionnelles.
- **Formats :** GLB, JSON, TXT.
- **Réel / synthétique / mixte :** Réel (scans HM3D avec labels d'experts).
- **Texte :** Vocabulaire sémantique architectural et mobilier très riche.
- **Images :** Rendus segmentés via Habitat-Sim.
- **Plans :** Layouts 2D sémantiques.
- **3D :** Oui.
- **RGB-D :** Oui.
- **Segmentation :** **Excellente** (segmentation 3D instance-level de haute qualité).
- **Depth :** Oui.
- **Graphes :** Graphe scène/objet.
- **Métadonnées :** Catégories lexicales unifiées.
- **Disponibilité :** Soumis à accord Matterport.
- **Restrictions :** Non commercial strict.
- **Préprocessing nécessaire :** Rendu via simulateur.
- **Coût stockage estimé :** ~100 GB.
- **Pertinence vision :** Forte.
- **Pertinence plan 2D :** Moyenne.
- **Pertinence spatial :** Très forte.
- **Pertinence ergonomie :** Excellente (rapport meuble / circulation / obstacle).
- **Pertinence matériaux :** Moyenne.
- **Pertinence lumière :** Moyenne.
- **Pertinence couleur :** Bonne.
- **Pertinence style :** Bonne.
- **Pertinence critique :** Bonne.
- **Pertinence pédagogie :** Forte.
- **Pertinence RAG :** Faible.
- **Pertinence benchmark :** Très bon pour le grounding sémantique.
- **Compatibilité Master Schema :** Bonne.
- **Risque leakage :** Isolation par scène HM3D.
- **Risque doublons :** Faible.
- **Risques licence :** Élevés (Matterport EULA).
- **Risques qualité :** Faible (annotations humaines très soignées).
- **Difficulté intégration :** Très élevée.
- **Recommandation d'utilisation :** `BENCHMARK ONLY` (Dans le cadre strict d'expériences de recherche).

---

### 13. StructScan3D

- **Nom :** StructScan3D (v1)
- **Catégorie :** Dataset RGB-D Spécialisé Éléments Architecturaux & BIM
- **Source primaire :** MDPI *Sensors* 2025, 25(3), 856 / PMC12158164.
- **Paper :** *"StructScan3D v1: A First RGB-D Dataset for Indoor Building Elements Segmentation and BIM Modeling"*, Chowdhury et al., 2025.
- **Repository :** https://github.com/ishraqrc/StructScan3D
- **Page téléchargement :** Dépôt GitHub / Liens Zenodo associés.
- **Licence :** **Creative Commons Attribution 4.0 International (CC BY 4.0)** (Open Access MDPI).
- **Statut de licence :** **Clairement utilisable**, usage commercial et académique permis avec simple attribution.
- **Taille :** Très compacte : ~4 à 8 GB.
- **Nombre d'exemples/scènes :** 2 594 images/trames annotées collectées via capteur Kinect Azure.
- **Modalités :** RGB, Depth (aligné), masques de segmentation sémantique pour éléments architecturaux.
- **Annotations :** Segmentation sémantique précise sur 6 classes architecturales structurelles fondamentales :
  1. Murs (*Walls*)
  2. Sols (*Floors*)
  3. Plafonds (*Ceilings*)
  4. Fenêtres (*Windows*)
  5. Portes (*Doors*)
  6. Objets divers (*Misc/Furniture*)
- **Formats :** PNG (RGB et masques), TIFF/NPY (profondeur 16-bit), JSON.
- **Réel / synthétique / mixte :** **100% Réel** (captures de bâtiments universitaires et administratifs réels).
- **Texte :** Labels de classes et métadonnées géométriques pour reconstruction BIM.
- **Images :** Oui, 2 594 paires RGB/Depth.
- **Plans :** Non direct (sert à la reconstruction Scan-to-BIM).
- **3D :** Nuages de points dérivables directement de la profondeur calibrée.
- **RGB-D :** Oui, calibré métriquement.
- **Segmentation :** **Ciblée éléments structurels de bâtiment**.
- **Depth :** Oui.
- **Graphes :** Non.
- **Métadonnées :** Paramètres intrinsèques de caméra Kinect.
- **Disponibilité :** Active et immédiatement téléchargeable.
- **Restrictions :** Aucune (CC BY 4.0).
- **Préprocessing nécessaire :** Conversion simple : formulation de paires VLM ("Identifie les limites structurelles mur/plafond et les ouvertures").
- **Coût stockage estimé :** ~6 GB.
- **Pertinence vision :** **Excellente pour la détection structurelle**.
- **Pertinence plan 2D :** Moyenne (sert de pont entre scan et plan BIM).
- **Pertinence spatial :** Forte (enveloppe architecturale pure).
- **Pertinence ergonomie :** Faible à moyenne.
- **Pertinence matériaux :** Moyenne.
- **Pertinence lumière :** Moyenne.
- **Pertinence couleur :** Moyenne.
- **Pertinence style :** Faible (architecture contemporaine institutionnelle).
- **Pertinence critique :** Bonne pour l'état des surfaces et alignements.
- **Pertinence pédagogie :** Très bonne pour l'identification de l'enveloppe bâtie.
- **Pertinence RAG :** Nulle.
- **Pertinence benchmark :** Idéal pour tester si un VLM sait distinguer un mur porteur/cloison d'un meuble.
- **Compatibilité Master Schema :** Excellente (`document_type: photography`, `skills: [VISION, ESPACE]`).
- **Risque leakage :** Séquences vidéo : déduplication par pHash indispensable pour ne pas garder des trames consécutives quasi identiques.
- **Risque doublons :** Élevé si toutes les trames vidéo sont conservées ; échantillonnage à 1 trame / seconde nécessaire (~500 images uniques).
- **Risques licence :** Nul (CC BY 4.0).
- **Risques qualité :** Faible.
- **Difficulté intégration :** Très faible.
- **Recommandation d'utilisation :** `DIRECTLY RELEVANT` (Excellente brique réelle, légère et libre de droits, pour ancrer la reconnaissance des parois et ouvertures).

---

### 14. ARKit LabelMaker

- **Nom :** ARKit LabelMaker
- **Catégorie :** Pseudo-Ground Truth Sémantique 3D à Grande Échelle
- **Source primaire :** https://labelmaker.org/
- **Paper :** *"ARKit LabelMaker: A New Scale for Indoor 3D Scene Understanding"*, arXiv:2410.13924v2 / 3DV 2024.
- **Repository :** https://github.com/cvg/labelmaker
- **Page téléchargement :** https://huggingface.co/datasets/labelmaker/arkit_labelmaker
- **Licence :** Code/pipeline sous licence BSD / CC BY-SA 4.0 ; données sous-jacentes régies par la **licence Apple ARKitScenes** (recherche non commerciale).
- **Statut de licence :** Utilisable sous conditions strictes de recherche non commerciale en raison des données sources d'Apple.
- **Taille :** ~80 à 180 GB selon les packages téléchargés.
- **Nombre d'exemples/scènes :** 5 048 captures vidéo iPad LIDAR, 1 661 scènes réelles uniques, millions de points labellisés automatiquement par projection de modèles 2D (SAM, DINO).
- **Modalités :** RGB vidéo, maillages iPad LIDAR, masques de segmentation sémantique 3D denses.
- **Annotations :** Labels sémantiques fins projetés en 3D sur les catégories ScanNet200.
- **Formats :** PLY, MP4, JSON.
- **Réel / synthétique / mixte :** Réel (scans Apple ARKit réels dans des foyers et bureaux).
- **Texte :** Vocabulaire ScanNet200.
- **Images :** Trames vidéo réelles.
- **Plans :** Non.
- **3D :** Maillages surfaciques réels.
- **RGB-D :** Oui.
- **Segmentation :** Oui (pseudo-labels 3D de haute densité).
- **Depth :** Oui.
- **Graphes :** Non.
- **Métadonnées :** Métadonnées ARKit Apple.
- **Disponibilité :** Active sur Hugging Face et GitHub.
- **Restrictions :** Non commercial (Apple Inc. terms).
- **Préprocessing nécessaire :** Extraction de trames clés, sous-échantillonnage vidéo, nettoyage des artefacts LIDAR iPad.
- **Coût stockage estimé :** ~70 GB.
- **Pertinence vision :** Bonne (environnement de vie réel spontané).
- **Pertinence plan 2D :** Faible.
- **Pertinence spatial :** Bonne.
- **Pertinence ergonomie :** Bonne.
- **Pertinence matériaux :** Moyenne.
- **Pertinence lumière :** Éclairage naturel/artificiel domestique réaliste.
- **Pertinence couleur :** Bonne.
- **Pertinence style :** Forte (vrais intérieurs contemporains habités).
- **Pertinence critique :** Bonne (encombrement réel, défauts d'agencement du quotidien).
- **Pertinence pédagogie :** Moyenne.
- **Pertinence RAG :** Nulle.
- **Pertinence benchmark :** Bon pour tester la robustesse aux images prises sur smartphone.
- **Compatibilité Master Schema :** Bonne.
- **Risque leakage :** Regroupement strict par identifiant de scène ARKit (`scene_id`).
- **Risque doublons :** Très fort sur les vidéos continues.
- **Risques licence :** Restreint au non commercial par Apple.
- **Risques qualité :** Les annotations sont des pseudo-labels (générés par IA, non vérifiés à 100% par des humains).
- **Difficulté intégration :** Moyenne à élevée.
- **Recommandation d'utilisation :** `SECONDARY` (Utile pour tester la robustesse "monde réel / smartphone", mais inférieur aux datasets avec plans pour le socle V1).

---

### 15. SmartScenes

- **Nom :** SmartScenes (Répertoire / Stanford SmartScenes Toolkit — SSTK)
- **Catégorie :** Annuaire, Toolkit & Simulateur de Scènes 3D (Stanford)
- **Source primaire :** https://smartscenes.github.io/pages/datasets.html
- **Paper :** *"SmartScenes: Visualizing and Annotating 3D Scenes on the Web"*, Savva et al.
- **Repository :** https://github.com/smartscenes/sstk
- **Page téléchargement :** Liens pointant vers Matterport3D, ScanNet, SUNCG, ShapeNet.
- **Licence :** MIT pour les outils logiciels (SSTK). Les datasets répertoriés ont chacun leur licence propre.
- **Statut de licence :** Hétérogène / Composite selon les sous-datasets.
- **Taille :** Non applicable au répertoire global.
- **Nombre d'exemples/scènes :** Agrégat de plusieurs centaines de milliers de scènes et modèles 3D.
- **Modalités :** Outils de visualisation Web, export 3D, parseurs.
- **Annotations :** Diverses selon les datasets sources.
- **Formats :** WebGL, Three.js, JSON, OBJ.
- **Réel / synthétique / mixte :** Mixte.
- **Texte :** Dépend des sources.
- **Images :** Dépend des sources.
- **Plans :** Outils de rendu 2D top-down intégrés dans SSTK.
- **3D :** Oui.
- **RGB-D :** Oui.
- **Segmentation :** Oui.
- **Depth :** Oui.
- **Graphes :** Graphes de relations spatiales (ex: Stanford Scene Database).
- **Métadonnées :** Multiples.
- **Disponibilité :** Le site et le code sont actifs, mais certains datasets listés sont morts ou indisponibles (ex: **SUNCG a été supprimé de tout l'écosystème académique à la suite du procès Planner5D**).
- **Restrictions :** Ne pas essayer de télécharger SUNCG (illégal / violation de propriété intellectuelle).
- **Préprocessing nécessaire :** N/A.
- **Coût stockage estimé :** 0 GB (ne pas télécharger comme dataset monolithique).
- **Pertinence vision :** Variable.
- **Pertinence plan 2D :** Variable.
- **Pertinence spatial :** Outils très utiles pour l'inférence.
- **Pertinence ergonomie :** N/A.
- **Pertinence matériaux :** N/A.
- **Pertinence lumière :** N/A.
- **Pertinence couleur :** N/A.
- **Pertinence style :** N/A.
- **Pertinence critique :** N/A.
- **Pertinence pédagogie :** N/A.
- **Pertinence RAG :** Faible.
- **Pertinence benchmark :** N/A.
- **Compatibilité Master Schema :** N/A.
- **Risque leakage :** Élevé si croisement ScanNet / Matterport3D non contrôlé.
- **Risque doublons :** Fort recouvrement entre répertoires Stanford.
- **Risques licence :** SUNCG = Interdit.
- **Risques qualité :** Variable.
- **Difficulté intégration :** N/A.
- **Recommandation d'utilisation :** `NOT RECOMMENDED AS A DATASET` (À utiliser uniquement comme référence bibliographique et boîte à outils de visualisation, aucun téléchargement global).

---

## Section B : Floorplans & Plans Résidentiels

### 16. ResPlan

- **Nom :** ResPlan
- **Catégorie :** Plans Résidentiels Vectoriels & Graphes de Pièces
- **Source primaire :** arXiv:2508.14006v1
- **Paper :** *"ResPlan: A Large-Scale Vector-Graph Dataset of 17,000 Residential Floor Plans"*, 2025.
- **Repository :** Code et utilitaires intégrés dans le package Kaggle (`resplan_utils.py`, `ResPlan_demo.ipynb`).
- **Page téléchargement :** https://www.kaggle.com/datasets/resplan/resplan
- **Licence :** **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
- **Statut de licence :** **Clairement utilisable sans restriction commerciale** (entraînement, dérivation et redistribution autorisés avec simple crédit).
- **Taille :** **~297,2 MB** (extrêmement compact et optimisé).
- **Nombre d'exemples/scènes :** **17 000 plans résidentiels complets** d'appartements et maisons individuelles.
- **Modalités :** Géométries vectorielles fermées, graphes de connectivité de pièces (`networkx`), coordonnées métriques à l'échelle, images rasterisées associées.
- **Annotations :** 17 classes architecturales unifiées :
  - Éléments structurels : murs, portes, fenêtres, balcons, gaines techniques.
  - Pièces fonctionnelles : salon, cuisine, chambre principale, chambre secondaire, salle de bains, WC, couloir, entrée, rangement, buanderie, etc.
- **Formats :** JSON (géométries vectorielles et graphes), SVG/PNG.
- **Réel / synthétique / mixte :** Réel (plans issus d'agences immobilières et de promoteurs, nettoyés et vectorisés par un pipeline géométrique strict).
- **Texte :** Typologies de pièces, surfaces métriques calculées, matrice d'adjacence textuelle.
- **Images :** Oui (rendus noir & blanc et couleur des plans).
- **Plans :** **100% Plans 2D de haute précision**.
- **3D :** Non (extrusion 2.5D possible grâce aux coordonnées métriques).
- **RGB-D :** Non.
- **Segmentation :** Oui (polygones vectoriels exacts sans perte de résolution).
- **Depth :** Non.
- **Graphes :** **Oui, graphes de connectivité de pièces complets natifs**.
- **Métadonnées :** Échelle métrique, orientation, surface totale, ratio de pièces.
- **Disponibilité :** Immédiate sur Kaggle via l'API Kaggle ou téléchargement direct.
- **Restrictions :** Aucune (CC BY 4.0).
- **Préprocessing nécessaire :** Pipeline propre : conversion JSON -> raster haute définition pour Qwen2-VL, synthèse de dialogues d'analyse de plan ("Quelles sont les pièces contiguës à la cuisine ?", "Où se situent les points d'eau ?").
- **Coût stockage estimé :** ~1,5 GB (avec rendus PNG haute résolution générés).
- **Pertinence vision :** Excellente pour la lecture de graphismes 2D.
- **Pertinence plan 2D :** **Majeure / Incontournable**.
- **Pertinence spatial :** **Exceptionnelle** (la connectivité est vérifiable mathématiquement par le graphe).
- **Pertinence ergonomie :** **Majeure** (circulations, passages, distances chambre-sanitaire).
- **Pertinence matériaux :** Faible (non documentés sur les plans de vente).
- **Pertinence lumière :** Forte (position des fenêtres et orientations cardinales).
- **Pertinence couleur :** Faible (plans techniques).
- **Pertinence style :** Moyenne (typologies spatiales contemporaines).
- **Pertinence critique :** **Excellente** (identification de pièces aveugles, de couloirs disproportionnés).
- **Pertinence pédagogie :** **Idéale pour le module PLANS_2D**.
- **Pertinence RAG :** Bonne (permet d'indexer les graphes spatiaux).
- **Pertinence benchmark :** Pilier fondamental du benchmark de lecture de plans.
- **Compatibilité Master Schema :** Parfaite (`document_type: plan_2d`, `skills: [PLANS_2D, ESPACE, CIRCULATION, ERGONOMIE]`).
- **Risque leakage :** Chaque plan possède un ID unique, isolation sans fuite.
- **Risque doublons :** Faible (déjà filtré dans le papier).
- **Risques licence :** **Nul** (CC BY 4.0).
- **Risques qualité :** Très faible (géométries propres, pas de bruit de scan).
- **Difficulté intégration :** **Très faible** (clé en main avec notebooks Python).
- **Recommandation d'utilisation :** `DIRECTLY RELEVANT` (Dataset de référence absolue pour les plans 2D dans ARCHI-AI V1).

---

### 17. Modified Swiss Dwellings (MSD)

- **Nom :** Modified Swiss Dwellings (MSD)
- **Catégorie :** Plans de Complexes Immobiliers & Logements Collectifs Européens
- **Source primaire :** https://caspervanengelenburg.github.io/msd-eccv24-page/
- **Paper :** *"MSD: A Benchmark Dataset for Floor Plan Generation of Building Complexes"*, van Engelenburg et al. (TU Delft / ETH Zurich), ECCV 2024 (arXiv:2407.10121).
- **Repository :** https://github.com/caspervanengelenburg/msd-eccv24
- **Page téléchargement :** https://www.kaggle.com/datasets/wassimjabi/modified-swiss-dwellings-01-json
- **Licence :** **Creative Commons Attribution 4.0 International (CC BY 4.0)** (dérivé de Swiss Dwellings v3.0.0, également sous CC BY 4.0).
- **Statut de licence :** **Clairement utilisable sans restriction commerciale.**
- **Taille :** ~1,2 GB.
- **Nombre d'exemples/scènes :** 5 372 plans d'immeubles de logements collectifs, englobant plus de **18 900 appartements distincts**.
- **Modalités :** Images matricielles, polygones vectoriels, graphes d'accessibilité (`torch_geometric` et `networkx`).
- **Annotations :** Cloisons, murs porteurs, cages d'escalier, ascenseurs, typologie d'appartement (du studio au T5+), balcons, gaines.
- **Formats :** JSON, PNG, NPY, Graph GML.
- **Réel / synthétique / mixte :** **100% Réel** (cadastre et archives architecturales de logements suisses construits).
- **Texte :** Typologies d'espaces, cantons, métadonnées de construction.
- **Images :** Oui (plans d'étages complets).
- **Plans :** **Oui, plans d'immeubles complets** (niveau d'échelle supérieur aux plans de simples appartements).
- **3D :** Non.
- **RGB-D :** Non.
- **Segmentation :** Oui (vectorielle et matricielle).
- **Depth :** Non.
- **Graphes :** Oui, graphes d'accès complexes (rue -> hall -> palier -> appartement -> pièce).
- **Métadonnées :** Année, surfaces, règles d'accès incendie/évacuation.
- **Disponibilité :** Active sur GitHub et Kaggle.
- **Restrictions :** Aucune (CC BY 4.0).
- **Préprocessing nécessaire :** Rendu des plans d'ensemble et découpage optionnel par appartement individuel, génération de Q/A sur la distribution des accès et l'orientation.
- **Coût stockage estimé :** ~3 GB avec rendus.
- **Pertinence vision :** Excellente pour les plans d'architecture de haute complexité.
- **Pertinence plan 2D :** **Majeure** (introduit l'architecture collective et le logement social de qualité).
- **Pertinence spatial :** Exceptionnelle (distinction parties communes / parties privatives).
- **Pertinence ergonomie :** Très forte (normes d'accessibilité, paliers, circulation verticale).
- **Pertinence matériaux :** Faible.
- **Pertinence lumière :** Bonne (plans traversants vs mono-orientés).
- **Pertinence couleur :** Faible.
- **Pertinence style :** Excellente représentativité de l'architecture moderne et contemporaine suisse (réputée pour sa rigueur de plan).
- **Pertinence critique :** Forte.
- **Pertinence pédagogie :** Majeure pour les étudiants et architectes (analyse de plan de masse et d'étage courant).
- **Pertinence RAG :** Bonne.
- **Pertinence benchmark :** Idéal pour évaluer la compréhension de la hiérarchie spatiale.
- **Compatibilité Master Schema :** Excellente.
- **Risque leakage :** Isoler par immeuble/bâtiment (`project_name` / `scene_id`).
- **Risque doublons :** Étages courants identiques : déduplication stricte nécessaire.
- **Risques licence :** Nul (CC BY 4.0).
- **Risques qualité :** Qualité architecturale exceptionnelle (plans professionnels certifiés).
- **Difficulté intégration :** Faible à modérée.
- **Recommandation d'utilisation :** `DIRECTLY RELEVANT` (Complément indispensable à ResPlan, apporte l'échelle de l'immeuble collectif et l'école d'architecture suisse sous licence libre).

---

### 18. RPLAN

- **Nom :** RPLAN
- **Catégorie :** Dataset Matriciel Massif de Plans Résidentiels
- **Source primaire :** http://staff.ustc.edu.cn/~fuxm/projects/DeepLayout/index.html
- **Paper :** *"Data-driven Interior Plan Generation for Residential Buildings"*, Wu et al., ACM Transactions on Graphics (SIGGRAPH 2019).
- **Repository :** GitHub / Python package `rplanpy`.
- **Page téléchargement :** Miroir Zenodo officiel (DOI: 10.5281/zenodo.18874946) + page projet USTC.
- **Licence :** **Creative Commons Attribution 4.0 International (CC-BY-4.0)** sur le miroir Zenodo de référence.
- **Statut de licence :** Utilisable pour l'entraînement et l'évaluation.
- **Taille :** ~2,5 à 4 GB.
- **Nombre d'exemples/scènes :** **80 788 plans d'appartements résidentiels**.
- **Modalités :** Images rasterisées PNG multi-canaux (canaux pour murs, pièces, portes, fenêtres).
- **Annotations :** Masques sémantiques de pièces, masques de murs, positions de portes et fenêtres, polygones d'emprise extérieure.
- **Formats :** PNG 8-bit / RGBA, utilitaires Python.
- **Réel / synthétique / mixte :** Réel (plans d'appartements construits en Chine, numérisés et standardisés).
- **Texte :** Labels de pièces simples (Living Room, Master Bedroom, Kitchen, etc.).
- **Images :** Oui, 80k images de plans.
- **Plans :** Oui, plans d'appartements standardisés.
- **3D :** Non.
- **RGB-D :** Non.
- **Segmentation :** Oui (masques de segmentation sémantique pixel).
- **Depth :** Non.
- **Graphes :** Graphe de contiguïté extractible via `rplanpy`.
- **Métadonnées :** Type d'appartement, orientation.
- **Disponibilité :** Active et pérenne sur Zenodo.
- **Restrictions :** Respect de l'attribution (SIGGRAPH 2019).
- **Préprocessing nécessaire :** Colorisation des plans (les PNG bruts encodent les labels dans des canaux d'entiers 0-10 peu lisibles directement pour un VLM sans palette visuelle), conversion en format visuel naturel.
- **Coût stockage estimé :** ~5 GB.
- **Pertinence vision :** Bonne.
- **Pertinence plan 2D :** Forte par son volume, mais inférieure géométriquement à ResPlan (les murs sont purement matriciels, sans vecteur).
- **Pertinence spatial :** Bonne.
- **Pertinence ergonomie :** Moyenne (typologies d'appartements chinois très répétitives).
- **Pertinence matériaux :** Nulle.
- **Pertinence lumière :** Bonne (présence marquée des balcons et baies vitrées).
- **Pertinence couleur :** Faible.
- **Pertinence style :** Très homogène (résidentiel standard urbain chinois des années 2010).
- **Pertinence critique :** Moyenne.
- **Pertinence pédagogie :** Bonne pour l'entraînement intensif à la détection de pièces.
- **Pertinence RAG :** Faible.
- **Pertinence benchmark :** Classique mais en passe d'être supplanté par ResPlan.
- **Compatibilité Master Schema :** Bonne.
- **Risque leakage :** Biais de plans miroirs ou identiques sur des programmes immobiliers de masse : déduplication pHash indispensable.
- **Risque doublons :** **Très élevé** (des milliers de plans sont de simples variantes ou miroirs d'un même modèle standard).
- **Risques licence :** Nul (CC BY 4.0 sur Zenodo).
- **Risques qualité :** Biais typologique fort (immeubles tours avec appartements traversants nord-sud standardisés).
- **Difficulté intégration :** Faible.
- **Recommandation d'utilisation :** `RELEVANT WITH PREPROCESSING` (Utile pour un sous-échantillon filtré de 5 000 plans dédupliqués, mais inutile de télécharger les 80 000 plans bruts en raison de la redondance massive).

---

### 19. CubiCasa5K

- **Nom :** CubiCasa5K
- **Catégorie :** Plans Immobiliers Réels Annotés Vectoriellement
- **Source primaire :** https://github.com/CubiCasa/CubiCasa5k
- **Paper :** *"CubiCasa5K: A Dataset and an Improved Multi-Task Model for Floorplan Image Analysis"*, Kalervo et al., ICCV 2019 Workshop.
- **Repository :** https://github.com/CubiCasa/CubiCasa5k
- **Page téléchargement :** https://zenodo.org/record/2613548 / GitHub officiel / Miroir Kaggle.
- **Licence :** **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.
- **Statut de licence :** Utilisable sous conditions de recherche non commerciale.
- **Taille :** ~18 à 25 GB.
- **Nombre d'exemples/scènes :** **5 000 plans d'architecte réels** avec annotations complètes.
- **Modalités :** Images raster originales (scans de brochures, plans PDF rasterisés), fichiers vectoriels SVG annotés par calques.
- **Annotations :** >80 catégories d'objets, murs (extérieurs et intérieurs), portes (battantes, coulissantes), fenêtres, pièces, équipements sanitaires (douche, baignoire, lavabo), meubles de cuisine, mobilier fixe.
- **Formats :** SVG (vectoriel polyline/polygone hiérarchique), PNG (raster original et masques), TXT.
- **Réel / synthétique / mixte :** **100% Réel** (plans réels du marché immobilier finlandais et nordique).
- **Texte :** Noms des pièces en finnois/anglais, surfaces mesurées.
- **Images :** Oui, styles graphiques réels extrêmement hétérogènes (plans dessinés main, plans DAO, plans commerciaux en couleur).
- **Plans :** **Oui, plans réels d'une authenticité totale**.
- **3D :** Non.
- **RGB-D :** Non.
- **Segmentation :** Oui, vectorielle SVG et matricielle.
- **Depth :** Non.
- **Graphes :** Déductibles des SVG.
- **Métadonnées :** Résolution originale, ratio d'aspect.
- **Disponibilité :** Active et pérenne sur Zenodo et GitHub.
- **Restrictions :** Non commercial (CC BY-NC 4.0).
- **Préprocessing nécessaire :** Nettoyage des textes en finnois, normalisation de l'échelle, conversion SVG -> masques d'apprentissage, génération de questions/réponses VLM multimodales.
- **Coût stockage estimé :** ~20 GB.
- **Pertinence vision :** **Incomparable pour la robustesse** (confrontation aux bruits graphiques réels : cotations, logos d'agence, hachures, boussoles).
- **Pertinence plan 2D :** **Majeure**.
- **Pertinence spatial :** Très forte.
- **Pertinence ergonomie :** Élevée (sanitaires et cuisines détaillés).
- **Pertinence matériaux :** Faible (quelques hachures de carrelage/parquet).
- **Pertinence lumière :** Bonne.
- **Pertinence couleur :** Variable selon le style graphique du plan.
- **Pertinence style :** Nordique / Européen contemporain.
- **Pertinence critique :** Bonne.
- **Pertinence pédagogie :** Excellente pour apprendre à un modèle à lire des plans du monde réel et pas seulement des vecteurs théoriques parfaits.
- **Pertinence RAG :** Moyenne.
- **Pertinence benchmark :** **Indispensable comme benchmark de robustesse graphique**.
- **Compatibilité Master Schema :** Excellente (`document_type: plan_2d`, `domain: interior_design`).
- **Risque leakage :** 5 000 plans indépendants, risque de fuite quasi nul si splits respectés.
- **Risque doublons :** Très faible.
- **Risques licence :** Restreint au non commercial.
- **Risques qualité :** Faible (annotations supervisées professionnelles par CubiCasa).
- **Difficulté intégration :** Faible à modérée.
- **Recommandation d'utilisation :** `DIRECTLY RELEVANT` (Dataset historique de référence, indispensable pour confronter ARCHI-AI aux plans réels scannés).

---

### 20. BRIDGE

- **Nom :** BRIDGE (Building Plan Repository for Image Description Generation, and Evaluation)
- **Catégorie :** Floorplans Appariés à des Descriptions Textuelles en Langage Naturel
- **Source primaire :** ICDAR 2019 / Goyal et al. (IIT Jodhpur)
- **Paper :** *"BRIDGE: Building plan repository for image description generation, and evaluation"*, Goyal, Mistry, Chattopadhyay, Bhatnagar, 2019.
- **Repository :** https://github.com/gesstalt/BRIDGE
- **Page téléchargement :** Référencé sur DataDrivenAEC / GitHub.
- **Licence :** Non spécifiée formellement dans le dépôt (`LICENSE UNCLEAR`), réputé pour usage académique.
- **Statut de licence :** `LICENSE UNCLEAR` / Données scrapées du web architectural sans licence claire d'exploitation.
- **Taille :** ~6 à 12 GB.
- **Nombre d'exemples/scènes :** >13 000 images de plans d'étage annotées.
- **Modalités :** Images de plans (PNG/JPG), descriptions textuelles au niveau paragraphe, boîtes englobantes de symboles, graphes de régions.
- **Annotations :** Symboles architecturaux (portes, fenêtres, lits, canapés, tables), légendes textuelles par zone, résumés textuels d'agencement.
- **Formats :** JSON, TXT, XML, PNG.
- **Réel / synthétique / mixte :** Réel (collecte sur sites web d'architecture, complétée par ROBIN et SESYD).
- **Texte :** **Oui, paragraphes descriptifs complets de la disposition du plan** (extrêmement rare pour les plans 2D).
- **Images :** Oui, plans d'étage 2D.
- **Plans :** Oui.
- **3D :** Non.
- **RGB-D :** Non.
- **Segmentation :** Boîtes englobantes et détection de symboles.
- **Depth :** Non.
- **Graphes :** Graphes de scène 2D (relation pièce-symbole).
- **Métadonnées :** Type de bâtiment.
- **Disponibilité :** Dépôt existant, mais liens de téléchargement de l'archive complète parfois instables.
- **Restrictions :** Droits d'auteur des images web d'origine incertains.
- **Préprocessing nécessaire :** Nettoyage des descriptions en anglais, filtrage des plans basse résolution ou filigranés.
- **Coût stockage estimé :** ~8 GB.
- **Pertinence vision :** Bonne.
- **Pertinence plan 2D :** Forte.
- **Pertinence spatial :** **Très forte grâce aux paragraphes descriptifs**.
- **Pertinence ergonomie :** Bonne.
- **Pertinence matériaux :** Faible.
- **Pertinence lumière :** Faible.
- **Pertinence couleur :** Faible.
- **Pertinence style :** Hétérogène.
- **Pertinence critique :** Bonne.
- **Pertinence pédagogie :** Très forte pour l'alignement vision-langage de plans.
- **Pertinence RAG :** Élevée (les paragraphes d'analyse de plans sont directement exploitables en RAG).
- **Pertinence benchmark :** Intéressant pour l'évaluation de captioning de plans.
- **Compatibilité Master Schema :** Excellente (adéquation naturelle avec `question`/`answer`).
- **Risque leakage :** Déduplication d'images obligatoire (scraping web).
- **Risque doublons :** Élevé.
- **Risques licence :** Élevés (absence de licence explicite et sourcing web hétérogène).
- **Risques qualité :** Qualité de texte inégale (paragraphes parfois générés par des règles ou non relus par des architectes).
- **Difficulté intégration :** Moyenne.
- **Recommandation d'utilisation :** `RAG ONLY` / `SECONDARY` (À exploiter pour enrichir le RAG et inspirer des templates de questions, mais prudence sur le fine-tuning direct sans clarification de licence).

---

### 21. FloorPlanCAD

- **Nom :** FloorPlanCAD
- **Catégorie :** Dessins CAD Vectoriels Professionnels & Panoptic Symbol Spotting
- **Source primaire :** ICCV 2021 (Zheng et al.)
- **Paper :** *"FloorPlanCAD: A Large-Scale CAD Drawing Dataset for Panoptic Symbol Spotting"*, ICCV 2021.
- **Repository :** Initialement `floorplancad.github.io` (projet fermé en 2022). Miroirs communautaires sur Hugging Face (`Voxel51/FloorPlanCAD`) et OpenDataLab.
- **Page téléchargement :** https://huggingface.co/datasets/Voxel51/FloorPlanCAD
- **Licence :** Déclarée non commerciale pour recherche lors de la publication ICCV. Statut complexe suite à la fermeture du projet officiel.
- **Statut de licence :** `RESEARCH ONLY` / Abandonware officiel maintenu par des miroirs tiers.
- **Taille :** ~15 à 30 GB.
- **Nombre d'exemples/scènes :** 15 663 plans CAD d'architectes réels sous format vectoriel SVG.
- **Modalités :** Vecteurs SVG au niveau primitif (lignes, arcs, polylignes), masques sémantiques et d'instances.
- **Annotations :** Annotations par primitive pour **30 classes d'objets** (28 classes d'instances "things" : portes, fenêtres, tables, sanitaires ; 2 classes de structure "stuff" : murs, parkings).
- **Formats :** SVG, JSON.
- **Réel / synthétique / mixte :** Réel (fichiers CAD d'agences d'architecture réelles).
- **Texte :** Labels sémantiques de symboles.
- **Images :** Rendu vectoriel SVG haute résolution sans pixellisation.
- **Plans :** **100% Plans techniques CAD / DAO**.
- **3D :** Non.
- **RGB-D :** Non.
- **Segmentation :** Oui (panoptique vectorielle exacte).
- **Depth :** Non.
- **Graphes :** Graphe de primitives géométriques.
- **Métadonnées :** Échelles, couches de calques.
- **Disponibilité :** Accessible via le miroir Hugging Face `Voxel51/FloorPlanCAD`.
- **Restrictions :** Projet original arrêté, aucun support officiel.
- **Préprocessing nécessaire :** Conversion SVG -> images haute résolution pour Qwen2-VL, filtrage des plans non résidentiels (certains plans sont des parkings ou des centres commerciaux).
- **Coût stockage estimé :** ~15 GB.
- **Pertinence vision :** Excellente pour le dessin technique pur.
- **Pertinence plan 2D :** Très forte pour la précision du tracé d'architecte.
- **Pertinence spatial :** Forte.
- **Pertinence ergonomie :** Moyenne.
- **Pertinence matériaux :** Faible.
- **Pertinence lumière :** Faible.
- **Pertinence couleur :** Faible (dessin au trait noir et blanc).
- **Pertinence style :** Bâtiments tertiaires et résidentiels contemporains.
- **Pertinence critique :** Faible.
- **Pertinence pédagogie :** Bonne pour l'analyse de plans d'exécution.
- **Pertinence RAG :** Nulle.
- **Pertinence benchmark :** Bon benchmark de détection de symboles techniques.
- **Compatibilité Master Schema :** Bonne (`document_type: plan_2d`).
- **Risque leakage :** Isolation par fichier SVG.
- **Risque doublons :** Faible.
- **Risques licence :** Projet officiel dissous, maintenance floue.
- **Risques qualité :** Faible sur les vecteurs, mais certaines classes non pertinentes pour l'habitat intérieur (parkings souterrains).
- **Difficulté intégration :** Moyenne.
- **Recommandation d'utilisation :** `SECONDARY` (Moins prioritaire que ResPlan et MSD qui possèdent des graphes de connectivité de pièces natifs et des licences CC BY 4.0 limpides).

---

### 22. MLSTRUCT-FP

- **Nom :** MLSTRUCT-FP
- **Catégorie :** Plans Structuraux Haute Résolution pour Bâtiments Résidentiels
- **Source primaire :** https://github.com/MLSTRUCT/MLStructFP
- **Paper :** Publication Universidad de Chile / Dépôt MLSTRUCT (2021-2023).
- **Repository :** https://github.com/MLSTRUCT/MLStructFP
- **Page téléchargement :** Formulaire de demande sur le dépôt GitHub.
- **Licence :** Licence académique de recherche non commerciale.
- **Statut de licence :** Utilisable sous conditions académiques, demande de lien requise.
- **Taille :** ~5 à 10 GB.
- **Nombre d'exemples/scènes :** 954 plans d'étage haute résolution (6 500 à 9 500 pixels de large), issus de 165 projets résidentiels multi-unités conçus par 52 agences d'architecture chiliennes.
- **Modalités :** Images PNG ultra-haute résolution, polygones vectoriels de structures.
- **Annotations :** Murs porteurs, dalles en béton (*slabs*), poteaux, gaines structurelles.
- **Formats :** PNG, JSON, bibliothèque Python dédiée `mlstructfp`.
- **Réel / synthétique / mixte :** Réel (projets d'ingénierie et d'architecture réels).
- **Texte :** Métadonnées de structures, typologies de bâtiment.
- **Images :** Oui, scans/rendus de plans d'ingénierie à très haute résolution.
- **Plans :** Oui, plans axés gros œuvre et structure porteuse.
- **3D :** Non direct (extrusion de dalles possible).
- **RGB-D :** Non.
- **Segmentation :** Oui (polygones JSON des murs et dalles).
- **Depth :** Non.
- **Graphes :** Non.
- **Métadonnées :** Dimensions réelles, agences d'architecture, années de conception.
- **Disponibilité :** Requiert soumission de formulaire en ligne.
- **Restrictions :** Non commercial.
- **Préprocessing nécessaire :** Recadrage et tuilage (images de 9 000 px impossibles à passer directement dans Qwen2-VL sans dépassement de contexte visuel), focalisation sur des zones clés.
- **Coût stockage estimé :** ~8 GB.
- **Pertinence vision :** Excellente pour le détail technique structurel.
- **Pertinence plan 2D :** Forte sur l'aspect gros œuvre/structure, mais absente sur l'aménagement intérieur et le mobilier.
- **Pertinence spatial :** Bonne pour l'enveloppe porteuse.
- **Pertinence ergonomie :** Faible (pas de meubles ni de désignation de pièces fines).
- **Pertinence matériaux :** Bonne sur le béton et la maçonnerie porteuse.
- **Pertinence lumière :** Faible.
- **Pertinence couleur :** Faible.
- **Pertinence style :** Architecture chilienne moderne parasismique.
- **Pertinence critique :** Très forte pour la faisabilité structurelle (murs porteurs non abattables).
- **Pertinence pédagogie :** Excellente pour enseigner la différence entre cloison légère et mur porteur.
- **Pertinence RAG :** Faible.
- **Pertinence benchmark :** Test ciblé de compréhension structurelle.
- **Compatibilité Master Schema :** Bonne (`skills: [PLANS_2D, ESPACE]`).
- **Risque leakage :** Isolation par projet (`scene_id`).
- **Risque doublons :** Faible.
- **Risques licence :** Demande de lien obligatoire.
- **Risques qualité :** Haute qualité d'ingénierie.
- **Difficulté intégration :** Moyenne (gestion de la très haute résolution).
- **Recommandation d'utilisation :** `SECONDARY` (Intéressant pour un module spécialisé "faisabilité et cloisons abattables" en V2, mais secondaire pour l'aménagement d'intérieur V1).

---

### 23. HomeWorld Floorplans

- **Nom :** HomeWorld Floorplans (Sous-composant 2D de HomeWorld)
- **Catégorie :** Corpus Massif de Plans 2D Normalisés par Arbres K-D
- **Source primaire :** https://kairos-homeworld.github.io/
- **Paper :** arXiv:2606.06390 (Section 3 : *Hierarchical Floorplan Representation*).
- **Repository :** https://github.com/Kairos-HomeWorld/HomeWorld
- **Page téléchargement :** Dépôt officiel GitHub (Coming Soon).
- **Licence :** `ACCESS UNCLEAR` (non publiée à cette date).
- **Statut de licence :** Non encore disponible au téléchargement public.
- **Taille :** Estimée à ~20-50 GB pour les 300 000 plans structurés.
- **Nombre d'exemples/scènes :** **300 000 plans d'étage résidentiels réels**.
- **Modalités :** Représentations hiérarchiques K-D Tree, coordonnées polygonales de pièces, étiquettes fonctionnelles.
- **Annotations :** Arbres de découpage spatial binaire, frontières de pièces, connectivité des portes, alignement géométrique.
- **Formats :** JSON (K-D trees), PNG.
- **Réel / synthétique / mixte :** Réel collecté à grande échelle puis filtré par algorithme.
- **Texte :** Prompts d'agencement et étiquettes fonctionnelles.
- **Images :** Plans rasterisés dérivés.
- **Plans :** Oui, 300k plans résidentiels.
- **3D :** Conçu pour être soulevé en 3D dans le framework.
- **RGB-D :** Non.
- **Segmentation :** Oui.
- **Depth :** Non.
- **Graphes :** Graphes hiérarchiques K-D natifs.
- **Métadonnées :** Typologies de maisons complètes.
- **Disponibilité :** **Non disponible immédiatement**.
- **Restrictions :** Inconnues.
- **Préprocessing nécessaire :** Décodage des arbres K-D en plans graphiques conventionnels.
- **Coût stockage estimé :** Variable.
- **Pertinence vision :** Potentiellement majeure.
- **Pertinence plan 2D :** **Majeure** (plus grand corpus structuré existant).
- **Pertinence spatial :** Exceptionnelle.
- **Pertinence ergonomie :** Élevée.
- **Pertinence matériaux :** Faible.
- **Pertinence lumière :** Moyenne.
- **Pertinence couleur :** Faible.
- **Pertinence style :** Diversité mondiale.
- **Pertinence critique :** Bonne.
- **Pertinence pédagogie :** Majeure.
- **Pertinence RAG :** Bonne.
- **Pertinence benchmark :** Futur benchmark de référence.
- **Compatibilité Master Schema :** Excellente.
- **Risque leakage :** Audit obligatoire lors de la publication.
- **Risque doublons :** Inconnu.
- **Risques licence :** Inconnu.
- **Risques qualité :** À vérifier lors de la parution.
- **Difficulté intégration :** Modérée.
- **Recommandation d'utilisation :** `ACCESS UNCLEAR` (Garder en veille stratégique active pour la version V2 d'ARCHI-AI).

---

## Section C : Scènes Synthétiques & Simulation

### 24. CHOrD

- **Nom :** CHOrD (Collision-free, House-scale, and Organized Digital Twins)
- **Catégorie :** Digital Twins d'Habitations Complètes sans Collision
- **Source primaire :** ECCV 2024 / OpenReview (arXiv:2409.xxxxx)
- **Paper :** *"CHOrD: Generation of Collision-free, House-scale, and Organized Digital Twins"*, 2024.
- **Repository :** Code et outils sur GitHub (référencé dans la publication).
- **Page téléchargement :** Liens open-source associés à la parution ECCV.
- **Licence :** Licence de recherche académique standard.
- **Statut de licence :** Utilisable pour la recherche.
- **Taille :** ~35 à 70 GB.
- **Nombre d'exemples/scènes :** **9 706 scènes d'intérieur complètes** à l'échelle de la maison (1,4x plus grand que 3D-FRONT).
- **Modalités :** Plans d'étage 2D, scènes 3D structurées, graphes de scène hiérarchiques, agencements d'objets sans collision.
- **Annotations :** Graphes hiérarchiques (Maison -> Pièce -> Groupe fonctionnel -> Objet), contraintes de dégagement physique.
- **Formats :** JSON (graphes de scène et agencements), OBJ/GLB, PNG.
- **Réel / synthétique / mixte :** Synthétique contrôlé par règles architecturales.
- **Texte :** Métadonnées hiérarchiques de pièces et d'objets.
- **Images :** Rendus 2D d'aménagement.
- **Plans :** Oui, floorplans 2D guidant la génération 3D.
- **3D :** Oui, scènes 3D complètes.
- **RGB-D :** Générable.
- **Segmentation :** Oui.
- **Depth :** Dérivable.
- **Graphes :** **Oui, graphes de scène hiérarchiques explicites**.
- **Métadonnées :** Règles de collision et distances de circulation.
- **Disponibilité :** Disponible via les ressources de publication.
- **Restrictions :** Non commercial.
- **Préprocessing nécessaire :** Rendu de vues intérieures et extraction des paires plan/vue 3D.
- **Coût stockage estimé :** ~40 GB.
- **Pertinence vision :** Bonne.
- **Pertinence plan 2D :** Très bonne.
- **Pertinence spatial :** **Excellente** (résolution mathématique des collisions physiques).
- **Pertinence ergonomie :** **Majeure** (garantie de passages dégagés et d'accessibilité des meubles).
- **Pertinence matériaux :** Moyenne.
- **Pertinence lumière :** Moyenne.
- **Pertinence couleur :** Moyenne.
- **Pertinence style :** Contemporain résidentiel standard.
- **Pertinence critique :** Très bonne pour l'analyse des dégagements.
- **Pertinence pédagogie :** Élevée pour enseigner les règles de circulation.
- **Pertinence RAG :** Bonne.
- **Pertinence benchmark :** Bon benchmark de conformité ergonomique.
- **Compatibilité Master Schema :** Excellente (`skills: [CIRCULATION, ERGONOMIE, ESPACE]`).
- **Risque leakage :** Isolation par scène ID.
- **Risque doublons :** Faible.
- **Risques licence :** Recherche académique.
- **Risques qualité :** Très propre (aucun meuble qui s'interpénètre).
- **Difficulté intégration :** Modérée.
- **Recommandation d'utilisation :** `RELEVANT WITH PREPROCESSING` (Source précieuse pour formuler des règles de non-collision et de circulation ergonomique).

---

### 25. MetaScenes

- **Nom :** MetaScenes
- **Catégorie :** Scènes d'Intérieur Haute Fidélité & Micro-Objets pour EAI
- **Source primaire :** CVPR 2025 (arXiv:2503.xxxxx)
- **Paper :** *"MetaScenes: A Large-scale Simulatable 3D Indoor Scene Dataset"*, CVPR 2025.
- **Repository :** https://github.com/ (référencé dans la publication CVPR)
- **Page téléchargement :** Dépôt officiel du projet / Hugging Face.
- **Licence :** Recherche non commerciale / MIT pour le code.
- **Statut de licence :** Utilisable pour la recherche.
- **Taille :** ~40 à 80 GB.
- **Nombre d'exemples/scènes :** **Rectification factuelle : 706 scènes et 15 366 objets** (contrairement aux ~10k parfois cités de façon imprécise), couvrant 831 catégories d'objets fins.
- **Modalités :** Scènes 3D complètes, objets remplacés par modèles CAO haute fidélité (*Scan2Sim*), descriptions en langage naturel, matrices de transformation physique.
- **Annotations :** Descriptions textuelles d'objets, poses 6D, bounding boxes orientées, annotations multimodales fines.
- **Formats :** USD, GLB, JSON.
- **Réel / synthétique / mixte :** Mixte : géométrie de scan réel avec rétro-ingénierie et remplacement par des assets 3D propres.
- **Texte :** Descriptions d'objets et de petits groupements spatiaux.
- **Images :** Rendus photoréalistes.
- **Plans :** Layouts de scènes.
- **3D :** Oui, très haute qualité géométrique.
- **RGB-D :** Oui.
- **Segmentation :** Oui (très fine, micro-objets).
- **Depth :** Oui.
- **Graphes :** Relations de support (ex: tasse sur table, livre sur étagère).
- **Métadonnées :** Propriétés physiques des objets.
- **Disponibilité :** Disponible publiquement.
- **Restrictions :** Non commercial.
- **Préprocessing nécessaire :** Pipeline de rendu nécessaire pour extraire des images statiques.
- **Coût stockage estimé :** ~45 GB.
- **Pertinence vision :** Excellente sur le détail d'objets.
- **Pertinence plan 2D :** Faible.
- **Pertinence spatial :** Forte sur la micro-échelle (surfaces de pose).
- **Pertinence ergonomie :** Forte pour les objets du quotidien à portée de main.
- **Pertinence matériaux :** Bonne.
- **Pertinence lumière :** Bonne.
- **Pertinence couleur :** Bonne.
- **Pertinence style :** Hétérogène.
- **Pertinence critique :** Moyenne.
- **Pertinence pédagogie :** Faible à moyenne pour l'architecture générale.
- **Pertinence RAG :** Faible.
- **Pertinence benchmark :** Axé manipulation robotique (Micro-Scene Synthesis).
- **Compatibilité Master Schema :** Moyenne.
- **Risque leakage :** Isolation par scène ID.
- **Risque doublons :** Faible.
- **Risques licence :** Recherche non commerciale.
- **Risques qualité :** Très haute qualité d'assets.
- **Difficulté intégration :** Élevée.
- **Recommandation d'utilisation :** `LOW PRIORITY` (Trop focalisé sur les micro-objets de table/étagère pour la vision globale d'architecture intérieure V1).

---

### 26. HSSD — House Scaled Scene Dataset

- **Nom :** HSSD (Habitat Synthetic Scenes Dataset / HSSD-200)
- **Catégorie :** Scènes Résidentielles Synthétiques Auteurées à la Main
- **Source primaire :** https://3dlg-hcvc.github.io/hssd/
- **Paper :** *"Habitat Synthetic Scenes Dataset (HSSD-200): An Analysis of 3D Scene Scale and Realism Tradeoffs for ObjectGoal Navigation"*, Khachatryan et al. (Meta / Simon Fraser Univ.), CVPR 2023.
- **Repository :** GitHub officiel 3DLG-HCVC.
- **Page téléchargement :** https://huggingface.co/datasets/hssd/hssd-models et `hssd/hssd-hab`
- **Licence :** **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.
- **Statut de licence :** Utilisable sous conditions de recherche non commerciale (accord à valider sur Hugging Face).
- **Taille :** ~30 à 50 GB.
- **Nombre d'exemples/scènes :** **211 scènes complètes de maisons**, plus de 18 000 modèles 3D individuels fidèles aux dimensions réelles.
- **Modalités :** Scènes 3D au format GLB/USD, scènes compatibles Habitat-Sim, floorplans 2D précis, annotations d'objets.
- **Annotations :** Modèles 3D créés par des artistes 3D professionnels respectant scrupuleusement les proportions architecturales humaines, catégories sémantiques strictes.
- **Formats :** GLB, JSON, NAVMESH.
- **Réel / synthétique / mixte :** Synthétique d'artiste (conception humaine experte, pas de bruit procédural).
- **Texte :** Labels d'objets normalisés.
- **Images :** Rendus via Habitat-Sim.
- **Plans :** Oui, plans d'étage d'architecte associés à chaque maison.
- **3D :** Oui, modèles de maison entière d'une grande pureté géométrique.
- **RGB-D :** Générable.
- **Segmentation :** Oui (instance 3D propre).
- **Depth :** Dérivable.
- **Graphes :** Graphe de navigation et d'adjacence de pièces.
- **Métadonnées :** Dimensions exactes des meubles du commerce.
- **Disponibilité :** Active sur Hugging Face.
- **Restrictions :** Non commercial (CC BY-NC 4.0).
- **Préprocessing nécessaire :** Rendu de quelques vues clés représentatives par scène via Blender ou Habitat-Sim.
- **Coût stockage estimé :** ~35 GB.
- **Pertinence vision :** Excellente (qualité de modélisation irréprochable).
- **Pertinence plan 2D :** Très bonne.
- **Pertinence spatial :** **Majeure** (proportions humaines réalistes, pas d'objets disproportionnés).
- **Pertinence ergonomie :** **Exceptionnelle** (les concepteurs 3D ont respecté les gabarits réels de passage).
- **Pertinence matériaux :** Bonne.
- **Pertinence lumière :** Bonne.
- **Pertinence couleur :** Bonne.
- **Pertinence style :** Résidentiel contemporain soigné.
- **Pertinence critique :** Bonne.
- **Pertinence pédagogie :** Forte.
- **Pertinence RAG :** Faible.
- **Pertinence benchmark :** Excellent benchmark de raisonnement spatial.
- **Compatibilité Master Schema :** Excellente.
- **Risque leakage :** 211 maisons uniques : split facile et étanche par maison.
- **Risque doublons :** Nul.
- **Risques licence :** Non commercial (CC BY-NC 4.0).
- **Risques qualité :** Qualité maximale (modélisation manuelle par des professionnels).
- **Difficulté intégration :** Modérée (nécessite un script de rendu pour obtenir les images PNG).
- **Recommandation d'utilisation :** `RELEVANT WITH PREPROCESSING` (Excellente référence de vérité terrain sur les proportions réalistes de mobilier).

---

## Section D : Image + Texte & Interior Design

### 27. iDesigner

- **Nom :** iDesigner
- **Catégorie :** Modèle de Diffusion & Données d'Intérieur
- **Source primaire :** arXiv:2312.04326v2
- **Paper :** *"iDesigner: A High-Resolution and Complex-Prompt Following Text-to-Image Diffusion Model for Interior Design"*, Wang et al., Décembre 2023.
- **Repository :** Aucun dépôt officiel public de dataset.
- **Page téléchargement :** Aucune page de téléchargement public de dataset trouvée sur Hugging Face ou GitHub.
- **Licence :** Non applicable (données non publiées).
- **Statut de licence :** `NOT APPLICABLE` / Dataset propriétaire interne non diffusé.
- **Taille :** Non disponible.
- **Nombre d'exemples/scènes :** Dataset propriétaire utilisé pour fine-tuner un modèle de diffusion.
- **Modalités :** Paires texte-image spécialisées en design d'intérieur bilingues (anglais/chinois).
- **Annotations :** Prompts descriptifs d'ambiances intérieures.
- **Formats :** Inconnu.
- **Réel / synthétique / mixte :** Inconnu (scraping web et rendus).
- **Texte :** Prompts complexes d'architecture intérieure.
- **Images :** Rendus et photos haute définition.
- **Plans :** Non.
- **3D :** Non.
- **RGB-D :** Non.
- **Segmentation :** Non.
- **Depth :** Non.
- **Graphes :** Non.
- **Métadonnées :** Styles et ambiances.
- **Disponibilité :** **Non disponible au public.** Seul le papier scientifique est accessible.
- **Restrictions :** Propriétaire.
- **Préprocessing nécessaire :** N/A.
- **Coût stockage estimé :** 0 GB.
- **Pertinence vision :** N/A.
- **Pertinence plan 2D :** Nulle.
- **Pertinence spatial :** N/A.
- **Pertinence ergonomie :** N/A.
- **Pertinence matériaux :** N/A.
- **Pertinence lumière :** N/A.
- **Pertinence couleur :** N/A.
- **Pertinence style :** Forte dans le concept du papier.
- **Pertinence critique :** Nulle.
- **Pertinence pédagogie :** Nulle.
- **Pertinence RAG :** Inspirations de prompts dans le papier.
- **Pertinence benchmark :** N/A.
- **Compatibilité Master Schema :** N/A.
- **Risque leakage :** N/A.
- **Risque doublons :** N/A.
- **Risques licence :** N/A.
- **Risques qualité :** N/A.
- **Difficulté intégration :** Impossible.
- **Recommandation d'utilisation :** `NOT RECOMMENDED` (Dataset non publié ; aucune donnée exploitable).

---

### 28. MMIS — Multimodal Interior Scenes

- **Nom :** MMIS (Multimodal Dataset for Interior Scene Visual Generation and Recognition)
- **Catégorie :** Corpus Image + Texte + Audio Spécialisé en Styles d'Intérieur
- **Source primaire :** arXiv:2407.05980 (Juillet 2024)
- **Paper :** *"MMIS: Multimodal Dataset for Interior Scene Visual Generation and Recognition"*, Kassab et al., 2024.
- **Repository :** https://github.com/AhmedMahmoudMostafa/MMIS
- **Page téléchargement :** Dépôt GitHub officiel (scripts de téléchargement et métadonnées).
- **Licence :** **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.
- **Statut de licence :** Utilisable pour l'entraînement avec partage à l'identique et attribution.
- **Taille :** ~45 à 80 GB (selon inclusion des fichiers audio).
- **Nombre d'exemples/scènes :** **~160 000 images d'intérieur**, chacune appariée à une description textuelle et un enregistrement audio de cette description.
- **Modalités :** Images photographiques d'intérieur, légendes textuelles détaillées, pistes audio correspondantes.
- **Annotations :** Structuration en **40 styles d'architecture d'intérieur** (Scandinave, Industriel, Bohème, Minimaliste, Art Déco, Japandi, Rustique, etc.) croisés avec **5 typologies de pièces** :
  1. Salon (*Living room*)
  2. Chambre (*Bedroom*)
  3. Salle à manger (*Dining room*)
  4. Salle de bains (*Bathroom*)
  5. Cuisine (*Kitchen*)
- **Formats :** JPG, TXT/JSON, WAV.
- **Réel / synthétique / mixte :** Réel photographique (collecte et labellisation experte).
- **Texte :** **Descriptions textuelles d'ambiances et d'éléments stylistiques explicites**.
- **Images :** Oui, 160 000 photographies d'architecture intérieure.
- **Plans :** Non.
- **3D :** Non.
- **RGB-D :** Non.
- **Segmentation :** Non.
- **Depth :** Non.
- **Graphes :** Non.
- **Métadonnées :** Style précis, type de pièce, descriptions verbales.
- **Disponibilité :** Active sur GitHub.
- **Restrictions :** Contrainte ShareAlike (CC BY-SA 4.0).
- **Préprocessing nécessaire :** Ignorer les fichiers audio (inutiles pour Qwen2-VL), filtrer les images de faible résolution, aligner les descriptions textuelles avec le vocabulaire de styles d'ARCHI-AI.
- **Coût stockage estimé :** ~35 GB (images seules sans audio).
- **Pertinence vision :** **Excellente pour la reconnaissance visuelle d'intérieurs**.
- **Pertinence plan 2D :** Nulle.
- **Pertinence spatial :** Moyenne.
- **Pertinence ergonomie :** Faible à moyenne.
- **Pertinence matériaux :** **Très forte** (textures, bois, métaux, tissus décrits dans le texte).
- **Pertinence lumière :** Bonne (ambiances lumineuses variées).
- **Pertinence couleur :** **Très forte** (palettes de couleurs associées aux styles).
- **Pertinence style :** **Majeure / Référence** (40 styles d'intérieur formellement étiquetés).
- **Pertinence critique :** Bonne.
- **Pertinence pédagogie :** Excellente pour le module STYLE et COULEUR.
- **Pertinence RAG :** **Très forte** (lexique et descriptions stylistiques réutilisables).
- **Pertinence benchmark :** Idéal pour évaluer la capacité du modèle à classifier et expliquer un style décoratif.
- **Compatibilité Master Schema :** Excellente (`document_type: photography`, `domain: interior_design`, `skills: [STYLE, MATERIAUX, COULEUR, MOBILIER]`).
- **Risque leakage :** Risque de redondance web : déduplication SHA-256 et pHash obligatoire.
- **Risque doublons :** Moyen (images de Pinterest/agences).
- **Risques licence :** Obligation ShareAlike (SA).
- **Risques qualité :** Faible à moyen (vérifier la précision des 40 classes).
- **Difficulté intégration :** Faible (paires image-texte directes).
- **Recommandation d'utilisation :** `DIRECTLY RELEVANT` (La source la plus riche et la mieux structurée pour enseigner les 40 styles d'intérieur et leurs matériaux à Qwen2-VL).

---

### 29. Rooms-with-Text

- **Nom :** Rooms-with-Text
- **Catégorie :** Détection de Texte Superposé & Watermarks (Vision OCR)
- **Source primaire :** arXiv:2211.11350 / ECCV 2022 Workshop ("Text in Everything")
- **Paper :** *"Rooms with Text: A Dataset for Overlaying Text Detection"*, Smirnov & Tewari, Novembre 2022.
- **Repository :** https://github.com/HCIILAB/Scene-Text-Recognition
- **Page téléchargement :** Liens dans le dépôt GitHub.
- **Licence :** Recherche académique.
- **Statut de licence :** Utilisable pour la recherche.
- **Taille :** ~2 à 4 GB.
- **Nombre d'exemples/scènes :** 4 836 images d'intérieurs annotées.
- **Modalités :** Images avec détection de texte incrusté (filigranes d'agences, logos, dates, bannières publicitaires) et texte dans la scène (posters, couvertures de livres).
- **Annotations :** Boîtes englobantes de texte superposé (*overlay text*).
- **Formats :** JPG, JSON (bounding boxes de texte).
- **Réel / synthétique / mixte :** Réel.
- **Texte :** **Attention : le texte n'est PAS une description architecturale**, ce sont des transcriptions de filigranes ou d'incrustations graphiques.
- **Images :** Photos de pièces d'habitation.
- **Plans :** Non.
- **3D :** Non.
- **RGB-D :** Non.
- **Segmentation :** Masques de texte.
- **Depth :** Non.
- **Graphes :** Non.
- **Métadonnées :** Type d'incrustation.
- **Disponibilité :** Active.
- **Restrictions :** Recherche.
- **Préprocessing nécessaire :** N/A pour l'architecture.
- **Coût stockage estimé :** ~3 GB.
- **Pertinence vision :** Non pertinente pour l'architecture.
- **Pertinence plan 2D :** Nulle.
- **Pertinence spatial :** Nulle.
- **Pertinence ergonomie :** Nulle.
- **Pertinence matériaux :** Nulle.
- **Pertinence lumière :** Nulle.
- **Pertinence couleur :** Nulle.
- **Pertinence style :** Nulle.
- **Pertinence critique :** Nulle.
- **Pertinence pédagogie :** Nulle.
- **Pertinence RAG :** Nulle.
- **Pertinence benchmark :** Utile uniquement pour tester la robustesse aux watermarks.
- **Compatibilité Master Schema :** Incompatible (aucun contenu métier).
- **Risque leakage :** N/A.
- **Risque doublons :** N/A.
- **Risques licence :** N/A.
- **Risques qualité :** Hors sujet architectural.
- **Difficulté intégration :** N/A.
- **Recommandation d'utilisation :** `NOT RECOMMENDED` (**Désillusion d'audit majeure :** Malgré son nom trompeur, ce dataset ne contient aucune description d'architecture, mais sert exclusivement à l'OCR et à la détection de filigranes graphiques).

---

### 30. 360SpatialAI

- **Nom :** 360SpatialAI
- **Catégorie :** Application Web & Prototype de Recherche pour Panoramas 360
- **Source primaire :** eCAADe 2025 (43rd Conference on Education and Research in CAAD in Europe), Ankara, Turquie.
- **Paper :** *"Development of 360SpatialAI: Indoor spatial information extraction and management web app based on 360 image and AI technology"*, Kim, Lee & Kim (Yonsei University), Septembre 2025 (Ref: `ecaade2025_407`).
- **Repository :** Aucun dépôt open-source public de dataset complet.
- **Page téléchargement :** Non disponible sous forme de dataset téléchargeable.
- **Licence :** Droits réservés aux auteurs / eCAADe proceedings.
- **Statut de licence :** `ACCESS UNCLEAR` / Prototype académique non distribué en open-data.
- **Taille :** Non applicable (~1 600 paires d'images de test interne à l'Université Yonsei).
- **Nombre d'exemples/scènes :** 1 600 paires image-texte produites lors d'une étude de cas pilote.
- **Modalités :** Panoramas 360 découpés en vues perspectives sphériques, descriptions d'espaces générées par LLM, déclinaisons générées via ComfyUI.
- **Annotations :** Descriptions d'occupation, de matériaux et de style.
- **Formats :** Prototype web applicatif.
- **Réel / synthétique / mixte :** Mixte.
- **Texte :** Descriptions d'intérieurs générées par pipeline multimodal.
- **Images :** Panoramas 360 et vues perspectives.
- **Plans :** Non.
- **3D :** Non direct.
- **RGB-D :** Non.
- **Segmentation :** Non.
- **Depth :** Non.
- **Graphes :** Non.
- **Métadonnées :** Paramètres d'analyse d'espace.
- **Disponibilité :** **Non disponible au téléchargement.** Il s'agit d'un article de conférence décrivant une application web interne, et non d'une ressource de données ouverte.
- **Restrictions :** N/A.
- **Préprocessing nécessaire :** N/A.
- **Coût stockage estimé :** 0 GB.
- **Pertinence vision :** Conceptuelle.
- **Pertinence plan 2D :** Nulle.
- **Pertinence spatial :** Intéressante méthodologiquement (découpage panorama 360 -> perspectives).
- **Pertinence ergonomie :** Faible.
- **Pertinence matériaux :** Moyenne.
- **Pertinence lumière :** Moyenne.
- **Pertinence couleur :** Moyenne.
- **Pertinence style :** Moyenne.
- **Pertinence critique :** Faible.
- **Pertinence pédagogie :** Bonne méthodologie pour notre propre pipeline futur.
- **Pertinence RAG :** Faible.
- **Pertinence benchmark :** N/A.
- **Compatibilité Master Schema :** N/A.
- **Risque leakage :** N/A.
- **Risque doublons :** N/A.
- **Risques licence :** N/A.
- **Risques qualité :** N/A.
- **Difficulté intégration :** Impossible.
- **Recommandation d'utilisation :** `NOT RECOMMENDED` (Article méthodologique très intéressant à citer dans la documentation d'architecture système, mais aucun dataset téléchargeable n'existe).

---

### 31. Kaggle interior_design

- **Nom :** Kaggle interior_design (`aishahsofea/interior-design`)
- **Catégorie :** Collection d'Images d'Intérieur Scrapées Basse Résolution
- **Source primaire :** Kaggle (`aishahsofea/interior-design`)
- **Paper :** Aucun paper officiel (utilisé ponctuellement dans des articles sur les filigranes numériques).
- **Repository :** N/A (compte utilisateur Kaggle personnel).
- **Page téléchargement :** https://www.kaggle.com/datasets/aishahsofea/interior-design
- **Licence :** "Unknown" / Données scrapées sur internet sans cession de droits.
- **Statut de licence :** `LICENSE UNCLEAR` / Risque juridique élevé d'images sous copyright non libre.
- **Taille :** ~150 à 250 MB.
- **Nombre d'exemples/scènes :** 4 147 images.
- **Modalités :** Images JPG basse résolution (256x256 pixels).
- **Annotations :** **Aucune annotation textuelle, aucune catégorie, aucun label.**
- **Formats :** JPG.
- **Réel / synthétique / mixte :** Réel (scraping web de photos de décoration).
- **Texte :** Aucun.
- **Images :** Oui, 4 147 petites vignettes (256x256 px).
- **Plans :** Non.
- **3D :** Non.
- **RGB-D :** Non.
- **Segmentation :** Non.
- **Depth :** Non.
- **Graphes :** Non.
- **Métadonnées :** Aucune.
- **Disponibilité :** Active sur Kaggle.
- **Restrictions :** Droits d'auteur inconnus.
- **Préprocessing nécessaire :** Tout est à créer (aucun texte d'accompagnement).
- **Coût stockage estimé :** ~0,3 GB.
- **Pertinence vision :** **Très faible** : la résolution 256x256 est dramatiquement insuffisante pour Qwen2-VL, qui nécessite de discerner les détails de textures et d'assemblages.
- **Pertinence plan 2D :** Nulle.
- **Pertinence spatial :** Faible.
- **Pertinence ergonomie :** Nulle.
- **Pertinence matériaux :** Inexploitable à 256x256 (flou de pixelisation).
- **Pertinence lumière :** Faible.
- **Pertinence couleur :** Moyenne.
- **Pertinence style :** Non annoté.
- **Pertinence critique :** Nulle.
- **Pertinence pédagogie :** Nulle.
- **Pertinence RAG :** Nulle.
- **Pertinence benchmark :** Inadapté.
- **Compatibilité Master Schema :** Très faible.
- **Risque leakage :** Incontrôlable.
- **Risque doublons :** Fort.
- **Risques licence :** Élevé.
- **Risques qualité :** Résolution obsolète indigne d'un modèle VLM 2026.
- **Difficulté intégration :** Faible techniquement, mais travail d'annotation complet à réaliser pour une valeur dérisoire.
- **Recommandation d'utilisation :** `NOT RECOMMENDED` (Qualité d'image trop basse, aucune annotation, aucun intérêt face à MMIS ou Structured3D).

---

### 32. rrustom/architecture2022clean

- **Nom :** rrustom/architecture2022clean
- **Catégorie :** Banque d'Images Architecturales pour Modèles de Diffusion
- **Source primaire :** Hugging Face (`rrustom/architecture2022clean`)
- **Paper :** Lié au modèle de diffusion `rrustom/stable-architecture-diffusers`.
- **Repository :** Hugging Face Datasets.
- **Page téléchargement :** https://huggingface.co/datasets/rrustom/architecture2022clean
- **Licence :** "Not specified" / Non enregistrée sur Hugging Face.
- **Statut de licence :** `LICENSE UNCLEAR`.
- **Taille :** **566 MB**.
- **Nombre d'exemples/scènes :** **2 415 images**.
- **Modalités :** Images JPG/PNG stockées en Parquet, métadonnées textuelles très sommaires.
- **Annotations :** Quelques légendes ou prompts de conditionnement diffusion courts (souvent un mot ou une phrase vague du type "modern exterior facade").
- **Formats :** Parquet, JPG.
- **Réel / synthétique / mixte :** Mixte (photos de bâtiments réels et rendus conceptuels Midjourney/Stable Diffusion mélangés).
- **Texte :** Prompts très courts et imprécis.
- **Images :** Oui, 2 415 images d'architecture extérieure et intérieure.
- **Plans :** Non.
- **3D :** Non.
- **RGB-D :** Non.
- **Segmentation :** Non.
- **Depth :** Non.
- **Graphes :** Non.
- **Métadonnées :** Identifiant d'image, prompt diffusion.
- **Disponibilité :** Active sur Hugging Face.
- **Restrictions :** Licence non spécifiée.
- **Préprocessing nécessaire :** Extraction du Parquet, tri des images intérieures vs extérieures.
- **Coût stockage estimé :** ~0,6 GB.
- **Pertinence vision :** Moyenne (mélange photos et générations IA sans label distinctif).
- **Pertinence plan 2D :** Nulle.
- **Pertinence spatial :** Faible.
- **Pertinence ergonomie :** Nulle.
- **Pertinence matériaux :** Moyenne.
- **Pertinence lumière :** Moyenne.
- **Pertinence couleur :** Moyenne.
- **Pertinence style :** Hétéroclite et non rigoureux.
- **Pertinence critique :** Nulle.
- **Pertinence pédagogie :** Nulle.
- **Pertinence RAG :** Nulle.
- **Pertinence benchmark :** Inadapté.
- **Compatibilité Master Schema :** Faible.
- **Risque leakage :** Présence d'images synthétiques non documentées pouvant corrompre la fidélité architecturale.
- **Risque doublons :** Moyen.
- **Risques licence :** Indéterminé.
- **Risques qualité :** Présence d'artefacts d'images générées par d'anciennes versions de Stable Diffusion.
- **Difficulté intégration :** Faible.
- **Recommandation d'utilisation :** `LOW PRIORITY` / `NOT RECOMMENDED FOR V1` (Volume trop faible, absence d'annotations expertes, mélange d'extérieurs et d'intérieurs non triés).

---

## Section E : Répertoires & Candidats Additionnels

### 33. DataDrivenAEC & Additional Candidates

- **Nom :** DataDrivenAEC (Répertoire d'annuaires de données AEC)
- **Source primaire :** https://datadrivenaec.com/datasets
- **Nature :** Annuaire spécialisé recensant 129 datasets et ressources pour l'Architecture, l'Ingénierie et la Construction (AEC).
- **Audit des catégories pertinentes :** Analyse ciblée sur les filtres *interior, floorplan, indoor, BIM, CAD, architecture, spatial, material, lighting, furniture*.

#### Candidats Additionnels Identifiés (`ADDITIONAL_CANDIDATES`)

À l'issue du criblage des 129 ressources de DataDrivenAEC, trois datasets émergent avec une valeur stratégique majeure pour ARCHI-AI (sans qu'aucun téléchargement n'ait été effectué) :

#### Candidat 1 : ZInD (Zillow Indoor Dataset)
- **Origine :** Zillow Research / CVPR 2021.
- **Contenu :** 71 474 panoramas d'intérieurs réels non meublés provenant de 1 524 maisons américaines réelles, accompagnés de **plans d'étage 2D et 3D complets alignés**.
- **Licence :** Non commerciale recherche Zillow.
- **Intérêt ARCHI-AI :** Exceptionnel pour la relation directe entre plan 2D et volume vide d'une vraie maison.
- **Statut recommandé :** `SECONDARY CANDIDATE` (À évaluer pour V2).

#### Candidat 2 : BIM/IFC Domain Knowledge QA
- **Origine :** Dépôts de recherche en Traitement Automatique du Langage appliqué au BIM (Tongji / TU Munich).
- **Contenu :** 13 485 paires de questions/réponses textuelles spécialisées sur les normes architecturales, le schéma IFC, la conformité réglementaire et la terminologie du bâtiment.
- **Licence :** Open-access recherche.
- **Intérêt ARCHI-AI :** **Valeur majeure pour le RAG**. Permet d'alimenter immédiatement la base documentaire d'ARCHI-AI avec du savoir normatif expert et des règles constructives sans aucun coût visuel.
- **Statut recommandé :** `DIRECTLY RELEVANT (RAG ONLY)`.

#### Candidat 3 : DrawScript
- **Origine :** Recherche en grammaire de forme algorithmique.
- **Contenu :** 71 334 plans architecturaux générés par programmation visuelle avec règles de distribution spatiales strictes.
- **Licence :** Open-source.
- **Intérêt ARCHI-AI :** Utile pour l'augmentation de données synthétiques sur la logique de distribution.
- **Statut recommandé :** `SECONDARY CANDIDATE`.

---

## Section F : Données Métier

### 34. Interior Design Trends 2026

- **Nom :** The 2026 Interior Design Survey: Costs, Trends and Client Expectations
- **Catégorie :** Enquête Métier / Données d'Opinion Professionnelle
- **Source primaire :** https://www.myarchitectai.com/research/interior-design-trends-2026
- **Éditeur :** MyArchitectAI (mars 2026).
- **Méthodologie vérifiée :**
  - **Taille réelle de l'échantillon : 74 répondants seulement** (professionnels du design d'intérieur auto-sélectionnés via la liste email du site).
  - Échantillonnage d'opportunité (non représentatif au sens statistique formel).
  - Format disponible : Téléchargement direct d'un tableau CSV de synthèse des réponses.
- **Licence :** Libre citation avec attribution à MyArchitectAI ("Journalists, researchers, and institutions are welcome to cite the findings").
- **Statut de licence :** Utilisable pour l'analyse et la citation.
- **Taille :** ~50 Ko (fichier CSV léger).
- **Contenu factuel :**
  - Préférences déclarées des clients en 2026 : cuisines ouvertes (*open-concept*) à 59%, espaces flexibles/bureau à 38%, dressings à 36%, buanderies et vestiaires (*mudrooms*) en forte hausse.
  - Tendances jugées éphémères par les professionnels : maximalisme outrancier (35%), cuisines intégralement blanches minimalistes (24%).
  - Réticence envers les hubs domotiques connectés complexes (obsolescence rapide perçue).
  - Montée en puissance de l'assistance par IA dans les phases préliminaires de décoration.
- **Évaluation critique pour ARCHI-AI :**
  - **Valeur pour l'entraînement ML : NULLE.** Un échantillon de 74 avis subjectifs ne constitue en aucun cas un corpus d'apprentissage. Entraîner un modèle sur ces pourcentages créerait un surapprentissage immédiat sur des opinions de court terme.
  - **Valeur pour le RAG : MOYENNE À BONNE.** Peut servir de document contextuel daté (*"Selon l'enquête MyArchitectAI 2026 auprès de 74 professionnels, les cuisines ouvertes demeurent plébiscitées à 59% malgré les critiques stylistiques"*).
  - **Risques :** Confusion entre tendances marketing éphémères et principes intemporels d'architecture (lumière, proportion, circulation).
- **Recommandation d'utilisation :** `RAG ONLY` (Intégrer comme document de contexte temporel dans la base de connaissances, mais **interdiction absolue de l'inclure dans les splits d'entraînement VLM**).

---
*Fin du document d'audit détaillé.*
