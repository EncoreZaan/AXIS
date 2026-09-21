# ARCHI-AI — Rapport d'Architecture du Supervision Engine (`SUPERVISION_ENGINE_REPORT`)

> **Date de génération :** 21 September 2026 à 18:13:02 UTC  
> **Statut :** SUPERVISION ENGINE OPÉRATIONNEL & CERTIFIÉ  
> **Conformité stricte :** 69 tâches répertoriées, 12 groupes, taxonomie L1 à L6, étanchéité zéro fuite  
> **Intégrité RAW :** Inaltéré, FloorPlanCAD gelé (`LEGAL_REVIEW_REQUIRED`)  
> **Règle d'or :** Zéro entraînement de modèle, zéro RunPod, zéro modification des poids  

---

## 1. Vue d'Ensemble & Mission du Supervision Engine

Le **Supervision Engine** d'ARCHI-AI constitue le sous-système de transformation cognitive. Son rôle est de convertir le Master Dataset intermédiaire (105 441 éléments normalisés) en **données supervisées de haute qualité** pour le fine-tuning multimodal, l'indexation RAG, et les outils déterministes, tout en prévenant formellement l'hallucination et la complaisance sycophante.

### Principes Architecturaux Enforcés

1. **Routage Cognitif Différencié :** Aucune donnée n'est injectée aveuglément dans les poids. Chaque item est routé selon sa nature (`FINETUNE`, `RAG`, `TOOL`, `BENCHMARK`, `MULTIUSE`, `HOLDOUT`).
2. **Standard Épistémique Rigoureux :** Séparation formelle entre `OBSERVATION` (fait tangible), `INTERPRÉTATION` (lecture experte), `INFÉRENCE` (combinaison), `UNKNOWN` (donnée absente), et `TO_VERIFY` (calcul d'outil).
3. **Supervision Déterministe :** Vérificateurs mathématiques exacts (géométrie Shapely pour les surfaces, graphes de scène 3D pour le comptage, parseur IFC pour les classes bâties, cotes anthropométriques avec conversions SI).
4. **Anti-Sycophantie Systématique :** Interdiction des formules de complaisance vide ("très beau projet", "c'est parfait"). Diagnostic objectif obligatoire avec points de friction et recommandations constructives.
5. **Éthique de Partition :** Isolation stricte des scènes et projets pour interdire toute fuite entre les jeux d'apprentissage et d'évaluation aveugle.

---

## 2. Catalogue Formel des 69 Tâches (Groupes A à L)

Le catalogue formalise l'ensemble des compétences de l'architecture intérieure :

| Groupe | Intitulé | Nombre de Tâches | Compétences Clés |
| :--- | :--- | :---: | :--- |
| **A** | **Visual Understanding** | 7 tâches | Vision, identification matériaux/mobilier, style, relations spatiales |
| **B** | **Floorplan** | 9 tâches | Lecture plan 2D, identification pièces, topologie, circulation, métrés |
| **C** | **Spatial / 3D** | 5 tâches | Scene graph 3D, relations objet-objet, aménagement volumétrique |
| **D** | **BIM / IFC** | 6 tâches | Classes IFC, propriétés, arborescence spatiale, IFC-Bench QA |
| **E** | **Ergonomie** | 5 tâches | Dégagements, largeurs de passage, cotes mobilier, accessibilité PMR |
| **F** | **Materials** | 4 tâches | Shaders PBR, canaux albedo/roughness, échelle métrique, prescription |
| **G** | **Lighting** | 4 tâches | Températures Kelvin, photométrie EV, éclairage naturel et artificiel |
| **H** | **Design & Histoire** | 5 tâches | 40 styles, histoire du design (MoMA/Met), cohérence matière/style |
| **I** | **Critique Architecturale** | 6 tâches | Diagnostic forces/faiblesses, conflits de conception, alternatives |
| **J** | **Professional Reasoning**| 6 tâches | Analyse programme, contraintes multiples, arbitrages et faisabilité |
| **K** | **Pédagogie de Studio** | 5 tâches | Explication didactique, maïeutique guidée pas-à-pas (Studio Tutor) |
| **L** | **Multimodalité Croisée** | 7 tâches | Triplet Image+Plan+Programme, Plan+3D (ResBIM), BIM+Plan |
| **TOTAL** | **Architecture Intérieure** | **69 tâches** | **Couverture intégrale des cas d'usage réels** |

---

## 3. Matrice Source → Capacité → Destinations

Le routage automatique oriente les données sans forçage :

- `CORE_RESPLAN` → Plans 2D, topologie, circulations, métrés (`MULTIUSE : FINETUNE + TOOL`)
- `CORE_RPLAN` → Segmentation et zonage fonctionnel (`FINETUNE`)
- `CORE_RESBIM_2D` & `CORE_RESBIM_IFC` → Appariement 2D/3D et BIM (`MULTIUSE`)
- `CORE_IL3D` & `CORE_STRUCTSCAN3D` → Scènes 3D, relations spatiales (`FINETUNE`)
- `CORE_BUILDINGSMART` & `CORE_IFC_BENCH` → Arborescence spatiale et BIM QA (`MULTIUSE / BENCHMARK`)
- `CORE_AMBIENTCG` & `CORE_POLYHAVEN_MATERIALS` → PBR et textures physiques (`FINETUNE + RAG`)
- `CORE_POLYHAVEN_LIGHTING` → Photométrie HDRI et ambiances (`FINETUNE`)
- `CORE_ERGONOMIE` → Dégagements et cotes d'usage (`TOOL + FINETUNE`)
- `CORE_NORMES_FR` → Réglementation PMR/ERP/CCH (`RAG + FINETUNE contrôlé`)
- `CORE_MOMA` & `CORE_MET` → Notices patrimoniales et design (`RAG + FINETUNE`)
- `CORE_FLOORPLANCAD` → **GELÉ / EXCLU** (`LEGAL_REVIEW_REQUIRED`)

---

## 4. Composants Algorithmiques & Vérificateurs

1. **`GeometryVerifier` :** Détermination déterministe des surfaces en m² à partir des coordonnées de polygones via Shapely, calculs de distances euclidiennes et vérification de gabarits.
2. **`SceneGraphVerifier` :** Validation du décompte exact d'objets 3D et des positions relatives (gauche, droite, devant, derrière, dessus).
3. **`IfcVerifier` :** Contrôle des types d'éléments IFC et de la hiérarchie spatiale IfcProject → Storey.
4. **`ErgonomicsVerifier` :** Conservation de `original_value`, `original_unit`, `normalized_value`, `normalized_unit` et validation face aux seuils minimaux Neufert/Panero.
5. **`QualityGate` :** Batterie de 4 validateurs (`ReferenceValidator`, `HallucinationValidator`, `EpistemicValidator`, `AntiSycophancyValidator`) statuant `PASS`, `WARNING`, `REVIEW`, `FAIL`.
6. **`SplitManager` :** Hachage stable par identifiant de projet garantissant l'étanchéité absolue inter-partitions.
