# ARCHI-AI — Audit de Couverture des Tâches & Compétences (`WAVE1_TASK_COVERAGE_AUDIT.md`)

> **Date d'audit :** 21 September 2026 à 15:00:00 UTC  
> **Auditeur Spécialiste :** Architecte Métier & Responsable Taxonomie ARCHI-AI  
> **Périmètre du Catalogue :** 69 tâches formelles (Groupes A à L), 17 compétences clés (Skills)  
> **Constat Majeur :** **Seules 22 tâches sur 69 sont représentées dans Wave 1 (31.9 % de couverture). 47 tâches ont strictement 0 exemple.**

---

## 1. Vue d'Ensemble de la Couverture des 69 Tâches

Alors que le rapport officiel de lancement affirmait une "couverture intégrale des cas d'usage réels", l'analyse du fichier `wave1_dataset.jsonl` démontre que le jeu pilote n'a couvert qu'un tiers des tâches prévues :

| Groupe de Tâches | Tâches au Catalogue | Tâches Couvertes | Tâches Absentes (0 ex) | Taux de Couverture | Volume d'Exemples Wave 1 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **A — Visual Understanding** | 7 | **1** | 6 | 14.3 % | 25 |
| **B — Floorplan (Plans 2D)** | 9 | **4** | 5 | 44.4 % | 144 |
| **C — Spatial / 3D** | 5 | **2** | 3 | 40.0 % | 150 |
| **D — BIM / IFC** | 6 | **2** | 4 | 33.3 % | 120 |
| **E — Ergonomie & Normes** | 5 | **2** | 3 | 40.0 % | 37 |
| **F — Matériaux & PBR** | 4 | **2** | 2 | 50.0 % | 110 |
| **G — Éclairage & HDRI** | 4 | **1** | 3 | 25.0 % | 80 |
| **H — Histoire & Design** | 5 | **2** | 3 | 40.0 % | 90 |
| **I — Critique Architecturale**| 6 | **1** | 5 | 16.7 % | 32 |
| **J — Professional Reasoning** | 6 | **2** | 4 | 33.3 % | 44 |
| **K — Pédagogie de Studio** | 5 | **1** | 4 | 20.0 % | 32 |
| **L — Multimodalité Croisée** | 7 | **2** | 5 | 28.6 % | 75 |
| **TOTAL** | **69 tâches** | **22 tâches** | **47 tâches** | **31.9 %** | **939 exemples** |

---

## 2. Inventaire Exhaustif des 47 Tâches Manquantes (0 Exemple)

L'audit liste formellement les 47 tâches du catalogue n'ayant fait l'objet d'aucune supervision dans Wave 1 :

### Groupe A — Visual Understanding (6 tâches manquantes sur 7)
- `FURNITURE_IDENTIFICATION` (A-1) : Reconnaissance fine du mobilier contemporain et classique.
- `STYLE_ANALYSIS` (A-3) : Détermination stylistique sur photographie intérieure.
- `MATERIAL_IDENTIFICATION` (A-4) : Identification visuelle des textures et finitions sur rendu photo.
- `VISUAL_LIGHTING_ANALYSIS` (A-5) : Analyse de la pénétration de la lumière naturelle sur image.
- `SPATIAL_RELATION_ANALYSIS` (A-6) : Relations visuelles de profondeur et perspectives.
- `IMAGE_ANALYSIS` (A-7) : Diagnostic général d'ambiance décorative.

### Groupe B — Floorplan (5 tâches manquantes sur 9)
- `DOOR_WINDOW_ANALYSIS` (B-12) : Diagnostic des sens d'ouverture de portes et des allèges de fenêtres.
- `FURNITURE_LAYOUT_ANALYSIS` (B-13) : Implantation du mobilier sur plan 2D.
- `PLAN_ERROR_DETECTION` (B-14) : Détection d'incohérences de dessin ou de cloisons aberrantes.
- `PLAN_SUMMARY` (B-15) : Synthèse globale du programme surfacique.
- `PLAN_TO_TEXT` (B-16) : Génération de notice descriptive à partir d'un plan d'étage.

