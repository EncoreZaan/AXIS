# ARCHI-AI — Plan de Montée en Charge & Scénarios d'Échelle (`DATASET_SCALE_PLAN`)

## 1. Introduction & Méthodologie d'Évaluation

Dans la construction d'un système expert multimodal, le volume de données ne doit jamais être choisi arbitrairement. Chaque palier d'échelle répond à des objectifs précis de compétence, de généralisation et de robustesse, tout en imposant des contraintes logistiques (stockage, preprocessing, temps d'entraînement, bande passante, mémoire GPU et coûts financiers).

Ce document compare de manière chiffrée et factuelle **quatre scénarios d'échelle** pour ARCHI-AI :
1. **Scénario 10k** : Le palier d'alignement chirurgical (haute densité d'expertise).
2. **Scénario 25k** : Le compromis optimal de référence (spécialisation robuste et couverture complète des 18 domaines).
3. **Scénario 50k** : Le palier de grande diversité typologique et stylistique (multi-échelles, grands ERP, micro-logements).
4. **Scénario 100k+** : L'industrialisation complète et le pré-entraînement continu de domaine.

---

## 2. Tableau Comparatif Synthétique des 4 Scénarios

| Critère d'Évaluation | Scénario 10k *(Alignement)* | Scénario 25k *(Optimal)* | Scénario 50k *(Grande Diversité)* | Scénario 100k+ *(Industriel)* |
|---|---|---|---|---|
| **Nombre d'exemples supervisés** | **10 000** | **25 000** | **50 000** | **100 000 à 150 000** |
| **Volume images/plans bruts (PNG/JPG)** | ~15 à 25 GB | ~40 à 70 GB | ~90 à 160 GB | ~200 à 400 GB |
| **Volume annotations (JSONL)** | ~35 MB | ~90 MB | ~200 MB | ~500 MB |
| **Temps de preprocessing (CPU i5-14400F)** | ~2 h | ~5 h | ~11 h | ~24 h (parallélisé) |
| **VRAM minimale d'entraînement (QLoRA 4-bit)** | 16 GB | 18 GB | 20 GB | 24 GB+ (ou multi-GPU) |
| **Temps RunPod RTX 3090 (24 GB)** | ~6 h | ~15 h | ~32 h | ~70 h (non recommandé en mono-GPU) |
| **Temps RunPod A100 SXM4 (80 GB)** | ~2 h | ~4,5 h | ~9 h | ~18 h |
| **Coût estimé RunPod (RTX 3090 @ 0,34$/h)** | **~2,04 $** | **~5,10 $** | **~10,88 $** | **~23,80 $** |
| **Coût estimé RunPod (A100 @ 1,89$/h)** | **~3,78 $** | **~8,50 $** | **~17,00 $** | **~34,00 $** |
| **Faisabilité locale (RTX 4060 Ti 8 GB)** | Inférence seule / Micro-tests | Inférence seule / Micro-tests | Inférence seule | Inférence seule |
| **Risque principal** | Sous-couverture des cas rares | Effort de curation soutenu | Bruit / redondance visuelle | Dilution de la qualité & surcoût de labeling |
| **Indice de diversité stylistique** | 7 / 10 | 9 / 10 | 9,5 / 10 | 10 / 10 |

---

## 3. Analyse Détaillée par Scénario

```text
                                ÉCHELLE DE MATURITÉ DU DATASET
                                              │
    ┌───────────────────┬─────────────────────┼────────────────────┐
    ▼                   ▼                     ▼                    ▼
[ 10k EXEMPLES ]    [ 25k EXEMPLES ]      [ 50k EXEMPLES ]     [ 100k+ EXEMPLES ]
Alignement Fin      Cœur de Compétence    Grande Diversité     Pré-entraînement
Chirurgical         Recommandé            Spécialisée          Continu Industriel
```

---

### Scénario 1 : 10 000 Exemples — "L'Alignement Chirurgical"

- **Objectif :** Spécialiser le comportement, le vocabulaire et le format de diagnostic d'ARCHI-AI avec une densité maximale de qualité, sans stocker d'exemples répétitifs.
- **Répartition des volumes :**
  - *Plans 2D & Topologie :* 2 500 exemples (ResPlan, CubiCasa5K, MSD).
  - *Perception spatiale & Enveloppe :* 2 500 exemples (Structured3D, StructScan3D).
  - *Styles & Matériaux :* 2 500 exemples (MMIS, MatSynth).
  - *Raisonnement, Ergonomie, Critique :* 2 500 exemples (IL3D, Expert Curated).
- **Avantages :**
  - Preprocessing très rapide (< 2 heures sur machine locale).
  - Audit de qualité faisable manuellement ou semi-automatiquement sur une part significative du dataset.
  - Entraînement en un après-midi sur RunPod (RTX 3090 pour ~2$).
  - Aucun risque de saturer le disque dur local (16 GB suffisent largement).
- **Limites :**
  - Risque d'oubli ou de mauvaise généralisation sur les styles rares (ex. brutaliste, Memphis, wabi-sabi extrême) et les programmes complexes (ERP, hôtels, musées).
  - Couverture limitée des variantes de symboles d'architectes régionaux.

---

### Scénario 2 : 25 000 Exemples — "Le Standard de Référence ARCHI-AI" *(RECOMMANDÉ)*

