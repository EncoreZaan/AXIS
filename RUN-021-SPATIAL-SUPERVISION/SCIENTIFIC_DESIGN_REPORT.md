# AXIS — Rapport de Conception Scientifique & Stratégie Expérimentale (`SCIENTIFIC_DESIGN_REPORT.md`)

> **Run Identifier:** `RUN-021-SPATIAL-SUPERVISION`  
> **Date:** 2026-09-23  
> **Auteur:** Agent d'Ingénierie Dataset & de Préparation Scientifique AXIS  
> **Objet:** Réponses formelles aux 12 questions scientifiques fondamentales de la Phase 6A

---

## Question 1 : Pourquoi RUN-019 a échoué à démontrer le grounding visuel ?

RUN-019 a échoué car son protocole d'entraînement a récompensé la **minimisation de la loss textuelle par apprentissage par cœur (template memorization)** au lieu de contraindre l'utilisation de la modalité visuelle.

L'expérience d'ablation visuelle de Phase 5 (`RUN-020`) a apporté la preuve falsificatrice irréfutable :
- En remplaçant l'image du plan par une **image 100 % noire**, le modèle RUN-019 a continué de générer la critique architecturale avec une **similarité textuelle de 92.0 %** par rapport à l'image originale.
- En masquant les cloisons et ouvertures, la similarité est restée de **95.3 %**.
- En mode **Text-Only** (sans aucun token visuel), la similarité était de **95.7 %**.

Ces chiffres démontrent que l'encodeur visuel de Qwen2-VL a été quasi-totalement court-circuité pendant l'entraînement LoRA : le modèle s'est contenté d'associer le prompt utilisateur standard à un gabarit de réponse appris, sans jamais inspecter la géométrie des plans.

---

## Question 2 : Quelles limitations précises ont été identifiées dans le dataset précédent ?

Trois failles majeures ont été identifiées dans `REAL_DATA_PILOT` :
1. **Uniformité structurelle et verbosité excessive :** Les 1 000 cibles d'entraînement étaient rédigées selon un unique canevas rigide en 5 sections (`OBSERVATION`, `ANALYSE`, `POINTS FORTS`, `POINTS DE VIGILANCE`, `RECOMMANDATION`), comptant en moyenne 220 mots. Le modèle a rapidement découvert qu'en reproduisant cette prose, il réduisait la loss de 98.6 % sans traiter l'image.
2. **Absence de questions à réponse fermée ou mesurable :** Les questions posées étaient ouvertes et vagues (ex: *"Analysez la composition spatiale, les parois et la distribution fonctionnelle..."*). Aucune question n'exigeait de calculer une valeur numérique, de vérifier un contact physique ou de déterminer une direction relative.
3. **Hallucination systématique d'identifiants :** Le dataset précédent introduisait des chaînes telles que `unit_001` ou des identifiants RPLAN dans la réponse cible, poussant le modèle à inventer des identifiants numériques aléatoires sur le jeu de test.

---

## Question 3 : Quelles nouvelles tâches corrigent ces limitations ?

Le nouveau dataset `AXIS_SPATIAL_SUPERVISION_V1` introduit 5 familles de tâches ciblées qui ne peuvent être résolues qu'en extrayant l'information visuelle :

1. **TASK A — Cardinalité et Décompte Déterministe :** "Combien de pièces intérieures composent ce plan ?" / "Combien de portes de passage sont répertoriées ?". La réponse est un entier unique, impossible à prédire sans compter les régions dans l'image.
2. **TASK B — Relations Directionnelles :** "Quelle est la position relative de la pièce [bbox_A] par rapport à la pièce [bbox_B] ?" (À gauche / À droite / Au-dessus / En dessous). Requiert l'ancrage spatial précis des coordonnées.
3. **TASK D — Connectivité Topologique (Positif & Négatif Contrastif) :** "La pièce A et la pièce B sont-elles directement reliées par une porte ?" (Oui / Non). Les exemples négatifs empêchent le modèle de supposer que deux pièces voisines sont toujours connectées.
4. **TASK F — Relations Comparatives et Extrémales :** "Quelle pièce présente la surface utile maximale ?". Force la comparaison visuelle de surface entre sous-espaces.
5. **TASK G — Raisonnement Multi-Hop sur Graphe :** "Quel est le nombre minimal de portes à franchir pour passer de la pièce A à la pièce B ?" / "Quel espace joue le rôle de noyau de distribution central ?". Exige un parcours topologique du plan.

