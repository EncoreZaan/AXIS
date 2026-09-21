# ARCHI-AI — Audit Juridique & Conformité des Licences

Ce document classe rigoureusement les licences de tous les datasets examinés afin d'assurer la conformité légale du projet **ARCHI-AI**.

---

## 1. Principes d'Audit Juridique ARCHI-AI

Un dataset disponible publiquement sur internet, GitHub, Kaggle ou Hugging Face n'est **JAMAIS** automatiquement libre d'utilisation.

Pour ARCHI-AI, nous distinguons trois niveaux d'impact juridique :
1. **Entraînement local fermé (Recherche pure) :** Acceptable sous la plupart des licences académiques non commerciales (CC BY-NC, accords universitaires).
2. **Redistribution des poids de modèle fine-tunés (Open-Weight / Open-Source) :** Soumis aux clauses de contamination des licences (ex: ShareAlike - SA) et aux restrictions contractuelles explicites interdisant la création de modèles dérivés partagés.
3. **Exploitation commerciale directe ou SaaS :** Strictement interdite dès lors qu'interviennent des clauses non commerciales (NC), des EULA propriétaires (Matterport) ou des clauses de non-concurrence.

---

## 2. Classification Complète par Catégorie Juridique

### Catégorie 1 : Clairement Utilisable (Commercial & Recherche Libre)

