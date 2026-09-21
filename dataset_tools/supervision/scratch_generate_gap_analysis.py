import os
import sys
import json
from collections import Counter

sys.path.insert(0, os.path.abspath("."))
from dataset_tools.supervision.task_catalogue import TASK_CATALOGUE
from dataset_tools.supervision.scratch_eval_tasks import TASK_AUDIT_SPECS

lines = []
lines.append("# ARCHI-AI — Audit & Gap Analysis des 69 Tâches de Supervision (`SUPERVISION_TASK_GAP_ANALYSIS.md`)")
lines.append("")
lines.append("> **Phase :** PHASE 2 — Supervision Engineering & Pre-Training Gate  ")
lines.append("> **Artefact d'entrée :** MASTER DATASET v2 (65 342 records consolidés, étanches et audités)  ")
lines.append("> **Statut de l'Audit :** AUDIT EXHAUSTIF RÉALISÉ — BASELINE 69 TÂCHES  ")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 1. Synthèse Exécutive de l'Audit des 69 Tâches")
lines.append("")

status_counts = Counter(v["status"] for v in TASK_AUDIT_SPECS.values())
lines.append("| Statut Forensic | Nombre de Tâches | % du Catalogue | Décision d'Ingénierie |")
lines.append("| :--- | :---: | :---: | :--- |")
status_descriptions = {
    "VALID": "Tâches pleinement ancrées dans le Master Dataset v2 avec cibles vérifiables et nécessité multimodale démontrée.",
    "DUPLICATE": "Tâches redondantes avec une autre tâche du catalogue (fusion ou restriction requise pour éviter l'inflation artificielle).",
    "PARTIAL": "Tâches valides conceptuellement mais nécessitant un cadrage strict de la consigne ou un formatage expert pour éviter la réponse générique.",
    "MISSING_EVIDENCE": "Données sources ou annotations manquantes dans le Master Dataset v2 (impossible à superviser de façon déterministe).",
    "INVALID": "Tâche mathématiquement ou physiquement invalide sur le corpus actuel (ex: surfaces métriques m² sur plans matriciels sans échelle).",
    "FAKE_MULTIMODAL": "Risque critique de faux multimodal : la modalité texte ou image suffit à elle seule à donner la réponse sans croisement.",
    "UNDERSPECIFIED": "Tâche trop générique ou floue, sans contrat d'évaluation atomique mesurable."
}

for st, count in status_counts.most_common():
    pct = (count / 69.0) * 100.0
    desc = status_descriptions.get(st, "")
    lines.append(f"| **`{st}`** | **{count}** | {pct:.1f} % | {desc} |")

lines.append(f"| **TOTAL** | **69** | **100.0 %** | *Catalogue complet V1 inspecté* |")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 2. Tableau d'Audit Forensic des 69 Tâches")
lines.append("")
lines.append("| N° | Task ID | Task Name | Family | Modality | Difficulty | Input Types | Target Type | Grounding | Status |")
lines.append("| :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :---: |")

for tid, t in sorted(TASK_CATALOGUE.items(), key=lambda x: x[1].number):
    num = t.number
    name = t.name
    spec = TASK_AUDIT_SPECS.get(tid, {})
    fam = spec.get("family", t.group.value)
    mod = spec.get("modality", "MULTIMODAL")
    diffs = [d.value.split('_')[0] for d in t.allowed_difficulties]
    diff_str = f"{diffs[0]}-{diffs[-1]}" if len(diffs) > 1 else diffs[0]
    inp = ", ".join(spec.get("input_types", ["generic"]))
    tgt = spec.get("target_type", "generic")
    grd = spec.get("grounding", "UNVERIFIED")
    st = spec.get("status", "REVIEW")
    
    lines.append(f"| {num:02d} | `{tid}` | {name} | {fam} | `{mod}` | {diff_str} | {inp} | {tgt} | {grd} | **`{st}`** |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## 3. Analyse Détaillée des Anomalies & Déclassements")