---

## Question 4 : Quelles données sont réellement disponibles ?

L'audit forensique sur disque a établi la disponibilité physique stricte suivante :
- **`CORE_RPLAN` (15 000 plans d'étage 256x256 px) :**
  - Pixels de cloisons rouges `[255, 0, 0]` : **DISPONIBLES**.
  - Pixels de portes vertes `[0, 255, 0]` : **DISPONIBLES**.
  - Pixels de pièces blanches `[255, 255, 255]` : **DISPONIBLES**.
  - Fond gris `[128, 128, 128]` : **DISPONIBLE**.
  - Labels textuels de pièces (chambre, salon, cuisine) : **NON DISPONIBLES** (expurgés dans la distribution ControlNet).
  - Échelle métrique continue (mètres réels) : **NON DISPONIBLE** (proscrite pour éviter les faux labels).
- **`CORE_RESBIM_PAIRED` (10 unités 2D/3D certifiées) :**
  - Dessins 2D haute résolution (7572x4189 px) : **DISPONIBLES**.
  - Maquettes 3D OpenBIM IFC : **DISPONIBLES**.
  - Entités `IfcWall`, `IfcDoor`, `IfcWindow` avec cotes millimétriques : **DISPONIBLES**.
  - Entités `IfcSpace` : **NON DISPONIBLES** (0 espace modélisé).
- **Sources Exclues :**
  - `CORE_FLOORPLANCAD` (Quarantaine juridique CC-BY-SA/NC).
  - `GOLD_SET_V3` (Sanctuaire d'évaluation inviolable).

---

## Question 5 : Quelle quantité de ground truth fiable existe ?

- **`SOURCE_GROUND_TRUTH` :** 30 exemples certifiés issus directement des attributs normalisés IFC de ResBIM (comptages de blocs-portes, fenêtres et parois murales certifiés par maquette OpenBIM).
- **`DERIVED_GROUND_TRUTH` :** 7 920 exemples calculés algorithmiquement de façon 100 % déterministe à partir des composantes connexes et de la topologie des tracés physiques de RPLAN.
- **`NOT_USABLE_AS_GROUND_TRUTH` :** 0 exemple. Aucune inférence par LLM, aucune estimation heuristique au jugé et aucune coordonnée fictive n'a été convertie en vérité terrain.

---

## Question 6 : Comment les relations sont-elles dérivées ?

Les relations sont dérivées selon les algorithmes formels spécifiés dans [`SPATIAL_RELATION_DEFINITIONS.md`](file:///c:/Users/teoba/Documents/Devs/AXIS/RUN-021-SPATIAL-SUPERVISION/SPATIAL_RELATION_DEFINITIONS.md) :
1. **Composantes connexes BFS :** Les pièces (pixels blancs) et les portes (pixels verts) sont isolées avec seuils d'aire géométriques ($A \ge 50$ px pour les pièces, $A \ge 4$ px pour les portes).
2. **Directionnalité normalisée :** Une relation `LEFT_OF` est assignée si le delta horizontal est dominant ($|\Delta x| > |\Delta y|$) et dépasse $0.4 \times$ la largeur moyenne des deux pièces.
3. **Connectivité par dilatation morphologique :** Deux pièces $A$ et $B$ sont connectées par une porte si la dilatation de 2 pixels du masque de la porte intersecte à la fois $A$ et $B$.
4. **Adjacence murale :** Détectée par dilatation de 3 pixels à travers la frontière des parois rouges.
5. **Graphe topologique :** Calcul du plus court chemin par l'algorithme de parcours en largeur (BFS) sur le graphe non orienté $G_P = (V_P, E_P)$.

---

## Question 7 : Comment le leakage est-il empêché ?

L'étanchéité absolue repose sur :
1. **Découpage au niveau de l'image racine (Asset-Level Partitioning) :** La graine pseudo-aléatoire déterministe 42 partitionne les 1 000 plans d'origine en 775 train, 98 validation, 127 test.
2. **Contrôle ensembliste des empreintes SHA-256 :** L'intersection des empreintes cryptographiques des images entre Train et Test est strictement nulle ($\text{Train} \cap \text{Test} = \emptyset$).
3. **Absence de contamination multi-tâches croisée :** Toutes les questions relatives à un même plan sont confinées dans le même split.
4. **Sanctuaire Gold Set V3 :** Zéro chevauchement avec les 200 exemples d'évaluation aveugle finale.

---

## Question 8 : Comment mesurer le grounding visuel ?

Le grounding visuel sera mesuré en Phase 6B au moyen du **protocole d'ablation d'images à 5 conditions** :
1. $\text{Acc}_{\text{original}}$ : Précision sur les images réelles non altérées.
2. $\text{Acc}_{\text{black}}$ : Précision lorsque l'image est remplacée par un aplat noir.
3. $\text{Acc}_{\text{masked}}$ : Précision lorsque les ouvertures ou parois sont masquées.
4. $\text{Acc}_{\text{noise}}$ : Précision sous bruit gaussien/uniforme non corrélé.
5. $\text{Acc}_{\text{text\_only}}$ : Précision sans tenseurs de vision.

**Indicateur de Dépendance Visuelle (VDI) :**
$$\text{VDI} = \frac{\text{Acc}_{\text{original}}}{\max(\text{Acc}_{\text{black}}, \text{Acc}_{\text{text\_only}})}$$
Dans RUN-019, $\text{VDI} \approx 1.0$ (dépendance nulle).
Pour prouver le grounding visuel, le futur modèle devra atteindre $\text{VDI} \ge 3.0$.

---

## Question 9 : Comment mesurer le raisonnement spatial ?

Le raisonnement spatial sera évalué par des métriques objectives exactes (Accuracy, Macro-F1, Exact Match) sur des réponses courtes :
- **Précision directionnelle 4-voies (Left / Right / Above / Below) :** Score vs chance aléatoire (25 %).
- **Précision de connectivité binaire (Oui / Non) :** Score vs chance aléatoire (50 %).
- **Erreur absolue moyenne sur le décompte de pièces :** $\text{MAE} = \frac{1}{N} \sum |\hat{y} - y|$.
- **Exactitude des chemins multi-hop :** Pourcentage de trajets dont le nombre de portes prédit est exact.

---

## Question 10 : Quels résultats seront considérés comme preuve ?

Seront considérés comme une preuve scientifique solide :
1. Une précision sur le test set $\text{Acc}_{\text{original}} \ge 70.0 \%$ sur les relations directionnelles et la connectivité.
2. Un effondrement de la performance sous ablation visuelle : $\text{Acc}_{\text{black}} \le 30.0 \%$ et $\text{Acc}_{\text{text\_only}} \le 30.0 \%$.
3. Un ratio de dépendance visuelle $\text{VDI} \ge 3.0$.
4. Une performance sur les exemples négatifs (`NOT_CONNECTED`) comparable à celle sur les exemples positifs (écart F1 $< 0.10$).
5. Un taux d'hallucination d'identifiants nul ($0.0 \%$).

---

## Question 11 : Quels résultats ne seront PAS considérés comme preuve ?

Ne seront **JAMAIS** considérés comme une preuve de compétence :
1. Une simple diminution de la validation loss sans amélioration de l'exactitude géométrique.
2. Des réponses verbeuses de type "OBSERVATION / ANALYSE" obtenant une forte similarité lexicale sans justesse spatiale.
3. Un modèle qui prédit "Oui" à 100 % sur les questions de connectivité (biais de classe positif).
4. Des performances qui restent stables lorsque l'image est supprimée ou noircie.
5. Toute évaluation sur des données contaminées par le split d'entraînement.

---

## Question 12 : Quel sera le protocole de Phase 6B ?

La Phase 6B (qui sera exécutée uniquement sur ordre explicite) comprendra :
1. **Entraînement LoRA contrôlé :** Utilisation de `training_config_proposal.yaml` sur le dataset `AXIS_SPATIAL_SUPERVISION_V1` (configuration Small ou Medium).
2. **Surveillance anti-overfitting :** Arrêt précoce (early stopping) basé sur la précision spatiale en validation, non sur la loss textuelle brute.
3. **Campagne d'ablation EVAL-D complète :** Exécution systématique des 5 conditions d'ablation sur le test set.
4. **Calcul du VDI et des matrices de confusion spatiales.**
5. **Rapport de falsification ou de validation scientifique.**
