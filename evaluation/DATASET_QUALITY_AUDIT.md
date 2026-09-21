# Dataset Quality Audit : ARCHI-AI (train.jsonl)

**Date** : 21 Septembre 2026  
**Auditeur** : Pipeline d'Assurance Qualité ARCHI-AI / AEON-RWKV  
**Fichier audité** : `ARCHI_AI/dataset/train.jsonl` (20 exemples d'entraînement)  
**Objectif unique** : Déterminer si les 20 réponses du dataset d'entraînement sont suffisamment rigoureuses et conformes pour servir de données de supervision multimodale.

---

## 1. Résumé Exécutif

L'audit approfondi mené sur l'intégralité des 20 exemples du jeu d'entraînement (`train.jsonl`), confrontant chaque texte (contexte, question, réponse de référence) au fichier image réel correspondant (`images/archi_*.jpg`), révèle une **anomalie structurelle majeure** :

* **Taux d'exemples problématiques** : **20 / 20 (100%)**
* **Désynchronisations totales / Inversions sémantiques (Gravité Critique)** : **14 exemples** (ex. texte de cuisine sur une terrasse extérieure, texte de salle de bain sur un salon cathédrale à étage, texte de chambre Japandi sur un salon teal à têtes de cerf, texte de cuisine familiale sur un chef de restaurant flambant une poêle).
* **Hallucinations majeures & Contradictions directes (Gravité Haute)** : **3 exemples** (ex. salle de bain carrelée clinique décrite sur un spa tropical en pierre, critique recommandant d'ajouter un tableau d'art abstrait alors qu'il est déjà présent au centre du mur, salle de bain en béton ciré sans rangement alors qu'un grand meuble à tiroirs blancs y trône).
* **Hallucinations partielles d'éléments / matériaux (Gravité Moyenne)** : **3 exemples** (canapé d'angle et carrelage décrits sur un canapé droit et parquet bois, etc.).

### Verdict global : **NOT_READY**
Bien que la structure formelle des réponses (`OBSERVATION`, `ANALYSE`, `POINTS FORTS`, `POINTS DE VIGILANCE`, `RECOMMANDATION`) et le vocabulaire architectural soient de très haut niveau théorique, **le texte n'a pas été produit à partir des images réelles**, mais semble avoir été rédigé pour des scènes idéalisées avant qu'un scraping automatique d'identifiants Unsplash non vérifiés ne vienne y associer des photographies sans rapport.

Entraîner le modèle multimodal `Qwen2-VL-7B` sur ces données apprendrait au modèle à **déconnecter totalement sa génération de l'image** et à halluciner des récits prédéfinis.

---

## 2. Cohérence Métier & Structurelle

### 2.1. Structure formelle (Intrinsèquement Excellente)
Sur le plan purement rédactionnel et méthodologique, la structure à 5 volets appliquée uniformément est exemplaire :
1. **OBSERVATION** : Inventaire des volumes, du mobilier et des matériaux.
2. **ANALYSE** : Décryptage des intentions spatiales, de la gestion des flux et des flux lumineux.
3. **POINTS FORTS** : Atouts architecturaux objectifs.
4. **POINTS DE VIGILANCE** : Réserves constructives, contraintes d'usage et mention explicite de l'absence de plan coté métré.
5. **RECOMMANDATION** : Prescriptions techniques et décoratives concrètes.

### 2.2. Rupture de la chaîne causale Image $\to$ Observation $\to$ Prescription
La cohérence s'effondre dès lors que la base de départ (*l'observation visuelle*) est confrontée à la vérité terrain de l'image. Le schéma logique devient :
$$\text{Image A (Salon)} \xrightarrow{\text{Dissociation}} \text{Observation B (Chambre)} \to \text{Analyse B} \to \text{Recommandation B}$$
Le modèle n'apprend pas à *analyser ce qu'il voit*, mais à *plaquer un template textuel sur n'importe quel signal visuel*.

