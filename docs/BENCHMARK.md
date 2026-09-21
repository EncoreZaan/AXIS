# Benchmark ARCHI-AI (13 Axes d'Évaluation)

## 1. Cadre Général

Le benchmark ARCHI-AI évalue les capacités d'un modèle de vision-langage (VLM) sur 13 dimensions architecturales indépendantes. Il permet d'éviter l'évaluation globale opaque et de cibler précisément les faiblesses techniques du modèle.

---

## 2. Définition des 13 Axes

| N° | Axe | Description | Métrique principale |
| :--- | :--- | :--- | :--- |
| 1 | **Vision** | Exactitude perceptive des éléments bâtis | Précision des objets et agencements |
| 2 | **Spatial** | Compréhension des volumes, hauteurs, relations | Clarté de la structure spatiale |
| 3 | **Ergonomie** | Respect des dimensions humaines et de l'usage | Détection des contraintes corporelles |
| 4 | **Matériaux** | Identification et calepinage des textures | Fidélité minérale, ligneuse, textile |
| 5 | **Lumière** | Analyse de l'éclairage naturel et artificiel | Gestion des ouvertures et ombres |
| 6 | **Couleur** | Cohérence chromatique et contrastes | Analyse des palettes tonales |
| 7 | **Style** | Reconnaissance stylistique et historique | Richesse du vocabulaire d'époque |
| 8 | **Circulation** | Analyse des flux et dégagements | Identification des axes de passage |
| 9 | **Critique** | Jugement équilibré points forts / vigilances | Pertinence de la balance critique |
| 10 | **Recommandation** | Qualité et faisabilité des solutions proposées | Réalisme des actions d'aménagement |
| 11 | **Plan 2D** | Lecture de schémas, coupes et cotes | Corrélation plan-image |
| 12 | **Pédagogie** | Clarté d'explication et transmission didactique | Accessibilité de la démonstration |
| 13 | **Anti-hallucination** | Prudence épistémique face aux données invisibles | Absence d'affirmations sans preuve |

---

## 3. Résultats de la Baseline Historique (`Qwen2-VL-7B-Instruct zero-shot`)

- **Score Global :** `5.7 / 10`
- **Scores détaillés par axe :**
  - Lumière : `6.8 / 10`
  - Vision : `6.6 / 10`
  - Ergonomie : `6.6 / 10`
  - Anti-hallucination : `6.5 / 10`
  - Spatial : `6.4 / 10`
  - Plan 2D : `6.4 / 10`
  - Matériaux : `6.2 / 10`
  - Couleur : `5.8 / 10`
  - Style : `5.0 / 10`
  - Circulation : `4.8 / 10`
  - Recommandation : `4.6 / 10`
  - Critique : `4.4 / 10`
  - Pédagogie : `4.0 / 10`

### Enseignements majeurs
Le modèle de base non spécialisé perçoit convenablement la lumière et les formes d'ensemble, mais manque de structure critique, de recommandations opérationnelles et de vision didactique. C'est précisément l'objectif du fine-tuning QLoRA spécialisé.
