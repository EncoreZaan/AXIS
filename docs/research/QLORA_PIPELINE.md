# Pipeline QLoRA — Qwen2-VL-7B-Instruct & ARCHI-AI

Date : 21 Septembre 2026  
Projet : **ARCHI-AI**  
Modèle de référence : `Qwen/Qwen2-VL-7B-Instruct`  
Méthode : **QLoRA 4-bit (NF4)**  
Statut : **Validé en Dry-Run (sans entraînement effectif)**  

---

## 1. Architecture du Pipeline

Le pipeline d'entraînement est conçu pour adapter les capacités de raisonnement spatial et d'expertise architecturale du modèle multimodal `Qwen2-VL-7B-Instruct` tout en préservant son intégrité visuelle et en minimisant l'empreinte VRAM.

```
[ Dataset JSONL ] (train: 20, val: 5)
       │
       ▼
[ Preprocessing Multimodal ]
   ├── Image Loader & Checker (512x512 max)
   ├── Chat Template Formatting (<|im_start|> ... <|im_end|>)
   └── Process Vision Info (qwen-vl-utils)
       │
       ▼
[ Custom VisionLanguage Collator ]
   ├── Token Padding (Right pad avec <|endoftext|>)
   ├── Label Masking (-100 sur Prompt utilisateur & Vision)
   ├── Vision Tensors Cat (pixel_values & image_grid_thw)
   └── M-RoPE Multimodal Token Type IDs (mm_token_type_ids)
       │
       ▼
[ Modèle Qwen2-VL 4-bit NF4 + PEFT LoRA ]
   ├── Tour Visuelle gelée (model.model.visual.requires_grad = False)
   ├── Projections LLM adaptées (q, k, v, o, gate, up, down)
   └── Gradient Checkpointing activé
       │
       ▼
[ Hugging Face Trainer ] (24 Go GPU Cible)
   ├── Optimizer : Paged AdamW 8-bit
   ├── Batch Size : 1 par device
   ├── Gradient Accumulation : 8 (Batch effectif = 8)
   └── Scheduler : Cosine avec warmup 5%
```

---

## 2. Format Attendu des Données

Le dataset expérimental est situé dans `ARCHI_AI/dataset/` (`train.jsonl` et `validation.jsonl`).

### Structure d'une entrée JSONL :
```json
{
  "id": "archi_001",
  "category": "ANALYSE D'ESPACE",
  "space_type": "salon",
  "style": "contemporain",
  "image": "images/archi_001.jpg",
  "context": "Pièce de vie principale d'une maison contemporaine...",
  "question": "En tant qu'architecte d'intérieur, réalisez une analyse spatiale...",
  "answer": "OBSERVATION\n...\n\nANALYSE\n...\n\nPOINTS FORTS\n...\n\nPOINTS DE VIGILANCE\n...\n\nRECOMMANDATION\n...",
  "conversations": [
    {
      "role": "user",
      "content": [
        {"type": "image", "image": "images/archi_001.jpg"},
        {"type": "text", "text": "Contexte : ...\n\nQuestion : ..."}
      ]
    },
    {
      "role": "assistant",
      "content": [
        {"type": "text", "text": "OBSERVATION\n...\n\nANALYSE\n..."}
      ]
    }
  ]
}
```

### Règles de gestion du format :
1. **Chemins d'images** : Le champ `"image"` dans `content` contient un chemin relatif (`images/archi_001.jpg`). La classe `ARCHIVisionDataset` résout automatiquement ce chemin vers `ARCHI_AI/dataset/images/archi_001.jpg`.
2. **Masquage des labels (Prompt Masking)** : Les tokens du prompt utilisateur, des patches visuels et des en-têtes système sont masqués avec l'indice `-100` (valeur `ignore_index` de PyTorch CrossEntropyLoss). Seuls les tokens de la réponse structurée de l'architecte contribuent au calcul de la loss.

---

## 3. Processeur et Collator Multimodal

* **Processeur** : `AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")`
* **Contraintes de résolution** :
  * `min_pixels` : `200 704` ($256 \times 28 \times 28$)
  * `max_pixels` : `262 144` ($512 \times 512$) — permet de plafonner le nombre de patches visuels à ~400–500 tokens par image, réduisant drastiquement les besoins mémoires d'activation.
* **Collator personnalisé (`VisionLanguageDataCollator`)** :
  * Aligne dynamiquement la longueur des séquences avec padding à droite.
  * Concatène les tenseurs 2D des patches visuels (`pixel_values`) sur la dimension 0.
  * Transmet la grille 3D des patches temporels/hauteur/largeur (`image_grid_thw`).
  * **Point critique** : Fournit `mm_token_type_ids` pour que l'attention M-RoPE (Multimodal Rotary Position Embedding) 3D puisse indexer correctement les coordonnées spatiales des patches visuels.

---

## 4. Choix du Trainer : Hugging Face Trainer vs TRL

Pour notre cas, **Hugging Face `Trainer`** natif a été retenu au détriment de TRL `SFTTrainer`.

