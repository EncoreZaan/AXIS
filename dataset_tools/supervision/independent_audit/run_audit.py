# -*- coding: utf-8 -*-
"""
ARCHI-AI — Run Independent Audit Script
=======================================
Command-line entrypoint to execute the independent pre-training audit.
"""

import os
import sys
import json
from pathlib import Path

# Ensure ARCHI_AI root is on python path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from dataset_tools.supervision.independent_audit.independent_auditor import IndependentAuditor


def main():
    print("=" * 70)
    print("ARCHI-AI — INDEPENDENT RED TEAM GOLD AUDIT & PRE-TRAINING GATE")
    print("=" * 70)
    print(f"Base Directory: {BASE_DIR}")

    auditor = IndependentAuditor(base_dir=BASE_DIR)
    summary = auditor.run_full_audit()

    print("\n" + "=" * 70)
    print("AUDIT SUMMARY RESULTS")
    print("=" * 70)
    m = summary["metrics"]
    st = summary["sampling"]["strata_stats"]
    g2 = summary["gold_v2_eval"]
    h = summary["holdout_stats"]
    gate = summary["gate_decision"]

    print(f"1. Total Audited Examples: {summary['total_audited_records']}")
    print(f"   - Wave 1 Repaired Sampled: {st['total_wave1_sampled']} ({st['wave1_sample_percentage']}%)")
    print(f"   - Gold Set V2 Audited: {st['gold_v2_sampled']} / {st['total_gold_v2']} (100%)")
    print(f"   - Warnings Audited: {st['wave1_warnings_sampled']} / {st['wave1_warnings_count']} (100%)")
    print(f"   - Review Queue Audited: {st['review_queue_sampled']} / {st['total_review_queue']} (100%)")
    print(f"   - L6 Audited: {st['wave1_l6_sampled']} / {st['wave1_l6_count']} (100%)")
    print(f"2. Independent Grounding Ratio: {m['grounding_ratio_pct']}%")
    print(f"3. Specific Answers Rate: {m['specific_answers_pct']}%")
    print(f"4. Fake Multimodal Rate: {m['fake_multimodal_pct']}%")
    print(f"5. Structural Duplication Rate: {m['structural_dup_pct']}%")
    print(f"6. L6 Authenticity Rate: {m['l6_authenticity_pct']}%")
    print(f"7. OBJECT_RELATION Conformity: {m['object_relation_pass_pct']}%")
    print(f"8. Floorplan Pixel Area Anomalies: {m['floorplan_pixel_area_pct']}%")
    print(f"9. BIM/IFC Payload Conformity: {m['ifc_payload_valid_pct']}%")
    print(f"10. Critique Structure Conformity: {m['critique_structure_pass_pct']}%")
    print(f"11. Gold Set V2 Classification: GOLD={g2['gold_count']} ({g2['gold_pct']}%), SILVER={g2['silver_count']}, BRONZE={g2['bronze_count']}, REJECT={g2['reject_count']}")
    print(f"12. Gold Set V2 Contamination with Train: {g2['contamination_count']} ({g2['contamination_pct']}%)")
    print(f"13. True Isolated Holdout Created: {h['total_holdout_examples']} examples in {h['holdout_path']}")
    print(f"14. Harmful Data Instances Detected: {summary['harm_stats']['total_harmful_count']}")
    print(f"15. Pre-Training Gate Decision: {gate['status']}")
    print(f"    Confidence: {gate['confidence_level']}")
    print(f"    Training Authorization: {gate['training_authorization']}")
    print("=" * 70)

    # Save summary json
    summary_path = BASE_DIR / "INDEPENDENT_AUDIT_SUMMARY.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        # Avoid non-serializable objects
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"Saved complete audit summary to {summary_path}")


if __name__ == "__main__":
    main()
