# ARCHI-AI — Rapport d'Audit Forensique de Calibration ResPlan (`RESPLAN_CALIBRATION_REPORT.md`)

> **Phase :** PHASE 3 — Corpus Expansion & Scientific Readiness  
> **Auteur :** Lead Dataset Engineer & Forensic Dataset Auditor  
> **Date :** 2026-09-21  
> **Actif Inspecté :** `core/resplan/extracted/ResPlan.pkl` (SHA-256: `103edd854a5f365aa875ed832e6cef0d8bc72c4b34e5df0856c01b6970684cb5`)  
> **Effectif :** 17 000 plans vectoriels résidentiels  
> **Statut Final de Calibration :** **`FAIL`**  
> **Décision de Modération :** **`QUARANTINED` (Strictement exclu de toute tâche métrique)**  

---

## 1. Diagnostic Forensique Exhaustif

L'audit approfondi mené sur le jeu complet de 17 000 plans d'appartements de `ResPlan.pkl` a révélé les anomalies structurelles suivantes :

### 1.1. Normalisation Matricielle Arbitraire à [0, 256]
- **Constat mathématique :** Chaque plan d'étage a été redimensionné de façon unitaire et indépendante afin que sa dimension maximale (`max(width, height)` du polygone `inner`) soit exactement égale à `256.0` (Moyenne : `256.0000`, Écart-type : `0.000000`).
- **Conséquence :** Un studio de 20 m² et un duplex de 300 m² occupent exactement la même emprise de 256 unités cartésiennes dans les coordonnées vectorielles.

### 1.2. Corruption Sévère du Champ `net_area`
- **32.1 % des plans (5 458 plans)** possèdent un `net_area` strictement nul (`0.0`).
- **4.1 % des plans (696 plans)** possèdent un `net_area` aberrante excédant 1 000 (valeur maximale observée : `79 140 857 694.65`).
- Médiane : `67.95` | Moyenne arithmétique : `4 707 661.72` (due aux valeurs aberrantes non filtrées par les auteurs originaux).

### 1.3. Absence de Rapport Déterministe entre Polygones et Métadonnées
- Le rapport entre l'aire calculée des polygones (en unités² de canevas) et le champ `area` textuel (estimé en m² dans l'annonce) varie de manière erratique :
  - Minimum observé : `36.20`
  - Maximum observé : `1 817.49`
  - Moyenne : `369.09`
  - Écart-type : `173.24`
- Il n'existe aucun coefficient multiplicateur universel reliant les unités de tracé aux surfaces physiques réelles.

---

## 2. Test des Méthodes Candidates de Calibration

Conformément à la Section 14 et 15 du mandat, quatre méthodes de calibration déterministe ont été testées et évaluées :

| Méthode | Source de Référence | Hypothèse Formulée | Preuve Disponible | Écart d'Erreur Mesuré | Statut |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **Méthode 1 : Inférence par `area` textuelle** | Champ `area` de l'annonce | $\text{scale} = \sqrt{\frac{\text{area}}{\text{geom\_area}}}$ | Texte libre extrait de l'annonce immobilière originale. | $\pm 46.9\,\%$ (l'aire de l'annonce inclut/exclut balcons et parties communes selon les pays). | **`REJECTED`** |
| **Méthode 2 : Étalonnage sur largeur de porte** | Polygones `door` | Largeur standard de porte battante = 0.80 m | Largeurs de baies mesurées entre 2.1 et 14.5 unités dans le canevas. | $\pm 38.2\,\%$ (aucune cote normalisée en sortie de vectorisation). | **`REJECTED`** |
| **Méthode 3 : Étalonnage sur épaisseur de mur** | Champ `wall_depth` | Épaisseur moyenne de mur = 0.20 m | Documenté dans le README : *« wall thickness is normalised per plan »*. | Non mesurable (artefact algorithmique de lissage de contour). | **`REJECTED`** |
| **Méthode 4 : Échelle graphique intégrée** | Fichiers source ou annotations | Présence d'un barreau d'échelle ou d'une cote écrite | Aucune image raster source ni annotation textuelle cotée n'est redistribuée. | Aucune preuve physique. | **`REJECTED`** |

---

## 3. Décision Formelle d'Audit

En application de la **Règle Absolue : « NE JAMAIS INVENTER une conversion pixel $\to$ m² »** :

1. **Le conteneur `ResPlan.pkl` échoue irrévocablement au test de calibration métrique.**
2. **Statut : `QUARANTINED`** pour :
   - la tâche `PLAN_SUMMARY` (#15) ;
   - tout calcul ou prédiction de surface en mètres carrés (m²) ;
   - toute extraction de cotes, longueurs de parois ou largeurs de baies en mètres.
3. **Interdiction de Supervision Métrique :** Aucun exemple portant sur des grandeurs dimensionnelles ne peut être généré à partir de `ResPlan.pkl`.
