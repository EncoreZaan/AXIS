# ARCHI-AI — Rapport d'Audit Qualitatif Approfondi : Wave 1 (`WAVE1_QUALITY_AUDIT.md`)

> **Date d'audit :** 21 September 2026 à 14:40:00 UTC  
> **Auditeur Cognitif :** Assistant Spécialiste ARCHI-AI  
> **Périmètre audité :** 939 exemples supervisés de Wave 1 (619 train, 270 validation, 50 benchmark isolé)  
> **Statut initial :** 905 PASS, 34 WARNING, 0 REVIEW, 0 FAIL  
> **Question Centrale :** *"Les exemples sont-ils réellement bons pour apprendre à un modèle multimodal spécialisé en architecture intérieure, ou passent-ils simplement les validateurs automatiques ?"*  
> **Règle absolue :** Aucun entraînement lancé, zéro RunPod, RAW immuable, aucune modification destructrice du dataset.

---

## 1. Diagnostic Global & Résumé Exécutif

L'audit approfondi de Wave 1 révèle une dichotomie frappante :
1. **Sur le plan syntaxique et formel :** Le dataset est techniquement irréprochable. Le schéma Pydantic est respecté à 100%, l'isolation train/validation/benchmark est mathématiquement étanche (zéro fuite inter-projets), et les 40 tests unitaires initiaux passent avec succès.
2. **Sur le plan cognitif et architectural réel :** Les validateurs de première génération (`ReferenceValidator`, `HallucinationValidator`, `EpistemicValidator`, `AntiSycophancyValidator`) ont laissé passer un volume considérable de **Faux PASS (451 exemples sur 905, soit 49.8%)**.

Ces défaillances qualitatives proviennent de l'architecture des générateurs initiaux, qui ont privilégié des **structures templates répétitives** (slot-filling) au détriment d'un raisonnement spatial profondément contextualisé :
- **Clichés génériques :** 401 exemples présentent des formulations stéréotypées (ex: 70 fois la même arborescence canonique IFC, 70 fois la même description de plan matriciel sans nommer les pièces, 32 fois la même recommandation de claustra ajouré).
- **Entrées manquantes :** 64 exemples possèdent un conteneur `inputs` totalement vide.
- **Pseudo-multimodalité :** 25 exemples de la tâche `IMAGE_PLUS_TEXT` ne comportent aucune entrée textuelle dans `inputs` et font référence à des fiches descriptives absentes.
- **Bugs d'interpolation numérique :** 25 exemples d'ergonomie contiennent la mention textuelle `(soit None m)` suite à une valeur normalisée non calculée.
- **Couverture restreinte :** Seules 22 tâches sur les 69 du catalogue officiel sont instanciées. 47 tâches ont 0 exemple dans Wave 1.

### Décision Qualité Consolidée sur Wave 1 :
- **RETAIN (Conforme & directement exploitable) :** **409 exemples (43.6 %)**
- **CORRECT (Potentiel élevé, correction déterministe immédiate) :** **25 exemples (2.7 %)**
- **REVIEW (Revue humaine / experte ou enrichissement requis) :** **416 exemples (44.3 %)**
- **EXCLUDE (À écarter impérativement du fine-tuning) :** **89 exemples (9.5 %)**

---

## 2. Échantillonnage Statistique Représentatif Audité

L'audit qualitatif s'est appuyé sur un échantillonnage déterministe et stratifié couvrant :
- **100% des 34 exemples WARNING** (audit exhaustif).
- **100% des 50 exemples du Benchmark sanctuarisé** (audit exhaustif).
- **100% des 37 exemples d'Ergonomie** (audit exhaustif).
- **100% des 32 exemples de Critique et 32 exemples de Pédagogie** (audit exhaustif).
- **Échantillon stratifié par Groupe de tâches A à L :**
  - Groupe A (Visual Understanding) : 25/25 audités (100%)
  - Groupe B (Floorplan) : 50/144 audités (34.7%)
  - Groupe C (Spatial 3D) : 50/150 audités (33.3%)
  - Groupe D (BIM/IFC) : 50/120 audités (41.7%)
  - Groupe E (Ergonomie) : 37/37 audités (100%)
  - Groupe F (Materials) : 40/110 audités (36.4%)
  - Groupe G (Lighting) : 30/80 audités (37.5%)
  - Groupe H (Design) : 30/90 audités (33.3%)
  - Groupe I (Critique) : 32/32 audités (100%)
  - Groupe J (Professional Reasoning) : 44/44 audités (100%)
  - Groupe K (Pedagogy) : 32/32 audités (100%)
  - Groupe L (Multimodal) : 75/75 audités (100%)