### Groupe C — Spatial / 3D (3 tâches manquantes sur 5)
- `ROOM_OBJECT_REASONING` (C-19) : Analyse de cohabitation entre objets volumétriques.
- `SPATIAL_LAYOUT_ANALYSIS` (C-20) : Analyse de compacité et d'équilibre volumétrique.
- `3D_TO_TEXT` (C-21) : Descriptif spatial complet à partir d'un maillage 3D.

### Groupe D — BIM / IFC (4 tâches manquantes sur 6)
- `IFC_ENTITY_IDENTIFICATION` (D-22) : Identification des entités `IfcWall`, `IfcDoor`, `IfcWindow`.
- `IFC_PROPERTY_REASONING` (D-23) : Requêtes sur les Property Sets (`Pset_WallCommon`).
- `BIM_OBJECT_QUERY` (D-25) : Filtrage et quantitatifs d'objets BIM.
- `BIM_REASONING` (D-26) : Cohérence structurelle et réseaux CVC dans la maquette.

### Groupe E — Ergonomie (3 tâches manquantes sur 5)
- `FURNITURE_DIMENSION_REASONING` (E-28) : Hauteurs de tables, plans de travail, assises.
- `CIRCULATION_CHECK` (E-30) : Vérification continue de passages d'évacuation ERP.
- `ERGONOMIC_ANALYSIS` (E-31) : Évaluation posturale et confort gestuel de l'usager.

### Groupe F — Matériaux (2 tâches manquantes sur 4)
- `MATERIAL_ANALYSIS` (F-33) : Comportement acoustique et thermique des revêtements.
- `MATERIAL_COMPARISON` (F-34) : Comparaison technique (parquet contrecollé vs carrelage grès cérame).

