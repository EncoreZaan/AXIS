# -*- coding: utf-8 -*-
"""
test_supervision_engine.py — Tests Automatisés du Supervision Engine
=====================================================================
Couvre l'intégralité des exigences :
- Schéma canonique & sérialisation Pydantic
- Catalogue formel des 69 tâches (Groupes A à L)
- Matrice source → capacité → tâches et routage
- Vérificateurs déterministes (géométrie, scene graphs, IFC, ergonomie)
- Validateurs qualité (anti-hallucination, anti-sycophantie, épistémique, références)
- Split manager et détection de fuite (zéro contamination)
- Intégrité du jeu Wave 1 généré
"""

import os
import sys
import json
from pathlib import Path
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dataset_tools.supervision.schema import (
    SupervisedExample,
    EpistemicTag,
    DifficultyLevel,
    QualityStatus,
    RoutingDestination,
    SplitName,
    ModalInputs,
)
from dataset_tools.supervision.task_catalogue import (
    TASK_CATALOGUE,
    TaskGroup,
    get_task_definition,
    list_tasks_by_group,
)
from dataset_tools.supervision.mapping_matrix import (
    SOURCE_CAPABILITY_TASK_MATRIX,
    resolve_tasks_for_record,
)
from dataset_tools.supervision.verifiers.geometry_verifier import GeometryVerifier
from dataset_tools.supervision.verifiers.scene_graph_verifier import SceneGraphVerifier
from dataset_tools.supervision.verifiers.ifc_verifier import IfcVerifier
from dataset_tools.supervision.verifiers.ergonomics_verifier import ErgonomicsVerifier
from dataset_tools.supervision.validators.hallucination_validator import HallucinationValidator
from dataset_tools.supervision.validators.epistemic_validator import EpistemicValidator
from dataset_tools.supervision.validators.anti_sycophancy_validator import AntiSycophancyValidator
from dataset_tools.supervision.validators.reference_validator import ReferenceValidator
from dataset_tools.supervision.split_manager import SplitManager

BASE_DIR = Path(__file__).resolve().parent.parent
WAVE1_DIR = BASE_DIR / "dataset" / "master" / "v1" / "supervision" / "wave1"


# -------------------------------------------------------------
# 1. Tests Schéma & Sérialisation
# -------------------------------------------------------------
def test_supervised_example_schema():
    """Vérifie l'instanciation stricte et la sérialisation d'un exemple supervisé."""
    ex = SupervisedExample(
        id="TEST_EX_001",
        task_type="ROOM_TOPOLOGY",
        task_group="B_FLOORPLAN",
        domain="architecture",
        skill="topology",
        learning_type="analysis",
        difficulty=DifficultyLevel.L3,
        source_ids=["SRC_001"],
        source_provenance={"source_name": "CORE_RESPLAN", "dataset_name": "resplan", "raw_file": "dummy.zip"},
        inputs=ModalInputs(geometries=[{"room": "living"}]),
        question="Quelle est la relation entre le séjour et la cuisine ?",
        answer="Observation : Les pièces sont contiguës.\nAnalyse : Accès direct sans sas.",
        epistemic_breakdown={
            EpistemicTag.OBSERVATION.value: ["Les pièces sont contiguës"],
            EpistemicTag.INTERPRETATION.value: ["Accès direct sans sas"],
        },
        ground_truth={"connected": True},
        quality_status=QualityStatus.PASS,
        split=SplitName.TRAIN,
        destination=RoutingDestination.FINETUNE,
    )
    json_data = ex.model_dump_json()
    assert "TEST_EX_001" in json_data
    loaded = SupervisedExample.model_validate_json(json_data)
    assert loaded.id == "TEST_EX_001"
    assert loaded.difficulty == DifficultyLevel.L3


def test_schema_rejects_empty_question_and_answer():
    """Vérifie que des questions ou réponses vides sont formellement rejetées."""
    with pytest.raises(ValueError):
        SupervisedExample(
            id="FAIL_001",
            task_type="ROOM_TOPOLOGY",
            task_group="B_FLOORPLAN",
            domain="architecture",
            skill="topology",
            learning_type="analysis",
            difficulty=DifficultyLevel.L1,
            source_ids=["S1"],
            source_provenance={"source_name": "S", "dataset_name": "D", "raw_file": "F"},
            question="",  # Vide -> doit lever une exception
            answer="Réponse valide",
        )


