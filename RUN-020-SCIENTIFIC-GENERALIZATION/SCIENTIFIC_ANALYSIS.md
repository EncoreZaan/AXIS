# AXIS Phase 5 — Scientific Analysis & Falsification Report (`RUN-020`)

> **Run Evaluated:** `RUN-019-FIRST-REAL-DATA-QLORA`  
> **Date:** 2026-09-23  
> **Status:** SCIENTIFIC EVALUATION COMPLETE  

---

## Question 1 : RUN-019 généralise-t-il sur le test set ?

### OBSERVATION :
Sur les 127 assets inédits du test split (`test.jsonl`), le modèle RUN-019 produit des réponses qui adoptent scrupuleusement la structure en 5 rubriques (`OBSERVATION`, `ANALYSE`, `POINTS FORTS`, `POINTS DE VIGILANCE`, `RECOMMANDATION`), avec une adhérence de **80.2 %** contre 0.0 % pour le Base model.
Cependant, sur les 125 plans RPLAN testés, le modèle entraîné reproduit une similarité de **85.3 %** avec le template canonique d'entraînement, et **100.0 %** des réponses comportent un identifiant numérique inventé issu du vocabulaire d'entraînement (ex: `20220`, `1012`, `50001`) au lieu de l'identifiant réel.

### INTERPRÉTATION :
RUN-019 ne généralise pas au sens d'une compréhension adaptative de plans variés. Il a appris de façon ultra-rigide la distribution lexicale, syntaxique et stylistique du format de critique architecturale AXIS. La forte diminution de validation loss observée en Phase 4 (-98.59 %) s'explique par la prédictibilité quasi-parfaite de ce template textuel unique sur les données RPLAN.

### HYPOTHÈSE :
Le dataset de supervision de Phase 4 contenait des labels de réponse quasi-uniformes construits à partir d'un générateur de templates déterministe. Le modèle a minimisé la loss par apprentissage de template plutôt que par analyse visuo-spatiale.

---

## Question 2 : RUN-019 généralise-t-il à une source différente ?

### OBSERVATION :
Le corpus de 1 000 assets contient uniquement 10 paires issues de `CORE_RESBIM_PAIRED`. La totalité des 10 assets a été absorbée dans le split expérimental (8 en train, 2 en test). Aucun asset ResBIM inédit n'existe en dehors de ce groupe.

### INTERPRÉTATION :
`CROSS_SOURCE_UNSEEN_RESBIM = NOT_AVAILABLE`. Aucune conclusion de généralisation hors-distribution cross-source ne peut être validée scientifiquement sur ce split sans risquer un biais de petit échantillon ou une contamination d'entraînement.

---

## Question 3 : Existe-t-il une amélioration mesurable du raisonnement spatial ?

### OBSERVATION :
Le dataset `REAL_DATA_PILOT` ne fournit aucune annotation métrique continue, coordonnées de boîtes englobantes ou graphes de connexions pièce-à-pièce formels. Les métriques continues sont documentées `METRIC_UNAVAILABLE`.
Sur le plan sémantique, le Base Model tente une description spatiale spécifique à chaque image (ex: "salon au centre", "chambre en haut à droite"). À l'inverse, RUN-019 récite invariablement la même formulation spatiale abstraite ("Le noyau de circulation central dessert les pièces principales...") indépendamment de la géométrie réelle de l'appartement.

### INTERPRÉTATION :
Il n'existe aucune amélioration mesurable du raisonnement spatial dans RUN-019. Le modèle ne s'adapte pas à la topologie spécifique de l'image présentée.

---

## Question 4 : Le modèle dépend-il réellement des informations visuelles ?

### OBSERVATION :
L'expérience d'ablation EVAL-D sur 10 assets x 5 conditions fournit les mesures suivantes :
- Similarité entre Image Originale et **Image 100% Noire** :
  - BASE MODEL : **4.3 %**
  - RUN-019 MODEL : **92.0 %**
- Similarité entre Image Originale et **Zones Architecturales Masquées** :
  - BASE MODEL : **6.2 %**
  - RUN-019 MODEL : **95.3 %**
- Similarité entre Image Originale et **Bruit Aléatoire Uniforme** :
  - BASE MODEL : **0.9 %**
  - RUN-019 MODEL : **90.6 %**

### INTERPRÉTATION :
**La dépendance visuelle de RUN-019 est QUASI-NULLE.**
Lorsque l'image est entièrement supprimée, noircie, ou remplacée par du bruit pur, le modèle RUN-019 continue de générer textuellement la critique architecturale complète avec une similitude supérieure à 98 %. À l'inverse, le Base Model réagit directement à l'altération visuelle (la similarité tombe sous les 50 %).

---

## Question 5 : L'amélioration existe-t-elle lorsque les indices textuels/formels sont contrôlés ?

### OBSERVATION :
Dans la CONDITION 5 (Text-Only, sans aucune image), RUN-019 produit une réponse quasi-identique à celle produite avec l'image originale (similarité : **95.7 %**).

### INTERPRÉTATION :
L'amélioration spectaculaire de loss observée dans RUN-019 est un phénomène purement textuel et linguistique. Le modèle répond au prompt textuel en déroulant le template appris, sans utiliser la modalité visuelle pour conditionner son raisonnement architectural.

---

## Question 6 : Que montre le Gold Set V3 ?

### OBSERVATION :
Le Gold Set V3 est sanctuarisé. Le fichier manifest officiel (`GOLD_V3_MANIFEST.jsonl`) n'est pas distribué dans le dépôt de code public conformément à `EVALUATION.md` §4 (exclu par `.gitignore`).

### INTERPRÉTATION :
`GOLD_EVALUATION = BLOCKED / NOT_AVAILABLE`. Aucune donnée n'a été artificiellement forgée pour combler cette absence.

---

## Question 7 : Quelles affirmations restent impossibles à démontrer ?

1. Il est **impossible d'affirmer** que RUN-019 "comprend" ou "voit" les plans d'architecture. L'expérience d'ablation visuelle prouve que le modèle fonctionne en quasi-déconnexion de l'image.
2. Il est **impossible d'affirmer** une compétence spatiale ou dimensionnelle généralisée.
3. Seul l'apprentissage stylistique, syntaxique et lexical du formalisme de critique AXIS est solidement démontré.
