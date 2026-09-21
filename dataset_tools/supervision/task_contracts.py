# -*- coding: utf-8 -*-
"""
ARCHI-AI — Spécification Formelle des Task Contracts (Task Contracts V2)
========================================================================
Définit le schéma formel et le contrat d'exécution pour chaque tâche du catalogue (69 tâches).
Chaque contrat établit :
- La famille architecturale et la modalité stricte
- Les entrées requises et les sources admissibles
- L'évidence nécessaire (grounding obligatoire)
- La structure de la cible attendue
- Les raisonnements permis et les hypothèses interdites
- L'échelle de difficulté (L1 à L6)
- La méthode d'évaluation et les modes d'échec identifiés
- Le statut forensic (VALID, PARTIAL, DUPLICATE, FAKE_MULTIMODAL, UNDERSPECIFIED, INVALID, MISSING_EVIDENCE)
"""

import json
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    VALID = "VALID"
    PARTIAL = "PARTIAL"
    DUPLICATE = "DUPLICATE"
    FAKE_MULTIMODAL = "FAKE_MULTIMODAL"
    UNDERSPECIFIED = "UNDERSPECIFIED"
    INVALID = "INVALID"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"


class TaskContract(BaseModel):
    task_id: str
    number: int
    task_name: str
    domain: str
    task_family: str
    modality: str
    input_types: List[str]
    required_evidence: List[str]
    target_type: str
    reasoning_requirement: str
    allowed_reasoning: List[str]
    forbidden_assumptions: List[str]
    difficulty_levels: List[str]
    source_requirements: List[str]
    negative_examples_allowed: bool = False
    evaluation_method: str
    quality_requirements: List[str]
    known_failure_modes: List[str]
    status: TaskStatus
    notes: Optional[str] = None


def get_all_task_contracts() -> Dict[str, TaskContract]:
    """Retourne l'ensemble des 69 contrats formels audités."""
    from .task_catalogue import TASK_CATALOGUE
    from .scratch_eval_tasks import TASK_AUDIT_SPECS

    contracts = {}
    for tid, t in sorted(TASK_CATALOGUE.items(), key=lambda x: x[1].number):
        spec = TASK_AUDIT_SPECS.get(tid, {})
        diffs = [d.value.split('_')[0] for d in t.allowed_difficulties]

        allowed_reasoning = [
            "Déduction géométrique directe à partir des coordonnées/masques",
            "Confrontation des seuils normatifs applicables (ERP/PMR/Neufert)",
            "Propagation topologique de connectivité entre locaux adjacents",
            "Analyse des contrastes de réflectance et distribution lumineuse",
            "Requêtage exact des entités et jeux de propriétés IFC"
        ]

        forbidden_assumptions = [
            "Supposer une échelle métrique sans échelle graphique ou cote explicite",
            "Inventer des surfaces en m² à partir d'un nombre brut de pixels",
            "Assumer la présence de mobilier non visualisé sur le plan",
            "Déclarer des pathologies constructives sans indices tangibles",
            "Répéter des formules génériques toutes faites ('organisation matricielle')"
        ]

        failure_modes = [
            "FALSE_PASS_GENERIC (phrases statiques recopiées aveuglément)",
            "FAKE_MULTIMODAL (la question divulgue la réponse ou l'image est inutile)",
            "UNSCALED_PIXEL_ANOMALY (confusion pixel / mètre carré)",
            "SHORTCUT_LEAK (nom de fichier ou token clé divulguant la solution)",
            "UNSUPPORTED_CLAIM (affirmation non démontrable par les assets)"
        ]

        contract = TaskContract(
            task_id=tid,
            number=t.number,
            task_name=t.name,
            domain=t.default_domain.value,
            task_family=spec.get("family", t.group.value),
            modality=spec.get("modality", "MULTIMODAL"),
            input_types=spec.get("input_types", ["generic"]),
            required_evidence=[spec.get("grounding", "DIRECT_EVIDENCE")],
            target_type=spec.get("target_type", "structured_response"),
            reasoning_requirement=f"Raisonnement {t.default_learning_type.value} axé sur {t.default_skill.value}",
            allowed_reasoning=allowed_reasoning,
            forbidden_assumptions=forbidden_assumptions,
            difficulty_levels=diffs,
            source_requirements=spec.get("sources", []),
            negative_examples_allowed=tid in [
                "PLAN_ERROR_DETECTION", "DESIGN_PROBLEM_DETECTION", "CLEARANCE_CHECK",
                "CIRCULATION_CHECK", "ACCESSIBILITY_ANALYSIS", "IMAGE_PLUS_TEXT"
            ],
            evaluation_method="DETERMINISTIC_RUBRIC_AND_VERIFIER" if t.requires_deterministic_verification else "MULTI_CRITERIA_RUBRIC",
            quality_requirements=[
                "Grounding tangible obligatoire dans inputs",
                "Décomposition épistémique stricte (OBSERVATION / INTERPRETATION / INFERENCE)",
                "Non-sycophancie et absence de clichés génériques"
            ],
            known_failure_modes=failure_modes,
            status=TaskStatus(spec.get("status", "VALID")),
            notes=spec.get("notes", "")
        )
        contracts[tid] = contract

    return contracts


def export_task_manifest(output_file: Path) -> int:
    """Exporte le catalogue officiel sous forme de TASK_MANIFEST.jsonl."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    contracts = get_all_task_contracts()
    count = 0
    with open(output_file, "w", encoding="utf-8") as f:
        for contract in contracts.values():
            f.write(contract.model_dump_json() + "\n")
            count += 1
    return count