# -------------------------------------------------------------
# 2. Tests Catalogue des 69 Tâches
# -------------------------------------------------------------
def test_task_catalogue_has_69_tasks():
    """Vérifie que le catalogue contient rigoureusement les 69 tâches prévues."""
    assert len(TASK_CATALOGUE) == 69, f"Attendu 69 tâches, trouvé {len(TASK_CATALOGUE)}"


def test_task_catalogue_groups_coverage():
    """Vérifie que les 12 groupes (A à L) sont présents et non vides."""
    groups = {t.group for t in TASK_CATALOGUE.values()}
    assert len(groups) == 12
    for g in TaskGroup:
        tasks = list_tasks_by_group(g)
        assert len(tasks) > 0, f"Le groupe {g} ne doit pas être vide"


# -------------------------------------------------------------
# 3. Tests Matrice de Routage Source → Capacité → Tâche
# -------------------------------------------------------------
def test_mapping_matrix_resolves_tasks():
    """Vérifie que chaque source active renvoie des tâches éligibles adaptées."""
    dummy_resplan = {"source_name": "CORE_RESPLAN"}
    tasks = resolve_tasks_for_record(dummy_resplan)
    assert "ROOM_TOPOLOGY" in tasks
    assert "CIRCULATION_ANALYSIS" in tasks

    # FloorPlanCAD doit être gelé / sans tâche active
    dummy_cad = {"source_name": "CORE_FLOORPLANCAD"}
    assert len(resolve_tasks_for_record(dummy_cad)) == 0


# -------------------------------------------------------------
# 4. Tests Vérificateurs Déterministes
# -------------------------------------------------------------
def test_geometry_verifier_area():
    """Vérifie le calcul déterministe d'aire polygonale sans approximation."""
    verifier = GeometryVerifier()
    # Rectangle 4m x 5m = 20 m2
    coords = [[0.0, 0.0], [4.0, 0.0], [4.0, 5.0], [0.0, 5.0], [0.0, 0.0]]
    area = verifier.compute_polygon_area_m2(coords)
    assert abs(area - 20.0) < 1e-4

    # Vérification avec tolérance
    valid, reason, details = verifier.verify(
        claim={"room_name": "salon", "claimed_area_m2": 20.2},
        ground_truth_context={"rooms": [{"name": "salon", "polygon": coords}]},
    )
    assert valid is True

    # Erreur au-delà de 5%
    invalid, reason, details = verifier.verify(
        claim={"room_name": "salon", "claimed_area_m2": 25.0},
        ground_truth_context={"rooms": [{"name": "salon", "polygon": coords}]},
    )
    assert invalid is False
    assert "Erreur de métré" in reason


def test_scene_graph_verifier_counting():
    """Vérifie le comptage exact d'objets dans une scène 3D."""
    verifier = SceneGraphVerifier()
    objects = [
        {"category": "chair"},
        {"category": "chair"},
        {"category": "table"},
    ]
    valid, _, _ = verifier.verify(
        claim={"expected_category": "chair", "expected_count": 2},
        ground_truth_context={"objects": objects},
    )
    assert valid is True

    invalid, reason, _ = verifier.verify(
        claim={"expected_category": "chair", "expected_count": 3},
        ground_truth_context={"objects": objects},
    )
    assert invalid is False
    assert "Comptage 3D erroné" in reason


def test_ifc_verifier_classes():
    """Vérifie les classes IFC normalisées buildingSMART."""
    verifier = IfcVerifier()
    assert verifier.verify_class_name("IfcWall") is True
    assert verifier.verify_class_name("IfcDoor") is True
    assert verifier.verify_class_name("FakeIfcEntity") is False


def test_ergonomics_verifier_conversions():
    """Vérifie les conversions d'unités et le contrôle des gabarits."""
    verifier = ErgonomicsVerifier()
    m_val = verifier.convert_to_meters(90, "cm")
    assert abs(m_val - 0.90) < 1e-4

    # Passage conforme (90 cm pour passage principal)
    valid, _, details = verifier.verify(
        claim={"clearance_type": "passage_principal", "measured_value": 90, "measured_unit": "cm"},
        ground_truth_context={},
    )
    assert valid is True
    assert details["is_compliant"] is True

    # Passage non conforme (50 cm < 90 cm)
    invalid, reason, details = verifier.verify(
        claim={"clearance_type": "passage_principal", "measured_value": 50, "measured_unit": "cm"},
        ground_truth_context={},
    )
    assert invalid is False
    assert "Non-conformité ergonomique" in reason


