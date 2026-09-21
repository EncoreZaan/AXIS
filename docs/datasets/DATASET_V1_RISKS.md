# ARCHI-AI — Analyse des Risques, Biais & Atténuations (Dataset V1)

Ce document analyse exhaustivement les risques méthodologiques, techniques, juridiques et qualitatifs associés à la constitution du Dataset V1 d'**ARCHI-AI**, et formalise les protocoles de mitigation mis en œuvre.

---

## 1. Cartographie des Risques Majeurs

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                       MATRICE DES RISQUES ARCHI-AI                      │
│                                                                         │
│   Élevé  │ [Biais Géographique]               [Risque Licence NC]       │
│          │ [Biais Stylistique Urbain]         [Fuite Inter-Pièces/Scène]│
│          │                                                              │
│  Moyen   │ [Surreprésentation Salon/Chambre]  [Artefacts Synthèse 3D]   │
│          │ [Redondance des Plans Miroirs]     [Bruit d'Annotation IA]   │
│          │                                                              │
│  Faible  │ [Format d'Export Qwen-VL]          [Déduplication Exacte]    │
│          └───────────────────────────────────────────────────────────── │
│                         Faible                Moyen             Élevé   │
│                                      IMPACT                             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Analyse Détaillée par Axe de Risque

### 2.1 Risque Juridique & Licence (Sévérité : ÉLEVÉE)
- **Description du risque :** Intégration accidentelle d'un dataset contenant une clause restrictive (CC BY-NC, Matterport EULA) dans le corpus d'entraînement de production, rendant les poids du modèle inexploitables commercialement ou exposés à des litiges.
- **Exemples concrets constatés lors de l'audit :**
  - `Matterport3D` et `HM3D` : clause unilatérale stipulant que les modèles entraînés constituent des informations dérivées soumises à leur EULA.
  - `OpenRooms` : dépendance indirecte aux droits commerciaux d'Adobe Stock sur les textures.
- **Protocole d'atténuation ARCHI-AI :**
  - Cloisonnement étanche : le socle de production `Core V1` n'admet que les licences permissives vérifiées (**Apache-2.0, CC BY 4.0**).
  - Tout dataset sous licence non commerciale (ex: `CubiCasa5K`, `HSSD`) est cantonné dans une branche d'expérimentation académique explicitement documentée.

---

### 2.2 Biais Géographiques & Typologiques (Sévérité : ÉLEVÉE)
- **Description du risque :** La majorité des datasets de recherche sont collectés dans une seule aire culturelle ou géographique, induisant des réflexes architecturaux inadaptés à d'autres contextes.
- **Constats d'audit :**
  - `RPLAN` : 100% appartements urbains chinois des années 2010 (tours résidentielles, cuisines fermées standardisées, loggias au sud, distribution traversante systématique).
  - `Matterport3D` : 100% maisons individuelles suburbaines nord-américaines (structure ossature bois, cloisons plâtre épaisses, dressings géants, très grandes surfaces au sol).
  - `MSD` : Bâtiments suisses de logements collectifs (règles strictes de sécurité incendie, paliers centraux, isolation renforcée).
- **Conséquence modèle :** Un modèle entraîné uniquement sur `RPLAN` et `Matterport3D` hallucinerait des typologies américaines ou chinoises inadaptées à un projet haussmannien ou méditerranéen européen.
- **Protocole d'atténuation ARCHI-AI :**
  - Équilibrage multipolaire :
    - Échelle européenne / suisse (`MSD` : 5 372 plans collectifs).
    - Échelle nordique / globale (`CubiCasa5K` : Finlande/Scandinave).
    - Diversité résidentielle internationale (`ResPlan` : 17 000 plans).
    - Architecture latino-américaine parasismique (`MLSTRUCT-FP`).
  - Sous-échantillonnage de `RPLAN` bridé à un maximum de 10% du volume total de plans.

---

### 2.3 Biais Stylistiques & Décoratifs (Sévérité : MOYENNE À ÉLEVÉE)
- **Description du risque :** Tendance naturelle des banques d'images d'intérieur à surreprésenter le style "moderne minimaliste blanc" ou le "scandinave bois clair", au détriment de l'histoire de l'architecture intérieure.
- **Constat d'audit :** De nombreux datasets récents comme `aishahsofea/interior-design` ou les générateurs diffusion sont saturés de salons scandinaves ou contemporains neutres interchangeables.
- **Protocole d'atténuation ARCHI-AI :**
  - Utilisation de `MMIS` comme régulateur stylistique : quotas stricts de 75 exemples pour chacun des **40 styles d'architecture d'intérieur distincts** (Art Déco, Mid-Century Modern, Japandi, Bauhaus, Industriel, Wabi-Sabi, Memphis, Classique Français, etc.).
  - Interdiction d'avoir un style représentant plus de 5% du corpus global.

---

### 2.4 Biais de Représentation des Pièces (Sévérité : MOYENNE)
- **Description du risque :** Les salons (*living rooms*) et chambres principales (*master bedrooms*) représentent souvent plus de 70% des photographies collectées, tandis que les espaces techniques indispensables (buanderies, celliers, entrées, circulations, toilettes séparées, couloirs) sont négligés.
- **Conséquence modèle :** Le modèle devient incapable de concevoir ou critiquer une entrée fonctionnelle ou un dégagement de salle d'eau.
- **Protocole d'atténuation ARCHI-AI :**
  - Quotas typologiques imposés dans le sous-échantillonnage de `MMIS` et `ResPlan` :
    - Salons & séjours : 25%
    - Chambres : 25%
    - Cuisines : 20%
    - Salles de bains & sanitaires : 15%
    - Espaces de distribution & circulations (entrées, couloirs, paliers) : 15%

---

### 2.5 Synthétique vs Réel : Le Piège des Données Artificielles (Sévérité : MOYENNE)
- **Description du risque :**
  - Les scènes purement synthétiques (CAO) souffrent souvent d'un "syndrome de maquette parfaite" (lumière mathématique sans poussière, absence de vie, pas de câbles électriques, textures sans patine).
  - Les scans 3D réels bruts souffrent de l'extrême inverse : trous de maillage, textures étirées, miroirs non réfléchissants noirs, distorsions optiques.
- **Protocole d'atténuation ARCHI-AI :**
  - **Stratégie hybride 50/50 :**
    - 50% de scènes et plans réels (`StructScan3D`, `ResPlan`, `MSD`, `CubiCasa5K`, `MMIS`) pour ancrer le bon sens physique et les imperfections de la réalité.
    - 50% de synthétique haute qualité (`IL3D`, `M3DLayout`, `Structured3D`) pour la pureté géométrique et la clarté des alignements.

---

### 2.6 Duplication Exacte & Plans Miroirs (Sévérité : MOYENNE)
- **Description du risque :** Dans les grands programmes immobiliers, les promoteurs déclinent le même plan en miroir (gauche/droite) ou le répètent à chaque étage d'une tour. Entraîner un modèle sur ces répétitions mène à un surapprentissage stérile.
- **Protocole d'atténuation ARCHI-AI :**
  - Déduplication cryptographique **SHA-256** (élimination des fichiers identiques).
  - Déduplication perceptuelle **pHash (Average Hash 64-bit)** : les images dont la distance de Hamming est <= 4 sont regroupées et une seule est retenue.
  - Détection géométrique des plans miroirs via l'outil `deduplication_analyzer`.

---

### 2.7 Fuite d'Apprentissage & Contamination des Splits (Sévérité : CRITIQUE)
- **Description du risque :** Si une photo de la cuisine d'une maison se trouve dans le split `train` et une photo du salon de la **même maison** se trouve dans le split `test`, le modèle "reconnaît" la maison au lieu de généraliser. De même, si le plan d'un appartement est en test alors que sa vue 3D est en train, le benchmark est entièrement falsifié (*data leakage*).
- **Protocole d'atténuation ARCHI-AI :**
  - **Verrouillage par `scene_id` et `building_id` :** la fonction `split_leak_detector` vérifie qu'aucun identifiant de scène, de projet ou de bâtiment n'est partagé entre train, validation et test.
  - Test d'étanchéité perceptuelle pHash entre splits : alerte immédiate si une image de test présente une similarité >90% avec une image d'entraînement.

---

### 2.8 Qualité des Annotations & Pseudo-Labels IA (Sévérité : MOYENNE)
- **Description du risque :** Des datasets récents génèrent leurs annotations par IA (pseudo-ground truth) sans relecture humaine experte, propageant des erreurs d'interprétation architecturale.
- **Protocole d'atténuation ARCHI-AI :**
  - Priorité absolue aux datasets disposant d'annotations humaines vérifiées ou de modèles géométriques mathématiques (`ResPlan`, `MSD`, `IL3D`, `StructScan3D`).
  - Validation QA systématique par notre pipeline `qa_validator` (vérification de conformité taxonomique, détection des réponses vides ou creuses).

---

## 3. Synthèse des Barrières de Sécurité ARCHI-AI V1

| Risque | Mécanisme de Défense ARCHI-AI | Outil Automatisé Associé |
| :--- | :--- | :--- |
| **Licence** | Cloisonnement Core Libre (Apache/CC-BY) vs Recherche | `Provenance.license` dans Master Schema |
| **Fuite (Leakage)** | Partitionnement strict par `scene_id` et vérification pHash | `dataset_tools/validation/split_leak_detector.py` |
| **Doublons** | Filtre SHA-256 + pHash distance <= 4 | `dataset_tools/deduplication/dedup_analyzer.py` |
| **Biais Géographique** | Quotas multicontinentaux stricts (Europe, US, Asie, LatAm) | Métadonnées de provenance |
| **Biais Stylistique** | 40 styles régulés à 75 exemples chacun (MMIS) | `category` / `style` dans Master Schema |
| **Biais Typologique** | Répartition équilibrée (Salons, Chambres, Cuisines, Bains, Flux) | `subcategory` / `space_type` |
| **Qualité QA** | Règles de validation syntaxique, sémantique et Pydantic | `dataset_tools/validation/qa_validator.py` |
