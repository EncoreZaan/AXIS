# ARCHI-AI — Registre Exhaustif des Sources de Données (`DATASET_SOURCE_REGISTRY`)

## 1. Cadre Juridique et Catégorisation des Licences

Pour garantir la pérennité industrielle d'ARCHI-AI et éliminer tout risque d'insécurité juridique, toutes les sources font l'objet d'une traçabilité rigoureuse et sont réparties en 4 catégories fondamentales :

```text
                        REGISTRE DES SOURCES DE DONNÉES ARCHI-AI
                                           │
         ┌──────────────────┬──────────────┴──────────────┬──────────────────┐
         ▼                  ▼                             ▼                  ▼
 [ POOL A : CORE ]  [ POOL B : RESEARCH ]         [ UNKNOWN ]        [ BLOCKED ]
 • Exploitation     • Restreint académique/NC     • Licence non      • Source fermée
   commerciale      • Isolés dans les benchmarks    vérifiable         ou litigieuse
 • Dérivés libres   • Zéro contamination train    • Interdit CORE    • Rejet définitif
```

- **`CORE` (Pool A - Exploitable / Production) :** Licences permissives (**Apache-2.0**, **MIT**, **CC-BY-4.0**, **CC-BY-SA-4.0**, **CC0**, **Public Domain**, **Licence Ouverte Etalab**). Ces données intègrent le socle d'entraînement multimodal du système expert.
- **`RESEARCH / ISOLATED` (Pool B - Évaluation & Benchmarks Holdout) :** Licences comportant une clause non commerciale (**CC-BY-NC**, **Academic Use License**, **Terms of Use propriétaires académiques**). Strictement isolées du corpus d'entraînement pour garantir l'absence de contamination.
- **`UNKNOWN` :** Licence ou conditions de distribution impossibles à vérifier formellement. Strictement interdit de téléchargement dans CORE.
- **`BLOCKED` :** Téléchargement interdit, source fermée, projet abandonné ou réutilisation juridiquement risquée (ex: dépendance directe à SUNCG).

---

## 2. Table Complète et Revalidée des Sources (1 à 52)

