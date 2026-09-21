import sys
import os
import json
sys.path.insert(0, os.path.abspath("."))
from dataset_tools.supervision.task_catalogue import TASK_CATALOGUE, TaskGroup
from dataset_tools.supervision.mapping_matrix import SOURCE_CAPABILITY_TASK_MATRIX

# Map each task to sources
task_sources = {}
for src, info in SOURCE_CAPABILITY_TASK_MATRIX.items():
    for t in info.get("eligible_tasks", []):
        task_sources.setdefault(t, []).append(src)

records = []
for tid, t in sorted(TASK_CATALOGUE.items(), key=lambda x: x[1].number):
    diffs = [d.value.split('_')[0] for d in t.allowed_difficulties]
    sources = task_sources.get(tid, [])
    records.append({
        "number": t.number,
        "task_id": tid,
        "name": t.name,
        "group": t.group.value,
        "description": t.description,
        "skill": t.default_skill.value,
        "learning_type": t.default_learning_type.value,
        "domain": t.default_domain.value,
        "difficulties": f"{diffs[0]}-{diffs[-1]}" if len(diffs) > 1 else diffs[0],
        "sources": sources,
        "requires_deterministic": t.requires_deterministic_verification
    })

print(f"Total: {len(records)} tasks")
for r in records[:15]:
    print(f"[{r['number']:02d}] {r['task_id']} | Group: {r['group']} | Sources: {r['sources']}")