- **Total audité en profondeur : 475 exemples distincts (50.6% de Wave 1).**

---

## 3. Analyse Détaillée par Discipline Métier

### 3.1. Lecture de Plans 2D (Groupe B — 144 ex)
- **Points forts :** Les 64 exemples issus de `CORE_RESPLAN` sont remarquablement grounded : polygones Shapely exacts, surfaces calculées sans approximation, pièces authentiques (`living`, `bedroom`, `bathroom`).
- **Faiblesses majeures :**
  - Les 70 exemples issus de `CORE_RPLAN` utilisent un texte 100% template (`FLOORPLAN_READING`). La réponse affirme que les zones fonctionnelles sont délimitées sans en citer aucune, sans donner de dimensions, et sans exploiter la segmentation pourtant présente dans les masques d'origine.
  - Les 5 exemples de `CIRCULATION_ANALYSIS` sont trop rares (0.5% du dataset) alors qu'il s'agit du cœur de métier.

### 3.2. Espace 3D & Scene Graphs (Groupe C — 150 ex)
- **Points forts :** 75 exemples de `SCENE_GRAPH_REASONING` (`CORE_IL3D`) bénéficient d'un inventaire déterministe certifié des objets 3D avec boîtes englobantes réelles.
- **Faiblesses majeures :**
  - Les 75 exemples d'`OBJECT_RELATION` postulent arbitrairement que les deux premiers objets de la liste sont "en vis-à-vis / proximité dans la même zone d'usage" sans vérifier leurs coordonnées 3D ni calculer la distance euclidienne réelle. Cela produit des déductions aberrantes (ex: relation de proximité postulée entre des objets situés aux extrémités opposées d'une pièce).

### 3.3. BIM & Maquettes IFC (Groupe D — 120 ex)
- **Points forts :** Les 50 questions/réponses d'`IFC_QA` (`CORE_IFC_BENCH_QA`) sont authentiques, techniques et hautement pertinentes.
- **Faiblesses majeures :**
  - Les 70 exemples de `BIM_SPATIAL_HIERARCHY` répètent mot pour mot le cours théorique buildingSMART : `L'arborescence spatiale organise le modèle selon la séquence canonique : IfcProject → IfcSite → IfcBuilding → IfcBuildingStorey`.
  - Aucune extraction des étages réels (`IfcBuildingStorey.Name`), des hauteurs sous plafond réelles, ni des espaces (`IfcSpace`) propres au fichier IFC audité n'a été réalisée.

### 3.4. Ergonomie & Cotes Anthropométriques (Groupe E — 37 ex)
- **Bug critique de formatage :** 25 exemples de `CLEARANCE_CHECK` affichent : `valeur originale 90 cm (soit None m)`. Le champ `normalized_value` n'a pas été calculé lors de la transformation. Ce bug a été validé `PASS` par le QualityGate initial car `None` n'était pas testé comme chaîne interdite.
- **Calibration :** La tâche `CLEARANCE_CHECK` est étiquetée `L3_ANALYSE` alors qu'elle consiste en une simple restitution d'une valeur issue d'un tableau (complexité cognitive L1).

### 3.5. Matériaux & Shaders PBR (Groupe F — 110 ex)
- **Points forts :** `PBR_REASONING` (55 ex) ancre parfaitement les maps disponibles (`color`, `roughness`, `normal`, `displacement`) et l'échelle physique en mètres (`2.8 m x 2.8 m`).
- **Faiblesses :** `MATERIAL_APPLICATION` (55 ex) applique la même recommandation stéréotypée : *"Ce matériau convient pour des surfaces de type sol ou doublage mural... L'association avec des matériaux lisses en contrepoint crée un contraste tactile recherché"*. Aucune contrainte spécifique de pièce (cuisine, salle de bain, séjour) n'est discriminée.

### 3.6. Lumière & Ambiances HDRI (Groupe G — 80 ex)
- **Points forts :** Extraction rigoureuse des valeurs d'exposition EV et des températures Kelvin mesurées.
- **Faiblesses :** Répétition textuelle stricte du diagnostic d'ambiance sur les 80 exemples (`"L'apport lumineux génère des ombres nettes ou diffuses adaptées à la mise en scène spatiale"`).

### 3.7. Histoire du Design & Collections Muséales (Groupe H — 90 ex)
- **Points forts :** 100% conformes et vérifiables. Les notices du MoMA et du Met (`Otto Wagner`, `Christian de Portzamparc`, etc.) sont authentiques, sans aucune attribution inventée. Destination cognitive `RAG` et `FINETUNE` parfaitement calibrée.