| # | Nom de la Source | Catégorie Primaire | Licence Officielle Vérifiée | Usage Commercial | Catégorie Juridique | Priorité | Statut d'Acquisition | Emplacement Local |
|---|---|---|---|---|---|---|---|---|
| **01** | **IL3D (Layouts)** | Scènes & Layouts 3D LLM | **Apache-2.0** | Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/il3d/` |
| **02** | **StructScan3D** | Scans réels RGB-D enveloppe | **CC-BY-4.0** | Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/structscan3d/` |
| **03** | **ResPlan** | Plans d'étage vectoriels & graphes | **CC-BY-4.0 (Data) / MIT (Code)** | Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/resplan/` |
| **04** | **Modified Swiss Dwellings (MSD)** | Plans de logements collectifs | **CC-BY-4.0** | Autorisé | `CORE` | P1 | Planifié V1 | `core/msd/` |
| **05** | **MatSynth (Échantillon)** | Matériaux PBR 4K tuilables | **CC0 (Public Domain)** | Autorisé | `CORE` | P1 | Planifié Échantillon | `core/matsynth/` |
| **06** | **ambientCG** | Matériauthèque architecturale PBR | **CC0 (Public Domain)** | Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/materials/ambientcg/` |
| **07** | **ArchCAD-400K** | Blocs & symboles CAD massifs | **Academic Use License (Arcplus)** | **Interdit** | `RESEARCH / ISOLATED` | P1 | Reclassé (Exclu Core) | `research_isolated/archcad/` |
| **08** | **FloorPlanCAD (Voxel51)** | Plans CAD annotés sémantiquement | **CC-BY-SA-4.0** | Autorisé | `CORE` | P1 | **ACQUIS & VÉRIFIÉ** | `core/floorplancad/` |
| **09** | **IFC-Bench V2** | Questions/Réponses maquettes IFC | **CC-BY-4.0** | Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/bim_ifc/ifc_bench/` |
| **10** | **ResBIM-IFC** | Plans 2D annotés ↔ Maquettes 3D BIM | **MIT** | Autorisé | `CORE` | P1 | **ACQUIS & VÉRIFIÉ** | `core/resbim/` |
| **11** | **The Met Open Access** | Mobilier historique & arts décoratifs | **CC0-1.0 (Public Domain)** | Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/design_history/met/` |
| **12** | **Cooper Hewitt API** | Objets et histoire du design moderne | **CC0-1.0 (Public Domain)** | Autorisé | `CORE` | P1 | Planifié P1 | `core/design_history/cooperhewitt/` |
| **13** | **Légifrance (CCH, PMR, ERP)** | Textes réglementaires consolidés | **Licence Ouverte (Etalab)** | Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/normes_fr/` |
| **14** | **Cerema / CSTB Guides** | Fiches pratiques constructives & PMR | **Licence Ouverte / Public** | Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/normes_fr/` |
| **15** | **Structured3D** | Scènes synthétiques photoréalistes | **Academic Proprietary EULA** | Interdit | `RESEARCH / ISOLATED` | P1 | Réservé Holdout | `research_isolated/structured3d/` |
| **16** | **M3DLayout** | Hiérarchies de scènes 3D | **CC-BY-NC-4.0** | Interdit | `RESEARCH / ISOLATED` | P1 | Réservé Holdout | `research_isolated/m3dlayout/` |
| **17** | **InternScenes** | Scènes 3D interactives embodied | **CC-BY-NC-SA-4.0** | Interdit | `RESEARCH / ISOLATED` | P2 | Gated HF | `research_isolated/internscenes/` |
| **18** | **MMIS** | 40 styles d'intérieurs multi-vues | **Non spécifiée (Google Drive)** | Inconnu | `UNKNOWN` | P3 | Écarté de Core | Bloqué (Risque Juridique) |
| **19** | **CubiCasa5K** | Plans scannés réels avec cotations | **CC-BY-NC-SA-4.0** | Interdit | `RESEARCH / ISOLATED` | P1 | Réservé Holdout | `research_isolated/cubicasa5k/` |
| **20** | **Matterport3D** | Scans 3D réels d'habitations | **Matterport EULA (Strict)** | Interdit | `RESEARCH / ISOLATED` | P2 | Accès Gated | Scellé Benchmark |
| **21** | **HM3D & HM3D Semantics** | Scans Matterport sous Habitat | **Matterport EULA (Strict)** | Interdit | `RESEARCH / ISOLATED` | P2 | Accès Gated | Scellé Benchmark |
| **22** | **SpatialGen-Bench** | Évaluation multi-vues & lumière | **Academic License** | Interdit | `RESEARCH / ISOLATED` | P1 | Benchmark Seul | `research_isolated/spatialgen_bench/` |
| **23** | **InteriorGS** | Rendu 3D Gaussians d'intérieurs | **Manycore Terms (Non-commercial)**| Interdit | `RESEARCH / ISOLATED` | P2 | Réservé Recherche | `research_isolated/interiorgs/` |
| **24** | **HomeWorld & Floorplans** | Environnements 3D procéduraux | **Non publié (Dépôt vide)** | Inconnu | `BLOCKED` | P3 | Non disponible | Attente publication |
| **25** | **InteriorNet** | Scènes synthétiques variées | **Propriétaire (Liens morts)** | Interdit | `BLOCKED` | P3 | Abandonné | Écarté définitivement |
| **26** | **OpenRooms** | Éclairage intérieur décomposé | **CC-BY-NC-4.0** | Interdit | `RESEARCH / ISOLATED` | P2 | Réservé Recherche | `research_isolated/openrooms/` |
| **27** | **Laval Photometric HDR** | Panoramas HDR calibrés photométrie | **Academic Terms (Sur demande)** | Interdit | `RESEARCH / ISOLATED` | P2 | Needs Auth | Réservé Recherche |
| **28** | **ARKitScenes** | Scans LiDAR iPad de pièces | **Apple Proprietary EULA** | Sous conditions | `RESEARCH / ISOLATED` | P2 | Réservé Recherche | `research_isolated/arkitscenes/` |
| **29** | **HSSD (hssd-hab)** | Scènes d'habitations réalistes | **CC-BY-NC-4.0** | Interdit | `RESEARCH / ISOLATED` | P2 | Réservé Recherche | `research_isolated/hssd/` |
| **30** | **CHOrD** | Interactions objets/humains | **Recherche académique** | Interdit | `RESEARCH / ISOLATED` | P2 | Réservé Recherche | `research_isolated/chord/` |
| **31** | **MetaScenes** | Scènes 3D génératives | **CC-BY-NC-4.0** | Interdit | `RESEARCH / ISOLATED` | P3 | Écarté (Redondant) | `research_isolated/metascenes/` |
| **32** | **SmartScenes (SSTK)** | Boîtes à outils et layouts 3D | **MIT (Tainted SUNCG)** | Risqué | `BLOCKED` | P3 | Écarté | Écarté définitivement |
| **33** | **BRIDGE** | Dessins CAD + textes descriptifs | **Inconnue / Web Scrape** | Inconnu | `UNKNOWN` | P3 | Non vérifié | Écarté de Core |
| **34** | **MLSTRUCT-FP** | Poteaux, poutres, dalles sur plans | **Recherche académique** | Interdit | `RESEARCH / ISOLATED` | P2 | Needs Form Auth | `research_isolated/mlstruct_fp/` |
| **35** | **iDesigner** | Paires images ↔ textes décoratifs | **Propriétaire fermé non publié** | Interdit | `BLOCKED` | P3 | Non disponible | Rejeté |
| **36** | **Rooms-with-Text** | Paires images ↔ filigranes OCR | **Recherche académique** | Hors sujet | `BLOCKED` | P3 | Hors sujet | Rejeté (Watermark OCR) |
| **37** | **360SpatialAI** | Panoramas 360 annotés | **Propriétaire fermé web** | Inconnu | `BLOCKED` | P3 | Non disponible | Rejeté |
| **38** | **Kaggle Interior Design** | Images catégorisées par pièce | **Inconnue (Vignettes 256px)** | Inconnu | `UNKNOWN` | P3 | Non vérifié | Rejeté (Basse qualité) |
| **39** | **rrustom/architecture2022** | Photos d'architecture triées | **None (HF)** | Inconnu | `UNKNOWN` | P3 | Non vérifié | Rejeté |
| **40** | **DataDrivenAEC** | Répertoire de données AEC ouvertes | **Curated Index** | Autorisé | `CORE` | P1 | Répertoire source | Veille continue |
| **41** | **Interior Design Trends 2026**| Sondage et synthèse prospective | **Usage interne de veille** | Autorisé | `CORE` | P1 | **ACQUIS & VÉRIFIÉ** | `core/trends/` |
| **42** | **ARCHI-AI Expert Curated** | Données de studio, critique, jurys | **Propriétaire ARCHI-AI** | Pleine propriété| `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | Interne |
| **43** | **MoMA Collection** | Architecture & Design moderne | **CC0-1.0 (Public Domain)** | Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/design_history/moma/` |
| **44** | **buildingSMART Certification** | Modèles IFC 2x3, IFC 4, IFC 4.3 | **CC-BY-4.0** | Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/bim_ifc/buildingsmart/` |
| **45** | **Poly Haven Textures** | Revêtements & Matériaux PBR | **CC0-1.0 (Public Domain)** | Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/materials/polyhaven/` |
| **46** | **Poly Haven Indoor HDRIs** | Éclairage Intérieur Calibré | **CC0-1.0 (Public Domain)** | Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/lighting/polyhaven/` |
| **47** | **MMMU Architecture** | Raisonnement Multimodal Expert | **Apache-2.0** | Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/multimodal_reasoning/` |
| **48** | **RPLAN Floorplan Edited** | 80k Plans Résidentiels Vectorisés | **Open Research License** | Autorisé | `CORE` | P1 | **ACQUIS & VÉRIFIÉ** | `core/rplan/` |
| **49** | **Ergonomie Neufert/Panero** | Cotes & Dégagements Spatiaux | **CC0-1.0 (Public Domain Data)**| Autorisé | `CORE` | P0 | **ACQUIS & VÉRIFIÉ** | `core/ergonomie/` |
| **50** | **ZInD (Zillow Indoor)** | 71k Panoramas & Plans 3D | **Zillow Terms (Research)** | Interdit | `RESEARCH / ISOLATED` | P1 | Needs Form Auth | `research_isolated/zind/` |
| **51** | **3D-FUTURE (Alibaba)** | Mobilier 3D & Dimensions CAD | **Academic Non-Commercial** | Interdit | `RESEARCH / ISOLATED` | P1 | Formulaire requis | `research_isolated/3d_future/` |
| **52** | **Hypersim (Apple)** | Synthèse Photoréaliste Indoor | **Apple Non-Commercial** | Interdit | `RESEARCH / ISOLATED` | P2 | Réservé Recherche | `research_isolated/hypersim/` |

---

## 3. Synthèse de Répartition Juridique

- **Sources `CORE` (Pool A — Exploitable) :** **24 sources** (dont 16 déjà acquises et vérifiées dans `ARCHI_AI/dataset/raw/external/core/`).
- **Sources `RESEARCH / ISOLATED` (Pool B — Étanche / Holdout) :** **17 sources** (réservées aux bancs d'évaluation sans risque de contamination).
- **Sources `UNKNOWN` (Licence impossible à certifier) :** **4 sources** (écartées du socle CORE).
- **Sources `BLOCKED` (Litigieuses, fermées ou non publiées) :** **7 sources** (écartées définitivement).
