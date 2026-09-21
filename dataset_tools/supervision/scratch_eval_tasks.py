import os
import sys
import json
from collections import Counter

sys.path.insert(0, os.path.abspath("."))
from dataset_tools.supervision.task_catalogue import TASK_CATALOGUE, TaskGroup
from dataset_tools.supervision.mapping_matrix import SOURCE_CAPABILITY_TASK_MATRIX

# Full forensic audit of all 69 tasks
audit_results = {}

# Mappings of tasks to their technical evaluation
TASK_AUDIT_SPECS = {
    # Group A: VISUAL UNDERSTANDING
    "IMAGE_ANALYSIS": {
        "family": "ARCHITECTURAL_PERCEPTION",
        "modality": "IMAGE_ONLY",
        "input_types": ["interior_photo", "render_image"],
        "target_type": "structured_visual_description",
        "grounding": "DIRECT_VISUAL_PIXELS",
        "status": "VALID",
        "notes": "Direct observation of visible architectural boundaries and fixtures."
    },
    "INTERIOR_ANALYSIS": {
        "family": "ARCHITECTURAL_PERCEPTION",
        "modality": "IMAGE_ONLY",
        "input_types": ["interior_photo"],
        "target_type": "space_typology_identification",
        "grounding": "DIRECT_VISUAL_PIXELS",
        "status": "DUPLICATE",
        "notes": "Overlaps directly with IMAGE_ANALYSIS and ROOM_IDENTIFICATION."
    },
    "MATERIAL_IDENTIFICATION": {
        "family": "MATERIAL_UNDERSTANDING",
        "modality": "IMAGE_ONLY",
        "input_types": ["material_texture_thumb", "interior_photo"],
        "target_type": "material_class_recognition",
        "grounding": "VERIFIABLE_METADATA_AND_PIXELS",
        "status": "VALID",
        "notes": "Verifiable against PolyHaven/AmbientCG metadata and texture maps."
    },
    "VISUAL_LIGHTING_ANALYSIS": {
        "family": "ARCHITECTURAL_PERCEPTION",
        "modality": "IMAGE_ONLY",
        "input_types": ["hdri_thumb", "interior_render"],
        "target_type": "lighting_distribution_evaluation",
        "grounding": "LUMINANCE_AND_SOURCE_DETECTION",
        "status": "VALID",
        "notes": "Identifies natural vs artificial lighting sources and shadow direction."
    },
    "FURNITURE_IDENTIFICATION": {
        "family": "INTERIOR_DESIGN",
        "modality": "IMAGE_ONLY",
        "input_types": ["rendered_scene_image", "interior_photo"],
        "target_type": "furniture_category_count",
        "grounding": "BOUNDING_BOX_AND_CLASS",
        "status": "VALID",
        "notes": "Grounded in IL3D / Scan object labels."
    },
    "STYLE_ANALYSIS": {
        "family": "ARCHITECTURAL_VOCABULARY",
        "modality": "IMAGE_ONLY",
        "input_types": ["interior_photo"],
        "target_type": "stylistic_label",
        "grounding": "UNGROUNDED_SUBJECTIVE",
        "status": "MISSING_EVIDENCE",
        "notes": "No ground-truth style labels in Master Dataset; high hallucination risk."
    },
    "SPATIAL_RELATION_ANALYSIS": {
        "family": "SPATIAL_REASONING",
        "modality": "IMAGE_ONLY",
        "input_types": ["interior_image", "3d_render"],
        "target_type": "relative_spatial_relations",
        "grounding": "2D_IMAGE_COORDINATES",
        "status": "VALID",
        "notes": "Qualitative relations (left of, right of, in front of, behind)."
    },

    # Group B: FLOORPLAN
    "FLOORPLAN_READING": {
        "family": "PLAN_UNDERSTANDING",
        "modality": "PLAN_ONLY",
        "input_types": ["segmented_raster_plan", "vector_floorplan"],
        "target_type": "graphic_code_decoding",
        "grounding": "SEGMENTATION_MASKS",
        "status": "VALID",
        "notes": "Decodes red walls, green openings, white habitable spaces."
    },
    "ROOM_IDENTIFICATION": {
        "family": "PLAN_UNDERSTANDING",
        "modality": "PLAN_ONLY",
        "input_types": ["segmented_raster_plan"],
        "target_type": "room_count_and_boundaries",
        "grounding": "CONNECTED_COMPONENTS_MASKS",
        "status": "VALID",
        "notes": "Verifiable discrete room count from segmentation."
    },
    "ROOM_TOPOLOGY": {
        "family": "PLAN_UNDERSTANDING",
        "modality": "PLAN_ONLY",
        "input_types": ["segmented_raster_plan"],
        "target_type": "adjacency_graph",
        "grounding": "DOOR_TRANSITION_INTERSECTIONS",
        "status": "VALID",
        "notes": "Deterministic topological graph of interconnected rooms."
    },
    "CIRCULATION_ANALYSIS": {
        "family": "PLAN_UNDERSTANDING",
        "modality": "PLAN_ONLY",
        "input_types": ["segmented_raster_plan"],
        "target_type": "circulation_spine_and_traversal",
        "grounding": "TOPOLOGICAL_DISTANCE_AND_PATHS",
        "status": "VALID",
        "notes": "Analyzes hallway distribution, dead ends, and room access."
    },
    "DOOR_WINDOW_ANALYSIS": {
        "family": "PLAN_UNDERSTANDING",
        "modality": "PLAN_ONLY",
        "input_types": ["segmented_raster_plan"],
        "target_type": "openings_count_and_orientation",
        "grounding": "OPENING_MASKS_AND_COORDINATES",
        "status": "VALID",
        "notes": "Count and spatial location of internal and external openings."
    },
    "FURNITURE_LAYOUT_ANALYSIS": {
        "family": "INTERIOR_DESIGN",
        "modality": "PLAN_ONLY",
        "input_types": ["floorplan_with_furniture"],
        "target_type": "furniture_placement_analysis",
        "grounding": "NO_FURNITURE_ON_RPLAN",
        "status": "MISSING_EVIDENCE",
        "notes": "RPLAN contains zero furniture annotations. ResPlan has unscaled pixel anomaly."
    },
    "PLAN_ERROR_DETECTION": {
        "family": "ERROR_DETECTION",
        "modality": "PLAN_ONLY",
        "input_types": ["floorplan_with_inconsistency"],
        "target_type": "flaw_localization_and_type",
        "grounding": "TOPOLOGICAL_OR_GEOMETRIC_CONTRADICTION",
        "status": "PARTIAL",
        "notes": "Requires controlled negative perturbation (e.g. trapped room without opening)."
    },
    "PLAN_SUMMARY": {
        "family": "PLAN_UNDERSTANDING",
        "modality": "PLAN_ONLY",
        "input_types": ["segmented_raster_plan"],
        "target_type": "metric_surface_summary",
        "grounding": "UNSCALED_PIXEL_RISK",
        "status": "INVALID",
        "notes": "RPLAN has no physical metric scale bar; inventing m2 values is forbidden."
    },
    "PLAN_TO_TEXT": {
        "family": "DOCUMENT_UNDERSTANDING",
        "modality": "PLAN_ONLY",
        "input_types": ["segmented_raster_plan"],
        "target_type": "holistic_spatial_narrative",
        "grounding": "INTEGRATED_TOPOLOGY_AND_ROOMS",
        "status": "VALID",
        "notes": "Full descriptive translation of plan topology into structured prose."
    },

    # Group C: SPATIAL 3D
    "SCENE_GRAPH_REASONING": {
        "family": "SPATIAL_REASONING",
        "modality": "3D",
        "input_types": ["scene_graph_json", "spatial_coordinates"],
        "target_type": "graph_path_and_relationship_query",
        "grounding": "IL3D_SCENE_GRAPHS",
        "status": "VALID",
        "notes": "Direct deterministic querying of IL3D nodes and edges."
    },
    "OBJECT_RELATION": {
        "family": "GEOMETRIC_REASONING",
        "modality": "3D",
        "input_types": ["3d_bounding_boxes"],
        "target_type": "euclidean_distance_and_relative_bearing",
        "grounding": "IL3D_BOUNDING_BOXES",
        "status": "VALID",
        "notes": "Exact 3D metric coordinates (x, y, z) and distance calculation."
    },
    "ROOM_OBJECT_REASONING": {
        "family": "SPATIAL_REASONING",
        "modality": "3D",
        "input_types": ["room_envelope_and_objects"],
        "target_type": "spatial_containment_and_wall_proximity",
        "grounding": "IL3D_LAYOUT_BOUNDARIES",
        "status": "VALID",
        "notes": "Calculates object positions relative to room walls and boundaries."
    },
    "SPATIAL_LAYOUT_ANALYSIS": {
        "family": "SPATIAL_REASONING",
        "modality": "3D",
        "input_types": ["3d_scene"],
        "target_type": "layout_density_and_zoning",
        "grounding": "IL3D_COORDINATES",
        "status": "DUPLICATE",
        "notes": "Redundant with SCENE_GRAPH_REASONING and ROOM_OBJECT_REASONING."
    },
    "3D_TO_TEXT": {
        "family": "DOCUMENT_UNDERSTANDING",
        "modality": "3D",
        "input_types": ["3d_scene_json"],
        "target_type": "3d_spatial_narrative",
        "grounding": "IL3D_OBJECT_LIST",
        "status": "VALID",
        "notes": "Structured textual description of 3D interior layout."
    },

    # Group D: BIM IFC
    "IFC_ENTITY_IDENTIFICATION": {
        "family": "BIM / IFC",
        "modality": "IFC",
        "input_types": ["ifc_step_file"],
        "target_type": "ifc_class_and_predefined_type",
        "grounding": "STEP_IFC_CLASSES",
        "status": "VALID",
        "notes": "Verifiable against real IFC files (IfcWall, IfcDoor, IfcSpace)."
    },
    "IFC_PROPERTY_REASONING": {
        "family": "BIM / IFC",
        "modality": "IFC",
        "input_types": ["ifc_psets"],
        "target_type": "pset_property_value_retrieval",
        "grounding": "IFC_PROPERTY_SET_RECORDS",
        "status": "VALID",
        "notes": "Queries real property sets (Pset_WallCommon, thermal, acoustic)."
    },
    "BIM_SPATIAL_HIERARCHY": {
        "family": "BIM / IFC",
        "modality": "IFC",
        "input_types": ["ifc_rel_aggregates"],
        "target_type": "spatial_containment_tree",
        "grounding": "IFC_SPATIAL_RELATIONS",
        "status": "VALID",
        "notes": "Extracts real Storey -> Space -> Element hierarchy."
    },
    "BIM_OBJECT_QUERY": {
        "family": "BIM / IFC",
        "modality": "IFC",
        "input_types": ["ifc_step_file"],
        "target_type": "filtered_element_guid_list",
        "grounding": "IFC_ATTRIBUTE_FILTERING",
        "status": "VALID",
        "notes": "Deterministic query by type, material or level."
    },
    "BIM_REASONING": {
        "family": "BIM / IFC",
        "modality": "IFC",
        "input_types": ["ifc_model"],
        "target_type": "trade_coordination_and_quantities",
        "grounding": "MULTI_DISCIPLINE_IFC",
        "status": "PARTIAL",
        "notes": "Needs rigorous boundary to avoid vague regurgitation."
    },
    "IFC_QA": {
        "family": "BIM / IFC",
        "modality": "IFC",
        "input_types": ["ifc_bench_qa_pairs"],
        "target_type": "expert_qa_answer",
        "grounding": "BENCHMARK_GROUND_TRUTH",
        "status": "VALID",
        "notes": "Direct benchmark questions verified against model."
    },

    # Group E: ERGONOMICS
    "ERGONOMIC_ANALYSIS": {
        "family": "CONSTRUCTION LOGIC",
        "modality": "PLAN_TEXT",
        "input_types": ["floorplan_or_3d", "ergonomic_norms"],
        "target_type": "activity_zone_compliance",
        "grounding": "NEUFERT_PANERO_RULES",
        "status": "VALID",
        "notes": "Evaluates clearances and activity spaces."
    },
    "CLEARANCE_CHECK": {
        "family": "GEOMETRIC_REASONING",
        "modality": "3D",
        "input_types": ["object_pair_distance", "normative_threshold"],
        "target_type": "pass_fail_clearance_verdict",
        "grounding": "MEASURED_DISTANCE_VS_NORM",
        "status": "VALID",
        "notes": "Checks whether distance >= threshold (e.g. 90 cm passage)."
    },
    "CIRCULATION_CHECK": {
        "family": "GEOMETRIC_REASONING",
        "modality": "PLAN_TEXT",
        "input_types": ["corridor_width", "regulatory_rule"],
        "target_type": "compliance_status_and_delta",
        "grounding": "CORRIDOR_WIDTH_VS_NORMES_FR",
        "status": "VALID",
        "notes": "Evaluates hallway width against 90 cm / 140 cm standards."
    },
    "FURNITURE_DIMENSION_REASONING": {
        "family": "GEOMETRIC_REASONING",
        "modality": "TEXT_ONLY",
        "input_types": ["furniture_dimensions_tuple"],
        "target_type": "anthropometric_plausibility",
        "grounding": "ANTHROPOMETRIC_STANDARDS",
        "status": "VALID",
        "notes": "Assesses standard table height (72-76 cm), seat height (45 cm)."
    },
    "ACCESSIBILITY_ANALYSIS": {
        "family": "CONSTRUCTION LOGIC",
        "modality": "PLAN_TEXT",
        "input_types": ["layout_plan", "pmr_normes_fr"],
        "target_type": "pmr_compliance_audit",
        "grounding": "ARRETE_PMR_2017",
        "status": "VALID",
        "notes": "1.50 m diameter turning circle, 83 cm door clearance."
    },

    # Group F: MATERIALS
    "MATERIAL_ANALYSIS": {
        "family": "MATERIAL_UNDERSTANDING",
        "modality": "IMAGE_TEXT",
        "input_types": ["pbr_maps", "material_catalog_json"],
        "target_type": "physical_property_specification",
        "grounding": "PBR_METADATA_AND_MAPS",
        "status": "VALID",
        "notes": "Evaluates roughness, albedo, normal perturbation."
    },
    "MATERIAL_COMPARISON": {
        "family": "COMPARISON",
        "modality": "IMAGE_TEXT",
        "input_types": ["material_pair_specs"],
        "target_type": "differential_performance_matrix",
        "grounding": "MATERIAL_TECH_DATA",
        "status": "VALID",
        "notes": "Contrasts porcelain stoneware vs solid parquet (wear, moisture)."
    },
    "MATERIAL_APPLICATION": {
        "family": "MATERIAL_UNDERSTANDING",
        "modality": "IMAGE_TEXT",
        "input_types": ["material_spec", "room_context"],
        "target_type": "prescription_justification",
        "grounding": "TECHNICAL_SUITABILITY_RULES",
        "status": "VALID",
        "notes": "Justifies wet room vs dry room material suitability."
    },
    "PBR_REASONING": {
        "family": "MATERIAL_UNDERSTANDING",
        "modality": "IMAGE_TEXT",
        "input_types": ["pbr_maps"],
        "target_type": "shader_behavior_deduction",
        "grounding": "PHYSICALLY_BASED_METRICS",
        "status": "VALID",
        "notes": "Explains light reflection changes under varying roughness/specular."
    },

    # Group G: LIGHTING
    "LIGHTING_ANALYSIS": {
        "family": "ARCHITECTURAL_PERCEPTION",
        "modality": "IMAGE_ONLY",
        "input_types": ["hdri_map", "interior_render"],
        "target_type": "ambient_light_distribution",
        "grounding": "EXPOSURE_AND_LUX_ESTIMATE",
        "status": "VALID",
        "notes": "Assesses primary illumination vector and glare index."
    },
    "LIGHTING_SCENARIO": {
        "family": "INTERIOR_DESIGN",
        "modality": "TEXT_ONLY",
        "input_types": ["room_function_context"],
        "target_type": "layered_lighting_specification",
        "grounding": "LIGHTING_STANDARDS_EN_12464",
        "status": "PARTIAL",
        "notes": "Must be bound to room function; risks subjective styling if unbounded."
    },
    "DAYLIGHT_REASONING": {
        "family": "SPATIAL_REASONING",
        "modality": "PLAN_TEXT",
        "input_types": ["plan_with_orientation"],
        "target_type": "solar_exposure_and_glare_analysis",
        "grounding": "COMPASS_ORIENTATION_AND_FACADES",
        "status": "VALID",
        "notes": "Assesses south sun exposure vs north diffused lighting."
    },
    "ARTIFICIAL_LIGHTING_REASONING": {
        "family": "MATERIAL_UNDERSTANDING",
        "modality": "IMAGE_TEXT",
        "input_types": ["luminaire_specs", "interior_context"],
        "target_type": "kelvin_and_cri_prescription",
        "grounding": "PHOTOMETRIC_STANDARDS",
        "status": "VALID",
        "notes": "Kelvin (2700K vs 4000K) and IRC >= 90 prescription."
    },

    # Group H: DESIGN HISTORY
    "STYLE_CLASSIFICATION": {
        "family": "ARCHITECTURAL_VOCABULARY",
        "modality": "IMAGE_ONLY",
        "input_types": ["interior_photo"],
        "target_type": "style_category",
        "grounding": "UNGROUNDED_IN_CORPUS",
        "status": "DUPLICATE",
        "notes": "Duplicate of STYLE_ANALYSIS (#06); lacks ground truth annotations."
    },
    "STYLE_COMPARISON": {
        "family": "COMPARISON",
        "modality": "TEXT_ONLY",
        "input_types": ["design_style_names"],
        "target_type": "historical_and_formal_contrast",
        "grounding": "CANONICAL_DESIGN_HISTORY",
        "status": "PARTIAL",
        "notes": "Text-only architectural theory."
    },
    "DESIGN_HISTORY": {
        "family": "ARCHITECTURAL_VOCABULARY",
        "modality": "TEXT_ONLY",
        "input_types": ["moma_met_record"],
        "target_type": "designer_date_movement_attribution",
        "grounding": "MOMA_MET_COLLECTIONS",
        "status": "VALID",
        "notes": "Real curated museum metadata (Breuer, Corbusier, Eames)."
    },
    "ARCHITECTURE_HISTORY": {
        "family": "ARCHITECTURAL_VOCABULARY",
        "modality": "TEXT_ONLY",
        "input_types": ["architectural_movement"],
        "target_type": "historical_narrative",
        "grounding": "NO_DEDICATED_ASSETS",
        "status": "MISSING_EVIDENCE",
        "notes": "Corpus contains design collection records (furniture), not building history."
    },
    "MATERIAL_AND_STYLE_RELATION": {
        "family": "MATERIAL_UNDERSTANDING",
        "modality": "TEXT_ONLY",
        "input_types": ["material_and_movement"],
        "target_type": "stylistic_material_concordance",
        "grounding": "MOMA_DESIGN_RECORDS",
        "status": "PARTIAL",
        "notes": "Links tubular chrome to modernism, bentwood to Thonet."
    },

    # Group I: CRITIQUE
    "PROJECT_CRITIQUE": {
        "family": "ERROR_DETECTION",
        "modality": "PLAN_ONLY",
        "input_types": ["floorplan"],
        "target_type": "multi_factor_spatial_critique",
        "grounding": "TOPOLOGICAL_AND_FUNCTIONAL_CONFLICTS",
        "status": "VALID",
        "notes": "Examines acoustic isolation, privacy filters, night/day zoning."
    },
    "STRENGTH_IDENTIFICATION": {
        "family": "ERROR_DETECTION",
        "modality": "PLAN_ONLY",
        "input_types": ["floorplan"],
        "target_type": "positive_spatial_qualities",
        "grounding": "TOPOLOGY_AND_LIGHT",
        "status": "DUPLICATE",
        "notes": "Subset of PROJECT_CRITIQUE (#46)."
    },
    "WEAKNESS_IDENTIFICATION": {
        "family": "ERROR_DETECTION",
        "modality": "PLAN_ONLY",
        "input_types": ["floorplan"],
        "target_type": "spatial_and_functional_defects",
        "grounding": "TOPOLOGICAL_CONFLICTS",
        "status": "DUPLICATE",
        "notes": "Subset of PROJECT_CRITIQUE (#46) and DESIGN_PROBLEM_DETECTION (#49)."
    },
    "DESIGN_PROBLEM_DETECTION": {
        "family": "ERROR_DETECTION",
        "modality": "PLAN_ONLY",
        "input_types": ["floorplan"],
        "target_type": "specific_functional_conflict",
        "grounding": "DIRECT_SIGHTLINE_OR_DOOR_SWING_CONFLICT",
        "status": "VALID",
        "notes": "Detects specific errors: WC opening into kitchen, door clash."
    },
    "IMPROVEMENT_PROPOSAL": {
        "family": "TRANSFORMATION",
        "modality": "PLAN_ONLY",
        "input_types": ["floorplan_with_identified_problem"],
        "target_type": "corrective_layout_action",
        "grounding": "ACTIONABLE_TOPOLOGY_CHANGE",
        "status": "VALID",
        "notes": "Proposes partition shift, pocket door, or buffer zone creation."
    },
    "ALTERNATIVE_DESIGN": {
        "family": "TRANSFORMATION",
        "modality": "PLAN_ONLY",
        "input_types": ["floorplan"],
        "target_type": "alternative_partitioning",
        "grounding": "TOPOLOGY_VARIANTS",
        "status": "DUPLICATE",
        "notes": "Duplicate of IMPROVEMENT_PROPOSAL (#50)."
    },

    # Group J: PROFESSIONAL REASONING
    "REQUIREMENTS_ANALYSIS": {
        "family": "DOCUMENT_UNDERSTANDING",
        "modality": "TEXT_ONLY",
        "input_types": ["client_brief_text"],
        "target_type": "spatial_program_decomposition",
        "grounding": "BRIEF_TEXT_EXTRACTION",
        "status": "PARTIAL",
        "notes": "Extracts functional requirements; text-only document understanding."
    },
    "CONSTRAINT_REASONING": {
        "family": "CROSS-MODAL REASONING",
        "modality": "PLAN_TEXT",
        "input_types": ["floorplan", "regulatory_constraints"],
        "target_type": "compliant_resolution_strategy",
        "grounding": "PLAN_GEOMETRY_VS_NORMS",
        "status": "VALID",
        "notes": "Joint optimization under PMR clearances and structure."
    },
    "DESIGN_DECISION": {
        "family": "CONSTRUCTION LOGIC",
        "modality": "PLAN_TEXT",
        "input_types": ["spatial_context", "architectural_choice"],
        "target_type": "tradeoff_justification",
        "grounding": "FUNCTIONAL_IMPACT_RATIONALE",
        "status": "PARTIAL",
        "notes": "Needs strict structure to prevent generic architectural babble."
    },
    "TRADEOFF_ANALYSIS": {
        "family": "COMPARISON",
        "modality": "PLAN_TEXT",
        "input_types": ["competing_criteria"],
        "target_type": "compromise_evaluation",
        "grounding": "SPACE_VS_COST_VS_LIGHT",
        "status": "DUPLICATE",
        "notes": "Overlaps with CONSTRAINT_REASONING (#53) and DESIGN_DECISION (#54)."
    },
    "OPTION_COMPARISON": {
        "family": "COMPARISON",
        "modality": "PLAN_ONLY",
        "input_types": ["plan_variant_a", "plan_variant_b"],
        "target_type": "comparative_matrix",
        "grounding": "NO_PAIRED_VARIANTS",
        "status": "MISSING_EVIDENCE",
        "notes": "Corpus does not contain genuine design variants of identical envelopes."
    },
    "FEASIBILITY_ANALYSIS": {
        "family": "CONSTRUCTION LOGIC",
        "modality": "PLAN_TEXT",
        "input_types": ["floorplan", "structural_elements"],
        "target_type": "structural_impact_verdict",
        "grounding": "LOAD_BEARING_WALL_WIDTH",
        "status": "VALID",
        "notes": "Distinguishes thick shear walls (unremovable) from thin partitions."
    },

    # Group K: PEDAGOGY
    "EXPLANATION": {
        "family": "ARCHITECTURAL_VOCABULARY",
        "modality": "TEXT_ONLY",
        "input_types": ["concept_term"],
        "target_type": "pedagogical_definition_and_example",
        "grounding": "ARCHITECTURAL_THEORY",
        "status": "PARTIAL",
        "notes": "Text-only architectural theory definition (e.g. servant spaces)."
    },
    "STUDIO_CRITIQUE": {
        "family": "ERROR_DETECTION",
        "modality": "PLAN_ONLY",
        "input_types": ["student_floorplan"],
        "target_type": "formative_studio_feedback",
        "grounding": "TOPOLOGY_AND_FLOW",
        "status": "DUPLICATE",
        "notes": "Duplicate of PROJECT_CRITIQUE (#46) disguised with studio tutor tone."
    },
    "GUIDED_REASONING": {
        "family": "PLAN_UNDERSTANDING",
        "modality": "PLAN_TEXT",
        "input_types": ["floorplan", "guiding_prompt"],
        "target_type": "step_by_step_maieutic_trace",
        "grounding": "STEPWISE_TOPOLOGICAL_EVIDENCE",
        "status": "VALID",
        "notes": "Guided step-by-step spatial analysis without jumping to conclusion."
    },
    "ERROR_EXPLANATION": {
        "family": "ERROR_DETECTION",
        "modality": "PLAN_TEXT",
        "input_types": ["spatial_error_case"],
        "target_type": "root_cause_pedagogical_explanation",
        "grounding": "CONFLICT_GEOMETRY",
        "status": "DUPLICATE",
        "notes": "Duplicate of DESIGN_PROBLEM_DETECTION (#49)."
    },
    "METHODOLOGY_EXPLANATION": {
        "family": "ARCHITECTURAL_VOCABULARY",
        "modality": "TEXT_ONLY",
        "input_types": ["project_phase_query"],
        "target_type": "project_workflow_breakdown",
        "grounding": "LOI_MOP_ORDRE_ARCHITECTES",
        "status": "PARTIAL",
        "notes": "Text-only explanation of French project phases (ESQ, APS, APD, PRO)."
    },

    # Group L: MULTIMODAL
    "IMAGE_PLUS_PLAN": {
        "family": "CROSS-MODAL REASONING",
        "modality": "IMAGE_PLAN",
        "input_types": ["plan_2d", "interior_image_or_render"],
        "target_type": "viewpoint_localization_or_consistency_check",
        "grounding": "CROSS_REFERENCED_CAMERA_AND_PLAN",
        "status": "VALID",
        "notes": "Requires paired assets (e.g. ResBIM or IL3D render). True multimodal."
    },
    "PLAN_PLUS_TEXT": {
        "family": "CROSS-MODAL REASONING",
        "modality": "PLAN_TEXT",
        "input_types": ["floorplan", "textual_program"],
        "target_type": "program_compliance_verification",
        "grounding": "PLAN_COUNT_VS_TEXT_REQUIREMENT",
        "status": "VALID",
        "notes": "True multimodal: question cannot be answered without both modalities."
    },
    "PLAN_PLUS_3D": {
        "family": "CROSS-MODAL REASONING",
        "modality": "MULTIMODAL",
        "input_types": ["floorplan_2d", "ifc_or_3d_mesh"],
        "target_type": "2d_to_3d_spatial_concordance",
        "grounding": "PAIRED_RESBIM_IFC_AND_PLAN",
        "status": "VALID",
        "notes": "True multimodal: cross-checks vertical height / volume against 2D plan."
    },
    "IMAGE_PLUS_TEXT": {
        "family": "CROSS-MODAL REASONING",
        "modality": "IMAGE_TEXT",
        "input_types": ["interior_photo", "text_claim"],
        "target_type": "claim_verification_or_discrepancy",
        "grounding": "VISUAL_CONFIRMATION_VS_CLAIM",
        "status": "FAKE_MULTIMODAL",
        "notes": "High fake-multimodal risk if question asks for info already stated in text."
    },
    "IMAGE_PLUS_PLAN_PLUS_TEXT": {
        "family": "CROSS-MODAL REASONING",
        "modality": "IMAGE_PLAN_TEXT",
        "input_types": ["triplet_image_plan_text"],
        "target_type": "triplet_cross_validation",
        "grounding": "MMMU_ARCHITECTURE_PAIRS",
        "status": "MISSING_EVIDENCE",
        "notes": "Only 3 MMMU records exist in corpus; insufficient for bulk supervision."
    },
    "BIM_PLUS_PLAN": {
        "family": "CROSS-MODAL REASONING",
        "modality": "MULTIMODAL",
        "input_types": ["ifc_model", "floorplan_2d"],
        "target_type": "semantic_bim_to_graphic_2d_alignment",
        "grounding": "PAIRED_RESBIM_MODELS",
        "status": "VALID",
        "notes": "True multimodal: connects BIM semantic attributes to graphic representations."
    },
    "MULTIMODAL_PROJECT_REASONING": {
        "family": "CROSS-MODAL REASONING",
        "modality": "MULTIMODAL",
        "input_types": ["heterogeneous_project_packet"],
        "target_type": "holistic_synthesis",
        "grounding": "COMPLEX_AGGREGATE",
        "status": "UNDERSPECIFIED",
        "notes": "Too broad / vague to form an atomic verifiable training target."
    }
}

status_counts = Counter(v["status"] for v in TASK_AUDIT_SPECS.values())
print("=== FORENSIC TASK STATUS SUMMARY ===")
for s, c in status_counts.most_common():
    print(f"  {s:20s}: {c:2d} tasks")
print(f"Total: {len(TASK_AUDIT_SPECS)} tasks")
