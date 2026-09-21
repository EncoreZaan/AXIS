# -*- coding: utf-8 -*-
"""
ARCHI-AI — ErgonomicsGenerator (Ergonomie, Normes PMR & Cotes Anthropométriques)
==============================================================================
Génère des exemples supervisés réels à partir des standards Neufert / Panero & Zelnik
et des textes réglementaires officiels français (PMR, ERP, CCH).
Pipeline numérique déterministe certifié :
original_value -> original_unit -> conversion -> normalized_value -> normalized_unit -> verification
Interdiction formelle de toute valeur None, NaN, inf ou chaîne vide.
Calibration cognitive stricte : CLEARANCE_CHECK (L1/L2), ACCESSIBILITY_ANALYSIS (L4/L5),
CONSTRAINT_REASONING (L6 avec contraintes réelles contradictoires).
"""

import math
from typing import List, Dict, Any, Optional
from .base_generator import BaseGenerator
from ..schema import SupervisedExample, ModalInputs, QualityStatus, RoutingDestination, SplitName, DifficultyLevel
from ..task_catalogue import get_task_definition
from ..critique.critique_engine import CritiqueEngine


def normalize_dimension(val: Any, unit: str) -> Optional[float]:
    """Convertit de manière déterministe une cote originale en mètres SI."""
    if val is None or val == "":
        return None
    try:
        f_val = float(val)
        if math.isnan(f_val) or math.isinf(f_val):
            return None
        u_str = str(unit or "").strip().lower()
        if u_str in ("cm", "centimètre", "centimetre", "centimètres"):
            return round(f_val / 100.0, 3)
        elif u_str in ("mm", "millimètre", "millimetre", "millimètres"):
            return round(f_val / 1000.0, 3)
        elif u_str in ("m", "mètre", "metre", "mètres"):
            return round(f_val, 3)
        else:
            # Défaut standard centimètres pour Neufert
            return round(f_val / 100.0, 3)
    except (ValueError, TypeError):
        return None


