# AXIS — Rapport de Maturité Scientifique Pré-Entraînement (`SCIENTIFIC_READINESS_REPORT.md`)

> **Phase :** PHASE 3 — Corpus Expansion & Scientific Readiness  
> **Auteur :** Lead Dataset Engineer, Multimodal Dataset Researcher & Forensic Auditor  
> **Date :** 2026-09-21  
> **Question Centrale :** *« Avons-nous actuellement une base scientifique suffisante pour passer à une première expérience d'entraînement ? »*  
> **Autorisation de Training :** **`INTERDICTION FORMELLE (TRAINING_ALLOWED: NO)`**  

---

## 1. Synthèse Globale des Travaux de la Phase 3

La Phase 3 a examiné avec une rigueur médico-légale les deux verrous scientifiques majeurs identifiés à l'issue de la Phase 2 :
1. **Le verrou de la rareté du vrai multimodal 2D $\leftrightarrow$ 3D (Problème A)** ;
2. **Le verrou de l'anomalie de calibration métrique de ResPlan (Problème B)**.

### 1.1. Résolution du Problème A (Paires 2D/3D dans le RAW)
- **Investigation exhaustive :** Les 66 847 fichiers du corpus RAW ont été audités par un détecteur à 4 niveaux (Identifiants, Structure, Géométrie, Sémantique).
- **Résultat irréfutable :** **Zéro nouvelle paire 2D Floorplan $\leftrightarrow$ 3D BIM cachée n'existe dans le RAW.**
- **Gisement réel :**
  - Le gisement de vrais plans d'architecte appariés à une maquette IFC est strictement borné à **10 unités** (`CORE_RESBIM_PAIRED`).
  - 20 projets IFC possèdent un rendu axonométrique/perspectif (`CORE_IFC_BENCH`), exploitables pour `IMAGE_PLUS_BIM` mais inaptes à la lecture de plan d'étage coté.
  - 2 592 trames RGB-D existent dans `CORE_STRUCTSCAN3D` pour la vision robotique subjective.
  - Toute tentative d'appariement artificiel entre RPLAN (2D) et IL3D (3D) a été formellement **rejetée** car arbitraire et scientifiquement indéfendable.

### 1.2. Résolution du Problème B (Calibration ResPlan)
- **Investigation forensique :** Audit des 17 000 plans vectoriels de `core/resplan/extracted/ResPlan.pkl`.
- **Preuve mathématique :** Chaque plan a été normalisé indépendamment sur un canevas arbitraire de dimension maximale 256.0. Le ratio surface de dessin / surface textuelle présente un écart-type de 173.2, et 32.1 % des plans présentent un `net_area` nul.
- **Décision :** Conformément à la règle *« Ne jamais inventer une conversion pixel $\to$ m² »*, `ResPlan.pkl` **échoue à la calibration métrique** et reste maintenu sous le statut strict **`QUARANTINED`** pour toute supervision de surfaces (m²) ou dimensions en mètres.
- **Capacités sûres :** 6 capacités purement topologiques et relationnelles (comptage de pièces, classification sémantique, graphe de connectivité, contiguïté, orientation relative) sont validées scientifiquement comme invariantes par échelle.

---

## 2. Évaluation de la Suffisance Scientifique pour l'Entraînement

### 2.1. Réponse Honnête et Détaillée
À la question fondamentale :
> *« Avons-nous maintenant suffisamment de données fiables pour commencer une première expérience d'entraînement scientifique ? »*

La réponse technique et rigoureuse est : **`CONDITIONAL` (CONDITIONNELLE)**.

#### Pourquoi la réponse n'est PAS un « OUI » inconditionnel :
- **Le volet multimodal 2D/3D (`BIM_PLUS_PLAN` et `PLAN_PLUS_3D`) N'EST PAS prêt pour un entraînement généraliste.** Entraîner un modèle sur 8 exemples d'entraînement et 2 exemples de test issus d'une unique typologie résidentielle relèverait du mirage expérimental. Le modèle mémoriserait les 8 appartements sans acquérir la moindre capacité de raisonnement architectural généralisable.
- **Le volet métrique m² N'EST PAS prêt sans calibration.** Entraîner le modèle sur des surfaces estimées ou inventées détruirait son bon sens physique.

#### Pourquoi la réponse n'est PAS un « NON » absolu :
- **Le socle unimodal compartimenté (Dataset A) est 100 % sain, propre et prêt pour un banc d'essai pilote :**
  - La lecture de plan raster et la topologie (`FLOORPLAN_READING`, `ROOM_TOPOLOGY`) reposent sur des vérités terrain déterministes.
  - Le raisonnement spatial 3D (`OBJECT_RELATION`, `CLEARANCE_CHECK`) dispose de 200 exemples vérifiés au millimètre près.
  - Les questions expertes BIM (`IFC_QA`) disposent de 1 026 paires rigoureusement vérifiées sur 21 projets réels.
  - Le Gold Set V3 (200 cas) et les 200 Hard Negatives fournissent un instrument d'évaluation contradictoire sans équivalent.

---

## 3. Conditions Impératives pour une Autorisation Future

Pour lever la conditionnelle et envisager un entraînement de production (`TRAINING_ALLOWED = YES`) :

1. **Acquisition P0 :** Intégrer au moins 50 à 100 nouvelles maquettes OpenBIM IFC avec plans d'étage associés sous licence permissive (MIT, CC-BY, Apache 2.0).
2. **Dérivation P1 :** Générer de manière déterministe des plans vectoriels cotés en millimètres à partir des entités `IfcWall` / `IfcSpace` des maquettes IFC pour résoudre définitivement la question métrique sans recourir à des pixels normalisés.
3. **Expérience Pilote A/B :** Réaliser le protocole d'ablation défini dans `ABLATION_DATASET_PLAN.md` (Dataset A vs Dataset C) avant tout scaling massif.

---

## 4. Décision Officielle du Gate

```text
==================================================
ARCHI-AI — SCIENTIFIC READINESS GATE
==================================================

MASTER DATASET:
PASS

SUPERVISION DATASET:
PASS_WITH_WARNINGS

MULTIMODAL PAIRS:
2622

CERTIFIED PAIRS:
2622 (10 BIM-Plan + 20 BIM-Image + 2592 RGB-D)

REVIEW PAIRS:
0

REJECTED PAIRS:
3 (Arbitrary cross-dataset pairings rejected)

TRUE MULTIMODAL EXAMPLES:
10 (BIM_PLUS_PLAN)

RESPLAN:
CALIBRATED: 0
QUARANTINED: 17000 (Metric tasks strictly prohibited)
SAFE NON-METRIC: 6 capabilities validated

FLOORPLANCAD:
LEGAL_REVIEW_REQUIRED

CORPUS GAPS:
- 2D Floorplan ↔ 3D BIM pairs critically limited (10 units)
- Photo ↔ Floorplan pairs absent from core (3 MMMU only)
- Metric uncalibrated pixels in RPLAN/ResPlan (0 calibrated 2D plans)
- Multi-option project variants absent (0 pairs)

NEW DATA REQUIRED:
YES (Specifically P0: 50-100 OpenBIM IFC pairs and P1: metric derived plans)

TRAINING DATA SCIENTIFICALLY SUFFICIENT:
CONDITIONAL (Ready for unimodal/pilot baseline; Insufficient for full multimodal generalist)

REMAINING RISKS:
- Overfitting on the 10 ResBIM units if multimodal training is forced prematurely
- Metric unit hallucination if ResPlan quarantine is violated
- Legal exposure if FloorPlanCAD quarantine is lifted without counsel

TRAINING_ALLOWED:
NO
==================================================
```
