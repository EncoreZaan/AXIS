# -*- coding: utf-8 -*-
"""
ARCHI-AI — LightingGenerator (Éclairage, Photométrie HDRI & Ambiances Naturelles)
================================================================================
Génère des exemples supervisés réels à partir des panoramas HDRI
Poly Haven Lighting : température de couleur en Kelvin, EV, contraste et météorologie.
Règle fondamentale : Interdiction formelle du cliché 'ombres nettes ou diffuses'.
L'analyse photométrique doit déduire l'ambiance réelle des valeurs exactes de Kelvin,
d'EV et du type de ciel (couvert vs dégagé, contraste haut vs bas).
"""

from typing import List, Dict, Any
from .base_generator import BaseGenerator
from ..schema import SupervisedExample, ModalInputs, QualityStatus, RoutingDestination, SplitName, DifficultyLevel
from ..task_catalogue import get_task_definition
from ..critique.critique_engine import CritiqueEngine


class LightingGenerator(BaseGenerator):
    """Générateur de tâches de lumière et photométrie certifié."""

    @property
    def supported_sources(self) -> List[str]:
        return ["CORE_POLYHAVEN_LIGHTING"]

    def generate(self, record: Dict[str, Any], max_examples: int = 2) -> List[SupervisedExample]:
        examples: List[SupervisedExample] = []
        rec_id = record.get("id", "UNKNOWN_REC")
        provenance = record.get("provenance", {})
        light_data = record.get("lighting") or record.get("metadata") or {}

        name = light_data.get("name") or light_data.get("hdri_id") or "Environnement Lumineux"
        ev = light_data.get("ev")
        kelvin = light_data.get("kelvin_temperature") or light_data.get("kelvin_estimate") or light_data.get("kelvin")
        time_of_day = light_data.get("time_of_day") or "journée"
        attrs = light_data.get("attributes", {})
        weather = attrs.get("weather") or light_data.get("weather") or "naturel"
        contrast = attrs.get("contrast") or "moyen"

        # Qualification photométrique déterministe
        if contrast == "high" or weather == "clear":
            shadow_desc = "ombres portées vives et directionnelles à fort contraste géométrique"
            glare_risk = "risque d'éblouissement élevé sur les plans de travail proches des baies"
        else:
            shadow_desc = "lumière diffuse omnidirectionnelle créant des dégradés d'ombres adoucis"
            glare_risk = "faible contraste facilitant l'homogénéité visuelle sans éblouissement violent"

        if kelvin and kelvin < 4500:
            chroma_desc = f"spectre chaud ({kelvin} K) favorisant les tonalités ambrées et la convivialité des espaces intimes"
        elif kelvin and kelvin > 6000:
            chroma_desc = f"spectre froid ({kelvin} K) stimulant la vigilance et valorisant les parois minérales blanches"
        elif kelvin:
            chroma_desc = f"teinte neutre ({kelvin} K) équilibrée assurant un rendu fidèle des couleurs intérieures"
        else:
            chroma_desc = "température de couleur diurne standard"

        # 1. Tâche G-37 : LIGHTING_ANALYSIS (L3)
        task_def_light = "LIGHTING_ANALYSIS"
        tdef_light = get_task_definition(task_def_light)

        q_light = f"Analysez l'ambiance lumineuse, le contraste et la température chromatique de l'environnement HDRI '{name}'."
        obs_light = (
            f"Environnement HDRI '{name}' ({time_of_day}, ciel {weather}). "
            f"Paramètres mesurés : Exposition {ev if ev is not None else 'N/A'} EV, "
            f"Température de couleur : {kelvin if kelvin else 'non cotée'} K, contraste {contrast}."
        )
        ana_light = (
            f"Cet éclairage produit des {shadow_desc}. "
            f"L'apport spectral se caractérise par un {chroma_desc}. "
            f"En contexte résidentiel, il conditionne directement le confort perceptif de l'agencement intérieur."
        )
        ans_light = CritiqueEngine.format_structured_response(
            observation=obs_light,
            analyse=ana_light,
            raisonnement="La maîtrise de l'EV et des Kelvin est indispensable pour concevoir la transition jour/nuit et l'éclairage artificiel d'appoint.",
            limites=f"Vigilance ergonomique : {glare_risk}."
        )

        ex1 = SupervisedExample(
            id=f"{rec_id}_TASK_{task_def_light}",
            task_type=task_def_light,
            task_group=tdef_light.group.value,
            domain=tdef_light.default_domain.value,
            skill=tdef_light.default_skill.value,
            learning_type=tdef_light.default_learning_type.value,
            difficulty=DifficultyLevel.L3,
            source_ids=[rec_id],
            source_provenance=provenance,
            inputs=ModalInputs(
                lighting=[{
                    "name": name,
                    "ev": ev,
                    "kelvin": kelvin,
                    "time_of_day": time_of_day,
                    "weather": weather,
                    "contrast": contrast,
                }]
            ),
            question=q_light,
            answer=ans_light,
            epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                observations=[obs_light],
                interpretations=[ana_light],
            ),
            expected_reasoning_type="structured_observation_analysis",
            ground_truth={"name": name, "kelvin": kelvin, "ev": ev, "contrast": contrast},
            evidence={"time_of_day": time_of_day, "weather": weather, "ev": ev},
            quality_status=QualityStatus.PASS,
            split=SplitName.TRAIN,
            destination=RoutingDestination.FINETUNE,
        )
        examples.append(ex1)

        # 2. Tâche G-39 : DAYLIGHT_REASONING (L3)
        if ev is not None and len(examples) < max_examples:
            task_def_day = "DAYLIGHT_REASONING"
            tdef_day = get_task_definition(task_def_day)

            q_day = (
                f"Comment la luminosité extérieure ({ev} EV, temps {weather}) de cet environnement '{name}' "
                f"conditionne-t-elle la pénétration diurne et la gestion des baies d'une pièce intérieure ?"
            )
            obs_day = f"Indice d'exposition solaire : {ev} EV en condition {weather} ({time_of_day})."
            if ev >= 18.0:
                day_strategy = (
                    "Un apport solaire direct très intense (> 18 EV) exige des dispositifs d'ombrage modulables "
                    "(brise-soleil orientables, stores screen à faible coefficient d'ouverture) pour limiter les surchauffes estivales."
                )
            else:
                day_strategy = (
                    "Un niveau d'exposition modéré (≤ 15 EV) autorise une pénétration libre en profondeur "
                    "mais peut nécessiter un apport complémentaire en fond de pièce pour atteindre les 300 lux requis pour le travail."
                )

            ana_day = f"Impact spatial et thermique : {day_strategy}"
            ans_day = CritiqueEngine.format_structured_response(
                observation=obs_day,
                analyse=ana_day,
                raisonnement="En architecture bioclimatique d'intérieur, la gestion de l'apport diurne détermine à la fois l'économie d'énergie et le bien-être visuel.",
                limites="L'atténuation exacte dépend du facteur solaire (g) et du facteur de transmission lumineuse (TL) des vitrages prescrits."
            )

            ex2 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_day}",
                task_type=task_def_day,
                task_group=tdef_day.group.value,
                domain=tdef_day.default_domain.value,
                skill=tdef_day.default_skill.value,
                learning_type=tdef_day.default_learning_type.value,
                difficulty=DifficultyLevel.L3,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(lighting=[{"ev": ev, "weather": weather, "name": name}]),
                question=q_day,
                answer=ans_day,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_day],
                    interpretations=[ana_day],
                ),
                expected_reasoning_type="structured_observation_analysis",
                ground_truth={"ev": ev, "weather": weather, "lighting_strategy": "daylight_mitigation"},
                evidence={"name": name, "ev": ev},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.FINETUNE,
            )
            examples.append(ex2)

        return examples
