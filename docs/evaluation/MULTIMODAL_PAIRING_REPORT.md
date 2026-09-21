# ARCHI-AI — Rapport Forensique d'Appariement Multimodal 2D/3D (`MULTIMODAL_PAIRING_REPORT.md`)

> **Phase :** PHASE 3 — Corpus Expansion & Scientific Readiness  
> **Auteur :** Lead Dataset Engineer & Forensic Dataset Auditor  
> **Date :** 2026-09-21  
> **Périmètre d'audit :** Exploration exhaustive du corpus RAW existant (`dataset/raw/external/core/`)  
> **Statut Final :** AUDIT RÉALISÉ — AUCUNE PAIRE CACHÉE DÉCOUVRABLE SANS HALLUCINATION  

---

## 1. Synthèse Exécutive

L'audit forensique multi-niveaux a passé au crible l'ensemble des 66 847 fichiers du corpus RAW pour identifier d'éventuelles correspondances implicites entre représentations 2D (plans d'architecte, dessins matriciels, images de synthèse) et modélisations 3D (maquettes IFC OpenBIM, agencements spatiaux, nuages de points/profondeur).

```text
==================================================
MULTIMODAL PAIRING AUDIT SUMMARY
==================================================
TOTAL CANDIDATES AUDITED:               2 625
CERTIFIED 2D PLAN ↔ 3D BIM PAIRS:          10 (CORE_RESBIM_PAIRED)
CERTIFIED 2D SNAPSHOT ↔ 3D BIM PAIRS:      20 (CORE_IFC_BENCH)
CERTIFIED 2D RGB ↔ 2.5D DEPTH FRAMES:   2 592 (CORE_STRUCTSCAN3D)
NEW 2D PLAN ↔ 3D BIM PAIRS IN RAW:          0
REJECTED CROSS-DATASET CANDIDATES:          3 (RPLAN↔IL3D, RESPLAN↔IFC, CAD↔IFC)
CONFIDENCE THRESHOLD RESPECTED:          100% (Aucun 'LOW' certifié)
==================================================
```

---

## 2. Protocole du Détecteur Multi-Niveaux

Conformément aux Sections 5 à 10 du mandat, chaque association candidate a été soumise à un filtre strict à quatre niveaux :

| Niveau | Méthode d'Appariement | Critères Vérifiés | Seuil d'Admissibilité |
| :--- | :--- | :--- | :--- |
| **Niveau 1** | **Identifiants & Provenance** | Rapprochement déterministe par `stem`, `UUID`, nom de projet, IFC GUID, `archive_path`, métadonnées officielles. | Identité stricte ou conteneur de projet partagé. |
| **Niveau 2** | **Structure & Typologie** | Comparaison du nombre de pièces, connectivité topologique, nombre de portes, fenêtres, parois structurales. | Isomorphisme topologique prouvé. |
| **Niveau 3** | **Géométrie & Métrique** | Comparaison des boîtes englobantes, cotes réelles, empreintes géométriques (IoU), ratios d'aspect. | Concordance géométrique sans distorsion. |
| **Niveau 4** | **Sémantique & BIM** | Concordance des noms de pièces, types d'espaces (`IfcSpace`), éléments d'équipement et mobilier. | Ne peut servir de preuve isolée. |

---

## 3. Inventaire Détaillé des Sources Auditées

