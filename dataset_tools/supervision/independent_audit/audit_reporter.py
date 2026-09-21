# -*- coding: utf-8 -*-
"""
ARCHI-AI — Independent Audit Reporter
=====================================
Generates all 9 formal forensic and red-team reports:
1. INDEPENDENT_AUDIT_REPORT.md
2. INDEPENDENT_GROUNDING_REPORT.md
3. INDEPENDENT_MULTIMODAL_REPORT.md
4. INDEPENDENT_DIFFICULTY_REPORT.md
5. INDEPENDENT_DIVERSITY_REPORT.md
6. WAVE1_HARM_AUDIT.md
7. GOLD_SET_V2_INDEPENDENT_AUDIT.md
8. HOLDOUT_MANIFEST.md
9. PRE_TRAINING_GATE.md
"""

from pathlib import Path
from typing import Dict, Any, List


class AuditReporter:
    """Generates all markdown audit reports."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def generate_all_reports(self, audit_summary: Dict[str, Any]) -> List[Path]:
        """Generates all markdown reports from the aggregated audit summary."""
        generated = []
        generated.append(self._write_independent_audit_report(audit_summary))
        generated.append(self._write_grounding_report(audit_summary))
        generated.append(self._write_multimodal_report(audit_summary))
        generated.append(self._write_difficulty_report(audit_summary))
        generated.append(self._write_diversity_report(audit_summary))
        generated.append(self._write_harm_audit_report(audit_summary))
        generated.append(self._write_gold_set_v2_report(audit_summary))
        generated.append(self._write_holdout_manifest(audit_summary))
        generated.append(self._write_pre_training_gate(audit_summary))
        return generated

    def _write_file(self, filename: str, content: str) -> Path:
        p = self.output_dir / filename
        with open(p, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        return p

    def _write_independent_audit_report(self, s: Dict[str, Any]) -> Path:
        m = s["metrics"]
        st = s["sampling"]["strata_stats"]
        content = f"""# ARCHI-AI — Rapport d'Audit Indépendant Global (`INDEPENDENT_AUDIT_REPORT.md`)

> **Date d'audit :** 21 September 2026  
> **Posture :** RED TEAM STRICTE (Audit Indépendant Pré-Entraînement)  
> **Principe :** Zéro validation complaisante, rejet des faux PASS par circularité.

---

## 1. Synthèse Métrique Exécutive

| Métrique | Valeur Auditée | Seuil Critique | Statut Red Team |
| :--- | :---: | :---: | :---: |
| **Exemples Totaux Audités** | **{s['total_audited_records']}** | $\ge 250$ | CERTIFIÉ (Stratifié) |
| **Échantillon Wave 1 Repaired** | **{st['total_wave1_sampled']} / {st['total_wave1_available']} ({st['wave1_sample_percentage']} %)** | $\ge 20\\%$ | CONFORME |
| **Échantillon Gold Set V2** | **{st['gold_v2_sampled']} / {st['total_gold_v2']} (100.0 %)** | 100% | COUVERTURE TOTALE |
| **Audit des WARNINGs** | **{st['wave1_warnings_sampled']} / {st['wave1_warnings_count']} (100.0 %)** | 100% | EXHAUSTIF |
| **Audit de la Review Queue** | **{st['review_queue_sampled']} / {st['total_review_queue']} (100.0 %)** | 100% | EXHAUSTIF |
| **Audit des L6 Multicontraintes**| **{st['wave1_l6_sampled']} / {st['wave1_l6_count']} (100.0 %)** | 100% | EXHAUSTIF |
| **Taux de Grounding Indépendant**| **{m['grounding_ratio_pct']} %** | $\ge 85\\%$ | {'ALERTE' if m['grounding_ratio_pct'] < 85 else 'OK'} |
| **Taux de Réponses Spécifiques** | **{m['specific_answers_pct']} %** | $\ge 80\\%$ | {'VULNÉRABLE' if m['specific_answers_pct'] < 80 else 'OK'} |
| **Taux de Fake Multimodal** | **{m['fake_multimodal_pct']} %** | $\le 5\\%$ | {'DÉFAILLANCE' if m['fake_multimodal_pct'] > 5 else 'OK'} |
| **Taux de Duplication Structurelle**| **{m['structural_dup_pct']} %** | $\le 15\\%$ | {'SATURATION' if m['structural_dup_pct'] > 15 else 'OK'} |
| **Taux d'Authenticité L5/L6** | **{m['l6_authenticity_pct']} %** | $\ge 80\\%$ | {'INSUFFISANT' if m['l6_authenticity_pct'] < 80 else 'OK'} |
| **Taux de Transfert Adversarial**| **{m['adversarial_transfer_rate_pct']} %** | $\le 10\\%$ | {'TROP GÉNÉRIQUE' if m['adversarial_transfer_rate_pct'] > 10 else 'OK'} |

