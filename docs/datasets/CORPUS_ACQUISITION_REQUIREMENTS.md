# ARCHI-AI — Spécifications d'Acquisition de Données Externes (`CORPUS_ACQUISITION_REQUIREMENTS.md`)

> **Phase :** PHASE 3 — Corpus Expansion & Scientific Readiness  
> **Auteur :** Lead Dataset Engineer & Multimodal Dataset Researcher  
> **Date :** 2026-09-21  
> **Règle Préalable :** Émis exclusivement après l'audit exhaustif du corpus RAW démontrant l'indisponibilité physique des données nécessaires.  
> **Directive d'Arrêt :** Aucun téléchargement externe automatique n'est exécuté sans décision explicite de l'utilisateur.  

---

## 1. Cahier des Charges d'Acquisition par Capacité Manquante

Conformément aux Sections 17 et 18 du mandat, chaque demande d'acquisition future est rigoureusement bornée :

### ACQUISITION-REQ-01 : Paires 2D Floorplan d'Architecte $\longleftrightarrow$ 3D OpenBIM IFC
- **Missing Capability :** Alignement multimodal et confrontation d'enveloppe entre dessin d'étage et maquette paramétrique IFC.
- **Why Needed :** Entraîner le VLM sur `BIM_PLUS_PLAN` et `PLAN_PLUS_3D` sans risque de surapprentissage sur les 10 unités de `CORE_RESBIM_PAIRED`.
- **Current Coverage :** 10 paires résidentielles (20 fichiers).
- **Required Quantity :** 50 à 100 unités/édifices distincts (représentant ~200 à 300 exemples supervisés étanches).
- **Desired Modalities :** Plans d'architecte vectoriels (PDF vectoriel, DWG, DXF ou SVG haute résolution) + Maquette 3D OpenBIM (`.ifc` IFC2x3 ou IFC4).
- **License Requirement :** Licences permissives obligatoires : **MIT, Apache 2.0, CC-BY 4.0 ou Domaine Public (CC0)**. Clause commerciale compatible.
- **Quality Requirement :** Modèles IFC valides selon le standard buildingSMART (géométries fermées, `IfcSpace` renseignés, pas d'éléments orphelins).
- **Pairing Requirement :** Isomorphisme 1:1 certifié entre le plan de niveau et l'étage (`IfcBuildingStorey`) correspondant.
- **Priority :** **`P0 (CRITIQUE / BLOQUANT POUR LE VRAI MULTIMODAL)`**

---

### ACQUISITION-REQ-02 : Plans 2D Vectoriels Métriquement Étalonnés (Dérivation Interne)
- **Missing Capability :** Calcul déterministe de surfaces réelles (m²), vérification de cotes et largeurs réglementaires de dégagements (CCH / PMR).
- **Why Needed :** Remplacer les plans matriciels non calibrés (RPLAN) et les vecteurs non métriques (ResPlan) par des plans physiquement étalonnés.
- **Current Coverage :** 0 plan coté certifié dans le CORE.
- **Required Quantity :** 200 à 500 plans d'étage cotés.
- **Desired Modalities :** Tracé vectoriel 2D en millimètres / mètres (SVG / DXF / GeoJSON) avec cotes linéaires et tables de surfaces vérifiées.
- **License Requirement :** Dérivé interne direct à partir des modèles OpenBIM IFC libres de droit déjà présents dans le RAW (ex: IFC-Bench, buildingSMART).
- **Quality Requirement :** Échelle métrique exacte 1:1, erreur dimensionnelle < 0.001 m, projection orthographique plane horizontale rigoureuse.
- **Pairing Requirement :** Vérité terrain géométrique extraite mathématiquement des entités `IfcWall` et `IfcSpace`.
- **Priority :** **`P1 (HAUTE / DÉBLOCAGE DE LA SUPERVISION MÉTRIQUE)`**

---

### ACQUISITION-REQ-03 : Confrontation Photo d'Intérieur $\longleftrightarrow$ Cône de Vue sur Plan
- **Missing Capability :** Localisation de prise de vue, confrontation d'ambiance et vérification de cohérence aménagement/dessin.
- **Why Needed :** Débloquer la tâche `IMAGE_PLUS_PLAN` (#63).
- **Current Coverage :** 3 exemples (MMMU).
- **Required Quantity :** 100 à 200 paires photo/plan avec positionnement spatial.
- **Desired Modalities :** Photographie intérieure réelle (RGB JPEG) + Plan d'étage 2D avec coordonnées cartésiennes de la caméra ($x, y, \theta$).
- **License Requirement :** CC-BY 4.0, MIT ou équivalent libre. Exclusion formelle des corpus académiques fermés (Non-Commercial) du split de production.
- **Quality Requirement :** Résolution photo $\ge 1920\times 1080$, absence de visages identifiables ou données privées (RGPD).
- **Pairing Requirement :** Matrice de pose caméra calibrée par rapport au repère du plan.
- **Priority :** **`P2 (MOYENNE / EXTENSION CAPACITAIRE PHASE ULTÉRIEURE)`**

---

### ACQUISITION-REQ-04 : Corpus Didactique d'Histoire de l'Architecture & Théorie Spatiale
- **Missing Capability :** Culture architecturale globale, typologies historiques d'édifices, mouvements architecturaux.
- **Why Needed :** Débloquer la tâche `ARCHITECTURE_HISTORY` (#44) et enrichir `EXPLANATION` (#58).
- **Current Coverage :** Meubles cultes MoMA/Met uniquement (aucun corpus bâtiment).
- **Required Quantity :** 500 à 1 000 fiches historiques et doctrinales vérifiées.
- **Desired Modalities :** Textes structurés (Markdown / JSON) sourcés auprès d'institutions publiques d'architecture.
- **License Requirement :** Domaine public, Open Access ou CC-BY.
- **Quality Requirement :** Vérifiabilité académique stricte (dates, architectes, manifestes, typologies constructives).
- **Pairing Requirement :** Unimodal textuel ou Text+Photo documentée.
- **Priority :** **`P3 (BASSE / ENRICHISSEMENT THÉORIQUE)`**

---

## 2. Matrice d'Admissibilité Juridique Préalable

Toute source candidate future devra être auditée selon la grille suivante avant toute intégration :

```text
==================================================
GRILLE D'ADMISSIBILITÉ JURIDIQUE ARCHI-AI
==================================================
[OBLIGATOIRE] Clause d'utilisation commerciale : AUTORISÉE
[OBLIGATOIRE] Droit de redistribution : AUTORISÉ
[OBLIGATOIRE] Droit de création d'œuvres dérivées : AUTORISÉ
[OBLIGATOIRE] Compatibilité de licence avec le pipeline ARCHI-AI (MIT / Apache 2.0 / CC-BY)
[OBLIGATOIRE] Respect de la vie privée (absence totale de PII, photos de personnes, adresses privées)
[INTERDIT] Clauses 'Non-Commercial' (NC) dans le CORE
[INTERDIT] Clauses 'Share-Alike' virales (SA) sans validation légale préalable
==================================================
```
