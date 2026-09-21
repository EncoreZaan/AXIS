# Plan d'Expérience : Micro-Entraînement QLoRA Qwen2-VL-7B

## 1. Objectif
Valider la faisabilité technique complète, de bout en bout, du pipeline de fine-tuning QLoRA pour le modèle vision-langage **Qwen2-VL-7B-Instruct** sur le dataset d'architecture V2 (25 exemples corrigés et certifiés).

Cette étape a pour vocation unique de valider la mécanique d'apprentissage sans chercher immédiatement des métriques de pointe :
* Chargement du dataset multimodal et du collator personnalisé
* Quantification 4-bit NF4 et greffe de l'adaptateur LoRA
* Calcul de la forward pass, backward pass et descente de gradient
* Mise à jour des poids LoRA via l'optimiseur Paged AdamW 8-bit
* Boucle de validation périodique
* Sauvegarde et rechargement de l'adaptateur LoRA sans altération du modèle de base

---

## 2. Matériel Attendu
* **GPU Cible** : 1x NVIDIA GPU avec au moins **24 Go de VRAM** (ex. RTX 3090, RTX 4090, A10G, A5000, ou A100).
* **OS** : Linux (Ubuntu 22.04 LTS recommandé).
* **CUDA / Driver** : CUDA Toolkit >= 12.1 (recommandé 12.4), Driver NVIDIA >= 535.
* **CPU / RAM** : 4+ vCPU, >= 16 Go de mémoire vive système.
* **Stockage** : >= 30 Go d'espace disque disponible (modèle de base Hugging Face ~14 Go + checkpoints LoRA ~200 Mo).

---

## 3. Données
* **Dataset Train** : `dataset/train.jsonl` (20 exemples conversationnels validés, 0 doublon, 0 hallucination).
* **Dataset Validation** : `dataset/validation.jsonl` (5 exemples conversationnels distincts).
* **Images** : `dataset/images/` (25 images photographiques haute résolution).
* **Structure des Réponses** : Format structuré strict en 5 sections architecturales canoniques (`OBSERVATION`, `ANALYSE`, `POINTS FORTS`, `POINTS DE VIGILANCE`, `RECOMMANDATION`).
* **Masquage** : Seuls les tokens de réponse de l'assistant sont rétropropagés (labels à `-100` sur le prompt système/utilisateur et les tokens de patch visuel).

---

## 4. Configuration QLoRA
| Paramètre | Valeur retenue | Justification technique |
| :--- | :--- | :--- |
| **Modèle de base** | `Qwen/Qwen2-VL-7B-Instruct` | VLM état de l'art pour le raisonnement visuel spatial. |
| **Quantification** | 4-bit NF4 (`load_in_4bit=True`, `bnb_4bit_use_double_quant=True`) | Réduit l'empreinte mémoire du modèle de base à ~5.5 Go. |
| **Type de calcul** | `bfloat16` (`bnb_4bit_compute_dtype=bfloat16`) | Préserve la dynamique numérique sans sous-flux/sur-flux. |
| **LoRA Rank ($r$)** | `8` | Espace de rang suffisant pour un premier ancrage stylistique. |
| **LoRA Alpha ($\alpha$)** | `16` | Facteur d'échelle standard $\alpha / r = 2.0$. |
| **LoRA Dropout** | `0.05` | Régularisation légère pour éviter le surapprentissage. |
| **Target Modules** | `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` | Couvre l'ensemble des projections d'attention et MLP du LLM. |
| **Vision Tower** | Gelée (`freeze_vision_tower=True`) | Conserve l'extracteur visuel intact et minimise la VRAM. |
| **Résolution max** | 512×512 pixels (`max_pixels=262144`) | Plafonne à ~400-500 tokens de vision par image. |
| **Contexte max** | 1536 tokens | Couvre largement prompt, vision tokens et réponse structurée. |
| **Batch size / Accumulation** | 1 par GPU / 8 steps d'accumulation | Batch effectif = 8 séquences par mise à jour. |
| **Optimiseur** | `paged_adamw_8bit` | Gestion paginée de la mémoire des états d'optimiseur. |
| **Gradient Checkpointing** | Activé (`True`) | Réduit drastiquement l'empreinte mémoire d'activation. |
| **Learning Rate** | `1.0e-4` avec scheduler `cosine` et 5% de warmup | Convergence douce et stable. |

