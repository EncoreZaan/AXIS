# -*- coding: utf-8 -*-
"""
Gold Set Builder and Detailed Auditor for ARCHI-AI Wave 1.
Selects and audits high-quality candidate examples across the 11 required capabilities.
Generates gold_set.jsonl, gold_set_manifest.json, and scores each example on the 12 audit axes.
"""
import json
import re
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Repository root, resolved from this file's location (this used to be reached
# via a local `ARCHI_AI/` directory junction — see DATASET.md §6 for history).
REPO_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = str(REPO_ROOT / "dataset" / "master" / "v1" / "supervision" / "wave1" / "wave1_dataset.jsonl")
GOLD_DIR = str(REPO_ROOT / "dataset" / "master" / "v1" / "supervision" / "gold_set")

# 12-axis internal audit scoring functions
# A - Grounding (0-10)
# B - Exactitude (0-10)
# C - Pertinence (0-10)
# D - Raisonnement (0-10)
# E - Architecture intérieure (0-10)
# F - Multimodalité (0-10)
# G - Épistémologie (0-10)
# H - Non-hallucination (0-10)
# I - Non-sycophantie (0-10)
# J - Pédagogie (0-10)
# K - Difficulté (0-10)
# L - Diversité (0-10)

def score_example(ex):
    scores = {}
    ans = ex['answer']
    q = ex['question']
    gt = ex['ground_truth']
    ttype = ex['task_type']
    group = ex['task_group']
    inputs = ex['inputs']

    # A: Grounding
    if 'None' in ans or 'None m' in ans:
        scores['A_Grounding'] = 4.0
    elif not any(inputs.values()):
        scores['A_Grounding'] = 5.0
    elif ttype in ('PROJECT_CRITIQUE', 'TRADEOFF_ANALYSIS') and "transition entre l'entrée" in ans:
        scores['A_Grounding'] = 6.0
    else:
        scores['A_Grounding'] = 8.5

    # B: Exactitude
    if 'None' in ans:
        scores['B_Exactitude'] = 5.0
    else:
        scores['B_Exactitude'] = 8.5

    # C: Pertinence
    scores['C_Pertinence'] = 8.5 if len(ans) > 50 else 5.0

    # D: Raisonnement
    if ttype in ('PROJECT_CRITIQUE', 'TRADEOFF_ANALYSIS', 'GUIDED_REASONING'):
        if "salon cathédrale" in ans or "goulot central" in ans:
            scores['D_Raisonnement'] = 5.0
        else:
            scores['D_Raisonnement'] = 7.5
    elif ttype == 'MULTIMODAL_PROJECT_REASONING' and 'MMMU' in ex['source_provenance'].get('source_name', ''):
        scores['D_Raisonnement'] = 4.0  # Only option letter!
    else:
        scores['D_Raisonnement'] = 7.5

    # E: Architecture intérieure
    if 'MMMU' in ex['source_provenance'].get('source_name', '') and ('triangle' in q.lower() or 'catenary' in q.lower() or 'camera' in q.lower()):
        scores['E_ArchiInt'] = 3.0  # Civil/geodesy engineering, not interior architecture
    else:
        scores['E_ArchiInt'] = 8.0

    # F: Multimodalité
    if ttype == 'IMAGE_PLUS_TEXT' and not inputs.get('text_contexts'):
        scores['F_Multimodalite'] = 3.0
    elif group == 'L_MULTIMODAL' and not (len([k for k, v in inputs.items() if v]) >= 2 or inputs.get('images')):
        scores['F_Multimodalite'] = 4.0
    elif any(inputs.values()):
        scores['F_Multimodalite'] = 8.0
    else:
        scores['F_Multimodalite'] = 5.0

    # G: Épistémologie
    if ex.get('epistemic_breakdown'):
        scores['G_Epistemologie'] = 9.0
    else:
        scores['G_Epistemologie'] = 6.0

    # H: Non-hallucination
    if ex['quality_status'] == 'WARNING' and 'Chiffres potentiellement' in str(ex.get('quality_checks')):
        scores['H_NonHallucination'] = 6.0
    else:
        scores['H_NonHallucination'] = 9.0

    # I: Non-sycophantie
    scores['I_NonSycophantie'] = 9.0

    # J: Pédagogie
    if group == 'K_PEDAGOGY':
        scores['J_Pedagogie'] = 8.0 if "Piste de réflexion" in ans else 6.0
    else:
        scores['J_Pedagogie'] = 7.0

    # K: Difficulté
    if ttype == 'CLEARANCE_CHECK' and ex['difficulty'] == 'L3_ANALYSE':
        scores['K_Difficulte'] = 4.0  # Overrated
    elif ttype == 'TRADEOFF_ANALYSIS' and ex['difficulty'] == 'L6_MULTICONTRAINTE':
        scores['K_Difficulte'] = 5.0  # Overrated
    else:
        scores['K_Difficulte'] = 8.0

    # L: Diversité
    if "Plan matriciel segmenté" in ans or "sont positionnés en vis-à-vis" in ans:
        scores['L_Diversite'] = 4.0
    else:
        scores['L_Diversite'] = 7.5

    mean_score = sum(scores.values()) / len(scores)
    return scores, mean_score

