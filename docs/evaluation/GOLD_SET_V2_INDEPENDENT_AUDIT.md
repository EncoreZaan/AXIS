# ARCHI-AI — Audit Indépendant du Gold Set V2 (`GOLD_SET_V2_INDEPENDENT_AUDIT.md`)

## 1. Réévaluation Red Team des 73 Exemples

Contrairement aux validateurs internes qui lui avaient accordé un 100% PASS, l'auditeur indépendant classe chaque exemple du Gold Set V2 selon sa valeur intrinsèque et son étanchéité :

| Classification | Nombre | % | Définition Red Team |
| :--- | :---: | :---: | :--- |
| **GOLD (Étalon Certifié)** | **1** | **1.4 %** | Grounding sans faille, forte spécificité, cotes vérifiables, zéro cliché. |
| **SILVER (Très Bon)** | **0** | **0.0 %** | Donnée solide, légère dépendance à un gabarit généraliste. |
| **BRONZE (Acceptable)** | **66** | **90.4 %** | Donnée correcte mais trop simple ou formulation stéréotypée. |
| **REJECT (Rejeté)** | **6** | **8.2 %** | Fausse multimodalité, contamination ou anomalie de grandeur. |
| **TOTAL** | **73** | **100.0 %** | Échantillon exhaustif du Gold Set V2. |

---

## 2. Évaluation de la Valeur Pédagogique (Training Value)

| Catégorie Training Value | Nombre | Description d'Impact |
| :--- | :---: | :--- |
| **HIGH_VALUE** | **1** | Améliore directement la compétence spatiale et architecturale. |
| **MEDIUM_VALUE** | **0** | Consolide des connaissances générales sans apport technique majeur. |
| **LOW_VALUE** | **66** | Répétition d'un template déjà acquis. |
| **HARMFUL** | **6** | Risque d'apprentissage d'un réflexe erroné (surface fausse, faux bimodal). |

---

## 3. Test de Contamination du Gold Set V2

- **Statut de séparation :** **CONTAMINATION DÉTECTÉE**.
- **Faits :** Les exemples du Gold Set V2 portent le tag `"split": "train"` et 58 exemples (79.5 %) sont physiquement partagés ou issus de la partition d'entraînement principale.
- **Conséquence impérative :** Le Gold Set V2 ne peut PAS servir de benchmark de test non biaisé tant qu'un holdout étanche n'a pas été sanctuarisé.