### 3.8. Critique d'Atelier & Pédagogie (Groupes I & K — 64 ex)
- **Diagnostic critique :** Les réponses ont été construites par un générateur statique (`critique_pedagogy_gen.py`).
  - Pour `PROJECT_CRITIQUE` (32 ex) : tous les plans se voient attribuer le même défaut ("la transition entre l'entrée et l'espace de vie manque de filtre spatial") et la même solution ("intégrer un claustra ajouré").
  - Pour `TRADEOFF_ANALYSIS` (32 ex) : tous les plans reçoivent la même problématique d'un "salon cathédrale baigné de lumière" et d'une "verrière atelier", même s'il s'agit d'un petit appartement deux pièces ordinaire.
  - Pour `GUIDED_REASONING` (32 ex) : tous les plans sont questionnés sur un prétendu "goulot central" où deux personnes se croiseraient.
  - De surcroît, les `inputs` de ces tâches dans les groupes J et K sont **totalement vides**.

### 3.9. Multimodalité Croisée (Groupe L — 75 ex)
- **Cas `IMAGE_PLUS_TEXT` (25 ex) :** Fausse multimodalité (`FAKE_MULTIMODAL`). L'objet `inputs` ne contient que le champ `images`. Le texte d'accompagnement (programme, contraintes) n'est pas présent.
- **Cas `CORE_MMMU_ARCHITECTURE` (50 ex) :** Affecté au split benchmark. Les réponses ne contiennent aucune analyse rédigée mais uniquement la lettre de l'option (`"Réponse certifiée du benchmark MMMU : A"`).

---

## 4. Audit Sanitaire du Benchmark Isolé (50 Exemples)

### 4.1. Étanchéité et Zéro Contamination
- **Vérification d'identifiants :** ZÉRO identifiant de projet partagé entre le benchmark et les splits train ou validation.
- **Vérification de questions :** ZÉRO chevauchement textuel de questions.
- **Isolation :** Parfaite et sanctuarisée.

### 4.2. Pertinence du Contenu pour l'Architecture Intérieure
Le benchmark actuel (100% issu de `CORE_MMMU_ARCHITECTURE`) pose un problème de fond :
- 33 questions sur 50 (66%) ont déclenché un `WARNING` du `HallucinationValidator` en raison de nombres non sourcés dans les options.
- Une part significative des questions relève du **génie civil lourd**, de la géodésie ou de la photogrammétrie aérienne (ex: calcul d'angles de triangulation par moindres carrés, flèche de déformation verticale d'un treillis P8.4, correction caténaire d'un ruban d'arpenteur à 20°C, prise de vue aérienne à 1 350 m d'altitude).
- **Conclusion d'audit :** Bien que ce benchmark mesure la robustesse académique globale en ingénierie/architecture, il **n'évalue pas directement les compétences spécifiques d'architecture intérieure** (circulations d'appartement, agencement de cuisine, ergonomie PMR, ambiances de matière, lecture de plans résidentiels).
- **Recommandation :** Conserver ce benchmark pour l'évaluation de résistance générale, mais créer un **Benchmark Spécialisé Architecture Intérieure (ArchiInt-Bench)** lors des prochaines étapes.

---

## 5. Bilan des Nouveaux Validateurs Intégrés

Suite aux constats d'audit, trois nouveaux validateurs ont été conçus et intégrés au moteur de supervision :

1. **`GenericAnswerValidator` :**
   - Intercepte les placeholders résiduels (`None m`).
   - Détecte les formulations stéréotypées répétitives (claustra ajouré, salon cathédrale, séquence canonique IFC, plan matriciel générique).
   - Statut : `REVIEW` ou `WARNING`.

2. **`MultimodalDependencyValidator` :**
   - Contrôle la présence effective de toutes les modalités annoncées par la tâche.
   - Détecte les cas `FAKE_MULTIMODAL` (ex: `IMAGE_PLUS_TEXT` orpheline de texte).
   - Statut : `REVIEW` ou `WARNING`.

3. **`DifficultyValidator` :**
   - Détecte les surévaluations de difficulté (ex: `CLEARANCE_CHECK` unitaire labellisée L3 au lieu de L1).
   - Détecte les tâches L6 dépourvues de matrice de contraintes réelles.
   - Statut : `WARNING`.

Ces 3 validateurs disposent d'une couverture de tests unitaires dédiée dans `ARCHI_AI/tests/test_audit_validators.py`. L'ensemble des 44 tests de la suite logicielle s'exécute avec un taux de réussite de **100%**.
