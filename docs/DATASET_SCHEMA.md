# Schéma de Données Master (ARCHI-AI)

## 1. Principes Directeurs

Le schéma de données Master (`MasterAnnotation`) résout les limitations constatées lors du premier audit :
- **Support multi-images et multi-documents natif :** permet d'associer plusieurs photos d'une même pièce, un plan 2D et une vue 3D à un même exemple.
- **Suppression du carcan rigide à 5 sections imposées :** Les blocs `OBSERVATION`, `ANALYSE`, `POINTS FORTS`, `POINTS DE VIGILANCE`, `RECOMMANDATION` sont optionnels et structurables sans être imposés à des questions purement ponctuelles.
- **Richesse sémantique & cognitive :** Prise en compte explicite des `observables`, `interpretations`, `unknowns` et `constraints`.

---

## 2. Structure Pydantic (`dataset/master/schema/models.py`)

### `ImageItem`
| Champ | Type | Description |
| :--- | :--- | :--- |
| `path` | `str` | Chemin d'accès relatif au document |
| `document_type` | `DocumentType` | `photography`, `render_3d`, `plan_2d`, `section_2d`, `elevation_2d`, `moodboard`... |
| `caption` | `Optional[str]` | Légende contextuelle de l'image |
| `role` | `Optional[str]` | `primary`, `secondary`, `detail`, `plan_ref` |
| `width` | `Optional[int]` | Largeur mesurée en pixels |
| `height` | `Optional[int]` | Hauteur mesurée en pixels |
| `sha256` | `Optional[str]` | Empreinte cryptographique exacte pour déduplication |
| `phash` | `Optional[str]` | Empreinte perceptuelle (Average Hash) |

### `Provenance`
| Champ | Type | Description |
| :--- | :--- | :--- |
| `source_name` | `str` | Nom du corpus ou de la source de collecte |
| `source_url` | `Optional[str]` | URL de référence |
| `license` | `str` | Régime de licence |
| `project_name` | `Optional[str]` | Nom du bâtiment ou du projet d'architecture |
| `scene_id` | `Optional[str]` | Identifiant d'espace pour verrouiller le split leakage |
| `image_family` | `Optional[str]` | Regroupement de prises de vues d'un même projet |
| `collector` | `Optional[str]` | Identifiant de l'opérateur ou du prompt de génération |

### `MasterAnnotation`
| Champ | Type | Obligatoire | Description |
| :--- | :--- | :--- | :--- |
| `id` | `str` | Oui | Identifiant unique (ex: `archi_001`) |
| `images` | `List[ImageItem]` | Oui (min 1) | Liste des supports visuels |
| `document_type` | `DocumentType` | Oui | Typologie visuelle prédominante |
| `domain` | `Domain` | Oui | `architecture`, `interior_design`, `landscape`... |
| `category` | `str` | Oui | Catégorie métier générale |
| `subcategory` | `Optional[str]` | Non | Typologie spatiale (cuisine, bureau...) |
| `learning_type` | `LearningType` | Oui | `observation`, `analysis`, `critique`, `pedagogy`... |
| `difficulty` | `DifficultyLevel` | Oui | `beginner`, `intermediate`, `advanced`, `expert` |
| `skills` | `List[Skill]` | Oui | Liste des compétences architecturales requises |
| `context` | `Optional[str]` | Non | Données de cadrage du projet |
| `question` | `str` | Oui | Question posée à l'architecte/modèle |
| `answer` | `str` | Oui | Réponse d'autorité experte |
| `observables` | `List[str]` | Non | Éléments objectivement visibles |
| `interpretations`| `List[str]` | Non | Déductions et analyses spatiales |
| `unknowns` | `List[str]` | Non | Données non mesurables sans plan (réserves) |
| `constraints` | `List[str]` | Non | Normes, contraintes d'usage et ergonomie |
| `provenance` | `Provenance` | Oui | Métadonnées de traçabilité |
| `qa_status` | `QAStatus` | Oui | `PASS`, `WARNING`, `REVIEW`, `FAIL` |
| `qa_flags` | `List[str]` | Non | Alertes et remarques QA |
| `version` | `str` | Oui | Tag de version (ex: `v0.1-micro-baseline`) |
| `assigned_split` | `Optional[SplitName]` | Non | Split cible (`train`, `validation`, `test`) |
| `metadata` | `Dict[str, Any]` | Non | Champs extensibles arbitraires |
