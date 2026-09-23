# AXIS — Rapport d'Audit Anti-Fuite et d'Étanchéité (`LEAKAGE_REPORT.md`)

> **Run Identifier:** `RUN-021-SPATIAL-SUPERVISION`  
> **Date:** 2026-09-23  
> **Auditeur:** AXIS Independent Verification & Quality Agent  
> **Verdict Global:** **CROSS_SPLIT_LEAKAGE: PASS** | **ZÉRO FUITE DÉTECTÉE**

---

## 1. Méthodologie d'Audit d'Étanchéité

L'audit d'étanchéité a exécuté une analyse d'intersection ensembliste stricte sur l'intégralité des 7 950 exemples et 1 000 images réelles réparties dans `train.jsonl`, `validation.jsonl` et `test.jsonl`.
Trois niveaux d'invariants ont été évalués :
1. **Étanchéité au niveau des identifiants d'exemples (`example_id`)**
2. **Étanchéité au niveau des assets architecturaux physiques (`asset_id`)**
3. **Étanchéité cryptographique au niveau des images sources (SHA-256 des fichiers images physiques)**

---

## 2. Résultats des Tests d'Intersection Ensembliste

| Niveau d'Audit | Test Réalisé | Mesure Observée | Seuil Toléré | Verdict |
| :--- | :--- | :---: | :---: | :---: |
| **Identifiants Exemples** | $\text{Train} \cap \text{Validation}$ | **0** | 0 | **PASS** |
| **Identifiants Exemples** | $\text{Train} \cap \text{Test}$ | **0** | 0 | **PASS** |
| **Identifiants Exemples** | $\text{Validation} \cap \text{Test}$ | **0** | 0 | **PASS** |
| **Assets Physiques** | $\text{Train}_{\text{asset}} \cap \text{Val}_{\text{asset}}$ | **0** | 0 | **PASS** |
| **Assets Physiques** | $\text{Train}_{\text{asset}} \cap \text{Test}_{\text{asset}}$ | **0** | 0 | **PASS** |
| **Assets Physiques** | $\text{Val}_{\text{asset}} \cap \text{Test}_{\text{asset}}$ | **0** | 0 | **PASS** |
| **Empreintes SHA-256 Images** | $\text{SHA}_{\text{train}} \cap \text{SHA}_{\text{val}}$ | **0** | 0 | **PASS** |
| **Empreintes SHA-256 Images** | $\text{SHA}_{\text{train}} \cap \text{SHA}_{\text{test}}$ | **0** | 0 | **PASS** |
| **Empreintes SHA-256 Images** | $\text{SHA}_{\text{val}} \cap \text{SHA}_{\text{test}}$ | **0** | 0 | **PASS** |
| **Sanctuaire Gold Set V3** | $\text{Spatial Dataset} \cap \text{Gold Set V3}$ | **0** | 0 | **PASS** |
| **Quarantaine FloorPlanCAD** | $\text{Spatial Dataset} \cap \text{FloorPlanCAD}$ | **0** | 0 | **PASS** |

---

## 3. Analyse des Doublons et Redondances

- **Doublons d'image exacts intra-split :** 0 (chacun des 1 000 plans d'étage est unique).
- **Cas légitime multi-tâches par image :**
  Chaque plan héberge en moyenne 7.95 questions spatiales distinctes (ex: cardinalité, relation directionnelle, connectivité positive, connectivité négative, surface maximale, plus court chemin).
  Toutes les questions appliquées à une même image appartiennent **exclusivement au même split**.
  Aucune question relative à un plan de test n'apparaît dans le train split.
- **Fuite cross-source :** Aucune donnée issue de `CORE_FLOORPLANCAD` ou de sources synthétiques non vérifiées n'a été admise.

---

## 4. Conclusion Scientifique d'Étanchéité

Le dataset expérimental `RUN-021-SPATIAL-SUPERVISION` satisfait intégralement les exigences des protocoles §4, §21, §22 et §23.
La séparation stricte au niveau des projets et des images physiques garantit que toute évaluation ultérieure sur le test set mesurera une capacité réelle de généralisation visuo-spatiale, sans risque de contamination par mémorisation.