---

## 3. Analyse des Hallucinations & Distinctions Épistémiques

L'analyse distingue trois niveaux d'affirmations dans les réponses :

| Niveau | Définition | Statut dans le dataset |
| :--- | :--- | :--- |
| **OBSERVATION FACTUELLE** | Éléments directement observables et vérifiables sur l'image fournie. | **Très minoritaire ou erronée** dans la majorité des exemples (formes de meubles, pièces entières et revêtements faux). |
| **INTERPRÉTATION RAISONNÉE** | Déduction architecturale légitime à partir d'indices visibles (ex. déduire un risque acoustique d'un carrelage nu). | **Valide en théorie**, mais appliquée à des objets ou des pièces imaginaires. |
| **AFFIRMATION NON JUSTIFIÉE** | Invention pure d'objets, d'usages, de pièces ou de structures absentes de l'image. | **Omniprésente** (baignoires îlots inexistantes, verrières d'atelier absentes, bureaux de télétravail imaginaires, mezzanines omises au profit de douches). |

### Principales catégories d'hallucinations relevées :
* **Typologie d'espace erronée** : Décrire une chambre là où l'image montre un salon (`archi_007`, `archi_022`), une salle d'eau sur un grand salon à étage (`archi_013`), ou un intérieur sur une prise de vue extérieure de jardin/piscine (`archi_002`, `archi_019`).
* **Objets et mobilier fantômes** : Fauteuils ergonomiques et écrans d'ordinateur inventés (`archi_012`), îlot de cuisine et suspensions (`archi_002`, `archi_021`), table de repas compacte (`archi_014`), suspensions tombantes de mansarde (`archi_017`).
* **Matériaux et textures inventés** : Béton ciré affirmé sur un mur blanc et meuble laqué (`archi_018`), mur en briques anciennes rouges sur un mur de plâtre blanc lisse (`archi_009`), carrelage grand format sur un plancher en bois (`archi_001`).

---

## 4. Qualité du Raisonnement Architectural

* **Raisonnement intrinsèque (hors image)** : **9.5/10**. Le niveau d'expertise, le lexique professionnel (triangle d'activité, modénature shaker, warm minimalism, Wabi-Sabi, hauteur d'échappée, flux primaires/secondaires) et la mesure critique (réserve systématique sur l'absence de plan coté métré) sont d'une qualité remarquable pour un dataset spécialisé.
* **Ancrage multimodal (Grounding visuel)** : **1.5/10**. Le gradient de rétropropagation (Loss) pénaliserait l'attention visuelle du modèle : si l'encodeur visuel détecte un salon verdoyant avec un miroir rond, la cible de loss lui impose de prédire "lit bas avec tête de lit intégrée". Le modèle apprendrait donc à ignorer les caractéristiques visuelles extraites par le Vision Tower de Qwen2-VL.

---

## 5. Diversité du Dataset

* **Diversité programmatique annoncée** : Excellente sur le papier (5 catégories équilibrées : Analyse, Matériaux/Ambiance, Ergonomie/Flux, Critique, Amélioration).
* **Diversité réelle des scènes** : Faussée. Comme plusieurs images sont des vues de salon avec compositions murales ou des extérieurs, la diversité visuelle effective est mal alignée avec les questions posées.
* **Diversité des recommandations** :
  * Présence de recommandations très pertinentes et variées (éclairage indirect 2700K, panneaux tasseaux bois acoustiques, trappes passe-câbles, réglettes micro-LED, rangements sur-mesure sous rampant).
  * Quelques récurrences systématiques (les panneaux tasseaux bois sur feutre et les miroirs rétroéclairés reviennent très fréquemment).

---

## 6. Risque de Surapprentissage et Pertinence pour un Test Pipeline

On pourrait être tenté de se dire : *"Puisqu'il s'agit seulement d'un test technique de pipeline (vérifier que le backward tourne et que LoRA sauvegarde les poids), la qualité sémantique n'a pas d'importance."*

