# AXIS — Forensic Data Capability Audit (`DATA_CAPABILITY_AUDIT.md`)

> **Audit Identifier:** `RUN-021-DATA-CAPABILITY-AUDIT`  
> **Date:** 2026-09-23  
> **Auditor:** AXIS Dataset Engineering & Scientific Preparation Agent  
> **Operational Invariants:** `TRAINING_ALLOWED: NO` | `TRAINING_MAY_BEGIN: NO`

---

## 1. Executive Summary & Forensic Discovery

Phase 5 (`RUN-020-SCIENTIFIC-GENERALIZATION`) established that the previous supervision protocol in `RUN-019` produced near-zero visual grounding:
- The model generated the canonical 5-section critique with 92.0% similarity on 100% black images and 90.6% on uniform noise.
- 100% of tested responses contained hallucinated numerical IDs memorized during training.
- The training loss minimization was driven by **template memorization** rather than multimodal visual understanding.

To rectify this, this forensic audit physically examines the raw data of authorized sources (`CORE_RPLAN` and `CORE_RESBIM_PAIRED`) to identify what spatial and geometric signals are genuinely available, what signals are absent, and what can be rigorously derived as ground truth without fabricating data.

---

## 2. Forensic Signal Capability Matrix

In accordance with Phase 6A Protocol §6, every potential architectural and spatial signal is classified into:
- **`AVAILABLE`**: Signal physically present or mathematically computable from certified raw data.
- **`NOT_AVAILABLE`**: Signal absent from the source files.
- **`PARTIAL`**: Signal present for a subset of assets or with constrained fidelity.
- **`UNRELIABLE`**: Signal cannot be used as ground truth without unverified assumptions.

| Signal | Source | Statut Disponibilité | Fiabilité | Statut Utilisabilité | Rationale & Preuve Forensic |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Images matricielles 2D** | RPLAN | **AVAILABLE** | ÉLEVÉE | **SOURCE_GROUND_TRUTH** | 15 000 plans PNG 256x256 px (`rplan_dataset.zip`). SHA-256 vérifié. |
| **Labels textuels de pièces** | RPLAN | **NOT_AVAILABLE** | NULLE | **NOT_USABLE** | La distribution `metindeder/rplan-floorplan-edited` utilise un prompt ControlNet uniforme pour 100% des plans. Zéro label sémantique (séjour, cuisine, etc.). |
| **Masques/Régions de pièces** | RPLAN | **AVAILABLE** | ÉLEVÉE | **DERIVED_GROUND_TRUTH** | Composantes connexes des pixels blancs `[255, 255, 255]`. Découpage topologique net. |
| **Boîtes englobantes (BBoxes)**| RPLAN | **AVAILABLE** | ÉLEVÉE | **DERIVED_GROUND_TRUTH** | Calculées déterministement $[ymin, xmin, ymax, xmax]$ par composante connexe ($\ge 50$ px). |
| **Centres de gravité (Centroids)**| RPLAN | **AVAILABLE** | ÉLEVÉE | **DERIVED_GROUND_TRUTH** | Moyenne arithmétique $(\bar{x}, \bar{y})$ des coordonnées des pixels de chaque pièce. |
| **Aires des pièces (px)** | RPLAN | **AVAILABLE** | ÉLEVÉE | **DERIVED_GROUND_TRUTH** | Nombre exact de pixels blancs par composante connexe. |
| **Géométrie des parois (Murs)**| RPLAN | **AVAILABLE** | ÉLEVÉE | **DERIVED_GROUND_TRUTH** | Masque des pixels rouges `[255, 0, 0]` délimitant les pièces et l'enveloppe extérieure. |
| **Géométrie des portes (Baies)**| RPLAN | **AVAILABLE** | ÉLEVÉE | **DERIVED_GROUND_TRUTH** | Composantes connexes des pixels verts `[0, 255, 0]`. Centroïdes et emprises calculables. |
| **Géométrie des fenêtres** | RPLAN | **NOT_AVAILABLE** | NULLE | **NOT_USABLE** | Aucune fenêtre distincte n'est encodée dans la palette RPLAN 4 couleurs. |
| **Connectivité pièce-porte** | RPLAN | **AVAILABLE** | ÉLEVÉE | **DERIVED_GROUND_TRUTH** | Dilation morphologique $r=2$ px des portes intersectant les pièces adjacentes. |
| **Adjacence murale (Mitoyenneté)**| RPLAN | **AVAILABLE** | ÉLEVÉE | **DERIVED_GROUND_TRUTH** | Dilation $r=3$ px des pièces à travers la cloison rouge intersectant une pièce voisine. |
| **Relations directionnelles** | RPLAN | **AVAILABLE** | ÉLEVÉE | **DERIVED_GROUND_TRUTH** | `LEFT_OF`, `RIGHT_OF`, `ABOVE`, `BELOW` calculées selon vecteurs d'offset normalisés. |
| **Relations extrémales** | RPLAN | **AVAILABLE** | ÉLEVÉE | **DERIVED_GROUND_TRUTH** | `NEAREST_TO`, `FARTHEST_FROM`, `LARGEST_ROOM`, `SMALLEST_ROOM`. |
| **Distance métrique (mètres)** | RPLAN | **NOT_AVAILABLE** | NULLE | **PROHIBITED** | Coordonnées de raster 256x256 px sans échelle métrique physique certifiée. Interdiction absolue d'inventer des mètres. |
| **Distance pixel (euclidienne)**| RPLAN | **AVAILABLE** | ÉLEVÉE | **DERIVED_GROUND_TRUTH** | $d(c_A, c_B) = \sqrt{\Delta x^2 + \Delta y^2}$ exprimée rigoureusement en pixels. |
| **Graphe de pièces (Room Graph)**| RPLAN | **AVAILABLE** | ÉLEVÉE | **DERIVED_GROUND_TRUTH** | Graphe formel $G = (V, E)$ : $V = \{\text{pièces}\}$, $E = \{\text{portes}\}$. |
| **Dessins 2D haute résolution**| ResBIM | **AVAILABLE** | ÉLEVÉE | **SOURCE_GROUND_TRUTH** | 10 plans JPEG d'architecte (7572x4189 px) appariés aux maquettes IFC. |
| **Entités IfcSpace** | ResBIM | **NOT_AVAILABLE** | NULLE | **NOT_USABLE** | L'inspection physique des 10 maquettes IFC montre 0 entité `IfcSpace`. |
| **Entités IfcWall** | ResBIM | **AVAILABLE** | ÉLEVÉE | **SOURCE_GROUND_TRUTH** | 12 à 18 parois par modèle IFC (ex: `Basiswand:Wall-Ext...`). |
| **Entités IfcDoor** | ResBIM | **AVAILABLE** | ÉLEVÉE | **SOURCE_GROUND_TRUTH** | 5 à 6 portes par modèle, cotes physiques millimétriques réelles (1010x2110 mm). |
| **Entités IfcWindow** | ResBIM | **AVAILABLE** | ÉLEVÉE | **SOURCE_GROUND_TRUTH** | 4 fenêtres par modèle avec cotes d'ouverture. |
| **Calibration pixel ↔ mètre 2D/3D**| ResBIM| **NOT_AVAILABLE** | NULLE | **PROHIBITED** | Aucun fichier de transformation affine ou matrice de projection 2D/3D n'est distribué. |

