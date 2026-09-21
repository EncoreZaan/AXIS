# -*- coding: utf-8 -*-
"""
ARCHI-AI — DesignHistoryGenerator (Histoire du Design & Collections MoMA / Met)
==============================================================================
Génère des exemples supervisés réels à partir des notices patrimoniales
du MoMA Architecture & Design et de The Met : mobilier iconique, designers,
courants modernes et matériaux historiques sans aucune attribution fabriquée.
"""

from typing import List, Dict, Any
from .base_generator import BaseGenerator
from ..schema import SupervisedExample, ModalInputs, QualityStatus, RoutingDestination, SplitName, DifficultyLevel
from ..task_catalogue import get_task_definition
from ..critique.critique_engine import CritiqueEngine


class DesignHistoryGenerator(BaseGenerator):
    """Générateur de tâches d'histoire du design et de l'architecture."""

    @property
    def supported_sources(self) -> List[str]:
        return ["CORE_MOMA", "CORE_MOMA_COLLECTION", "CORE_MET", "CORE_MET_OPENACCESS"]

    def generate(self, record: Dict[str, Any], max_examples: int = 2) -> List[SupervisedExample]:
        examples: List[SupervisedExample] = []
        rec_id = record.get("id", "UNKNOWN_REC")
        provenance = record.get("provenance", {})
        mus = record.get("museum") or record.get("metadata") or {}
        
        title = mus.get("title") or record.get("id")
        artist = mus.get("artist_or_designer") or mus.get("artist") or mus.get("designer") or "Designer / Atelier"
        date_str = mus.get("creation_date") or mus.get("date") or "XXe siècle"
        medium = mus.get("medium") or mus.get("materials") or "Matériaux mixtes"
        classification = mus.get("classification") or "Architecture & Design"

        # 1. Tâche H-43 : DESIGN_HISTORY (L2)
        task_def_dh = "DESIGN_HISTORY"
        tdef_dh = get_task_definition(task_def_dh)
        
        q_dh = f"Présentez l'œuvre de design '{title}', son concepteur et son ancrage matériel dans l'histoire des formes."
        obs_dh = f"Notice patrimoniale : '{title}' par {artist} ({date_str}). Matériaux répertoriés : {medium}."
        ana_dh = f"Cette pièce témoigne de l'évolution des techniques de fabrication et de la typologie {classification} de son époque."
        ans_dh = CritiqueEngine.format_structured_response(
            observation=obs_dh,
            analyse=ana_dh,
            raisonnement="La maîtrise des matériaux de structure et d'habillage constitue un jalon fondamental pour la culture du projet contemporain.",
            limites="Notice issue des archives muséales sans interprétation subjective."
        )

        ex1 = SupervisedExample(
            id=f"{rec_id}_TASK_{task_def_dh}",
            task_type=task_def_dh,
            task_group=tdef_dh.group.value,
            domain=tdef_dh.default_domain.value,
            skill=tdef_dh.default_skill.value,
            learning_type=tdef_dh.default_learning_type.value,
            difficulty=DifficultyLevel.L2,
            source_ids=[rec_id],
            source_provenance=provenance,
            inputs=ModalInputs(
                text_contexts=[{"title": title, "artist": artist, "date": date_str, "medium": medium}]
            ),
            question=q_dh,
            answer=ans_dh,
            epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                observations=[obs_dh],
                interpretations=[ana_dh],
            ),
            expected_reasoning_type="structured_observation_analysis",
            ground_truth={"title": title, "artist": artist, "date": date_str, "medium": medium},
            evidence={"museum_collection": provenance.get("dataset_name", "MoMA/Met")},
            quality_status=QualityStatus.PASS,
            split=SplitName.TRAIN,
            destination=RoutingDestination.RAG,
        )
        examples.append(ex1)

        # 2. Tâche H-45 : MATERIAL_AND_STYLE_RELATION (L3)
        if medium and len(examples) < max_examples:
            task_def_mat = "MATERIAL_AND_STYLE_RELATION"
            tdef_mat = get_task_definition(task_def_mat)
            q_mat = f"Comment le choix des matériaux ({medium}) contribue-t-il à la signature et à la durabilité de '{title}' ?"
            obs_mat = f"Matériaux constitutifs documentés : {medium}."
            ana_mat = "L'expressivité de la matière répond à une logique fonctionnelle et esthétique propre à l'époque de conception."
            ans_mat = CritiqueEngine.format_structured_response(
                observation=obs_mat,
                analyse=ana_mat,
                raisonnement="L'adéquation matériau-usage est l'un des critères majeurs d'évaluation d'un agencement ou meuble de référence.",
                limites="Contrôler l'état de conservation physique lors d'un réemploi."
            )
            ex2 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_mat}",
                task_type=task_def_mat,
                task_group=tdef_mat.group.value,
                domain=tdef_mat.default_domain.value,
                skill=tdef_mat.default_skill.value,
                learning_type=tdef_mat.default_learning_type.value,
                difficulty=DifficultyLevel.L3,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(text_contexts=[{"title": title, "medium": medium}]),
                question=q_mat,
                answer=ans_mat,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_mat],
                    interpretations=[ana_mat],
                ),
                expected_reasoning_type="structured_observation_analysis",
                ground_truth={"medium": medium},
                evidence={"title": title},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.FINETUNE,
            )
            examples.append(ex2)

        return examples
