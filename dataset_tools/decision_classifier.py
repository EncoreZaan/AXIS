# -*- coding: utf-8 -*-
"""
Exhaustive Classifier & Report Generator for ARCHI-AI Wave 1 Audit.
Assigns RETAIN / CORRECT / REVIEW / EXCLUDE to each of the 939 examples.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Repository root, resolved from this file's location (this used to be reached
# via a local `ARCHI_AI/` directory junction — see DATASET.md §6 for history).
REPO_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = str(REPO_ROOT / "dataset" / "master" / "v1" / "supervision" / "wave1" / "wave1_dataset.jsonl")

def classify_all():
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        examples = [json.loads(line) for line in f]

    decisions = Counter()
    decision_details = defaultdict(list)
    by_group = defaultdict(lambda: Counter())
    by_task = defaultdict(lambda: Counter())

    for ex in examples:
        eid = ex['id']
        ttype = ex['task_type']
        group = ex['task_group']
        src = ex['source_provenance'].get('source_name', '')
        diff = ex['difficulty']
        ans = ex['answer']
        inputs = ex['inputs']
        qstatus = ex['quality_status']

        has_any_input = any(bool(v) for k, v in inputs.items())

        # Decision rules:
        # 1. EXCLUDE:
        # - FAKE_MULTIMODAL: IMAGE_PLUS_TEXT with no text in inputs (25 ex)
        # - Completely empty inputs for tasks that require modal inputs (Group J & K: 64 ex)
        if ttype == 'IMAGE_PLUS_TEXT' and not inputs.get('text_contexts'):
            d = 'EXCLUDE'
            reason = 'FAKE_MULTIMODAL : tâche IMAGE_PLUS_TEXT sans modalité texte dans inputs'
        elif not has_any_input:
            d = 'EXCLUDE'
            reason = 'Entrées multimodales totalement absentes (ModalInputs vide)'
        # 2. CORRECT:
        # - Ergonomics None bug (25 ex): original_value exists, normalized_value is None. Can be automatically repaired.
        elif 'None' in ans and ttype == 'CLEARANCE_CHECK':
            d = 'CORRECT'
            reason = 'Valeur normalisée None m réparable par conversion déterministe (cm -> m)'
        # - Overrated difficulty (e.g. CLEARANCE_CHECK labeled L3, TRADEOFF labeled L6 without formal constraints)
        elif ttype == 'CLEARANCE_CHECK' and diff == 'L3_ANALYSE':
            d = 'CORRECT'
            reason = 'Difficulté L3 surévaluée pour une consultation unitaire (recalibrer en L1/L2)'
        # 3. REVIEW:
        # - Warning examples (34 ex): 33 MMMU + 1 NORMES_FR
        elif qstatus == 'WARNING':
            d = 'REVIEW'
            reason = f'Statut WARNING du QualityGate : {ex.get("quality_checks", [{}])[1].get("message", "")}'
        # - Generic template answers in Floorplan reading (RPLAN: 70 ex), BIM Spatial Hierarchy (70 ex), Lighting (80 ex), Materials (55 ex)
        elif ttype == 'BIM_SPATIAL_HIERARCHY' and "séquence canonique : IfcProject" in ans:
            d = 'REVIEW'
            reason = 'Template générique répliqué 70x sans extraction de la hiérarchie spécifique du fichier IFC'
        elif ttype == 'FLOORPLAN_READING' and src == 'CORE_RPLAN' and "Plan matriciel segmenté : parois, baies" in ans:
            d = 'REVIEW'
            reason = 'Description de plan matriciel 100% template sans mention de pièces ni surfaces réelles'
        elif ttype == 'OBJECT_RELATION' and "sont positionnés en vis-à-vis / proximité" in ans:
            d = 'REVIEW'
            reason = 'Relation spatiale 3D présumée sans calcul de distance euclidienne'
        elif ttype == 'PROJECT_CRITIQUE' and "transition entre l'entrée et l'espace de vie manque de filtre spatial" in ans:
            d = 'REVIEW'
            reason = 'Critique stéréotypée répliquée sans ancrage sur les spécificités du plan'
        elif ttype == 'LIGHTING_ANALYSIS' and "L'apport lumineux génère des ombres nettes ou diffuses" in ans:
            d = 'REVIEW'
            reason = 'Analyse d\'ambiance HDRI formulée de façon générique sans impact spatial calculé'
        elif ttype == 'MATERIAL_APPLICATION' and "Ce matériau convient pour des surfaces de type sol ou doublage mural" in ans:
            d = 'REVIEW'
            reason = 'Prescription de matériau stéréotypée sans contrainte d\'espace'
        # 4. RETAIN:
        else:
            d = 'RETAIN'
            reason = 'Exemple de haute qualité, ancré dans la source, spécifique et directement exploitable'

        decisions[d] += 1
        decision_details[d].append((eid, ttype, src, reason))
        by_group[group][d] += 1
        by_task[ttype][d] += 1

    print("=== DECISIONS BREAKDOWN ===")
    total = len(examples)
    for d, c in decisions.most_common():
        print(f"  {d:8s}: {c:3d} ({c/total*100:5.1f}%)")

    print("\n=== DECISIONS BY TASK GROUP ===")
    for g, counts in sorted(by_group.items()):
        print(f"  {g:25s}: {dict(counts)}")

    print("\n=== DECISIONS BY TASK ===")
    for t, counts in sorted(by_task.items()):
        print(f"  {t:30s}: {dict(counts)}")

if __name__ == '__main__':
    classify_all()
