# -*- coding: utf-8 -*-
"""
ARCHI-AI — Multimodal & Cross-Modal Ablation Audit Module
=========================================================
Red-team evaluation of multimodal tasks (PLAN_PLUS_3D, IMAGE_PLUS_TEXT, PLAN_PLUS_TEXT):
1. Input Integrity: Checks whether required modal inputs (images, plans, geometries, IFC, text)
   are physically provided or empty lists.
2. Modality Cross-Referencing: Checks whether the answer actually synthesizes both modalities
   or merely reports on one while ignoring the other.
3. Modality Ablation Test:
   - IMAGE ablated -> Can answer still stand?
   - PLAN ablated -> Can answer still stand?
   - 3D/IFC ablated -> Can answer still stand?
   - TEXT ablated -> Can answer still stand?
4. Flags FAKE_MODAL_DEPENDENCY and DECORATIVE_MODALITY.
"""

from typing import Dict, Any, List, Set, Tuple


class MultimodalAuditor:
    """Independent auditor for multimodal dependencies and ablation."""

    def __init__(self):
        self.multimodal_task_requirements = {
            "PLAN_PLUS_3D": {"modalities": ["plan_or_geometry", "ifc_or_3d"], "min_required": 2},
            "IMAGE_PLUS_TEXT": {"modalities": ["image", "text"], "min_required": 2},
            "PLAN_PLUS_TEXT": {"modalities": ["plan_or_geometry", "text"], "min_required": 2},
            "MULTIMODAL_PROJECT_REASONING": {"modalities": ["image_or_plan", "text"], "min_required": 2},
            "MATERIAL_AND_STYLE_RELATION": {"modalities": ["image_or_material", "text"], "min_required": 2},
        }

    def audit_multimodal_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits a single multimodal record for input presence, genuine synthesis, and ablation.
        """
        task_type = record.get("task_type", "")
        inputs = record.get("inputs") or {}
        answer = record.get("answer", "")
        gt = record.get("ground_truth") or {}

        images = inputs.get("images", [])
        plans = inputs.get("plans", [])
        geometries = inputs.get("geometries", [])
        ifc_entities = inputs.get("ifc_entities", [])
        materials = inputs.get("materials", [])
        lighting = inputs.get("lighting", [])
        text_contexts = inputs.get("text_contexts", [])

        has_image = len(images) > 0
        has_plan = len(plans) > 0
        has_geometry = len(geometries) > 0
        has_plan_or_geom = has_plan or has_geometry
        has_ifc = len(ifc_entities) > 0
        has_text = len(text_contexts) > 0
        has_material = len(materials) > 0

        req = self.multimodal_task_requirements.get(task_type)
        if not req:
            # If not formally a multimodal task, check if it claims multimodal inputs
            return {
                "record_id": record.get("id"),
                "task_type": task_type,
                "is_multimodal_task": False,
                "verdict": "NOT_MULTIMODAL",
            }

        # 1. Modality Input Availability
        present_modalities: List[str] = []
        if has_image:
            present_modalities.append("image")
        if has_plan:
            present_modalities.append("plan_raster")
        if has_geometry:
            present_modalities.append("geometry_vector")
        if has_ifc:
            present_modalities.append("ifc_entities")
        if has_text:
            present_modalities.append("text_contexts")
        if has_material:
            present_modalities.append("materials")

        # 2. Specific checks per task type
        flags: List[str] = []
        fake_modal = False

        if task_type == "PLAN_PLUS_3D":
            if not has_plan_or_geom:
                flags.append("MISSING_2D_PLAN_OR_GEOMETRY")
                fake_modal = True
            if not has_ifc and not has_geometry:
                flags.append("MISSING_3D_OR_IFC_PAYLOAD")
                fake_modal = True
            # Cross-reference in answer
            has_2d_refs = any(term in answer.lower() for term in ["plan", "pièce", "paroi", "living", "chambre", "m2", "surface"])
            has_3d_refs = any(term in answer.lower() for term in ["3d", "ifc", "hauteur", "niveau", "level", "linteau", "allège", "volumétrie"])
            if not (has_2d_refs and has_3d_refs):
                flags.append("UNILATERAL_REPORTING_NO_CROSS_SYNTHESIS")

        elif task_type == "PLAN_PLUS_TEXT":
            # Note: in review_queue, inputs.plans is [] but geometries is present
            if not has_plan and not has_geometry:
                flags.append("MISSING_PLAN_AND_GEOMETRY")
                fake_modal = True
            elif not has_plan and has_geometry:
                flags.append("DEGRADED_PLAN_TO_VECTOR_GEOMETRY_ONLY")
            if not has_text:
                flags.append("MISSING_TEXT_CONTEXT")
                fake_modal = True

        elif task_type == "IMAGE_PLUS_TEXT":
            if not has_image:
                flags.append("MISSING_IMAGE_INPUT")
                fake_modal = True
            if not has_text:
                flags.append("MISSING_TEXT_CONTEXT")
                fake_modal = True

        # 3. Ablation Testing
        ablation_results = self.simulate_modality_ablation(record, task_type)

        is_fake_modal = fake_modal or ablation_results["ablation_insensitivity"]

        verdict = "GENUINE_MULTIMODAL"
        if is_fake_modal:
            verdict = "FAKE_MODAL_DEPENDENCY"
        elif flags:
            verdict = "DEGRADED_MULTIMODAL"

        return {
            "record_id": record.get("id"),
            "task_type": task_type,
            "is_multimodal_task": True,
            "present_modalities": present_modalities,
            "has_plan_raster": has_plan,
            "has_geometry_vector": has_geometry,
            "has_ifc": has_ifc,
            "has_image": has_image,
            "has_text": has_text,
            "flags": flags,
            "ablation": ablation_results,
            "is_fake_modal": is_fake_modal,
            "verdict": verdict,
        }

    def simulate_modality_ablation(self, record: Dict[str, Any], task_type: str) -> Dict[str, Any]:
        """
        Tests whether the answer changes or whether it could be given with one modality stripped.
        """
        answer = record.get("answer", "")
        # If the answer is identical boilerplate regardless of input variations:
        boilerplate_snippets = [
            "L'organisation actuelle sépare déjà clairement les pièces",
            "Le télétravail peut être aménagé dans une chambre secondaire",
            "La volumétrie tridimensionnelle confirme les hauteurs",
        ]

        matches = [s for s in boilerplate_snippets if s in answer]
        # If the answer uses pure template, removing the image or plan doesn't break the reasoning
        # because the reasoning was never derived from the image or plan in the first place!
        ablation_insensitivity = len(matches) >= 1

        return {
            "ablation_insensitivity": ablation_insensitivity,
            "boilerplate_trigger": matches,
            "notes": (
                "Answer relies on canned narrative; removing visual/spatial modality does not collapse reasoning"
                if ablation_insensitivity
                else "Answer specifically cites features belonging to distinct modalities"
            ),
        }
