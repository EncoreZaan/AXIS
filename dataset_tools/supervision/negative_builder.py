# -*- coding: utf-8 -*-
"""
ARCHI-AI — Constructeur de Hard Negatives & Paires de Contre-Exemples (Negative Builder V2)
========================================================================================
Construit des paires formelles pédagogiques [CORRECT vs PLAUSIBLE_BUT_WRONG] :
Types supportés :
- wrong_dimension (erreur de cote de passage, violation PMR invisible au coup d'œil)
- wrong_room_relation (fausse contiguïté topologique ou inversion d'adjacence)
- wrong_plan_interpretation (confusion symbole porte battante vs porte à galandage)
- wrong_scale (supposition arbitraire d'échelle métrique sur raster non calibré)
- wrong_bim_relation (entité affectée au mauvais niveau ou mauvaise classe IFC)
- unsupported_claim (affirmation séduisante mais absente des documents graphiques)
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class NegativeAnnotation(BaseModel):
    negative_type: str
    perturbed_assertion: str
    why_wrong: str
    evidence: Dict[str, Any]
    correct_interpretation: str


class CounterexamplePair(BaseModel):
    pair_id: str
    task_id: str
    difficulty: str
    question: str
    correct_example_id: str
    correct_answer: str
    counterexample_id: str
    counterexample_answer: str
    negative_annotation: NegativeAnnotation


class NegativeBuilder:
    """Générateur de contre-exemples architecturaux à haute valeur pédagogique."""

    @staticmethod
    def create_dimension_negative(
        base_id: str,
        task_id: str,
        question: str,
        valid_answer: str,
        measured_value_m: float,
        threshold_m: float,
        norm_name: str
    ) -> CounterexamplePair:
        """Crée un contre-exemple sur une erreur subtile de dimensionnement."""
        pair_id = f"PAIR_{base_id}_DIM"
        # Plausible but wrong: inversion du statut de conformité
        is_compliant = measured_value_m >= threshold_m
        delta_cm = abs(measured_value_m - threshold_m) * 100.0

        if is_compliant:
            perturbed = (
                f"Le passage utile mesuré ({measured_value_m:.2f} m) est insuffisant "
                f"et ne respecte pas le seuil minimal de {threshold_m:.2f} m exigé par {norm_name}."
            )
            why_wrong = (
                f"Erreur d'appréciation géométrique : la cote réelle est de {measured_value_m:.2f} m, "
                f"ce qui est supérieur ou égal au minimum réglementaire de {threshold_m:.2f} m."
            )
        else:
            perturbed = (
                f"Le dégagement observé ({measured_value_m:.2f} m) est pleinement conforme aux prescriptions "
                f"de {norm_name}, permettant une circulation fluide sans obstacle."
            )
            why_wrong = (
                f"Violation normative masquée : la cote mesurée ({measured_value_m:.2f} m) "
                f"est inférieure au seuil strict ({threshold_m:.2f} m) d'un écart de {delta_cm:.1f} cm."
            )

        annotation = NegativeAnnotation(
            negative_type="wrong_dimension",
            perturbed_assertion=perturbed,
            why_wrong=why_wrong,
            evidence={"measured_value_m": measured_value_m, "threshold_m": threshold_m, "norm": norm_name},
            correct_interpretation=valid_answer
        )

        return CounterexamplePair(
            pair_id=pair_id,
            task_id=task_id,
            difficulty="L4_RAISONNEMENT",
            question=question,
            correct_example_id=f"{base_id}_CORRECT",
            correct_answer=valid_answer,
            counterexample_id=f"{base_id}_HARD_NEGATIVE",
            counterexample_answer=perturbed,
            negative_annotation=annotation
        )

    @staticmethod
    def create_topology_negative(
        base_id: str,
        task_id: str,
        question: str,
        valid_answer: str,
        room_a: str,
        room_b: str,
        truly_connected: bool,
        via_door: Optional[str] = None
    ) -> CounterexamplePair:
        """Crée un contre-exemple sur une erreur de relation topologique."""
        pair_id = f"PAIR_{base_id}_TOPO"

        if truly_connected:
            perturbed = (
                f"Les espaces '{room_a}' et '{room_b}' sont strictement isolés sans passage direct, "
                f"nécessitant de traverser l'espace extérieur ou les circulations communes."
            )
            why_wrong = (
                f"Erreur de lecture topologique : une ouverture libre ou porte battante "
                f"assure une liaison directe franchissable entre '{room_a}' et '{room_b}'."
            )
        else:
            perturbed = (
                f"L'accès à la pièce '{room_b}' s'effectue directement depuis '{room_a}' "
                f"au moyen d'une baie de distribution directe."
            )
            why_wrong = (
                f"Fausse adjacence : une paroi continue étanche sépare '{room_a}' et '{room_b}'. "
                f"Aucune baie ne permet le franchissement direct entre ces deux volumes."
            )

        annotation = NegativeAnnotation(
            negative_type="wrong_room_relation",
            perturbed_assertion=perturbed,
            why_wrong=why_wrong,
            evidence={"room_a": room_a, "room_b": room_b, "direct_connection": truly_connected},
            correct_interpretation=valid_answer
        )

        return CounterexamplePair(
            pair_id=pair_id,
            task_id=task_id,
            difficulty="L3_ANALYSE",
            question=question,
            correct_example_id=f"{base_id}_CORRECT",
            correct_answer=valid_answer,
            counterexample_id=f"{base_id}_HARD_NEGATIVE",
            counterexample_answer=perturbed,
            negative_annotation=annotation
        )

    @staticmethod
    def create_unscaled_area_negative(
        base_id: str,
        task_id: str,
        question: str,
        valid_answer: str,
        pixel_count: int
    ) -> CounterexamplePair:
        """Crée un contre-exemple sur le piège critique de conversion pixel en m2."""
        pair_id = f"PAIR_{base_id}_UNSCALED"
        fake_m2 = pixel_count / 100.0  # Faux calcul arbitraire typique

        perturbed = (
            f"La surface de cette pièce est exactement de {fake_m2:.2f} m², "
            f"obtenue par la conversion directe du décompte de {pixel_count} pixels du plan."
        )
        why_wrong = (
            f"Anomalie critique d'échelle (UNSCALED_PIXEL_TRAP) : le plan ne dispose pas d'échelle physique "
            f"ou de barre étalon certifiée. Convertir {pixel_count} px en {fake_m2:.2f} m² est une hallucination mathématique."
        )

        annotation = NegativeAnnotation(
            negative_type="wrong_scale",
            perturbed_assertion=perturbed,
            why_wrong=why_wrong,
            evidence={"pixel_count": pixel_count, "scale_present": False},
            correct_interpretation=valid_answer
        )

        return CounterexamplePair(
            pair_id=pair_id,
            task_id=task_id,
            difficulty="L4_RAISONNEMENT",
            question=question,
            correct_example_id=f"{base_id}_CORRECT",
            correct_answer=valid_answer,
            counterexample_id=f"{base_id}_HARD_NEGATIVE",
            counterexample_answer=perturbed,
            negative_annotation=annotation
        )
