# ARCHI-AI — Rapport de Diversité Multi-Échelle (`INDEPENDENT_DIVERSITY_REPORT.md`)

## 1. Métriques de Duplication

- **Nombre d'exemples analysés :** 506
- **Doublons stricts de questions :** 144 (28.5 %)
- **Doublons stricts de réponses :** 143 (28.3 %)
- **Paires de réponses en Quasi-Doublon (Jaccard 3-gramme $\ge 0,80$) :** 2044
- **Groupes de squelettes structurels identiques ($\ge 3$ occurrences) :** 19
- **Exemples issus de gabarits structurels répétés :** 204 (40.3 %)

---

## 2. Richesse Lexicale & Diversité des Sources

- **Type-Token Ratio (TTR) des Questions :** 0.1063 (Vocabulaire varié)
- **Type-Token Ratio (TTR) des Réponses :** 0.0455
- **Nombre de sources uniques mobilisées :** 309
- **Part de la source majoritaire :** 1.2 %

---

## 3. Évaluation du Risque de Surapprentissage de Gabarits (Template Overfitting)
Un taux de duplication structurelle de 40.3 % présente un risque réel de conditionner un modèle à réciter des structures de phrases identiques plutôt que de raisonner de manière plastique sur la géométrie.
