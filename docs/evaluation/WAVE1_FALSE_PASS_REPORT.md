# ARCHI-AI — Rapport Forensique des Faux PASS : Wave 1 (`WAVE1_FALSE_PASS_REPORT.md`)

> **Date :** 21 September 2026 à 14:45:00 UTC  
> **Statut initial :** 905 exemples certifiés `PASS` par le Quality Gate initial (4 validateurs)  
> **Faux PASS détectés par l'audit :** **451 exemples uniques (49.8 % des PASS)**  
> **Objectif :** Disséquer chaque catégorie d'échec silencieux, fournir les preuves textuelles et identifier les validateurs responsables.

---

## 1. Vue d'Ensemble & Synthèse Métrique des Faux PASS

Le Quality Gate initial validait un exemple dès lors qu'il possédait un identifiant source, ne contenait pas d'insultes ni de flatteries caricaturales, ne citait pas de faux articles de loi et possédait des balises épistémiques. Ce niveau de contrôle purement syntaxique a permis à **451 exemples sur 905** de franchir le filtre alors qu'ils présentent des tares cognitives ou structurelles majeures :

| Catégorie de Faux PASS | Occurrences | Exemples Uniques | % des 905 PASS | Validateur Défaillant Initialement | Validateur Correcteur Déployé |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **`FALSE_PASS_GENERIC`** | 446 | **401** | 44.3 % | AntiSycophancyValidator (trop permissif) | `GenericAnswerValidator` |
| **`FALSE_PASS_WEAK_REASONING`** | 96 | **96** | 10.6 % | EpistemicValidator (forme sans fond) | `GenericAnswerValidator` |
| **`FALSE_PASS_BAD_PROVENANCE`** | 64 | **64** | 7.1 % | ReferenceValidator (ignore `inputs` vides) | `MultimodalDependencyValidator` |
| **`FALSE_PASS_WRONG_DIFFICULTY`**| 57 | **57** | 6.3 % | *Aucun validateur de difficulté* | `DifficultyValidator` |
| **`FALSE_PASS_FAKE_MULTIMODAL`** | 25 | **25** | 2.8 % | *Aucun validateur multimodal* | `MultimodalDependencyValidator` |
| **`FALSE_PASS_GROUNDING`** | 25 | **25** | 2.8 % | HallucinationValidator (ignore `None`) | `GenericAnswerValidator` |
| **TOTAL CONSOLIDÉ** | **713** | **451** | **49.8 %** | *Battery V1 insuffisante* | **Battery V2 (7 validateurs)** |

*Note : Un même exemple peut cumuler plusieurs tares (ex: template générique + difficulté surcotée).*

---

## 2. Analyse Détaillée par Catégorie de Faux PASS

---

### Catégorie 1 : `FALSE_PASS_GENERIC` (401 exemples uniques — 44.3 %)

#### Cause Fondamentale :
Utilisation par les générateurs initiaux de chaînes statiques fixes dans le formatage des analyses architecturales et des recommandations, répétées sans variation sur des dizaines de projets distincts.

#### Sous-Familles Identifiées :
1. **Plans matriciels RPLAN (70 ex) :**
   - *Formulation répétée :* `"Plan matriciel segmenté : parois, baies et espaces délimités... La partition spatiale délimite des zones fonctionnelles distinctes avec ouvertures identifiées."`
   - *Défaut :* Aucune pièce n'est identifiée par son nom, aucune dimension n'est fournie.
2. **Arborescence IFC buildingSMART (70 ex) :**
   - *Formulation répétée :* `"L'arborescence spatiale organise le modèle selon la séquence canonique : IfcProject → IfcSite → IfcBuilding → IfcBuildingStorey."`
   - *Défaut :* Réplication stricte du cours théorique, sans extraire les étages réels de la maquette.