### Raisons du choix :
1. **Stabilité multimodale** : `TRL SFTTrainer` a connu de multiples changements d'API sur les modèles VLM récents et gère mal l'injection de tenseurs hétérogènes (`pixel_values` 2D aplati + `image_grid_thw` + `mm_token_type_ids`).
2. **Simplicité et robustesse** : Le `Trainer` natif de Transformers gère nativement le gradient checkpointing, `BitsAndBytesConfig`, l'optimiseur `paged_adamw_8bit`, et s'interface directement avec `peft`.
3. **Contrôle total du masquage** : Le calcul exact des labels `-100` est transparent dans notre classe `ARCHIVisionDataset`, garantissant que le modèle n'apprend pas à prédire les images ni les questions utilisateur.

---

## 5. Configuration LoRA

* **Modèle de base** : `Qwen/Qwen2-VL-7B-Instruct`
* **Quantification** : 4-bit NormalFloat (`nf4`), double quantification, compute dtype `torch.bfloat16`.
* **Rang LoRA ($r$)** : 8
* **Facteur d'échelle ($\alpha$)** : 16 (ratio $\alpha/r = 2.0$)
* **Dropout LoRA** : 0.05
* **Modules ciblés** :
  * `q_proj`, `k_proj`, `v_proj`, `o_proj` (Attention LLM)
  * `gate_proj`, `up_proj`, `down_proj` (MLP LLM)
* **Tour de Vision** : `model.model.visual.requires_grad = False` (totalement gelée).
* **Bilan des paramètres** :
  * **Paramètres entraînables** : `20 185 088` (20.19 M)
  * **Paramètres totaux** : `8 311 560 704` (8.31 B)
  * **Ratio de paramètres entraînables** : **0.2429 %**

---

## 6. Paramètres d'Entraînement et Mémoire

Centralisés dans `ARCHI_AI/config/qlora_experiment.yaml` :

| Paramètre | Valeur | Justification |
| :--- | :--- | :--- |
| **GPU Cible** | 24 Go VRAM (Cloud / RunPod) | Permet un entraînement fluide sans OOM lors du backward |
| **Batch Size (par device)** | 1 | Réduit le pic d'activation par step |
| **Gradient Accumulation** | 8 | Batch effectif de 8 exemples pour stabiliser le gradient |
| **Learning Rate** | 1e-4 | Taux standard éprouvé pour LoRA sur LLM 7B |
| **Scheduler** | Cosine avec 5% Warmup | Décroissance progressive sans choc d'optimisation |
| **Optimiseur** | `paged_adamw_8bit` | Pagination CPU en cas de pic mémoire |
| **Précision** | `bfloat16` natif | Stabilité numérique sans risque de sous-flux FP16 |
| **Gradient Checkpointing** | Activé (`True`) | Réduit de > 50% la mémoire d'activation au détriment de ~20% de calcul |
| **Contexte maximal** | 1 536 tokens | Couvre largement prompt + 512px image + réponse structurée |

---

## 7. Problèmes Rencontrés & Corrections Apportées

Lors des tests de validation et du dry-run, deux particularités techniques majeures ont été identifiées et corrigées :

### Problème 1 : Hiérarchie de la Tour de Vision dans Transformers
* **Symptôme** : Tentative d'accès à `model.visual` provoquant un `AttributeError: 'Qwen2VLForConditionalGeneration' object has no attribute 'visual'`.
* **Cause** : Dans l'implémentation Hugging Face de Qwen2-VL, la tour visuelle est instanciée sous `model.model.visual`, tandis que le LLM est sous `model.model.language_model`.
* **Correction** : Le gel explicite cible `model.model.visual.requires_grad_(False)`. De plus, la liste des `target_modules` (`q_proj`, `k_proj`, etc.) ne matche que les couches de `language_model`, garantissant que la tour de vision reste vierge de tout adaptateur.

### Problème 2 : Obligation de `mm_token_type_ids` pour M-RoPE
* **Symptôme** : Erreur `ValueError: Multimodal data was passed (via image_grid_thw) but mm_token_type_ids is missing.` lors du premier forward pass.
* **Cause** : Qwen2-VL utilise des plongements rotatifs multidimensionnels (M-RoPE) pour encoder simultanément la position temporelle, verticale et horizontale des patches d'image. `transformers 5.x` exige que le tenseur `mm_token_type_ids` (généré par le processeur) soit passé explicitement au modèle pour distinguer les tokens de texte des tokens d'image.
* **Correction** : Le `ARCHIVisionDataset` extrait désormais `mm_token_type_ids` et le `VisionLanguageDataCollator` l'aligne et le transmet directement dans le batch de forward.

---

## 8. Résultats du Dry-Run

Le dry-run exécuté avec la commande :
```bash
python ARCHI_AI/train_qlora.py --dry-run
```
a produit les résultats suivants :

* **Poids chargés** : 730/730 tenseurs en 4-bit NF4.
* **Paramètres LoRA greffés** : 20.19 M paramètres (0.24%).
* **Batch de test** : 2 exemples assemblés dynamiquement (input_ids `[2, 877]`, pixel_values `[2492, 1176]`).
* **Masquage des labels** : 410 tokens masqués (-100), 467 tokens actifs sur la réponse.
* **Passe avant (Forward Pass)** : Exécutée avec succès sur GPU CUDA.
* **Loss calculée** : **1.9771**
* **Logits obtenus** : Tenseur de forme `[1, 877, 152064]`.
* **Garantie de non-entraînement** :
  * Aucun backward pass exécuté.
  * Aucune mise à jour d'optimiseur.
  * Aucune modification des poids du modèle ni de l'environnement.
