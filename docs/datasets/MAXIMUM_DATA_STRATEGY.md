# ARCHI-AI — Stratégie de Données Maximale pour Système Expert

## 1. Vision et Principes Directeurs

Le projet **ARCHI-AI** a pour mission de construire un **système expert multimodal de référence en architecture intérieure, design d'espace et scénographie spatiale**. 

Le but d'ARCHI-AI n'est pas d'obtenir un modèle conversationnel générique capable de formuler quelques platitudes décoratives. Son ambition est d'atteindre le niveau d'un **architecte d'intérieur chevronné et d'un enseignant en atelier de projet**, capable d'analyser rigoureusement :
- des plans de masse, plans d'étage, coupes et élévations techniques ;
- des circulations, gabarits ergonomiques et flux d'usage ;
- des maquettes numériques BIM / IFC et des liaisons de composants bâtis ;
- des textures, calepinages, propriétés physiques et finitions de matériaux ;
- des ambiances lumineuses, photométrie, températures de couleur et rapports plein/vide ;
- des grammaires stylistiques historiques et contemporaines ;
- des diagnostics critiques argumentés et des alternatives d'aménagement ;
- la conformité aux contraintes constructives et réglementaires (PMR, ERP, sécurité incendie).

Pour y parvenir, la stratégie de données ne recherche pas le "minimum viable" mais le **maximum de compétences utiles, de couverture spatiale, de diversité typologique et de fiabilité cognitive**, selon le principe fondamental :

$$\text{Compétence Maximale} = \text{Architecture Hybride} \times (\text{Supervision Multimodale} + \text{RAG Normatif} + \text{Outils Déterministes})$$

---

## 2. Architecture Cible du Système Expert Hybride

Pour garantir une fiabilité absolue et éliminer les hallucinations sur les aspects mesurables et réglementaires, ARCHI-AI sépare strictement les rôles cognitifs :

```text
                                  UTILISATEUR / ÉTUDIANT / ARCHITECTE
                                                   │
                                                   ▼
                         ┌──────────────────────────────────────────────────┐
                         │               ORCHESTRATEUR ARCHI-AI             │
                         │    (Analyse d'intention, dispatch multimodal)    │
                         └──────────────┬───────────────────┬───────────────┘
                                        │                   │
         ┌──────────────────────────────┴───────┐           │
         ▼                                      ▼           ▼
┌─────────────────────────────────┐   ┌───────────────────────────┐   ┌─────────────────────────────┐
│     VLM (Poids Spécialisés)     │   │       RAG SPECIALISE      │   │    DETERMINISTIC ENGINES    │
│    Qwen2-VL-7B-Instruct (LoRA)  │   │  (Index Vectoriel & BM25) │   │     (Outils et Parseurs)    │
├─────────────────────────────────┤   ├───────────────────────────┤   ├─────────────────────────────┤
│ • Perception spatiale (2D / 3D) │   │ • Textes officiels (CCH,  │   │ • Calculateur de surfaces   │
│ • Reconnaissance de composants  │   │   ERP, PMR, Arrêtés)      │   │ • Analyseur de graphes (A*) │
│ • Vocabulaire architectural fin │   │ • DTU et règles de l'art  │   │ • Parseur IFC / DXF / SVG   │
│ • Raisonnement d'agencement     │   │ • Histoire de l'art/design│   │ • Détecteur de collisions   │
│ • Diagnostic critique studio    │   │ • Catalogues & fiches PBR │   │ • Vérificateur de gabarits  │
│ • Pédagogie & maïeutique        │   │ • Cours & programmes      │   │ • Calculateur FLJ / lux     │
└────────────────┬────────────────┘   └─────────────┬─────────────┘   └──────────────┬──────────────┘
                 │                                  │                                │
                 └──────────────────────────┬───────┴────────────────────────────────┘
                                            ▼
                        ┌───────────────────────────────────────┐
                        │      MOTEUR DE VÉRIFICATION COGNITIF  │
                        │  - Confronte les assertions aux cotes │
                        │  - Valide les citations normatives    │
                        │  - Enforce le statut épistémique      │
                        └───────────────────┬───────────────────┘
                                            ▼
                        ┌───────────────────────────────────────┐
                        │            RÉPONSE FINALE             │
                        │   (Structurée, sourcée, vérifiée)     │
                        └───────────────────────────────────────┘
```

---

## 3. Architecture de la Plateforme de Données (`DATA PLATFORM`)