**C'est une erreur méthodologique critique pour trois raisons :**
1. **Dégénérescence de l'alignement multimodal** : Même sur 3 époques, entraîner un adaptateur LoRA (notamment sur les couches de projection de texte et de vision) avec des cibles en contradiction frontale avec les images détruit les représentations acquises lors du pré-entraînement de Qwen2-VL.
2. **Inutilisabilité de l'évaluation post-training** : L'évaluation post-entraînement sur `validation.jsonl` donnerait des résultats absurdes ou ininterprétables, empêchant de mesurer si le pipeline QLoRA améliore ou dégrade le modèle.
3. **Apprentissage de l'hallucination** : Le modèle intègrerait que l'observation factuelle n'a pas besoin de correspondre aux pixels.

---

## 7. Correspondance avec les Défauts du Modèle Baseline

Dans `ARCHI_AI/evaluation/BASELINE_EVALUATION.md`, 5 faiblesses clés du modèle Vanilla ont été identifiées :
1. **Complaisance et ton publicitaire** ("judicieuse et innovante", "harmonieuse et élégante").
2. **Absence de structure professionnelle normée**.
3. **Descriptions décoratives génériques** sans analyse spatiale ni géométrique.
4. **Omission des contraintes d'exécution** (hauteurs d'échappée, plans cotés, portance, porosité).
5. **Hallucinations visuelles ponctuelles** (ex. inventer des plantes suspendues ou un meuble combiné).

### Confrontation :
* Le dataset cible **parfaitement** les défauts 1, 2, 3 et 4 : la structure impose une posture critique, technique, mesurée et normée.
* En revanche, le dataset **aggrave dramatiquement le défaut 5 (hallucinations)** : au lieu d'apprendre au modèle à être rigoureusement factuel et ancré dans l'image, il lui fournit des exemples d'entraînement où l'hallucination est totale et délibérée.

---

## 8. Inventaire Exhaustif des 20 Exemples d'Entraînement

