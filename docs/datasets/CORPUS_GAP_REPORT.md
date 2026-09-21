# ARCHI-AI — Rapport Forensique des Lacunes du Corpus (`CORPUS_GAP_REPORT.md`)

> **Phase :** PHASE 3 — Corpus Expansion & Scientific Readiness  
> **Auteur :** Lead Dataset Engineer & Forensic Dataset Auditor  
> **Date :** 2026-09-21  
> **Objectif :** Dresser l'inventaire exhaustif et chiffré des déficits de données séparant le corpus actuel d'un entraînement complet.  

---

## 1. Synthèse des Lacunes Critiques du Corpus

L'audit croisé entre le catalogue des 69 tâches de supervision et les actifs physiques certifiés dans le Master Dataset v2 met en évidence **6 lacunes structurelles majeures** :

| N° | Lacune Identifiée | Tâches Bloquées | Couverture Actuelle | État dans le RAW | Gravité pour le Pré-Entraînement |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **GAP 1** | **Pénurie de paires 2D Plan $\leftrightarrow$ 3D BIM** | `BIM_PLUS_PLAN` (#68), `PLAN_PLUS_3D` (#65) | 10 paires (1 typologie) | Aucune paire supplémentaire trouvée | **`CRITIQUE` (Bloquant VLM Multimodal)** |
| **GAP 2** | **Absence de couplage Photo $\leftrightarrow$ Plan 2D** | `IMAGE_PLUS_PLAN` (#63) | 3 paires (MMMU) | Aucun gisement dans le CORE | **`ÉLEVÉE` (Tâche non entraînable)** |
| **GAP 3** | **Absence de plans 2D métriquement calibrés** | `PLAN_SUMMARY` (#15), `CIRCULATION_CHECK` (#30) | 0 plan coté certifié | RPLAN non coté, ResPlan en quarantaine | **`CRITIQUE` (Risque d'hallucination de m²)** |
| **GAP 4** | **Absence de triplets Photo + Plan + Programme** | `IMAGE_PLUS_PLAN_PLUS_TEXT` (#67) | 3 cas isolés | Insuffisant pour la généralisation | **`MOYENNE` (Tâche complexe de synthèse)** |
| **GAP 5** | **Absence de variantes de projet sur même site** | `OPTION_COMPARISON` (#56), `ALTERNATIVE_DESIGN` (#51) | 0 paire de variantes | Aucun doublet 'Variante A vs B' | **`MODÉRÉE` (Comparaison multi-options)** |
| **GAP 6** | **Quarantaine légale FloorPlanCAD** | Corpus vectoriel CAD (741 fichiers) | 0 fichier dans le CORE | 741 fichiers isolés sous `LEGAL_REVIEW_REQUIRED` | **`JURIDIQUE` (Blocage de réintégration)** |

---

## 2. Dataset Value Analysis (Analyse Multidimensionnelle de Valeur)

Conformément à la Section 20 du mandat, chaque lacune est évaluée selon ses dimensions objectives d'impact, de risque et de faisabilité :

### GAP 1 : Paires 2D Floorplan $\leftrightarrow$ 3D OpenBIM IFC
- **CURRENT_COVERAGE :** 10 paires résidentielles (20 fichiers).
- **EXPECTED_GAIN :** Très élevé. Permet l'alignement multimodal réel entre conventions de dessin 2D et géométrie paramétrique 3D (cœur de valeur d'ARCHI-AI).
- **COST :** Moyen. Nécessite la sélection et l'extraction de 50 à 100 maquettes IFC open-source avec plans associés.
- **RISK :** Faible si les sources sont openBIM natives (licences CC-BY ou MIT).
- **LICENSE_COMPLEXITY :** Faible à moyenne (vérification des clauses d'attribution).
- **TRAINING_IMPACT :** **DÉCISIF.** Sans cette extension, le modèle ne peut apprendre de raisonnement BIM/Plan généralisable.

### GAP 2 : Paires Photo Intérieure $\leftrightarrow$ Plan 2D d'Étage
- **CURRENT_COVERAGE :** 3 exemples (MMMU).
- **EXPECTED_GAIN :** Élevé. Permet le repérage de cône de vue, l'identification de pièces à partir d'une photo et la vérification de cohérence d'aménagement.
- **COST :** Élevé. Nécessite des datasets avec poses caméra étalonnées (ex: Matterport3D, Structured3D, Gibson).
- **RISK :** Élevé. La majorité de ces datasets ont des clauses restrictives (Non-Commercial, Recherche fermée).
- **LICENSE_COMPLEXITY :** **TRÈS ÉLEVÉE.** Risque d'incompatibilité avec un déploiement industriel.
- **TRAINING_IMPACT :** Secondaire par rapport au cœur BIM/Plan.

### GAP 3 : Plans Vectoriels 2D Métriquement Étalonnés (avec cotation réelle)
- **CURRENT_COVERAGE :** 0 plan (RPLAN est un raster matriciel 256×256; ResPlan est normalisé artificiellement à [0, 256]).
- **EXPECTED_GAIN :** Majeur. Débloque l'apprentissage rigoureux des surfaces réelles (m²), des largeurs de dégagements PMR et des ratios d'habitabilité CCH.
- **COST :** Faible à moyen. Peut être dérivé de maquettes IFC existantes (génération automatique de plans vectoriels cotés en SVG/DXF à partir d'IFC via `ifcopenshell`).
- **RISK :** Nul (la génération est 100 % déterministe et conserve l'échelle physique en millimètres).
- **LICENSE_COMPLEXITY :** Nulle (dérivé direct d'IFC déjà sous licence permissive).
- **TRAINING_IMPACT :** **MAJEUR.** Éradique définitivement le risque d'hallucination métrique.

---

## 3. Statut Spécifique de FloorPlanCAD

- Les 741 fichiers présents dans `core/floorplancad/` demeurent sous le statut formel :
  ```text
  FLOORPLANCAD STATUS: LEGAL_REVIEW_REQUIRED
  ```
- **Règle Absolue (Section 19) :** Aucun fichier de FloorPlanCAD n'a été réintroduit dans le Master Dataset v2 ou dans la supervision.
- Ces données restent exclues de tout split d'apprentissage tant qu'un avis juridique formel n'aura pas certifié la compatibilité de leurs conditions de diffusion.
