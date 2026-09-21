# ARCHI-AI — Rapport de Réparation Approfondie des Générateurs (`GENERATOR_REPAIR_REPORT.md`)

> **Date d'élaboration :** 21 September 2026 à 18:20:00 UTC  
> **Auditeur Technique :** Assistant Spécialiste ARCHI-AI  
> **Objectif :** Documenter pour chacun des 9 générateurs du moteur de supervision la défaillance observée, les exemples concrets, la cause racine structurelle et la réparation déterministe apportée.

---

## 1. `floorplan_gen.py` (Plans 2D, Topologie & Circulations)

### GENERATOR
`FloorplanGenerator` (`ARCHI_AI/dataset_tools/supervision/generators/floorplan_gen.py`)

### FAILURE MODE
Production systématique d'une description abstraite et invariable sur les 70 plans RPLAN sans citer la moindre pièce, sans donner de cote, et sans exploiter les canaux de segmentation couleur du masque sémantique.

### EXAMPLE(S)
`ARCHI_MASTER_RPLAN_42007_TASK_FLOORPLAN_READING` :
- *Réponse initiale :* `"Plan matriciel segmenté : parois, baies et espaces délimités... La partition spatiale délimite des zones fonctionnelles distinctes avec ouvertures identifiées."*
- *Problème :* Strictement identique sur tous les plans RPLAN. Cotes non cotées présentées implicitement comme complètes.

### ROOT CAUSE
Absence d'analyse du format raster RPLAN : le code vérifiait `if not rooms and visual:` et injectait immédiatement une chaîne template sans interroger la résolution (`256x256`), les canaux sémantiques réels (`doors_green`, `walls_red`, `rooms_white`), ni expliciter le statut `UNKNOWN` pour les dimensions métriques manquantes.

### FIX
- Intégration du décodage exact des 4 canaux couleur : parois rouges, baies vertes, pièces blanches, fond gris.
- Déclaration formelle du statut `UNKNOWN` pour les cotes millimétriques vectorielles non résolues sur l'image matricielle.
- Exploitation approfondie de ResPlan : extraction des pièces réelles (`living`, `bedrooms`, `bathrooms`), du graphe d'adjacence (`ROOM_TOPOLOGY`) et du repérage de la porte d'entrée (`CIRCULATION_ANALYSIS`).

---

## 2. `spatial_gen.py` (Scènes 3D, Scene Graphs & Relations Spatiales)

### GENERATOR
`SpatialGenerator` (`ARCHI_AI/dataset_tools/supervision/generators/spatial_gen.py`)

### FAILURE MODE
Prise arbitraire des deux premiers objets de la liste pour la tâche `OBJECT_RELATION`, avec affirmation péremptoire qu'ils sont *"positionnés en vis-à-vis / proximité dans la même zone d'usage"* sans aucun calcul spatial réel.

### EXAMPLE(S)
`ARCHI_MASTER_IL3D_scene_0104_TASK_OBJECT_RELATION` :
- *Réponse initiale :* `"Le/la exercise_rack-0 et le/la storage_bench-0 sont positionnés en vis-à-vis / proximité dans la même zone d'usage... Cette proximité crée une synergie fonctionnelle directe."*
- *Problème :* Les deux objets étaient en réalité situés aux deux extrémités opposées de la pièce à plus de 7 mètres de distance ($x_1=6.8, x_2=0.247$) !

### ROOT CAUSE
Laxisme algorithmique dans la méthode `generate()` : affectation `o1 = obj_labels[0]`, `o2 = obj_labels[1]` et injection d'un texte fixe sans lire les champs `position: [x, y, z]` pourtant extraits et disponibles dans le record.

### FIX
- Création d'une fonction mathématique déterministe `compute_euclidean_distance(pos1, pos2)`.
- Fonction `qualify_spatial_relation(o1, o2)` calculant la distance euclidienne $d = \sqrt{\Delta x^2 + \Delta y^2 + \Delta z^2}$ et les vecteurs directeurs ($\Delta x$ latéral, $\Delta y$ élévation, $\Delta z$ profondeur).
- Qualification stricte des paliers ergonomiques : contiguïté directe ($d < 1.0$ m), dégagement intermédiaire ($1.0 \le d \le 2.5$ m), ou séparation éloignée ($d > 2.5$ m). Si coordonnées absentes : `UNKNOWN`.

---

## 3. `ergonomics_gen.py` (Ergonomie, Normes PMR & Cotes Anthropométriques)

### GENERATOR
`ErgonomicsGenerator` (`ARCHI_AI/dataset_tools/supervision/generators/ergonomics_gen.py`)

### FAILURE MODE
Injection de la mention littérale `(soit None m)` dans 25 réponses d'ergonomie et dans `ground_truth.normalized_value`. Surcotation systématique de la tâche unitaire `CLEARANCE_CHECK` étiquetée `L3_ANALYSE`.