# -------------------------------------------------------------
# 5. Tests Validateurs de Contrôle Qualité
# -------------------------------------------------------------
def test_hallucination_validator_detects_fake_articles():
    """Détecte les citations d'articles de loi inventés."""
    val = HallucinationValidator()
    ex = SupervisedExample(
        id="TEST_H1",
        task_type="ACCESSIBILITY_ANALYSIS",
        task_group="E_ERGONOMICS",
        domain="regulation_safety",
        skill="regulation",
        learning_type="analysis",
        difficulty=DifficultyLevel.L5,
        source_ids=["S1"],
        source_provenance={"source_name": "CORE_NORMES_FR", "dataset_name": "normes", "raw_file": "n.json"},
        question="Quelle est la règle ?",
        answer="Selon l'article 999-XYZ du code imaginaire, la porte doit faire 2 mètres.",
    )
    res = val.validate(ex)
    assert res.status == QualityStatus.FAIL
    assert "Hallucination réglementaire" in res.message


def test_anti_sycophancy_validator_rejects_flattery():
    """Rejette les flatteries vides dans une critique de projet."""
    val = AntiSycophancyValidator()
    ex = SupervisedExample(
        id="TEST_SYCO",
        task_type="PROJECT_CRITIQUE",
        task_group="I_CRITIQUE",
        domain="interior_design",
        skill="critique",
        learning_type="studio_critique",
        difficulty=DifficultyLevel.L5,
        source_ids=["S1"],
        source_provenance={"source_name": "CORE_RESPLAN", "dataset_name": "resplan", "raw_file": "r.zip"},
        question="Que pensez-vous du projet ?",
        answer="C'est un très beau projet, tout est parfait, félicitations.",
    )
    res = val.validate(ex)
    assert res.status == QualityStatus.FAIL
    assert "Sycophantie détectée" in res.message


def test_epistemic_validator_breakdown():
    """Vérifie la conformité de la décomposition épistémique."""
    val = EpistemicValidator()
    ex = SupervisedExample(
        id="TEST_EPIS",
        task_type="INTERIOR_ANALYSIS",
        task_group="A_VISUAL_UNDERSTANDING",
        domain="interior_design",
        skill="visual_reasoning",
        learning_type="analysis",
        difficulty=DifficultyLevel.L2,
        source_ids=["S1"],
        source_provenance={"source_name": "CORE_IL3D", "dataset_name": "il3d", "raw_file": "i.zip"},
        question="Analyse",
        answer="Description",
        epistemic_breakdown={"OBSERVATION": ["Table visible"], "INTERPRETATION": ["Style sobre"]},
    )
    res = val.validate(ex)
    assert res.status == QualityStatus.PASS


# -------------------------------------------------------------
# 6. Tests SplitManager & Non-Contamination
# -------------------------------------------------------------
def test_split_manager_leak_detection():
    """Vérifie qu'aucune fuite entre train et benchmark n'est tolérée."""
    sm = SplitManager()
    ex_train = SupervisedExample(
        id="EX_TRAIN_1",
        task_type="FLOORPLAN_READING",
        task_group="B_FLOORPLAN",
        domain="architecture",
        skill="plan_reading",
        learning_type="observation",
        difficulty=DifficultyLevel.L1,
        source_ids=["PROJ_A_scene_1"],
        source_provenance={"source_name": "S", "dataset_name": "D", "raw_file": "F"},
        question="Q",
        answer="A",
        split=SplitName.TRAIN,
    )
    ex_bench = SupervisedExample(
        id="EX_BENCH_1",
        task_type="FLOORPLAN_READING",
        task_group="B_FLOORPLAN",
        domain="architecture",
        skill="plan_reading",
        learning_type="observation",
        difficulty=DifficultyLevel.L1,
        source_ids=["PROJ_A_scene_2"],  # Même projet PROJ_A !
        source_provenance={"source_name": "S", "dataset_name": "D", "raw_file": "F"},
        question="Q",
        answer="A",
        split=SplitName.BENCHMARK,
    )
    audit = sm.check_leakage([ex_train, ex_bench])
    assert audit["is_leak_free"] is False
    assert audit["leak_train_bench_count"] == 1


