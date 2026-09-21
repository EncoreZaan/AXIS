# ARCHI-AI — Analyse de Couverture Multimodale (`MULTIMODAL_COVERAGE_ANALYSIS.md`)

> **Phase :** PHASE 3 — Corpus Expansion & Scientific Readiness  
> **Auteur :** Multimodal Dataset Researcher & Experimental Design Engineer  
> **Date :** 2026-09-21  
> **Objectif :** Cartographier précisément la couverture des tâches multimodales et identifier les points de blocage scientifique réels.  

---

## 1. Cartographie de Couverture par Tâche Multimodale

Le catalogue ARCHI-AI définit 7 tâches multimodales directes (croisement d'au moins deux modalités physiques distinctes) parmi ses 69 tâches. Le tableau ci-dessous dresse l'état exact de leur couverture sur la base du corpus certifié actuel :

| Task ID | Intitulé de la Tâche | Modalités Requises | Paires Disponibles | Exemples Uniques Réalisables | Statut de Couverture | Impact sur l'Entraînement |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **`BIM_PLUS_PLAN` (#68)** | Confrontation Maquette IFC et Plan Étage | `PLAN_2D` + `IFC_3D` | 10 | 10 à 30 max | **`LIMITED`** | **Goulot d'étranglement critique.** 10 unités résidentielles ne permettent pas d'apprendre la variabilité architecturale (bureaux, ERP, hôpitaux). |
| **`PLAN_PLUS_3D` (#65)** | Appariement Plan 2D et Géométrie 3D | `PLAN_2D` + `3D_MESH_IFC` | 10 | 10 à 20 max | **`LIMITED`** | **Goulot critique.** Même limitation que `BIM_PLUS_PLAN`. Risque de mémorisation des 10 plans. |
| **`IMAGE_PLUS_PLAN` (#63)** | Confrontation Image Intérieure et Plan 2D | `IMAGE_PHOTO` + `PLAN_2D` | 3 (MMMU) | 3 | **`UNMET`** | **Bloquant.** Aucun dataset de localisation de point de vue ou confrontation photo-plan n'est présent dans le CORE. |
| **`IMAGE_PLUS_TEXT` (#66)** | Image Intérieure et Affirmation Technique | `IMAGE_PHOTO` + `TEXT_CLAIM` | 107 images | ~50 | **`MODERATE`** | **Partiellement couvert.** Faux multimodal évité grâce au test de détection de divergence / discordance stricte. |
| **`IMAGE_PLUS_PLAN_PLUS_TEXT` (#67)** | Triplet Image + Plan + Programme Textuel | `IMAGE` + `PLAN` + `TEXT` | 3 (MMMU) | 3 | **`CRITICAL_GAP`** | **Bloquant.** Impossibilité statistique d'entraîner une tâche complexe à 3 modalités sur 3 exemples. |
| **`IFC_QA` (#27)** | Questions / Réponses Expertes sur Maquette BIM | `IFC_MODEL` + `QA_TEXT` | 21 projets | 1 026 QA vérifiées | **`ROBUST`** | **Prêt scientifiquement.** Couverture complète d'extraction de métriques réelles, quantitatifs et disciplines. |
| **`BIM_REASONING` (#26)** | Coordination Multidisciplinaire BIM | `IFC_MULTI_DISCIPLINE` | 6 projets | ~40 | **`MODERATE`** | **Couverture partielle.** 6 projets multi-disciplines (`mep.ifc`, `str.ifc`, `heating.ifc`) exploitables. |

---

## 2. Analyse de Volume & Règle Anti-Surgénération

### 2.1. Pourquoi 10 Paires ne Peuvent Pas Être Multipliées Artificiellement
- Dans le pipeline Phase 2, chaque paire a généré exactement 1 exemple supervisé (`BIM_PLUS_PLAN`), soit 10 exemples.
- Même en décomposant les angles d'analyse (alignement des baies, détection de cloisons non modélisées, conformité des désignations spatiales), une même unité `unit_XXX` ne peut légitimement produire plus de **2 à 3 requêtes réellement indépendantes**.
- Multiplier artificiellement les questions (par reformulation lexicale ou variations de synonymes) sur ces 10 unités :
  1. violerait la **Règle 22** (*Interdiction de multiplier artificiellement les exemples à partir d'un même asset*) ;
  2. créerait un surapprentissage massif sur la signature géométrique des 10 appartements de `CORE_RESBIM_PAIRED` ;
  3. masquerait la pauvreté réelle de la distribution architecturale sous un faux volume de données.

### 2.2. Répartition par Split des 10 Unités Actuelles
Conformément au scellement anti-fuite (`project_group_id`) :
- **Train split :** 8 unités (`unit_001`, `unit_002`, `unit_003`, `unit_005`, `unit_010`, `unit_100`, `unit_101`, `unit_102`) $\rightarrow$ 8 exemples.
- **Validation split :** 0 unité.
- **Test / Holdout split :** 2 unités (`unit_000`, `unit_004`) $\rightarrow$ 2 exemples.

**Constat scientifique formel :**  
Entraîner un VLM multimodal avec seulement **8 exemples en train** et **2 exemples en test** pour la tâche `BIM_PLUS_PLAN` est statistiquement indéfendable et mènerait à un échec de généralisation garanti.

---

## 3. Synthèse des Tâches Bloquantes pour le Pré-Entraînement

1. **L'apprentissage du multimodal 2D/3D (`BIM_PLUS_PLAN` et `PLAN_PLUS_3D`) est actuellement bloqué par le manque de diversité physique.** Il nécessite un apport de paires certifiées supplémentaires d'au moins 50 à 100 unités diversifiées (logements collectifs, maisons individuelles, tertiaire).
2. **L'apprentissage de la relation Photo $\leftrightarrow$ Plan (`IMAGE_PLUS_PLAN`) est totalement vacant.**
3. **En revanche, les tâches unimodales BIM (`IFC_QA`), plan 2D (`FLOORPLAN_READING`, `ROOM_TOPOLOGY`) et perception 3D (`OBJECT_RELATION`, `CLEARANCE_CHECK`) disposent d'un volume et d'une diversité scientifiquement exploitables pour un premier pilote contrôlé.**