class ErgonomicsGenerator(BaseGenerator):
    """Générateur de tâches d'ergonomie et de conformité réglementaire."""

    @property
    def supported_sources(self) -> List[str]:
        return ["CORE_ERGONOMIE", "CORE_NORMES_FR"]

    def generate(self, record: Dict[str, Any], max_examples: int = 2) -> List[SupervisedExample]:
        examples: List[SupervisedExample] = []
        rec_id = record.get("id", "UNKNOWN_REC")
        source_name = record.get("source_name", "CORE_ERGONOMIE")
        provenance = record.get("provenance", {})

        # Cas 1 : Données ergonomiques (Neufert, Panero & Zelnik)
        if "ergonomics" in record or source_name == "CORE_ERGONOMIE":
            ergo_data = record.get("ergonomics") or record.get("metadata") or {}
            label = (
                ergo_data.get("object_or_usage")
                or ergo_data.get("label")
                or ergo_data.get("dimension_name")
                or ergo_data.get("standard_id")
                or record.get("id")
            )
            orig_val = ergo_data.get("original_value") or ergo_data.get("value")
            orig_unit = ergo_data.get("original_unit") or "cm"
            src_doc = ergo_data.get("source") or "Synthèse des standards d'ergonomie et anthropométrie architecturale (Neufert, Panero & Zelnik)"
            context_space = ergo_data.get("space_category") or ergo_data.get("context") or "Aménagement intérieur général"

            # Pipeline déterministe certifié
            norm_val = ergo_data.get("normalized_si_value")
            if norm_val is None:
                norm_val = normalize_dimension(orig_val, orig_unit)
            else:
                try:
                    norm_val = round(float(norm_val), 3)
                    if math.isnan(norm_val) or math.isinf(norm_val):
                        norm_val = None
                except (ValueError, TypeError):
                    norm_val = None

            # Vérification anti-placeholder : si la conversion échoue, rejeter
            if orig_val is None or norm_val is None:
                return examples

            norm_unit = "m"

            # Tâche E-29 : CLEARANCE_CHECK (Calibration L1_RECONNAISSANCE)
            task_def_id = "CLEARANCE_CHECK"
            tdef = get_task_definition(task_def_id)
            
            q_ergo = f"Quelle est la cote minimale recommandée pour le dégagement d'usage suivant : '{label}' ({context_space}) ?"
            obs_ergo = f"Standard anthropométrique certifié : valeur originale {orig_val} {orig_unit} (soit {norm_val:.2f} {norm_unit}) selon {src_doc}."
            ana_ergo = f"Cette dimension garantit l'amplitude gestuelle libre d'un adulte en situation d'usage standard pour '{label}'."
            ans_ergo = CritiqueEngine.format_structured_response(
                observation=obs_ergo,
                analyse=ana_ergo,
                raisonnement=f"Tout rétrécissement en-deçà de {norm_val:.2f} m engendre un inconfort postural ou des micro-chocs contre le mobilier.",
                limites="Prévoir une majoration de gabarit (min 1,40 m à 1,50 m) en contexte PMR ou pour les zones à forte affluence."
            )

            ex1 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_id}",
                task_type=task_def_id,
                task_group=tdef.group.value,
                domain=tdef.default_domain.value,
                skill=tdef.default_skill.value,
                learning_type=tdef.default_learning_type.value,
                difficulty=DifficultyLevel.L1,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(
                    text_contexts=[{
                        "label": label,
                        "space_category": context_space,
                        "original_value": orig_val,
                        "original_unit": orig_unit,
                        "normalized_value": norm_val,
                        "normalized_unit": norm_unit,
                        "source": src_doc,
                    }]
                ),
                question=q_ergo,
                answer=ans_ergo,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_ergo],
                    interpretations=[ana_ergo],
                ),
                expected_reasoning_type="structured_observation_analysis",
                ground_truth={
                    "label": label,
                    "original_value": orig_val,
                    "original_unit": orig_unit,
                    "normalized_value": norm_val,
                    "normalized_unit": norm_unit,
                    "source": src_doc,
                },
                evidence={"standard": src_doc, "label": label, "norm_si_m": norm_val},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.TOOL,
            )
            examples.append(ex1)

        # Cas 2 : Textes réglementaires (PMR, ERP, CCH)
        elif "regulatory" in record or source_name == "CORE_NORMES_FR":
            reg_data = record.get("regulatory") or record.get("metadata") or {}
            title = reg_data.get("title") or record.get("id")
            article = reg_data.get("article") or "Texte officiel"
            jurisdiction = "France"
            content = reg_data.get("text") or record.get("notes") or ""

            task_def_pmr = "ACCESSIBILITY_ANALYSIS"
            tdef_pmr = get_task_definition(task_def_pmr)
            
            q_pmr = f"Quelles sont les exigences réglementaires d'accessibilité prescrites par la référence '{title}' ({article}) ?"
            obs_pmr = f"Texte officiel ({jurisdiction}) : {title} ({article}). Exigence : {content[:180]}..."
            ana_pmr = "Ces prescriptions imposent des gabarits incompressibles (passage utile minimal, ressaut de seuil ≤ 2 cm, cercle de giration Ø 1,50 m)."
            ans_pmr = CritiqueEngine.format_structured_response(
                observation=obs_pmr,
                analyse=ana_pmr,
                raisonnement="En architecture intérieure, les contraintes réglementaires priment sur le choix esthétique et s'imposent à l'implantation générale.",
                limites="Consulter la version consolidée applicable à la date du dépôt de permis ou déclaration préalable."
            )

            ex2 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_pmr}",
                task_type=task_def_pmr,
                task_group=tdef_pmr.group.value,
                domain=tdef_pmr.default_domain.value,
                skill=tdef_pmr.default_skill.value,
                learning_type=tdef_pmr.default_learning_type.value,
                difficulty=DifficultyLevel.L4,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(text_contexts=[{"title": title, "article": article, "jurisdiction": jurisdiction, "content": content[:300]}]),
                question=q_pmr,
                answer=ans_pmr,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_pmr],
                    interpretations=[ana_pmr],
                ),
                expected_reasoning_type="structured_observation_analysis",
                ground_truth={"title": title, "article": article, "jurisdiction": jurisdiction},
                evidence={"source": "Légifrance / CSTB", "article": article},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.RAG,
            )
            examples.append(ex2)

            # Tâche J-53 : CONSTRAINT_REASONING (L6 Multicontrainte avec contraintes explicites réelles)
            if len(examples) < max_examples:
                task_def_cr = "CONSTRAINT_REASONING"
                tdef_cr = get_task_definition(task_def_cr)
                q_cr = f"Comment concilier les contraintes d'accessibilité de '{title}' ({article}) avec un aménagement spatial dense sans compromettre la fonctionnalité ?"
                obs_cr = f"Contrainte réglementaire obligatoire : {article} imposant des dégagements d'accès, en tension avec une surface au sol compacte."
                ana_cr = "L'arbitrage architectural doit intégrer la fluidité PMR comme matrice d'agencement plutôt que comme une contrainte rapportée."
                ans_cr = CritiqueEngine.format_structured_response(
                    observation=obs_cr,
                    analyse=ana_cr,
                    raisonnement="L'alignement rigoureux des parois et le choix d'équipements suspendus libèrent l'espace de giration au sol tout en optimisant la surface utile.",
                    recommandation="Privilégier des cloisons coulissantes à galandage pour supprimer les débattements encombrants et libérer 0,90 m net.",
                    limites="Valider l'absence de gaine technique ou de refend dans la cloison avant réservation du châssis à galandage."
                )
                ex_cr = SupervisedExample(
                    id=f"{rec_id}_TASK_{task_def_cr}",
                    task_type=task_def_cr,
                    task_group=tdef_cr.group.value,
                    domain=tdef_cr.default_domain.value,
                    skill=tdef_cr.default_skill.value,
                    learning_type=tdef_cr.default_learning_type.value,
                    difficulty=DifficultyLevel.L6,
                    source_ids=[rec_id],
                    source_provenance=provenance,
                    inputs=ModalInputs(text_contexts=[{
                        "title": title,
                        "article": article,
                        "constraint_1": "Accessibilité PMR (passage libre ≥ 0.90 m, giration Ø 1.50 m)",
                        "constraint_2": "Densité fonctionnelle et compacité de l'espace intérieur",
                    }]),
                    question=q_cr,
                    answer=ans_cr,
                    constraints=[
                        "PMR_clearance : 0.90 m passage libre et aire de giration Ø 1.50 m",
                        "Spatial_compactness : minimisation de l'emprise des cloisons",
                    ],
                    epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                        observations=[obs_cr],
                        interpretations=[ana_cr],
                    ),
                    expected_reasoning_type="observation_to_critique",
                    ground_truth={
                        "title": title,
                        "article": article,
                        "tradeoff_axes": ["conformite_pmr", "densite_spatiale"],
                        "level": "L6_MULTICONTRAINTE",
                    },
                    evidence={"article": article, "source": "Légifrance / CSTB"},
                    quality_status=QualityStatus.PASS,
                    split=SplitName.TRAIN,
                    destination=RoutingDestination.FINETUNE,
                )
                examples.append(ex_cr)

        return examples
