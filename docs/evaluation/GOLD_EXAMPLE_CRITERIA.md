# ARCHI-AI — Critères de Définition d'un Exemple d'Or (`GOLD_EXAMPLE_CRITERIA.md`)

> **Version :** 1.0.0  
> **Date de publication :** 21 September 2026  
> **Statut :** STANDARD DE QUALITÉ CANONIQUE ARCHI-AI  
> **Objectif :** Définir sans ambiguïté ce qui constitue un "Exemple d'Or" (Gold Standard Example) pour la supervision d'un modèle multimodal expert en architecture intérieure.  

---

## 1. Philosophie Fondamentale

Un exemple d'apprentissage pour ARCHI-AI ne doit pas simplement "avoir l'air plausible" ou passer des filtres syntaxiques superficiels. Il doit **enseigner au réseau de neurones les réflexes cognitifs d'un architecte d'intérieur chevronné**, capable d'analyser un plan, d'interpréter un modèle 3D ou IFC, de prescrire des matériaux physiques, et de formuler une critique constructive sans complaisance.

Un exemple est qualifié de **Gold Standard** s'il satisfait l'intégralité des 10 commandements suivants :

---

## 2. Les 10 Commandements d'un Exemple d'Or

### I. Ancrage Source Intégral (Strict Grounding)
- **Règle :** Chaque entité, cote, matériau ou relation mentionné dans la question et la réponse doit provenir d'une source traçable (ID Master Dataset vérifié).
- **Prohibé :** L'ajout de pièces imaginaires ("un balcon filant" alors que le plan est aveugle), de cotes estimées au hasard, ou de notices muséales inventées.
- **Vérification :** `source_provenance` complet (`source_name`, `dataset_name`, `raw_file`, `normalized_id`).

### II. Spécificité Architecturale (Zéro Réponse Interchangeable)
- **Règle :** La réponse doit être tellement spécifique à l'exemple qu'elle devient inapplicable à un autre projet sans modification majeure.
- **Prohibé :** Les truismes ("Améliorer la circulation rend l'espace plus agréable", "Cette couleur apporte de la chaleur", "Les cloisons séparent les espaces").
- **Exigence :** Citer les noms réels des pièces (`bedroom_1`, `cuisine`), les cotes exactes en mètres (`passage libre : 0.85 m`), les propriétés physiques réelles (`échelle métrique 2.80 m x 2.80 m`).

### III. Multimodalité Réelle et Nécessaire (Non-Fictivité Multimodale)
- **Règle :** Si l'exemple est présenté comme multimodal (bimodal ou trimodal), la réponse **doit impérativement nécessiter l'examen conjoint de toutes les modalités déclarées**.
- **Prohibé :** Déclarer une tâche `IMAGE_PLUS_TEXT` ou `PLAN_PLUS_3D` sans fournir le texte ou le modèle 3D dans `inputs`, ou rédiger une réponse qui pourrait être générée sans regarder l'image ou le plan (`FAKE_MULTIMODAL`).
- **Test du masquage :** Si la suppression de l'image ou du plan ne change rien à la validité de la réponse, l'exemple est rejeté.

### IV. Découpage Épistémique Rigoureux (Vérité vs Inférence)
- **Règle :** La réponse doit séparer formellement les strates de connaissance :
  1. `OBSERVATION` : Ce qui est directement mesurable ou visible sur le document (ex: "Le séjour mesure 24.5 m² et comporte deux baies vitrées orientées sud").
  2. `INTERPRÉTATION` : L'analyse qualitative experte (ex: "Cette double orientation favorise une ventilation traversante naturelle").
  3. `INFÉRENCE` : La déduction combinatoire (ex: "L'absence de sas entre l'entrée et l'espace nuit crée un conflit d'intimité").
  4. `UNKNOWN` / `TO_VERIFY` : L'explicitation honnête des données manquantes (ex: "Épaisseur des cloisons non cotée sur ce document, à vérifier sur carnet de détails").
- **Prohibé :** Présenter une hypothèse comme un fait avéré.

### V. Exactitude Numérique et Cohérence des Unités
- **Règle :** Tout nombre doit être accompagné de son unité légale (système international : mètres, mètres carrés, millimètres, degrés, Kelvin, EV).
- **Prohibé :** Les placeholders non résolus (`None m`), les valeurs textuelles non converties, les confusions entre surface brute et surface utile nette.
- **Traçabilité :** Tout chiffre doit figurer dans `ground_truth` avec `original_value`, `original_unit`, `normalized_value`, `normalized_unit`.