### EXAMPLE(S)
`ARCHI_MASTER_ERGO_circulations_couloir_personne_seule_TASK_CLEARANCE_CHECK` :
- *Réponse initiale :* `"Standard anthropométrique : valeur originale 90 cm (soit None m) selon Synthèse des standards d'ergonomie..."*
- *Ground Truth :* `{"original_value": 90, "original_unit": "cm", "normalized_value": null}`

### ROOT CAUSE
Désalignement de clé de dictionnaire : le préprocesseur stockait la valeur dans `normalized_si_value`, alors que le générateur cherchait `normalized_value` ou `value_m`. La variable restait `None` et était concaténée sans vérification.

### FIX
- Pipeline numérique certifié : extraction de `original_value`, détection de `original_unit`, conversion déterministe en mètres ($cm/100$, $mm/1000$) et validation anti-placeholder.
- Test unitaire d'intégrité interdisant formellement `None`, `NaN`, `inf` ou chaîne vide.
- Recalibration de `CLEARANCE_CHECK` au niveau cognitif exact : `L1_RECONNAISSANCE` (requête de cote unitaire).

---

## 4. `bim_gen.py` (Maquettes Numériques IFC & BIM QA)

### GENERATOR
`BimGenerator` (`ARCHI_AI/dataset_tools/supervision/generators/bim_gen.py`)

### FAILURE MODE
Récitation mot pour mot du cours théorique buildingSMART (`IfcProject → IfcSite → IfcBuilding → IfcBuildingStorey`) sur 70 maquettes distinctes, sans extraire les vrais étages ni les quantitatifs d'éléments réels.

### EXAMPLE(S)
`ARCHI_MASTER_CORE_BUILDINGSMART_IFC_Building-Architecture_TASK_BIM_SPATIAL_HIERARCHY` :
- *Réponse initiale :* `"L'arborescence spatiale organise le modèle selon la séquence canonique : IfcProject → IfcSite → IfcBuilding → IfcBuildingStorey. Chaque élément architectural est rattaché à son niveau de plancher respectif..."*

### ROOT CAUSE
Clé d'accès incorrecte : le générateur appelait `record.get("bim_ifc", {})` alors que les fichiers traités contenaient la clé `record.get("bim", {})`. Le dictionnaire résultant était vide, forçant le repli sur le texte théorique statique.

### FIX
- Implémentation des 4 helpers d'accès requis : `get_entity()`, `get_property()`, `get_relationship()`, `get_spatial_container()`.
- Extraction des étages effectifs (`['00 groundfloor']`, `['Level 0', 'Level 1']`), des espaces réels (`['living room', 'entry hall']`), et des quantitatifs d'éléments (`element_counts`).

---

## 5. `multimodal_cross_gen.py` (Appariements Croisés 2D ↔ 3D & Multimodalité)

### GENERATOR
`MultimodalCrossGenerator` (`ARCHI_AI/dataset_tools/supervision/generators/multimodal_cross_gen.py`)

### FAILURE MODE
Fausse multimodalité (`FAKE_MULTIMODAL`) : 25 exemples `IMAGE_PLUS_TEXT` ne comportaient aucun texte dans `inputs.text_contexts`, tout en affirmant dans la réponse évaluer des "fiches descriptives". Tâches `PLAN_PLUS_3D` sans réelle confrontation 2D/3D.

### EXAMPLE(S)
`ARCHI_MASTER_STRUCTSCAN_appt_harr_s10_00000_TASK_IMAGE_PLUS_TEXT` :
- *Inputs réels :* `{"images": [{"path": "..."}], "plans": [], "geometries": [], "text_contexts": []}`
- *Réponse initiale :* `"La concordance entre perception visuelle et fiches descriptives valide la qualité perçue de l'ouvrage."` (Fiche inexistante !).

### ROOT CAUSE
Génération de tâches annoncées bimodales sans construction préalable de la seconde modalité.

### FIX
- Pour `IMAGE_PLUS_TEXT` : injection obligatoire d'un cahier des charges textuel authentique (programme fonctionnel, exigences PMR, dégagements prescrits) dans `inputs.text_contexts`.
- Pour `PLAN_PLUS_3D` : création d'un cache de couplage ResBIM (`unit_000` à `unit_102`) reliant directement le plan 2D vectoriel et le modèle 3D IFC correspondant (niveaux, murs, portes, fenêtres).
- Ajout de `PLAN_PLUS_TEXT` reliant le plan 2D au programme de rénovation client.

---

## 6. `materials_gen.py` (Matériaux PBR & Shaders Physiques)

### GENERATOR
`MaterialsGenerator` (`ARCHI_AI/dataset_tools/supervision/generators/materials_gen.py`)

