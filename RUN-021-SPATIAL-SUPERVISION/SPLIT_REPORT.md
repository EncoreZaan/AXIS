# AXIS — Rapport de Découpage du Dataset Spatial (`SPLIT_REPORT.md`)

> **Run Identifier:** `RUN-021-SPATIAL-SUPERVISION`  
> **Date:** 2026-09-23  
> **Stratégie de Split:** `project_group_id_deterministic_hash` (Graine = 42)  
> **Statut:** **SPLIT_INTEGRITY: PASS** | **HERMÉTIQUE**

---

## 1. Découpage Global des Données

Le partitionnement a été appliqué au niveau racine des assets physiques d'origine (`asset_id`), garantissant qu'aucune image ni aucun plan d'appartement ne franchisse la frontière entre les ensembles d'entraînement, de validation et de test.

| Split | Nombre d'Assets Physiques | Pourcentage d'Assets | Nombre d'Exemples Supervisés | Pourcentage d'Exemples |
| :--- | :---: | :---: | :---: | :---: |
| **TRAIN** | **775** | 77.5 % | **6 160** | 77.5 % |
| **VALIDATION** | **98** | 9.8 % | **784** | 9.9 % |
| **TEST** | **127** | 12.7 % | **1 006** | 12.7 % |
| **TOTAL** | **1 000** | 100.0 % | **7 950** | 100.0 % |

---

## 2. Répartition par Source dans Chaque Split

### Split TRAIN (775 assets / 6 160 exemples) :
- `CORE_RPLAN` : 767 plans d'étage (6 136 exemples supervisés)
- `CORE_RESBIM_PAIRED` : 8 unités résidentielles certifiées (24 exemples supervisés)

### Split VALIDATION (98 assets / 784 exemples) :
- `CORE_RPLAN` : 98 plans d'étage (784 exemples supervisés)
- `CORE_RESBIM_PAIRED` : 0 unité

### Split TEST (127 assets / 1 006 exemples) :
- `CORE_RPLAN` : 125 plans d'étage (1 000 exemples supervisés)
- `CORE_RESBIM_PAIRED` : 2 unités résidentielles certifiées (6 exemples supervisés)

---

## 3. Répartition par Famille de Tâches

| Famille de Tâches | Train | Validation | Test | Total | Ratio |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **TASK A (Identification & Cardinalité)** | 1 558 | 196 | 256 | **2 010** | 25.3 % |
| **TASK B (Relations Spatiales Directionnelles)** | 767 | 98 | 125 | **990** | 12.5 % |
| **TASK D (Connectivité & Portes)** | 1 534 | 196 | 250 | **1 980** | 24.9 % |
| **TASK F (Relations Extrémales & Comparatives)**| 767 | 98 | 125 | **990** | 12.5 % |
| **TASK G (Raisonnement Topologique & Graphe)** | 1 534 | 196 | 250 | **1 980** | 24.9 % |
| **TOTAL** | **6 160** | **784** | **1 006** | **7 950** | **100.0 %** |

---

## 4. Répartition par Niveau de Difficulté

- **EASY** (1-hop, cardinalités, contact direct) : 4 980 exemples (62.6 %)
- **MEDIUM** (comparatif, recherche d'extremum) : 990 exemples (12.5 %)
- **HARD** (multi-hop graph reachability, circulation hub) : 1 980 exemples (24.9 %)

---

## 5. Tailles Recommandées du Dataset

Conformément à la Règle §20 :
- **Small (Minimum Viable)** : 1 000 exemples (échantillonnage équilibré 200/famille).
- **Medium (Recommandé pour Phase 6B)** : 3 000 exemples (600/famille, ratio optimal signal/compute).
- **Full (Maximum Certifié Disponible)** : **7 950 exemples** (génération intégrale sur les 1 000 assets physiques).
