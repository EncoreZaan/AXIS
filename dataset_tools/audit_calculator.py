# -*- coding: utf-8 -*-
"""
Full Forensic and Quality Audit Calculator for Wave 1 Dataset.
Computes precise numbers, percentages, samples, and taxonomy mapping.
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
TRAIN_PATH = str(REPO_ROOT / "dataset" / "master" / "v1" / "supervision" / "wave1" / "splits" / "train.jsonl")
VAL_PATH = str(REPO_ROOT / "dataset" / "master" / "v1" / "supervision" / "wave1" / "splits" / "validation.jsonl")
BENCH_PATH = str(REPO_ROOT / "dataset" / "master" / "v1" / "supervision" / "wave1" / "splits" / "benchmark.jsonl")

def run_analysis():
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        examples = [json.loads(l) for l in f]

    with open(TRAIN_PATH, 'r', encoding='utf-8') as f:
        train_ex = [json.loads(l) for l in f]
    with open(VAL_PATH, 'r', encoding='utf-8') as f:
        val_ex = [json.loads(l) for l in f]
    with open(BENCH_PATH, 'r', encoding='utf-8') as f:
        bench_ex = [json.loads(l) for l in f]

    print("=== DATASET OVERVIEW ===")
    print(f"Total: {len(examples)} | Train: {len(train_ex)} | Val: {len(val_ex)} | Bench: {len(bench_ex)}")

    # 1. Benchmark leakage check
    print("\n=== BENCHMARK LEAKAGE AUDIT ===")
    bench_source_ids = set()
    for e in bench_ex:
        bench_source_ids.update(e['source_ids'])
    
    train_source_ids = set()
    for e in train_ex:
        train_source_ids.update(e['source_ids'])
        
    val_source_ids = set()
    for e in val_ex:
        val_source_ids.update(e['source_ids'])

    leak_train = bench_source_ids & train_source_ids
    leak_val = bench_source_ids & val_source_ids
    print(f"Benchmark source IDs count: {len(bench_source_ids)}")
    print(f"Train/Bench shared source IDs: {len(leak_train)}")
    print(f"Val/Bench shared source IDs: {len(leak_val)}")

    bench_q_hashes = set(e['question'].strip() for e in bench_ex)
    train_q_hashes = set(e['question'].strip() for e in train_ex)
    leak_q = bench_q_hashes & train_q_hashes
    print(f"Train/Bench exact question overlap: {len(leak_q)}")

    # 2. WARNING Audit (34 warnings)
    print("\n=== WARNING AUDIT ===")
    warnings = [e for e in examples if e['quality_status'] == 'WARNING']
    print(f"Total warnings: {len(warnings)} ({len(warnings)/len(examples)*100:.2f}%)")
    warn_by_task = Counter(e['task_type'] for e in warnings)
    warn_by_split = Counter(e['split'] for e in warnings)
    warn_by_src = Counter(e['source_provenance'].get('source_name') for e in warnings)
    print(f"  By task: {dict(warn_by_task)}")
    print(f"  By split: {dict(warn_by_split)}")
    print(f"  By source: {dict(warn_by_src)}")

    # 3. FALSE PASS Detection & Categorization
    print("\n=== FALSE PASS DETAILED DETECTION ===")
    # Categories:
    # FALSE_PASS_GROUNDING
    # FALSE_PASS_HALLUCINATION
    # FALSE_PASS_GENERIC
    # FALSE_PASS_WRONG_TASK
    # FALSE_PASS_WRONG_DIFFICULTY
    # FALSE_PASS_REDUNDANT
    # FALSE_PASS_WEAK_REASONING
    # FALSE_PASS_FAKE_MULTIMODAL
    # FALSE_PASS_SYCOPHANTIC
    # FALSE_PASS_BAD_PROVENANCE

    false_passes = defaultdict(list)

    for e in examples:
        if e['quality_status'] != 'PASS':
            continue
        eid = e['id']
        ttype = e['task_type']
        ans = e['answer']
        diff = e['difficulty']
        inputs = e['inputs']
        gt = e['ground_truth']

        # Check Grounding: None in answer / uncalculated normalized values
        if 'None' in ans or any(v is None for v in gt.values() if isinstance(v, (str, float, int))):
            false_passes['FALSE_PASS_GROUNDING'].append((eid, "Contient 'None' ou valeur non calculée dans la réponse/ground_truth"))

        # Check Fake Multimodal
        # Group L or task containing MULTIMODAL, or IMAGE_PLUS_TEXT
        if ttype == 'IMAGE_PLUS_TEXT':
            # Check if there is text in inputs
            if not inputs.get('text_contexts') and not inputs.get('plans'):
                false_passes['FALSE_PASS_FAKE_MULTIMODAL'].append((eid, "Tâche IMAGE_PLUS_TEXT sans aucune entrée textuelle dans inputs (seulement image)"))
        
        # Check Generic & Weak Reasoning
        # Critique tasks that have hardcoded phrases
        if ttype in ('PROJECT_CRITIQUE', 'TRADEOFF_ANALYSIS', 'GUIDED_REASONING'):
            if "transition entre l'entrée et l'espace de vie manque de filtre spatial" in ans or \
               "salon cathédrale baigné de lumière" in ans or \
               "goulot central" in ans:
                false_passes['FALSE_PASS_GENERIC'].append((eid, "Template statique de critique/arbitrage/maïeutique appliqué aveuglément sans ancrage plan"))
                false_passes['FALSE_PASS_WEAK_REASONING'].append((eid, "Raisonnement préfabriqué non dérivé des caractéristiques spatiales réelles"))

        # Check BIM Spatial Hierarchy generic template
        if ttype == 'BIM_SPATIAL_HIERARCHY':
            if "L'arborescence spatiale organise le modèle selon la séquence canonique : IfcProject" in ans:
                false_passes['FALSE_PASS_GENERIC'].append((eid, "Template statique d'arborescence IFC répété sans extraction de l'arbre réel de la maquette"))

        # Check Object Relation generic template
        if ttype == 'OBJECT_RELATION':
            if "sont positionnés en vis-à-vis / proximité dans la même zone d'usage" in ans:
                false_passes['FALSE_PASS_GENERIC'].append((eid, "Relation spatiale 3D supposée arbitrairement (vis-à-vis) sans calcul de distance euclidienne"))

        # Check RPLAN Floorplan Reading generic template
        if ttype == 'FLOORPLAN_READING' and e['source_provenance'].get('source_name') == 'CORE_RPLAN':
            if "Plan matriciel segmenté : parois, baies et espaces délimités" in ans:
                false_passes['FALSE_PASS_GENERIC'].append((eid, "Description générique de plan matriciel sans extraction d'entités réelles ni métrés"))

        # Check Material Application generic template
        if ttype == 'MATERIAL_APPLICATION':
            if "Ce matériau convient pour des surfaces de type sol ou doublage mural" in ans:
                false_passes['FALSE_PASS_GENERIC'].append((eid, "Prescription de matériau générique sans contrainte d'espace ni usage réel"))

        # Check Lighting Analysis generic template
        if ttype == 'LIGHTING_ANALYSIS':
            if "L'apport lumineux génère des ombres nettes ou diffuses adaptées à la mise en scène spatiale." in ans:
                false_passes['FALSE_PASS_GENERIC'].append((eid, "Analyse photométrique générique répétée à l'identique"))

        # Check Wrong Difficulty
        # CLEARANCE_CHECK is single lookup table -> labeled L3, but actually L1
        if ttype == 'CLEARANCE_CHECK' and diff == 'L3_ANALYSE':
            false_passes['FALSE_PASS_WRONG_DIFFICULTY'].append((eid, "CLEARANCE_CHECK (consultation d'une cote unitaire) surcoté L3 au lieu de L1"))
        
        # TRADEOFF_ANALYSIS labeled L6, but has no actual multi-constraint solving -> L2/L3 template
        if ttype == 'TRADEOFF_ANALYSIS' and diff == 'L6_MULTICONTRAINTE':
            false_passes['FALSE_PASS_WRONG_DIFFICULTY'].append((eid, "TRADEOFF_ANALYSIS labellisé L6 sans aucun calcul de compromis effectif"))

        # Empty inputs
        has_any_input = any(bool(v) for k, v in inputs.items())
        if not has_any_input:
            false_passes['FALSE_PASS_BAD_PROVENANCE'].append((eid, "Entrées multimodales totalement vides (ModalInputs vide)"))

    print("FALSE PASS COUNTS BY CATEGORY:")
    unique_false_pass_ids = set()
    for cat, items in sorted(false_passes.items()):
        unique_eids = set(x[0] for x in items)
        unique_false_pass_ids.update(unique_eids)
        print(f"  {cat}: {len(items)} occurrences ({len(unique_eids)} exemples uniques)")

    print(f"\nTotal unique PASS examples with at least one FALSE PASS flaw: {len(unique_false_pass_ids)} / 905 ({len(unique_false_pass_ids)/905*100:.1f}%)")

    # 4. Redundancy & Template Clustering
    print("\n=== SEMANTIC REDUNDANCY AUDIT ===")
    answer_clusters = defaultdict(list)
    for e in examples:
        # mask numbers and quotes
        norm = re.sub(r'\b\d+(\.\d+)?\b', '<NUM>', e['answer'])
        norm = re.sub(r"'[^']*'", '<STR>', norm)
        norm = re.sub(r'"[^"]*"', '<STR>', norm)
        # normalize whitespace
        norm = " ".join(norm.split())
        answer_clusters[norm[:80]].append(e['id'])

    print(f"Unique template prefixes (first 80 chars normalized): {len(answer_clusters)}")
    for templ, ids in sorted(answer_clusters.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"  [{len(ids)}x] {templ}...")

    # 5. Difficulty Matrix (Declared vs Actual)
    print("\n=== DIFFICULTY CALIBRATION AUDIT ===")
    # Count declared difficulty
    decl_diff = Counter(e['difficulty'] for e in examples)
    print("Declared difficulties:", dict(decl_diff))

if __name__ == '__main__':
    run_analysis()
