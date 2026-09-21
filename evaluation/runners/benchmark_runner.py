#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Runner de Benchmark et pont d'évaluation
==================================================
Permet d'évaluer les sorties modèles (y compris la baseline historique)
sur les 13 axes d'architecture.
Ne requiert pas de GPU pour l'agrégation et le scoring des inférences existantes.
Conserve la baseline comme référence immuable.
"""

import os
import sys
import json
import re
from typing import Dict, Any, List, Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from evaluation.benchmark.benchmark_axes import BenchmarkAxis, BenchmarkResult, BenchmarkEvaluationMetric


class ArchiBenchmarkRunner:
    """Moteur de benchmark modulaire."""

    # Dictionnaire de mots-clés d'architecture pour heuristique de validation d'axe
    AXIS_LEXICON = {
        BenchmarkAxis.VISION: ["voit", "perçoit", "visible", "composition", "armoire", "façade", "fenêtre", "présente"],
        BenchmarkAxis.SPATIAL: ["volume", "espace", "hauteur", "profondeur", "hiérarchie", "continuité", "cloison"],
        BenchmarkAxis.ERGONOMIE: ["passage", "hauteur", "assise", "recul", "circulation", "confort", "usage", "accessibilité"],
        BenchmarkAxis.MATERIAUX: ["bois", "chêne", "marbre", "pierre", "verre", "métal", "laiton", "béton", "textile", "cuir"],
        BenchmarkAxis.LUMIERE: ["lumière", "naturelle", "baie vitrée", "éclairage", "ombres", "suspension", "applique", "soleil"],
        BenchmarkAxis.COULEUR: ["blanc", "noir", "gris", "cognac", "ton", "palette", "contraste", "nuance", "chromatique"],
        BenchmarkAxis.STYLE: ["contemporain", "moderne", "minimaliste", "industriel", "classique", "farmhouse", "haussmannien"],
        BenchmarkAxis.CIRCULATION: ["circulation", "flux", "cheminement", "passage", "dégagement", "axe", "accès"],
        BenchmarkAxis.CRITIQUE: ["point fort", "vigilance", "limite", "inconvénient", "déséquilibre", "atout", "risque"],
        BenchmarkAxis.RECOMMANDATION: ["recommandation", "prévoir", "veiller", "optimiser", "ajouter", "modifier", "remplacer"],
        BenchmarkAxis.PLAN_2D: ["plan", "coupe", "élévation", "axe", "surface", "échelle", "trame", "cote"],
        BenchmarkAxis.PEDAGOGIE: ["méthode", "approche", "expliquer", "remarquer", "principe", "sensibilisation"],
        BenchmarkAxis.ANTI_HALLUCINATION: ["sans plan métré", "ne peut être certifié", "à vérifier", "semble", "suppose", "non mesurable"]
    }

    def evaluate_response_on_axes(
        self,
        question: str,
        response: str,
        reference_answer: Optional[str] = None
    ) -> Dict[str, BenchmarkEvaluationMetric]:
        """Évalue une réponse sur les 13 axes."""
        evaluations = {}
        resp_lower = response.lower()

        for axis in BenchmarkAxis:
            keywords = self.AXIS_LEXICON[axis]
            matched = [kw for kw in keywords if kw in resp_lower]
            
            # Score de base heuristique basé sur la présence et la richesse notionnelle
            if axis == BenchmarkAxis.ANTI_HALLUCINATION:
                # Anti-hallucination privilégie la prudence épistémique
                has_epistemic = any(kw in resp_lower for kw in self.AXIS_LEXICON[BenchmarkAxis.ANTI_HALLUCINATION])
                has_hallucination_claim = bool(re.search(r"\b(?:mesure exactement \d+|épaisseur de paroi de \d+ cm)\b", resp_lower))
                
                score = 8.5 if has_epistemic and not has_hallucination_claim else (6.0 if not has_hallucination_claim else 3.0)
                evaluations[axis.value] = BenchmarkEvaluationMetric(
                    axis=axis,
                    score=score,
                    strengths=["Reconnaissance explicite des limites du support visuel"] if has_epistemic else [],
                    weaknesses=["Affirmation technique sans nuance"] if has_hallucination_claim else [],
                    epistemic_caution_detected=has_epistemic
                )
            else:
                ratio = len(matched) / min(len(keywords), 5)
                score = min(10.0, round(5.0 + (ratio * 5.0), 1)) if matched else 4.0
                evaluations[axis.value] = BenchmarkEvaluationMetric(
                    axis=axis,
                    score=score,
                    strengths=[f"Mobilisation du vocabulaire clé : {matched[:3]}"] if matched else [],
                    weaknesses=["Peu de références explicites à cet axe"] if not matched else []
                )

        return evaluations

    def evaluate_baseline_file(self, baseline_json_path: str) -> BenchmarkResult:
        """Charge et benchmarke les inférences de la baseline historique."""
        if not os.path.exists(baseline_json_path):
            raise FileNotFoundError(f"Fichier baseline introuvable : {baseline_json_path}")

        with open(baseline_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Baseline contient la clé "exemples"
        if isinstance(data, list):
            items = data
        else:
            items = data.get("exemples", data.get("evaluations", data.get("results", [])))
        
        axis_totals = {a.value: 0.0 for a in BenchmarkAxis}
        axis_counts = {a.value: 0 for a in BenchmarkAxis}
        sample_evals = []

        for it in items:
            q = it.get("question", "")
            resp = (
                it.get("reponse_generee") or 
                it.get("réponse générée") or 
                it.get("reponse_generée") or 
                it.get("response") or 
                it.get("answer", "")
            )
            ref = (
                it.get("reponse_attendue") or 
                it.get("réponse attendue") or 
                it.get("reference_answer", "")
            )
            
            axes_res = self.evaluate_response_on_axes(q, resp, ref)
            for a_name, metric in axes_res.items():
                axis_totals[a_name] += metric.score
                axis_counts[a_name] += 1

            sample_evals.append({
                "id": it.get("id"),
                "axes": {k: m.model_dump() for k, m in axes_res.items()}
            })

        avg_scores = {}
        for a_name in axis_totals:
            cnt = axis_counts[a_name]
            avg_scores[a_name] = round(axis_totals[a_name] / cnt, 2) if cnt > 0 else 0.0

        global_score = round(sum(avg_scores.values()) / len(avg_scores), 2) if avg_scores else 0.0

        return BenchmarkResult(
            model_name="Qwen2-VL-7B-Instruct",
            checkpoint_or_tag="baseline_zero_shot",
            dataset_version="v0.1-micro-baseline",
            axis_scores=avg_scores,
            global_score=global_score,
            sample_evaluations=sample_evals,
            metadata={"source_file": baseline_json_path, "samples_count": len(items)}
        )


def run_benchmark_cli():
    """Exécution en ligne de commande pour la baseline."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    baseline_path = os.path.join(base_dir, "evaluation", "baseline", "baseline_results.json")
    out_report = os.path.join(base_dir, "evaluation", "reports", "BENCHMARK_BASELINE_REPORT.json")

    runner = ArchiBenchmarkRunner()
    if os.path.exists(baseline_path):
        res = runner.evaluate_baseline_file(baseline_path)
        os.makedirs(os.path.dirname(out_report), exist_ok=True)
        with open(out_report, "w", encoding="utf-8") as f:
            f.write(res.model_dump_json(indent=2))
        print("--- BENCHMARK BASELINE RESULTS (13 AXES) ---")
        print(f"Modèle : {res.model_name} ({res.checkpoint_or_tag})")
        print(f"Score Global : {res.global_score}/10")
        for k, v in res.axis_scores.items():
            print(f"  - {k:20s}: {v}/10")
        print(f"Rapport sauvegardé dans {out_report}")


if __name__ == "__main__":
    run_benchmark_cli()
