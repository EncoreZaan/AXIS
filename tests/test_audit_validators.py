# -*- coding: utf-8 -*-
"""
test_audit_validators.py — Tests des Nouveaux Validateurs Qualitatifs ARCHI-AI
==============================================================================
Teste les 3 nouveaux validateurs introduits lors de l'Audit Approfondi Wave 1 :
- GenericAnswerValidator
- MultimodalDependencyValidator
- DifficultyValidator
"""

import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dataset_tools.supervision.schema import (
    SupervisedExample,
    DifficultyLevel,
    QualityStatus,
    ModalInputs,
)
from dataset_tools.supervision.validators.generic_answer_validator import GenericAnswerValidator
from dataset_tools.supervision.validators.multimodal_dependency_validator import MultimodalDependencyValidator
from dataset_tools.supervision.validators.difficulty_validator import DifficultyValidator


def test_generic_answer_validator_detects_placeholder_none():
    val = GenericAnswerValidator()
    ex = SupervisedExample(
        id="TEST_NONE_BUG",
        task_type="CLEARANCE_CHECK",
        task_group="E_ERGONOMICS",
        domain="ergonomics",
        skill="ergonomics",
        learning_type="rule_check",
        difficulty=DifficultyLevel.L1,
        source_ids=["S1"],
        source_provenance={"source_name": "S", "dataset_name": "D", "raw_file": "F"},
        question="Quelle cote ?",
        answer="Standard : valeur 90 cm (soit None m).",
    )
    res = val.validate(ex)
    assert res.status == QualityStatus.REVIEW
    assert "placeholder non résolue" in res.message


def test_generic_answer_validator_detects_cliche():
    val = GenericAnswerValidator()
    ex = SupervisedExample(
        id="TEST_CLICHE",
        task_type="FLOORPLAN_READING",
        task_group="B_FLOORPLAN",
        domain="architecture",
        skill="plan_reading",
        learning_type="observation",
        difficulty=DifficultyLevel.L1,
        source_ids=["S1"],
        source_provenance={"source_name": "S", "dataset_name": "D", "raw_file": "F"},
        question="Que voyez-vous ?",
        answer="Plan matriciel segmenté : parois, baies et espaces délimités avec cloisons.",
    )
    res = val.validate(ex)
    assert res.status == QualityStatus.WARNING
    assert "Formulation générique" in res.message


def test_multimodal_dependency_validator_detects_fake_multimodal():
    val = MultimodalDependencyValidator()
    ex = SupervisedExample(
        id="TEST_FAKE_MM",
        task_type="IMAGE_PLUS_TEXT",
        task_group="L_MULTIMODAL",
        domain="multimodal",
        skill="multimodal_reasoning",
        learning_type="cross_modal",
        difficulty=DifficultyLevel.L3,
        source_ids=["S1"],
        source_provenance={"source_name": "S", "dataset_name": "D", "raw_file": "F"},
        inputs=ModalInputs(images=[{"path": "dummy.jpg"}]),  # Pas de text_contexts !
        question="Confrontez image et texte.",
        answer="L'image montre les ouvertures.",
    )
    res = val.validate(ex)
    assert res.status == QualityStatus.REVIEW
    assert "FAKE_MULTIMODAL" in res.message


def test_difficulty_validator_flags_overrated_clearance_check():
    val = DifficultyValidator()
    ex = SupervisedExample(
        id="TEST_OVERRATED_ERGO",
        task_type="CLEARANCE_CHECK",
        task_group="E_ERGONOMICS",
        domain="ergonomics",
        skill="ergonomics",
        learning_type="rule_check",
        difficulty=DifficultyLevel.L5,  # Consultation d'une simple cote labellisée L5 !
        source_ids=["S1"],
        source_provenance={"source_name": "S", "dataset_name": "D", "raw_file": "F"},
        question="Quelle est la cote ?",
        answer="La cote minimale est 90 cm.",
    )
    res = val.validate(ex)
    assert res.status == QualityStatus.WARNING
    assert "Surévaluation de difficulté" in res.message