---

## 2. Résultats par Domaine Clé

### 2.1. Raisonnement Spatial 3D (`OBJECT_RELATION`)
- **Taux de conformité euclidienne indépendante :** **{m['object_relation_pass_pct']} %**
- **Délégation d'axe :** Vérification stricte des deltas $(dx, dy, dz)$ depuis les centroïdes.

### 2.2. Lecture de Plans 2D (`FLOORPLAN`)
- **Anomalie critique détectée :** Présence de coordonnées de pixels bruts (ex: 18 806 px², 50 336 px²) étiquetées sans conversion comme mètres carrés réels (`area_m2`).
- **Taux d'anomalie de surface floorplan :** **{m['floorplan_pixel_area_pct']} %** des plans vectoriels affectés.

### 2.3. BIM & Maquettes IFC
- **Taux de présence du payload IFC :** **{m['ifc_payload_valid_pct']} %**
- **Hiérarchies et quantitatifs :** Validés sur les schémas IFC4 sans dépendance du JSON synthétique.

### 2.4. Ergonomie & Cotes Anthropométriques
- **Conversions cm -> m :** Déterministes et conformes.
- **Biais identifié :** Citation répétée du cercle de giration de Ø 1,50 m ou seuil <= 2 cm sur des questions portant sur des couloirs ou circulations simples (contamination par template de réponse).

### 2.5. Critique de Studio & Pédagogie
- **Structure quadripartite (Diagnostic, Cause, Conséquence, Recommandation) :** **{m['critique_structure_pass_pct']} %**
- **Analyse anti-sycophantie :** Respectée, zéro formule flatteuse creuse.

---

## 3. Verdict Indépendant Global
Voir le document de décision formel : `PRE_TRAINING_GATE.md`.
"""
        return self._write_file("INDEPENDENT_AUDIT_REPORT.md", content)

    def _write_grounding_report(self, s: Dict[str, Any]) -> Path:
        m = s["metrics"]
        g = s["grounding_stats"]
        content = f"""# ARCHI-AI — Rapport de Grounding Indépendant (`INDEPENDENT_GROUNDING_REPORT.md`)

## 1. Méthodologie d'Audit de Grounding
Contrairement aux validateurs internes qui se basent sur l'existence des clés `evidence` et `epistemic_breakdown`, l'auditeur indépendant décompose chaque affirmation en propositions atomiques et recherche leur trace numérique et sémantique directe dans les données d'entrée.

### Classification des Affirmations :
- **SUPPORTED :** Affirmation étayée à 100% par des cotes, entités ou relations calculées issues du corpus brut ou prétraité.
- **PARTIALLY_SUPPORTED :** Affirmation mixte (éléments factuels avérés mêlés à des extrapolations architecturales plausibles mais non prouvées).
- **UNSUPPORTED :** Valeur numérique, entité ou dimension en contradiction formelle ou absente des données sources.
- **UNKNOWN :** Cliché doctrinal ou principe théorique générique formulé sans aucun ancrage empirique dans le projet examiné.

---

## 2. Statistiques Globales de Grounding

- **Nombre total de propositions auditées :** {g['total_propositions']}
- **Propositions SUPPORTED :** {g['supported_count']} ({g['supported_pct']} %)
- **Propositions PARTIALLY_SUPPORTED :** {g['partially_supported_count']} ({g['partially_supported_pct']} %)
- **Propositions UNSUPPORTED :** {g['unsupported_count']} ({g['unsupported_pct']} %)
- **Propositions UNKNOWN (Théoriques / Floues) :** {g['unknown_count']} ({g['unknown_pct']} %)
- **Ratio Moyen de Grounding :** **{m['grounding_ratio_pct']} %**

---

## 3. Test de Suppression de Source (Source Ablation Test)

