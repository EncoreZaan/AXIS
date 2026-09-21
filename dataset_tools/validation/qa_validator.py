#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Validateur complet de qualité et d'intégrité (QA Engine)
=================================================================
Vérifie :
- Validation Pydantic & JSON Schema
- Existence et lisibilité des images (PIL)
- Dimensions minimales des images
- Validité des taxonomies (catégories, compétences, types d'apprentissage)
- Cohérence des champs textuels (réponses vides, formats)
- Signaux anti-hallucination gradués : PASS, WARNING, REVIEW, FAIL
  (Pas de suppression aveugle par simple regex, mais détection des affirmations non fondées)
- Non-contamination et intégrité des splits
"""

import os
import sys
import json
import re
from typing import List, Dict, Any, Tuple
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from dataset.master.schema.models import MasterAnnotation
from dataset_tools.validation.taxonomy import (
    DocumentType,
    Domain,
    DifficultyLevel,
    LearningType,
    Skill,
    QAStatus
)
from dataset_tools.deduplication.dedup_detector import DeduplicationAnalyzer
from dataset_tools.splitting.leak_detector import SplitLeakageDetector


class QAValidator:
    """Validateur multicritères pour le dataset ARCHI-AI."""

    # Patterns signalant un risque d'affirmation péremptoire ou hallucination sur photo
    HALLUCINATION_RISK_PATTERNS = [
        r"\b(?:mesure exactement|fait exactement|largeur de \d+[\.,]?\d*\s*cm|hauteur sous plafond de \d+[\.,]?\d*\s*m)\b",
        r"\b(?:coût de|facturé à|acheté chez|marque certifiée)\b",
        r"\b(?:température de|degré d'isolation thermique R=)\b",
        r"\b(?:béton armé dosé à|acoustique de \d+ dB)\b"
    ]

    # Patterns vertueux d'incertitude épistémique (reconnaissance des limites visuelles)
    EPISTEMIC_AWARENESS_PATTERNS = [
        r"\b(?:ne peut être certifié|sans plan métré|à confirmer|visuellement|semble|suppose|non mesurable)\b",
        r"\b(?:sous réserve|impossible d'affirmer|difficilement évaluable|aspect)\b"
    ]

    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.dedup_analyzer = DeduplicationAnalyzer()
        self.leak_detector = SplitLeakageDetector()

    def validate_record(self, raw_record: Dict[str, Any]) -> Tuple[QAStatus, List[str]]:
        """Valide un enregistrement individuel et retourne son statut QA et ses alertes."""
        flags: List[str] = []
        status = QAStatus.PASS_STATUS

        # 1. Validation Pydantic
        try:
            record = MasterAnnotation(**raw_record)
        except Exception as e:
            flags.append(f"FAIL_SCHEMA: {e}")
            return QAStatus.FAIL, flags

        # 2. Validation des images (existence, lisibilité, dimensions)
        for img in record.images:
            # Chemins absolus ou relatifs à base_dir
            full_path = os.path.join(self.base_dir, img.path) if not os.path.isabs(img.path) else img.path
            if not os.path.exists(full_path):
                # Essayer avec le préfixe dataset si manquant
                alt_path = os.path.join(self.base_dir, "dataset", img.path)
                if os.path.exists(alt_path):
                    full_path = alt_path
                else:
                    flags.append(f"FAIL_MISSING_IMAGE: Image introuvable {img.path}")
                    status = QAStatus.FAIL
                    continue

            try:
                with Image.open(full_path) as im:
                    w, h = im.size
                    if w < 100 or h < 100:
                        flags.append(f"WARNING_IMAGE_TOO_SMALL: Dimensions {w}x{h} inférieures au seuil recommandé (100x100)")
                        if status == QAStatus.PASS_STATUS:
                            status = QAStatus.WARNING
            except Exception as e:
                flags.append(f"FAIL_CORRUPT_IMAGE: Image illisible {img.path} ({e})")
                status = QAStatus.FAIL

        # 3. Contrôle textuel
        if len(record.question.strip()) < 10:
            flags.append("WARNING_SHORT_QUESTION: Question très courte (<10 chars)")
            if status == QAStatus.PASS_STATUS:
                status = QAStatus.WARNING

        if len(record.answer.strip()) < 50:
            flags.append("FAIL_SHORT_ANSWER: Réponse anormalement courte (<50 chars)")
            status = QAStatus.FAIL

        # 4. Détection prudente anti-hallucination (Système de Flags au lieu de regex bloquante)
        answer_text = record.answer
        hallucination_triggers = []
        for pat in self.HALLUCINATION_RISK_PATTERNS:
            if re.search(pat, answer_text, re.IGNORECASE):
                hallucination_triggers.append(pat)

        has_epistemic_caution = any(
            re.search(pat, answer_text, re.IGNORECASE) for pat in self.EPISTEMIC_AWARENESS_PATTERNS
        )

        if hallucination_triggers:
            if not has_epistemic_caution and len(record.unknowns) == 0:
                flags.append(f"REVIEW_HALLUCINATION_RISK: Affirmation métrique/technique sans précaution épistémique ({hallucination_triggers})")
                if status in (QAStatus.PASS_STATUS, QAStatus.WARNING):
                    status = QAStatus.REVIEW
            else:
                flags.append("INFO_METRIC_CAUTION_PRESENT: Mention métrique accompagnée de clauses de réserve")

        return status, flags

    def validate_dataset_file(self, file_path: str) -> Dict[str, Any]:
        """Valide l'ensemble d'un fichier master ou split."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Fichier à valider introuvable : {file_path}")

        records = []
        with open(file_path, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    return {
                        "is_valid": False,
                        "error": f"Erreur de syntaxe JSON ligne {idx}: {e}",
                        "total": 0
                    }

        stats = {
            QAStatus.PASS_STATUS.value: 0,
            QAStatus.WARNING.value: 0,
            QAStatus.REVIEW.value: 0,
            QAStatus.FAIL.value: 0
        }
        item_reports = []

        for r in records:
            st, flags = self.validate_record(r)
            stats[st.value] += 1
            item_reports.append({
                "id": r.get("id"),
                "status": st.value,
                "flags": flags
            })

        # Analyse des doublons
        dedup_res = self.dedup_analyzer.analyze(records)

        # Vérification des splits si train et val présents
        train_s = [r for r in records if r.get("assigned_split") == "train"]
        val_s = [r for r in records if r.get("assigned_split") == "validation"]
        test_s = [r for r in records if r.get("assigned_split") == "test"]
        leak_res = self.leak_detector.check_splits(train_s, val_s, test_s)

        is_overall_valid = (stats[QAStatus.FAIL.value] == 0) and leak_res["is_clean"]

        return {
            "is_valid": is_overall_valid,
            "total_records": len(records),
            "status_distribution": stats,
            "deduplication": dedup_res,
            "leak_report": leak_res,
            "item_reports": item_reports
        }


def run_qa_cli():
    """Point d'entrée en ligne de commande."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    master_file = os.path.join(base_dir, "dataset", "master", "annotations", "master_annotations.jsonl")
    
    print(f"Lancement du contrôle QA sur {master_file}...")
    validator = QAValidator(base_dir)
    res = validator.validate_dataset_file(master_file)
    
    print("\n================ RÉSULTAT DU CONTRÔLE QUALITÉ QA ================")
    print(f"Statut Global : {'VALIDE' if res['is_valid'] else 'ÉCHEC'}")
    print(f"Total exemples audités : {res['total_records']}")
    print(f"Distribution QA : {res['status_distribution']}")
    print(f"Intégrité des Splits (Non-contamination) : {'GARANTIE' if res['leak_report']['is_clean'] else 'VIOLATION'}")
    print(f"Collisions d'IDs : {len(res['deduplication']['id_collisions'])}")
    print(f"Doublons d'images : {len(res['deduplication']['exact_image_duplicates'])}")
    print("=================================================================\n")


if __name__ == "__main__":
    run_qa_cli()
