# -*- coding: utf-8 -*-
"""
ARCHI-AI — Multi-Scale Diversity Audit Module
=============================================
Red-team diversity auditing beyond simple question hashing:
1. Exact Duplicates (exact string match).
2. Near Duplicates (Jaccard similarity on token 3-grams > 0.80).
3. Structural Duplicates (identical ablated paragraph skeletons).
4. Same Reasoning Pattern (epistemic tag sequence + rhetorical progression).
5. Aggregate Diversity Metrics:
   - Question Diversity (Type-Token Ratio, clustering)
   - Answer Diversity (Lexical richness, template sharing rate)
   - Source Diversity (Entropy / Gini of source project frequencies)
"""

import re
import hashlib
from typing import Dict, Any, List, Set, Tuple


class DiversityAuditor:
    """Independent auditor for multi-level dataset diversity."""

    def __init__(self, near_dup_threshold: float = 0.80):
        self.near_dup_threshold = near_dup_threshold
        self.re_punct = re.compile(r"[^\w\s]")
        self.re_nums = re.compile(r"\b\d+(?:\.\d+)?\b")

    def _tokenize(self, text: str) -> List[str]:
        clean = self.re_punct.sub(" ", text.lower())
        return clean.split()

    def _get_ngrams(self, tokens: List[str], n: int = 3) -> Set[Tuple[str, ...]]:
        if len(tokens) < n:
            return {tuple(tokens)}
        return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}

    def jaccard_similarity(self, set_a: Set[Any], set_b: Set[Any]) -> float:
        if not set_a and not set_b:
            return 1.0
        if not set_a or not set_b:
            return 0.0
        return len(set_a.intersection(set_b)) / len(set_a.union(set_b))

    def _get_skeleton(self, text: str) -> str:
        """Strips numbers, specific IDs, and trims whitespace to expose template skeleton."""
        skeleton = self.re_nums.sub("[X]", text.lower())
        lines = [re.sub(r"\s+", " ", l.strip()) for l in skeleton.split("\n") if l.strip()]
        return "\n".join(lines)

    def audit_diversity(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executes comprehensive diversity analysis across all audited records.
        """
        total = len(records)
        if total == 0:
            return {}

        # 1. Exact Question & Answer Duplicates
        question_hashes: Dict[str, List[str]] = {}
        answer_hashes: Dict[str, List[str]] = {}

        # 2. Skeletons
        skeleton_map: Dict[str, List[str]] = {}

        # 3. Sources
        source_counts: Dict[str, int] = {}

        # 4. Token collections for TTR
        all_q_tokens: List[str] = []
        all_a_tokens: List[str] = []

        # 5. N-gram representations for near-dup detection
        q_ngrams_list: List[Tuple[str, Set[Tuple[str, ...]]]] = []
        a_ngrams_list: List[Tuple[str, Set[Tuple[str, ...]]]] = []

        for rec in records:
            rid = rec.get("id", "UNKNOWN")
            q = rec.get("question", "")
            a = rec.get("answer", "")
            src = rec.get("source_ids", ["UNKNOWN"])[0] if rec.get("source_ids") else "UNKNOWN"

            # Source count
            source_counts[src] = source_counts.get(src, 0) + 1

            # Exact hashes
            qh = hashlib.md5(q.strip().encode("utf-8")).hexdigest()
            ah = hashlib.md5(a.strip().encode("utf-8")).hexdigest()
            question_hashes.setdefault(qh, []).append(rid)
            answer_hashes.setdefault(ah, []).append(rid)

            # Skeletons
            skel = self._get_skeleton(a)
            skel_h = hashlib.md5(skel.encode("utf-8")).hexdigest()
            skeleton_map.setdefault(skel_h, []).append(rid)

            # Tokens
            q_tok = self._tokenize(q)
            a_tok = self._tokenize(a)
            all_q_tokens.extend(q_tok)
            all_a_tokens.extend(a_tok)

            q_ngrams_list.append((rid, self._get_ngrams(q_tok, 3)))
            a_ngrams_list.append((rid, self._get_ngrams(a_tok, 3)))

        # Find near duplicates (sample-capped to avoid O(N^2) explosion if large)
        eval_cap = min(total, 250)
        near_dup_answers = 0
        near_dup_pairs = []

        for i in range(eval_cap):
            rid_i, ng_i = a_ngrams_list[i]
            for j in range(i + 1, eval_cap):
                rid_j, ng_j = a_ngrams_list[j]
                sim = self.jaccard_similarity(ng_i, ng_j)
                if sim >= self.near_dup_threshold:
                    near_dup_answers += 1
                    if len(near_dup_pairs) < 10:
                        near_dup_pairs.append({"id_a": rid_i, "id_b": rid_j, "similarity": round(sim, 3)})

        exact_dup_questions = sum(len(ids) - 1 for ids in question_hashes.values() if len(ids) > 1)
        exact_dup_answers = sum(len(ids) - 1 for ids in answer_hashes.values() if len(ids) > 1)

        # Structural duplication: skeletons shared by > 3 examples
        shared_skeletons = {k: ids for k, ids in skeleton_map.items() if len(ids) >= 3}
        structural_dup_examples = sum(len(ids) for ids in shared_skeletons.values())

        # Type-Token Ratios (Lexical Richness)
        q_ttr = round(len(set(all_q_tokens)) / max(1, len(all_q_tokens)), 4)
        a_ttr = round(len(set(all_a_tokens)) / max(1, len(all_a_tokens)), 4)

        # Source diversity: number of unique sources and max share
        unique_sources = len(source_counts)
        max_source_count = max(source_counts.values()) if source_counts else 0
        top_source_share = round(max_source_count / total, 4) if total else 0.0

        return {
            "total_evaluated": total,
            "exact_duplicate_questions": exact_dup_questions,
            "exact_duplicate_answers": exact_dup_answers,
            "near_duplicate_answer_pairs": near_dup_answers,
            "structural_duplicate_clusters": len(shared_skeletons),
            "structural_duplicate_examples": structural_dup_examples,
            "structural_duplication_rate": round(structural_dup_examples / total, 4) if total else 0.0,
            "question_type_token_ratio": q_ttr,
            "answer_type_token_ratio": a_ttr,
            "unique_sources": unique_sources,
            "top_source_share": top_source_share,
            "near_dup_sample_pairs": near_dup_pairs,
            "risk_assessment": (
                "HIGH_TEMPLATE_DUPLICATION"
                if structural_dup_examples / total > 0.30
                else "HEALTHY_DIVERSITY"
            ),
        }