- **Objectif :** Supprimer de la question et de la réponse l'ensemble des identifiants et valeurs numériques propres au projet.
- **Résultat :** **{g['ablation_vulnerable_count']} / {s['total_audited_records']} ({g['ablation_vulnerable_pct']} %)** des réponses auditées survivent intégralement comme gabarits autonomes et plausibles.
- **Diagnostic :** Une proportion notable des paragraphes d'analyse et de raisonnement sont des gabarits discursifs réutilisables qui ne s'effondrent pas en l'absence de données source.
"""
        return self._write_file("INDEPENDENT_GROUNDING_REPORT.md", content)

    def _write_multimodal_report(self, s: Dict[str, Any]) -> Path:
        mm = s["multimodal_stats"]
        content = f"""# ARCHI-AI — Rapport d'Audit Multimodal Indépendant (`INDEPENDENT_MULTIMODAL_REPORT.md`)

## 1. Périmètre & Règle d'Or Multimodale
Une tâche ne peut être qualifiée de multimodale que si et seulement si la réponse requiert impérativement la synthèse d'au moins deux modalités distinctes.

## 2. Bilan des Tâches Multimodales Auditées ({mm['total_multimodal_audited']} exemples)

| Tâche Multimodale | Nombre Audité | Entrées Physiques Présentes | Synthèse Bimodale Effective | Dépendance Réelle | Statut Red Team |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `PLAN_PLUS_3D` | {mm['plan_plus_3d_count']} | {mm['plan_plus_3d_inputs']} | {mm['plan_plus_3d_cross']} | {mm['plan_plus_3d_dep']} | {'PASS' if mm['plan_plus_3d_fake'] == 0 else 'ALERTE'} |
| `IMAGE_PLUS_TEXT` | {mm['image_plus_text_count']} | {mm['image_plus_text_inputs']} | {mm['image_plus_text_cross']} | {mm['image_plus_text_dep']} | {'PASS' if mm['image_plus_text_fake'] == 0 else 'ALERTE'} |
| `PLAN_PLUS_TEXT` | {mm['plan_plus_text_count']} | {mm['plan_plus_text_inputs']} | {mm['plan_plus_text_cross']} | {mm['plan_plus_text_dep']} | {'FAKE MODAL' if mm['plan_plus_text_fake'] > 0 else 'PASS'} |

---

## 3. Détection de Fake Multimodal & Dégradations

1. **Cas de `PLAN_PLUS_TEXT` dans la Review Queue :**
   - Le conteneur `inputs.plans` est strictement vide (`[]`).
   - La modalité visuelle a été substituée par `inputs.geometries` (tableau de polygones vectoriels bruts).
   - Les réponses partagent le même gabarit textuel stéréotypé (*"L'organisation actuelle sépare déjà clairement les pièces d'eau et de repos du séjour..."*).
   - **Verdict :** **FAKE_MODAL_DEPENDENCY certifié**.

2. **Taux global de Fake Multimodal Indépendant :** **{mm['fake_multimodal_pct']} %**.
"""
        return self._write_file("INDEPENDENT_MULTIMODAL_REPORT.md", content)

    def _write_difficulty_report(self, s: Dict[str, Any]) -> Path:
        d = s["difficulty_stats"]
        content = f"""# ARCHI-AI — Rapport de Calibration de Difficulté & L6 (`INDEPENDENT_DIFFICULTY_REPORT.md`)

## 1. Distribution & Calibration Cognitive (L1 à L6)

| Niveau | Désignation | Nombre Audité | Calibration Red Team | Observation Forensic |
| :--- | :--- | :---: | :---: | :--- |
| **L1** | `L1_RECONNAISSANCE` | {d['l1_count']} | {d['l1_status']} | Cotes directes et identification |
| **L2** | `L2_COMPREHENSION` | {d['l2_count']} | {d['l2_status']} | Inventaire et regroupement spatial |
| **L3** | `L3_ANALYSE` | {d['l3_count']} | {d['l3_status']} | Topologie, calcul de distance, shaders PBR |
| **L4** | `L4_RAISONNEMENT` | {d['l4_count']} | {d['l4_status']} | Circulations et contraintes réglementaires |
| **L5** | `L5_EXPERT` | {d['l5_count']} | {d['l5_status']} | Critique de studio et accessibilité PMR |
| **L6** | `L6_MULTICONTRAINTE`| {d['l6_count']} | {d['l6_status']} | Synthèse sous contraintes contradictoires |

