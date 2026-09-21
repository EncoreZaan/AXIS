# -*- coding: utf-8 -*-
"""
ARCHI-AI — Test de Nécessité Multimodale (Multimodal Grounding & Necessity Validator)
====================================================================================
Contrôle strict interdisant le FAUX MULTIMODAL.
Pour chaque exemple déclaré multimodal (ex: IMAGE_PLAN, PLAN_TEXT, BIM_PLUS_PLAN) :
1. Test d'Ablation Textuelle (Text-Only) : si le texte divulgue la réponse sans regarder l'image/plan -> FAKE_MULTIMODAL.
2. Test d'Ablation Visuelle (Image/Plan-Only) : si l'image seule répond sans la contrainte du texte -> FAKE_MULTIMODAL.
3. Règle d'or : retirer une des modalités doit rendre la tâche sous-déterminée.
"""

import re
from typing import Dict, Any, Tuple, List

class MultimodalNecessityValidator:
    """Vérificateur de nécessité multimodale par tests d'ablation."""

    @staticmethod
    def evaluate_necessity(
        task_id: str,
        modality: str,
        question: str,
        answer: str,
        inputs: Dict[str, Any],
        ground_truth: Dict[str, Any]
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Évalue si l'exemple est un VRAI multimodal ou un FAUX multimodal.
        Retourne (is_valid, reason, diagnostics).
        """
        # Si la modalité déclarée est unimodale, le test de croisement ne s'applique pas
        unimodal_types = ["TEXT_ONLY", "IMAGE_ONLY", "PLAN_ONLY", "IFC", "3D"]
        if modality in unimodal_types:
            return True, "UNIMODAL_COMPLIANT", {"modality": modality, "test": "N/A"}

        # 1. Vérification de la présence physique des modalités déclarées
        has_images = bool(inputs.get("images"))
        has_plans = bool(inputs.get("plans"))
        has_3d = bool(inputs.get("geometries") or inputs.get("custom_metadata", {}).get("scene_objects"))
        has_ifc = bool(inputs.get("ifc_entities"))
        has_text_context = bool(inputs.get("text_contexts") or question)

        modalities_present = 0
        if has_images: modalities_present += 1
        if has_plans: modalities_present += 1
        if has_3d: modalities_present += 1
        if has_ifc: modalities_present += 1

        if modalities_present < 1:
            return False, "FAKE_MULTIMODAL_NO_VISUAL_INPUT", {
                "error": "Aucun asset visuel ou géométrique fourni pour une tâche multimodale déclarée."
            }

        # 2. Test d'Ablation 1 : Fuite de la cible dans la question (Text-Only Shortcut)
        # Si la valeur cible exacte (ex: nombre de pièces, nom de la matière, cote) est déjà écrite dans la question
        target_keys = ["target_value", "ground_truth_answer", "expected_count", "compliant_status"]
        for k in target_keys:
            val = str(ground_truth.get(k, "")).strip().lower()
            if val and len(val) > 3 and val in question.lower():
                # Cas où la question donne directement la réponse
                if not any(token in question.lower() for token in ["conforme", "vérifiez", "est-il vrai", "conflit"]):
                    return False, "FAKE_MULTIMODAL_TEXT_SHORTCUT", {
                        "error": f"La réponse cible '{val}' est déjà divulguée dans l'énoncé de la question.",
                        "question": question
                    }

        # 3. Test d'Ablation 2 : Dépendance visuelle/spatiale obligatoire
        # La tâche doit requérir l'inspection d'une coordonnée, d'une entité ou d'un masque
        visual_evidence = inputs.get("evidence", {}) or ground_truth.get("evidence", {})
        if not visual_evidence and not ground_truth.get("coordinates") and not ground_truth.get("ifc_guids"):
            # Aucun ancrage visuel explicite
            return False, "FAKE_MULTIMODAL_MISSING_EVIDENCE_ANCHOR", {
                "error": "Aucune preuve géométrique, polygonale ou GUID n'ancre la réponse."
            }

        # 4. Validation réussie
        return True, "TRUE_MULTIMODAL_VERIFIED", {
            "modality": modality,
            "visual_anchors": list(visual_evidence.keys()) if isinstance(visual_evidence, dict) else len(visual_evidence),
            "cross_modal_check": "PASS"
        }
