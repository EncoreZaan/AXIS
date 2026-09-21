# ARCHI-AI — Décision du Pre-Training Gate (`PRE_TRAINING_GATE.md`)

> **Statut Officiel du Gate :** **RED**  
> **Niveau de Confiance Sanitaire :** **HAUTE RIGUEUR (Audit Red Team)**  
> **Autorisation de Fine-Tuning :** **INTERDICTION FORMELLE**

---

## 1. Justification Red Team de la Décision

Le statut du Pre-Training Gate est évalué à : **RED**.

### Motifs de la Décision :
1. **Anomalie de Grandeur sur Floorplans (Bloquant pour GREEN) :** Des surfaces brutes exprimées en pixels (ex: 18 806 px²) sont étiquetées en m² dans plusieurs exemples de Wave 1 Repaired. Un modèle entraîné sur ces données hallucinerait des ordres de grandeur grotesques.
2. **Dépendance Multimodale Incomplète (Bloquant pour GREEN) :** Les exemples de `PLAN_PLUS_TEXT` de la Review Queue ont un champ `inputs.plans` vide et des analyses répétitives par gabarits.
3. **Contamination du Gold Set V2 (Bloquant pour GREEN) :** Les exemples du Gold Set V2 étaient tagués `"split": "train"`, rendant toute évaluation circulaire sans le holdout indépendant que nous venons d'isoler.
5. **Pourquoi le statut RED est impératif :** Le taux de grounding effectif (19.6 %), les anomalies de surface sur les plans (38.5 % des floorplans affectés par des pixels étiquetés en m²), le fake multimodal (21.2 %) et la contamination du Gold Set (79.5 %) interdisent formellement tout apprentissage sous peine de détériorer cognitivement le modèle par des réflexes d'hallucination.

---

## 2. Conditions Impératives Avant Tout Micro-Fine-Tuning

Pour faire passer le Gate au statut **GREEN** :
- [ ] **Correction du convertisseur ResPlan :** Convertir les surfaces de pixels en mètres carrés réels à l'aide de l'échelle ou exclure ces exemples.
- [ ] **Purge de la Review Queue :** Renseigner le plan réel pour `PLAN_PLUS_TEXT` ou déclasser la tâche en tâche textuelle unimodale.
- [ ] **Sanctuarisation du Holdout :** Utiliser exclusivement le holdout créé dans `dataset/master/v1/supervision/holdout/`.
- [ ] **Filtrage des données HARMFUL :** Exclure du split `train` les 41 exemples identifiés comme nocifs.

---

## 3. Règle d'Arrêt
**AUCUN ENTRAÎNEMENT N'EST DÉCLENCHÉ.**  
Le pipeline reste au repos complet en attente de la décision utilisateur.