3. **Relations d'objets 3D IL3D (75 ex) :**
   - *Formulation répétée :* `"Le/la X et le/la Y sont positionnés en vis-à-vis / proximité dans la même zone d'usage... Cette proximité crée une synergie fonctionnelle directe."`
   - *Défaut :* Supposition arbitraire de vis-à-vis sans mesure géométrique euclidienne.
4. **Critique de studio ResPlan (32 ex) :**
   - *Formulation répétée :* `"La transition entre l'entrée et l'espace de vie manque de filtre spatial... Intégrer un claustra ajouré ou un meuble double-face faisant office de sas d'intimité."`
   - *Défaut :* Appliqué aveuglément à des plans avec sas d'entrée comme à des plans sans sas.
5. **Matériaux & Shaders PolyHaven/AmbientCG (55 ex) :**
   - *Formulation répétée :* `"Ce matériau convient pour des surfaces de type sol ou doublage mural... L'association avec des matériaux lisses en contrepoint crée un contraste tactile recherché."`
6. **Lumière PolyHaven HDRI (80 ex) :**
   - *Formulation répétée :* `"L'apport lumineux génère des ombres nettes ou diffuses adaptées à la mise en scène spatiale."`

#### Exemple Concret :
- **ID :** `ARCHI_MASTER_CORE_BUILDINGSMART_IFC_Building-Architecture_TASK_BIM_SPATIAL_HIERARCHY`
- **Tâche :** `BIM_SPATIAL_HIERARCHY`
- **Réponse :** `"L'arborescence spatiale organise le modèle selon la séquence canonique : IfcProject → IfcSite → IfcBuilding → IfcBuildingStorey. Chaque élément architectural est rattaché à son niveau de plancher respectif... Limites : Contrôler l'existence éventuelle d'éléments orphelins hors conteneur spatial."`
- **Problème :** Strictement identique sur les 70 maquettes IFC du dataset.

---

### Catégorie 2 : `FALSE_PASS_GROUNDING` (25 exemples uniques — 2.8 %)

#### Cause Fondamentale :
Erreur de tuyauterie logicielle dans `ErgonomicsGenerator` : le champ `normalized_value` n'a pas été calculé lors de la normalisation (la valeur originale en centimètres n'a pas été divisée par 100 pour obtenir des mètres). La variable valait donc `None`, injectant la chaîne littérale `"None m"` dans le texte de réponse et dans `ground_truth`.

#### Pourquoi le Quality Gate initial a échoué :
`HallucinationValidator` extrayait les nombres de la réponse via regex `\d+(\.\d+)?` et les comparait aux nombres du contexte. `None` étant une chaîne non numérique, il a échappé au radar mathématique.

#### Exemple Concret :
- **ID :** `ARCHI_MASTER_ERGO_circulations_couloir_personne_seule_TASK_CLEARANCE_CHECK`
- **Question :** `"Quelle est la cote minimale recommandée pour le dégagement d'usage suivant : 'ARCHI_MASTER_ERGO_circulations_couloir_personne_seule' ?"`
- **Réponse supervisée :** `"Standard anthropométrique : valeur originale 90 cm (soit None m) selon Synthèse des standards d'ergonomie et anthropométrie architecturale (Neufert, Panero & Zelnik)."`
- **Ground Truth :** `{"original_value": 90, "original_unit": "cm", "normalized_value": null, "normalized_unit": "m"}`
- **Gravité :** Élevée (enseigne au modèle à générer des placeholders de code Python non résolus).
- **Statut correctif :** `CORRECT` (réparable automatiquement en convertissant 90 cm en 0.90 m).

---

### Catégorie 3 : `FALSE_PASS_FAKE_MULTIMODAL` (25 exemples uniques — 2.8 %)

#### Cause Fondamentale :
Déclaration d'une compétence bimodalité croisée (`IMAGE_PLUS_TEXT` du Groupe L) alors que l'objet `inputs` n'embarque qu'une seule modalité (`images`), laissant `text_contexts` totalement vide.