---

## 5. Nombre de Steps et Durée
* **Nombre d'exemples train** : 20
* **Taille de batch effectif** : 8 ($1 \times 8$)
* **Nombre d'époques** : 2
* **Steps d'optimisation prévus** :
  $$\text{Steps par époque} = \lceil 20 / 8 \rceil = 2.5 \rightarrow \approx 2.5 \text{ steps}$$
  Sur 2 époques : **5 steps d'optimisation au total** (avec logging à chaque step).
* **Durée estimée** : 2 à 4 minutes sur GPU 24 Go (hors téléchargement initial des poids Hugging Face).

---

## 6. Critères de Réussite
1. **Validation de l'environnement** : `python check_environment.py` renvoie `STATUS : READY FOR TRAINING`.
2. **Garde-fou actif** : Le script ne démarre que si `--train` est explicitement fourni.
3. **Passe d'entraînement complète** : Les 5 steps s'exécutent sans erreur CUDA OOM (Out Of Memory).
4. **Calcul de la perte (Loss)** : La courbe de loss décroît ou reste stable et finie (pas de `NaN` ni d'`Inf`).
5. **Phase de validation** : L'évaluation sur les 5 exemples produit une `eval_loss` calculée.
6. **Sauvegarde des artefacts** : L'ensemble des fichiers checkpoints est généré dans `outputs/archi_ai_micro_experiment/`.
7. **Rechargement LoRA** : Le script recharge l'adaptateur sauvegardé avec succès via `PeftModel.from_pretrained`.

---

## 7. Critères d'Échec
* Erreur d'allocation mémoire CUDA OOM lors du backward pass ou du step d'optimisation.
* Perte divergente (`NaN` ou `Inf`) dès les premiers steps.
* Erreur d'indexation dans les masques M-RoPE ou de dimensions lors du collating multimodal.
* Incompatibilité de compilation de `bitsandbytes` sur la plateforme distante.
* Échec de sauvegarde ou corruption des poids de l'adaptateur LoRA.

---

## 8. Artefacts Produits
Dossier de sortie : `outputs/archi_ai_micro_experiment/`
1. `adapter_model.safetensors` : Poids entraînés des matrices LoRA $A$ et $B$ (~50-100 Mo).
2. `adapter_config.json` : Métadonnées et hyperparamètres PEFT LoRA.
3. `preprocessor_config.json` & fichiers tokenizer : Configuration de preprocessing multimodal.
4. `experiment_config.yaml` : Copie de la configuration exacte ayant servi à l'exécution.
5. `train_results.json` : Métriques finales d'entraînement (loss finale, runtime, samples_per_second).
6. `eval_results.json` : Métriques finales d'évaluation sur le split validation.
7. `trainer_state.json` : Journal pas-à-pas de l'historique d'optimisation.

---

## 9. Étape Suivante
Une fois ce premier micro-test validé :
1. **Évaluation comparative** : Exécuter le script d'inférence avec l'adaptateur entraîné sur le jeu de validation pour comparer avec la baseline brute sauvegardée (`BASELINE.md`).
2. **Analyse des gradients et de la loss** : Vérifier que l'alignement sur le template en 5 parties commence à s'ancrer sans surapprentissage.
3. **Passage à l'échelle (Scale-up)** : Si les résultats sont cohérents, planifier l'expansion du dataset (100 à 250 exemples) et l'entraînement sur 3 à 5 époques complètes.
