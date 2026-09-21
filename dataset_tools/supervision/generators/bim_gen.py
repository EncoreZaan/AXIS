# -*- coding: utf-8 -*-
"""
ARCHI-AI — BimGenerator (Maquettes Numériques IFC & BIM QA Déterministe)
========================================================================
Génère des exemples supervisés réels à partir des modèles IFC buildingSMART,
IFC-Bench et ResBIM, ainsi que des paires QA expertes d'IFC-Bench et MMMU Architecture.
Helpers d'accès certifiés : get_entity(), get_property(), get_relationship(), get_spatial_container().
Interdiction formelle de citation théorique générique sans exploitation des entités,
étages, pièces ou quantitatifs réels du fichier IFC.
"""

from typing import List, Dict, Any, Optional
from .base_generator import BaseGenerator
from ..schema import SupervisedExample, ModalInputs, QualityStatus, RoutingDestination, SplitName, DifficultyLevel
from ..task_catalogue import get_task_definition
from ..critique.critique_engine import CritiqueEngine


def get_entity(bim_data: Dict[str, Any], class_name: str) -> Optional[int]:
    """Retourne le nombre d'occurrences d'une classe IFC dans le modèle."""
    counts = bim_data.get("element_counts", {})
    return counts.get(class_name)


def get_property(bim_data: Dict[str, Any], prop_name: str) -> Any:
    """Retourne une propriété spécifique extraite de la maquette."""
    props = bim_data.get("properties_extracted", {})
    return props.get(prop_name) or bim_data.get(prop_name)


def get_relationship(bim_data: Dict[str, Any]) -> Dict[str, Any]:
    """Retourne les relations sémantiques entre conteneurs et composants."""
    storeys = bim_data.get("storeys", [])
    counts = bim_data.get("element_counts", {})
    return {"storeys_count": len(storeys), "component_classes": list(counts.keys())}


def get_spatial_container(bim_data: Dict[str, Any]) -> Dict[str, Any]:
    """Retourne la structure d'emboîtement spatial réelle extraite du fichier IFC."""
    return {
        "project": bim_data.get("project_name") or "Projet IFC",
        "site": bim_data.get("site_name") or "Site du projet",
        "building": bim_data.get("building_name") or bim_data.get("model_id") or "Bâtiment",
        "storeys": bim_data.get("storeys", []),
        "spaces": bim_data.get("spaces", []),
    }