Pour organiser les données de manière pérenne sans contamination ni redondance, l'arborescence cible s'organise en 9 répertoires fonctionnels :

```text
ARCHI-AI DATA PLATFORM
│
├── 01_RAW/                           # Archives immuables des sources externes d'origine
│   ├── cad_bim/                      # ArchCAD, IFC-Bench, ResBIM, FloorPlanCAD
│   ├── floorplans/                   # ResPlan, CubiCasa5K, MSD, RPLAN
│   ├── indoor_3d/                    # Structured3D, IL3D, M3DLayout, StructScan3D
│   ├── materials/                    # MatSynth, ambientCG, MINC
│   ├── lighting/                     # Laval Photometric HDR, OpenRooms
│   ├── styles_design/                # MMIS, Met Open Access, Cooper Hewitt
│   └── regulatory/                   # Textes légaux bruts (Légifrance, CSTB)
│
├── 02_PERCEPTION/                    # Datasets normalisés pour la vision pure
│   ├── indoor_enveloppe/             # Murs, sols, plafonds, menuiseries (StructScan3D)
│   ├── objects_grounding/            # Bounding boxes 2D/3D et détection d'objets meublants
│   ├── materials_pbr/                # Paires patch visuel ↔ nature minérale/organique
│   ├── lighting_environment/         # Reconnaissance des sources lumineuses et contrastes
│   └── scene_typologies/             # Identification des pièces (cuisine, suite, sas, etc.)
│
├── 03_SPATIAL/                       # Raisonnement géométrique, vectoriel et topologique
│   ├── floorplans_raster/            # Plans matriciels nettoyés avec segmentation
│   ├── floorplans_vector/            # Plans SVG / DXF normalisés et polyline loops
│   ├── connectivity_graphs/          # Graphes de pièces, adjacences et circulations
│   ├── spatial_relations_3d/         # Paires [Image, Orientation, Proximité relative]
│   └── layout_comparisons/           # Paires jumelles pièce vide vs meublée
│
├── 04_ARCHITECTURE/                  # Construction, enveloppe, second œuvre et BIM
│   ├── ifc_entities/                 # Entités IFC sérialisées (IfcWall, IfcDoor, IfcSpace)
│   ├── cad_symbols/                  # Dictionnaires et détections de symboles normalisés
│   ├── technical_details/            # Coupes constructives et liaisons de second œuvre
│   └── building_systems/             # Réseaux, gaines techniques, fluides et faux-plafonds
│
├── 05_DESIGN/                        # Culture du projet, composition et ambiance
│   ├── style_taxonomies/             # Banques d'images multi-styles avec fiches critères
│   ├── furniture_typologies/         # Meubles iconiques, cotes standard, designers
│   ├── color_harmonies/              # Palettes chromatiques, contrastes et saturations
│   ├── lighting_atmospheres/         # Ambiances diurnes/nocturnes, températures en Kelvin
│   └── spatial_composition/          # Trames, rythmes, symétries, pleins et vides
│
├── 06_KNOWLEDGE/                     # Base documentaire structurée pour le RAG
│   ├── history_architecture/         # Chronologie des mouvements architecturaux
│   ├── history_design/               # Monographies de designers et écoles de pensée
│   ├── french_standards_cch/         # Code de la Construction et de l'Habitation
│   ├── accessibility_pmr/            # Textes consolidés et fiches pratiques d'accessibilité
│   ├── fire_safety_erp/              # Règles de dégagements, escaliers et issues de secours
│   └── technical_dtu/                # DTU plâtrerie, carrelage, menuiserie, parquets
│
├── 07_REASONING/                     # Données d'entraînement cognitif de haut niveau
│   ├── studio_critique/              # Diagnostics argumentés d'experts sur projets
│   ├── error_detection/              # Identification d'erreurs spatiales et contre-exemples
│   ├── spatial_recommendations/      # Propositions d'optimisation d'aménagement
│   ├── comparative_analysis/         # Analyse comparative d'options d'aménagement
│   └── multimodal_consistency/       # Validation croisée [Plan ↔ Rendu ↔ Moodboard]
│
├── 08_USER/                          # Espace personnel et pédagogique évolutif (Futur)
│   ├── school_curricula/             # Cours d'écoles d'architecture (ex. MJM Graphic Design)
│   ├── student_projects/             # Projets réels, carnets de croquis et planches
│   ├── teacher_feedback/             # Retours de jurys et corrections d'enseignants
│   └── user_profiles/                # Profils de style, exigences et préférences de travail
│
└── 09_BENCHMARK/                     # Bancs de test scellés (Zéro contamination train)
    ├── blind_floorplans/             # Évaluation de lecture de plans inconnus
    ├── spatial_reasoning_eval/       # Évaluation des relations 3D et dégagements
    ├── style_recognition_eval/       # Test d'identification stylistique et matérielle
    ├── normative_audit_eval/         # Détection d'infractions aux normes PMR/ERP
    └── cross_modal_coherence_eval/   # Détection de divergences plan vs rendu
```

