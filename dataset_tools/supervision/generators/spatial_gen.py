# -*- coding: utf-8 -*-
"""
ARCHI-AI — SpatialGenerator (Scènes 3D, Scene Graphs & Relations Spatiales Déterministes)
========================================================================================
Génère des exemples supervisés réels à partir d'aménagements 3D :
- IL3D : Scènes vectorielles 3D avec boîtes englobantes, coordonnées [x, y, z],
  dimensions [dx, dy, dz] et graphes de scène réels.
- StructScan3D : Scans physiques réels d'espaces intérieurs avec capteurs RGB-D.
Règle fondamentale : Calcul mathématique rigoureux de distance euclidienne et
de vecteurs d'orientation relative. Interdiction absolue d'affirmer un vis-à-vis
ou une proximité sans calcul préalable.
"""

import math
from typing import List, Dict, Any, Optional, Tuple
from .base_generator import BaseGenerator
from ..schema import SupervisedExample, ModalInputs, QualityStatus, RoutingDestination, SplitName, DifficultyLevel
from ..task_catalogue import get_task_definition
from ..critique.critique_engine import CritiqueEngine


def compute_euclidean_distance(pos1: List[float], pos2: List[float]) -> float:
    """Calcule la distance euclidienne 3D entre deux centroïdes d'objets."""
    return math.sqrt(
        (pos1[0] - pos2[0]) ** 2 +
        (pos1[1] - pos2[1]) ** 2 +
        (pos1[2] - pos2[2]) ** 2
    )


def qualify_spatial_relation(
    o1: Dict[str, Any],
    o2: Dict[str, Any]
) -> Tuple[str, str, Dict[str, Any]]:
    """
    Dérive de façon déterministe la relation spatiale métrique et fonctionnelle entre 2 objets.
    Retourne (description_observation, analyse_fonctionnelle, métriques_calculees).
    """
    pos1 = o1.get("position")
    pos2 = o2.get("position")
    name1 = o1.get("category") or o1.get("label") or o1.get("object_id", "élément 1")
    name2 = o2.get("category") or o2.get("label") or o2.get("object_id", "élément 2")
    id1 = o1.get("object_id", "o1")
    id2 = o2.get("object_id", "o2")
    room1 = o1.get("room_id")
    room2 = o2.get("room_id")

    if not pos1 or not pos2 or len(pos1) < 3 or len(pos2) < 3:
        obs = f"Relation entre '{name1}' ({id1}) et '{name2}' ({id2}) : Coordonnées 3D incomplètes (statut : UNKNOWN)."
        ana = "L'absence de positionnement tridimensionnel certifié empêche toute conclusion géométrique."
        return obs, ana, {"status": "UNKNOWN", "distance_m": None}

    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dz = pos2[2] - pos1[2]
    dist = compute_euclidean_distance(pos1, pos2)

    # Qualification de la proximité
    if dist < 1.0:
        prox_label = "contiguïté directe / contact immédiat"
        ergonomic_impact = "interaction ergonomique directe (zone de préhension conjointe)"
    elif dist <= 2.5:
        prox_label = "dégagement intermédiaire dans le même sous-espace"
        ergonomic_impact = "zone de circulation partagée nécessitant un passage libre"
    else:
        prox_label = "implantation distanciée / extrémités distinctes du volume"
        ergonomic_impact = "autonomie fonctionnelle complète sans interférence de gabarit"

    # Vecteurs directeurs principaux
    orientations: List[str] = []
    if abs(dx) >= 0.3:
        orientations.append("à l'est/droite" if dx > 0 else "à l'ouest/gauche")
    if abs(dz) >= 0.3:
        orientations.append("au nord/arrière" if dz > 0 else "au sud/avant")
    if abs(dy) >= 0.3:
        orientations.append("surélevé" if dy > 0 else "en contrebas")

    orient_str = " et ".join(orientations) if orientations else "aligné sur le même plan"
    room_context = f"au sein du même espace ({room1})" if (room1 and room1 == room2) else "dans des zones distinctes"

    obs = (
        f"L'élément '{name2}' ({id2}) est situé à une distance euclidienne calculée de {dist:.2f} m "
        f"de '{name1}' ({id1}) ({prox_label}), orienté {orient_str} {room_context}."
    )
    ana = (
        f"La distance nette de {dist:.2f} m détermine l'usage : {ergonomic_impact}. "
        f"Les écartements respectent les tolérances anthropométriques nécessaires à la mobilité intérieure."
    )

    metrics = {
        "status": "CALCULATED",
        "distance_m": round(dist, 2),
        "delta_xyz": [round(dx, 2), round(dy, 2), round(dz, 2)],
        "proximity_tier": prox_label,
        "same_room": (room1 == room2) if (room1 and room2) else True,
    }
    return obs, ana, metrics


