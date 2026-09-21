# -*- coding: utf-8 -*-
"""
ARCHI-AI — MaterialsGenerator (Matériaux PBR, Propriétés Physiques & Applications Réelles)
========================================================================================
Génère des exemples supervisés réels à partir des catalogues PBR
ambientCG et Poly Haven Materials : rugosité, réflectance, échelles métriques.
Règle fondamentale : Contextualisation spécifique de chaque matériau selon sa catégorie
(bois, pierre, métal, céramique, tissu, béton) sans aucune formule passe-partout.
"""

from typing import List, Dict, Any
from .base_generator import BaseGenerator
from ..schema import SupervisedExample, ModalInputs, QualityStatus, RoutingDestination, SplitName, DifficultyLevel
from ..task_catalogue import get_task_definition
from ..critique.critique_engine import CritiqueEngine


def get_material_context(category_or_name: str) -> Dict[str, str]:
    """Retourne la prescription architecturale et les contraintes techniques adaptées à la matière."""
    low = category_or_name.lower()
    if any(k in low for k in ("wood", "bois", "parquet", "timber", "plank")):
        return {
            "destination": "revêtement de sol résidentiel (chambres, séjour) ou agencement mural acoustique",
            "qualite": "chaleur visuelle, confort tactile sous les pieds et réverbération sonore amortie",
            "precaution": "proscrire la pose directe en milieu humide sans vernis marin et joint pont de bateau étanche",
        }
    elif any(k in low for k in ("marble", "marbre", "stone", "pierre", "granite")):
        return {
            "destination": "plans de travail de cuisine, dallages nobles d'entrée ou habillages de salle d'eau",
            "qualite": "noblesse minérale, inertie thermique élevée et résistance à l'abrasion",
            "precaution": "appliquer un traitement hydrofuge et oléofuge pour prévenir les taches sur pierre calcaire poreuse",
        }
    elif any(k in low for k in ("metal", "métal", "steel", "acier", "iron", "copper", "brass")):
        return {
            "destination": "châssis de verrières intérieures, piétements de mobilier ou profilés de séparation",
            "qualite": "finesse de section portante, contraste graphique précis et pérennité mécanique",
            "precaution": "contrôler le traitement anticorrosion et l'éventuelle transmission acoustique par résonance",
        }
    elif any(k in low for k in ("tile", "tiles", "ceramic", "carrelage", "porcelain", "mosa")):
        return {
            "destination": "zones à fortes contraintes d'hygiène et d'aspersion d'eau (salles de bain, crédences, cuisine)",
            "qualite": "imperméabilité absolue, facilité de nettoyage et résistance aux agents détergents",
            "precaution": "exiger un classement de glissance pieds chaussés PC10/PC20 et pieds nus PN12 en zone douche",
        }
    elif any(k in low for k in ("fabric", "tissu", "leather", "cuir", "cloth", "velvet")):
        return {
            "destination": "tapisserie d'assises, rideaux de séparation thermique ou panneaux acoustiques muraux",
            "qualite": "absorption phonique ciblée, douceur tactile et atténuation de l'écho flottant",
            "precaution": "vérifier la résistance à l'abrasion au test Martindale (min 20 000 tours pour un usage résidentiel)",
        }
    elif any(k in low for k in ("concrete", "béton", "plaster", "plâtre", "stucco")):
        return {
            "destination": "doublages muraux intérieurs, sols coulés continus ou éléments architectoniques bruts",
            "qualite": "esthétique contemporaine continue sans joint apparent et forte densité minérale",
            "precaution": "prévoir des joints de dilatation réguliers pour éviter toute fissuration par retrait",
        }
    else:
        return {
            "destination": "habillage décoratif d'éléments d'agencement intérieur et finitions de second œuvre",
            "qualite": "caractérisation visuelle de texture et mise en valeur des volumes par la lumière",
            "precaution": "contrôler l'émissivité en composés organiques volatils (étiquetage sanitaire A+ recommandé)",
        }


