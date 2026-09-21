# ARCHI-AI — Audit & Gap Analysis des 69 Tâches de Supervision (`SUPERVISION_TASK_GAP_ANALYSIS.md`)

> **Phase :** PHASE 2 — Supervision Engineering & Pre-Training Gate  
> **Artefact d'entrée :** MASTER DATASET v2 (65 342 records consolidés, étanches et audités)  
> **Statut de l'Audit :** AUDIT EXHAUSTIF RÉALISÉ — BASELINE 69 TÂCHES  

---

## 1. Synthèse Exécutive de l'Audit des 69 Tâches

| Statut Forensic | Nombre de Tâches | % du Catalogue | Décision d'Ingénierie |
| :--- | :---: | :---: | :--- |
| **`VALID`** | **43** | 62.3 % | Tâches pleinement ancrées dans le Master Dataset v2 avec cibles vérifiables et nécessité multimodale démontrée. |
| **`DUPLICATE`** | **9** | 13.0 % | Tâches redondantes avec une autre tâche du catalogue (fusion ou restriction requise pour éviter l'inflation artificielle). |
| **`PARTIAL`** | **9** | 13.0 % | Tâches valides conceptuellement mais nécessitant un cadrage strict de la consigne ou un formatage expert pour éviter la réponse générique. |
| **`MISSING_EVIDENCE`** | **5** | 7.2 % | Données sources ou annotations manquantes dans le Master Dataset v2 (impossible à superviser de façon déterministe). |
| **`INVALID`** | **1** | 1.4 % | Tâche mathématiquement ou physiquement invalide sur le corpus actuel (ex: surfaces métriques m² sur plans matriciels sans échelle). |
| **`FAKE_MULTIMODAL`** | **1** | 1.4 % | Risque critique de faux multimodal : la modalité texte ou image suffit à elle seule à donner la réponse sans croisement. |
| **`UNDERSPECIFIED`** | **1** | 1.4 % | Tâche trop générique ou floue, sans contrat d'évaluation atomique mesurable. |
| **TOTAL** | **69** | **100.0 %** | *Catalogue complet V1 inspecté* |

---

## 2. Tableau d'Audit Forensic des 69 Tâches

| N° | Task ID | Task Name | Family | Modality | Difficulty | Input Types | Target Type | Grounding | Status |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :---: |
| 01 | `IMAGE_ANALYSIS` | Analyse Visuelle Globale | ARCHITECTURAL_PERCEPTION | `IMAGE_ONLY` | L1-L3 | interior_photo, render_image | structured_visual_description | DIRECT_VISUAL_PIXELS | **`VALID`** |
| 02 | `INTERIOR_ANALYSIS` | Analyse Typologique d'Intérieur | ARCHITECTURAL_PERCEPTION | `IMAGE_ONLY` | L2-L4 | interior_photo | space_typology_identification | DIRECT_VISUAL_PIXELS | **`DUPLICATE`** |
| 03 | `MATERIAL_IDENTIFICATION` | Identification Visuelle de Matériaux | MATERIAL_UNDERSTANDING | `IMAGE_ONLY` | L1-L3 | material_texture_thumb, interior_photo | material_class_recognition | VERIFIABLE_METADATA_AND_PIXELS | **`VALID`** |
| 04 | `VISUAL_LIGHTING_ANALYSIS` | Analyse Visuelle de l'Éclairage | ARCHITECTURAL_PERCEPTION | `IMAGE_ONLY` | L2-L4 | hdri_thumb, interior_render | lighting_distribution_evaluation | LUMINANCE_AND_SOURCE_DETECTION | **`VALID`** |
| 05 | `FURNITURE_IDENTIFICATION` | Identification de Mobilier | INTERIOR_DESIGN | `IMAGE_ONLY` | L1-L2 | rendered_scene_image, interior_photo | furniture_category_count | BOUNDING_BOX_AND_CLASS | **`VALID`** |
| 06 | `STYLE_ANALYSIS` | Analyse Stylistique Visuelle | ARCHITECTURAL_VOCABULARY | `IMAGE_ONLY` | L2-L4 | interior_photo | stylistic_label | UNGROUNDED_SUBJECTIVE | **`MISSING_EVIDENCE`** |
| 07 | `SPATIAL_RELATION_ANALYSIS` | Analyse des Relations Spatiales Visuelles | SPATIAL_REASONING | `IMAGE_ONLY` | L2-L3 | interior_image, 3d_render | relative_spatial_relations | 2D_IMAGE_COORDINATES | **`VALID`** |
| 08 | `FLOORPLAN_READING` | Lecture de Plan d'Étage | PLAN_UNDERSTANDING | `PLAN_ONLY` | L1-L3 | segmented_raster_plan, vector_floorplan | graphic_code_decoding | SEGMENTATION_MASKS | **`VALID`** |
| 09 | `ROOM_IDENTIFICATION` | Identification des Pièces | PLAN_UNDERSTANDING | `PLAN_ONLY` | L1-L2 | segmented_raster_plan | room_count_and_boundaries | CONNECTED_COMPONENTS_MASKS | **`VALID`** |
| 10 | `ROOM_TOPOLOGY` | Topologie et Connectivité des Pièces | PLAN_UNDERSTANDING | `PLAN_ONLY` | L2-L4 | segmented_raster_plan | adjacency_graph | DOOR_TRANSITION_INTERSECTIONS | **`VALID`** |
| 11 | `CIRCULATION_ANALYSIS` | Analyse des Circulations et Flux | PLAN_UNDERSTANDING | `PLAN_ONLY` | L3-L5 | segmented_raster_plan | circulation_spine_and_traversal | TOPOLOGICAL_DISTANCE_AND_PATHS | **`VALID`** |
| 12 | `DOOR_WINDOW_ANALYSIS` | Analyse des Baies et Ouvertures | PLAN_UNDERSTANDING | `PLAN_ONLY` | L2-L3 | segmented_raster_plan | openings_count_and_orientation | OPENING_MASKS_AND_COORDINATES | **`VALID`** |
| 13 | `FURNITURE_LAYOUT_ANALYSIS` | Analyse de l'Implantation du Mobilier sur Plan | INTERIOR_DESIGN | `PLAN_ONLY` | L3-L4 | floorplan_with_furniture | furniture_placement_analysis | NO_FURNITURE_ON_RPLAN | **`MISSING_EVIDENCE`** |
| 14 | `PLAN_ERROR_DETECTION` | Détection d'Erreurs Spatiales sur Plan | ERROR_DETECTION | `PLAN_ONLY` | L3-L5 | floorplan_with_inconsistency | flaw_localization_and_type | TOPOLOGICAL_OR_GEOMETRIC_CONTRADICTION | **`PARTIAL`** |
| 15 | `PLAN_SUMMARY` | Synthèse Métrique du Plan | PLAN_UNDERSTANDING | `PLAN_ONLY` | L2-L3 | segmented_raster_plan | metric_surface_summary | UNSCALED_PIXEL_RISK | **`INVALID`** |
| 16 | `PLAN_TO_TEXT` | Description Textuelle Complète du Plan | DOCUMENT_UNDERSTANDING | `PLAN_ONLY` | L2-L3 | segmented_raster_plan | holistic_spatial_narrative | INTEGRATED_TOPOLOGY_AND_ROOMS | **`VALID`** |
| 17 | `SCENE_GRAPH_REASONING` | Raisonnement sur Scene Graph 3D | SPATIAL_REASONING | `3D` | L3-L4 | scene_graph_json, spatial_coordinates | graph_path_and_relationship_query | IL3D_SCENE_GRAPHS | **`VALID`** |
| 18 | `OBJECT_RELATION` | Relations Spatiales Objet-Objet 3D | GEOMETRIC_REASONING | `3D` | L2-L3 | 3d_bounding_boxes | euclidean_distance_and_relative_bearing | IL3D_BOUNDING_BOXES | **`VALID`** |
| 19 | `ROOM_OBJECT_REASONING` | Raisonnement Objet-Espace Englobant | SPATIAL_REASONING | `3D` | L3-L4 | room_envelope_and_objects | spatial_containment_and_wall_proximity | IL3D_LAYOUT_BOUNDARIES | **`VALID`** |
| 20 | `SPATIAL_LAYOUT_ANALYSIS` | Analyse d'Aménagement Tridimensionnel | SPATIAL_REASONING | `3D` | L3-L4 | 3d_scene | layout_density_and_zoning | IL3D_COORDINATES | **`DUPLICATE`** |
| 21 | `3D_TO_TEXT` | Description Textuelle de Scène 3D | DOCUMENT_UNDERSTANDING | `3D` | L2-L3 | 3d_scene_json | 3d_spatial_narrative | IL3D_OBJECT_LIST | **`VALID`** |
| 22 | `IFC_ENTITY_IDENTIFICATION` | Identification d'Entités IFC | BIM / IFC | `IFC` | L1-L2 | ifc_step_file | ifc_class_and_predefined_type | STEP_IFC_CLASSES | **`VALID`** |
| 23 | `IFC_PROPERTY_REASONING` | Raisonnement sur Propriétés IFC (Pset) | BIM / IFC | `IFC` | L2-L4 | ifc_psets | pset_property_value_retrieval | IFC_PROPERTY_SET_RECORDS | **`VALID`** |
| 24 | `BIM_SPATIAL_HIERARCHY` | Hiérarchie Spatiale BIM | BIM / IFC | `IFC` | L2-L3 | ifc_rel_aggregates | spatial_containment_tree | IFC_SPATIAL_RELATIONS | **`VALID`** |
| 25 | `BIM_OBJECT_QUERY` | Requête d'Objets BIM | BIM / IFC | `IFC` | L2-L3 | ifc_step_file | filtered_element_guid_list | IFC_ATTRIBUTE_FILTERING | **`VALID`** |
| 26 | `BIM_REASONING` | Raisonnement Synthétique BIM | BIM / IFC | `IFC` | L3-L4 | ifc_model | trade_coordination_and_quantities | MULTI_DISCIPLINE_IFC | **`PARTIAL`** |
| 27 | `IFC_QA` | Questions / Réponses Expertes IFC | BIM / IFC | `IFC` | L3-L5 | ifc_bench_qa_pairs | expert_qa_answer | BENCHMARK_GROUND_TRUTH | **`VALID`** |
| 28 | `ERGONOMIC_ANALYSIS` | Analyse Ergonomique Globale | CONSTRUCTION LOGIC | `PLAN_TEXT` | L3-L4 | floorplan_or_3d, ergonomic_norms | activity_zone_compliance | NEUFERT_PANERO_RULES | **`VALID`** |
| 29 | `CLEARANCE_CHECK` | Contrôle des Dégagements d'Usage | GEOMETRIC_REASONING | `3D` | L3-L5 | object_pair_distance, normative_threshold | pass_fail_clearance_verdict | MEASURED_DISTANCE_VS_NORM | **`VALID`** |
| 30 | `CIRCULATION_CHECK` | Vérification de Largeur de Passage | GEOMETRIC_REASONING | `PLAN_TEXT` | L2-L4 | corridor_width, regulatory_rule | compliance_status_and_delta | CORRIDOR_WIDTH_VS_NORMES_FR | **`VALID`** |
| 31 | `FURNITURE_DIMENSION_REASONING` | Raisonnement sur Cotes de Mobilier | GEOMETRIC_REASONING | `TEXT_ONLY` | L2-L3 | furniture_dimensions_tuple | anthropometric_plausibility | ANTHROPOMETRIC_STANDARDS | **`VALID`** |
| 32 | `ACCESSIBILITY_ANALYSIS` | Analyse d'Accessibilité PMR | CONSTRUCTION LOGIC | `PLAN_TEXT` | L4-L6 | layout_plan, pmr_normes_fr | pmr_compliance_audit | ARRETE_PMR_2017 | **`VALID`** |
| 33 | `MATERIAL_ANALYSIS` | Analyse des Propriétés Matériau | MATERIAL_UNDERSTANDING | `IMAGE_TEXT` | L2-L3 | pbr_maps, material_catalog_json | physical_property_specification | PBR_METADATA_AND_MAPS | **`VALID`** |
| 34 | `MATERIAL_COMPARISON` | Comparaison Technique de Matériaux | COMPARISON | `IMAGE_TEXT` | L3-L4 | material_pair_specs | differential_performance_matrix | MATERIAL_TECH_DATA | **`VALID`** |
| 35 | `MATERIAL_APPLICATION` | Prescription et Contexte d'Application | MATERIAL_UNDERSTANDING | `IMAGE_TEXT` | L3-L4 | material_spec, room_context | prescription_justification | TECHNICAL_SUITABILITY_RULES | **`VALID`** |
| 36 | `PBR_REASONING` | Raisonnement Physique PBR | MATERIAL_UNDERSTANDING | `IMAGE_TEXT` | L2-L4 | pbr_maps | shader_behavior_deduction | PHYSICALLY_BASED_METRICS | **`VALID`** |
| 37 | `LIGHTING_ANALYSIS` | Analyse de l'Ambiance Lumineuse | ARCHITECTURAL_PERCEPTION | `IMAGE_ONLY` | L2-L4 | hdri_map, interior_render | ambient_light_distribution | EXPOSURE_AND_LUX_ESTIMATE | **`VALID`** |
| 38 | `LIGHTING_SCENARIO` | Scénarisation Lumineuse | INTERIOR_DESIGN | `TEXT_ONLY` | L3-L5 | room_function_context | layered_lighting_specification | LIGHTING_STANDARDS_EN_12464 | **`PARTIAL`** |
| 39 | `DAYLIGHT_REASONING` | Raisonnement Éclairage Naturel | SPATIAL_REASONING | `PLAN_TEXT` | L3-L4 | plan_with_orientation | solar_exposure_and_glare_analysis | COMPASS_ORIENTATION_AND_FACADES | **`VALID`** |
| 40 | `ARTIFICIAL_LIGHTING_REASONING` | Raisonnement Éclairage Artificiel | MATERIAL_UNDERSTANDING | `IMAGE_TEXT` | L3-L4 | luminaire_specs, interior_context | kelvin_and_cri_prescription | PHOTOMETRIC_STANDARDS | **`VALID`** |
| 41 | `STYLE_CLASSIFICATION` | Classification de Style d'Intérieur | ARCHITECTURAL_VOCABULARY | `IMAGE_ONLY` | L1-L3 | interior_photo | style_category | UNGROUNDED_IN_CORPUS | **`DUPLICATE`** |
| 42 | `STYLE_COMPARISON` | Comparaison de Styles Décoratifs | COMPARISON | `TEXT_ONLY` | L3-L4 | design_style_names | historical_and_formal_contrast | CANONICAL_DESIGN_HISTORY | **`PARTIAL`** |
| 43 | `DESIGN_HISTORY` | Histoire du Design et Objets Cultes | ARCHITECTURAL_VOCABULARY | `TEXT_ONLY` | L2-L4 | moma_met_record | designer_date_movement_attribution | MOMA_MET_COLLECTIONS | **`VALID`** |
| 44 | `ARCHITECTURE_HISTORY` | Histoire de l'Architecture | ARCHITECTURAL_VOCABULARY | `TEXT_ONLY` | L2-L4 | architectural_movement | historical_narrative | NO_DEDICATED_ASSETS | **`MISSING_EVIDENCE`** |
| 45 | `MATERIAL_AND_STYLE_RELATION` | Relation Matériaux et Signature Stylistique | MATERIAL_UNDERSTANDING | `TEXT_ONLY` | L3-L4 | material_and_movement | stylistic_material_concordance | MOMA_DESIGN_RECORDS | **`PARTIAL`** |
| 46 | `PROJECT_CRITIQUE` | Critique Globale de Projet | ERROR_DETECTION | `PLAN_ONLY` | L4-L6 | floorplan | multi_factor_spatial_critique | TOPOLOGICAL_AND_FUNCTIONAL_CONFLICTS | **`VALID`** |
| 47 | `STRENGTH_IDENTIFICATION` | Identification des Points Forts | ERROR_DETECTION | `PLAN_ONLY` | L3-L4 | floorplan | positive_spatial_qualities | TOPOLOGY_AND_LIGHT | **`DUPLICATE`** |
| 48 | `WEAKNESS_IDENTIFICATION` | Identification des Faiblesses Spatiales | ERROR_DETECTION | `PLAN_ONLY` | L3-L5 | floorplan | spatial_and_functional_defects | TOPOLOGICAL_CONFLICTS | **`DUPLICATE`** |
| 49 | `DESIGN_PROBLEM_DETECTION` | Détection de Conflits de Conception | ERROR_DETECTION | `PLAN_ONLY` | L4-L5 | floorplan | specific_functional_conflict | DIRECT_SIGHTLINE_OR_DOOR_SWING_CONFLICT | **`VALID`** |
| 50 | `IMPROVEMENT_PROPOSAL` | Proposition d'Amélioration Spatiale | TRANSFORMATION | `PLAN_ONLY` | L4-L6 | floorplan_with_identified_problem | corrective_layout_action | ACTIONABLE_TOPOLOGY_CHANGE | **`VALID`** |
| 51 | `ALTERNATIVE_DESIGN` | Proposition d'Alternative d'Aménagement | TRANSFORMATION | `PLAN_ONLY` | L5-L6 | floorplan | alternative_partitioning | TOPOLOGY_VARIANTS | **`DUPLICATE`** |
| 52 | `REQUIREMENTS_ANALYSIS` | Analyse du Cahier des Charges | DOCUMENT_UNDERSTANDING | `TEXT_ONLY` | L3-L4 | client_brief_text | spatial_program_decomposition | BRIEF_TEXT_EXTRACTION | **`PARTIAL`** |
| 53 | `CONSTRAINT_REASONING` | Raisonnement sous Contraintes Multiples | CROSS-MODAL REASONING | `PLAN_TEXT` | L4-L6 | floorplan, regulatory_constraints | compliant_resolution_strategy | PLAN_GEOMETRY_VS_NORMS | **`VALID`** |
| 54 | `DESIGN_DECISION` | Justification de Décision de Conception | CONSTRUCTION LOGIC | `PLAN_TEXT` | L4-L5 | spatial_context, architectural_choice | tradeoff_justification | FUNCTIONAL_IMPACT_RATIONALE | **`PARTIAL`** |
| 55 | `TRADEOFF_ANALYSIS` | Analyse d'Arbitrage et Compromis | COMPARISON | `PLAN_TEXT` | L4-L6 | competing_criteria | compromise_evaluation | SPACE_VS_COST_VS_LIGHT | **`DUPLICATE`** |
| 56 | `OPTION_COMPARISON` | Comparaison Multi-Options de Projet | COMPARISON | `PLAN_ONLY` | L4-L5 | plan_variant_a, plan_variant_b | comparative_matrix | NO_PAIRED_VARIANTS | **`MISSING_EVIDENCE`** |
| 57 | `FEASIBILITY_ANALYSIS` | Étude de Faisabilité Technique | CONSTRUCTION LOGIC | `PLAN_TEXT` | L4-L5 | floorplan, structural_elements | structural_impact_verdict | LOAD_BEARING_WALL_WIDTH | **`VALID`** |
| 58 | `EXPLANATION` | Explication Pédagogique d'une Notion | ARCHITECTURAL_VOCABULARY | `TEXT_ONLY` | L2-L3 | concept_term | pedagogical_definition_and_example | ARCHITECTURAL_THEORY | **`PARTIAL`** |
| 59 | `STUDIO_CRITIQUE` | Critique d'Atelier Pédagogique (Studio Tutor) | ERROR_DETECTION | `PLAN_ONLY` | L4-L5 | student_floorplan | formative_studio_feedback | TOPOLOGY_AND_FLOW | **`DUPLICATE`** |
| 60 | `GUIDED_REASONING` | Guidage Maïeutique Pas-à-Pas | PLAN_UNDERSTANDING | `PLAN_TEXT` | L3-L5 | floorplan, guiding_prompt | step_by_step_maieutic_trace | STEPWISE_TOPOLOGICAL_EVIDENCE | **`VALID`** |
| 61 | `ERROR_EXPLANATION` | Explication Didactique d'une Erreur | ERROR_DETECTION | `PLAN_TEXT` | L3-L4 | spatial_error_case | root_cause_pedagogical_explanation | CONFLICT_GEOMETRY | **`DUPLICATE`** |
| 62 | `METHODOLOGY_EXPLANATION` | Méthodologie de Projet d'Espace | ARCHITECTURAL_VOCABULARY | `TEXT_ONLY` | L2-L3 | project_phase_query | project_workflow_breakdown | LOI_MOP_ORDRE_ARCHITECTES | **`PARTIAL`** |
| 63 | `IMAGE_PLUS_PLAN` | Confrontation Image et Plan 2D | CROSS-MODAL REASONING | `IMAGE_PLAN` | L3-L5 | plan_2d, interior_image_or_render | viewpoint_localization_or_consistency_check | CROSS_REFERENCED_CAMERA_AND_PLAN | **`VALID`** |
| 64 | `PLAN_PLUS_TEXT` | Plan 2D et Programme Textuel | CROSS-MODAL REASONING | `PLAN_TEXT` | L3-L4 | floorplan, textual_program | program_compliance_verification | PLAN_COUNT_VS_TEXT_REQUIREMENT | **`VALID`** |
| 65 | `PLAN_PLUS_3D` | Appariement Plan 2D et Maquette 3D | CROSS-MODAL REASONING | `MULTIMODAL` | L4-L5 | floorplan_2d, ifc_or_3d_mesh | 2d_to_3d_spatial_concordance | PAIRED_RESBIM_IFC_AND_PLAN | **`VALID`** |
| 66 | `IMAGE_PLUS_TEXT` | Image Intérieure et Fiche Technique | CROSS-MODAL REASONING | `IMAGE_TEXT` | L3-L4 | interior_photo, text_claim | claim_verification_or_discrepancy | VISUAL_CONFIRMATION_VS_CLAIM | **`FAKE_MULTIMODAL`** |
| 67 | `IMAGE_PLUS_PLAN_PLUS_TEXT` | Triplet Image + Plan + Programme | CROSS-MODAL REASONING | `IMAGE_PLAN_TEXT` | L5-L6 | triplet_image_plan_text | triplet_cross_validation | MMMU_ARCHITECTURE_PAIRS | **`MISSING_EVIDENCE`** |
| 68 | `BIM_PLUS_PLAN` | Confrontation Maquette IFC et Plan Étage | CROSS-MODAL REASONING | `MULTIMODAL` | L4-L5 | ifc_model, floorplan_2d | semantic_bim_to_graphic_2d_alignment | PAIRED_RESBIM_MODELS | **`VALID`** |
| 69 | `MULTIMODAL_PROJECT_REASONING` | Raisonnement Multimodal Projet Complet | CROSS-MODAL REASONING | `MULTIMODAL` | L5-L6 | heterogeneous_project_packet | holistic_synthesis | COMPLEX_AGGREGATE | **`UNDERSPECIFIED`** |

---

## 3. Analyse Détaillée des Anomalies & Déclassements

### 3.1. Tâches Invalidées (`INVALID`) — 1 tâche
- **`PLAN_SUMMARY` (#15)** : Cette tâche prétendait extraire la 'synthèse métrique' (surfaces m², dimensions en mètres) des plans 2D. Or, 99.8 % des plans 2D du Master Dataset proviennent de `CORE_RPLAN` (rasters 256x256 sans échelle métrique) et `CORE_RESPLAN` (6 enregistrements présentant une anomalie critique de pixels bruts étiquetés comme m²). Déclarer des mètres carrés sur ces données constitue une hallucination d'unité. **Action : INVALIDÉ / REJETÉ** pour la supervision métrique, ou restreint strictement au comptage de pièces et dimensions en pixels.

### 3.2. Faux Multimodal Critique (`FAKE_MULTIMODAL`) — 1 tâche
- **`IMAGE_PLUS_TEXT` (#66)** : Dans la configuration précédente, une image était fournie avec une description textuelle complète où la réponse figurait déjà dans l'énoncé textuel (ex : 'Cette photo montre un parquet en chêne massif. Quel est le revêtement ?'). L'image devenait un simple artefact décoratif. **Action : RECLASSIFIÉ EN TEST DE COHÉRENCE / DISCRÉPANCE STRICTE** : le texte doit porter une assertion (potentiellement erronée) que seule l'image permet de confirmer ou d'infirmer.

### 3.3. Données Manquantes (`MISSING_EVIDENCE`) — 5 tâches
1. **`STYLE_ANALYSIS` (#06)** : Le Master Dataset ne possède pas d'annotations de styles vérifiées sur le corpus visuel (un seul fichier CSV de tendances générales est présent). Générer des styles sans vérité terrain mène à des hallucinations pures.
2. **`FURNITURE_LAYOUT_ANALYSIS` (#13)** : Le corpus `CORE_RPLAN` ne contient aucun masque de mobilier (uniquement murs, portes, pièces). Seul `CORE_IL3D` possède du mobilier en 3D.
3. **`ARCHITECTURE_HISTORY` (#44)** : Aucun corpus textuel ou visuel d'histoire globale du bâtiment n'est présent (uniquement du mobilier design MoMA/Met).
4. **`OPTION_COMPARISON` (#56)** : Aucun doublet de plans 'Variante A vs Variante B' sur la même emprise n'existe dans le Master Dataset.
5. **`IMAGE_PLUS_PLAN_PLUS_TEXT` (#67)** : Le corpus ne compte que 3 enregistrements MMMU Architecture comportant ce triplet, insuffisant pour un entraînement robuste.

### 3.4. Tâches Redondantes (`DUPLICATE`) — 9 tâches
- `INTERIOR_ANALYSIS` (#02) → Doublon de `IMAGE_ANALYSIS` (#01)
- `SPATIAL_LAYOUT_ANALYSIS` (#20) → Doublon de `SCENE_GRAPH_REASONING` (#17) et `ROOM_OBJECT_REASONING` (#19)
- `STYLE_CLASSIFICATION` (#41) → Doublon de `STYLE_ANALYSIS` (#06)
- `STRENGTH_IDENTIFICATION` (#47) → Sous-ensemble de `PROJECT_CRITIQUE` (#46)
- `WEAKNESS_IDENTIFICATION` (#48) → Sous-ensemble de `PROJECT_CRITIQUE` (#46) et `DESIGN_PROBLEM_DETECTION` (#49)
- `ALTERNATIVE_DESIGN` (#51) → Doublon de `IMPROVEMENT_PROPOSAL` (#50)
- `TRADEOFF_ANALYSIS` (#55) → Doublon de `CONSTRAINT_REASONING` (#53)
- `STUDIO_CRITIQUE` (#59) → Doublon stylistique de `PROJECT_CRITIQUE` (#46)
- `ERROR_EXPLANATION` (#61) → Doublon didactique de `DESIGN_PROBLEM_DETECTION` (#49)

### 3.5. Tâches Sous-Spécifiées (`UNDERSPECIFIED`) — 1 tâche
- **`MULTIMODAL_PROJECT_REASONING` (#69)** : Tâche 'chapeau' sans critères de réussite mesurables ni entrées bornées. Doit être décomposée en tâches atomiques.

---

## 4. Recommandations pour le Pipeline de Supervision Phase 2
1. **Périmètre Utile :** Se concentrer sur les **43 tâches `VALID`** hautement ancrées et les **9 tâches `PARTIAL`** rigoureusement bornées.
2. **Quarantaine ResPlan :** Isoler strictement les 6 assets ResPlan jusqu'à vérification formelle de calibration.
3. **Interdiction Formelle des Templates Fixes :** Chaque exemple doit découler dynamiquement des coordonnées, entités IFC, masques ou graphes réels.
4. **Vérification de Nécessité Multimodale :** Appliquer le test d'ablation pour rejeter tout exemple solvable en mode aveugle.