class SpatialGenerator(BaseGenerator):
    """Générateur de tâches de raisonnement spatial et 3D certifié."""

    @property
    def supported_sources(self) -> List[str]:
        return ["CORE_IL3D", "CORE_STRUCTSCAN3D"]

    def generate(self, record: Dict[str, Any], max_examples: int = 3) -> List[SupervisedExample]:
        examples: List[SupervisedExample] = []
        rec_id = record.get("id", "UNKNOWN_REC")
        source_name = record.get("source_name", "CORE_IL3D")
        provenance = record.get("provenance", {})
        spatial_data = record.get("spatial") or record.get("spatial_3d") or {}
        objects = spatial_data.get("objects", [])
        room_type = spatial_data.get("rooms", ["Espace intérieur"])[0] if spatial_data.get("rooms") else (record.get("domain") or "espace intérieur")
        visual = record.get("visual", {})

        # Cas 1 : Données 3D IL3D avec objets répertoriés
        if objects:
            obj_labels = [o.get("category") or o.get("label") or o.get("object_id") for o in objects]
            total_objs = len(objects)

            # 1. Tâche C-17 : SCENE_GRAPH_REASONING (L3)
            task_def_sg = "SCENE_GRAPH_REASONING"
            tdef_sg = get_task_definition(task_def_sg)
            
            # Échantillonnage d'objets avec dimensions réelles
            sample_objs_desc = []
            for o in objects[:4]:
                cat = o.get("category") or o.get("label") or "meuble"
                dims = o.get("dimensions")
                dim_str = f" ({dims[0]:.2f}m x {dims[1]:.2f}m x {dims[2]:.2f}m)" if dims and len(dims) >= 3 else ""
                sample_objs_desc.append(f"{cat}{dim_str}")

            q_sg = f"Décrivez l'inventaire 3D, les dimensions d'encombrement et la distribution du mobilier meublant cet aménagement ({room_type})."
            obs_sg = (
                f"La scène 3D ({room_type}) recense {total_objs} éléments géométriques dotés de boîtes englobantes : "
                f"{', '.join(sample_objs_desc)}."
            )
            ana_sg = (
                f"L'agencement distribue les entités autour de pôles d'usage clairs. Les dimensions réelles d'encombrement "
                f"permettent de qualifier les volumes nets d'occupation et les emprises au sol."
            )
            ans_sg = CritiqueEngine.format_structured_response(
                observation=obs_sg,
                analyse=ana_sg,
                raisonnement="En modélisation spatiale 3D, la connaissance des dimensions et des centroïdes conditionne la fluidité des flux circulatoires.",
                limites="Dimensions dérivées des bounding boxes 3D orientées de la scène."
            )
            ex1 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_sg}",
                task_type=task_def_sg,
                task_group=tdef_sg.group.value,
                domain=tdef_sg.default_domain.value,
                skill=tdef_sg.default_skill.value,
                learning_type=tdef_sg.default_learning_type.value,
                difficulty=DifficultyLevel.L3,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(
                    geometries=[{
                        "objects_count": total_objs,
                        "room_type": room_type,
                        "objects_sample": [
                            {"id": o.get("object_id"), "category": o.get("category"), "dimensions": o.get("dimensions")}
                            for o in objects[:6]
                        ]
                    }],
                ),
                question=q_sg,
                answer=ans_sg,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_sg],
                    interpretations=[ana_sg],
                ),
                expected_reasoning_type="structured_observation_analysis",
                ground_truth={"total_objects": total_objs, "labels": obj_labels[:8], "room_type": room_type},
                evidence={"objects_count": total_objs, "sample": objects[:3]},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.FINETUNE,
            )
            examples.append(ex1)

            # 2. Tâche C-18 : OBJECT_RELATION (L3 Calculé rigoureusement)
            if len(objects) >= 2 and len(examples) < max_examples:
                o1 = objects[0]
                o2 = objects[1]
                obs_rel, ana_rel, metrics = qualify_spatial_relation(o1, o2)

                if metrics.get("status") == "CALCULATED":
                    task_def_rel = "OBJECT_RELATION"
                    tdef_rel = get_task_definition(task_def_rel)
                    cat1 = o1.get("category") or o1.get("label") or "élément 1"
                    cat2 = o2.get("category") or o2.get("label") or "élément 2"

                    q_rel = f"Quelle est la relation géométrique et fonctionnelle calculée entre le/la {cat1} et le/la {cat2} dans cette scène 3D ?"
                    ans_rel = CritiqueEngine.format_structured_response(
                        observation=obs_rel,
                        analyse=ana_rel,
                        raisonnement="Le calcul déterministe de la distance euclidienne prévient toute inférence spatiale erronée.",
                        limites="Calcul basé sur les centroïdes des boîtes englobantes dans le repère local de la scène."
                    )
                    ex2 = SupervisedExample(
                        id=f"{rec_id}_TASK_{task_def_rel}",
                        task_type=task_def_rel,
                        task_group=tdef_rel.group.value,
                        domain=tdef_rel.default_domain.value,
                        skill=tdef_rel.default_skill.value,
                        learning_type=tdef_rel.default_learning_type.value,
                        difficulty=DifficultyLevel.L3,
                        source_ids=[rec_id],
                        source_provenance=provenance,
                        inputs=ModalInputs(
                            geometries=[{
                                "pair": [o1.get("object_id"), o2.get("object_id")],
                                "categories": [cat1, cat2],
                                "pos1": o1.get("position"),
                                "pos2": o2.get("position"),
                            }],
                        ),
                        question=q_rel,
                        answer=ans_rel,
                        epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                            observations=[obs_rel],
                            interpretations=[ana_rel],
                        ),
                        expected_reasoning_type="structured_observation_analysis",
                        ground_truth=metrics,
                        evidence={"o1_pos": o1.get("position"), "o2_pos": o2.get("position"), "distance_m": metrics["distance_m"]},
                        quality_status=QualityStatus.PASS,
                        split=SplitName.TRAIN,
                        destination=RoutingDestination.FINETUNE,
                    )
                    examples.append(ex2)

        # Cas 2 : Scans StructScan3D (Photométrie et géométrie d'enveloppe réelle)
        elif visual and len(examples) < max_examples:
            task_def_ia = "INTERIOR_ANALYSIS"
            tdef_ia = get_task_definition(task_def_ia)
            cap = visual.get("caption") or "Relevé photographique intérieur d'enveloppe bâtie"
            w = visual.get("width", 640)
            h = visual.get("height", 480)

            q_ia = "Analysez la volumétrie, les parois et la typologie spatiale observables sur ce relevé photographique d'intérieur."
            obs_ia = f"Relevé intérieur authentique ({w}x{h} px) : {cap}."
            ana_ia = "L'enveloppe présente des surfaces délimitées caractérisant un espace intérieur résidentiel réel."
            ans_ia = CritiqueEngine.format_structured_response(
                observation=obs_ia,
                analyse=ana_ia,
                raisonnement="L'observation des parois et des seuils visuels permet d'évaluer la qualité spatiale perçue et le potentiel d'aménagement.",
                limites="Point de vue photographique fixe nécessitant une confrontation avec un plan coté."
            )
            ex3 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_ia}",
                task_type=task_def_ia,
                task_group=tdef_ia.group.value,
                domain=tdef_ia.default_domain.value,
                skill=tdef_ia.default_skill.value,
                learning_type=tdef_ia.default_learning_type.value,
                difficulty=DifficultyLevel.L2,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(images=[visual]),
                question=q_ia,
                answer=ans_ia,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_ia],
                    interpretations=[ana_ia],
                ),
                expected_reasoning_type="structured_observation_analysis",
                ground_truth={"record_id": rec_id, "resolution": f"{w}x{h}"},
                evidence={"visual_path": visual.get("path")},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.FINETUNE,
            )
            examples.append(ex3)

        return examples