- **Objectif :** Offrir une couverture complète et exhaustive des 18 domaines métier, incluant la totalité des 40 styles d'intérieur, les différentes typologies de logements (studios étudiants, appartements haussmanniens, lofts, maisons individuelles), et une riche diversité de plans techniques.
- **Répartition des volumes :**
  - *Plans 2D & DAO/CAD :* 6 000 exemples (ResPlan 2 500, MSD 1 500, CubiCasa5K 1 000, FloorPlanCAD 1 000).
  - *Perception spatiale & 3D :* 6 000 exemples (Structured3D 3 000, StructScan3D 1 000, IL3D 2 000).
  - *Styles, Matériaux & Ambiance :* 6 000 exemples (MMIS 4 000, MatSynth 1 000, Laval HDR 1 000).
  - *Raisonnement, Circulation, Ergonomie :* 4 000 exemples (M3DLayout, CHOrD, Anthropométrie).
  - *Critique, Pédagogie, Multi-documents :* 3 000 exemples (ARCHI-AI Curated & Synthetic).
- **Avantages :**
  - Ratio qualité/volume optimal pour un modèle de 7 milliards de paramètres (Qwen2-VL-7B).
  - Suffisamment de données pour que le modèle mémorise le vocabulaire technique précis sans surapprendre.
  - Temps d'entraînement très raisonnable (~15 h sur RTX 3090 ou ~4,5 h sur A100 pour moins de 10$).
  - Stockage maîtrisé (~50 GB d'images compressées et optimisées).
- **Limites :**
  - Nécessite une rigueur de déduplication et de détection de fuites (split leakage) sans faille.

---

### Scénario 3 : 50 000 Exemples — "La Grande Diversité Typologique"

- **Objectif :** Étendre l'expertise aux programmes complexes au-delà du résidentiel standard : bureaux, restaurants, commerces de détail, réhabilitations patrimoniales, structures hôtelières et tertiaires.
- **Répartition des volumes :**
  - *Plans & CAD :* 14 000 exemples (intégration de fragments d'ArchCAD-400K).
  - *Scènes 3D & Espaces :* 14 000 exemples (Structured3D étendu, InteriorGS, Matterport3D sélectif).
  - *Styles & Matériauthèque :* 10 000 exemples (MMIS étendu, textures PBR variées).
  - *Ergonomie & Normes :* 6 000 exemples (gabarits ERP, issues de secours).
  - *Critique de projet & Maïeutique :* 6 000 exemples.
- **Avantages :**
  - Robustesse absolue face aux plans bruités ou mal scannés.
  - Capacité à traiter des projets hors-normes (duplex, mezzanines, combles, sous-sols aménagés).
- **Limites & Risques :**
  - Temps d'entraînement dépassant 30 heures sur une seule RTX 3090, justifiant le recours à une A100 ou un cluster bi-GPU.
  - Risque d'introduire des exemples de moindre qualité (bruit de labellisation dans les datasets massifs).
  - Stockage nécessitant ~150 GB d'espace disque dédié.

---

### Scénario 4 : 100 000+ Exemples — "L'Industrialisation & Pré-Entraînement Continu"

- **Objectif :** Réentraîner ou pré-entraîner de manière continue les couches de vision et le connecteur multimodal de Qwen2-VL sur l'architecture intérieure avant la phase d'instruction tuning.
- **Composition :**
  - 50 000 paires image ↔ description d'ambiance et d'espace (pre-training).
  - 30 000 plans d'étage et CAD vectoriels (apprentissage de la géométrie).
  - 20 000 paires de dialogue expert instruction-tuned (critique, diagnostic, conformité).
- **Avantages :**
  - Ancrage profond de la représentation spatiale dans l'espace latent du modèle.
  - Comportement d'expert natif sans artefact d'alignement superficiel.
- **Limites & Risques :**
  - Coût GPU significatif (> 100$ avec itérations et ablations).
  - Infrastructure de données lourde nécessitant un cluster de stockage distribué.
  - Rendements décroissants : pour une utilisation interactive en tutorat et critique, le modèle 25k ou 50k associé à un excellent RAG apporte une fiabilité souvent supérieure à un modèle 100k+ gavé de données non filtrées.

---

## 4. Recommandation Stratégique Par Étapes

La feuille de route d'ARCHI-AI adopte une **approche incrémentale par jalons validés** :

$$\text{Jalon 0 (25 ex.)} \xrightarrow{\quad\text{Validé}\quad} \mathbf{\text{Jalon 1 (10k ex.)}} \xrightarrow{\quad\text{Ablation}\quad} \mathbf{\text{Jalon 2 (25k ex.)}} \xrightarrow{\quad\text{Expansion}\quad} \mathbf{\text{Jalon 3 (50k ex.)}}$$

1. **Jalon 1 : Constitution du Core 10k.** 
   Permet d'aligner le pipeline de tokenisation, de vérifier l'absence d'overfitting et de mesurer le premier grand saut de performance sur le Benchmark indépendant.
2. **Jalon 2 : Déploiement du Standard 25k.**
   C'est la cible recommandée pour la version de production de l'expert ARCHI-AI. Elle offre l'équilibre parfait entre précision, coût RunPod (< 10$) et rigueur métier.
3. **Jalon 3 : Expansion à 50k (Optionnelle).**
   Déclenchée uniquement si le Benchmark du Jalon 2 révèle des faiblesses persistantes sur des programmes tertiaires ou des styles très marginaux.