---

## 4. Cadre Anti-Hallucination : Statuts Épistémiques

Un architecte d'intérieur professionnel ne devine pas : il constate ce qui est visible, explicite ses hypothèses, calcule ce qui est mesurable et signale ce qui nécessite une vérification in-situ.

ARCHI-AI applique obligatoirement à chaque affirmation un **statut épistémique rigoureux** :

| Statut | Définition | Exemple d'application |
|---|---|---|
| **`OBSERVÉ`** | Fait tangible directement visible sur le document fourni (image ou plan). | *"La cloison entre l'entrée et le salon présente une ouverture sans vantail de 90 cm."* |
| **`INTERPRÉTÉ`** | Déduction spatiale ou compositionnelle fondée sur les règles de l'art. | *"La disposition en vis-à-vis du canapé et des assises favorise un salon convivial axé sur la verrière."* |
| **`INFÉRÉ`** | Estimation géométrique ou dimensionnelle probable, soumise à tolérance. | *"Au regard de l'emprise du lit standard 160×200, le passage latéral est estimé à environ 65-70 cm."* |
| **`INCONNU`** | Information strictement inaccessible sur les documents fournis. | *"La nature porteuse ou non de ce refend ne peut être confirmée sans plan de structure ou sondage destructif."* |
| **`À VÉRIFIER`** | Point critique d'usage ou de conformité exigeant une mesure terrain. | *"Vérifier la hauteur sous plafond réelle sous le faux-plafond technique de la gaine de ventilation."* |

Le modèle est entraîné sur des exemples négatifs explicites où il refuse de certifier des dimensions au millimètre sur une simple perspective sans échelle graphique.

---

## 5. Structuration des Formats de Supervision

ARCHI-AI refuse l'écueil consistant à formater l'intégralité du savoir en simples questions/réponses génériques (`Q: Que vois-tu ? A: Un salon`). Chaque type de donnée conserve sa structure native de supervision :

1. **Supervision Vectorielle & Topologique (Plans) :**
   - Représentation en boucles polygonales fermées pour les pièces.
   - Graphes de connectivité `Node(Room, Type, Area)` et `Edge(Door/Opening, Width)`.
2. **Supervision Géométrique (Objets & Volumes) :**
   - Coordonnées de bounding boxes 2D normalisées `[ymin, xmin, ymax, xmax]` pour le visual grounding.
   - Boîtes orientées 3D `[x, y, z, dx, dy, dz, r, p, y]` pour le placement spatial.
3. **Supervision Multimodale Entrelacée (Critique & Diagnostic) :**
   - Chaîne d'analyse structurée :
     1. Relevé des observables ;
     2. Identification des lignes directrices et points focaux ;
     3. Diagnostic critique des flux et circulations ;
     4. Évaluation ergonomique et lumière ;
     5. Recommandations chiffrées d'amélioration.
4. **Supervision de Raisonnement Croisé (Plan ↔ Image) :**
   - Paires multi-images [Plan 2D, Rendu 3D] avec détection des disparités d'implantation de mobilier ou de baies vitrées.

---

## 6. Architecture de l'Espace `08_USER` (Données Personnelles & Écoles)

Pour accueillir dans un second temps les données propres à l'utilisateur (cours d'écoles spécialisées telles que MJM Graphic Design, projets personnels, retours de jurys), l'infrastructure prévoit un cloisonnement strict :

- **Isolation des Poids :** Les cours et notes d'écoles ne sont pas injectés directement dans les poids du modèle de base pour éviter tout surapprentissage ou violation de propriété intellectuelle.
- **Ingestion RAG Dédiée :** Chaque cours (ex. "Technologie du bâtiment", "Histoire des arts décoratifs", "Dessin technique et conventions") est vectorisé dans un index documentaire privatif `user_school_kb`.
- **Adaptation Few-Shot & In-Context :** Les grilles de notation et critères d'évaluation des enseignants d'atelier sont fournis en consigne de contexte dynamique lors des sessions de critique de projet.
