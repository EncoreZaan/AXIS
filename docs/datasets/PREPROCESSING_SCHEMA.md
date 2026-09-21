# ARCHI-AI — Spécification du Master Schema Canonique Pivot

## 1. Philosophie du Schéma Pivot

Le Master Schema (`dataset_tools/preprocessing/schema.py`) est le pivot d'interopérabilité d'ARCHI-AI.
Il permet de représenter uniformément n'importe quel actif architectural tout en préservant 100% des spécificités géométriques, topologiques, physiques et réglementaires de chaque source.

---

## 2. Structure Universelle (`MasterCanonicalItem`)

Chaque enregistrement normalisé possède les champs d'identification, de routage et de traçabilité suivants :

| Champ | Type | Description |
| :--- | :--- | :--- |
| `id` | `str` | Identifiant canonique unique (ex: `ARCHI_MASTER_RESPLAN_004281`) |
| `source_id` | `str` | Identifiant dans la source d'origine |
| `source_name` | `str` | Nom de la source officielle (ex: `CORE_RESPLAN`) |
| `source_license` | `str` | Licence vérifiée (ex: `CC-BY-4.0`, `CC0-1.0`) |
| `modality` | `ModalityType` | `floorplan_2d`, `spatial_3d`, `bim_ifc`, `material_pbr`, etc. |
| `data_type` | `str` | Format précis (`vector_polygon_graph`, `pbr_material_spec`...) |
| `domain` | `str` | `architecture`, `interior_design`, `bim`, `heritage`, `regulatory` |
| `routing` | `RoutingType` | `FINETUNE`, `RAG`, `TOOL`, `BENCHMARK`, `HOLDOUT`, `MULTIUSE` |
| `quality_status` | `QualityStatus` | `PASS`, `WARNING`, `REVIEW`, `FAIL` |
| `provenance` | `ProvenanceRecord`| Chaîne d'ancrage jusqu'au fichier RAW source |

---

## 3. Payloads Spécialisés par Modalité

Selon la modalité, l'un des blocs spécialisés est instancié :

### A. Plans 2D (`floorplan`) — `PlanGeometry`
- `rooms` : liste de `PlanRoom` avec label, coordonnées polygonales réelles, surface métrique certifiée.
- `walls` & `openings` : parois, portes, baies vitrées avec repérage des pièces connectées.
- `room_adjacency_graph` : dictionnaire de topologie de circulation (pièce -> pièces accessibles).
- `scale` : échelle déclarée ou `null` si non étalonnée.
- `unknown_fields` : documentation formelle des cotes non disponibles à la source.

### B. Spatial 3D (`spatial`) — `SpatialScene`
- `objects` : liste de `SpatialObject` avec catégorie, position `[x,y,z]`, rotation `[rx,ry,rz]`, boîtes englobantes `[dx,dy,dz]`, et appartenance à la pièce (`room_id`).
- `scene_graph` : graphe hiérarchique (`room_contains`, `spatial_co_presence`).

### C. BIM / IFC (`bim`) — `BimModelSummary`
- `ifc_schema` : schéma certifié (`IFC2X3`, `IFC4`, `IFC4X3`).
- `storeys` & `spaces` : arborescence spatiale du bâtiment.
- `element_counts` : décompte rigoureux des classes (`IfcWall`, `IfcDoor`, `IfcWindow`, etc.).
- `materials_declared` : matériaux réels extraits du modèle.

### D. Matériaux PBR (`material`) — `PbrMaterialItem`
- `physical_scale_m` : dimensions réelles métriques `[largeur, hauteur]` en mètres.
- `maps_available` : canaux PBR identifiés (`color`, `roughness`, `normal`, `displacement`, `ao`).

### E. Lumière HDRI (`lighting`) — `HdriLightingItem`
- `kelvin_temperature` : température de couleur de la balance des blancs.
- `ev` : valeur d'exposition calibrée.
- `environment_type` : intérieur, extérieur, studio, nature.

### F. Réglementation (`regulatory`) — `RegulatoryArticle`
- `document`, `theme`, `section`, `article_number`, `text` inaltéré, `jurisdiction`.

### G. Ergonomie (`ergonomics`) — `ErgonomicStandard`
- `original_value` & `original_unit` (cotes inaltérées en cm).
- `normalized_si_value` & `normalized_si_unit` (conversion certifiée en mètres).
- `min_value` & `recommended_value`.

### H. Questions / Réponses (`qa`) — `MultimodalQAPair`
- `question`, `answer`, `options`, `ground_truth`.
- `is_benchmark_holdout` : drapeau d'isolation étanche pour évaluation aveugle.