---

## 3. Analyse Forensique Détaillée

### 3.1 Découverte Critique sur CORE_RPLAN
Dans `metindeder/rplan-floorplan-edited`, les métadonnées textuelles associées à chaque image consistent en une phrase unique répétée 15 000 fois :
```json
{"text": "an architectural floorplan layout with green doors, red walls, and white rooms on a gray background"}
```
Les labels sémantiques initiaux du papier R-PLAN (Bao et al., ICCV 2019) ayant été expurgés lors de la préparation ControlNet par l'auteur amont, **aucun nom de pièce fonctionnel (salon, cuisine, chambre) n'existe dans cette distribution**.
C'est précisément cette absence qui avait conduit l'ancien générateur `floorplan_gen.py` (ligne 40) à déclencher le fallback vers un paragraphe descriptif générique :
```python
if not rooms and visual:
    # émission du template statique canonique "Document matriciel raster..."
```
Ce fallback a provoqué la pathologie de RUN-019 : une minimisation artificielle de la loss par récitation de prose architecturale sans aucun ancrage visuel.

### 3.2 Solution Méthodologique Phase 6A : Référence Spatiale Déterministe
Plutôt que d'inventer des labels sémantiques ou d'utiliser un modèle pour prédire des noms de pièces (ce qui violerait la Règle §7 interdisant le pseudo-ground truth), la Phase 6A référence chaque pièce de façon **strictement géométrique et spatiale** :
1. **Ancrage par Boîte Englobante / Coordonnées :**
   Exemple : "Considérez la pièce délimitée par la boîte $[ymin, xmin, ymax, xmax]$..."
2. **Ancrage par Position Relative / Extrémale :**
   Exemple : "Considérez la pièce située dans l'angle supérieur gauche...", "Considérez la pièce de plus grande surface...", "Considérez le nœud central distribuant le plus de portes...".
3. **Ancrage Topologique :**
   Exemple : "Combien de pièces sont directement connectées par une porte à la pièce $R_1$ ?"

Cette formulation garantit que :
- La tâche est **100% VISUAL_REQUIRED** : impossible de répondre sans analyser la disposition des pixels de l'image.
- Le ground truth est **100% DERIVED_GROUND_TRUTH** calculé mathématiquement à partir des masques physiques réels.

### 3.3 Statut Forensique de CORE_RESBIM_PAIRED
ResBIM fournit 10 paires authentiques dessin 2D JPEG ↔ maquette 3D IFC. L'audit forensic par `ifcopenshell` démontre :
- Absence totale d'`IfcSpace` (les volumes d'ambiance n'ont pas été modélisés dans Revit avant export IFC).
- Présence certifiée des éléments constructifs physiques : `IfcWall`, `IfcDoor`, `IfcWindow`.
- Dimensions millimétriques réelles des menuiseries (`SOURCE_GROUND_TRUTH`).
- Absence de matrice de calibration affine entre le raster 7572x4189 px et le repère IFC. Toute régression de cotes métriques sur le dessin 2D est donc interdite.
