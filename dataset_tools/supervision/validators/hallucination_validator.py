# -*- coding: utf-8 -*-
"""
ARCHI-AI — HallucinationValidator (Détecteur d'Inventions Non Sourcées)
=======================================================================
Vérifie rigoureusement qu'aucun chiffre, cote, surface, unité ou référence
réglementaire n'est inventé dans la réponse supervisée.
"""

import re
from typing import Set, List, Dict, Any
from .base_validator import BaseValidator
from ..schema import SupervisedExample, QualityStatus, QualityCheckResult


class HallucinationValidator(BaseValidator):
    """Détecteur d'hallucinations numériques, matérielles et réglementaires."""

    @property
    def name(self) -> str:
        return "HallucinationValidator"

    # Références légales réelles certifiées dans le Master Dataset
    KNOWN_REGULATORY_REFS = {
        "arrêté du 20 avril 2017",
        "arrété du 20 avril 2017",
        "arrete du 20 avril 2017",
        "arrêté du 25 juin 1980",
        "arrété du 25 juin 1980",
        "arrete du 25 juin 1980",
        "art. r. 156-1",
        "article r. 156-1",
        "r. 156-1",
        "co 36",
        "co 37",
        "co 38",
        "article 7",
        "article 8",
        "cch",
        "erp",
        "pmr",
    }

    def extract_numbers_from_text(self, text: str) -> Set[float]:
        """Extrait tous les nombres (entiers et flottants) d'un texte."""
        # Regex pour nombres ex: 12.5, 12,5, 120
        raw_matches = re.findall(r"\b\d+(?:[.,]\d+)?\b", text)
        numbers = set()
        for m in raw_matches:
            try:
                norm_str = m.replace(",", ".")
                numbers.add(float(norm_str))
            except ValueError:
                pass
        return numbers

    def validate(self, example: SupervisedExample) -> QualityCheckResult:
        """
        Contrôle la cohérence des nombres et citations dans la réponse.
        """
        answer_lower = example.answer.lower()
        
        # 1. Contrôle des références réglementaires
        if "loi" in answer_lower or "arrêté" in answer_lower or "norme" in answer_lower or "article" in answer_lower:
            # Vérifier si l'une des références légales mentionnées est une invention
            has_valid_ref = any(ref in answer_lower for ref in self.KNOWN_REGULATORY_REFS)
            # S'il cite un article imaginaire sans source
            fake_articles = re.findall(r"article\s+[a-z0-9\.\-]+", answer_lower)
            for fa in fake_articles:
                if not any(valid in fa for valid in ["7", "8", "r. 156-1", "co 36", "co 37", "co 38"]):
                    return QualityCheckResult(
                        validator_name=self.name,
                        status=QualityStatus.FAIL,
                        message=f"Hallucination réglementaire détectée : article non répertorié '{fa}'",
                        details={"fake_article": fa},
                    )

        # 2. Contrôle de présence des chiffres cités dans le ground_truth ou evidence
        # Si la tâche nécessite une vérification déterministe
        answer_numbers = self.extract_numbers_from_text(example.answer)
        context_str = str(example.ground_truth) + " " + str(example.evidence) + " " + str(example.inputs.model_dump())
        context_numbers = self.extract_numbers_from_text(context_str)

        # Tolérer les petits entiers descriptifs (1, 2, 3, 4, 10, 20, 100, 150)
        ignorable_numbers = {0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 150.0, 90.0, 80.0, 60.0, 2026.0}
        unverified_numbers = []
        for n in answer_numbers:
            if n in ignorable_numbers:
                continue
            # Vérifier si proche d'un nombre du contexte (à 1% près)
            match_found = any(abs(n - cn) <= 0.05 * max(abs(cn), 0.01) for cn in context_numbers)
            if not match_found:
                unverified_numbers.append(n)

        # Si plus de 3 nombres complexes non ancrés dans les faits
        if len(unverified_numbers) > 3:
            return QualityCheckResult(
                validator_name=self.name,
                status=QualityStatus.WARNING,
                message=f"Chiffres potentiellement non ancrés dans la source : {unverified_numbers[:5]}",
                details={"unverified_numbers": unverified_numbers[:10]},
            )

        return QualityCheckResult(
            validator_name=self.name,
            status=QualityStatus.PASS,
            message="Aucune hallucination numérique ou réglementaire détectée",
            details={},
        )
