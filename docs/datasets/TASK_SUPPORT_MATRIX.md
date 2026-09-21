# ARCHI-AI — Matrice de Supportabilité des 69 Tâches (`TASK_SUPPORT_MATRIX.md`)

> **Date d'élaboration :** 21 September 2026 à 18:25:00 UTC  
> **Auditeur Technique :** Assistant Spécialiste ARCHI-AI  
> **Principe Recteur :** Aucune tâche ne doit être instanciée artificiellement sans données réelles, sans preuve formelle (evidence) et sans vérifiabilité déterministe.  
> **Classification :**
> - **`SUPPORTED`** : Données brutes et traitées immédiatement disponibles, evidence vérifiable, qualité certifiée.
> - **`PARTIALLY_SUPPORTED`** : Données partiellement présentes (nécessite une contrainte textuelle ou un recoupement d'expert).
> - **`NOT_SUPPORTED`** : Données sources absentes du corpus actuel (interdiction formelle de génération sous peine de faux PASS).

---

## 1. Synthèse Globale de la Couverture

| Statut | Nombre de Tâches | % du Catalogue | Règle Opérationnelle Wave 1 Repaired |
| :--- | :---: | :---: | :--- |
| **`SUPPORTED`** | **28** | 40.6 % | **Génération active prioritaire** avec contrôle déterministe total. |
| **`PARTIALLY_SUPPORTED`** | **23** | 33.3 % | **Génération encadrée et contingentée** avec injection explicite de programme. |
| **`NOT_SUPPORTED`** | **18** | 26.1 % | **Strictement 0 exemple généré** tant que les sources requises ne sont pas acquises. |
| **TOTAL** | **69** | **100.0 %** | Catalogue exhaustif Groupes A à L. |

---

## 2. Matrice Complète par Groupe de Tâches

### Groupe A : Visual Understanding (7 tâches)

| Code Tâche | Intitulé | Statut | Source Mobilisable | Justification Technique & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| `IMAGE_ANALYSIS` | Analyse Visuelle Globale | **SUPPORTED** | StructScan3D / MMMU | Image RGB réelle avec dimensions et rôle d'enveloppe. |
| `INTERIOR_ANALYSIS` | Typologie d'Intérieur | **SUPPORTED** | StructScan3D | Espaces résidentiels réels avec métadonnées de volume. |
| `MATERIAL_IDENTIFICATION` | Identification Visuelle Matériau | **PARTIALLY_SUPPORTED** | PolyHaven / AmbientCG | Rendu de sphère/planche disponible, mais pas de photo in situ meublée. |
| `VISUAL_LIGHTING_ANALYSIS` | Analyse Visuelle Éclairage | **SUPPORTED** | PolyHaven HDRI | Panoramas avec EV et Kelvin mesurés. |
| `FURNITURE_IDENTIFICATION` | Identification Mobilier | **PARTIALLY_SUPPORTED** | MoMA / The Met | Notices et visuels patrimoniaux, inventaire spécifique. |
| `STYLE_ANALYSIS` | Analyse Stylistique Visuelle | **PARTIALLY_SUPPORTED** | MoMA / The Met | Classification stylistique documentée par les conservateurs. |
| `SPATIAL_RELATION_ANALYSIS`| Relations Spatiales Visuelles | **NOT_SUPPORTED** | *Aucune source 2D pure* | Nécessite des annotations 2D bounding boxes (absentes des photos simples). |

---

### Groupe B : Floorplan Reading & Topologie 2D (9 tâches)

| Code Tâche | Intitulé | Statut | Source Mobilisable | Justification Technique & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| `FLOORPLAN_READING` | Lecture de Plan d'Étage | **SUPPORTED** | ResPlan / RPLAN | Masques matriciels 256x256 et plans vectoriels. |
| `ROOM_IDENTIFICATION` | Identification des Pièces | **SUPPORTED** | ResPlan | Polygones nominatifs réels (`living`, `bedroom`, `kitchen`). |
| `ROOM_TOPOLOGY` | Topologie & Adjacence | **SUPPORTED** | ResPlan | Graphe d'adjacence certifié (`room_adjacency_graph`). |
| `CIRCULATION_ANALYSIS` | Circulations & Flux | **SUPPORTED** | ResPlan | Repérage de porte palière et calcul de desserte. |
| `DOOR_WINDOW_ANALYSIS` | Baies & Ouvertures | **SUPPORTED** | ResPlan | Coordonnées et types réels (`front_door`, `door`, `window`). |
| `FURNITURE_LAYOUT_ANALYSIS`| Mobilier sur Plan | **NOT_SUPPORTED** | *Absent de ResPlan 2D* | Les plans 2D vectoriels ne comportent pas les blocs de meubles meublants. |
| `PLAN_ERROR_DETECTION` | Détection d'Erreurs sur Plan | **PARTIALLY_SUPPORTED** | ResPlan | Détection de pièces aveugles ou goulots étroits. |
| `PLAN_SUMMARY` | Synthèse Métrique du Plan | **SUPPORTED** | ResPlan | Surfaces calculées sans approximation ($m^2$ réels). |
| `PLAN_TO_TEXT` | Description Textuelle Globale | **PARTIALLY_SUPPORTED** | ResPlan | Synthèse narrative complète des pièces et surfaces. |

---

### Groupe C : Espace 3D & Scene Graphs (5 tâches)

| Code Tâche | Intitulé | Statut | Source Mobilisable | Justification Technique & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| `SCENE_GRAPH_REASONING` | Raisonnement Scene Graph 3D | **SUPPORTED** | IL3D | Objets avec bounding boxes 3D et pièces englobantes réelles. |
| `OBJECT_RELATION` | Relations Objet-Objet 3D | **SUPPORTED** | IL3D | Calcul euclidien déterministe $d = \sqrt{\Delta x^2+\Delta y^2+\Delta z^2}$. |
| `ROOM_OBJECT_REASONING` | Objet-Espace Englobant | **SUPPORTED** | IL3D | Appartenance sémantique validée (`room_contains`). |
| `SPATIAL_LAYOUT_ANALYSIS` | Analyse d'Aménagement 3D | **PARTIALLY_SUPPORTED** | IL3D | Densité d'occupation et emprise volumétrique. |
| `3D_TO_TEXT` | Description de Scène 3D | **PARTIALLY_SUPPORTED** | IL3D | Narration des centroïdes et groupements d'usage. |

---

### Groupe D : BIM & Maquettes IFC (6 tâches)

| Code Tâche | Intitulé | Statut | Source Mobilisable | Justification Technique & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| `IFC_ENTITY_IDENTIFICATION`| Entités IFC Réelles | **SUPPORTED** | buildingSMART / IFC-Bench | Décompte exact des classes (`IfcWall`, `IfcDoor`, etc.). |
| `IFC_PROPERTY_REASONING` | Propriétés IFC (Psets) | **PARTIALLY_SUPPORTED** | buildingSMART IFC | Propriétés thermiques/acoustiques parfois non renseignées. |
| `BIM_SPATIAL_HIERARCHY` | Hiérarchie Spatiale BIM | **SUPPORTED** | buildingSMART / IFC-Bench | Étages réels (`storeys`) et espaces délimités (`spaces`). |
| `BIM_OBJECT_QUERY` | Requête d'Objets BIM | **SUPPORTED** | IFC-Bench QA | Questions expertes sur les quantitatifs réels. |
| `BIM_REASONING` | Raisonnement Synthétique BIM | **PARTIALLY_SUPPORTED** | ResBIM IFC | Vérification de conformité gros œuvre / second œuvre. |
| `IFC_QA` | QA Experte IFC | **SUPPORTED** | IFC-Bench QA | Paires questions/réponses techniques authentifiées. |

---

### Groupe E : Ergonomie & Normes (5 tâches)

| Code Tâche | Intitulé | Statut | Source Mobilisable | Justification Technique & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| `ERGONOMIC_ANALYSIS` | Analyse Ergonomique Globale | **PARTIALLY_SUPPORTED** | Neufert / Normes FR | Confrontation d'un aménagement à un ensemble de cotes. |
| `CLEARANCE_CHECK` | Contrôle de Dégagement | **SUPPORTED** | Neufert / Panero | Cotes déterministes normalisées en mètres (L1). |
| `CIRCULATION_CHECK` | Largeur de Passage | **SUPPORTED** | Normes PMR / Neufert | Prescriptions de passage utile ($\ge 0,80$ m et $\ge 0,90$ m). |
| `FURNITURE_DIMENSION_REASONING`| Cotes de Mobilier | **PARTIALLY_SUPPORTED** | Neufert | Hauteurs d'assise et de plan de travail standards. |
| `ACCESSIBILITY_ANALYSIS`| Accessibilité PMR | **SUPPORTED** | Normes FR (Légifrance) | Articles de loi officiels et exigences incompressibles. |

---

### Groupe F : Matériaux PBR (4 tâches)

| Code Tâche | Intitulé | Statut | Source Mobilisable | Justification Technique & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| `MATERIAL_ANALYSIS` | Propriétés Physiques | **SUPPORTED** | AmbientCG / PolyHaven | Canaux roughness, normal, displacement, échelle métrique. |
| `MATERIAL_COMPARISON` | Comparaison Technique | **PARTIALLY_SUPPORTED** | AmbientCG | Comparaison de deux shaders de la même famille. |
| `MATERIAL_APPLICATION` | Prescription d'Usage | **SUPPORTED** | PolyHaven Materials | Contextualisation selon la matière (bois, pierre, carrelage). |
| `PBR_REASONING` | Raisonnement Shader PBR | **SUPPORTED** | AmbientCG | Comportement sous lumière rasante et réflectance. |

---

### Groupe G : Éclairage & Photométrie (4 tâches)

| Code Tâche | Intitulé | Statut | Source Mobilisable | Justification Technique & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| `LIGHTING_ANALYSIS` | Ambiance & Photométrie | **SUPPORTED** | PolyHaven Lighting | Kelvin, EV, contraste, météo réels. |
| `LIGHTING_SCENARIO` | Scénarisation Lumineuse | **PARTIALLY_SUPPORTED** | PolyHaven Lighting | Transition jour/nuit et scénario d'ambiance. |
| `DAYLIGHT_REASONING` | Éclairage Naturel | **SUPPORTED** | PolyHaven HDRI | Pénétration diurne et stratégies d'occultation. |
| `ARTIFICIAL_LIGHTING_REASONING`| Éclairage Artificiel | **NOT_SUPPORTED** | *Aucun plan de calepinage* | Absence de plans de câblage et circuits d'allumage dans le RAW. |

---

### Groupe H : Histoire & Styles (5 tâches)

| Code Tâche | Intitulé | Statut | Source Mobilisable | Justification Technique & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| `STYLE_CLASSIFICATION` | Classification de Style | **PARTIALLY_SUPPORTED** | MoMA Collection | Courants modernes (Bauhaus, De Stijl, Art Déco). |
| `STYLE_COMPARISON` | Comparaison de Styles | **PARTIALLY_SUPPORTED** | MoMA / The Met | Mise en regard de deux créateurs d'époques distinctes. |
| `DESIGN_HISTORY` | Histoire du Design | **SUPPORTED** | MoMA / The Met | Notices patrimoniales exactes, designers et dates certifiés. |
| `ARCHITECTURE_HISTORY` | Histoire Architecture | **PARTIALLY_SUPPORTED** | The Met | Dessins et relevés d'architectes historiques. |
| `MATERIAL_AND_STYLE_RELATION`| Signature Matériaux | **SUPPORTED** | MoMA / The Met | Matériaux constitutifs documentés dans les cartouches. |

---

### Groupe I : Critique d'Atelier (6 tâches)

| Code Tâche | Intitulé | Statut | Source Mobilisable | Justification Technique & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| `PROJECT_CRITIQUE` | Critique Globale de Projet | **SUPPORTED** | ResPlan | Ancrée sur pièces réelles, perméabilité jour/nuit et surfaces. |
| `STRENGTH_IDENTIFICATION` | Identification Points Forts | **SUPPORTED** | ResPlan | Optimisation de surface et compacité des circulations. |
| `WEAKNESS_IDENTIFICATION`| Faiblesses Spatiales | **SUPPORTED** | ResPlan | Conflits acoustiques et ouvertures directes sur séjour. |
| `DESIGN_PROBLEM_DETECTION`| Détection de Conflits | **SUPPORTED** | ResPlan | Croisements de flux et débattements de portes. |
| `IMPROVEMENT_PROPOSAL` | Proposition d'Amélioration | **PARTIALLY_SUPPORTED** | ResPlan | Recommandations d'aménagement spatial constructif. |
| `ALTERNATIVE_DESIGN` | Alternative d'Aménagement | **NOT_SUPPORTED** | *Nécessite regénération CAD* | Proposer un tracé vectoriel alternatif complet non supporté. |

---

### Groupe J : Raisonnement Professionnel (6 tâches)

| Code Tâche | Intitulé | Statut | Source Mobilisable | Justification Technique & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| `REQUIREMENTS_ANALYSIS` | Analyse Cahier des Charges | **SUPPORTED** | ResPlan + Programme | Découpage des demandes client vs potentiel du plan. |
| `CONSTRAINT_REASONING` | Raisonnement sous Contraintes | **SUPPORTED** | Normes FR | Arbitrage PMR vs compacité (L6 certifié avec 2 contraintes). |
| `DESIGN_DECISION` | Décision de Conception | **PARTIALLY_SUPPORTED** | ResPlan | Justification du choix de distribution. |
| `TRADEOFF_ANALYSIS` | Arbitrage & Compromis | **SUPPORTED** | ResPlan | Lumière naturelle vs acoustique (L6 certifié). |
| `OPTION_COMPARISON` | Comparaison Multi-Options | **NOT_SUPPORTED** | *Absence de variantes* | Le corpus RAW ne dispose pas de versions A/B d'un même plan. |
| `FEASIBILITY_ANALYSIS` | Étude de Faisabilité | **PARTIALLY_SUPPORTED** | ResPlan / IFC | Analyse des contraintes porteuses avant abattement. |

---

### Groupe K : Pédagogie & Maïeutique (5 tâches)

| Code Tâche | Intitulé | Statut | Source Mobilisable | Justification Technique & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| `EXPLANATION` | Explication Didactique | **SUPPORTED** | Neufert / Standards | Définition des principes fondamentaux d'agencement. |
| `STUDIO_CRITIQUE` | Critique Pédagogique | **SUPPORTED** | ResPlan | Débriefing de studio avec niveau d'étudiant ciblé. |
| `GUIDED_REASONING` | Guidage Maïeutique | **SUPPORTED** | ResPlan | Dialogue socratique pas-à-pas avec inputs non vides. |
| `ERROR_EXPLANATION` | Explication d'une Erreur | **PARTIALLY_SUPPORTED** | ResPlan | Démonstration du défaut de conception. |
| `METHODOLOGY_EXPLANATION`| Méthodologie de Projet | **PARTIALLY_SUPPORTED** | Standards | Étapes de conception (esquisse, APS, APD, DOE). |

---

### Groupe L : Multimodalité Croisée (7 tâches)

| Code Tâche | Intitulé | Statut | Source Mobilisable | Justification Technique & Evidence |
| :--- | :--- | :---: | :--- | :--- |
| `IMAGE_PLUS_PLAN` | Image + Plan 2D | **PARTIALLY_SUPPORTED** | StructScan3D / ResPlan | Nécessite un appariement certifié de la même pièce. |
| `PLAN_PLUS_TEXT` | Plan 2D + Programme | **SUPPORTED** | ResPlan + Programme | Plan vectoriel confronté aux besoins de la famille. |
| `PLAN_PLUS_3D` | Plan 2D + Maquette 3D | **SUPPORTED** | ResBIM (2D + IFC) | Couplage certifié unit_000 à unit_102 (murs, ouvertures, niveaux). |
| `IMAGE_PLUS_TEXT` | Image + Programme | **SUPPORTED** | StructScan3D + Programme | Relevé photographique in situ + cahier des charges PMR. |
| `IMAGE_PLUS_PLAN_PLUS_TEXT`| Triplet Image+Plan+Texte | **NOT_SUPPORTED** | *Absence de triplet certifié* | Aucun projet du RAW ne dispose à la fois d'une photo, d'un plan et d'un texte. |
| `BIM_PLUS_PLAN` | IFC + Plan 2D | **SUPPORTED** | ResBIM | Alignement maquette IFC et cartouche plan d'architecte. |
| `MULTIMODAL_PROJECT_REASONING`| Multimodal Complet | **SUPPORTED** | MMMU Architecture | Questions multimodales expertes du benchmark. |

---

## 3. Recommandation pour les Vagues Ultérieures
1. **Sanctuarisation des 18 tâches NOT_SUPPORTED** : Aucune génération synthétique ou slot-filling ne doit être tentée pour ces tâches tant que les données appropriées (ex: triplets complets, variantes A/B, plans de réseaux électriques) ne sont pas intégrées dans le RAW.
2. **Priorité d'enrichissement pour Wave 2** : Transformer les 23 tâches `PARTIALLY_SUPPORTED` en `SUPPORTED` par l'acquisition de données complémentaires annotées.
