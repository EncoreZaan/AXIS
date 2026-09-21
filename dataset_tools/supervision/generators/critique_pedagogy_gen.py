# -*- coding: utf-8 -*-
"""
ARCHI-AI — CritiquePedagogyGenerator (Critique d'Atelier, Pédagogie & Arbitrage Réels)
=====================================================================================
Génère des exemples supervisés de haut niveau cognitif (L4 à L6) :
- PROJECT_CRITIQUE (L5) : Critique rigoureusement ancrée sur des faits observables :
  OBSERVATION → IMPACT → ANALYSE → PROBLÈME → JUSTIFICATION → RECOMMANDATION.
  Interdiction absolue des clichés ('claustra ajouré', 'filtre spatial générique').
- GUIDED_REASONING (L4) : Guidage maïeutique rattaché à une scène réelle.
  Interdiction formelle des inputs vides : notion, contexte, problème, niveau étudiant.
- TRADEOFF_ANALYSIS (L6) : Arbitrage multicontrainte explicite avec au moins 2 contraintes
  réelles et contradictoires documentées.
"""

from typing import List, Dict, Any, Optional
from .base_generator import BaseGenerator
from ..schema import SupervisedExample, ModalInputs, QualityStatus, RoutingDestination, SplitName, DifficultyLevel
from ..task_catalogue import get_task_definition
from ..taxonomy import SupervisionLearningType
from ..critique.critique_engine import CritiqueEngine


