# -*- coding: utf-8 -*-
"""
Detailed Analysis of Anomalies, False Passes, and Quality across Wave 1.
"""
import json
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

DATASET_PATH = 'ARCHI_AI/dataset/master/v1/supervision/wave1/wave1_dataset.jsonl'

def run_deep_checks():
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        examples = [json.loads(line) for line in f]

    print(f"Total examples: {len(examples)}")

    # 1. Check for "None" or formatting bugs in answers/questions
    none_in_answers = [e for e in examples if 'None' in e['answer']]
    print(f"\n1. Examples with 'None' in answer: {len(none_in_answers)}")
    for e in none_in_answers[:5]:
        print(f"  ID: {e['id']} | Task: {e['task_type']} | Match: {[m.start() for m in re.finditer(r'None', e['answer'])]}")
        # print snippet around 'None'
        for m in re.finditer(r'None', e['answer']):
            start = max(0, m.start() - 30)
            end = min(len(e['answer']), m.end() + 30)
            print(f"    Snippet: ...{e['answer'][start:end]}...")

    # 2. Check modal inputs per task / group
    print("\n2. Modal Inputs inspection:")
    empty_inputs = []
    modal_stats = defaultdict(lambda: defaultdict(int))
    for e in examples:
        has_any_input = any(bool(v) for k, v in e['inputs'].items())
        if not has_any_input:
            empty_inputs.append(e)
        for k, v in e['inputs'].items():
            if v:
                modal_stats[e['task_group']][k] += 1
    print(f"  Total examples with completely EMPTY inputs: {len(empty_inputs)}")
    for g, counts in sorted(modal_stats.items()):
        print(f"  Group {g}: {dict(counts)}")

    # 3. Multimodal Audit (Group L & Others)
    print("\n3. Multimodal Audit:")
    group_l = [e for e in examples if e['task_group'] == 'L_MULTIMODAL']
    print(f"  Group L total: {len(group_l)}")
    for e in group_l[:10]:
        input_keys = [k for k, v in e['inputs'].items() if v]
        print(f"  ID: {e['id']} | Task: {e['task_type']} | Inputs: {input_keys} | Source: {e['source_provenance'].get('source_name')}")

    # 4. Check for MMMU benchmark examples
    mmmu_ex = [e for e in examples if 'MMMU' in e['source_provenance'].get('source_name', '')]
    print(f"\n4. MMMU examples: {len(mmmu_ex)}")
    for e in mmmu_ex[:3]:
        print(f"  ID: {e['id']}")
        print(f"  Q: {e['question'][:150]}")
        print(f"  A: {e['answer'][:150]}")
        print(f"  Ground Truth: {e['ground_truth']}")
        print(f"  Evidence: {e['evidence']}")
        print(f"  Inputs: {[k for k, v in e['inputs'].items() if v]}")

    # 5. Generic Responses & Template Formulas
    print("\n5. Generic / Template Analysis:")
    # Check repeated sentences or phrases across answers
    first_lines = Counter(e['answer'].split('\n')[0].strip() for e in examples)
    print("  Top 10 answer starting lines:")
    for line, c in first_lines.most_common(10):
        print(f"    ({c}x) {line[:80]}")

    # Check for identical / near-identical answer templates
    # Replace variable names/numbers and check hash
    templates = Counter()
    for e in examples:
        ans = e['answer']
        # normalize out numbers and quotes
        norm = re.sub(r'\b\d+(\.\d+)?\b', '<NUM>', ans)
        norm = re.sub(r"'[^']*'", '<STR>', norm)
        norm = re.sub(r'"[^"]*"', '<STR>', norm)
        templates[norm[:100]] += 1
    print("\n  Top 10 normalized answer prefixes:")
    for templ, c in templates.most_common(10):
        print(f"    ({c}x) {templ.strip()}")

    # 6. Check Ergonomics values & conversions
    print("\n6. Ergonomics Ground Truth & Values:")
    ergo_ex = [e for e in examples if e['task_group'] == 'E_ERGONOMICS']
    for e in ergo_ex[:5]:
        print(f"  ID: {e['id']} | Task: {e['task_type']}")
        print(f"  GT: {e['ground_truth']}")
        print(f"  Evidence: {e['evidence']}")
        print(f"  Answer: {e['answer'][:150]}")

    # 7. Check Floorplan (ResPlan vs RPLAN vs ResBIM)
    print("\n7. Floorplan Ground Truth & Sources:")
    fp_ex = [e for e in examples if e['task_group'] == 'B_FLOORPLAN']
    fp_by_src = Counter(e['source_provenance'].get('source_name') for e in fp_ex)
    print(f"  Sources in Floorplan: {dict(fp_by_src)}")
    for e in fp_ex[:3]:
        print(f"  ID: {e['id']} | Task: {e['task_type']} | Source: {e['source_provenance'].get('source_name')}")
        print(f"  GT: {e['ground_truth']}")
        print(f"  Inputs: {[k for k, v in e['inputs'].items() if v]}")

    # 8. Check 3D (IL3D)
    print("\n8. 3D / Spatial Ground Truth:")
    spatial_ex = [e for e in examples if e['task_group'] == 'C_SPATIAL_3D']
    for e in spatial_ex[:3]:
        print(f"  ID: {e['id']} | Task: {e['task_type']}")
        print(f"  GT: {e['ground_truth']}")
        print(f"  Evidence: {e['evidence']}")
        print(f"  Answer: {e['answer'][:150]}")

    # 9. Check BIM / IFC
    print("\n9. BIM / IFC Ground Truth:")
    bim_ex = [e for e in examples if e['task_group'] == 'D_BIM_IFC']
    for e in bim_ex[:3]:
        print(f"  ID: {e['id']} | Task: {e['task_type']}")
        print(f"  GT: {e['ground_truth']}")
        print(f"  Answer: {e['answer'][:150]}")

    # 10. Check Design & History
    print("\n10. Design & History Ground Truth:")
    design_ex = [e for e in examples if e['task_group'] == 'H_DESIGN']
    for e in design_ex[:3]:
        print(f"  ID: {e['id']} | Task: {e['task_type']}")
        print(f"  GT: {e['ground_truth']}")
        print(f"  Answer: {e['answer'][:150]}")

    # 11. Check Critique & Pedagogy
    print("\n11. Critique & Pedagogy Answers:")
    crit_ex = [e for e in examples if e['task_group'] in ('I_CRITIQUE', 'K_PEDAGOGY', 'J_PROFESSIONAL_REASONING')]
    for e in crit_ex[:4]:
        print(f"  ID: {e['id']} | Group: {e['task_group']} | Task: {e['task_type']} | Diff: {e['difficulty']}")
        print(f"  Q: {e['question']}")
        print(f"  A: {e['answer']}")
        print(f"  GT: {e['ground_truth']}")
        print(f"  Inputs: {[k for k, v in e['inputs'].items() if v]}")
        print("-" * 40)

if __name__ == '__main__':
    run_deep_checks()