def select_gold_set():
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        examples = [json.loads(l) for l in f]

    os.makedirs(GOLD_DIR, exist_ok=True)

    # We want 35-50 exemplary examples representing the 11 capabilities:
    # 1. Lecture de plan (ResPlan vectoriel avec noms et surfaces exactes)
    # 2. Spatial reasoning (IL3D avec scene graph 3D précis)
    # 3. Circulation (CIRCULATION_ANALYSIS avec flux réels)
    # 4. Ergonomie (standards réglementaires / accessibilité vérifiés sans bug)
    # 5. Matériaux (PBR maps & échelle physique réelles)
    # 6. Lumière (HDRI avec EV et Kelvin exacts)
    # 7. BIM/IFC (IFC-Bench QA certifié & buildingSMART)
    # 8. Critique (Critique structurée)
    # 9. Pédagogie (Guidage maïeutique)
    # 10. Multimodalité (ResBIM 2D+IFC ou StructScan3D)
    # 11. Raisonnement multicontrainte (Accessibilité & contraintes spatiales)

    candidates_by_cap = defaultdict(list)
    for ex in examples:
        ttype = ex['task_type']
        group = ex['task_group']
        src = ex['source_provenance'].get('source_name', '')
        scores, mean_s = score_example(ex)

        # Skip examples with None bug
        if 'None' in ex['answer']:
            continue
        # Skip pure generic template duplicates if better exists
        
        if ttype in ('ROOM_IDENTIFICATION', 'FLOORPLAN_READING', 'PLAN_SUMMARY') and 'RESPLAN' in src:
            candidates_by_cap['lecture_de_plan'].append((ex, scores, mean_s))
        elif ttype in ('SCENE_GRAPH_REASONING', 'OBJECT_RELATION') and 'IL3D' in src:
            candidates_by_cap['spatial_reasoning'].append((ex, scores, mean_s))
        elif ttype == 'CIRCULATION_ANALYSIS':
            candidates_by_cap['circulation'].append((ex, scores, mean_s))
        elif ttype == 'ACCESSIBILITY_ANALYSIS':
            candidates_by_cap['ergonomie_reglementation'].append((ex, scores, mean_s))
        elif ttype in ('PBR_REASONING', 'MATERIAL_APPLICATION'):
            candidates_by_cap['materiaux'].append((ex, scores, mean_s))
        elif ttype in ('LIGHTING_ANALYSIS', 'DAYLIGHT_REASONING'):
            candidates_by_cap['lumiere'].append((ex, scores, mean_s))
        elif ttype in ('IFC_QA', 'BIM_SPATIAL_HIERARCHY') and 'IFC_BENCH' in src:
            candidates_by_cap['bim_ifc'].append((ex, scores, mean_s))
        elif ttype == 'PROJECT_CRITIQUE':
            candidates_by_cap['critique'].append((ex, scores, mean_s))
        elif ttype == 'GUIDED_REASONING':
            candidates_by_cap['pedagogie'].append((ex, scores, mean_s))
        elif ttype == 'PLAN_PLUS_3D' or (ttype == 'INTERIOR_ANALYSIS' and 'STRUCTSCAN' in src):
            candidates_by_cap['multimodalite'].append((ex, scores, mean_s))
        elif ttype == 'CONSTRAINT_REASONING':
            candidates_by_cap['raisonnement_multicontrainte'].append((ex, scores, mean_s))
        elif ttype == 'DESIGN_HISTORY':
            candidates_by_cap['histoire_design'].append((ex, scores, mean_s))

    print("Candidates per capability:")
    for cap, c_list in sorted(candidates_by_cap.items()):
        print(f"  {cap}: {len(c_list)}")

    # Target: 44 curated Gold Set examples (4 per capability across 11 key capabilities)
    selected_gold = []
    gold_manifest = {
        "gold_set_version": "v1.0.0",
        "description": "Gold Set Indépendant ARCHI-AI Wave 1 - Étalon Qualité pour Audit Approfondi",
        "total_examples": 0,
        "capabilities": {},
        "examples_summary": []
    }

    for cap, c_list in sorted(candidates_by_cap.items()):
        # Sort by mean score descending
        c_list.sort(key=lambda x: -x[2])
        # Pick top 4 distinct items
        seen_rec_ids = set()
        picked = []
        for ex, sc, ms in c_list:
            rec_id = ex['source_ids'][0]
            if rec_id not in seen_rec_ids:
                seen_rec_ids.add(rec_id)
                picked.append((ex, sc, ms))
            if len(picked) == 4:
                break
        gold_manifest["capabilities"][cap] = len(picked)
        for ex, sc, ms in picked:
            selected_gold.append(ex)
            gold_manifest["examples_summary"].append({
                "id": ex['id'],
                "capability": cap,
                "task_type": ex['task_type'],
                "source": ex['source_provenance'].get('source_name'),
                "difficulty": ex['difficulty'],
                "mean_audit_score": round(ms, 2),
                "scores_12_axes": {k: round(v, 2) for k, v in sc.items()}
            })

    gold_manifest["total_examples"] = len(selected_gold)

    # Write gold_set.jsonl
    gold_jsonl_path = os.path.join(GOLD_DIR, 'gold_set.jsonl')
    with open(gold_jsonl_path, 'w', encoding='utf-8') as f:
        for ex in selected_gold:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')

    # Write gold_set_manifest.json
    gold_manifest_path = os.path.join(GOLD_DIR, 'gold_set_manifest.json')
    with open(gold_manifest_path, 'w', encoding='utf-8') as f:
        json.dump(gold_manifest, f, ensure_ascii=False, indent=2)

    print(f"\nCreated Gold Set: {len(selected_gold)} examples.")
    print(f"Written to: {gold_jsonl_path}")
    print(f"Manifest to: {gold_manifest_path}")

if __name__ == '__main__':
    select_gold_set()
