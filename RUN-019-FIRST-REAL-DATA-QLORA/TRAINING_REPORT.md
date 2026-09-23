# AXIS — Phase 4 Training Report (`RUN-019-FIRST-REAL-DATA-QLORA`)

> **Run Identifier:** `RUN-019-FIRST-REAL-DATA-QLORA`  
> **Date:** 2026-09-22 / 2026-09-23  
> **Audited Git Commit:** `f4d5e949053743d97091ea35080de5d365899df7`  
> **Status:** **COMPLETE** | **TRAINING_RUN_VALID: YES**

---

## 1. Pourquoi ce run a été effectué

La Phase 3 d'AXIS a conclu le cycle d'audit et d'ingestion de données réelles, aboutissant à un dataset expérimental certifié de 1 000 assets architecturaux (`REAL_DATA_PILOT`), scellé par empreintes SHA-256 et validé par un dry run à zéro pas d'optimiseur (`RUN-018-REAL_DATA_DRY_RUN`).

L'objectif de `RUN-019-FIRST-REAL-DATA-QLORA` est d'exécuter le **premier entraînement scientifique réel contrôlé** d'AXIS. Conformément à l'hypothèse pré-enregistrée, ce run ne vise pas à proclamer une capacité architecturale surhumaine ou générale, mais à répondre rigoureusement à la question expérimentale :
> *Sur le pilote architectural réel verrouillé (1 000 assets), une adaptation QLoRA (r=16, α=32, 512px, lr=1e-4) de Qwen2-VL-7B-Instruct permet-elle une optimisation stable sans NaN/Inf, sans instabilité mémoire, avec une amélioration mesurable et reproductible de la loss d'entraînement et de validation par rapport à l'état initial ?*

---

## 2. Dataset Utilisé

Le run a exploité exclusivement le dataset congelé et cryptographiquement verrouillé dans `experiments/runpod_2026-09-22/REAL_DATA_PILOT/` :

- **Total assets uniques :** 1 000
- **Train split :** 775 assets (77.5 %)
- **Validation split :** 98 assets (9.8 %)
- **Test split :** 127 assets (12.7 %) — **Strictement Sanctuarisé (0 accès)**
- **Sources autorisées :** `CORE_RPLAN` (990 assets raster 2D) et `CORE_RESBIM_PAIRED` (10 paires certifiées 2D CAD / 3D IFC).
- **Sources exclues & sanctuarisées :** `CORE_FLOORPLANCAD` (quarantaine), `Master Dataset v2` (inchangé), `Gold Set V3` (sanctuaire absolu), `runtime fixture sample_interior.jpg` (exclu).

### Empreintes SHA-256 vérifiées avant entraînement :
- `train.jsonl`: `246e22b372180a6b4be6c61eeea77e10a2c2d35b7128503463d32d6185ec3c47`
- `validation.jsonl`: `23a0f44ec54a98202d2e47f582b901010f286f7ad83be990447317e0029cee0e`
- `test.jsonl`: `113b7313340d1026c6a693f6fb2e8b00fd41dde06485f299b13add1018f37eb1`
- `manifest.jsonl`: `340ce603432d0057837b6aab9484ad369895d0279023b79169f6ce62ab69564a`
- `dataset_config.json`: `1d07982755f61200614039912b498c2df5e29f8701599e3ef8da605a55f18996`
- `README.md`: `12b9af24029546580f77dfbfaa131e1bc5355ab247cb8059ee104651c8f06546`

---

## 3. Configuration Exacte du Run