### Groupe G — Éclairage (3 tâches manquantes sur 4)
- `LIGHTING_SCENARIO` (G-38) : Scénographie lumineuse (éclairage direct, indirect, rasant, d'accentuation).
- `DAYLIGHT_REASONING` (G-39) : Calcul du facteur lumière jour (FLJ).
- `ARTIFICIAL_LIGHTING_REASONING` (G-40) : Dimensionnement des flux lumineux (lumens, lux requis).

### Groupe H — Histoire & Style (3 tâches manquantes sur 5)
- `STYLE_COMPARISON` (H-41) : Confrontation critique Art Déco vs Modernisme vs Brutalisme.
- `STYLE_CLASSIFICATION` (H-42) : Classification d'une œuvre parmi les 40 styles référencés.
- `ARCHITECTURE_HISTORY` (H-44) : Monographies d'architectes et manifestes théoriques.

### Groupe I — Critique Architecturale (5 tâches manquantes sur 6)
- `DESIGN_PROBLEM_DETECTION` (I-47) : Repérage des impasses de circulation et pièces borgnes.
- `STRENGTH_IDENTIFICATION` (I-48) : Diagnostic valorisant les atouts majeurs d'un projet.
- `WEAKNESS_IDENTIFICATION` (I-49) : Identification pointue des défauts de spatialité.
- `IMPROVEMENT_PROPOSAL` (I-50) : Variantes d'optimisation sans modification structurelle.
- `ALTERNATIVE_DESIGN` (I-51) : Proposition de plans alternatifs pour un même plateau.

### Groupe J — Professional Reasoning (4 tâches manquantes sur 6)
- `REQUIREMENTS_ANALYSIS` (J-52) : Traduction d'un cahier des charges client en surfaces utiles.
- `FEASIBILITY_ANALYSIS` (J-54) : Faisabilité technique d'abattage de cloison ou création de trémie.
- `OPTION_COMPARISON` (J-56) : Comparaison objective de deux partis d'aménagement.
- `DESIGN_DECISION` (J-57) : Justification argumentée du parti architectural retenu.

### Groupe K — Pédagogie (4 tâches manquantes sur 5)
- `EXPLANATION` (K-58) : Explication didactique d'un concept spatial à un étudiant.
- `ERROR_EXPLANATION` (K-59) : Analyse bienveillante des erreurs d'échelle sur un rendu d'élève.
- `STUDIO_CRITIQUE` (K-61) : Conduite d'un échange d'atelier de projet de fin d'études.
- `METHODOLOGY_EXPLANATION` (K-62) : Transmission des étapes de la méthode de conception.

### Groupe L — Multimodalité Croisée (5 tâches manquantes sur 7)
- `IMAGE_PLUS_PLAN` (L-64), `PLAN_PLUS_TEXT` (L-66), `PLAN_PLUS_3D` (L-67), `IMAGE_PLUS_PLAN_PLUS_TEXT` (L-68), `BIM_PLUS_PLAN` (L-69).

---

## 3. Analyse de la Distribution des 17 Compétences (Skills)

| Compétence (Skill) | Exemples Wave 1 | % du Total | Statut Forensique |
| :--- | :---: | :---: | :--- |
| **`spatial_reasoning`** | 150 | 16.0 % | Surreprésenté (IL3D mono-source) |
| **`plan_reading`** | 112 | 11.9 % | Surreprésenté mais 70/112 sont des templates RPLAN |
| **`materials`** | 110 | 11.7 % | Bonne base, mais manque d'images réelles |
| **`lighting`** | 80 | 8.5 % | Répétitif (80x la même formulation d'ambiance) |
| **`multimodal_reasoning`**| 75 | 8.0 % | Fragilisé (25 fake multimodal, 50 examens MMMU) |
| **`BIM`** | 70 | 7.5 % | 100% template spatial containment théorique |
| **`IFC`** | 50 | 5.3 % | Excellent niveau technique (IFC-Bench QA) |
| **`design_history`** | 45 | 4.8 % | Excellent ancrage patrimonial (MoMA/Met) |
| **`style`** | 45 | 4.8 % | Bon ancrage matériaux historiques |
| **`problem_solving`** | 44 | 4.7 % | Fragile (32 inputs vides dans TRADEOFF_ANALYSIS) |
| **`critique`** | 32 | 3.4 % | Stéréotypé (32x le claustra ajouré) |
| **`pedagogical_explanation`**| 32 | 3.4 % | Artificiel (32 inputs vides dans GUIDED_REASONING) |
| **`topology`** | 27 | 2.9 % | Excellent (ResPlan connectivité déterministe) |
| **`visual_reasoning`** | 25 | 2.7 % | Sous-représenté |
| **`ergonomics`** | 25 | 2.7 % | Pollué par le bug `None m` |
| **`regulation`** | 12 | 1.3 % | **Critiquement sous-représenté** (Normes PMR/ERP) |
| **`circulation`** | 5 | 0.5 % | **Critiquement sous-représenté** (Cœur de métier) |

---

## 4. Risques Majeurs pour l'Entraînement & Plan de Rééquilibrage

1. **Biais de Circulation :** Avec seulement 5 exemples de `circulation` (0.5%) contre 150 exemples de `spatial_reasoning` 3D (16%), le modèle développerait une cécité sur la fluidité des flux piétons dans un appartement.
2. **Sur-apprentissage de Phrases Clichés :** Si les 70 exemples de plan matriciel ou les 32 exemples de claustra ajouré étaient entraînés tels quels, le modèle répéterait ces phrases comme des tics de langage dès qu'il verrait un plan.
3. **Plan d'Action :**
   - Écarter du training les 89 exemples `EXCLUDE` (inputs vides et faux multimodaux).
   - Reconfigurer les générateurs en Wave 2 pour cibler prioritairement les **47 tâches vierges**, avec un focus absolu sur les circulations (Groupe B), l'ergonomie (Groupe E) et la conformité réglementaire (Groupe J).
