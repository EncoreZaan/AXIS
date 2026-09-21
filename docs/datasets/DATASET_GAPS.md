# ARCHI-AI — Analyse des Lacunes & Angles Morts des Données (`DATASET_GAPS`)

## 1. Introduction

Une démarche scientifique et industrielle rigoureuse exige d'identifier avec lucidité les compétences que **les datasets publics existants ne permettent PAS d'enseigner directement** à un modèle multimodal, quelle que soit la quantité de données accumulée.

La majorité des datasets académiques indoor (Matterport3D, Structured3D, HM3D, RPLAN) ont été créés pour des tâches de **computer vision classique** (reconstruction 3D, estimation de profondeur, segmentation sémantique, navigation de robots aspirateurs). Ils sont pour la plupart :
- dépourvus de texte argumenté ou de critique spatiale ;
- limités à des typologies génériques d'appartements d'agences immobilières ;
- muets sur la culture architecturale, la qualité d'ambiance et la noblesse des matériaux ;
- totalement ignorants de la réglementation constructive française (PMR, ERP, CCH).

Ce document dresse l'inventaire précis de ces angles morts et définit les **stratégies concrètes de remédiation**.

---

## 2. Inventaire des 8 Lacunes Critiques

```text
                                LES 8 ANGLES MORTS CRITIQUES
                                              │
         ┌───────────────────┬────────────────┼───────────────────┐
         ▼                   ▼                ▼                   ▼
    GAP 1 : PARTI PRIS  GAP 2 : CRITIQUE  GAP 3 : MULTI-DOC   GAP 4 : SECOND ŒUVRE
   (Intention d'auteur)  (Jury d'atelier)  (Plan + Coupe + Vue) (Détails réels)
         │                   │                │                   │
         ├───────────────────┼────────────────┼───────────────────┤
         ▼                   ▼                ▼                   ▼
    GAP 5 : NORMES FR   GAP 6 : PÉDAGOGIE GAP 7 : MATIÈRES    GAP 8 : SUBTILITÉ
    (ERP, PMR, CCH)     (Maïeutique)     (Toucher & Patine)  (Lumière sensible)
```

---