| Hyperparamètre | Valeur Verrouillée | Statut |
| :--- | :--- | :---: |
| **Modèle de Base** | `Qwen/Qwen2-VL-7B-Instruct` | Conforme |
| **Model Revision** | `eed13092ef92e448dd6875b2a00151bd3f7db0ac` | Conforme |
| **Méthode** | QLoRA 4-bit (NF4, double quant, compute bfloat16) | Conforme |
| **LoRA Rank ($r$)** | 16 | Conforme |
| **LoRA Alpha ($\alpha$)** | 32 | Conforme |
| **LoRA Dropout** | 0.05 | Conforme |
| **Modules Cibles** | `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj` | Conforme |
| **Paramètres Entraînables** | 40,370,176 / 8,331,745,792 (0.485 %) | Conforme |
| **Tour Visuelle** | Gelée (`visual.requires_grad = False`) | Conforme |
| **Résolution Pixel** | `min_pixels: 200704`, `max_pixels: 262144` (~512x512) | Conforme |
| **Longueur de Séquence** | 1 536 tokens | Conforme |
| **Micro-batch size** | 1 par device | Conforme |
| **Gradient Accumulation** | 8 micro-batches (batch effectif = 8) | Conforme |
| **Nombre d'Époques** | 2 époques complètes (194 pas d'optimisation) | Conforme |
| **Learning Rate** | $1.0 \times 10^{-4}$ | Conforme |
| **LR Scheduler** | Cosine decay | Conforme |
| **Warmup** | 9 pas (~5 % du budget total de 194 pas) | Conforme |
| **Optimiseur** | `paged_adamw_8bit` | Conforme |
| **Gradient Checkpointing** | Activé (`True`) | Conforme |
| **Seed** | 42 | Conforme |

---

## 4. Environnement d'Exécution

- **Machine Hôte :** RunPod Remote GPU Instance (`territorial_green_minnow`)
- **GPU :** NVIDIA GeForce RTX 3090 (24,576 MiB VRAM physique, 24,124.2 MiB allouables PyTorch)
- **NVIDIA Driver :** `580.159.04`
- **CUDA Runtime :** 12.4 (PyTorch) / 13.0 (Driver)
- **Python :** 3.12.3 (environnement virtuel isolé `/workspace/AXIS/.venv`)
- **PyTorch :** 2.6.0+cu124
- **Transformers :** 5.17.0
- **PEFT :** 0.21.0
- **bitsandbytes :** 0.50.2

---

## 5. Durée d'Exécution

- **Évaluation initiale baseline :** 35.46 secondes
- **Entraînement (2 époques, 194 pas) :** 1 870.89 secondes (**31.18 minutes**)
- **Débit moyen entraînement :** 0.829 échantillons/seconde, 0.104 pas/seconde (~9.64 s par pas effectif de 8 micro-batches)
- **Évaluation finale validation :** 35.51 secondes
- **Génération qualitative (baseline + entraîné) :** ~120 secondes

---

## 6. Consommation Mémoire VRAM

