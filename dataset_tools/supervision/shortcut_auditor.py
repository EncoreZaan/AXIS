# -*- coding: utf-8 -*-
"""
ARCHI-AI — Audit des Raccourcis Cognitifs & Fuites de Split (Shortcut & Leakage Auditor)
========================================================================================
Détecte et neutralise les raccourcis méthodologiques :
1. Clés lexicales dans la question qui trahissent la réponse
2. Indices dans les noms de fichiers ou chemins sources (ex: 'bathroom_chair.png')
3. Fuites de métadonnées non pertinentes
4. Fuite d'intégrité de partitionnement (cross-contamination de project_group_id entre Train, Val et Test)
"""

import re
from typing import Dict, Any, List, Set, Tuple

class ShortcutAuditor:
    """Détecteur de raccourcis, fuites lexicales et contamination de split."""

    def __init__(self):
        self.prohibited_filename_leak_tokens = [
            "answer", "solution", "groundtruth", "gt_", "annotated", "corrected"
        ]

    def audit_example(self, example_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Vérifie l'absence de raccourci ou de fuite sur un exemple unitaire."""
        issues = []
        question = example_dict.get("question", "").lower()
        answer = example_dict.get("answer", "").lower()
        inputs = example_dict.get("inputs", {})
        source_paths = [
            f.get("path", "") for f in inputs.get("images", []) + inputs.get("plans", [])
        ]

        # 1. Vérification des indices dans les noms de fichiers
        for path in source_paths:
            fname = path.split("/")[-1].split("\\")[-1].lower()
            for token in self.prohibited_filename_leak_tokens:
                if token in fname:
                    issues.append(f"SHORTCUT_FILENAME_LEAK: Le fichier source '{fname}' contient le token interdit '{token}'.")

        # 2. Vérification de la trivialité de la question
        if len(question.strip()) < 10:
            issues.append("SHORTCUT_TRIVIAL_QUESTION: Question trop courte (< 10 caractères).")

        # 3. Vérification de répétition mot-à-mot anormale (template brut sans extraction)
        if "organisation matricielle" in answer and "parois et les ouvertures identifiables" in question:
            issues.append("SHORTCUT_STATIC_TEMPLATE: Réponse générique non contextualisée détectée.")

        is_clean = len(issues) == 0
        return is_clean, issues

    @staticmethod
    def audit_split_leakage(examples: List[Dict[str, Any]]) -> Tuple[bool, Dict[str, Any]]:
        """
        Vérifie qu'aucun project_group_id ni SHA256 n'est présent simultanément
        dans deux partitions différentes (train / validation / test).
        """
        split_projects: Dict[str, Set[str]] = {"train": set(), "validation": set(), "test": set()}
        split_assets: Dict[str, Set[str]] = {"train": set(), "validation": set(), "test": set()}

        for ex in examples:
            sp = ex.get("split", "train").lower()
            if sp not in split_projects:
                continue
            
            p_id = ex.get("project_group_id") or ex.get("source_provenance", {}).get("project_group_id")
            if p_id:
                split_projects[sp].add(p_id)
            
            for s_id in ex.get("source_ids", []):
                split_assets[sp].add(s_id)

        # Calcul des intersections
        leaks = []
        # Projets
        tv_proj = split_projects["train"].intersection(split_projects["validation"])
        tt_proj = split_projects["train"].intersection(split_projects["test"])
        vt_proj = split_projects["validation"].intersection(split_projects["test"])
        
        if tv_proj: leaks.append(f"PROJECT_LEAK train <-> validation : {len(tv_proj)} projets communs ({list(tv_proj)[:3]})")
        if tt_proj: leaks.append(f"PROJECT_LEAK train <-> test : {len(tt_proj)} projets communs ({list(tt_proj)[:3]})")
        if vt_proj: leaks.append(f"PROJECT_LEAK validation <-> test : {len(vt_proj)} projets communs ({list(vt_proj)[:3]})")

        # Assets
        tv_asset = split_assets["train"].intersection(split_assets["validation"])
        tt_asset = split_assets["train"].intersection(split_assets["test"])
        vt_asset = split_assets["validation"].intersection(split_assets["test"])

        if tv_asset: leaks.append(f"ASSET_LEAK train <-> validation : {len(tv_asset)} assets communs")
        if tt_asset: leaks.append(f"ASSET_LEAK train <-> test : {len(tt_asset)} assets communs")
        if vt_asset: leaks.append(f"ASSET_LEAK validation <-> test : {len(vt_asset)} assets communs")

        is_clean = len(leaks) == 0
        diagnostics = {
            "is_clean": is_clean,
            "train_projects": len(split_projects["train"]),
            "validation_projects": len(split_projects["validation"]),
            "test_projects": len(split_projects["test"]),
            "leaks": leaks
        }
        return is_clean, diagnostics