| ID | Catégorie annoncée | Sujet dans le texte | Contenu réel de l'image | Gravité | Diagnostic du problème |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **archi_001** | ANALYSE D'ESPACE | Salon contemporain, canapé d'angle, carrelage clair | Salon contemporain, **canapé droit en cuir cognac** + 2 fauteuils blancs, **sol parquet bois clair**, mur de 16 cadres | **Moyenne** | Erreur sur la typologie du canapé (droit vs angle) et sur le matériau du sol (bois vs carrelage). |
| **archi_002** | ANALYSE D'ESPACE | Cuisine contemporaine ouverte avec îlot et tabourets | **Vue extérieure** d'une maison moderne, pelouse, grand arbre, terrasse avec table à manger extérieure | **Critique** | **Désynchronisation totale**. L'image est une façade extérieure / jardin de nuit ; le texte analyse un intérieur de cuisine. |
| **archi_003** | ANALYSE D'ESPACE | Salon scandinave, canapé pieds hauts, tables gigognes | Salon boho/scandi, **canapé d'angle massif à pieds bas rasants**, table basse ronde unique (non gigogne), crâne de bison | **Moyenne** | Erreur de description morphologique du canapé et des tables. Décoration ethnique/boho ignorée. |
| **archi_004** | ANALYSE D'ESPACE | Loft industriel, verrières d'atelier, poteaux, poutres acier | Vignette épurée contre mur blanc : **petite banquette noire**, commode vintage peinte, lampadaire noir, ficus | **Critique** | **Désynchronisation totale**. Aucune verrière, aucune poutre, aucun poteau, aucun plateau de loft. |
| **archi_006** | STYLE / MATÉRIAUX | Salon Japandi, teintes écrues, une seule plante sobre | Salon moderne, **canapé gris**, poufs cuir cognac, **immense lampadaire arc laiton**, fente vitrée bandeau, 5+ plantes | **Moyenne** | Discordance de teintes (gris/cognac vs écru), oubli du lampadaire géant et du fenestron bandeau caractéristique. |
| **archi_007** | STYLE / MATÉRIAUX | Chambre parentale, lit bas, tête de lit bois, chevets | **Salon / Entrée** : mur vert sauge, **grand miroir rond**, enfilade basse en cannage, plantes tropicales | **Critique** | **Désynchronisation totale**. Il s'agit d'un buffet de séjour avec miroir ; le texte décrit une chambre à coucher avec lit. |
| **archi_008** | STYLE / MATÉRIAUX | Salle de bain, baignoire îlot ovale, miroir rond rétroéclairé | Salle de bain, **baignoire encastrée d'angle**, douche vitrée, meuble double vasque gris, **grand miroir rectangulaire bois** | **Haute** | Hallucination des éléments clés : baignoire îlot (fausse), miroir circulaire rétroéclairé (faux, il est rectangulaire en bois). |
| **archi_009** | STYLE / MATÉRIAUX | Salon industriel, mur briques rouges, canapé cuir tabac | Mur blanc lisse avec **étagère tiroir suspendue**, masque africain, petit appareil photo vintage, cadres | **Critique** | **Désynchronisation totale**. Zéro brique rouge, zéro canapé cuir, zéro table à roulettes. Simple mur blanc décoré. |
| **archi_011** | ERGONOMIE / CIRCULATION | Cuisine familiale, îlot avec évier intégré, flux | **Photo culinaire rapprochée d'une femme** cuisinant sur plaque gaz d'îlot avec citrons ; évier au fond sur mur | **Haute** | Cadrage portrait lifestyle : les couloirs de circulation et le sol sont invisibles. L'évier est décrit sur l'îlot alors qu'il est au mur du fond. |
| **archi_012** | ERGONOMIE / CIRCULATION | Espace télétravail dédié, bureau droit, fauteuil réglable, écran | **Espace lounge / attente coworking** : fauteuils crapauds gris/verts, canapé d'angle, tables basses, lampadaire araignée | **Critique** | **Désynchronisation totale**. Zéro bureau informatique, zéro écran, zéro fauteuil de bureau ergonomique. |
| **archi_013** | ERGONOMIE / CIRCULATION | Salle d'eau, douche à l'italienne de plain-pied, double vasque | **Immense séjour cathédrale double hauteur** avec escalier monumental vers mezzanine, canapés et cuisine au fond | **Critique** | **Désynchronisation totale grotesque**. Une photo de grand séjour américain à étage étiquetée et décrite comme une douche à l'italienne. |
| **archi_014** | ERGONOMIE / CIRCULATION | Petit espace, table de repas compacte, chaises ajourées | Salon avec parquet à chevrons, canapé bleu, fauteuil blanc, **meuble TV bas linéaire blanc, télévision**. | **Critique** | **Désynchronisation totale**. Aucune table de repas, aucune chaise de salle à manger. Toute l'analyse ergonomique repose sur du vide. |
| **archi_016** | CRITIQUE DE PROJET | Salon design, fauteuil jaune, mur immaculé, recommandation d'ajouter un tableau abstrait | Fauteuil jaune moutarde, lampadaire laiton, **grand tableau d'art abstrait géométrique (cercle noir) DÉJÀ présent au mur** | **Haute** | **Contradiction frontale**. Le texte affirme que le mur est nu et prescrit un tableau abstrait qui trône déjà au centre de l'image. |
| **archi_017** | CRITIQUE DE PROJET | Chambre scandinave sous mansarde, suspensions tombantes très basses | Chambre à **plafond parfaitement plat**, plafonnier tambour, **lampes de chevet posées sur tables de nuit**, tableau mouton | **Critique** | Absence de mansarde et de suspensions tombantes. Tout le raisonnement de sécurité (chocs de tête sur suspensions) est halluciné. |
| **archi_018** | CRITIQUE DE PROJET | Salle de bain béton ciré ultra-minimaliste, **aucun meuble ni rangement visible** | Salle de bain avec **grand meuble vasque suspendu à tiroirs blancs**, baignoire îlot blanche, porte-serviettes | **Critique** | **Contradiction frontale**. Le texte fonde sa critique sur l'absence totale de rangement alors qu'un grand meuble à tiroirs est au premier plan. |
| **archi_019** | CRITIQUE DE PROJET | Espace ouvert intérieur villa, problèmes d'écho et réverbération, tapis 3x4m | **Vue extérieure** d'une villa avec **piscine bleu turquoise**, terrasse en dalles blanches, ciel bleu et palmiers | **Critique** | **Désynchronisation totale**. Vue extérieure de piscine analysée comme un volume intérieur cathédrale réverbérant. |
| **archi_021** | AMÉLIORATION | Cuisine contemporaine, îlot bois clair, plan marbre, tabourets | **Cuisine professionnelle de restaurant avec chef cuisinier flambant une poêle** avec des flammes de 50 cm | **Critique** | **Désynchronisation totale grotesque**. Scène d'action culinaire restaurant étiquetée comme cuisine résidentielle zen en bois clair. |
| **archi_022** | AMÉLIORATION | Chambre Japandi dépouillée, sommier bas au sol, sol minéral nu | **Salon avec mur vert canard / teal**, canapé cuir camel, **deux têtes de cerfs sculptées**, galerie de 6 cadres | **Critique** | **Désynchronisation totale**. Salon feutré avec têtes de cerf décrit comme une chambre zen japonaise au sol nu. |
| **archi_023** | AMÉLIORATION | Salle de bain froide et clinique, carrelage blanc, à réchauffer avec du bois/plantes | **Salle de bain spa tropicale de luxe**, baignoire ovale en pierre sur **lit de galets blancs, palmier vivant**, mur texturé | **Critique** | **Inversion totale**. La pièce est déjà un spa tropical en pierre avec plantes et galets, décrite par le texte comme un hôpital carrelé de blanc ! |
| **archi_024** | AMÉLIORATION | Bureau bibliothèque toute hauteur, grande table de travail, goulotte câbles | **Mur blanc couvert d'une galerie dense de cadres photos** et petites cimaises décoratives avec plantes miniatures | **Critique** | **Désynchronisation totale**. Aucun meuble bibliothèque, aucun bureau, aucun câble. Simple mur galerie de cadres. |