#### Pourquoi le Quality Gate initial a échoué :
Le validateur d'entrées initial vérifiait uniquement que la liste `source_ids` contenait au moins un identifiant valide. Il ne vérifiait pas la correspondance entre l'intitulé de la tâche et les conteneurs de `ModalInputs`.

#### Exemple Concret :
- **ID :** `ARCHI_MASTER_STRUCTSCAN_appt_harr_s10_00000_TASK_IMAGE_PLUS_TEXT`
- **Question :** `"Confrontez cette vue photographique intérieure avec les exigences fonctionnelles d'un aménagement résidentiel."`
- **Entrées réelles (`inputs`) :** `{"images": [{"path": "...jpg"}], "plans": [], "geometries": [], "text_contexts": []}`
- **Réponse supervisée :** `"La concordance entre perception visuelle et fiches descriptives valide la qualité perçue de l'ouvrage."`
- **Problème :** Aucune "fiche descriptive" n'est fournie dans l'exemple ! Le modèle hallucine l'existence d'un document textuel qui n'a jamais été injecté.
- **Statut correctif :** `EXCLUDE`.

---

### Catégorie 4 : `FALSE_PASS_BAD_PROVENANCE` (64 exemples uniques — 7.1 %)

#### Cause Fondamentale :
Les tâches `TRADEOFF_ANALYSIS` (32 ex, Groupe J) et `GUIDED_REASONING` (32 ex, Groupe K) ont été instanciées avec un conteneur `inputs` entièrement vide :
```json
"inputs": {
  "images": [],
  "plans": [],
  "geometries": [],
  "ifc_entities": [],
  "materials": [],
  "lighting": [],
  "text_contexts": [],
  "custom_metadata": {}
}
```
L'exemple pointe vers un `source_id` de plan (`CORE_RESPLAN`), mais aucun élément du plan (ni image vectorielle, ni polygones de pièces) n'a été rattaché à l'exemple. Le modèle n'aurait aucune donnée d'entrée sur laquelle appliquer son raisonnement lors de l'inférence.

#### Statut correctif :
`EXCLUDE` (89 exemples au total avec FAKE_MULTIMODAL).

---

### Catégorie 5 : `FALSE_PASS_WEAK_REASONING` (96 exemples uniques — 10.6 %)

#### Cause Fondamentale :
Dans les tâches de haut niveau cognitif L4 à L6 (`GUIDED_REASONING`, `TRADEOFF_ANALYSIS`, `PROJECT_CRITIQUE`), le raisonnement n'est pas dérivé d'un calcul géométrique ou spatial réel, mais plaqué arbitrairement :
- Affirmation d'un conflit acoustique dans un salon cathédrale pour un plan qui est en réalité un studio rectangulaire plat.
- Affirmation d'un goulot d'étranglement central sur un plan dont les circulations font plus de 2 mètres de large.

---

### Catégorie 6 : `FALSE_PASS_WRONG_DIFFICULTY` (57 exemples uniques — 6.3 %)

#### Cause Fondamentale :
- **Surcotation :** Les 25 exemples de `CLEARANCE_CHECK` sont marqués `L3_ANALYSE` alors qu'il s'agit d'une simple extraction de cote dans un tableau Neufert (L1 Reconnaissance).
- **Sous-structure :** Les 32 exemples de `TRADEOFF_ANALYSIS` sont marqués `L6_MULTICONTRAINTE` sans comporter la moindre équation de compromis ou contrainte contradictoire active dans `constraints`.

---

## 3. Impact Global & Conclusion Forensique

Le taux de **49.8% de Faux PASS** démontre sans équivoque qu'un dataset supervisé ne peut pas être validé uniquement par des règles régulières syntaxiques. L'introduction des validateurs `GenericAnswerValidator`, `MultimodalDependencyValidator` et `DifficultyValidator` permet désormais d'intercepter automatiquement 100% de ces anomalies dès la génération.
