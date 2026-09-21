# ARCHI-AI — Matrice Décisionnelle : Poids (Fine-Tune) vs RAG vs Outils (`RAG_VS_FINETUNE_MAP`)

## 1. Principes Fondateurs de la Répartition Cognitive

Pour concevoir un système expert fiable en architecture intérieure, il est impératif de ne pas commettre l'erreur courante de vouloir "tout injecter dans les poids du modèle". Les réseaux de neurones sont d'excellents moteurs d'intuition visuelle et de synthèse qualitative, mais de très mauvais calculateurs arithmétiques et des mémorisateurs peu fiables pour les textes de lois changeants.

ARCHI-AI applique une règle d'ingénierie stricte :

```text
       NATURE DE L'INFORMATION                  DESTINATION SYSTÈME
────────────────────────────────────────       ─────────────────────────
Perception visuelle, ambiance, style    ───►   POIDS DU MODÈLE (VLM Fine-Tuning)
Raisonnement spatial, critique, pédagogie───►   POIDS DU MODÈLE (VLM Fine-Tuning)
Normes, lois, fiches techniques, dates   ───►   RAG DYNAMIQUE (Index Vectoriel/BM25)
Surfaces, cotes, dégagements, graphes    ───►   DETERMINISTIC TOOLS (Calculs & Parseurs)
Validation impartiale de performance    ───►   BENCHMARK INDÉPENDANT (Holdout strict)
```

---

## 2. Tableau Décisionnel par Domaine Métier