---

## 9. Conclusion et Décision

### Niveaux d'évaluation :
* `READY` : Suffisamment propre pour le test technique.
* `NEEDS_REVIEW` : Quelques problèmes mineurs mais utilisable après corrections ciblées.
* **`NOT_READY`** : Données inaptes à l'entraînement, risquant de corrompre l'alignement multimodal du modèle.

### Décision finale : **NOT_READY**

Le dataset `train.jsonl` actuel est **inutilisable en l'état pour un entraînement supervisé**, même dans le cadre d'un PoC ou d'un simple galop d'essai technique. 

Lancer un fine-tuning sur ce jeu de données produirait un modèle qui apprendrait à **ignorer les pixels de l'image** pour régurgiter des réponses déconnectées du réel, ruinant l'objectif d'ancrage visuel professionnel d'ARCHI-AI.

### Plan de remédiation recommandé (hors périmètre de cette tâche) :
1. **Option A (Réalignement des images)** : Remplacer les 20 images Unsplash par de véritables images correspondant fidèlement aux 20 textes (qui, eux, sont d'une excellente tenue architecturale).
2. **Option B (Réécriture des annotations)** : Conserver les images actuelles et réécrire les 20 annotations en appliquant la même méthodologie d'analyse spatiale stricte aux scènes réellement photographiées.