### VI. Non-Sycophantie et Rigueur Critique
- **Règle :** Dans les tâches de critique ou d'évaluation de projet, le ton doit être celui d'un enseignant d'atelier ou d'un confrère bienveillant mais intransigeant sur les défauts d'usage.
- **Prohibé :** Les formules de flatterie creuse ("Magnifique réalisation", "Projet parfait sans aucun défaut", "Bravo à l'architecte").
- **Structure obligatoire :** Constat factuel → Point de friction avéré → Conséquence fonctionnelle → Recommandation constructive et alternative concrète.

### VII. Posture Pédagogique Active (Maïeutique de Studio)
- **Règle :** Pour les tâches pédagogiques (`GUIDED_REASONING`, `STUDIO_CRITIQUE`), le modèle ne doit pas "donner la solution sur un plateau" mais stimuler l'autonomie de l'étudiant.
- **Structure :** Questionnement d'amorce → Pointage du conflit spatial → Règle de l'art sous-jacente → Exercice pratique de vérification au calque/croquis.

### VIII. Calibration Précise de la Complexité (L1 à L6)
- **L1 (Reconnaissance) :** Identification directe d'une entité ou lecture immédiate d'une étiquette.
- **L2 (Compréhension) :** Décodage de la distribution et des fonctions globales.
- **L3 (Analyse) :** Calcul de métrés, topologie de voisinage, propriétés physiques de shaders.
- **L4 (Raisonnement) :** Diagnostic d'un conflit d'usage bimodal ou d'une erreur d'implantation.
- **L5 (Expertise) :** Synthèse critique d'aménagement, conformité réglementaire stricte (PMR/ERP).
- **L6 (Multicontrainte) :** Arbitrage complexe conciliant faisabilité technique, conformité légale, budget et intention plastique.
- **Prohibé :** Labelliser L6 une simple restitution de texte, ou L1 une analyse d'arbitrage croisé.

### IX. Richesse et Pertinence Métier (Vocabulaire Canonique)
- **Règle :** L'expression doit mobiliser le lexique professionnel exact :
  - *Architecture intérieure :* nu intérieur, plinthe, trémie, imposte, tableau, allège, retombée de poutre, calepinage, gabarit d'évitement, triangle d'activité.
  - *BIM / IFC :* `IfcSpace`, `IfcWallStandardCase`, `IfcRelContainedInSpatialStructure`, MVD, Pset.
  - *Matériaux & Éclairage :* Albédo, Normal Map, Roughness, indice IOR, température Kelvin, réflectance spéculaire, indice IRC, EV (Exposure Value).

### X. Vérifiabilité et Réfutabilité (Déterministe)
- **Règle :** Toute assertion géométrique, de comptage ou de hiérarchie doit pouvoir être réfutée ou confirmée par les vérificateurs déterministes mathématiques (`GeometryVerifier`, `SceneGraphVerifier`, `IfcVerifier`, `ErgonomicsVerifier`).

---

## 3. Matrice de Rejet Immédiat (Kill Switches)

Un exemple est **immédiatement disqualifié du statut Gold** (et classé `EXCLUDE` ou `CORRECT`) s'il présente l'un des défauts suivants :

| Défaut | Détection Algorithmique | Action |
| :--- | :--- | :--- |
| **Présence de 'None'** | Regex `\bNone\b` | Rejet immédiat (`CORRECT` ou `EXCLUDE`) |
| **Entrées multimodales vides** | `ModalInputs` avec listes vides | Rejet immédiat (`EXCLUDE`) |
| **Faux multimodal** | Tâche croisée sans 2ème modalité | Rejet immédiat (`EXCLUDE`) |
| **Template textuel répliqué > 5 fois** | Clustering sémantique d'ans | Rejet immédiat (`REVIEW`) |
| **Flatterie sycophante** | AntiSycophancyValidator FAIL | Rejet immédiat (`EXCLUDE`) |
| **Article de loi imaginaire** | HallucinationValidator FAIL | Rejet immédiat (`EXCLUDE`) |
| **Cote non sourcée** | Absence dans ground_truth | Rejet immédiat (`REVIEW`) |