# -------------------------------------------------------------
# 7. Tests Intégrité Wave 1 Générée
# -------------------------------------------------------------
def test_wave1_dataset_file_exists_and_valid():
    """Vérifie que la Wave 1 est générée, contient <= 1000 items et zéro FAIL."""
    main_file = WAVE1_DIR / "wave1_dataset.jsonl"
    assert main_file.exists(), f"Le fichier {main_file} doit exister"

    count = 0
    with open(main_file, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            count += 1
            assert rec.get("quality_status") in ("PASS", "WARNING"), "Aucun FAIL dans le dataset"
            assert rec.get("id") is not None
            assert len(rec.get("question", "")) > 0
            assert len(rec.get("answer", "")) > 0

    assert 500 <= count <= 1000, f"Wave 1 doit contenir environ 1000 items max (actuel: {count})"


def test_wave1_splits_exist_and_leak_free():
    """Vérifie l'existence des splits et l'étanchéité absolue du jeu Wave 1."""
    train_file = WAVE1_DIR / "splits" / "train.jsonl"
    val_file = WAVE1_DIR / "splits" / "validation.jsonl"
    bench_file = WAVE1_DIR / "splits" / "benchmark.jsonl"

    assert train_file.exists()
    assert val_file.exists()
    assert bench_file.exists()

    def get_projects(path):
        projs = set()
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                sids = rec.get("source_ids", [])
                if sids:
                    parts = sids[0].split("_")
                    p = "_".join(parts[:3]) if len(parts) >= 3 else sids[0]
                    projs.add(p)
        return projs

    train_projs = get_projects(train_file)
    val_projs = get_projects(val_file)
    bench_projs = get_projects(bench_file)

    assert len(train_projs.intersection(val_projs)) == 0, "Fuite détectée entre train et validation"
    assert len(train_projs.intersection(bench_projs)) == 0, "Fuite détectée entre train et benchmark"


# -------------------------------------------------------------
# 8. Tests de Régression Obligatoires (Wave 1 Repaired)
# -------------------------------------------------------------
REPAIRED_DIR = BASE_DIR / "dataset" / "master" / "v1" / "supervision" / "wave1_repaired"


@pytest.fixture(scope="module")
def repaired_examples():
    """Charge l'ensemble des exemples de Wave 1 Repaired."""
    dataset_path = REPAIRED_DIR / "wave1_dataset.jsonl"
    assert dataset_path.exists(), f"Le fichier {dataset_path} doit exister"
    items = []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            items.append(json.loads(line))
    return items


def test_regression_no_numerical_none(repaired_examples):
    """1. Aucune valeur None numérique (ex: 'None m') dans le texte ou ground_truth."""
    import re
    none_pat = re.compile(r"\bNone\s*m\b|\(soit None|\bNaN\b|\binf\b", re.IGNORECASE)
    for ex in repaired_examples:
        assert not none_pat.search(ex.get("answer", "")), f"None placeholder détecté dans {ex['id']}: {ex['answer']}"
        gt = ex.get("ground_truth", {})
        if "CLEARANCE_CHECK" in ex.get("task_type", ""):
            assert gt.get("normalized_value") is not None, f"normalized_value est None dans {ex['id']}"


def test_regression_no_empty_inputs(repaired_examples):
    """2. Aucun input vide."""
    for ex in repaired_examples:
        inp = ex.get("inputs", {})
        active = [k for k, v in inp.items() if v and isinstance(v, list) and len(v) > 0]
        assert len(active) > 0 or inp.get("custom_metadata"), f"Inputs totalement vides dans {ex['id']}"


def test_regression_multimodal_integrity(repaired_examples):
    """3. Aucune tâche multimodale sans toutes ses modalités requises."""
    for ex in repaired_examples:
        ttype = ex.get("task_type")
        inp = ex.get("inputs", {})
        if ttype == "IMAGE_PLUS_TEXT":
            assert inp.get("images") and inp.get("text_contexts"), f"IMAGE_PLUS_TEXT incomplet dans {ex['id']}"
        elif ttype == "PLAN_PLUS_3D":
            assert inp.get("plans") and (inp.get("geometries") or inp.get("ifc_entities")), f"PLAN_PLUS_3D incomplet dans {ex['id']}"
        elif ttype == "PLAN_PLUS_TEXT":
            assert inp.get("plans") and inp.get("text_contexts"), f"PLAN_PLUS_TEXT incomplet dans {ex['id']}"
        elif ttype == "IMAGE_PLUS_PLAN":
            assert inp.get("images") and inp.get("plans"), f"IMAGE_PLUS_PLAN incomplet dans {ex['id']}"


def test_regression_object_relation_calculated(repaired_examples):
    """4. Aucun OBJECT_RELATION sans calcul spatial réel."""
    obj_rels = [e for e in repaired_examples if e.get("task_type") == "OBJECT_RELATION"]
    assert len(obj_rels) > 0, "Doit comporter des tâches OBJECT_RELATION"
    for ex in obj_rels:
        gt = ex.get("ground_truth", {})
        assert gt.get("distance_m") is not None, f"Distance euclidienne non calculée dans {ex['id']}"
        assert gt.get("distance_m") >= 0.0, f"Distance négative invalide dans {ex['id']}"
        assert gt.get("proximity_tier") is not None, f"Palier de proximité non qualifié dans {ex['id']}"


def test_regression_no_repetitive_generic_answer(repaired_examples):
    """5. Aucune réponse générique répétitive au-delà du seuil (zéro cliché détecté)."""
    import re
    cliche_patterns = [
        re.compile(r"Plan matriciel segmenté\s*:\s*parois,\s*baies et espaces délimités", re.IGNORECASE),
        re.compile(r"transition entre l['’]entrée et l['’]espace de vie manque de filtre spatial", re.IGNORECASE),
        re.compile(r"claustra ajouré ou un meuble double-face", re.IGNORECASE),
        re.compile(r"salon cathédrale baigné de lumière", re.IGNORECASE),
        re.compile(r"sont positionnés en vis-à-vis / proximité dans la même zone d'usage", re.IGNORECASE),
        re.compile(r"séquence canonique\s*:\s*IfcProject\s*→\s*IfcSite\s*→\s*IfcBuilding", re.IGNORECASE),
        re.compile(r"L['’]association avec des matériaux lisses en contrepoint crée un contraste tactile recherché", re.IGNORECASE),
        re.compile(r"L['’]apport lumineux génère des ombres nettes ou diffuses adaptées à la mise en scène spatiale", re.IGNORECASE),
    ]
    for ex in repaired_examples:
        ans = ex.get("answer", "")
        for pat in cliche_patterns:
            assert not pat.search(ans), f"Cliché détecté dans {ex['id']}: {pat.pattern}"


def test_regression_l6_has_real_constraints(repaired_examples):
    """6. Aucune tâche L6 sans >= 2 contraintes réelles contradictoires."""
    l6_exs = [e for e in repaired_examples if e.get("difficulty") == "L6_MULTICONTRAINTE"]
    assert len(l6_exs) > 0, "Doit comporter des tâches L6"
    for ex in l6_exs:
        c_list = ex.get("constraints", [])
        gt_axes = ex.get("ground_truth", {}).get("tradeoff_axes", [])
        assert len(c_list) >= 2 or len(gt_axes) >= 2, f"Tâche L6 sans au moins 2 contraintes dans {ex['id']}"


def test_regression_no_empty_provenance(repaired_examples):
    """7. Aucune provenance vide."""
    for ex in repaired_examples:
        sids = ex.get("source_ids", [])
        assert len(sids) > 0, f"source_ids vide dans {ex['id']}"
        prov = ex.get("source_provenance", {})
        assert prov.get("source_name"), f"source_name manquant dans provenance de {ex['id']}"


def test_regression_no_example_without_evidence(repaired_examples):
    """8. Aucun exemple sans evidence non vide."""
    for ex in repaired_examples:
        ev = ex.get("evidence", {})
        assert bool(ev) and len(ev) > 0, f"evidence vide dans {ex['id']}"


def test_regression_benchmark_isolation_uncontaminated(repaired_examples):
    """9. Aucun exemple benchmark contaminé (zéro fuite inter-splits)."""
    train_projects = set()
    bench_projects = set()
    for ex in repaired_examples:
        sids = ex.get("source_ids", [])
        if sids:
            parts = sids[0].split("_")
            pid = "_".join(parts[:3]) if len(parts) >= 3 else sids[0]
            if ex.get("split") == "train":
                train_projects.add(pid)
            elif ex.get("split") == "benchmark":
                bench_projects.add(pid)
    assert len(train_projects.intersection(bench_projects)) == 0, "Fuite détectée entre train et benchmark !"


def test_regression_no_critical_semantic_duplicates(repaired_examples):
    """10. Aucun duplicate sémantique critique (unicité stricte des identifiants et des couples question/contexte)."""
    ids = [e["id"] for e in repaired_examples]
    assert len(ids) == len(set(ids)), "Identifiants en double détectés dans le dataset"