Ces datasets bénéficient de licences open-source hautement permissives autorisant l'entraînement, la modification, la dérivation et l'exploitation commerciale sans restriction de redistribution (seule l'attribution est requise).

| Dataset | Licence Officielle | Droits d'Entraînement | Droits de Redistribution | Exploitation Commerciale |
| :--- | :--- | :--- | :--- | :--- |
| **IL3D** | **Apache-2.0** | Total | Libre avec mention de licence et notice | **Autorisée** |
| **ResPlan** | **CC BY 4.0** | Total | Libre avec attribution | **Autorisée** |
| **Modified Swiss Dwellings (MSD)**| **CC BY 4.0** | Total | Libre avec attribution | **Autorisée** |
| **StructScan3D** | **CC BY 4.0** | Total | Libre avec attribution | **Autorisée** |
| **RPLAN (Miroir Zenodo)** | **CC BY 4.0** | Total | Libre avec attribution | **Autorisée** |

> **Implication stratégique :** Ce groupe forme le **socle libre inviolable** d'ARCHI-AI. Un modèle entraîné exclusivement sur ces 5 datasets peut être redistribué et commercialisé sans aucun risque de litige.

---

### Catégorie 2 : Utilisable sous Conditions (ShareAlike / Partage à l'Identique)

Ces datasets autorisent l'utilisation et la dérivation, mais imposent que toute redistribution d'œuvres dérivées soit effectuée sous la même licence (effet viral partiel).

| Dataset | Licence Officielle | Contrainte Clé | Impact ARCHI-AI |
| :--- | :--- | :--- | :--- |
| **MMIS** | **CC BY-SA 4.0** | Obligation de redistribuer les données dérivées sous CC BY-SA 4.0 | Si les paires de Q/A dérivées de MMIS sont publiées, elles doivent être sous CC BY-SA 4.0. |

---

### Catégorie 3 : Recherche Non Commerciale Uniquement (CC BY-NC & Variantes)

Ces datasets autorisent la recherche, l'expérimentation et l'entraînement interne, mais interdisent formellement toute exploitation commerciale ou monétisation directe.

| Dataset | Licence Officielle | Conditions de Redistribution | Risque de Contamination Commerciale |
| :--- | :--- | :--- | :--- |
| **CubiCasa5K** | **CC BY-NC 4.0** | Redistribution des données brutes soumise à la clause NC | Élevé si le modèle final est vendu ou monétisé. Nul pour la recherche open-weights non commerciale. |
| **M3DLayout** | **CC BY-NC 4.0** | Soumis aux termes 3D-FRONT sous-jacents | Identique à CubiCasa5K. |
| **HSSD** | **CC BY-NC 4.0** | Acceptation des termes Hugging Face | Identique. |
| **InternScenes** | **CC BY-NC-SA 4.0** | Non commercial ET Partage à l'identique | Double contrainte : non commercial + dérivés sous licence identique. |
| **SpatialGen** | **CC BY-NC-SA 4.0** | Non commercial ET Partage à l'identique | Identique. |
| **CHOrD** | Recherche Académique NC | Données de recherche | Limité à l'expérimentation académique. |
| **MLSTRUCT-FP** | Recherche Universitaire NC | Demande de lien / Pas de redistribution | Pas de rediffusion des données brutes chiliennes. |

---

### Catégorie 4 : Licences Restrictives / EULA Propriétaires (Danger Juridique Élevé)

Ces licences imposent des contrats d'adhésion spécifiques avec des clauses léonines ou des interdictions de concurrence directe.

| Dataset | Type de Licence | Clauses Bloquantes | Verdict ARCHI-AI |
| :--- | :--- | :--- | :--- |
| **Matterport3D** | Matterport Academic EULA | - Interdiction formelle de concurrence avec Matterport 3D Showcase.<br>- Interdiction d'identification des biens réels.<br>- Droit de révocation unilatéral.<br>- Les modèles entraînés sont considérés comme des "données dérivées". | **INTERDIT POUR LE SOCLE PRODUCTION**.<br>Réservé à de l'évaluation comparative en sandbox fermée. |
| **Habitat-Matterport 3D (HM3D)** | Matterport Academic EULA | Mêmes restrictions que Matterport3D. | **INTERDIT POUR LE SOCLE PRODUCTION**. |
| **HM3D Semantics** | Matterport Academic EULA | Mêmes restrictions. | Réservé comme benchmark externe non entraîné. |
| **OpenRooms** | ScanNet + Adobe Stock Licensing | - Nécessite une licence individuelle auprès d'Adobe Stock pour l'exploitation des textures d'intérieur. | Risque de contrefaçon de droits d'auteur sur les textures commerciales. |
| **Structured3D** | Structured3D Terms of Use | - Formulaire individuel d'accord.<br>- Interdiction formelle de redistribution des scans/rendus bruts. | Acceptable pour l'entraînement local, mais interdiction d'héberger publiquement les images brutes sur notre Hugging Face. |
| **InteriorGS** | Manycore Terms of Use | - Gated dataset sous contrôle de Manycore Tech Inc. | Usage restreint sous contrôle éditeur. |

---

### Catégorie 5 : Licences Inconnues, Floues ou Scrapées (Risque de Contrefaçon)

Données collectées sans cadre juridique explicite, présentant un risque élevé d'appropriation illégitime.

| Dataset | Statut Légal Constaté | Nature du Risque |
| :--- | :--- | :--- |
| **BRIDGE** | `LICENSE UNCLEAR` | Collecté sur des sites web d'agences d'architecture sans traçabilité des droits patrimoniaux. |
| **Kaggle interior_design** | `LICENSE UNCLEAR` | Images web scrapées sans autorisation des photographes ou des designers. |
| **rrustom/architecture2022clean** | `LICENSE UNCLEAR` | Licence non enregistrée, images d'origines disparates (photos + générations IA). |
| **FloorPlanCAD** | `RESEARCH ONLY (ABANDONWARE)` | Site officiel éteint en 2022, licences des plans d'agences non renouvelées. |

> **Règle absolue ARCHI-AI :** Aucun dataset de cette catégorie ne doit être injecté dans le pipeline d'entraînement sans purge ou accord explicite.

---

### Catégorie 6 : Données Fermées ou Non Publiées

| Dataset | Statut | Constat |
| :--- | :--- | :--- |
| **iDesigner** | `NOT APPLICABLE` | Données internes propriétaires non publiées par les auteurs. |
| **360SpatialAI** | `NOT APPLICABLE` | Prototype expérimental sans dataset distribué. |
| **HomeWorld** | `ACCESS UNCLEAR` | Projet très prometteur (Juin 2026), mais dépôt GitHub encore en statut "Coming Soon". |

---

## 3. Analyse des Risques Juridiques pour ARCHI-AI

### Risque A : Contamination par Licence "Non Commerciale" (NC)
Si ARCHI-AI est entraîné sur un mélange contenant `CubiCasa5K` (CC BY-NC) ou `M3DLayout` (CC BY-NC), les poids finaux du modèle Qwen2-VL fine-tuné ne pourront **légalement pas être commercialisés** ou intégrés dans une offre payante sans renégociation des droits avec chaque ayant-droit.

### Risque B : Clauses Dérivées Matterport Inc.
L'EULA de Matterport affirme explicitement que tout algorithme ou modèle entraîné sur ses données constitue une "information dérivée" sujette à ses restrictions. Déployer un modèle entraîné sur HM3D dans un environnement de production présente un risque de mise en demeure par Matterport Inc.

### Risque C : Violation de Copyright sur Textures (OpenRooms)
L'inclusion de textures commerciales Adobe Stock au sein du pipeline de rendu OpenRooms crée une dépendance directe envers des licences tierces propriétaires.

---

## 4. Recommandation Stratégique pour ARCHI-AI V1

Afin de préserver la totale liberté d'ARCHI-AI, nous adoptons une **stratégie à deux enceintes hermétiques** :

```text
┌─────────────────────────────────────────────────────────────┐
│ ENCEINTE 1 : SOCLE V1 LIBRE & COMMERCIALISABLE (CORE V1)    │
│ - IL3D (Apache-2.0)                                         │
│ - ResPlan (CC BY 4.0)                                       │
│ - Modified Swiss Dwellings (CC BY 4.0)                      │
│ - StructScan3D (CC BY 4.0)                                  │
│ - Sous-ensemble RPLAN filtré (CC BY 4.0)                    │
│ - BIM/IFC QA (Open Access)                                  │
│ ==> 100% SÉCURISÉ POUR TOUT USAGE (TRAIN, POIDS, SAAS)      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ ENCEINTE 2 : EXTENSION RECHERCHE NON COMMERCIALE (ACADÉMIQUE)│
│ - CubiCasa5K (CC BY-NC 4.0)                                 │
│ - Structured3D (Terms of Use NC)                            │
│ - M3DLayout (CC BY-NC 4.0)                                  │
│ - MMIS (CC BY-SA 4.0)                                       │
│ - HSSD (CC BY-NC 4.0)                                       │
│ ==> RÉSERVÉ AUX EXPÉRIMENTATIONS ET BENCHMARKS COMPARATIFS  │
└─────────────────────────────────────────────────────────────┘
```

Cette distinction protège le projet : nous savons exactement quels exemples peuvent composer une version de production libre et lesquels relèvent de la recherche non commerciale.
