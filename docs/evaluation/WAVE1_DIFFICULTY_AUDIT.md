# ARCHI-AI — Audit de la Difficulté & Curriculum L1-L6 (`WAVE1_DIFFICULTY_AUDIT.md`)

> **Date d'audit :** 21 September 2026 à 14:55:00 UTC  
> **Auditeur Spécialiste :** Expert Curriculum Cognitif ARCHI-AI  
> **Question Clé :** *"Le niveau L1 à L6 déclaré correspond-il réellement à la complexité de la tâche, ou observe-t-on des distorsions d'étiquetage ?"*  

---

## 1. Vue d'Ensemble de l'Échelle Cognitive L1 à L6

L'échelle L1 à L6 d'ARCHI-AI définit le curriculum d'apprentissage progressif du modèle :
- **L1 (Reconnaissance) :** Identification directe d'entités visibles ou dénomination élémentaire.
- **L2 (Compréhension) :** Organisation générale, distribution des fonctions sans calcul complexe.
- **L3 (Analyse) :** Métrés précis, topologie spatiale, canaux PBR, photométrie.
- **L4 (Raisonnement) :** Conflits d'usage, flux de circulation, requêtes BIM relationnelles.
- **L5 (Expertise) :** Synthèse critique de studio, réglementation stricte (PMR/ERP).
- **L6 (Multicontrainte) :** Arbitrage complexe sous faisceau de contraintes contradictoires.

---

## 2. Matrice de Confusion Déclaré vs Réel (Audit Forensique)

La confrontation entre la difficulté déclarée dans les métadonnées et la complexité cognitive effective des réponses générées produit la matrice suivante (939 exemples) :

| Niveau Déclaré | Réel L1 | Réel L2 | Réel L3 | Réel L4 | Réel L5 | Réel L6 | Total Déclaré | Taux de Concordance |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **L1 — Reconnaissance** | **80** | 0 | 0 | 0 | 0 | 0 | **80** | **100.0 %** |
| **L2 — Compréhension** | 0 | **102** | 0 | 0 | 0 | 0 | **102** | **100.0 %** |
| **L3 — Analyse** | 25 | 0 | **507** | 0 | 0 | 0 | **532** | **95.3 %** |
| **L4 — Raisonnement** | 0 | 32 | 0 | **55** | 0 | 0 | **87** | **63.2 %** |
| **L5 — Expert** | 0 | 0 | 32 | 62 | **0** | 0 | **94** | **0.0 %** |
| **L6 — Multicontrainte** | 0 | 32 | 0 | 0 | 12 | **0** | **44** | **0.0 %** |
| **TOTAL RÉEL** | **105** | **166** | **539** | **117** | **12** | **0** | **939** | **79.2 % global** |

---

## 3. Analyse des Distorsions Majeures Détectées

### 3.1. Le Mirage du Niveau L6 (44 déclarés → 0 réel L6)
- **Tâche `TRADEOFF_ANALYSIS` (32 ex) :** Déclarée au niveau maximal L6 (Arbitrage multicontrainte).
  - *Réalité observée :* Ces 32 exemples possèdent un conteneur `inputs` **totalement vide**. La réponse est un template statique répétant mot pour mot l'arbitrage entre un "salon cathédrale baigné de lumière" et une "verrière atelier".
  - *Complexité réelle :* Niveau **L2** (simple récitation d'un cliché conceptuel, sans aucun calcul d'arbitrage).
- **Tâche `CONSTRAINT_REASONING` (12 ex) :** Déclarée L6.
  - *Réalité observée :* Analyse de textes réglementaires PMR avec préconisation de cloisons à galandage.
  - *Complexité réelle :* Niveau **L5** (expertise réglementaire rigoureuse, mais sans équation de compromis multicontrainte formelle).

### 3.2. L'Effondrement du Niveau L5 (94 déclarés → 0 réel L5)
- **Tâche `PROJECT_CRITIQUE` (32 ex) :** Déclarée L5 (Critique d'atelier).
  - *Réalité observée :* Répétition à l'identique de la même remarque ("manque de filtre spatial à l'entrée", "ajouter un claustra ajouré") sur tous les plans.
  - *Complexité réelle :* Niveau **L3** (analyse typologique superficielle).
- **Tâche `MULTIMODAL_PROJECT_REASONING` (50 ex — MMMU) :** Déclarée L5.
  - *Réalité observée :* La réponse fournie dans le dataset se résume à : `"Réponse certifiée du benchmark MMMU : A. Options : ..."` sans la moindre démonstration de calcul ni étape de raisonnement.
  - *Complexité réelle :* Niveau **L4** (QCM technique sans chaîne de pensée explicite).
- **Tâche `ACCESSIBILITY_ANALYSIS` (12 ex) :** Déclarée L5 → Niveau **L4** (restitution et commentaire d'un article réglementaire).

### 3.3. Dérive de la Tâche Pédagogique L4 (`GUIDED_REASONING` — 32 ex)
- Déclarée L4 (Guidage maïeutique).
- En raison de l'absence totale d'entrées spatiales (`inputs: {}`), le dialogue pédagogique proposé est déconnecté du plan et récite une devinette préfabriquée sur le croisement de deux personnes dans un couloir central.
- Complexité réelle : **L2**.

### 3.4. Surcotation de l'Ergonomie L3 (`CLEARANCE_CHECK` — 25 ex)
- Déclarée L3 (Analyse).
- La question demande : *"Quelle est la cote minimale pour 'couloir personne seule' ?"* et la réponse extrait `90 cm`.
- Il s'agit d'une simple interrogation de dictionnaire de constantes anthropométriques.
- Complexité réelle : **L1 (Reconnaissance / Consultation)**.

---

## 4. Recommandations de Recalibration pour le Supervision Engine

1. **Intégration du `DifficultyValidator` :** Déployé et validé lors de cet audit pour bloquer toute attribution automatique L5 ou L6 qui ne justifierait pas d'une matrice d'arbitrage ou d'une chaîne de pensée multi-étapes vérifiée.
2. **Reclassification formelle des exemples de Wave 1 :** Réaligner les métadonnées `difficulty` des 195 exemples mal calibrés avant tout entraînement pour éviter de biaiser le conditionnement du modèle RWKV sur les tokens de difficulté.
3. **Véritables tâches L6 en Wave 2 :** Générer de vrais scénarios multicontraintes où l'étudiant/modèle doit arbitrer entre :
   - Surface utile minimale CCH (ex: chambre ≥ 9 m²).
   - Dégagement PMR obligatoire (cercle Ø 1,50 m et passage ≥ 0,90 m).
   - Contrainte budgétaire (€/m²) et structurelle (gaine technique fixe inamovible).
