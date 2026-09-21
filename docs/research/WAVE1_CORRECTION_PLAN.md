# ARCHI-AI — Plan d'Action & de Correction : Wave 1 (`WAVE1_CORRECTION_PLAN.md`)

> **Date d'élaboration :** 21 September 2026 à 15:05:00 UTC  
> **Statut :** PLAN D'ACTION OPÉRATIONNEL & PROTOCOLE QUALITÉ  
> **Principe Recteur :** Zéro correction aveugle, traçabilité intégrale, non-altération de RAW, aucun entraînement prématuré.  

---

## 1. Synthèse de l'Arbitrage Qualité sur Wave 1

L'audit approfondi classe les 939 exemples de Wave 1 selon 4 statuts d'exploitation stricts :

| Statut Qualité | Volume d'Exemples | % du Dataset | Action Opérationnelle |
| :--- | :---: | :---: | :--- |
| **`RETAIN`** | **409** | **43.6 %** | **Conservés pour le fine-tuning.** Exemples grounded, précis et authentiques. |
| **`CORRECT`** | **25** | **2.7 %** | **Correction automatisable déterministe.** Calcul de `normalized_value` en m. |
| **`REVIEW`** | **416** | **44.3 %** | **Mis en attente d'enrichissement.** Templates répétitifs ou QA hors cible. |
| **`EXCLUDE`** | **89** | **9.5 %** | **Exclus définitivement du training.** Inputs vides ou FAKE_MULTIMODAL. |
| **TOTAL** | **939** | **100.0 %** | **Audit exhaustif et cloisonné.** |

---

## 2. Corrections Déterministes Immédiates (`CORRECT` — 25 Exemples)

### Problème Identifié :
Dans la tâche `CLEARANCE_CHECK` (`CORE_ERGONOMIE`), 25 exemples contiennent la chaîne `(soit None m)` suite à une omission de calcul dans `ErgonomicsGenerator`. La cote originale est présente et exacte (ex: 90 cm), mais la conversion métrique n'a pas été exécutée.

### Protocole de Réparation :
1. Calculer `normalized_value = round(original_value / 100.0, 2)` pour toute valeur en centimètres.
2. Mettre à jour `ground_truth.normalized_value`.
3. Remplacer dans le texte de la réponse `(soit None m)` par `(soit {normalized_value} m)`.
4. Réaligner la difficulté déclarée de `L3_ANALYSE` vers `L1_RECONNAISSANCE` (ou `L2_COMPREHENSION`), conformément aux conclusions du rapport de difficulté.

---

## 3. Traitement des Exclus (`EXCLUDE` — 89 Exemples)

Les 89 exemples suivants ne doivent **en aucun cas être intégrés à un run de fine-tuning** :
1. **25 exemples de `IMAGE_PLUS_TEXT` (Groupe L) :** Fausse multimodalité (`FAKE_MULTIMODAL`). L'objet `inputs` ne comporte pas de document textuel, alors que la réponse prétend évaluer la conformité à des fiches descriptives.
2. **32 exemples de `TRADEOFF_ANALYSIS` (Groupe J) :** Conteneur `inputs` entièrement vide (`{}`).
3. **32 exemples de `GUIDED_REASONING` (Groupe K) :** Conteneur `inputs` entièrement vide (`{}`).

*Ces exemples seront déplacés vers une archive de quarantaine `dataset/master/v1/supervision/quarantine/` sans suppression physique.*

---

## 4. Traitement de la File de Revue (`REVIEW` — 416 Exemples)

Les 416 exemples placés en `REVIEW` présentent une valeur documentaire réelle mais un niveau de template ou d'inadéquation trop élevé pour être entraînés en l'état :
1. **70 exemples RPLAN `FLOORPLAN_READING` :** Réécrire le générateur pour injecter les vrais noms de pièces et les masques de segmentation RPLAN au lieu du texte générique.
2. **70 exemples buildingSMART `BIM_SPATIAL_HIERARCHY` :** Parser réellement les entités `IfcBuildingStorey` du fichier IFC pour lister les vrais noms d'étages et hauteurs sous plafond.
3. **75 exemples IL3D `OBJECT_RELATION` :** Calculer la distance euclidienne réelle $d = \sqrt{(x_1-x_2)^2 + (y_1-y_2)^2 + (z_1-z_2)^2}$ avant d'affirmer une relation de proximité ou de vis-à-vis.
4. **32 exemples ResPlan `PROJECT_CRITIQUE` :** Contextualiser la critique à partir de l'analyse réelle des surfaces et de la position de la porte d'entrée.
5. **80 exemples PolyHaven `LIGHTING_ANALYSIS` & 55 ex `MATERIAL_APPLICATION` :** Diversifier les structures syntaxiques et relier la lumière à une pièce type.
6. **34 exemples WARNING (33 MMMU Architecture + 1 Normes FR) :** Les 33 exemples MMMU de génie civil/géodésie doivent être réévalués quant à leur pertinence pour un modèle d'architecture intérieure pure.

---

## 5. Renforcement Architectural du Supervision Engine

Le Supervision Engine est désormais doté de 7 validateurs dans son Quality Gate :
1. `ReferenceValidator`
2. `HallucinationValidator`
3. `EpistemicValidator`
4. `AntiSycophancyValidator`
5. **`GenericAnswerValidator`** (Nouveau — Détection clichés & placeholders)
6. **`MultimodalDependencyValidator`** (Nouveau — Détection `FAKE_MULTIMODAL` & inputs vides)
7. **`DifficultyValidator`** (Nouveau — Calibration cognitive L1-L6)

Ces validateurs interdiront structurellement à toute future génération (Wave 2) de produire des exemples non ancrés, stéréotypés ou orphelins de données d'entrée.