### FAILURE MODE
Prescription stéréotypée identique pour tous les matériaux : *"Ce matériau convient pour des surfaces de type sol ou doublage mural... L'association avec des matériaux lisses en contrepoint crée un contraste tactile recherché."*

### EXAMPLE(S)
`ARCHI_MASTER_AMBIENTCG_Asphalt033_TASK_MATERIAL_APPLICATION` et `ARCHI_MASTER_POLYHAVEN_wood_floor_TASK_MATERIAL_APPLICATION` :
- Deux matériaux radicalement opposés (asphalte extérieur vs parquet bois noble intérieur) recevaient la même recommandation de doublage mural avec contrepoint lisse.

### ROOT CAUSE
Absence de discrimination sémantique par famille de matériau.

### FIX
- Module `get_material_context()` analysant la catégorie et les tags du matériau : bois (confort thermique, proscrire en pièce d'eau sans joint pont de bateau), marbre/pierre (noblesse, traitement hydrofuge requis), métal (finesse de section, châssis verrière), carrelage (norme de glissance R10/PN12 pour pièce humide), tissu (absorption phonique, test Martindale).

---

## 7. `lighting_gen.py` (Éclairage, Photométrie HDRI & Ambiances)

### GENERATOR
`LightingGenerator` (`ARCHI_AI/dataset_tools/supervision/generators/lighting_gen.py`)

### FAILURE MODE
Répétition mot pour mot du diagnostic d'ambiance sur 80 exemples : *"L'apport lumineux génère des ombres nettes ou diffuses adaptées à la mise en scène spatiale."*

### EXAMPLE(S)
`ARCHI_MASTER_POLYHAVEN_aarfontein_dawn_2_TASK_LIGHTING_ANALYSIS` (lever de soleil doux) et `aarfontein_dirt_road` (plein soleil éblouissant de midi) recevaient la même phrase neutre.

### ROOT CAUSE
Mauvaise extraction des métadonnées : le code cherchait `kelvin_estimate` au lieu de `kelvin_temperature`, trouvant `None` et tombant dans le texte par défaut.

### FIX
- Extraction exacte de `kelvin_temperature`, `time_of_day`, `contrast` et `weather`.
- Qualification déterministe des ombres (vives et nettes si ciel dégagé/contraste haut, diffuses et adoucies si couvert/brumeux).
- Analyse de la température de couleur (chaude < 4 500 K, neutre 4 500–6 000 K, froide > 6 000 K) et de la pénétration diurne selon l'indice EV.

---

## 8. `critique_pedagogy_gen.py` (Critique d'Atelier & Pédagogie Maïeutique)

### GENERATOR
`CritiquePedagogyGenerator` (`ARCHI_AI/dataset_tools/supervision/generators/critique_pedagogy_gen.py`)

### FAILURE MODE
- `PROJECT_CRITIQUE` : imposition systématique du même défaut ("manque de filtre spatial") et de la même solution ("claustra ajouré ou meuble double-face") sur tous les plans.
- `TRADEOFF_ANALYSIS` : invention d'un "salon cathédrale" et d'une "verrière atelier" même sur un T2 standard.
- `GUIDED_REASONING` : conteneur `inputs` totalement vide (`{}`).

### EXAMPLE(S)
`ARCHI_MASTER_RESPLAN_014433_TASK_PROJECT_CRITIQUE` et `ARCHI_MASTER_RESPLAN_014433_TASK_GUIDED_REASONING`.

### ROOT CAUSE
Templates statiques non conditionnés aux polygones vectoriels et absence de remplissage de `ModalInputs`.

### FIX
- Critique conditionnée aux métriques réelles du plan : détection des liaisons directes séjour-chambre (vulnérabilité acoustique réelle), calcul du ratio surfacique jour/nuit.
- Pédagogie maïeutique contextualisée : injection de la notion de studio, du contexte de projet, du problème spatial et du niveau étudiant dans `inputs.text_contexts` (zéro input vide).
- `TRADEOFF_ANALYSIS` requérant au moins 2 contraintes explicites contradictoires pour valider la complexité L6.

---

## 9. `design_history_gen.py` (Histoire du Design & Collections Patrimoniales)

### GENERATOR
`DesignHistoryGenerator` (`ARCHI_AI/dataset_tools/supervision/generators/design_history_gen.py`)

### FAILURE MODE
Bien que globalement conforme, risque de questions redondantes sur les pièces ne disposant pas de date de création précise ou de description de matière complète.

### ROOT CAUSE
Absence de filtrage des notices trop laconiques de collections muséales.

### FIX
- Maintien de l'étanchéité et de l'ancrage documentaire vérifié (MoMA & The Met).
- Remplissage rigoureux des métadonnées de collection dans `evidence` et assignation stricte à la destination `RAG`.