class BimGenerator(BaseGenerator):
    """Générateur de tâches BIM / IFC certifié sur données réelles."""

    @property
    def supported_sources(self) -> List[str]:
        return [
            "CORE_BUILDINGSMART",
            "CORE_BUILDINGSMART_IFC",
            "CORE_IFC_BENCH_MODELS",
            "CORE_IFC_BENCH_QA",
            "CORE_RESBIM_IFC",
            "CORE_MMMU_ARCHITECTURE",
        ]

    def generate(self, record: Dict[str, Any], max_examples: int = 3) -> List[SupervisedExample]:
        examples: List[SupervisedExample] = []
        rec_id = record.get("id", "UNKNOWN_REC")
        source_name = record.get("source_name", "CORE_BUILDINGSMART")
        provenance = record.get("provenance", {})
        data_type = record.get("data_type", "")
        visual = record.get("visual", {})

        # Cas 1 : Questions/Réponses réelles IFC-Bench QA ou MMMU Architecture
        if data_type == "multimodal_qa_pair" or "qa" in record or "multimodal_qa" in record:
            qa_data = record.get("qa") or record.get("multimodal_qa") or {}
            question_text = qa_data.get("question") or record.get("question")
            answer_text = qa_data.get("answer") or record.get("answer")
            options = qa_data.get("options", [])

            if question_text and answer_text:
                if source_name == "CORE_MMMU_ARCHITECTURE":
                    task_def_id = "MULTIMODAL_PROJECT_REASONING"
                    tdef = get_task_definition(task_def_id)
                    split_val = SplitName.BENCHMARK
                    dest_val = RoutingDestination.BENCHMARK
                    diff_val = DifficultyLevel.L5
                    formatted_ans = f"Réponse certifiée du benchmark MMMU : {answer_text}."
                    if options:
                        formatted_ans += f" Options : {', '.join(options)}."
                else:
                    task_def_id = "IFC_QA"
                    tdef = get_task_definition(task_def_id)
                    split_val = SplitName.TRAIN if record.get("split") != "benchmark_test" else SplitName.BENCHMARK
                    dest_val = RoutingDestination.MULTIUSE if split_val == SplitName.TRAIN else RoutingDestination.BENCHMARK
                    diff_val = DifficultyLevel.L4
                    formatted_ans = answer_text

                ex = SupervisedExample(
                    id=f"{rec_id}_SUP_QA",
                    task_type=task_def_id,
                    task_group=tdef.group.value,
                    domain=tdef.default_domain.value,
                    skill=tdef.default_skill.value,
                    learning_type=tdef.default_learning_type.value,
                    difficulty=diff_val,
                    source_ids=[rec_id],
                    source_provenance=provenance,
                    inputs=ModalInputs(
                        images=[visual] if visual else [],
                        ifc_entities=[{"qa_ref": rec_id, "topic": "IFC component analysis"}],
                        text_contexts=[{"question": question_text}],
                    ),
                    question=question_text,
                    answer=formatted_ans,
                    epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                        observations=[f"Énoncé technique : {question_text[:120]}..."],
                        interpretations=[f"Réponse technique vérifiée issue du référentiel source : {answer_text[:120]}..."],
                    ),
                    expected_reasoning_type="structured_observation_analysis",
                    ground_truth={"qa_pair": {"q": question_text, "a": answer_text}},
                    evidence={"source_dataset": source_name, "raw_id": rec_id},
                    quality_status=QualityStatus.PASS,
                    split=split_val,
                    destination=dest_val,
                )
                examples.append(ex)
                return examples

        # Cas 2 : Modèles IFC complets (buildingSMART, ResBIM, IFC-Bench Models)
        bim_data = record.get("bim") or record.get("bim_ifc") or {}
        if not bim_data:
            return examples

        model_id = bim_data.get("model_id") or rec_id
        schema_ver = bim_data.get("ifc_schema") or bim_data.get("schema_version") or "IFC4"
        element_counts = bim_data.get("element_counts", {})
        classes_present = list(element_counts.keys()) or bim_data.get("classes_present", [])
        storeys = bim_data.get("storeys", [])
        spaces = bim_data.get("spaces", [])
        materials = bim_data.get("materials_declared", [])
        walls_cnt = bim_data.get("walls_count") or element_counts.get("IfcWall", 0) or element_counts.get("IfcWallStandardCase", 0)
        doors_cnt = bim_data.get("doors_count") or element_counts.get("IfcDoor", 0)
        windows_cnt = bim_data.get("windows_count") or element_counts.get("IfcWindow", 0)

        # 1. Tâche D-22 : IFC_ENTITY_IDENTIFICATION (L2)
        if classes_present:
            task_def_id = "IFC_ENTITY_IDENTIFICATION"
            tdef = get_task_definition(task_def_id)
            sample_classes_with_counts = [f"{cls} ({element_counts.get(cls, 'présent')})" for cls in classes_present[:6]]
            q_ent = f"Quelles sont les entités IFC constitutives du gros œuvre et du second œuvre de la maquette '{model_id}' ?"
            obs_ent = (
                f"La maquette IFC '{model_id}' (schéma {schema_ver}) recense {len(classes_present)} classes d'éléments : "
                f"{', '.join(sample_classes_with_counts)}."
            )
            ana_ent = (
                f"L'inventaire met en évidence {walls_cnt} éléments de mur/cloison, {doors_cnt} bloc(s)-porte(s) "
                f"et {windows_cnt} baie(s) vitrée(s), structurant l'enveloppe et la distribution intérieure."
            )
            ans_ent = CritiqueEngine.format_structured_response(
                observation=obs_ent,
                analyse=ana_ent,
                raisonnement="L'extraction automatisée des classes IFC permet de vérifier la complétude sémantique du modèle avant analyse spatiale.",
                limites="Contrôler la conformité de modélisation selon la MVD (Model View Definition) d'échange."
            )
            ex1 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_id}",
                task_type=task_def_id,
                task_group=tdef.group.value,
                domain=tdef.default_domain.value,
                skill=tdef.default_skill.value,
                learning_type=tdef.default_learning_type.value,
                difficulty=DifficultyLevel.L2,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(
                    ifc_entities=[{
                        "model_id": model_id,
                        "schema": schema_ver,
                        "classes_sample": classes_present[:8],
                        "element_counts": {k: element_counts[k] for k in list(element_counts.keys())[:8]},
                    }]
                ),
                question=q_ent,
                answer=ans_ent,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_ent],
                    interpretations=[ana_ent],
                ),
                expected_reasoning_type="structured_observation_analysis",
                ground_truth={"classes": classes_present, "element_counts": element_counts, "schema": schema_ver},
                evidence={"model_id": model_id, "walls": walls_cnt, "doors": doors_cnt, "windows": windows_cnt},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.FINETUNE,
            )
            examples.append(ex1)

        # 2. Tâche D-24 : BIM_SPATIAL_HIERARCHY (L3)
        if len(examples) < max_examples:
            task_def_hier = "BIM_SPATIAL_HIERARCHY"
            tdef_hier = get_task_definition(task_def_hier)
            spatial_info = get_spatial_container(bim_data)
            p_name = spatial_info["project"]
            b_name = spatial_info["building"]

            storey_desc = f"comprenant {len(storeys)} niveau(x) : {', '.join(storeys)}" if storeys else "sans niveau IfcBuildingStorey explicite déclaré"
            space_desc = f" et {len(spaces)} espace(s) intérieur(s) répertorié(s) ({', '.join(spaces[:4])})" if spaces else ""

            q_hier = f"Décrivez la structure d'emboîtement spatial réelle extraite de la maquette '{model_id}'."
            obs_hier = (
                f"Décomposition spatiale du modèle IFC '{model_id}' (schéma {schema_ver}) : Projet '{p_name}', "
                f"Bâtiment '{b_name}', {storey_desc}{space_desc}."
            )
            ana_hier = (
                f"Cette organisation hiérarchique rattache formellement les {sum(element_counts.values()) if element_counts else 'éléments'} "
                f"composants à leurs conteneurs d'étage respectifs, garantissant l'intégrité des coupes et des quantitatifs par niveau."
            )
            ans_hier = CritiqueEngine.format_structured_response(
                observation=obs_hier,
                analyse=ana_hier,
                raisonnement="Le respect de l'arborescence IfcBuildingStorey / IfcSpace est obligatoire pour la localisation des éléments du second œuvre.",
                limites="Contrôler l'existence éventuelle d'éléments sans conteneur spatial d'étage (IsContainedInBoundary)."
            )
            ex2 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_hier}",
                task_type=task_def_hier,
                task_group=tdef_hier.group.value,
                domain=tdef_hier.default_domain.value,
                skill=tdef_hier.default_skill.value,
                learning_type=tdef_hier.default_learning_type.value,
                difficulty=DifficultyLevel.L3,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(
                    ifc_entities=[{
                        "model_id": model_id,
                        "project": p_name,
                        "building": b_name,
                        "storeys": storeys,
                        "spaces": spaces[:6],
                        "schema": schema_ver,
                    }]
                ),
                question=q_hier,
                answer=ans_hier,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_hier],
                    interpretations=[ana_hier],
                ),
                expected_reasoning_type="structured_observation_analysis",
                ground_truth={"spatial_containment": spatial_info, "schema": schema_ver},
                evidence={"storeys": storeys, "spaces_count": len(spaces)},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.FINETUNE,
            )
            examples.append(ex2)

        return examples
