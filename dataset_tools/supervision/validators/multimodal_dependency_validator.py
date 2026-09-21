# -*- coding: utf-8 -*-
"""
ARCHI-AI — MultimodalDependencyValidator (Contrôle d'Intégrité Multimodale Stricte)
===================================================================================
Vérifie que les tâches déclarées comme multimodales ou cross-modales comportent
réellement toutes les modalités requises dans 'inputs' (ex: IMAGE_PLUS_TEXT,
PLAN_PLUS_3D, PLAN_PLUS_TEXT, IMAGE_PLUS_PLAN). Détecte les faux multimodaux (FAKE_MULTIMODAL)
et interdit rigoureusement les inputs entièrement vides.
"""

from typing import List
from .base_validator import BaseValidator
from ..schema import SupervisedExample, QualityStatus, QualityCheckResult


class MultimodalDependencyValidator(BaseValidator):
    """Vérificateur de la dépendance et complétude effective des entrées multimodales."""

    @property
    def name(self) -> str:
        return "MultimodalDependencyValidator"

    def validate(self, example: SupervisedExample) -> QualityCheckResult:
        inputs = example.inputs
        task_type = example.task_type
        task_group = example.task_group

        active_modalities: List[str] = [
            k for k, v in inputs.model_dump().items()
            if v and isinstance(v, list) and len(v) > 0
        ]

        # 1. Vérification d'absence totale d'entrées (Interdiction absolue -> REVIEW)
        if not active_modalities and not inputs.custom_metadata:
            return QualityCheckResult(
                validator_name=self.name,
                status=QualityStatus.REVIEW,
                message="Entrées multimodales vides (aucun document image, plan, géométrie ou contexte textuel fourni)",
                details={"active_modalities": []},
            )

        # 2. Cas spécifique : IMAGE_PLUS_TEXT (Nécessite image ET text_contexts)
        if task_type == "IMAGE_PLUS_TEXT":
            has_image = bool(inputs.images)
            has_text = bool(inputs.text_contexts)
            if not (has_image and has_text):
                return QualityCheckResult(
                    validator_name=self.name,
                    status=QualityStatus.REVIEW,
                    message="FAKE_MULTIMODAL détecté : tâche IMAGE_PLUS_TEXT sans image ET texte simultanément présents",
                    details={"missing": [k for k, v in [("images", has_image), ("text_contexts", has_text)] if not v]},
                )

        # 3. Cas spécifique : PLAN_PLUS_3D (Nécessite plan 2D ET modèle/géométrie 3D)
        if task_type == "PLAN_PLUS_3D":
            has_plan = bool(inputs.plans)
            has_3d = bool(inputs.geometries or inputs.ifc_entities)
            if not (has_plan and has_3d):
                return QualityCheckResult(
                    validator_name=self.name,
                    status=QualityStatus.REVIEW,
                    message="Dépendance bimodal incomplète pour PLAN_PLUS_3D (nécessite plan 2D ET modèle/géométrie 3D)",
                    details={"has_plan": has_plan, "has_3d": has_3d},
                )

        # 4. Cas spécifique : PLAN_PLUS_TEXT (Nécessite plan 2D ET contexte textuel)
        if task_type == "PLAN_PLUS_TEXT":
            has_plan = bool(inputs.plans)
            has_text = bool(inputs.text_contexts)
            if not (has_plan and has_text):
                return QualityCheckResult(
                    validator_name=self.name,
                    status=QualityStatus.REVIEW,
                    message="Dépendance bimodal incomplète pour PLAN_PLUS_TEXT (nécessite plan 2D ET texte de contraintes)",
                    details={"has_plan": has_plan, "has_text": has_text},
                )

        # 5. Cas spécifique : IMAGE_PLUS_PLAN (Nécessite image ET plan)
        if task_type == "IMAGE_PLUS_PLAN":
            has_img = bool(inputs.images)
            has_plan = bool(inputs.plans)
            if not (has_img and has_plan):
                return QualityCheckResult(
                    validator_name=self.name,
                    status=QualityStatus.REVIEW,
                    message="Dépendance bimodal incomplète pour IMAGE_PLUS_PLAN (nécessite image vue ET plan d'étage)",
                    details={"has_img": has_img, "has_plan": has_plan},
                )

        # 6. Vérification pour le groupe L_MULTIMODAL
        if task_group == "L_MULTIMODAL" and len(active_modalities) < 1:
            return QualityCheckResult(
                validator_name=self.name,
                status=QualityStatus.REVIEW,
                message="Groupe L_MULTIMODAL sans modalité active",
                details={"active_modalities": active_modalities},
            )

        return QualityCheckResult(
            validator_name=self.name,
            status=QualityStatus.PASS,
            message="Entrées multimodales conformes aux dépendances de la tâche",
            details={"active_modalities": active_modalities},
        )
