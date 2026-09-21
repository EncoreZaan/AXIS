# ARCHI-AI — Rapport d'Audit Indépendant Global (`INDEPENDENT_AUDIT_REPORT.md`)

> **Date d'audit :** 21 September 2026  
> **Posture :** RED TEAM STRICTE (Audit Indépendant Pré-Entraînement)  
> **Principe :** Zéro validation complaisante, rejet des faux PASS par circularité.

---

## 1. Synthèse Métrique Exécutive

| Métrique | Valeur Auditée | Seuil Critique | Statut Red Team |
| :--- | :---: | :---: | :---: |
| **Exemples Totaux Audités** | **506** | $\ge 250$ | CERTIFIÉ (Stratifié) |
| **Échantillon Wave 1 Repaired** | **462 / 722 (63.99 %)** | $\ge 20\%$ | CONFORME |
| **Échantillon Gold Set V2** | **73 / 73 (100.0 %)** | 100% | COUVERTURE TOTALE |
| **Audit des WARNINGs** | **33 / 33 (100.0 %)** | 100% | EXHAUSTIF |
| **Audit de la Review Queue** | **21 / 21 (100.0 %)** | 100% | EXHAUSTIF |
| **Audit des L6 Multicontraintes**| **50 / 50 (100.0 %)** | 100% | EXHAUSTIF |
| **Taux de Grounding Indépendant**| **19.6 %** | $\ge 85\%$ | ALERTE |
| **Taux de Réponses Spécifiques** | **18.6 %** | $\ge 80\%$ | VULNÉRABLE |
| **Taux de Fake Multimodal** | **21.2 %** | $\le 5\%$ | DÉFAILLANCE |
| **Taux de Duplication Structurelle**| **40.3 %** | $\le 15\%$ | SATURATION |
| **Taux d'Authenticité L5/L6** | **100.0 %** | $\ge 80\%$ | OK |
| **Taux de Transfert Adversarial**| **14.0 %** | $\le 10\%$ | TROP GÉNÉRIQUE |

---

## 2. Résultats par Domaine Clé

### 2.1. Raisonnement Spatial 3D (`OBJECT_RELATION`)
- **Taux de conformité euclidienne indépendante :** **100.0 %**
- **Délégation d'axe :** Vérification stricte des deltas $(dx, dy, dz)$ depuis les centroïdes.

### 2.2. Lecture de Plans 2D (`FLOORPLAN`)
- **Anomalie critique détectée :** Présence de coordonnées de pixels bruts (ex: 18 806 px², 50 336 px²) étiquetées sans conversion comme mètres carrés réels (`area_m2`).
- **Taux d'anomalie de surface floorplan :** **38.5 %** des plans vectoriels affectés.

### 2.3. BIM & Maquettes IFC
- **Taux de présence du payload IFC :** **100.0 %**
- **Hiérarchies et quantitatifs :** Validés sur les schémas IFC4 sans dépendance du JSON synthétique.

### 2.4. Ergonomie & Cotes Anthropométriques
- **Conversions cm -> m :** Déterministes et conformes.
- **Biais identifié :** Citation répétée du cercle de giration de Ø 1,50 m ou seuil <= 2 cm sur des questions portant sur des couloirs ou circulations simples (contamination par template de réponse).

### 2.5. Critique de Studio & Pédagogie
- **Structure quadripartite (Diagnostic, Cause, Conséquence, Recommandation) :** **100.0 %**
- **Analyse anti-sycophantie :** Respectée, zéro formule flatteuse creuse.

---

## 3. Verdict Indépendant Global
Voir le document de décision formel : `PRE_TRAINING_GATE.md`.