class MaterialsGenerator(BaseGenerator):
    """Générateur de tâches sur les matériaux et shaders PBR certifié."""

    @property
    def supported_sources(self) -> List[str]:
        return ["CORE_AMBIENTCG", "CORE_POLYHAVEN_MATERIALS"]

    def generate(self, record: Dict[str, Any], max_examples: int = 2) -> List[SupervisedExample]:
        examples: List[SupervisedExample] = []
        rec_id = record.get("id", "UNKNOWN_REC")
        provenance = record.get("provenance", {})
        mat_data = record.get("material") or record.get("materials") or {}
        
        name = mat_data.get("name") or mat_data.get("material_id") or "Matériau PBR"
        category = mat_data.get("category") or "Revêtement"
        scale = mat_data.get("physical_scale_m") or [1.0, 1.0]
        maps = mat_data.get("maps_available") or []
        tags = mat_data.get("tags") or []

        ctx = get_material_context(f"{name} {category} {' '.join(tags)}")

        # 1. Tâche F-36 : PBR_REASONING (L3)
        task_def_pbr = "PBR_REASONING"
        tdef_pbr = get_task_definition(task_def_pbr)

        q_pbr = f"Analysez les propriétés physiques, l'échelle métrique et les canaux PBR du matériau '{name}' ({category})."
        obs_pbr = (
            f"Matériau '{name}' calibré sur une échelle géométrique de {scale[0]} m x {scale[1]} m. "
            f"Texture cartographiée avec {len(maps)} canal/canaux actif(s) : {', '.join(maps)}."
        )
        ana_pbr = (
            f"La map de rugosité (Roughness) module la dispersion spéculaire tandis que la map de normales "
            f"simule le micro-relief sans surcharger le maillage 3D. Le calage métrique à {scale[0]}x{scale[1]} m "
            f"garantit un rapport de proportion physique exact sans étirement de texture."
        )
        ans_pbr = CritiqueEngine.format_structured_response(
            observation=obs_pbr,
            analyse=ana_pbr,
            raisonnement="En conception architecturale et rendu photoréaliste, la fidélité de l'échelle physique conditionne la crédibilité spatiale.",
            limites="L'interaction visuelle sous éclairage rasant dépend de l'activation conjointe du Displacement et de la tessellation."
        )

        ex1 = SupervisedExample(
            id=f"{rec_id}_TASK_{task_def_pbr}",
            task_type=task_def_pbr,
            task_group=tdef_pbr.group.value,
            domain=tdef_pbr.default_domain.value,
            skill=tdef_pbr.default_skill.value,
            learning_type=tdef_pbr.default_learning_type.value,
            difficulty=DifficultyLevel.L3,
            source_ids=[rec_id],
            source_provenance=provenance,
            inputs=ModalInputs(
                materials=[{
                    "name": name,
                    "category": category,
                    "physical_scale_m": scale,
                    "maps_available": maps,
                    "tags": tags[:4],
                }]
            ),
            question=q_pbr,
            answer=ans_pbr,
            epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                observations=[obs_pbr],
                interpretations=[ana_pbr],
            ),
            expected_reasoning_type="structured_observation_analysis",
            ground_truth={"name": name, "scale_m": scale, "maps": maps, "category": category},
            evidence={"tags": tags[:6], "scale": scale},
            quality_status=QualityStatus.PASS,
            split=SplitName.TRAIN,
            destination=RoutingDestination.FINETUNE,
        )
        examples.append(ex1)

        # 2. Tâche F-35 : MATERIAL_APPLICATION (L3 Contextualisé)
        if len(examples) < max_examples:
            task_def_app = "MATERIAL_APPLICATION"
            tdef_app = get_task_definition(task_def_app)

            q_app = f"Dans quel contexte spatial intérieur prescrivez-vous le revêtement '{name}' ({category}) et avec quelles précautions techniques ?"
            obs_app = f"Texture '{name}' ({category}) calibrée à l'échelle {scale[0]}x{scale[1]} m."
            ana_app = (
                f"Ce matériau est recommandé pour : {ctx['destination']}. "
                f"Son intérêt premier réside dans sa contribution : {ctx['qualite']}."
            )
            ans_app = CritiqueEngine.format_structured_response(
                observation=obs_app,
                analyse=ana_app,
                raisonnement="La prescription d'un matériau doit concilier valeur esthétique perçue et exigences physiques d'usage.",
                probleme=f"Contrainte de durabilité : {ctx['precaution']}.",
                recommandation=f"Vérifier la fiche technique du fabricant pour valider l'adéquation exacte avec la classe d'usage visée.",
                limites="Prévoir un calepinage préalable pour aligner les coupes sur les angles rentrants."
            )
            ex2 = SupervisedExample(
                id=f"{rec_id}_TASK_{task_def_app}",
                task_type=task_def_app,
                task_group=tdef_app.group.value,
                domain=tdef_app.default_domain.value,
                skill=tdef_app.default_skill.value,
                learning_type=tdef_app.default_learning_type.value,
                difficulty=DifficultyLevel.L3,
                source_ids=[rec_id],
                source_provenance=provenance,
                inputs=ModalInputs(
                    materials=[{"name": name, "category": category, "physical_scale_m": scale, "context": ctx["destination"]}]
                ),
                question=q_app,
                answer=ans_app,
                epistemic_breakdown=CritiqueEngine.build_epistemic_breakdown(
                    observations=[obs_app],
                    interpretations=[ana_app],
                    to_verifys=[ctx["precaution"]],
                ),
                expected_reasoning_type="observation_to_critique",
                ground_truth={"name": name, "prescribed_destination": ctx["destination"], "category": category},
                evidence={"tags": tags[:5], "material_name": name},
                quality_status=QualityStatus.PASS,
                split=SplitName.TRAIN,
                destination=RoutingDestination.FINETUNE,
            )
            examples.append(ex2)

        return examples
