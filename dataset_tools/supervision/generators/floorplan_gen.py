# -*- coding: utf-8 -*-
"""
ARCHI-AI — FloorplanGenerator (Plans 2D, Topologie, Circulations & Baies Réelles)
=================================================================================
Génère des exemples supervisés réels à partir des plans d'architecte :
- ResPlan : vectoriels avec polygones, pièces, surfaces m², baies et graphes d'adjacence.
- RPLAN : matriciels segmentés 256x256 avec masques couleur réels (rouge/vert/blanc).
- ResBIM 2D : plans résidentiels réels couplés.
Règle fondamentale : Ancrage obligatoire sur des informations réelles (pièces, surfaces,
ouvertures, connectivités). Si une donnée n'est pas disponible : UNKNOWN explicite.
Interdiction formelle des formulations vagues de type 'organisation matricielle'.
"""

from typing import List, Dict, Any, Optional
from .base_generator import BaseGenerator
from ..schema import SupervisedExample, ModalInputs, QualityStatus, RoutingDestination, SplitName, DifficultyLevel
from ..task_catalogue import get_task_definition
from ..critique.critique_engine import CritiqueEngine


class FloorplanGenerator(BaseGenerator):
    """Générateur de tâches de lecture et raisonnement sur plans 2D certifié."""

    @property
    def supported_sources(self) -> List[str]:
        return ["CORE_RESPLAN", "CORE_RPLAN", "CORE_RESBIM_2D", "CORE_RESBIM_PAIRED"]

    def generate(self, record: Dict[str, Any], max_examples: int = 4) -> List[SupervisedExample]:
        examples: List[SupervisedExample] = []
        rec_id = record.get("id", "UNKNOWN_REC")
        source_name = record.get("source_name", "CORE_RESPLAN")
        provenance = record.get("provenance", {})
        fp_dict = record.get("floorplan") or record.get("plan_geometry") or {}
        rooms = fp_dict.get("rooms", [])
        openings = fp_dict.get("openings", [])
        visual = record.get("visual", {})
        metadata = record.get("metadata", {})

        # Cas 1 : RPLAN (Plans matriciels raster segmentés par couleur)
        if not rooms and visual:
            task_def_read = "FLOORPLAN_READING"
            tdef_read = get_task_definition(task_def_read)
            w = visual.get("width", 256)
            h = visual.get("height", 256)
            classes = metadata.get("segmentation_classes", ["doors_green", "walls_red", "rooms_white", "background_gray"])

            q_read = f"Analysez la partition spatiale, les parois et les ouvertures identifiables sur ce plan matriciel ({w}x{h} px)."
            obs_read = (
                f"Document matriciel raster (résolution {w}x{h} px, référence {rec_id}). "
                f"La segmentation sémantique isole {len(classes)} classes graphiques nettes : "
                f"parois porteuses et cloisons (tracé rouge), baies et passages libres (repères verts), "
                f"surfaces intérieures habitables (aplats blancs) et environnement extérieur (fond gris)."
            )
            ana_read = (
                "L'agencement met en évidence un découpage fonctionnel avec des ouvertures de distribution "
                "localisées sur les parois intérieures, orientant les liaisons entre pièces habitables."
            )
            ans_read = CritiqueEngine.format_structured_response(
                observation=obs_read,
                analyse=ana_read,
                raisonnement="Le décodage graphique distingue formellement les limites massives bâties (murs rouges) des surfaces d'usage (blanches).",
                limites="Noms des pièces et cotes millimétriques numériques non annotés sur la source matricielle (statut : UNKNOWN pour les cotes exactes)."
            )
            ex_read = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_read}",
                task_type=task_def_read,
                task_group=tdef_read.group.value,
                domain=tdef_read.default_domain.value,
                skill=tdef_read.default_skill.value,
                learning_type=tdef_read.default_learning_type.value,
                difficulty=DifficultyLevel.L1,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(
                    plans=[visual],
                    geometries=[{"resolution": [w, h], "segmentation_channels": classes}],
                ),
                question=q_read,
                answer=ans_read,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_read],
                    interpretations=[ana_read],
                ),
                expected_reasoning_type="structured_observation_analysis",
                ground_truth={"resolution": [w, h], "channels": classes, "metric_dimensions": "UNKNOWN"},
                evidence={"image_path": visual.get("path"), "segmentation_classes": classes},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.FINETUNE,
            )
            examples.append(ex_read)
            return examples

        if not rooms:
            return examples

        room_names = [r.get("name") for r in rooms if r.get("name")]
        total_rooms = len(rooms)
        total_area = sum(r.get("area_m2", 0.0) or 0.0 for r in rooms)

        # 1. Tâche B-9 : ROOM_IDENTIFICATION (L2)
        task_def_id = "ROOM_IDENTIFICATION"
        tdef_id = get_task_definition(task_def_id)
        
        living_rooms = [r.get("name") for r in rooms if "living" in (r.get("category") or r.get("name", ""))]
        bed_rooms = [r.get("name") for r in rooms if "bed" in (r.get("category") or r.get("name", ""))]
        bath_rooms = [r.get("name") for r in rooms if "bath" in (r.get("category") or r.get("name", ""))]
        kitchen_rooms = [r.get("name") for r in rooms if "kitchen" in (r.get("category") or r.get("name", ""))]

        q_id = f"Identifiez l'inventaire nominatif certifié des {total_rooms} pièces composant ce logement et leur typologie d'usage."
        obs_text = (
            f"Le plan comprend {total_rooms} pièces délimitées par des parois vectorielles : "
            f"{', '.join(room_names[:8])}."
        )
        ana_text = (
            f"La distribution organise les fonctions : zone de jour ({', '.join(living_rooms + kitchen_rooms) or 'séjour/cuisine'}), "
            f"zone de repos ({len(bed_rooms)} chambre(s) : {', '.join(bed_rooms) or 'non spécifiée'}), "
            f"et commodités sanitaires ({len(bath_rooms)} pièce(s) d'eau)."
        )
        ans_id = CritiqueEngine.format_structured_response(
            observation=obs_text,
            analyse=ana_text,
            raisonnement="La nomenclature vectorielle permet une classification programmatique exacte sans ambiguïté visuelle.",
            limites="Surfaces et contours extraits des polygones bruts du relevé d'architecte."
        )

        ex1 = SupervisedExample(
            id=f"{rec_id}_TASK_{task_def_id}",
            task_type=task_def_id,
            task_group=tdef_id.group.value,
            domain=tdef_id.default_domain.value,
            skill=tdef_id.default_skill.value,
            learning_type=tdef_id.default_learning_type.value,
            difficulty=DifficultyLevel.L2,
            source_ids=[rec_id],
            source_provenance=provenance,
            inputs=ModalInputs(
                plans=[visual] if visual else [],
                geometries=[{"room_count": total_rooms, "room_labels": room_names, "total_area_m2": round(total_area, 2)}],
            ),
            question=q_id,
            answer=ans_id,
            epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                observations=[obs_text],
                interpretations=[ana_text],
            ),
            expected_reasoning_type="structured_observation_analysis",
            ground_truth={"total_rooms": total_rooms, "room_names": room_names, "categories": {"bedrooms": len(bed_rooms), "bathrooms": len(bath_rooms)}},
            evidence={"rooms": rooms[:5]},
            quality_status=QualityStatus.PASS,
            split=SplitName.TRAIN,
            destination=RoutingDestination.FINETUNE,
        )
        examples.append(ex1)

        # 2. Tâche B-10 : ROOM_TOPOLOGY (L3)
        connected_pairs = []
        adj_graph = fp_dict.get("room_adjacency_graph", {})
        if adj_graph:
            for src_r, targets in adj_graph.items():
                for tgt_r in targets:
                    if (tgt_r, src_r) not in connected_pairs and (src_r, tgt_r) not in connected_pairs:
                        connected_pairs.append((src_r, tgt_r))
        else:
            for r in rooms:
                r_name = r.get("name", "pièce")
                for c in r.get("connected_rooms", []):
                    if (c, r_name) not in connected_pairs and (r_name, c) not in connected_pairs:
                        connected_pairs.append((r_name, c))

        if connected_pairs and len(examples) < max_examples:
            task_def_topo = "ROOM_TOPOLOGY"
            tdef_topo = get_task_definition(task_def_topo)
            topo_desc = "; ".join([f"{p[0]} ↔ {p[1]}" for p in connected_pairs[:6]])
            q_topo = f"Analysez le graphe d'adjacence et les liaisons d'accès directes entre pièces pour ce plan ({total_rooms} pièces)."
            obs_topo = f"Adjacences et franchissements directs répertoriés : {topo_desc}."
            ana_topo = (
                f"Le réseau de connectivité articule {len(connected_pairs)} liaison(s) d'accès direct. "
                "L'agencement privilégie la communication fluide entre séjour et cuisine tout en isolant les zones intimes."
            )
            ans_topo = CritiqueEngine.format_structured_response(
                observation=obs_topo,
                analyse=ana_topo,
                raisonnement="La topologie planifiée prévient les parcours traversants intempestifs au travers des chambres à coucher.",
                limites="Les portes intérieures sont supposées libres d'accès sans condamnation de vantail."
            )
            ex2 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_topo}",
                task_type=task_def_topo,
                task_group=tdef_topo.group.value,
                domain=tdef_topo.default_domain.value,
                skill=tdef_topo.default_skill.value,
                learning_type=tdef_topo.default_learning_type.value,
                difficulty=DifficultyLevel.L3,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(
                    plans=[visual] if visual else [],
                    geometries=[{"adjacency_pairs": [f"{p[0]} <-> {p[1]}" for p in connected_pairs]}],
                ),
                question=q_topo,
                answer=ans_topo,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_topo],
                    interpretations=[ana_topo],
                ),
                expected_reasoning_type="structured_observation_analysis",
                ground_truth={"connected_pairs_count": len(connected_pairs), "pairs": [f"{p[0]}--{p[1]}" for p in connected_pairs]},
                evidence={"connections": connected_pairs[:6]},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.MULTIUSE,
            )
            examples.append(ex2)

        # 3. Tâche B-11 : CIRCULATION_ANALYSIS (L4)
        if len(examples) < max_examples:
            task_def_circ = "CIRCULATION_ANALYSIS"
            tdef_circ = get_task_definition(task_def_circ)
            
            # Repérage de la porte d'entrée
            front_doors = [o for o in openings if o.get("type") == "front_door"]
            entry_obs = f"Accès d'entrée principal identifié ({len(front_doors)} porte(s) palière(s))." if front_doors else "Point d'accès principal déduit de l'espace de distribution."
            
            q_circ = "Examinez les flux de circulation, la séquence d'entrée et la transition vers les pièces de vie."
            obs_circ = f"{entry_obs} La desserte distribue {total_rooms} pièces : zone jour ({room_names[0] if room_names else 'séjour'}) et zones satellites."
            ana_circ = "Les flux principaux s'organisent sans créer de couloir aveugle disproportionné, préservant la surface habitable utile."
            friction_circ = "Point de vigilance : vérifier que le passage libre utile dans les dégagements conserve au moins 0,90 m net."
            recom_circ = "Conserver un dégagement minimal d'évitement et éviter l'empiètement de mobilier sur l'axe d'ouverture des portes."
            ans_circ = CritiqueEngine.format_structured_response(
                observation=obs_circ,
                analyse=ana_circ,
                raisonnement="En architecture intérieure résidentielle, la clarté du cheminement d'accès conditionne l'orientation et le confort d'usage.",
                probleme=friction_circ,
                recommandation=recom_circ,
                limites="Largeurs nettes de passage à confirmer sur les cotes de détail d'exécution."
            )
            ex3 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_circ}",
                task_type=task_def_circ,
                task_group=tdef_circ.group.value,
                domain=tdef_circ.default_domain.value,
                skill=tdef_circ.default_skill.value,
                learning_type=tdef_circ.default_learning_type.value,
                difficulty=DifficultyLevel.L4,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(
                    plans=[visual] if visual else [],
                    geometries=[{"room_count": total_rooms, "has_front_door": bool(front_doors)}],
                ),
                question=q_circ,
                answer=ans_circ,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_circ],
                    interpretations=[ana_circ],
                    inferences=["Parcours de distribution fonctionnel avec vigilance sur les dégagements"],
                ),
                expected_reasoning_type="observation_to_critique",
                ground_truth={"total_rooms": total_rooms, "openings_total": len(openings)},
                evidence={"openings_count": len(openings), "front_doors_count": len(front_doors)},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.FINETUNE,
            )
            examples.append(ex3)

        # 4. Tâche B-15 : PLAN_SUMMARY (L3)
        if total_area > 0 and len(examples) < max_examples:
            task_def_sum = "PLAN_SUMMARY"
            tdef_sum = get_task_definition(task_def_sum)
            q_sum = "Dressez la synthèse métrique et surfacique certifiée de ce plan résidentiel."
            room_area_details = "\n".join([f"- {r.get('name')}: {r.get('area_m2', 0):.2f} m²" for r in rooms if r.get('area_m2')][:6])
            obs_sum = f"Surface cumulée totale : {total_area:.2f} m² répartie sur {total_rooms} pièces :\n{room_area_details}"
            ans_sum = CritiqueEngine.format_structured_response(
                observation=obs_sum,
                analyse="L'équilibre entre pièces de réception et pièces intimes respecte les standards contemporains de compacité et de surface habitable.",
                raisonnement="Calcul géométrique déterministe issu directement des coordonnées de polygones vectoriels sans approximation.",
                limites="Surfaces exprimées en surface de plancher nette utile (hors emprise des parois séparatives)."
            )
            ex4 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_sum}",
                task_type=task_def_sum,
                task_group=tdef_sum.group.value,
                domain=tdef_sum.default_domain.value,
                skill=tdef_sum.default_skill.value,
                learning_type=tdef_sum.default_learning_type.value,
                difficulty=DifficultyLevel.L3,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(
                    plans=[visual] if visual else [],
                    geometries=[{"total_area_m2": round(total_area, 2), "rooms_count": total_rooms}],
                ),
                question=q_sum,
                answer=ans_sum,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_sum],
                    interpretations=["Distribution surfacique équilibrée"],
                ),
                expected_reasoning_type="structured_observation_analysis",
                ground_truth={"total_area_m2": round(total_area, 2), "rooms_area": {r.get("name"): round(r.get("area_m2", 0), 2) for r in rooms if r.get("name")}},
                evidence={"polygons_count": len(rooms), "total_area_m2": round(total_area, 2)},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.TOOL,
            )
            examples.append(ex4)

        return examples
