# -*- coding: utf-8 -*-
import json
from collections import Counter

dataset_path = 'ARCHI_AI/dataset/master/v1/supervision/wave1/wave1_dataset.jsonl'
with open(dataset_path, 'r', encoding='utf-8') as f:
    examples = [json.loads(line) for line in f]

warnings = [ex for ex in examples if ex['quality_status'] == 'WARNING']
print(f"Total warnings: {len(warnings)}")
src_counter = Counter(ex['source_provenance']['dataset'] for ex in warnings)
print("Sources of warnings:", src_counter)

task_counter = Counter(ex['task_type'] for ex in warnings)
print("Tasks of warnings:", task_counter)

split_counter = Counter(ex['split'] for ex in warnings)
print("Splits of warnings:", split_counter)

dest_counter = Counter(ex['destination'] for ex in warnings)
print("Destinations of warnings:", dest_counter)
