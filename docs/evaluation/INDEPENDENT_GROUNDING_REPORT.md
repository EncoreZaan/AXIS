# ARCHI-AI — Rapport de Grounding Indépendant (`INDEPENDENT_GROUNDING_REPORT.md`)

## 1. Méthodologie d'Audit de Grounding
Contrairement aux validateurs internes qui se basent sur l'existence des clés `evidence` et `epistemic_breakdown`, l'auditeur indépendant décompose chaque affirmation en propositions atomiques et recherche leur trace numérique et sémantique directe dans les données d'entrée.

### Classification des Affirmations :
- **SUPPORTED :** Affirmation étayée à 100% par des cotes, entités ou relations calculées issues du corpus brut ou prétraité.
- **PARTIALLY_SUPPORTED :** Affirmation mixte (éléments factuels avérés mêlés à des extrapolations architecturales plausibles mais non prouvées).
- **UNSUPPORTED :** Valeur numérique, entité ou dimension en contradiction formelle ou absente des données sources.
- **UNKNOWN :** Cliché doctrinal ou principe théorique générique formulé sans aucun ancrage empirique dans le projet examiné.

---

## 2. Statistiques Globales de Grounding

- **Nombre total de propositions auditées :** 2440
- **Propositions SUPPORTED :** 234 (9.6 %)
- **Propositions PARTIALLY_SUPPORTED :** 504 (20.7 %)
- **Propositions UNSUPPORTED :** 115 (4.7 %)
- **Propositions UNKNOWN (Théoriques / Floues) :** 1587 (65.0 %)
- **Ratio Moyen de Grounding :** **19.6 %**

---

## 3. Test de Suppression de Source (Source Ablation Test)

- **Objectif :** Supprimer de la question et de la réponse l'ensemble des identifiants et valeurs numériques propres au projet.
- **Résultat :** **38 / 506 (7.5 %)** des réponses auditées survivent intégralement comme gabarits autonomes et plausibles.
- **Diagnostic :** Une proportion notable des paragraphes d'analyse et de raisonnement sont des gabarits discursifs réutilisables qui ne s'effondrent pas en l'absence de données source.