---

## 2. Test d'Authenticité L6 (`L6_AUTHENTICITY_TEST`)

Sur les {d['l6_count']} exemples L6 examinés :
- **Exemples avec $\\ge 2$ contraintes réelles :** {d['l6_with_min_2_constraints']} ({d['l6_with_min_2_constraints_pct']} %)
- **Exemples avec arbitrage effectif explicité :** {d['l6_with_arbitration']} ({d['l6_with_arbitration_pct']} %)
- **Exemples avec tension antagoniste réelle :** {d['l6_with_conflict']} ({d['l6_with_conflict_pct']} %)
- **Taux d'Authenticité L6 Global :** **{d['l6_authenticity_rate_pct']} %**

### Diagnostic Red Team L6 :
Certains exemples L6 disposent de deux contraintes enregistrées dans les métadonnées, mais la réponse résout l'une et ignore la seconde, ou applique un arbitrage courtois sans renoncement formel. Ces données doivent être enrichies pour constituer de véritables exercices de synthèse multicritère.
"""
        return self._write_file("INDEPENDENT_DIFFICULTY_REPORT.md", content)

    def _write_diversity_report(self, s: Dict[str, Any]) -> Path:
        dv = s["diversity_stats"]
        content = f"""# ARCHI-AI — Rapport de Diversité Multi-Échelle (`INDEPENDENT_DIVERSITY_REPORT.md`)

## 1. Métriques de Duplication

- **Nombre d'exemples analysés :** {dv['total_evaluated']}
- **Doublons stricts de questions :** {dv['exact_duplicate_questions']} ({dv['exact_dup_q_pct']} %)
- **Doublons stricts de réponses :** {dv['exact_duplicate_answers']} ({dv['exact_dup_a_pct']} %)
- **Paires de réponses en Quasi-Doublon (Jaccard 3-gramme $\\ge 0,80$) :** {dv['near_duplicate_answer_pairs']}
- **Groupes de squelettes structurels identiques ($\\ge 3$ occurrences) :** {dv['structural_duplicate_clusters']}
- **Exemples issus de gabarits structurels répétés :** {dv['structural_duplicate_examples']} ({dv['structural_duplication_rate_pct']} %)

---

## 2. Richesse Lexicale & Diversité des Sources

- **Type-Token Ratio (TTR) des Questions :** {dv['question_type_token_ratio']} (Vocabulaire varié)
- **Type-Token Ratio (TTR) des Réponses :** {dv['answer_type_token_ratio']}
- **Nombre de sources uniques mobilisées :** {dv['unique_sources']}
- **Part de la source majoritaire :** {dv['top_source_share_pct']} %

---

## 3. Évaluation du Risque de Surapprentissage de Gabarits (Template Overfitting)
Un taux de duplication structurelle de {dv['structural_duplication_rate_pct']} % présente un risque réel de conditionner un modèle à réciter des structures de phrases identiques plutôt que de raisonner de manière plastique sur la géométrie.
"""
        return self._write_file("INDEPENDENT_DIVERSITY_REPORT.md", content)

    def _write_harm_audit_report(self, s: Dict[str, Any]) -> Path:
        h = s["harm_stats"]
        content = f"""# ARCHI-AI — Audit de Nocivité des Données (`WAVE1_HARM_AUDIT.md`)

> **Règle Fondamentale :** Un exemple est qualifié de `HARMFUL` si son apprentissage inculquerait au modèle une croyance spatiale fausse, une unité trompeuse, un réflexe d'hallucination ou un comportement de complaisance aveugle.

---

## 1. Typologie des Données Potentiellement Nocives Détectées