| # | Domaine Métier | Décision d'Attribution | Rôle des Poids (VLM) | Rôle du RAG | Rôle des Outils (Tools) |
|---|---|---|---|---|---|
| **01** | **Perception de l'Espace & Pièces** | `FINE-TUNE` | Reconnaissance visuelle immédiate des typologies, volumes et baies. | Aucun (inutile). | Détection de boîtes englobantes et plans de coupe. |
| **02** | **Plans 2D : Parois & Ouvertures** | `COMBINAISON` *(VLM + Tool)* | Compréhension sémantique des symboles (portes, fenêtres, allèges). | Aucun. | Vectorisation SVG/DXF, calcul exact des longueurs de cloisons. |
| **03** | **Plans 2D : Topologie & Flux** | `COMBINAISON` *(VLM + Tool)* | Interprétation qualitative de la fluidité et des vis-à-vis. | Fiches méthodologiques sur la syntaxe spatiale. | Algorithme A*, calcul des distances de parcours et couloirs. |
| **04** | **BIM / IFC & Composants** | `COMBINAISON` *(VLM + RAG + Tool)* | Reconnaissance visuelle des familles d'objets (IfcWall, IfcDoor). | Schémas IFC et définitions buildingSMART. | Parseur `IfcOpenShell` pour extraire métrés réels et propriétés. |
| **05** | **Matériaux : Perception Visuelle** | `FINE-TUNE` | Discrimination fine des essences de bois, pierres, bétons, textiles. | Aucun. | Analyseur d'histogrammes de texture et rugosité. |
| **06** | **Matériaux : Propriétés & Mise en œuvre** | `RAG` | Vocabulaire descriptif de base. | DTU carrelage/parquet, fiches fabricants, résistance au poinçonnement. | Calculateur de quantité et déboursé sec matière. |
| **07** | **Lumière : Ambiance & Perception** | `FINE-TUNE` | Lecture des ombres portées, contrastes, ambiance diurne/nocturne. | Principes de scénographie d'éclairage. | Masquage de surexposition et analyse colorimétrique RVB. |
| **08** | **Lumière : Photométrie & Éclairement** | `COMBINAISON` *(Tool + RAG)* | Estimation qualitative de la clarté d'une pièce. | Niveaux d'éclairement recommandés en lux (EN 12464-1). | Moteur de calcul du ratio de baie vitrée et du FLJ (Facteur Lumière Jour). |
| **09** | **Ergonomie : Posture & Usage** | `COMBINAISON` *(VLM + Tool)* | Repérage visuel des postures et encombrements anormaux. | Données d'anthropométrie (Panero & Zelnik, Neufert). | Boîtes d'encombrement 3D et détection de collisions physiques. |
| **10** | **Normes PMR / Accessibilité** | `COMBINAISON` *(Tool + RAG)* | Repérage visuel des ressauts ou portes étroites. | Arrêtés PMR 2015/2017 consolidés (Articles exacts cités). | Vérificateur de gabarit (Cercle de rotation Ø 150 cm, sas d'isolement). |
| **11** | **Sécurité Incendie ERP** | `COMBINAISON` *(RAG + Tool)* | Identification des issues et blocs secours. | Règlement de sécurité ERP (articles CO 36 à 42 pour les dégagements). | Calcul déterministe des Unités de Passage (UP = 0,60 m). |
| **12** | **Mobilier : Style & Placement** | `FINE-TUNE` | Cohérence de sélection, échelle et agencement harmonieux. | Catalogues de mobilier avec cotes fabricant. | Vérification des dégagements d'usage autour des tables/lits. |
| **13** | **Histoire de l'Architecture** | `COMBINAISON` *(RAG + VLM)* | Reconnaissance visuelle des ordres, modénatures et courants. | Monographies exhaustives, dates d'édifices, manifestes d'architectes. | Frise chronologique interactive. |
| **14** | **Histoire du Design** | `COMBINAISON` *(RAG + VLM)* | Reconnaissance des pièces maîtresses (Eames, Breuer, Prouvé). | Biographies de designers, contextes d'écoles (Bauhaus, Ulm, Memphis). | Aucun. |
| **15** | **Styles d'Intérieur** | `FINE-TUNE` | Discrimination et caractérisation des 40 styles d'espace. | Fiches de synthèse sur la genèse des tendances. | Palette d'extraction chromatique dominante. |
| **16** | **Critique de Projet (Studio)** | `FINE-TUNE` | Diagnostic argumenté, identification de faiblesses, esprit de synthèse. | Grilles de critères pédagogiques d'écoles d'art/architecture. | Vérification des allégations de surface ou d'exposition. |
| **17** | **Pédagogie & Maïeutique** | `FINE-TUNE` | Posture de tuteur bienveillant et exigeant, guidage pas-à-pas. | Exercices types d'atelier et programmes pédagogiques. | Aucun. |
| **18** | **Technique Constructive & Second Œuvre** | `RAG` | Compréhension des notions d'allège, trémie, refend, doublage. | DTU 25.41, fiches Placo, règles d'assemblage et de fixation. | Calculateur d'épaisseurs cumulées de complexes de cloisons. |
| **19** | **Physique du Bâtiment (Acoustique/Thermique)**| `RAG` | Sensibilité aux parois réverbérantes ou ponts thermiques évidents. | Guides acoustiques Qualitel, exigences RE2020, affaiblissements Rw. | Moteur de calcul de temps de réverbération (Formule de Sabine). |
| **20** | **Multimodalité Croisée (Plan ↔ Rendu)** | `FINE-TUNE` | Détection visuelle et logique des disparités plan vs perspective. | Aucun. | Recalage géométrique de caméra (perspective matching). |

---

## 3. Justification Approfondie des Rôles

### Pourquoi le RAG pour les Normes et la Réglementation ?
1. **Évolutivité temporelle :** Un décret ministériel ou un arrêté modifiant les obligations d'accessibilité PMR ne doit pas nécessiter le réentraînement d'un modèle de 7 milliards de paramètres. Une simple mise à jour de la base vectorielle suffit.
2. **Exigence de citation littérale :** Dans un cadre professionnel, un architecte engage sa responsabilité. ARCHI-AI doit être en mesure de citer : *"Selon l'article 7 de l'arrêté du 24 décembre 2015, le passage utile sous la porte d'entrée doit être au minimum de 0,83 m..."*. Le RAG fournit la preuve textuelle inattaquable.
3. **Zéro hallucination :** Les modèles de langage inventent fréquemment des numéros d'articles de loi ou des tolérances inexistantes lorsqu'ils sont interrogés de mémoire.

### Pourquoi les Outils Déterministes pour la Géométrie et les Cotes ?
1. **Précision arithmétique :** Les réseaux de neurones sont des estimateurs statistiques, pas des mètres rubans. Calculer si un lit de 160 cm laisse un passage réglementaire de 90 cm dans une chambre de 270 cm de large est une soustraction ($270 - 160 = 110 \ge 90$). L'outil calcule avec une exactitude de 100%.
2. **Vérification d'accessibilité PMR :** L'outil trace géométriquement un cercle virtuel de diamètre 1,50 m dans la pièce et vérifie s'il intersecte un obstacle fixe (cloison ou équipement sanitaire).

### Pourquoi le Fine-Tuning pour la Perception, le Style et la Critique ?
1. **Tacite et non-formalisable :** La notion d'harmonie d'un parti pris, l'équilibre des pleins et des vides, la sensation d'étouffement dans un couloir mal proportionné ou l'élégance d'une association chêne/laiton ne se réduisent pas à une table de base de données.
2. **Posture professionnelle :** Le ton incisif mais constructif de l'enseignant de studio d'architecture ne s'obtient que par l'ajustement fin des poids du modèle sur des exemples de haut niveau d'expertise.
