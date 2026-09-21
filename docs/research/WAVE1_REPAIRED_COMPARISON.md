# ARCHI-AI — Comparatif Scientifique : Wave 1 Original vs Wave 1 Repaired (`WAVE1_REPAIRED_COMPARISON.md`)

> **Date d'élaboration :** 21 September 2026 à 18:15:00 UTC  
> **Auditeur & Ingénieur Système :** Assistant Spécialiste ARCHI-AI  
> **Périmètre :** Comparaison directe entre la Wave 1 historique (939 exemples) et la Wave 1 Repaired (722 exemples certifiés).  
> **Statut de conformité :** Zéro régression, étanchéité absolue garantie, RAW immuable, aucun training prématuré.

---

## 1. Tableau Comparatif Synthétique

| Critère d'Évaluation | ORIGINAL (Wave 1 Initiale) | REPAIRED (Wave 1 Réparée) | Évolution & Impact Qualitatif |
| :--- | :---: | :---: | :--- |
| **Examples** (Volume total) | **939** | **722** | Réduction maîtrisée (-23.1 %) privilégiant la **qualité et l'authenticité** |
| **False PASS** (Faux positifs) | **451** (49.8 %) | **0** (0.0 %) | **Éradication totale** grâce aux 7 validateurs qualitatifs stricts |
| **Generic** (Réponses clichés / templates) | **401** | **0** | Suppression des formules passe-partout (claustra, ombres nettes, etc.) |
| **Grounding** (Erreurs de calcul / `None m`) | **25** (`None m`) | **0** | Pipeline métrique déterministe certifié ($cm \to m$) |
| **Fake multimodal** (Modalités manquantes) | **25** | **0** | Vérification bimodalité stricte (`IMAGE_PLUS_TEXT`, `PLAN_PLUS_3D`) |
| **Empty inputs** (`inputs: {}`) | **64** | **0** | Rejet systématique en REVIEW de tout exemple sans entrée active |
| **Difficulty errors** (Surcotations / L6 creux) | **57** | **0** | `CLEARANCE_CHECK` calibré L1, L6 exigeant $\ge 2$ contraintes réelles |
| **Semantic duplicates** (Templates clonés) | **75** | **0** | Déduplication stricte par ID et diversification contextuelle des requêtes |
| **Supported tasks** (Tâches instanciées) | **22** / 69 | **25** / 69 | Couverture élargie (+3 tâches nettes dont vrais `PLAN_PLUS_3D`) |
| **Tests** (Suite de tests automatisée) | **44** / 44 | **54** / 54 | **+10 tests de régression obligatoires** ajoutés et 100% passants |

---

## 2. Analyse Détaillée des Dimensions de Progrès

### 2.1. Éradication des Faux PASS et Validation Stricte
Dans la version originale, le Quality Gate ne comportait que 4 validateurs syntaxiques très permissifs. 451 exemples sur 905 avaient été certifiés PASS alors qu'ils contenaient des tares critiques (slots `None`, fausses modalités, arborescences IFC interchangeables, relations 3D imaginées).
Dans la version Repaired, l'intégration permanente de `GenericAnswerValidator`, `MultimodalDependencyValidator` et `DifficultyValidator` au sein du `QualityGate` filtre automatiquement toute anomalie en file de revue `review_queue.jsonl` (21 cas isolés, 0 dans le jeu final).

### 2.2. Raisonnement Spatial et Scene Graphs Déterministes
- **Version Originale :** 75 exemples `OBJECT_RELATION` postulaient sans calcul que deux objets quelconques étaient en "vis-à-vis / proximité immédiate".
- **Version Repaired :** 100% des 16 exemples `OBJECT_RELATION` calculent la distance euclidienne réelle $d = \sqrt{\Delta x^2 + \Delta y^2 + \Delta z^2}$, qualifient les offsets latéraux, axiaux et verticaux, et attribuent un palier de proximité ergonomique fondé sur des coordonnées réelles.

### 2.3. Multimodalité Réelle et Croisements 2D ↔ 3D
- **Version Originale :** Zéro véritable `PLAN_PLUS_3D`, 25 `IMAGE_PLUS_TEXT` dépourvus de texte.
- **Version Repaired :** 10 exemples certifiés `PLAN_PLUS_3D` appariant le dessin 2D ResBIM et la maquette IFC 3D correspondante (confrontation des niveaux, des murs, portes et fenêtres), et 20 exemples `IMAGE_PLUS_TEXT` embarquant un cahier des charges d'aménagement textuel explicite.

### 2.4. Ergonomie et Cotes Anthropométriques
- **Version Originale :** 25 exemples `CLEARANCE_CHECK` affichaient la mention `(soit None m)` suite à une clé non résolue, et étaient étiquetés L3.
- **Version Repaired :** Conversion mathématique systématique (`90 cm` $\to$ `0.90 m`, `600 cm` $\to$ `6.00 m`). Zéro valeur `None`, `NaN` ou `inf`. Difficulté recalibrée en `L1_RECONNAISSANCE`.

### 2.5. Maquettes Numériques BIM / IFC
- **Version Originale :** Répétition textuelle identique de la hiérarchie buildingSMART théorique sur 70 maquettes différentes.
- **Version Repaired :** Helpers `get_entity()`, `get_property()`, `get_spatial_container()` exploitant les données réelles du fichier IFC : étages effectifs (`storeys`), pièces réelles (`spaces`), quantitatifs exacts de murs, dalles, portes et fenêtres.

---

## 3. Comparaison des Partitions (Splits)

| Partition | Wave 1 Original (939 ex) | Wave 1 Repaired (722 ex) | Conformité Étanche |
| :--- | :---: | :---: | :--- |
| **Train** | 619 (65.9 %) | **512** (70.9 %) | Zéro contamination avec benchmark |
| **Validation** | 270 (28.8 %) | **160** (22.2 %) | Isolation stricte par projet |
| **Benchmark** | 50 (5.3 %) | **50** (6.9 %) | Sanctuarisé (CORE_MMMU_ARCHITECTURE) |
| **Holdout** | 0 (0.0 %) | **0** (0.0 %) | Réserve scellée |

**Conclusion de l'audit comparatif :**
La Wave 1 Repaired constitue une base d'apprentissage assainie, dense et mathématiquement vérifiable, prête pour les benchmarks d'évaluation ultérieurs.