class CritiquePedagogyGenerator(BaseGenerator):
    """Générateur de tâches de critique architecturale et de pédagogie certifié."""

    @property
    def supported_sources(self) -> List[str]:
        return ["CORE_RESPLAN", "CORE_IL3D", "CORE_RESBIM_2D", "CORE_RESBIM_PAIRED"]

    def generate(self, record: Dict[str, Any], max_examples: int = 2) -> List[SupervisedExample]:
        examples: List[SupervisedExample] = []
        rec_id = record.get("id", "UNKNOWN_REC")
        source_name = record.get("source_name", "CORE_RESPLAN")
        provenance = record.get("provenance", {})
        plan_geom = record.get("floorplan") or record.get("plan_geometry") or {}
        rooms = plan_geom.get("rooms", [])
        visual = record.get("visual", {})
        spatial_3d = record.get("spatial") or record.get("spatial_3d") or {}
        objects_3d = spatial_3d.get("objects", [])

        if not rooms and not objects_3d:
            return examples

        room_names = [r.get("name") for r in rooms if r.get("name")]
        total_rooms = len(rooms) or len(objects_3d)
        total_area = plan_geom.get("total_area_m2") or sum(r.get("area_m2", 0) for r in rooms)

        # -------------------------------------------------------------
        # 1. Tâche I-46 : PROJECT_CRITIQUE (L5 Expert, Ancrée sur Faits Réels)
        # -------------------------------------------------------------
        task_def_crit = "PROJECT_CRITIQUE"
        tdef_crit = get_task_definition(task_def_crit)

        # Analyse des singularités observables réelles du plan
        direct_living_bed = [
            r.get("name") for r in rooms
            if "bed" in (r.get("category") or r.get("name", ""))
            and any("living" in c for c in r.get("connected_rooms", []))
        ]
        isolated_baths = [
            r.get("name") for r in rooms
            if "bath" in (r.get("category") or r.get("name", ""))
            and not r.get("connected_rooms")
        ]

        if direct_living_bed:
            obs_crit = (
                f"Configuration spatiale ({total_rooms} pièces) : La chambre '{direct_living_bed[0]}' "
                f"débouche directement dans le séjour sans sas intermédiaire de distribution."
            )
            fric_crit = (
                f"Point de friction : La perméabilité directe entre le séjour et '{direct_living_bed[0]}' "
                f"crée une vulnérabilité acoustique immédiate et une rupture d'intimité lors de réceptions."
            )
            recom_crit = (
                f"Intercaler un vestibule de décompression ou inverser le sens de battement de la porte "
                f"avec un retour de doublage acoustique pour découpler les zones d'usage."
            )
        elif total_area > 0 and total_rooms >= 4:
            living_area = sum(r.get("area_m2", 0) for r in rooms if "living" in (r.get("category") or r.get("name", "")))
            ratio_living = (living_area / total_area) * 100 if total_area > 0 else 30
            obs_crit = (
                f"Proportion spatiale : La zone de jour représente {ratio_living:.1f}% de la surface totale ({total_area:.1f} m²), "
                f"desservant {total_rooms} pièces ({', '.join(room_names[:5])})."
            )
            fric_crit = (
                "Point d'arbitrage : Un volume de jour généreux impose une compression des pièces satellites, "
                "pouvant contraindre les capacités de rangement fixe dans les dégagements."
            )
            recom_crit = (
                "Intégrer des linéaires de placards menuisés toute hauteur en doublage de couloir "
                "pour compenser l'optimisation surfacique des chambres."
            )
        else:
            obs_crit = (
                f"Aménagement intérieur structuré autour de {total_rooms} entités fonctionnelles "
                f"({', '.join(room_names[:5]) if room_names else 'mobilier répertorié'})."
            )
            fric_crit = (
                "Point de vigilance : Vérifier la continuité des largeurs utiles de passage (≥ 0,80 m) "
                "entre les différents sous-espaces pour prévenir tout rétrécissement d'usage."
            )
            recom_crit = (
                "Maintenir l'alignement des circulations majeures et éviter les décrochements de cloisons résiduels."
            )

        ana_crit = (
            "L'évaluation architecturale confronte la partition géométrique avec le confort psycho-spatial "
            "et les exigences de gradation entre sphère publique de réception et sphère privée de repos."
        )

        ans_crit = CritiqueEngine.format_structured_response(
            observation=obs_crit,
            analyse=ana_crit,
            raisonnement="Une critique d'atelier rigoureuse repose sur la corrélation objective entre géométrie observée, acoustique et intimité d'usage.",
            probleme=fric_crit,
            recommandation=recom_crit,
            limites="Vérifier la nature porteuse des voiles avant toute proposition de déplacement d'ouverture."
        )

        ex1 = SupervisedExample(
            id=f"{rec_id}_TASK_{task_def_crit}",
            task_type=task_def_crit,
            task_group=tdef_crit.group.value,
            domain=tdef_crit.default_domain.value,
            skill=tdef_crit.default_skill.value,
            learning_type=tdef_crit.default_learning_type.value,
            difficulty=DifficultyLevel.L5,
            source_ids=[rec_id],
            source_provenance=provenance,
            inputs=ModalInputs(
                plans=[visual] if visual else [],
                geometries=[{
                    "rooms_inventory": room_names[:8],
                    "total_rooms": total_rooms,
                    "total_area_m2": round(total_area, 2) if total_area else None,
                    "direct_living_connections": direct_living_bed,
                }],
            ),
            question="Proposez une critique architecturale argumentée de cet aménagement intérieur comme lors d'un jury d'atelier.",
            answer=ans_crit,
            epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                observations=[obs_crit],
                interpretations=[ana_crit],
                inferences=[fric_crit],
                to_verifys=["Vérifier la descente de charges structurelle avant modification de cloison"],
            ),
            expected_reasoning_type="observation_to_critique",
            ground_truth={"total_rooms": total_rooms, "critical_frictions": [fric_crit]},
            evidence={"rooms": room_names[:4], "area_m2": round(total_area, 2) if total_area else None},
            quality_status=QualityStatus.PASS,
            split=SplitName.TRAIN,
            destination=RoutingDestination.FINETUNE,
        )
        examples.append(ex1)

        # -------------------------------------------------------------
        # 2. Tâche K-60 : GUIDED_REASONING (L4 Maïeutique Studio avec Inputs Non Vides)
        # -------------------------------------------------------------
        if len(examples) < max_examples:
            task_def_guide = "GUIDED_REASONING"
            tdef_guide = get_task_definition(task_def_guide)

            pedagogy_metadata = {
                "studio_session": "Atelier de Projet — Architecture Intérieure & Espace Habité",
                "pedagogical_notion": "Séquence d'accès, seuil d'intimité et gestion des flux",
                "student_level": "Deuxième cycle / Studio Master Architecture Intérieure",
                "target_plan": rec_id,
            }

            q_guide = (
                f"En tant qu'enseignant de studio d'architecture intérieure, guidez-moi par maïeutique "
                f"pour identifier les points de friction circulatoires de ce plan ({total_rooms} pièces), "
                f"sans me donner la solution immédiatement."
            )
            fric_obs = (
                f"Examinez précisément l'enchaînement des circulations depuis l'entrée vers les pièces "
                f"({', '.join(room_names[:4]) if room_names else 'volumes intérieurs'})."
            )
            clue = (
                "Quel conflit d'usage apparaît lorsqu'un occupant traverse le séjour pour rejoindre la zone nuit "
                "pendant qu'une activité collective a lieu dans la pièce principale ?"
            )
            principe = (
                "Principe de gradation spatiale : Un aménagement équilibré ménage une hiérarchie "
                "public → semi-privé → intime, évitant que la pièce de séjour ne serve de simple couloir traversant."
            )
            exercice = (
                "Tracez au calque les axes de circulation primaire (vitesse) et secondaire (desserte), "
                "puis quantifiez le pourcentage de surface de séjour neutralisé par les cônes de passage."
            )

            ans_guide = CritiqueEngine.build_maieutic_dialogue(
                observed_friction=fric_obs,
                clue_question=clue,
                guiding_principle=principe,
                follow_up_step=exercice,
            )

            ex2 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_guide}",
                task_type=task_def_guide,
                task_group=tdef_guide.group.value,
                domain=tdef_guide.default_domain.value,
                skill=tdef_guide.default_skill.value,
                learning_type=SupervisionLearningType.MAIEUTIC_GUIDANCE.value,
                difficulty=DifficultyLevel.L4,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(
                    plans=[visual] if visual else [],
                    geometries=[{"room_count": total_rooms, "rooms": room_names[:6]}],
                    text_contexts=[pedagogy_metadata],
                ),
                question=q_guide,
                answer=ans_guide,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[fric_obs],
                    interpretations=[clue],
                    inferences=[principe],
                ),
                expected_reasoning_type="maieutic_guidance",
                ground_truth={
                    "pedagogy_mode": "maieutic",
                    "notion": pedagogy_metadata["pedagogical_notion"],
                    "student_level": pedagogy_metadata["student_level"],
                },
                evidence={"plan_context": rec_id, "pedagogy_framework": pedagogy_metadata["studio_session"]},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.FINETUNE,
            )
            examples.append(ex2)

        # -------------------------------------------------------------
        # 3. Tâche J-55 : TRADEOFF_ANALYSIS (L6 Multicontrainte Explicite)
        # -------------------------------------------------------------
        if len(examples) < max_examples + 1:
            task_def_to = "TRADEOFF_ANALYSIS"
            tdef_to = get_task_definition(task_def_to)

            constraints_matrix = [
                {
                    "name": "Lumiere_Naturelle",
                    "description": "Maximiser l'éclairement diurne et les perspectives visuelles profondes",
                    "polarite": "Ouverture des volumes et suppression des cloisons opaques",
                },
                {
                    "name": "Isolation_Acoustique",
                    "description": "Garantir un affaiblissement acoustique (Rw ≥ 42 dB) pour les zones de repos/travail",
                    "polarite": "Fermeture des baies et présence de parois massives séparatives",
                },
            ]

            q_to = (
                f"Analysez l'arbitrage multicontrainte de ce projet ({total_rooms} pièces) : "
                f"comment concilier la recherche de luminosité naturelle traversante avec les exigences d'isolation acoustique ?"
            )
            obs_to = (
                f"Configuration spatiale ({total_rooms} pièces répertoriées : {', '.join(room_names[:5])}). "
                f"Deux impératifs contradictoires s'opposent : la demande d'ouverture spatiale pour la lumière "
                f"et le besoin de séparation physique pour le confort sonore."
            )
            ana_to = (
                "Le décloisonnement intégral amplifie la sensation volumétrique mais dégrade la performance acoustique. "
                "L'arbitrage optimal consiste à introduire des séparations translucides (châssis vitrés à double vitrage acoustique) "
                "qui laissent cheminer le flux lumineux tout en maintenant l'atténuation phonique requise."
            )
            fric_to = (
                "Compromis d'arbitrage : La transparence visuelle n'offre pas l'intimité occultante nécessaire au repos "
                "sans ajout de rideaux phoniques absorbants lourds."
            )
            recom_to = (
                "Prescrire une cloison vitrée avec vitrage feuilleté Silence (33.2 ou 44.2) "
                "et des rideaux en velours absorbant à l'intérieur de la pièce intime."
            )
            ans_to = CritiqueEngine.format_structured_response(
                observation=obs_to,
                analyse=ana_to,
                raisonnement="En architecture intérieure de haut niveau, l'arbitrage n'est pas un compromis affaiblissant mais une synthèse constructive intégrant les polarités divergentes.",
                probleme=fric_to,
                recommandation=recom_to,
                limites="Intégrer le coût spécifique du vitrage acoustique feuilleté dans l'enveloppe budgétaire prévisionnelle."
            )

            ex3 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_to}",
                task_type=task_def_to,
                task_group=tdef_to.group.value,
                domain=tdef_to.default_domain.value,
                skill=tdef_to.default_skill.value,
                learning_type=tdef_to.default_learning_type.value,
                difficulty=DifficultyLevel.L6,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(
                    plans=[visual] if visual else [],
                    geometries=[{"room_count": total_rooms, "rooms": room_names[:6]}],
                    text_contexts=[{"tradeoff_matrix": constraints_matrix}],
                ),
                question=q_to,
                answer=ans_to,
                constraints=[
                    "Lumiere_Naturelle : maximiser l'éclairement diurne et les perspectives visuelles profondes",
                    "Isolation_Acoustique : garantir un affaiblissement acoustique (Rw ≥ 42 dB) pour les zones de repos/travail",
                ],
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_to],
                    interpretations=[ana_to],
                    inferences=[fric_to],
                ),
                expected_reasoning_type="observation_to_critique",
                ground_truth={
                    "tradeoff_axes": ["luminosite_naturelle", "isolation_acoustique"],
                    "constraints_count": len(constraints_matrix),
                    "level": "L6_MULTICONTRAINTE",
                },
                evidence={"rooms_count": total_rooms, "constraints": constraints_matrix},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.FINETUNE,
            )
            examples.append(ex3)

        return examples
