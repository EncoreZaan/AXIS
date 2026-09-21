# ARCHI-AI — Audit Spécialisé de la Multimodalité : Wave 1 (`WAVE1_MULTIMODAL_AUDIT.md`)

> **Date d'audit :** 21 September 2026 à 14:50:00 UTC  
> **Auditeur Spécialiste :** Expert Vision & Multimodalité ARCHI-AI  
> **Question Clé :** *"La réponse utilise-t-elle réellement toutes les modalités nécessaires, ou peut-on supprimer l'image, le plan ou le texte sans changer la validité de la réponse ?"*  

---

## 1. Vue d'Ensemble des Modalités dans Wave 1

Pour former un modèle multimodal d'architecture intérieure (basé sur l'architecture bimodal/trimodal RWKV-7 World / Qwen2-VL), la qualité de l'alignement croisé entre le texte, l'image, le plan 2D vectoriel et le modèle 3D/IFC est déterminante.

### Distribution des Conteneurs dans `ModalInputs` (939 exemples) :
- `geometries` renseigné : **294 exemples** (31.3 %) — ResPlan, IL3D
- `materials` renseigné : **110 exemples** (11.7 %) — AmbientCG, PolyHaven Materials
- `ifc_entities` renseigné : **120 exemples** (12.8 %) — buildingSMART, IFC-Bench
- `images` renseigné : **100 exemples** (10.6 %) — StructScan3D, MMMU
- `text_contexts` renseigné : **127 exemples** (13.5 %) — MoMA, Met, Normes FR, IFC-Bench QA
- `lighting` renseigné : **80 exemples** (8.5 %) — PolyHaven Lighting
- `plans` renseigné : **80 exemples** (8.5 %) — RPLAN, ResBIM
- **Conteneurs totalement vides (`ModalInputs` vide) : 64 exemples (6.8 %)** — Groupes J et K

---

## 2. Détection Formelle des Cas FAKE_MULTIMODAL

Un exemple est qualifié de **`FAKE_MULTIMODAL`** lorsqu'il est étiqueté comme relevant d'une tâche croisée à plusieurs modalités, mais que :
1. Une des modalités requises est absente de l'objet `inputs`.
2. OU la réponse pourrait être produite sans examiner l'un des documents fournis (*test du masquage modal*).

### Cas Flagrant : Tâche `IMAGE_PLUS_TEXT` (25 exemples — Groupe L)
- **Définition théorique du catalogue (L-65) :** Confronter une photographie d'espace avec un cahier des charges textuel (programme client, contraintes dimensionnelles ou descriptif sommaire).
- **Réalité dans Wave 1 :**
  - `inputs.images` : `[{"path": "..."}]` (présent).
  - `inputs.text_contexts` : `[]` (**STRICTEMENT VIDE**).
  - `inputs.plans` : `[]` (vide).
- **Analyse du texte de la réponse :**
  - Phrase clé générée : *"La concordance entre perception visuelle et fiches descriptives valide la qualité perçue de l'ouvrage."*
  - **Verdict forensique :** Le générateur `multimodal_cross_gen.py` prétend comparer l'image à des "fiches descriptives", mais ces fiches n'ont jamais été injectées dans le record ! Le modèle apprendrait ainsi à prétendre vérifier des documents textuels inexistants.
  - **Sanction d'audit :** **`FAKE_MULTIMODAL` avéré → Statut `EXCLUDE`**.

---

## 3. Matrice de Couverture des Combinaisons Multimodales

Le catalogue théorique des 69 tâches prévoyait 7 tâches multimodales majeures dans le Groupe L. Voici l'état des lieux réel dans Wave 1 :

