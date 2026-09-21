# ARCHI-AI — Capacités Scientifiquement Sûres de ResPlan (`RESPLAN_SAFE_CAPABILITIES.md`)

> **Phase :** PHASE 3 — Corpus Expansion & Scientific Readiness  
> **Auteur :** Lead Dataset Engineer & Multimodal Dataset Researcher  
> **Date :** 2026-09-21  
> **Principe Directeur :** « Le fait qu'un plan ne soit pas métriquement calibré ne signifie pas que toutes ses informations soient inutilisables. Mais chaque capacité doit être validée séparément. »  

---

## 1. Cadre Scientifique de Validation Non-Métrique

Bien que `ResPlan.pkl` soit en quarantaine formelle pour toutes les tâches métriques (m², dimensions physiques), ses structures géométriques et ses graphes relationnels offrent des garanties mathématiques invariantes par échelle (invariance aux similitudes et homothéties).

Le tableau ci-dessous recense les 6 capacités formellement certifiées et leurs conditions d'exploitation :

| N° | Capacité Non-Métrique | Tâches Éligibles | Fondement Algorithmique | Garantie Scientifique | Statut de Validation |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **01** | **Inventaire & Comptage de Pièces** | `FLOORPLAN_READING` (#08), `ROOM_IDENTIFICATION` (#09) | Dénombrement déterministe des composantes connexes disjointes (`Polygon` / `MultiPolygon`). | Exactitude entière 100 % sur les polygones labellisés. | **`VALID_SAFE`** |
| **02** | **Taxonomie & Classification Spatiale** | `ROOM_IDENTIFICATION` (#09), `PLAN_TO_TEXT` (#16) | Étiquetage sémantique parmi 17 catégories (`living`, `bedroom`, `bathroom`, `kitchen`, `balcony`, `storage`, `stair`). | F1-Score > 0.95 (validé par modèle GraphGPS dans l'article ResPlan). | **`VALID_SAFE`** |
| **03** | **Graphe de Connectivité Topologique** | `ROOM_TOPOLOGY` (#10), `CIRCULATION_ANALYSIS` (#11) | Intersection géométrique `door ∩ room` et ouvertures franches (`via_door`, `direct`). | Topologie exacte d'accessibilité sans référence métrique. | **`VALID_SAFE`** |
| **04** | **Graphe de Contiguïté (Adjacence)** | `ROOM_TOPOLOGY` (#10), `SPATIAL_RELATION_ANALYSIS` (#07) | Buffer géométrique (`wall_gap`) détectant les pièces partageant une cloison séparative. | Relations spatiales de voisinage invariantes par homothétie. | **`VALID_SAFE`** |
| **05** | **Orientation Relative & Gisement** | `SPATIAL_RELATION_ANALYSIS` (#07), `DAYLIGHT_REASONING` (#39) | Calcul du gisement angulaire ($\theta = \text{atan2}(\Delta y, \Delta x)$) entre centroïdes de pièces. | Orientation relative et ordre spatial préservés à 100 %. | **`VALID_SAFE`** |
| **06** | **Détection de Conflits Topologiques** | `DESIGN_PROBLEM_DETECTION` (#49), `PLAN_ERROR_DETECTION` (#14) | Détection de pièces aveugles, accès direct inopportun (ex: WC ouvrant directement sur séjour/cuisine). | Règles de composition spatiale indépendantes de l'échelle métrique. | **`VALID_SAFE`** |

---

## 2. Capacités Strictement Prohibées sur ResPlan

Les capacités suivantes sont formellement interdites sur tout asset ResPlan :

```text
==================================================
CAPACITÉS STRICTEMENT PROHIBÉES SUR RESPLAN
==================================================
[PROHIBÉ] PLAN_SUMMARY (Surfaces globales ou partielles en m²)
[PROHIBÉ] Cotes linéaires en mètres (longueur, largeur d'une pièce)
[PROHIBÉ] Vérification de largeur réglementaire de dégagement PMR (ex: >= 0.90 m ou 1.40 m)
[PROHIBÉ] Calcul de ratio de vitrage (surface baie / surface pièce)
[PROHIBÉ] Évaluation de respect de surfaces minimales habitables CCH (ex: chambre >= 9 m²)
==================================================
```

---

## 3. Recommandations d'Intégration Future

1. **Branche Isolée :** Créer une branche de supervision spécifique `dataset/supervision/v1_resplan_topological/` strictement bornée aux tâches `ROOM_TOPOLOGY` et `ROOM_IDENTIFICATION`.
2. **Clause de Non-Métrique (`UNKNOWN`) :** Dans chaque consigne et réponse issue de ResPlan, imposer un tag formel :
   `[SCALE_STATUS: UNCALIBRATED_NORMALIZED_CANVAS]`.
3. **Maintien de la Quarantaine en Production :** Tant que cette séparation stricte n'est pas scellée dans un pipeline de données dédié, `ResPlan.pkl` reste exclu du split d'entraînement de base pour éviter toute contamination des notions de dimension physique.
