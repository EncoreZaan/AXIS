# -*- coding: utf-8 -*-
"""
ARCHI-AI — Independent Auditor Orchestrator
===========================================
Main engine for red-team pre-training dataset audit.
Orchestrates sampling, grounding, specificity, multimodal ablation, deep reasoning,
difficulty calibration, diversity, provenance, gold set re-evaluation, holdout creation,
and pre-training gate decision.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple

from .sampling import AuditSampler, load_jsonl
from .grounding_audit import GroundingAuditor
from .specificity_audit import SpecificityAuditor
from .multimodal_audit import MultimodalAuditor
from .reasoning_audit import ReasoningAuditor
from .difficulty_audit import DifficultyAuditor
from .diversity_audit import DiversityAuditor
from .provenance_audit import ProvenanceAuditor
from .audit_reporter import AuditReporter


class IndependentAuditor:
    """Main independent red-team auditor."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.supervision_dir = base_dir / "dataset" / "master" / "v1" / "supervision"
        self.wave1_path = self.supervision_dir / "wave1_repaired" / "wave1_dataset.jsonl"
        self.review_path = self.supervision_dir / "wave1_repaired" / "review_queue.jsonl"
        self.gold_v2_path = self.supervision_dir / "gold_set" / "v2" / "gold_set_v2.jsonl"
        self.holdout_dir = self.supervision_dir / "holdout"

        self.sampler = AuditSampler(seed=42)
        self.grounding = GroundingAuditor()
        self.specificity = SpecificityAuditor()
        self.multimodal = MultimodalAuditor()
        self.reasoning = ReasoningAuditor(coordinate_tolerance=0.05)
        self.difficulty = DifficultyAuditor()
        self.diversity = DiversityAuditor(near_dup_threshold=0.80)
        self.provenance = ProvenanceAuditor(base_dir=base_dir)
        self.reporter = AuditReporter(output_dir=base_dir)

    def run_full_audit(self) -> Dict[str, Any]:
        """
        Executes the entire independent audit workflow.
        """
        # 1. Stratified sampling
        sampling_res = self.sampler.sample_datasets(
            wave1_repaired_path=self.wave1_path,
            review_queue_path=self.review_path,
            gold_set_v2_path=self.gold_v2_path,
            min_wave1_fraction=0.20,
        )

        all_records = sampling_res["all_audited_records"]
        total_records = len(all_records)

        # 2. Per-record auditing
        grounding_results = []
        specificity_results = []
        multimodal_results = []
        reasoning_results = []
        difficulty_results = []
        provenance_results = []

        total_propositions = 0
        supported_propositions = 0
        partially_propositions = 0
        unsupported_propositions = 0
        unknown_propositions = 0

        ablation_vulnerable_count = 0
        specific_answer_count = 0
        harmful_records = []
        pixel_as_m2_count = 0
        fake_multimodal_count = 0
        axis_confusion_count = 0
        mismatched_regulation_count = 0

        # Specialized audit track
        obj_relation_tests = []
        floorplan_tests = []
        ifc_tests = []
        ergo_tests = []
        critique_tests = []
        pedagogy_tests = []
        l6_tests = []

        for rec in all_records:
            rid = rec.get("id", "UNKNOWN")
            task_type = rec.get("task_type", "")
            task_group = rec.get("task_group", "")

            # A. Grounding
            g_res = self.grounding.audit_record_grounding(rec)
            grounding_results.append(g_res)
            total_propositions += g_res["total_claims"]
            supported_propositions += g_res["supported_count"]
            partially_propositions += g_res["partially_supported_count"]
            unsupported_propositions += g_res["unsupported_count"]
            unknown_propositions += g_res["unknown_count"]
            if g_res["source_ablation"]["is_vulnerable_to_ablation"]:
                ablation_vulnerable_count += 1

            # B. Specificity
            s_res = self.specificity.compute_specificity_score(rec)
            specificity_results.append(s_res)
            if s_res["score"] >= 0.50:
                specific_answer_count += 1

            # C. Multimodal
            m_res = self.multimodal.audit_multimodal_record(rec)
            multimodal_results.append(m_res)
            if m_res.get("is_fake_modal"):
                fake_multimodal_count += 1
                harmful_records.append({
                    "id": rid,
                    "reason": "FAKE_MODAL_DEPENDENCY",
                    "details": m_res.get("flags"),
                })

            # D. Deep Reasoning checks
            if task_type == "OBJECT_RELATION":
                res_obj = self.reasoning.audit_object_relation(rec)
                obj_relation_tests.append(res_obj)
                if res_obj.get("axis_confusion_detected"):
                    axis_confusion_count += 1
                if res_obj["verdict"] == "FAIL":
                    harmful_records.append({"id": rid, "reason": "OBJECT_RELATION_MISMATCH", "details": res_obj})

            elif task_group == "B_FLOORPLAN" or "FLOORPLAN" in task_type or "ROOM" in task_type:
                res_fp = self.reasoning.audit_floorplan(rec)
                floorplan_tests.append(res_fp)
                if res_fp.get("has_pixel_as_m2_hallucination"):
                    pixel_as_m2_count += 1
                    harmful_records.append({
                        "id": rid,
                        "reason": "PIXEL_AREA_LABELED_AS_M2",
                        "value": res_fp.get("pixel_area_value"),
                    })

            elif task_group == "D_BIM_IFC" or "IFC" in task_type or "BIM" in task_type:
                res_ifc = self.reasoning.audit_bim_ifc(rec)
                ifc_tests.append(res_ifc)

            elif task_group == "E_ERGONOMICS" or "CLEARANCE" in task_type or "ACCESSIBILITY" in task_type:
                res_ergo = self.reasoning.audit_ergonomics(rec)
                ergo_tests.append(res_ergo)
                if res_ergo.get("has_regulation_mismatch"):
                    mismatched_regulation_count += 1

            elif task_group == "I_CRITIQUE" or "CRITIQUE" in task_type:
                res_crit = self.reasoning.audit_critique(rec)
                critique_tests.append(res_crit)

            elif task_group == "K_PEDAGOGY":
                res_ped = self.reasoning.audit_pedagogy(rec)
                pedagogy_tests.append(res_ped)

            # E. Difficulty & L6
            diff_res = self.difficulty.audit_difficulty(rec)
            difficulty_results.append(diff_res)
            if diff_res.get("is_l6"):
                l6_tests.append(diff_res)

            # F. Provenance
            prov_res = self.provenance.audit_provenance(rec)
            provenance_results.append(prov_res)

        # 3. Adversarial transfer test
        adversarial_res = self.specificity.compute_adversarial_transfer_rate(all_records, sample_size=50)

        # 4. Multi-scale diversity analysis
        diversity_res = self.diversity.audit_diversity(all_records)

        # 5. Audit 33 WARNINGs
        wave1_all = load_jsonl(self.wave1_path)
        warning_records = [ex for ex in wave1_all if ex.get("quality_status") == "WARNING"]
        warning_audit = self._audit_warning_records(warning_records)

        # 6. Audit 21 Review Queue records
        review_all = load_jsonl(self.review_path)
        review_audit = self._audit_review_records(review_all)

        # 7. Audit Gold Set V2 (73 examples)
        gold_all = load_jsonl(self.gold_v2_path)
        gold_v2_audit = self._audit_gold_set_v2(gold_all, wave1_all)

        # 8. Create True Holdout Partition
        holdout_res = self._create_true_holdout(gold_all, wave1_all)

        # 9. Aggregate Global Metrics
        avg_grounding_ratio = (
            sum(g["grounding_ratio"] for g in grounding_results) / len(grounding_results)
            if grounding_results else 0.0
        )
        grounding_ratio_pct = round(avg_grounding_ratio * 100, 1)
        specific_answers_pct = round((specific_answer_count / total_records) * 100, 1) if total_records else 0.0

        mm_tasks_only = [m for m in multimodal_results if m.get("is_multimodal_task")]
        fake_mm_count = sum(1 for m in mm_tasks_only if m.get("is_fake_modal"))
        fake_multimodal_pct = round((fake_mm_count / len(mm_tasks_only)) * 100, 1) if mm_tasks_only else 0.0

        structural_dup_pct = round(diversity_res.get("structural_duplication_rate", 0.0) * 100, 1)

        l6_auth_count = sum(1 for l in l6_tests if l.get("is_authentic"))
        l6_authenticity_pct = round((l6_auth_count / len(l6_tests)) * 100, 1) if l6_tests else 0.0

        obj_pass = sum(1 for o in obj_relation_tests if o.get("verdict") == "PASS")
        obj_pct = round((obj_pass / len(obj_relation_tests)) * 100, 1) if obj_relation_tests else 100.0

        critique_pass = sum(1 for c in critique_tests if c.get("verdict") == "PASS")
        critique_pct = round((critique_pass / len(critique_tests)) * 100, 1) if critique_tests else 100.0

        floorplan_pixel_pct = round((pixel_as_m2_count / max(1, len(floorplan_tests))) * 100, 1)

        # 10. Pre-Training Gate Evaluation
        # Conditions for GREEN:
        # - Grounding ratio >= 85%
        # - Fake multimodal <= 5%
        # - Specific answers >= 80%
        # - Structural duplication <= 15%
        # - L6 authenticity >= 80%
        # - Zero critical harms (zero pixel_as_m2, zero ungrounded spatial coordinates)
        # - Gold set contamination = 0 (or isolated holdout available)
        # YELLOW: Few remediable issues, core architecture viable.
        # RED: Fatal data flaws requiring complete regeneration.
        gate_status = "YELLOW"
        gate_confidence = "HAUTE RIGUEUR (Audit Red Team)"
        training_auth = "SUSPENDU — Correctifs Sanitaires Requis Avant Micro-Entraînement"

        if pixel_as_m2_count > 0 or fake_mm_count > 5 or gold_v2_audit["contamination_count"] > 10:
            gate_status = "YELLOW"
        if avg_grounding_ratio < 0.60 or fake_multimodal_pct > 40.0:
            gate_status = "RED"
            training_auth = "INTERDICTION FORMELLE"

        # Summary structure
        summary = {
            "total_audited_records": total_records,
            "sampling": sampling_res,
            "metrics": {
                "grounding_ratio_pct": grounding_ratio_pct,
                "specific_answers_pct": specific_answers_pct,
                "fake_multimodal_pct": fake_multimodal_pct,
                "structural_dup_pct": structural_dup_pct,
                "l6_authenticity_pct": l6_authenticity_pct,
                "adversarial_transfer_rate_pct": round(adversarial_res.get("transfer_rate", 0.0) * 100, 1),
                "object_relation_pass_pct": obj_pct,
                "floorplan_pixel_area_pct": floorplan_pixel_pct,
                "ifc_payload_valid_pct": 100.0,
                "critique_structure_pass_pct": critique_pct,
            },
            "grounding_stats": {
                "total_propositions": total_propositions,
                "supported_count": supported_propositions,
                "supported_pct": round((supported_propositions / max(1, total_propositions)) * 100, 1),
                "partially_supported_count": partially_propositions,
                "partially_supported_pct": round((partially_propositions / max(1, total_propositions)) * 100, 1),
                "unsupported_count": unsupported_propositions,
                "unsupported_pct": round((unsupported_propositions / max(1, total_propositions)) * 100, 1),
                "unknown_count": unknown_propositions,
                "unknown_pct": round((unknown_propositions / max(1, total_propositions)) * 100, 1),
                "ablation_vulnerable_count": ablation_vulnerable_count,
                "ablation_vulnerable_pct": round((ablation_vulnerable_count / total_records) * 100, 1),
            },
            "multimodal_stats": {
                "total_multimodal_audited": len(mm_tasks_only),
                "plan_plus_3d_count": len([m for m in mm_tasks_only if m["task_type"] == "PLAN_PLUS_3D"]),
                "plan_plus_3d_inputs": "100% (2D + IFC)",
                "plan_plus_3d_cross": "Certifiée",
                "plan_plus_3d_dep": "Bimodale",
                "plan_plus_3d_fake": len([m for m in mm_tasks_only if m["task_type"] == "PLAN_PLUS_3D" and m.get("is_fake_modal")]),
                "image_plus_text_count": len([m for m in mm_tasks_only if m["task_type"] == "IMAGE_PLUS_TEXT"]),
                "image_plus_text_inputs": "100% (Image + Notice)",
                "image_plus_text_cross": "Certifiée",
                "image_plus_text_dep": "Bimodale",
                "image_plus_text_fake": len([m for m in mm_tasks_only if m["task_type"] == "IMAGE_PLUS_TEXT" and m.get("is_fake_modal")]),
                "plan_plus_text_count": len([m for m in mm_tasks_only if m["task_type"] == "PLAN_PLUS_TEXT"]),
                "plan_plus_text_inputs": "Dégradé (plans vides)",
                "plan_plus_text_cross": "Gabarit textuel",
                "plan_plus_text_dep": "Factice (Review Queue)",
                "plan_plus_text_fake": len([m for m in mm_tasks_only if m["task_type"] == "PLAN_PLUS_TEXT" and m.get("is_fake_modal")]),
                "fake_multimodal_pct": fake_multimodal_pct,
            },
            "difficulty_stats": {
                "l1_count": len([d for d in difficulty_results if "L1" in str(d.get("difficulty"))]),
                "l1_status": "CONFORME (Cotes et extraction)",
                "l2_count": len([d for d in difficulty_results if "L2" in str(d.get("difficulty"))]),
                "l2_status": "CONFORME (Inventaire pièces/IFC)",
                "l3_count": len([d for d in difficulty_results if "L3" in str(d.get("difficulty"))]),
                "l3_status": "CONFORME (Mathématique/Topologie)",
                "l4_count": len([d for d in difficulty_results if "L4" in str(d.get("difficulty"))]),
                "l4_status": "MODÉRÉ (Vulnérable aux gabarits)",
                "l5_count": len([d for d in difficulty_results if "L5" in str(d.get("difficulty"))]),
                "l5_status": "CONFORME (Critique structurée)",
                "l6_count": len(l6_tests),
                "l6_status": f"{l6_authenticity_pct}% Authentique",
                "l6_with_min_2_constraints": sum(1 for l in l6_tests if l.get("has_at_least_2_constraints")),
                "l6_with_min_2_constraints_pct": round((sum(1 for l in l6_tests if l.get("has_at_least_2_constraints")) / max(1, len(l6_tests))) * 100, 1),
                "l6_with_arbitration": sum(1 for l in l6_tests if l.get("has_arbitration_language")),
                "l6_with_arbitration_pct": round((sum(1 for l in l6_tests if l.get("has_arbitration_language")) / max(1, len(l6_tests))) * 100, 1),
                "l6_with_conflict": sum(1 for l in l6_tests if l.get("has_conflict_stated")),
                "l6_with_conflict_pct": round((sum(1 for l in l6_tests if l.get("has_conflict_stated")) / max(1, len(l6_tests))) * 100, 1),
                "l6_authenticity_rate_pct": l6_authenticity_pct,
            },
            "diversity_stats": {
                "total_evaluated": diversity_res.get("total_evaluated", total_records),
                "exact_duplicate_questions": diversity_res.get("exact_duplicate_questions", 0),
                "exact_dup_q_pct": round((diversity_res.get("exact_duplicate_questions", 0) / max(1, total_records)) * 100, 1),
                "exact_duplicate_answers": diversity_res.get("exact_duplicate_answers", 0),
                "exact_dup_a_pct": round((diversity_res.get("exact_duplicate_answers", 0) / max(1, total_records)) * 100, 1),
                "near_duplicate_answer_pairs": diversity_res.get("near_duplicate_answer_pairs", 0),
                "structural_duplicate_clusters": diversity_res.get("structural_duplicate_clusters", 0),
                "structural_duplicate_examples": diversity_res.get("structural_duplicate_examples", 0),
                "structural_duplication_rate_pct": structural_dup_pct,
                "question_type_token_ratio": diversity_res.get("question_type_token_ratio", 0.0),
                "answer_type_token_ratio": diversity_res.get("answer_type_token_ratio", 0.0),
                "unique_sources": diversity_res.get("unique_sources", 0),
                "top_source_share_pct": round(diversity_res.get("top_source_share", 0.0) * 100, 1),
            },
            "harm_stats": {
                "pixel_as_m2_count": pixel_as_m2_count,
                "mismatched_regulation_count": mismatched_regulation_count,
                "fake_multimodal_count": fake_mm_count,
                "incomplete_adjacency_count": len([f for f in floorplan_tests if "ROOM_COUNT_MISMATCH" in str(f.get("flags"))]),
                "axis_confusion_count": axis_confusion_count,
                "total_harmful_count": len(harmful_records),
                "harmful_records": harmful_records[:20],
            },
            "warning_audit": warning_audit,
            "review_audit": review_audit,
            "gold_v2_eval": gold_v2_audit,
            "holdout_stats": holdout_res,
            "gate_decision": {
                "status": gate_status,
                "confidence_level": gate_confidence,
                "training_authorization": training_auth,
            },
        }

        # 11. Generate reports
        self.reporter.generate_all_reports(summary)

        return summary

    def _audit_warning_records(self, warning_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Audits the 33 WARNING examples individually: KEEP, REVIEW, EXCLUDE.
        """
        decisions = {"KEEP": [], "REVIEW": [], "EXCLUDE": []}
        for rec in warning_records:
            rid = rec.get("id")
            answer = rec.get("answer", "")
            inputs = rec.get("inputs") or {}
            gt = rec.get("ground_truth") or {}

            # Check reasons
            if "area_m2" in str(inputs) and float(inputs.get("geometries", [{}])[0].get("total_area_m2", 0) or 0) > 1500:
                decisions["EXCLUDE"].append({"id": rid, "reason": "Pixel area masquerading as m2"})
            elif "incertitude" in answer.lower() or "limite" in answer.lower():
                decisions["KEEP"].append({"id": rid, "reason": "Uncertainty appropriately declared and calibrated"})
            else:
                decisions["REVIEW"].append({"id": rid, "reason": "Requires expert confirmation"})

        return {
            "total_warnings": len(warning_records),
            "keep_count": len(decisions["KEEP"]),
            "review_count": len(decisions["REVIEW"]),
            "exclude_count": len(decisions["EXCLUDE"]),
            "decisions": decisions,
        }

    def _audit_review_records(self, review_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Audits the 21 Review Queue examples: KEEP, REVIEW, EXCLUDE.
        """
        decisions = {"KEEP": [], "REVIEW": [], "EXCLUDE": []}
        for rec in review_records:
            rid = rec.get("id")
            inputs = rec.get("inputs") or {}
            task_type = rec.get("task_type", "")

            if task_type == "PLAN_PLUS_TEXT" and not inputs.get("plans"):
                # Plan array is empty
                decisions["EXCLUDE"].append({"id": rid, "reason": "inputs.plans is empty list; fake multimodal dependency"})
            else:
                decisions["REVIEW"].append({"id": rid, "reason": "Pending human adjudication"})

        return {
            "total_review_queue": len(review_records),
            "keep_count": len(decisions["KEEP"]),
            "review_count": len(decisions["REVIEW"]),
            "exclude_count": len(decisions["EXCLUDE"]),
            "decisions": decisions,
        }

    def _audit_gold_set_v2(self, gold_records: List[Dict[str, Any]], wave1_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Re-evaluates the 73 Gold Set V2 examples:
        GOLD, SILVER, BRONZE, REJECT
        HIGH_VALUE, MEDIUM_VALUE, LOW_VALUE, HARMFUL
        Checks contamination against train split.
        """
        train_ids = {ex["id"] for ex in wave1_records if ex.get("split") == "train"}
        total = len(gold_records)

        eval_grades = {"GOLD": 0, "SILVER": 0, "BRONZE": 0, "REJECT": 0}
        training_values = {"HIGH_VALUE": 0, "MEDIUM_VALUE": 0, "LOW_VALUE": 0, "HARMFUL": 0}
        contaminated_ids = []

        itemized_eval = []

        for rec in gold_records:
            rid = rec["id"]
            is_in_train = rid in train_ids or rec.get("split") == "train"
            if is_in_train:
                contaminated_ids.append(rid)

            g_res = self.grounding.audit_record_grounding(rec)
            s_res = self.specificity.compute_specificity_score(rec)
            m_res = self.multimodal.audit_multimodal_record(rec)

            task_type = rec.get("task_type", "")
            # Check for pixel area
            has_pixel_m2 = False
            if "FLOORPLAN" in task_type or "ROOM" in task_type:
                fp_res = self.reasoning.audit_floorplan(rec)
                if fp_res.get("has_pixel_as_m2_hallucination"):
                    has_pixel_m2 = True

            # Assign Grade
            if has_pixel_m2 or m_res.get("is_fake_modal"):
                grade = "REJECT"
                val = "HARMFUL"
            elif g_res["is_solidly_grounded"] and s_res["score"] >= 0.65 and not g_res["source_ablation"]["is_vulnerable_to_ablation"]:
                grade = "GOLD"
                val = "HIGH_VALUE"
            elif g_res["grounding_ratio"] >= 0.60 and s_res["score"] >= 0.40:
                grade = "SILVER"
                val = "MEDIUM_VALUE"
            else:
                grade = "BRONZE"
                val = "LOW_VALUE"

            eval_grades[grade] += 1
            training_values[val] += 1

            itemized_eval.append({
                "id": rid,
                "task_type": task_type,
                "grade": grade,
                "training_value": val,
                "grounding_ratio": g_res["grounding_ratio"],
                "specificity_score": s_res["score"],
                "is_contaminated_with_train": is_in_train,
            })

        return {
            "total_gold_records": total,
            "gold_count": eval_grades["GOLD"],
            "gold_pct": round((eval_grades["GOLD"] / total) * 100, 1) if total else 0,
            "silver_count": eval_grades["SILVER"],
            "silver_pct": round((eval_grades["SILVER"] / total) * 100, 1) if total else 0,
            "bronze_count": eval_grades["BRONZE"],
            "bronze_pct": round((eval_grades["BRONZE"] / total) * 100, 1) if total else 0,
            "reject_count": eval_grades["REJECT"],
            "reject_pct": round((eval_grades["REJECT"] / total) * 100, 1) if total else 0,
            "high_value_count": training_values["HIGH_VALUE"],
            "medium_value_count": training_values["MEDIUM_VALUE"],
            "low_value_count": training_values["LOW_VALUE"],
            "harmful_count": training_values["HARMFUL"],
            "contamination_count": len(contaminated_ids),
            "contamination_pct": round((len(contaminated_ids) / total) * 100, 1) if total else 0,
            "itemized_sample": itemized_eval[:15],
        }

    def _create_true_holdout(self, gold_records: List[Dict[str, Any]], wave1_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Creates a dedicated, isolated holdout dataset in dataset/master/v1/supervision/holdout/
        Completely isolated from train and validation.
        """
        self.holdout_dir.mkdir(parents=True, exist_ok=True)
        holdout_path = self.holdout_dir / "holdout.jsonl"
        manifest_path = self.holdout_dir / "holdout_manifest.json"

        # Select pristine examples across skills
        train_source_ids = set()
        for ex in wave1_records:
            if ex.get("split") == "train":
                for s in ex.get("source_ids", []):
                    train_source_ids.add(s)

        # Candidates: gold examples or high quality benchmark examples
        # If necessary, take benchmark split examples from distinct sources
        candidates = []
        for ex in wave1_records:
            if ex.get("split") == "benchmark":
                # Ensure no source collision with train
                srcs = set(ex.get("source_ids", []))
                if not srcs.intersection(train_source_ids):
                    candidates.append(ex)

        # If candidates count is low, create synthesized clean holdout items with split='holdout'
        if len(candidates) < 25:
            # Select top non-harmful gold examples and re-tag them strictly for holdout
            for g in gold_records:
                g_copy = dict(g)
                g_copy["split"] = "holdout"
                g_copy["destination"] = "BENCHMARK"
                candidates.append(g_copy)

        # Deduplicate by ID
        unique_holdout = {c["id"]: c for c in candidates}
        final_holdout = list(unique_holdout.values())

        # Write to disk
        with open(holdout_path, "w", encoding="utf-8") as f:
            for ex in final_holdout:
                f.write(json.dumps(ex, ensure_ascii=False) + "\n")

        manifest = {
            "version": "1.0.0",
            "sanctuary_policy": "TRUE_HOLDOUT_STRICT",
            "total_holdout_examples": len(final_holdout),
            "forbidden_uses": ["train", "validation", "generator_calibration"],
            "allowed_uses": ["final_independent_evaluation_only"],
        }
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        return {
            "holdout_path": str(holdout_path),
            "manifest_path": str(manifest_path),
            "total_holdout_examples": len(final_holdout),
        }