### 3.1. `CORE_RESBIM_PAIRED` — Paires 2D Plan $\leftrightarrow$ 3D IFC (10 Paires Certifiées)
- **Origine :** Dépôt officiel HuggingFace `tsesterh/ResBIM-IFC` (Licence MIT).
- **Composition :** 10 fichiers `.jpg` (plans d'architecte 7572×4189 px) et 10 fichiers `.ifc` (IFC4 CoordinationView V2.0).
- **Audit Niveau 1 :** Correspondance parfaite par radical de nom (`unit_000`, `unit_001`, `unit_002`, `unit_003`, `unit_004`, `unit_005`, `unit_010`, `unit_100`, `unit_101`, `unit_102`).
- **Audit Niveaux 2, 3, 4 :** Parois, baies et désignations spatiales du plan d'architecte coïncident strictement avec les entités `IfcWall`, `IfcDoor`, `IfcWindow` et `IfcSpace`.
- **Verdict :** **`CERTIFIED`** (Niveau de confiance : **`EXACT`**).
- **Usage Scientifique :** Tâches `BIM_PLUS_PLAN` (#68) et `PLAN_PLUS_3D` (#65).

### 3.2. `CORE_IFC_BENCH` — 3D IFC $\leftrightarrow$ Rendu Snapshot (20 Paires Certifiées)
- **Origine :** Benchmark `sylvainhellin/ifc-bench` (Licence CC BY 4.0).
- **Composition :** 21 projets architecturaux réels contenant `arc.ifc`, `snapshot.png` (1040×1164 px), `model_card.md` et `license.txt`.
- **Audit Niveau 1 :** 20 projets possèdent un modèle architectural `arc.ifc` apparié nativement au snapshot de rendu dans le même sous-dossier de projet (le projet `ettenheim_gis` utilise `city.ifc` et est exclu du corpus bâtiment).
- **Verdict :** **`CERTIFIED`** pour la modalité `IMAGE_PLUS_BIM` / `IFC_QA` (#27).
- **Restriction Majeure :** Le fichier `snapshot.png` est une **vue 3D perspective/axonométrique texturée**, et non un plan d'étage orthographique 2D coté. Il ne peut en aucun cas être requalifié en plan d'étage sans falsifier la distribution de données.

### 3.3. `CORE_STRUCTSCAN3D` — 2D RGB $\leftrightarrow$ Profondeur 2.5D (2 592 Paires Certifiées)
- **Origine :** StructScan3D (RGB-D structural scanning).
- **Composition :** 2 594 images RGB, 2 594 cartes de profondeur métriques PNG, 2 594 masques de segmentation structurelle.
- **Audit Niveau 1 :** 2 592 triplets de trames vidéo concordent à 100 % sur leur `timestamp stem` (ex: `appt_harr_s10_00000`).
- **Verdict :** **`CERTIFIED`** pour l'estimation de profondeur et segmentation structurelle en vue subjective (robotique / vision).
- **Restriction Majeure :** Donnée de caméra subjective d'intérieur, dépourvue de plan architectural global ou de maquette paramétrique IFC.

---

## 4. Audit des Candidats Trans-Datasets & Rejets Formels

Conformément à la Règle 10 (*Interdiction d'inventer des paires artificielles sans vérité terrain*) :

### 4.1. Candidat Rejeté #1 : `CORE_RPLAN` (Plans 2D) $\longleftrightarrow$ `CORE_IL3D` (Scènes 3D)
- **Hypothèse testée :** Vérifier si les agencements 3D de meubles d'IL3D pouvaient correspondre aux contours d'appartements d'RPLAN.
- **Audit Niveau 1 (Identifiants) :** 0 correspondance. RPLAN utilise des entiers séquentiels (`42007.png`), IL3D des UUIDv4 aléatoires (`74673e32-94ff-11f0...json`).
- **Audit Niveau 2 (Structure) :** Divergence complète. RPLAN modélise des appartements multi-pièces complets chinois (salon, chambres, sanitaires, cuisine). IL3D modélise des agencements synthétiques de pièces unitaires isolées (`Synth_Floor`, rectangle 4 sommets).
- **Audit Niveau 3 (Géométrie) :** RPLAN est matriciel non calibré (256×256 px). IL3D est en coordonnées métriques cartésiennes (mètres).
- **Verdict :** **`REJECTED`** (Confiance : **`REJECTED`**). Tout appariement relèverait de la pure hallucination statistique.

### 4.2. Candidat Rejeté #2 : `CORE_RESPLAN` (Vecteurs 2D) $\longleftrightarrow$ `CORE_BIM_IFC` (Modèles IFC)
- **Hypothèse testée :** Vérifier si les 17 000 plans ResPlan possédaient une contrepartie IFC dans buildingSMART ou ifc-bench.
- **Audit Niveaux 1 à 4 :** Aucune provenance commune. ResPlan provient d'annonces immobilières d'Asie du Sud (Inde/Pakistan) vectorisées par vision par ordinateur. Les fichiers IFC proviennent d'édifices témoins européens et américains (KIT, BIMserver, buildingSMART).
- **Verdict :** **`REJECTED`** (Confiance : **`REJECTED`**).

### 4.3. Candidat Rejeté #3 : `CORE_FLOORPLANCAD` $\longleftrightarrow$ IFC
- **Statut légal :** `LEGAL_REVIEW_REQUIRED`.
- **Verdict :** **`QUARANTINED / REJECTED`**.

---

## 5. Conclusion de l'Audit d'Appariement

L'exploration exhaustive du corpus RAW existant démontre de façon irréfutable que :
1. **Aucune paire 2D Plan $\leftrightarrow$ 3D BIM supplémentaire n'existe de manière cachée dans le RAW.**
2. Le gisement réel de paires 2D/3D certifiables avec plan d'architecte et maquette IFC reste strictement borné à **10 unités** (`CORE_RESBIM_PAIRED`).
3. Toute tentative d'associer arbitrairement des plans 2D d'une source avec des maquettes 3D d'une autre source violerait les règles fondamentales d'intégrité scientifique d'ARCHI-AI.