| Combinaison Requise | Tâche Catalogue | Présence Wave 1 | Statut Qualitatif | Problème Détecté |
| :--- | :--- | :---: | :---: | :--- |
| **IMAGE + PLAN** | `IMAGE_PLUS_PLAN` (L-64) | **0 exemple** | *Non instancié* | Tâche totalement absente de Wave 1 |
| **IMAGE + TEXTE** | `IMAGE_PLUS_TEXT` (L-65) | **25 exemples** | **ÉCHEC CRITIQUE**| `FAKE_MULTIMODAL` (texte absent dans `inputs`) |
| **PLAN + TEXTE** | `PLAN_PLUS_TEXT` (L-66) | **0 exemple** | *Non instancié* | Tâche totalement absente de Wave 1 |
| **PLAN + 3D** | `PLAN_PLUS_3D` (L-67) | **0 exemple** | *Non instancié* | Non généré dans le split final |
| **IMAGE + PLAN + TEXTE**| `IMAGE_PLUS_PLAN_PLUS_TEXT` (L-68) | **0 exemple** | *Non instancié* | Tâche reine absente de Wave 1 |
| **BIM + PLAN** | `BIM_PLUS_PLAN` (L-69) | **0 exemple** | *Non instancié* | Tâche non instanciée |
| **EXAMEN MULTIMODAL** | `MULTIMODAL_PROJECT_REASONING` | **50 exemples** | **MITIGÉ** | Issu de MMMU Architecture (50% civil/géodésie) |
| **TOTAL GROUPE L** | **7 tâches théoriques** | **75 exemples** | **2 tâches sur 7**| **5 tâches à 0 exemple (71.4% de trou)** |

---

## 4. Audit du Test de Masquage Modal (Modal Ablation Test)

Pour évaluer si la multimodalité est authentique, nous avons soumis les exemples audités au **test de masquage** :

### Test 1 : Tâche `SCENE_GRAPH_REASONING` (Groupe C — 75 ex)
- **Entrées :** `inputs.geometries` (coordonnées 3D) + `inputs.images` (vue render).
- **Test :** Si on masque l'image, la réponse reste-t-elle calculable ?
  - *Résultat :* OUI. La réponse se base sur la liste textuelle des objets issue du graphe 3D. L'image n'est pas strictement exploitée pour décrire des textures ou des couleurs non présentes dans les métadonnées.
  - *Observation :* Multimodalité asymétrique (l'image sert de contexte d'illustration mais n'apporte pas d'information différentielle à la réponse).

### Test 2 : Tâche `ROOM_IDENTIFICATION` (Groupe B — 32 ex)
- **Entrées :** `inputs.geometries` (polygones vectoriels et étiquettes).
- **Test :** Si on masque le plan matriciel, la réponse reste-t-elle valide ?
  - *Résultat :* OUI. Le générateur extrait directement la liste des pièces depuis la structure JSON `rooms`.
  - *Observation :* L'entraînement apprend à traiter des données vectorielles structurées plutôt qu'à "voir" le plan avec un encodeur de vision matriciel (ViT). Pour un apprentissage ViT effectif, des tâches de repérage visuel (visual grounding avec boîtes 2D `[ymin, xmin, ymax, xmax]`) devront être ajoutées en Wave 2.

### Test 3 : Tâche `PBR_REASONING` (Groupe F — 55 ex)
- **Entrées :** `inputs.materials` (métadonnées d'échelles et de maps).
- **Test :** Les images des canaux de texture (albedo map, normal map) sont-elles injectées ?
  - *Résultat :* NON. Seules les métadonnées textuelles des maps sont présentes dans `inputs.materials`. Le modèle apprend la théorie des shaders PBR, mais pas la vision directe de textures graphiques.

---

## 5. Recommandations Impératives pour Wave 2

1. **Supprimer immédiatement les 25 exemples `IMAGE_PLUS_TEXT` orphelins de texte** ou leur adjoindre un véritable extrait de programme architectural avant tout apprentissage.
2. **Implémenter les tâches d'appariement croisé effectif :**
   - Vraie bimodalité `PLAN_PLUS_3D` : apparier les polygones d'étage ResBIM avec la maquette IFC 3D correspondante.
   - Vraie trimodalité `IMAGE_PLUS_PLAN_PLUS_TEXT` : une perspective 3D + un plan d'étage coté + une fiche programme client avec contraintes.
3. **Rendre obligatoire le `MultimodalDependencyValidator`** : interdire à tout générateur de produire un exemple bimodal sans fournir les deux conteneurs d'entrées correspondants.