lines.append("")
lines.append("### 3.1. Tâches Invalidées (`INVALID`) — 1 tâche")
lines.append("- **`PLAN_SUMMARY` (#15)** : Cette tâche prétendait extraire la 'synthèse métrique' (surfaces m², dimensions en mètres) des plans 2D. Or, 99.8 % des plans 2D du Master Dataset proviennent de `CORE_RPLAN` (rasters 256x256 sans échelle métrique) et `CORE_RESPLAN` (6 enregistrements présentant une anomalie critique de pixels bruts étiquetés comme m²). Déclarer des mètres carrés sur ces données constitue une hallucination d'unité. **Action : INVALIDÉ / REJETÉ** pour la supervision métrique, ou restreint strictement au comptage de pièces et dimensions en pixels.")
lines.append("")
lines.append("### 3.2. Faux Multimodal Critique (`FAKE_MULTIMODAL`) — 1 tâche")
lines.append("- **`IMAGE_PLUS_TEXT` (#66)** : Dans la configuration précédente, une image était fournie avec une description textuelle complète où la réponse figurait déjà dans l'énoncé textuel (ex : 'Cette photo montre un parquet en chêne massif. Quel est le revêtement ?'). L'image devenait un simple artefact décoratif. **Action : RECLASSIFIÉ EN TEST DE COHÉRENCE / DISCRÉPANCE STRICTE** : le texte doit porter une assertion (potentiellement erronée) que seule l'image permet de confirmer ou d'infirmer.")
lines.append("")
lines.append("### 3.3. Données Manquantes (`MISSING_EVIDENCE`) — 5 tâches")
lines.append("1. **`STYLE_ANALYSIS` (#06)** : Le Master Dataset ne possède pas d'annotations de styles vérifiées sur le corpus visuel (un seul fichier CSV de tendances générales est présent). Générer des styles sans vérité terrain mène à des hallucinations pures.")
lines.append("2. **`FURNITURE_LAYOUT_ANALYSIS` (#13)** : Le corpus `CORE_RPLAN` ne contient aucun masque de mobilier (uniquement murs, portes, pièces). Seul `CORE_IL3D` possède du mobilier en 3D.")
lines.append("3. **`ARCHITECTURE_HISTORY` (#44)** : Aucun corpus textuel ou visuel d'histoire globale du bâtiment n'est présent (uniquement du mobilier design MoMA/Met).")
lines.append("4. **`OPTION_COMPARISON` (#56)** : Aucun doublet de plans 'Variante A vs Variante B' sur la même emprise n'existe dans le Master Dataset.")
lines.append("5. **`IMAGE_PLUS_PLAN_PLUS_TEXT` (#67)** : Le corpus ne compte que 3 enregistrements MMMU Architecture comportant ce triplet, insuffisant pour un entraînement robuste.")
lines.append("")
lines.append("### 3.4. Tâches Redondantes (`DUPLICATE`) — 9 tâches")
lines.append("- `INTERIOR_ANALYSIS` (#02) → Doublon de `IMAGE_ANALYSIS` (#01)")
lines.append("- `SPATIAL_LAYOUT_ANALYSIS` (#20) → Doublon de `SCENE_GRAPH_REASONING` (#17) et `ROOM_OBJECT_REASONING` (#19)")
lines.append("- `STYLE_CLASSIFICATION` (#41) → Doublon de `STYLE_ANALYSIS` (#06)")
lines.append("- `STRENGTH_IDENTIFICATION` (#47) → Sous-ensemble de `PROJECT_CRITIQUE` (#46)")
lines.append("- `WEAKNESS_IDENTIFICATION` (#48) → Sous-ensemble de `PROJECT_CRITIQUE` (#46) et `DESIGN_PROBLEM_DETECTION` (#49)")
lines.append("- `ALTERNATIVE_DESIGN` (#51) → Doublon de `IMPROVEMENT_PROPOSAL` (#50)")
lines.append("- `TRADEOFF_ANALYSIS` (#55) → Doublon de `CONSTRAINT_REASONING` (#53)")
lines.append("- `STUDIO_CRITIQUE` (#59) → Doublon stylistique de `PROJECT_CRITIQUE` (#46)")
lines.append("- `ERROR_EXPLANATION` (#61) → Doublon didactique de `DESIGN_PROBLEM_DETECTION` (#49)")
lines.append("")
lines.append("### 3.5. Tâches Sous-Spécifiées (`UNDERSPECIFIED`) — 1 tâche")
lines.append("- **`MULTIMODAL_PROJECT_REASONING` (#69)** : Tâche 'chapeau' sans critères de réussite mesurables ni entrées bornées. Doit être décomposée en tâches atomiques.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 4. Recommandations pour le Pipeline de Supervision Phase 2")
lines.append("1. **Périmètre Utile :** Se concentrer sur les **43 tâches `VALID`** hautement ancrées et les **9 tâches `PARTIAL`** rigoureusement bornées.")
lines.append("2. **Quarantaine ResPlan :** Isoler strictement les 6 assets ResPlan jusqu'à vérification formelle de calibration.")
lines.append("3. **Interdiction Formelle des Templates Fixes :** Chaque exemple doit découler dynamiquement des coordonnées, entités IFC, masques ou graphes réels.")
lines.append("4. **Vérification de Nécessité Multimodale :** Appliquer le test d'ablation pour rejeter tout exemple solvable en mode aveugle.")

report_content = "\n".join(lines)
output_path = os.path.abspath("SUPERVISION_TASK_GAP_ANALYSIS.md")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(report_content)

print(f"Generated {output_path} ({len(report_content)} bytes)")