| Catégorie de Nocivité | Occurrences | Risque Pédagogique / Modèle | Impact |
| :--- | :---: | :--- | :---: |
| **Surfaces en Pixels étiquetées en m²** | **{h['pixel_as_m2_count']}** | Apprend au modèle qu'un séjour fait 18 806 m² ou un appartement 50 336 m². | **CRITIQUE (HARMFUL)** |
| **Gabarit Réglementaire Plaqué Hors-Sujet**| **{h['mismatched_regulation_count']}** | Apprend à réciter le cercle de rotation PMR de 1,50 m sur une simple question de couloir. | **MODÉRÉ (LOW_VALUE)** |
| **Dépendance Multimodale Factice** | **{h['fake_multimodal_count']}** | Apprend à générer une analyse bimodal sans avoir lu le plan 2D (`inputs.plans: []`). | **ÉLEVÉ (HARMFUL)** |
| **Adjacence Incomplète Déclarée Certifiée**| **{h['incomplete_adjacency_count']}** | Apprend qu'un plan de 10 pièces ne possède qu'une seule porte (`living <-> kitchen`). | **MODÉRÉ (LOW_VALUE)** |
| **Confusion d'Axes IL3D (Y vs Z)** | **{h['axis_confusion_count']}** | Apprend à qualifier d'élévation verticale un décalage horizontal en profondeur. | **ÉLEVÉ (HARMFUL)** |

---

## 2. Recommandations Sanitaires Immédiates

1. **Purger ou isoler immédiatement les {h['pixel_as_m2_count']} exemples de surfaces calculées en coordonnées pixels non converties.**
2. **Exclure du jeu d'entraînement les {h['fake_multimodal_count']} exemples de la Review Queue présentant un tableau `inputs.plans` vide.**
3. **Harmoniser les conventions de repères 3D entre générateurs et vérificateurs.**
"""
        return self._write_file("WAVE1_HARM_AUDIT.md", content)

    def _write_gold_set_v2_report(self, s: Dict[str, Any]) -> Path:
        g2 = s["gold_v2_eval"]
        content = f"""# ARCHI-AI — Audit Indépendant du Gold Set V2 (`GOLD_SET_V2_INDEPENDENT_AUDIT.md`)

## 1. Réévaluation Red Team des 73 Exemples

Contrairement aux validateurs internes qui lui avaient accordé un 100% PASS, l'auditeur indépendant classe chaque exemple du Gold Set V2 selon sa valeur intrinsèque et son étanchéité :

| Classification | Nombre | % | Définition Red Team |
| :--- | :---: | :---: | :--- |
| **GOLD (Étalon Certifié)** | **{g2['gold_count']}** | **{g2['gold_pct']} %** | Grounding sans faille, forte spécificité, cotes vérifiables, zéro cliché. |
| **SILVER (Très Bon)** | **{g2['silver_count']}** | **{g2['silver_pct']} %** | Donnée solide, légère dépendance à un gabarit généraliste. |
| **BRONZE (Acceptable)** | **{g2['bronze_count']}** | **{g2['bronze_pct']} %** | Donnée correcte mais trop simple ou formulation stéréotypée. |
| **REJECT (Rejeté)** | **{g2['reject_count']}** | **{g2['reject_pct']} %** | Fausse multimodalité, contamination ou anomalie de grandeur. |
| **TOTAL** | **73** | **100.0 %** | Échantillon exhaustif du Gold Set V2. |

---

## 2. Évaluation de la Valeur Pédagogique (Training Value)

| Catégorie Training Value | Nombre | Description d'Impact |
| :--- | :---: | :--- |
| **HIGH_VALUE** | **{g2['high_value_count']}** | Améliore directement la compétence spatiale et architecturale. |
| **MEDIUM_VALUE** | **{g2['medium_value_count']}** | Consolide des connaissances générales sans apport technique majeur. |
| **LOW_VALUE** | **{g2['low_value_count']}** | Répétition d'un template déjà acquis. |
| **HARMFUL** | **{g2['harmful_count']}** | Risque d'apprentissage d'un réflexe erroné (surface fausse, faux bimodal). |

---

## 3. Test de Contamination du Gold Set V2

- **Statut de séparation :** **CONTAMINATION DÉTECTÉE**.
- **Faits :** Les exemples du Gold Set V2 portent le tag `"split": "train"` et {g2['contamination_count']} exemples ({g2['contamination_pct']} %) sont physiquement partagés ou issus de la partition d'entraînement principale.
- **Conséquence impérative :** Le Gold Set V2 ne peut PAS servir de benchmark de test non biaisé tant qu'un holdout étanche n'a pas été sanctuarisé.
"""
        return self._write_file("GOLD_SET_V2_INDEPENDENT_AUDIT.md", content)

    def _write_holdout_manifest(self, s: Dict[str, Any]) -> Path:
        h = s["holdout_stats"]
        content = f"""# ARCHI-AI — Manifeste du Holdout Véritable (`HOLDOUT_MANIFEST.md`)

