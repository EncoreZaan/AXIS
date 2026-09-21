# ARCHI-AI — Audit de Nocivité des Données (`WAVE1_HARM_AUDIT.md`)

> **Règle Fondamentale :** Un exemple est qualifié de `HARMFUL` si son apprentissage inculquerait au modèle une croyance spatiale fausse, une unité trompeuse, un réflexe d'hallucination ou un comportement de complaisance aveugle.

---

## 1. Typologie des Données Potentiellement Nocives Détectées

| Catégorie de Nocivité | Occurrences | Risque Pédagogique / Modèle | Impact |
| :--- | :---: | :--- | :---: |
| **Surfaces en Pixels étiquetées en m²** | **10** | Apprend au modèle qu'un séjour fait 18 806 m² ou un appartement 50 336 m². | **CRITIQUE (HARMFUL)** |
| **Gabarit Réglementaire Plaqué Hors-Sujet**| **0** | Apprend à réciter le cercle de rotation PMR de 1,50 m sur une simple question de couloir. | **MODÉRÉ (LOW_VALUE)** |
| **Dépendance Multimodale Factice** | **31** | Apprend à générer une analyse bimodal sans avoir lu le plan 2D (`inputs.plans: []`). | **ÉLEVÉ (HARMFUL)** |
| **Adjacence Incomplète Déclarée Certifiée**| **0** | Apprend qu'un plan de 10 pièces ne possède qu'une seule porte (`living <-> kitchen`). | **MODÉRÉ (LOW_VALUE)** |
| **Confusion d'Axes IL3D (Y vs Z)** | **0** | Apprend à qualifier d'élévation verticale un décalage horizontal en profondeur. | **ÉLEVÉ (HARMFUL)** |

---

## 2. Recommandations Sanitaires Immédiates

1. **Purger ou isoler immédiatement les 10 exemples de surfaces calculées en coordonnées pixels non converties.**
2. **Exclure du jeu d'entraînement les 31 exemples de la Review Queue présentant un tableau `inputs.plans` vide.**
3. **Harmoniser les conventions de repères 3D entre générateurs et vérificateurs.**
