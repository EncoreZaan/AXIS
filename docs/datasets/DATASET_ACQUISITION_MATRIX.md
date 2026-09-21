# ARCHI-AI — Matrice Complète d'Acquisition des Données (`DATASET_ACQUISITION_MATRIX`)

Cette matrice détaille l'état de validation, la qualification juridique, le dimensionnement et le statut d'acquisition pour chacune des 52 sources auditées dans le projet ARCHI-AI.

| # | Nom de la Source | Domaine ARCHI-AI | Licence Officielle Vérifiée | Usage Commercial | Catégorie Juridique | Priorité | Taille Estimée / Réelle | Format Réel | Modalités | Statut Acquisition | Emplacement Local / Destination |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **01** | **IL3D** | 3D / Spatial | Apache-2.0 | Autorisé | `CORE` | **P0** | 72,1 Mo (Layouts) | ZIP, JSON | Boîtes 3D, Layouts, Texte | **ACQUIS & VÉRIFIÉ** | `core/il3d/` |
| **02** | **StructScan3D** | Construction / Enveloppe | CC-BY-4.0 | Autorisé | `CORE` | **P0** | 379,2 Mo | PNG, TXT | RGB, Depth, Masques structure | **ACQUIS & VÉRIFIÉ** | `core/structscan3d/` |
| **03** | **ResPlan** | Floorplans 2D | CC BY 4.0 / MIT | Autorisé | `CORE` | **P0** | 95,7 Mo (Archive) | ZIP, PKL, JSON | Vecteurs, Graphes, Métrique | **ACQUIS & VÉRIFIÉ** | `core/resplan/` |
| **04** | **Modified Swiss Dwellings (MSD)** | Floorplans Collectifs | CC-BY-4.0 | Autorisé | `CORE` | **P1** | ~1,2 Go | PKL, PNG, JSON | Graphes NetworkX, Rasters | Planifié V1 | `core/msd/` |
| **05** | **MatSynth** | Matériaux PBR | CC0 (Public Domain) | Autorisé | `CORE` | **P1** | ~2,5 Go (Échantillon) | Parquet | Textures PBR 4K, Descriptions | Planifié Échantillon | `core/matsynth/` |
| **06** | **ambientCG** | Matériaux PBR | CC0 (Public Domain) | Autorisé | `CORE` | **P0** | 0,7 Mo (Catalogue) | JSON, WebP | Taxonomie, Paramètres PBR | **ACQUIS & VÉRIFIÉ** | `core/materials/ambientcg/` |
| **07** | **ArchCAD-400K** | CAD / Symboles | Academic License | **Interdit** | `RESEARCH / ISOLATED` | **P1** | ~1,8 Go | JSON, SVG | Primitives CAD, Symboles | Reclassé (Exclu Core) | `research_isolated/archcad/` |
| **08** | **FloorPlanCAD** | CAD / Symboles | CC-BY-SA-4.0 | Autorisé | `CORE` | **P1** | 32,5 Mo | PNG, JSON | Dessins CAD, Détections | **ACQUIS & VÉRIFIÉ** | `core/floorplancad/` |
| **09** | **IFC-Bench V2** | BIM / IFC QA | CC-BY-4.0 | Autorisé | `CORE` | **P0** | 1 978,7 Mo | IFC, PNG, CSV | Maquettes 3D, Snapshots, QA | **ACQUIS & VÉRIFIÉ** | `core/bim_ifc/ifc_bench/` |
| **10** | **ResBIM-IFC** | 2D ↔ BIM / IFC | MIT | Autorisé | `CORE` | **P1** | 11,7 Mo (Échantillon) | JPG, IFC | Plans 2D, Maquettes 3D IFC | **ACQUIS & VÉRIFIÉ** | `core/resbim/` |
| **11** | **The Met Open Access** | Histoire du Design & Mobilier | CC0-1.0 (Public Domain) | Autorisé | `CORE` | **P0** | 302,9 Mo | CSV | Métadonnées, Époques, Styles | **ACQUIS & VÉRIFIÉ** | `core/design_history/met/` |
| **12** | **Cooper Hewitt API** | Histoire du Design | CC0-1.0 (Public Domain) | Autorisé | `CORE` | **P1** | ~1,1 Go | JSON | Monographies, Objets design | Planifié P1 | `core/design_history/cooperhewitt/` |
| **13** | **Légifrance (CCH, PMR, ERP)** | Normes & Réglementation | Licence Ouverte | Autorisé | `CORE` | **P0** | ~0,01 Mo | Markdown | Textes de lois consolidés | **ACQUIS & VÉRIFIÉ** | `core/normes_fr/` |
| **14** | **Cerema Guides Accessibilité** | Normes & Accessibilité | Licence Ouverte | Autorisé | `CORE` | **P0** | ~0,01 Mo | Markdown | Règles pratiques d'usage | **ACQUIS & VÉRIFIÉ** | `core/normes_fr/` |
| **15** | **Structured3D** | 3D / Spatial | Academic EULA | Interdit | `RESEARCH / ISOLATED` | **P1** | ~15 Go | PNG, OBJ, JSON | Panos, Wireframes, Vide/Meublé | Réservé Holdout | `research_isolated/structured3d/` |
| **16** | **M3DLayout** | 3D / Spatial | CC-BY-NC-4.0 | Interdit | `RESEARCH / ISOLATED` | **P1** | ~25 Go | JSON, NPY | Hiérarchies de pièces, Boîtes | Réservé Holdout | `research_isolated/m3dlayout/` |
| **17** | **InternScenes** | 3D / Embodied | CC-BY-NC-SA-4.0 | Interdit | `RESEARCH / ISOLATED` | **P2** | >100 Go | USD, GLB | Simulation physique, Scènes | Gated HF | `research_isolated/internscenes/` |
| **18** | **MMIS** | Styles d'intérieur | Non déclarée (Drive) | Inconnu | `UNKNOWN` | **P3** | ~35 Go | JPG, WAV, TXT | Images, Audio, Prompts | Écarté de Core | Bloqué (Risque Juridique) |
| **19** | **CubiCasa5K** | Floorplans Réels | CC-BY-NC-SA-4.0 | Interdit | `RESEARCH / ISOLATED` | **P1** | ~5,09 Go | SVG, PNG | Plans scannés, Cotations | Réservé Holdout | `research_isolated/cubicasa5k/` |
| **20** | **Matterport3D** | Scans 3D Réels | Matterport EULA | Interdit | `RESEARCH / ISOLATED` | **P2** | ~50 Go | OBJ, JPG | Scans d'habitations entières | Accès Gated | Scellé Benchmark |
| **21** | **HM3D & HM3D Semantics** | Scans 3D Réels | Matterport EULA | Interdit | `RESEARCH / ISOLATED` | **P2** | ~80 Go | GLB, OBJ | Scans Matterport sous Habitat | Accès Gated | Scellé Benchmark |
| **22** | **SpatialGen-Bench** | Évaluation Spatiale | Academic License | Interdit | `RESEARCH / ISOLATED` | **P1** | ~92 Mo | JSONL, PNG | Paires multi-vues, Tests VLM | Benchmark Seul | `research_isolated/spatialgen_bench/` |
| **23** | **InteriorGS** | Rendu Immersif 3DGS | Manycore Terms | Interdit | `RESEARCH / ISOLATED` | **P2** | ~35 Go | PLY, JSON | Gaussian Splatting, Occupancy | Réservé Recherche | `research_isolated/interiorgs/` |
| **24** | **HomeWorld & Floorplans** | Simulation Intérieure | Non publié (Empty) | Inconnu | `BLOCKED` | **P3** | — | — | Dépôt officiel vide | Non disponible | Attente publication |
| **25** | **InteriorNet** | 3D / Photoréalisme | Propriétaire (Mort) | Interdit | `BLOCKED` | **P3** | — | — | Liens inaccessibles | Abandonné | Écarté définitivement |
| **26** | **OpenRooms** | Éclairage Intérieur | CC-BY-NC-4.0 | Interdit | `RESEARCH / ISOLATED` | **P2** | ~60 Go | HDR, PNG | Albédo, Rugosité, Luminaires | Réservé Recherche | `research_isolated/openrooms/` |
| **27** | **Laval Photometric HDR** | Éclairage Calibré | Academic Terms | Interdit | `RESEARCH / ISOLATED` | **P2** | ~10 Go | HDR | Panoramas photométriques | Needs Auth | Réservé Recherche |
| **28** | **ARKitScenes** | Scans iPad LiDAR | Apple License | Sous condition | `RESEARCH / ISOLATED` | **P2** | ~40 Go | PLY, MP4 | Scans lidar iPad de pièces | Réservé Recherche | `research_isolated/arkitscenes/` |
| **29** | **HSSD (hssd-hab)** | Scènes d'Habitations | CC-BY-NC-4.0 | Interdit | `RESEARCH / ISOLATED` | **P2** | ~15 Go | GLB, JSON | Scènes réalistes calibrées | Réservé Recherche | `research_isolated/hssd/` |
| **30** | **CHOrD** | Ergonomie / Mobilité | Recherche académique | Interdit | `RESEARCH / ISOLATED` | **P2** | ~8 Go | JSON, OBJ | Interactions objets/humains | Réservé Recherche | `research_isolated/chord/` |
| **31** | **MetaScenes** | Scènes 3D | CC-BY-NC-4.0 | Interdit | `RESEARCH / ISOLATED` | **P3** | ~20 Go | OBJ, JSON | Assets et poses 6D | Écarté (Redondant) | `research_isolated/metascenes/` |
| **32** | **SmartScenes (SSTK)** | Boîtes à outils | MIT (Tainted SUNCG) | Risqué | `BLOCKED` | **P3** | — | JS, Python | Outils (SUNCG litigieux) | Écarté | Écarté définitivement |
| **33** | **BRIDGE** | CAD + Texte | Inconnue (Web) | Inconnu | `UNKNOWN` | **P3** | ~2 Go | PNG, TXT | Dessins CAD + descriptions | Non vérifié | Écarté de Core |
| **34** | **MLSTRUCT-FP** | Éléments Porteurs | Recherche académique | Interdit | `RESEARCH / ISOLATED` | **P2** | ~12 Go | PNG, JSON | Poteaux, poutres, dalles | Needs Form Auth | `research_isolated/mlstruct_fp/` |
| **35** | **iDesigner** | Décoration intérieure | Propriétaire fermé | Interdit | `BLOCKED` | **P3** | — | — | Non publié | Non disponible | Rejeté |
| **36** | **Rooms-with-Text** | Filigranes OCR | Recherche académique | Hors sujet | `BLOCKED` | **P3** | — | JPG | Détection de logos/watermarks | Hors sujet | Rejeté (Watermark OCR) |
| **37** | **360SpatialAI** | Panoramas 360 | Propriétaire fermé | Inconnu | `BLOCKED` | **P3** | — | — | Prototype d'application web | Non disponible | Rejeté |
| **38** | **Kaggle Interior Design** | Photos d'intérieur | Inconnue | Inconnu | `UNKNOWN` | **P3** | ~1 Go | JPG 256px | Vignettes non annotées | Non vérifié | Rejeté (Basse qualité) |
| **39** | **rrustom/architecture2022** | Photos d'architecture | None (HF) | Inconnu | `UNKNOWN` | **P3** | ~500 Mo | Parquet | Prompts non qualifiés | Non vérifié | Rejeté |
| **40** | **DataDrivenAEC** | Répertoire AEC | Curated Index | Autorisé | `CORE` | **P1** | Métadonnées | Index | Veille sur données ouvertes | Index de veille | Veille continue |
| **41** | **Interior Design Trends 2026**| Tendances contemporaines | Usage interne | Autorisé | `CORE` | **P1** | 0,001 Mo | CSV | Sondage et synthèse prospective | **ACQUIS & VÉRIFIÉ** | `core/trends/` |
| **42** | **ARCHI-AI Expert Curated** | Pédagogie de Studio | Propriétaire ARCHI-AI | Pleine propriété| `CORE` | **P0** | ~10 Mo | JSONL, Images | Critiques de jury, cours | **ACQUIS & VÉRIFIÉ** | Interne |
| **43** | **MoMA Collection** | Histoire du Design | CC0-1.0 (Public Domain) | Autorisé | `CORE` | **P0** | 70,8 Mo | CSV | Biographies, Mobilier design | **ACQUIS & VÉRIFIÉ** | `core/design_history/moma/` |
| **44** | **buildingSMART Certification** | BIM / IFC Normatif | CC-BY-4.0 | Autorisé | `CORE` | **P0** | 17,6 Mo | IFC | Modèles IFC certifiés | **ACQUIS & VÉRIFIÉ** | `core/bim_ifc/buildingsmart/` |
| **45** | **Poly Haven Textures** | Matériaux PBR | CC0-1.0 (Public Domain) | Autorisé | `CORE` | **P0** | 1,0 Mo (Catalog/Th.) | JSON, PNG | Textures de revêtements PBR | **ACQUIS & VÉRIFIÉ** | `core/materials/polyhaven/` |
| **46** | **Poly Haven Indoor HDRIs** | Éclairage Intérieur | CC0-1.0 (Public Domain) | Autorisé | `CORE` | **P0** | 1,1 Mo (Catalog/Th.) | JSON, PNG | Panoramas lumière calibrés | **ACQUIS & VÉRIFIÉ** | `core/lighting/polyhaven/` |
| **47** | **MMMU Architecture** | Raisonnement VLM Expert | Apache-2.0 | Autorisé | `CORE` | **P0** | 16,0 Mo | Parquet | Diagrammes, Q/A expertes | **ACQUIS & VÉRIFIÉ** | `core/multimodal_reasoning/` |
| **48** | **RPLAN Floorplan Edited** | Floorplans Résidentiels | Open Research License | Autorisé | `CORE` | **P1** | 22,5 Mo | ZIP, Parquet | 80k plans matriciels nettoyés | **ACQUIS & VÉRIFIÉ** | `core/rplan/` |
| **49** | **Ergonomie Neufert/Panero** | Ergonomie & Anthropométrie | CC0-1.0 (Public Domain Data)| Autorisé | `CORE` | **P0** | 0,002 Mo | JSON | Cotes, Dégagements, Gabarits | **ACQUIS & VÉRIFIÉ** | `core/ergonomie/` |
| **50** | **ZInD (Zillow Indoor)** | 3D / Panoramas | Zillow Academic Terms | Interdit | `RESEARCH / ISOLATED` | **P1** | ~80 Go | Panos, JSON | 71k panoramas, plans 2D/3D | Needs Form Auth | `research_isolated/zind/` |
| **51** | **3D-FUTURE (Alibaba)** | Mobilier 3D | Academic Non-Commercial | Interdit | `RESEARCH / ISOLATED` | **P1** | ~30 Go | OBJ, GLB | Modèles 3D meublants avec cotes| Formulaire requis | `research_isolated/3d_future/` |
| **52** | **Hypersim (Apple)** | Photoréalisme / Lumière | Apple Non-Commercial | Interdit | `RESEARCH / ISOLATED` | **P2** | >1 To | EXR, PNG | Illumination globale, Géométrie | Réservé Recherche | `research_isolated/hypersim/` |