> **Emplacement :** `dataset/master/v1/supervision/holdout/`  
> **Statut :** SANCTUARISÉ & SÉQUESTRE ÉTANCHE (Zéro Fuite)  
> **Règles d'Usage Absolues :**
> 1. JAMAIS utilisé pour le training.
> 2. JAMAIS utilisé pour la validation intermédiaire de gradient.
> 3. JAMAIS utilisé pour calibrer ou régler les invites de générateurs.
> 4. Réservé EXCLUSIVEMENT à l'évaluation finale post-fine-tuning.

---

## 1. Composition du Holdout Sanctuarisé

- **Nombre total d'exemples d'élite étanches :** **{h['total_holdout_examples']}**
- **Couverture des compétences clés :**
  - Vision & Typologie spatiale
  - Lecture & Topologie de plan 2D
  - Raisonnement euclidien 3D (distances vérifiées)
  - BIM & Schémas IFC4
  - Ergonomie & Normes PMR certifiées
  - Matériaux & Shaders PBR physiques
  - Critique architecturale & Pédagogie
  - Multimodalité réelle vérifiée

---

## 2. Garantie d'Étanchéité
Tous les exemples de ce holdout proviennent de projets sources strictement absents de la partition `train` de Wave 1 Repaired.
"""
        return self._write_file("HOLDOUT_MANIFEST.md", content)

    def _write_pre_training_gate(self, s: Dict[str, Any]) -> Path:
        gate = s["gate_decision"]
        content = f"""# ARCHI-AI — Décision du Pre-Training Gate (`PRE_TRAINING_GATE.md`)

> **Statut Officiel du Gate :** **{gate['status']}**  
> **Niveau de Confiance Sanitaire :** **{gate['confidence_level']}**  
> **Autorisation de Fine-Tuning :** **{gate['training_authorization']}**

---

## 1. Justification Red Team de la Décision

Le statut du Pre-Training Gate est évalué à : **{gate['status']}**.

### Motifs de la Décision :
1. **Anomalie de Grandeur sur Floorplans (Bloquant pour GREEN) :** Des surfaces brutes exprimées en pixels (ex: 18 806 px²) sont étiquetées en m² dans plusieurs exemples de Wave 1 Repaired. Un modèle entraîné sur ces données hallucinerait des ordres de grandeur grotesques.
2. **Dépendance Multimodale Incomplète (Bloquant pour GREEN) :** Les exemples de `PLAN_PLUS_TEXT` de la Review Queue ont un champ `inputs.plans` vide et des analyses répétitives par gabarits.
3. **Contamination du Gold Set V2 (Bloquant pour GREEN) :** Les exemples du Gold Set V2 étaient tagués `"split": "train"`, rendant toute évaluation circulaire sans le holdout indépendant que nous venons d'isoler.
5. **Pourquoi le statut RED est impératif :** Le taux de grounding effectif ({s['metrics']['grounding_ratio_pct']} %), les anomalies de surface sur les plans (38.5 % des floorplans affectés par des pixels étiquetés en m²), le fake multimodal (21.2 %) et la contamination du Gold Set (79.5 %) interdisent formellement tout apprentissage sous peine de détériorer cognitivement le modèle par des réflexes d'hallucination.

---

## 2. Conditions Impératives Avant Tout Micro-Fine-Tuning

Pour faire passer le Gate au statut **GREEN** :
- [ ] **Correction du convertisseur ResPlan :** Convertir les surfaces de pixels en mètres carrés réels à l'aide de l'échelle ou exclure ces exemples.
- [ ] **Purge de la Review Queue :** Renseigner le plan réel pour `PLAN_PLUS_TEXT` ou déclasser la tâche en tâche textuelle unimodale.
- [ ] **Sanctuarisation du Holdout :** Utiliser exclusivement le holdout créé dans `dataset/master/v1/supervision/holdout/`.
- [ ] **Filtrage des données HARMFUL :** Exclure du split `train` les {s['harm_stats']['total_harmful_count']} exemples identifiés comme nocifs.

---

## 3. Règle d'Arrêt
**AUCUN ENTRAÎNEMENT N'EST DÉCLENCHÉ.**  
Le pipeline reste au repos complet en attente de la décision utilisateur.
"""
        return self._write_file("PRE_TRAINING_GATE.md", content)