### GAP 1 : Le "Parti Pris" et l'Intention Architecturale
- **Description de la lacune :** Aucun dataset public ne contient d'explication formalisée sur le *parti pris* d'un projet d'architecture intérieure (ex. pourquoi avoir créé une percée visuelle traversante depuis l'entrée vers le jardin ? pourquoi avoir choisi une boîte dans la boîte pour isoler la salle d'eau ?). Les annotations existantes se bornent à étiqueter : `wall`, `sofa`, `door`.
- **Conséquence sur le modèle :** Le modèle risque de décrire les objets présents sans comprendre la logique génératrice du plan.
- **Stratégie de remédiation :** 
  - Curation d'un sous-ensemble dédié de **notices d'architectes** (concours, revues d'architecture de référence, dossiers de projets diplômants).
  - Génération supervisée de chaînes de pensée (*Chain-of-Thought*) reliant le besoin programmatique au geste spatial.

---

### GAP 2 : La Critique Argumentée de Studio ("Critique de Projet")
- **Description de la lacune :** Dans une école d'architecture intérieure, un enseignant n'énumère pas les meubles : il diagnostique les dysfonctionnements, souligne les contradictions d'échelle, questionne la hiérarchie des volumes et challenge l'étudiant. Les datasets de vision actuels n'ont aucune culture de la critique constructive négative ou équilibrée.
- **Conséquence sur le modèle :** Tendance à l'adulation passive et aux compliments superficiels (*"Ce magnifique salon présente un canapé gris très élégant..."*), ce qui est inutile pour un professionnel ou un étudiant.
- **Stratégie de remédiation :**
  - Curation d'un corpus expert de **diagnostics critiques** structurés selon la méthode :
    1. *Constat objectif (OBSERVÉ)* ;
    2. *Point de friction fonctionnel ou esthétique* ;
    3. *Règle architecturale enfreinte* ;
    4. *Alternative concrète d'amélioration*.
  - Intégration de paires contrastives (contre-exemples volontairement dysfonctionnels annotés).

---

### GAP 3 : Le Raisonnement Holistique Multi-Documents (Plan + Coupe + Rendu + Moodboard)
- **Description de la lacune :** Presque tous les datasets existants associent au mieux une image et un texte, ou un plan 2D isolé. Aucun dataset public n'associe simultanément pour un même projet :
  - Le plan côté au 1/50e ;
  - La coupe longitudinale avec hauteurs sous plafond ;
  - Le moodboard de matériaux (échantillons) ;
  - La perspective d'ambiance finale.
- **Conséquence sur le modèle :** Incapacité native à détecter qu'une cloison dessinée sur le plan a été oubliée sur le rendu 3D, ou que le parquet posé en chevron sur le rendu est représenté droit sur le plan de calepinage.
- **Stratégie de remédiation :**
  - Exploitation des paires multi-vues alignées de `Structured3D` et `ResBIM`.
  - Construction d'un jeu synthétique de **divergences contrôlées** (introduire une incohérence sur le rendu et entraîner le modèle à la relever par comparaison avec le plan).

---

### GAP 4 : Les Détails Constructifs et le Second Œuvre Intérieur
- **Description de la lacune :** Les modèles de vision voient des surfaces lisses. Ils ignorent :
  - l'épaisseur d'une ossature métallique de cloison Placostil (72/48) ;
  - le passage des gaines techniques d'évacuation gravitaire des eaux vannes (pente de 1 à 2 cm/m) ;
  - la réservation pour receveur de douche à l'italienne ;
  - les plinthes à gorge, retombées de faux-plafonds et trappes de visite.
- **Conséquence sur le modèle :** Proposition d'aménagements impossibles à réaliser sur le plan technique (ex. déplacer un WC à 10 mètres de la colonne de chute sans estrade, ou abattre une cloison sans vérifier les réseaux).
- **Stratégie de remédiation :**
  - Injection des fiches techniques du CSTB et des **DTU de second œuvre dans le RAG**.
  - Développement d'un outil déterministe de vérification de faisabilité des fluides et des hauteurs sous plafond techniques.

---

### GAP 5 : La Réglementation et la Normalisation Française (PMR / ERP / CCH)
- **Description de la lacune :** 99% des datasets de recherche sont anglo-saxons ou asiatiques. Les normes américaines (ADA) diffèrent profondément des normes françaises (Arrêté du 24 décembre 2015 pour les logements, arrêté du 25 juin 1980 modifié pour les ERP). Les notions d'UP (Unités de Passage), de girons et d'échappées d'escaliers (norme NF P 01-012) sont absentes des corpus d'entraînement.
- **Conséquence sur le modèle :** Hallucination de cotes non réglementaires en France (ex. affirmer qu'une porte de 70 cm est accessible PMR).
- **Stratégie de remédiation :**
  - **Refus formel d'apprendre les normes par cœur dans les poids du modèle.**
  - **Architecture RAG stricte** couplée à un moteur de vérification déterministe qui interroge les textes de Légifrance et du Cerema pour chaque diagnostic de conformité.

---

### GAP 6 : La Posture Pédagogique et la Maïeutique
- **Description de la lacune :** Les datasets de questions/réponses actuels sont télégraphiques et doctrinaires. Ils ne pratiquent pas le questionnement socratique qui caractérise la pédagogie en école d'art et d'architecture.
- **Conséquence sur le modèle :** Réponse brutale et directive ("Faites ceci"), au lieu de stimuler la réflexion de l'étudiant ("Avez-vous pensé à la manière dont la lumière matinale pénètre dans cette pièce si vous placez le dressing contre cette baie ?").
- **Stratégie de remédiation :**
  - Entraînement sur des templates de dialogues didactiques guidés (`LearningType.PEDAGOGY`).
  - Utilisation de prompts système modulant l'attitude selon le profil utilisateur (Mode Étudiant vs Mode Maître d'œuvre).

---

### GAP 7 : La Sensibilité aux Matériaux et à la Patine Réelle
- **Description de la lacune :** Les modèles de vision classent "bois" ou "marbre", mais peinent à distinguer un chêne blanchi brossé d'un stratifié imitation chêne, ou un marbre Calacatta d'un terrazzo ou d'un grès cérame poli.
- **Conséquence sur le modèle :** Vocabulaire pauvre et générique, incapable de prescrire des finitions réalistes au niveau attendu d'un architecte d'intérieur.
- **Stratégie de remédiation :**
  - Intégration du dataset spécialisé **`MatSynth`** (4K PBR tileable avec étiquetage fin des traitements de surface et de la rugosité).
  - Création d'une matériauthèque textuelle RAG avec fiches techniques fabricants.

---

### GAP 8 : La Compréhension de la Lumière Sensible et de l'Ambiance
- **Description de la lacune :** Les modèles détectent la présence d'une lampe ou d'une fenêtre, mais ne savent pas qualifier l'ambiance lumineuse (lumière rasante mettant en valeur la matière d'un mur en pierre, température de couleur blanc chaud 2700K vs blanc neutre 4000K, facteur d'éblouissement UGR, éclairage d'accentuation vs éclairage d'ambiance).
- **Conséquence sur le modèle :** Recommandations d'éclairage limitées à "ajoutez des lampes".
- **Stratégie de remédiation :**
  - Entraînement sur les panoramas photométriques calibrés de **`Laval Indoor HDR`** et **`OpenRooms`**.
  - Vocabulaire spécialisé supervisé associant lumens, kelvins, IRC et types de diffusion lumineuse.

---

## 3. Synthèse des Stratégies de Remédiation

| Lacune / Angle Mort | Gravité | Solution Privilégiée | Données / Dispositif |
|---|---|---|---|
| **Intention / Parti pris** | Élevée | Supervision de raisonnement (CoT) | Notices de concours d'architecture |
| **Critique de studio** | Majeure | Fine-tuning sur diagnostics contrastifs | Corpus Expert Curated ARCHI-AI |
| **Multi-documents croisés** | Élevée | Entraînement multi-images synchronisé | Structured3D + ResBIM avec paires altérées |
| **Détails second œuvre** | Moyenne | RAG technique + Outils fluides | DTU 25.41 / DTU 52.1 + Règles de pente |
| **Normes françaises PMR/ERP** | Critique | RAG légal + Outil déterministe | Textes Légifrance consolidés + Guardrails |
| **Posture pédagogique** | Moyenne | Fine-tuning de tonalité et maïeutique | Dialogues socratiques annotés |
| **Matériaux & finitions** | Élevée | Dataset PBR haute définition | MatSynth + ambientCG + Fiches fabricants |
| **Lumière sensible** | Élevée | Dataset HDR photométrique | Laval Photometric HDR + Vocabulaire Kelvin/lux |