- **VRAM Allouée Stable :** 7 988.05 MiB
- **VRAM Réservée Stable :** 11 686.00 MiB
- **Peak VRAM Enregistré :** **10 842.95 MiB** (sur une capacité totale de 24 576 MiB)
- **Marge de Sécurité Mémoire :** ~13.73 GiB de réserve inemployée (stabilité thermique et zéro risque d'OOM).
- **Incidents OOM :** 0

---

## 7 & 8. Évolution des Métriques (Training Loss & Validation Loss)

| Étape | Global Step | Époque | Training Loss | Validation Loss (98 assets) | Learning Rate | Grad Norm |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline Initial** | 0 | 0.00 | N/A | **2.4067** | $0.00$ | N/A |
| **Début Training** | 1 | 0.01 | 2.4005 | — | $1.11 \times 10^{-5}$ | 0.8965 |
| **Fin Warmup** | 9 | 0.09 | 0.9412 | — | $1.00 \times 10^{-4}$ | 0.3812 |
| **Mi-Époque 1** | 50 | 0.52 | 0.0418 | — | $8.83 \times 10^{-5}$ | 0.0612 |
| **Fin Époque 1** | 97 | 1.00 | 0.0345 | **0.0342** | $5.08 \times 10^{-5}$ | 0.0385 |
| **Mi-Époque 2** | 150 | 1.55 | 0.0337 | — | $1.39 \times 10^{-5}$ | 0.0321 |
| **Fin Époque 2** | 194 | 2.00 | **0.0343** | **0.0339** | $7.21 \times 10^{-9}$ | 0.0417 |

- **Training Loss Moyenne :** 0.1693
- **Validation Loss Delta :** **-2.3728** (soit une réduction de **-98.59 %**)
- **Anomalies numériques (NaN/Inf) :** 0
- **Explosion de gradient :** 0 (Norme stabilisée entre 0.03 et 0.11 après la phase d'acquisition du prompt).

---

## 9. Analyse de la Convergence

La courbe de loss révèle une dynamique en deux régimes très nets :
1. **Régime d'Alignement Syntaxique et Lexical (Pas 1 à 25) :** Décroissance exponentielle de la loss de 2.40 à 0.08 sous l'effet de l'acquisition du schéma structurel d'analyse architecturale (rubriques `OBSERVATION`, `ANALYSE`, `POINTS FORTS`, `POINTS DE VIGILANCE`, `RECOMMANDATION`).
2. **Régime de Stabilisation et d'Affinement Sémantique (Pas 26 à 194) :** Stabilisation asymptotique autour de 0.034. La loss de validation passe de 0.0342 à l'époque 1 à 0.0339 à l'époque 2, confirmant une absence totale de divergence ou d'overfitting destructeur.

---

## 10. Checkpoints Produits & Hachage Cryptographique

Les checkpoints ont été sauvegardés sous `experiments/runpod_2026-09-22/RUN-019-FIRST-REAL-DATA-QLORA/checkpoints/` et dupliqués à la racine :

- `checkpoint-97/` : Checkpoint de fin d'Époque 1 (adapter, optimizer, scheduler, rng_state, trainer_state, training_args)
- `checkpoint-194/` : Checkpoint final d'Époque 2 (adapter, optimizer, scheduler, rng_state, trainer_state, training_args)
- `final_adapter/` : Adaptateur LoRA déployable + configuration du processor et tokenizer.

### Empreintes Clés des Adaptateurs (SHA-256) :
- `checkpoint-194/adapter_model.safetensors`: `409d2098fbe6ea74c9659ab84b33d66179b2a294e95d360f36ce0fdd32685f22` (161,539,072 bytes)
- `final_adapter/adapter_model.safetensors`: `409d2098fbe6ea74c9659ab84b33d66179b2a294e95d360f36ce0fdd32685f22` (Identique bit-à-bit)
- `checkpoint-97/adapter_model.safetensors`: `af89f763db62d712f89e98920ecbe3825c9396aabd1fffea4df18450498dece6` (161,539,072 bytes)

L'inventaire complet des 23 fichiers de checkpoints avec leur taille et SHA-256 est consigné dans `checkpoint_hashes.json`.

---

## 11. Erreurs et Incidents Éventuels

- **Comportement pendant l'entraînement :** Zéro crash, zéro OOM, zéro NaN/Inf.
- **Incident de télémétrie post-entraînement résolu :** La fermeture anticipée du descripteur de fichier de log avant le hook final d'évaluation d'un callback a provoqué une exception bénigne lors de l'appel final à `trainer.evaluate()`. Comme l'évaluation d'époque 2 était déjà entièrement enregistrée dans `trainer_state.json` (val loss: `0.033865`), un script de finalisation indépendant (`finish_phase4_artifacts.py`) a extrait l'historique complet, réalisé l'inférence qualitative déterministe sur les checkpoints intacts, et généré tous les artefacts.

---

## 12 & 13. Comparaison Baseline / Entraîné & Évaluation Qualitative

5 échantillons de validation prédéterminés de façon fixe (indices 0, 20, 40, 60, 80) ont été soumis au même prompt exact en utilisant le modèle de base sans adaptateur, puis le modèle avec l'adaptateur de `checkpoint-194`.

### Synthèse Qualitative :
1. **Compréhension du contenu architectural :**
   - *Base :* Réponses vagues, spéculations incertaines (« la pièce semble être... », « probablement une salle de bains »), vocabulaire généraliste.
   - *Entraîné :* Identification immédiate de la nature du document (plan matriciel segmenté 256x256), reconnaissance de la typologie des cloisons séparatives et des baies.
2. **Cohérence et Structuration de la réponse :**
   - *Base :* Structure en liste à puces basique, style conversationnel flou.
   - *Entraîné :* Adoption stricte du protocole d'expertise architectural AXIS (`OBSERVATION`, `ANALYSE`, `POINTS FORTS`, `POINTS DE VIGILANCE`, `RECOMMANDATION`).
3. **Pertinence spatiale et topologique :**
   - *Base :* Confusions sur les liaisons entre pièces, approximations sur la distribution.
   - *Entraîné :* Qualification rigoureuse du noyau distributif central, dissociation nette des zones jour/nuit, compacité des circulations au profit de la surface habitable.
4. **Identification des éléments et recommandations techniques :**
   - *Base :* Aucune référence normative ni mention des contraintes de passage.
   - *Entraîné :* Prescription systématique de la vérification de largeur minimale de passage (norme 80 cm pour les portes intérieures) et mention explicite de l'absence d'échelle métrique absolue sur raster non coté.

---

## 14. Limites Scientifiques

Il est impératif de souligner les limites méthodologiques strictes de cette expérience :
1. **Biais de formalisme :** La réduction drastique de la loss (de 2.40 à 0.034) reflète en grande partie l'apprentissage de la grammaire et du canevas textuel standardisé des critiques architecturales RPLAN. Une faible cross-entropy ne prouve pas une compréhension spatiale géométrique tridimensionnelle universelle.
2. **Résolution d'image :** Les plans RPLAN sont des rasters 256x256 agrandis pour le processor. L'évaluation de plans vectoriels haute résolution (DXF, DWG ou rasters 4K) nécessitera d'autres protocoles.
3. **Biais typologique :** Le corpus RPLAN est dominé par des appartements résidentiels compacts. La transférabilité à des équipements publics, bureaux ou bâtiments industriels demeure non mesurée.

---

## 15. Conclusions Strictement Supportées par les Données

1. Le pipeline QLoRA (r=16, α=32, 4-bit NF4, LR 1e-4) sur Qwen2-VL-7B-Instruct est **pleinement opérationnel et stable** sur GPU 24 Go (Peak VRAM 10.8 GB, 0 OOM).
2. L'optimisation converge de manière fluide et reproductible sur les 775 assets d'entraînement réels sans instabilité numérique (norme de gradient < 0.12).
3. Le modèle transfère avec succès sur les 98 assets de validation inédits, avec une validation loss divisée par plus de 70 par rapport à l'état initial.
4. L'hypothèse pré-enregistrée est donc **confirmée sur son volet engineering et sur son volet d'optimisation contrôlée**.

---

## 16. Prochaines Expériences Possibles

1. **Ablation du Learning Rate (Campagne B2 sur données réelles) :** Évaluer $1.5 \times 10^{-4}$ et $2.0 \times 10^{-4}$ pour déterminer si la dynamique d'apprentissage peut être accélérée sans instabilité.
2. **Évaluation Scientifique sur le Gold Set V3 :** Soumettre les checkpoints `checkpoint-97` et `checkpoint-194` à l'évaluation formelle et aveugle sur le Gold Set V3 sanctuarisé.
3. **Augmentation de la résolution visuelle :** Tester l'intégration de plans vectoriels ou de résolutions 1024x1024 (`max_pixels: 1048576`) pour mesurer la sensibilité de la compréhension spatiale à la granularité des traits.
