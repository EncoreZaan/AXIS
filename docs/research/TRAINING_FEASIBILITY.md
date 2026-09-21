# Étude de Faisabilité du Fine-Tuning — Qwen2-VL-7B-Instruct

Date : 21 Septembre 2026  
Projet : **ARCHI-AI**  
Modèle de référence : `Qwen/Qwen2-VL-7B-Instruct`  
Méthode visée : **LoRA / QLoRA** (gel du modèle de base, adaptation par adaptateurs de bas rang)  
Règle stricte : **Aucun entraînement complet (Full Fine-Tuning) envisagé**.

---

## 1. Hardware Actuel

Le matériel physique disponible localement a été rigoureusement audité lors de l'étape de baseline (`ARCHI_AI/BASELINE.md`) :

* **GPU** : NVIDIA GeForce RTX 4060 Ti (8 188 Mo / ~8.00 Go GDDR6, architecture Ada Lovelace, Compute Capability 8.9).
* **VRAM disponible hors charge** : ~6.90 Go libre (~1.12 Go à 1.20 Go réservés en permanence par Windows 11 et Desktop Window Manager - DWM).
* **CPU** : Intel Core i5-14400F (10 cœurs, 16 threads).
* **RAM Système** : 16 Go DDR (dont ~5.2 Go libres au repos sous Windows).
* **Stockage** : SSD NVMe (> 600 Go libres).
* **Mesure empirique en inférence 4-bit (NF4)** :
  * Modèle chargé au repos : **5.53 Go VRAM allouée** (6.79 Go VRAM totale système).
  * Pic d'inférence (batch 1, 1 064 tokens d'entrée, 145 tokens générés) : **5.99 Go VRAM allouée** (**7.54 Go VRAM totale système**).
  * **Marge VRAM résiduelle en inférence** : **467 Mo seulement**.

---

## 2. Analyse Scénario par Scénario

### SCÉNARIO A — RTX 4060 Ti 8 Go (Local)

* **Approche testée** : QLoRA 4-bit (bitsandbytes NF4).
* **Décomposition mathématique et mémoire de l'entraînement** :
  1. **Poids du modèle de base (4-bit NF4)** : ~5.0 à 5.5 Go alloués.
  2. **Paramètres LoRA (trainables en FP32/BF16)** : pour $r=16$ sur toutes les couches linéaires de projection du LLM, environ 20M à 40M paramètres $\rightarrow$ ~40 à 80 Mo.
  3. **Gradients** : calculés uniquement sur les adaptateurs LoRA $\rightarrow$ ~40 à 80 Mo.
  4. **Optimiseur (Paged AdamW 8-bit)** : états de momentum/variance quantifiés $\rightarrow$ ~80 à 160 Mo.
  5. **Tenseurs d'activation (avec Gradient Checkpointing)** :
     * Lors de la passe avant/arrière, les activations des couches du LLM (28 couches, hidden size 3584, intermediate size 18944) et la couche finale de vocabulaire (logits de taille `[batch, seq_len, 152064]`) doivent être allouées en FP32/BF16.
     * Pour une séquence de 1 024 tokens (image + prompt), la couche de sortie logits consomme à elle seule :  
       $1024 \times 152\,064 \times 4\text{ octets} \approx 623\text{ Mo}$.
     * L'espace mémoire d'activation minimal incompressible avec gradient checkpointing pour un VLM 7B à 1 024 tokens est d'environ **2.2 à 3.0 Go**.
  6. **Empreinte VRAM PyTorch totale requise** :  
     $5.5\text{ Go} \text{ (base)} + 0.3\text{ Go} \text{ (LoRA+opt)} + 2.5\text{ Go} \text{ (activations/workspace)} \approx \mathbf{8.3\text{ Go}}$.
  7. **Empreinte VRAM système requise sous Windows** :  
     $8.3\text{ Go} + 1.2\text{ Go (DWM/Windows)} \approx \mathbf{9.5\text{ Go}}$.
* **CPU Offload possible ?** :
  * Bitsandbytes permet d'offloader l'optimiseur vers la RAM système (`paged_adamw_8bit`). Cependant, cela n'économise que ~100 Mo de VRAM.
  * Offloader des couches du modèle de base vers la RAM CPU (via Accelerate/DeepSpeed ZeRO-Offload) détruit la bande passante (transferts PCIe x8 Gen4 continus) : le temps de step passerait de ~1 seconde à plus de 45 secondes par exemple, rendant l'entraînement impraticable.
  * La RAM système n'étant que de 16 Go (dont 5.2 Go libres), un CPU offload important saturerait immédiatement la RAM et déclencherait le fichier d'échange (swap disque).
* **Vitesse estimée** : < 0.1 step/s en offload partiel, ou freeze complet.
* **Stabilité** : Instable / Crash systématique par `CUDA Out of Memory` lors de la passe backward ou du calcul de la loss de vocabulaire.
* **Verdict** : **IRRÉALISTE** pour un entraînement exploitable. Même en dégradant la résolution d'image à un niveau microscopique (384x384, inadapté à l'architecture d'intérieur), la carte flirterait avec les 8.0 Go au risque de planter à la première variation de longueur de texte.

---

### SCÉNARIO B — GPU Distant 16 Go (ex. T4, V100 16G, RTX 4080 16G, L4 24G partitionné)

* **Environnement cible** : Instance Linux Cloud (consommation système GPU < 200 Mo, contre 1.2 Go sous Windows).
* **Faisabilité QLoRA 4-bit** : **RÉALISTE ET CONFORTABLE**.
  * Modèle de base 4-bit : ~5.0 Go.
  * LoRA + gradients + Paged AdamW 8-bit : ~0.3 Go.
  * Activations avec Gradient Checkpointing (longueur contexte 1 500 à 2 048 tokens, résolution 768x768) : ~3.0 à 4.0 Go.
  * Pic mémoire total : **~8.5 à 9.5 Go**.
  * Marge de sécurité sur 16 Go : **> 6.5 Go libres**.
* **Faisabilité LoRA 16-bit (BF16, modèle non quantifié)** : **IRRÉALISTE / OOM**.
  * Poids du modèle 7B en BF16 : ~14.5 Go.
  * Espace restant pour activations, LoRA et buffers : 16 - 14.5 = 1.5 Go (insuffisant pour la passe backward).
* **Vitesse estimée (QLoRA)** : ~1.0 à 1.8 step/s (selon GPU, ex. RTX 4080 ou L4).
* **Verdict** : **PARFAITEMENT RÉALISTE EN QLoRA 4-bit**, mais impossible en LoRA BF16 non quantifié.

---

### SCÉNARIO C — GPU Distant 24 Go (ex. RTX 3090, RTX 4090, A10G 24G)

* **Environnement cible** : Instance Linux Cloud (RunPod, Vast.ai, Lambda Labs, GCP).
* **Faisabilité QLoRA 4-bit** : **OPTIMALE ET TRÈS RAPIDE**.
  * Empreinte VRAM : ~9 à 11 Go.
  * Permet un batch size par device de 2, ou un contexte étendu (3 000+ tokens), avec Flash Attention 2 activé.
* **Faisabilité LoRA 16-bit (BF16 / FP16)** : **RÉALISTE**.
  * Poids de base en BF16 natif (sans quantification) : ~14.5 Go.
  * LoRA ($r=16$) + Gradients : ~0.15 Go.
  * Optimiseur (AdamW 8-bit) : ~0.15 Go.
  * Activations avec Gradient Checkpointing (contexte 1 500 tokens) : ~3.5 à 4.5 Go.
  * Pic mémoire total : **~18.5 à 20.0 Go sur 24 Go**.
  * Marge de sécurité : **~4 Go libres**.
  * *Avantage majeur du 16-bit LoRA* : Aucun bruit de déquantification pendant la passe backward, convergence plus propre et plus rapide qu'en 4-bit.
* **Vitesse estimée** :
  * RTX 4090 (Ada) : ~2.5 à 3.5 steps/s avec Flash Attention 2.
  * RTX 3090 (Ampere) : ~1.5 à 2.2 steps/s.
* **Coût indicatif** : ~$0.30 à $0.60 / heure sur les plateformes cloud communautaires.
* **Verdict** : **LE MEILLEUR COMPROMIS TECHNIQUE ET ÉCONOMIQUE**. Supporte à la fois QLoRA et LoRA 16-bit sans aucune restriction pénalisante.

---

### SCÉNARIO D — GPU Distant 48 Go+ (ex. A40 48G, A100 40G/80G, H100 80G)

* **Apport réel pour Qwen2-VL-7B avec LoRA/QLoRA** : **TRÈS FAIBLE / INUTILEMENT COÛTEUX**.
* **Analyse technique** :
  * Comme nous gelons le modèle de base et n'entraînons que des couches LoRA, l'empreinte mémoire maximale en 16-bit plafonne à ~20 Go.
  * Disposer de 48 Go ou 80 Go ne débloque aucune capacité qualitative supplémentaire pour un adaptateur LoRA 7B : la résolution utile d'une image d'intérieur n'a pas besoin de dépasser 1024x768 pour capturer les matériaux et agencements.
  * Les seuls cas d'usage justifiant 48 Go+ seraient :
    1. Un Full Fine-Tuning de tous les 7.6 milliards de paramètres (poids + gradients + AdamW FP32 = ~85 Go VRAM), ce que nous avons explicitement écarté.
    2. Un entraînement massif multi-images (10 images haute résolution simultanées par prompt, contextes > 16k tokens).
    3. Un entraînement à très grand batch size distribué sur des millions d'exemples.
* **Coût indicatif** : $1.80 à $4.50 / heure (3x à 8x plus cher qu'une RTX 4090 pour un résultat identique sur notre échelle).
* **Verdict** : **INUTILEMENT COÛTEUX** et disproportionné pour notre projet.

---

## 3. Matrice Comparative Synthétique

| Critère | Scénario A (4060 Ti 8 Go) | Scénario B (GPU 16 Go) | Scénario C (GPU 24 Go) | Scénario D (GPU 48 Go+) |
| :--- | :--- | :--- | :--- | :--- |
| **Type d'entraînement** | QLoRA 4-bit | QLoRA 4-bit uniquement | QLoRA 4-bit ET LoRA 16-bit | QLoRA, LoRA 16-bit, Full FT |
| **Mémoire VRAM requise** | ~9.5 Go (avec OS) | ~9.0 Go | ~10 Go (QLoRA) / ~20 Go (LoRA) | ~10 à 22 Go (LoRA) |
| **Risque d'OOM** | **Quasi-certain (100%)** | Faible | Nul si bien configuré | Nul |
| **Résolution d'image max** | Très dégradée (< 384x384) | Moyenne (768x768) | Élevée (1024x768 à 1024x1024) | Maximale (> 1024x1024) |
| **Contexte max supporté** | < 512 tokens | ~2 048 tokens | 2 048 à 4 096 tokens | > 8 192 tokens |
| **Vitesse (steps/sec)** | < 0.1 (si offload) | ~1.2 - 1.8 st/s | ~2.5 - 3.5 st/s (sur 4090) | ~3.5 - 5.0 st/s |
| **Coût estimé** | 0 € (matériel local) | ~$0.20 - $0.35 / h | ~$0.35 - $0.55 / h | ~$2.00 - $4.00 / h |
| **Statut de faisabilité** | **IRRÉALISTE** | **RÉALISTE (QLoRA)** | **RECOMMANDÉ (Sweet Spot)** | **SURDIMENSIONNÉ** |

---

## 4. Réponses Précises aux 12 Questions Techniques

### 1. Quelle résolution d'image serait raisonnable pour notre première expérimentation ?
* **Réponse** : **Entre 512x512 et 768x768 pixels** (ou capping via `max_pixels = 768 * 768 = 589 824`).
* *Justification Qwen2-VL* : Qwen2-VL découpe les images en patchs 2D RoPE de 28x28 pixels.
  * $512 \times 512 \rightarrow \sim 334$ tokens visuels.
  * $768 \times 768 \rightarrow \sim 750$ tokens visuels.
  * $1024 \times 768 \rightarrow \sim 1\,000$ tokens visuels.
  Pour un premier test de pipeline, 512x512 à 768x768 préserve les textures architecturales majeures tout en limitant la taille de la séquence d'entrée pour un temps de calcul ultra-rapide.

### 2. Quelle longueur de contexte ?
* **Réponse** : **1 536 à 2 048 tokens** (`max_seq_length = 2048`).
* *Décomposition* :
  * Tokens visuels : ~750 tokens.
  * Prompt système + question utilisateur : ~100 à 150 tokens.
  * Réponse experte cible (description architecturale détaillée) : ~250 à 450 tokens.
  * Marge de sécurité : ~200 tokens.

### 3. Quel batch size ?
* **Réponse** : **Batch size par GPU = 1**, combiné avec **Gradient Accumulation = 8 à 16**.
* *Batch size effectif* : **8 à 16**.
* *Pourquoi batch size 1 ?* : Les images n'ont pas toutes le même ratio d'aspect. Avec un batch size de 1, on évite le padding inutile de patchs visuels et on minimise les pics d'activation VRAM.

### 4. Combien de paramètres LoRA ?
* **Réponse** : Environ **20 millions à 35 millions de paramètres**, soit **~0.3% à 0.45%** des 7.6 milliards de paramètres totaux du modèle.

### 5. Quel rang LoRA ($r$) serait raisonnable ?
* **Réponse** : **$r = 16$ avec $\alpha = 32$** (ratio classique $\alpha / r = 2$).
* *Alternative de démarrage* : $r = 8, \alpha = 16$ pour une expérimentation initiale encore plus économe.
* *Modules cibles (`target_modules`)* : Appliquer LoRA sur les projections linéaires du LLM :  
  `["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]`.
* *Règle critique* : **Geler complètement la tour visuelle (Vision Tower / ViT)** pour notre phase. Adapter uniquement le modèle de langage aux concepts architecturaux.

### 6. Quel learning rate de départ ?
* **Réponse** :
  * En **QLoRA 4-bit** : **$1\times 10^{-4}$ à $2\times 10^{-4}$** ($1\text{e}-4$).
  * En **LoRA 16-bit** : **$5\times 10^{-5}$ à $1\times 10^{-4}$** ($5\text{e}-5$).
* *Scheduler* : `cosine` avec un warm-up sur les premiers 3% à 5% des steps, puis décroissance progressive.

### 7. Gradient checkpointing : nécessaire ou non ?
* **Réponse** : **ABSOLUMENT NÉCESSAIRE (OBLIGATOIRE)**.
* *Raison* : Sans gradient checkpointing, les tenseurs d'activation intermédiaires des 28 couches d'attention pour des séquences de 1 500+ tokens dépasseraient 16 Go à eux seuls. Le gradient checkpointing recalcule les activations pendant la passe backward plutôt que de les stocker, au prix d'un surcoût en temps de calcul modéré (~20-25%), mais divisant l'empreinte mémoire d'activation par 4.

### 8. Flash Attention : utile ou nécessaire ?
* **Réponse** : **TRÈS FORTEMENT RECOMMANDÉ** (nécessaire pour un débit acceptable).
* *Détails d'implémentation* :
  * Sous Linux avec GPU Ampere/Ada/Hopper (ex. RTX 3090/4090, A10G) : `flash-attn` (FlashAttention-2) réduit la complexité mémoire de l'attention de quadratique à linéaire et accélère l'entraînement d'un facteur 2x à 2.5x.
  * Sous Windows : FlashAttention-2 est notoirement difficile à compiler ; on doit alors se rabattre sur PyTorch SDPA (`torch.nn.functional.scaled_dot_product_attention`), qui est moins optimisé pour les séquences variables de Qwen2-VL. C'est une raison supplémentaire de privilégier un GPU distant sous Linux pour la phase d'entraînement.

### 9. Quel format de dataset utiliser ?
* **Réponse** : Format standard multi-tours **ShareGPT / LLaMA-Factory / SFT Hugging Face** au format JSON ou JSONL.
* *Structure type* :
  ```json
  [
    {
      "id": "archi_sample_001",
      "images": ["images/salon_haussmannien_01.jpg"],
      "conversations": [
        {
          "from": "human",
          "value": "<image>\nDécris cette pièce en tant qu'architecte d'intérieur : précise le type d'espace, le style dominant, les matériaux identifiables et l'ambiance lumineuse."
        },
        {
          "from": "gpt",
          "value": "Il s'agit d'un salon de réception de style néo-haussmannien. Les caractéristiques dominantes incluent des moulures d'époque, un parquet en point de Hongrie en chêne massif vitrifié mat..."
        }
      ]
    }
  ]
  ```

### 10. Combien d'exemples faudrait-il pour une première expérimentation significative ?
* **Réponse** : **150 à 300 exemples d'excellente qualité**.
* *Principe fondamental* : En LoRA spécialisé (alignement de domaine et de vocabulaire), la qualité et la rigueur de l'annotation priment sur le volume. 200 exemples rédigés ou validés avec un vocabulaire d'architecte d'intérieur strict produisent une métamorphose stylistique bien plus nette que 5 000 descriptions génériques bruitées du web.

### 11. Quelle taille de dataset permettrait de tester rapidement sans dépenser beaucoup d'argent ?
* **Réponse** : **20 à 50 exemples (Smoke Test de pipeline / Test de surapprentissage)**.
* *Objectif* :
  * Vérifier que le script de chargement des images et de tokenisation fonctionne.
  * Valider que la loss d'entraînement décroît continuellement (de ~2.5 à < 0.6 sur 3 à 5 époques).
  * Vérifier la sauvegarde des poids LoRA et leur rechargement en inférence.
* *Durée & Coût* : Moins de 10 minutes sur une RTX 4090 distante, soit **moins de 0,10 $**.

### 12. Comment mesurer si le fine-tuning améliore réellement le modèle ?
* **Réponse** : Protocole d'évaluation en 3 volets complémentaires :
  1. **Décroissance de la Loss sur un jeu de test (Validation Loss)** :
     * Isoler strictement 20% des exemples dans un split de validation (`eval_loss`). L'amélioration de la perplexité valide que le modèle apprend la distribution linguistique cible sans sur-apprendre bêtement.
  2. **Audit comparatif côte à côte (A/B Testing en aveugle)** :
     * Sur 15 images de test inédites, générer en parallèle la réponse du **Baseline (Qwen2-VL-7B natif 4-bit)** et celle du **Modèle Fine-tuné (LoRA)**.
     * Soumettre les deux réponses anonymisées à une grille d'évaluation architecturale :
       * *Richesse du vocabulaire technique* (ex. : distinction chêne massif vs stratifié, éclairage direct vs indirect).
       * *Structure et méthodologie* (suivi rigoureux des rubriques demandées).
       * *Précision spatiale*.
  3. **Taux d'hallucination de matériaux** :
     * Vérifier que le modèle fine-tuné n'invente pas d'éléments invisibles sur l'image pour "faire style architecte" (contrôle de fidélité visuelle).

---

## 5. Configuration QLoRA Recommandée (Production / Entraînement Final)

* **Plateforme** : GPU distant 24 Go (ex. RTX 4090 ou A10G sous Linux).
* **Mode** : LoRA 16-bit natif (BF16) ou QLoRA 4-bit (si l'on veut maximiser le débit et la taille de batch).
* **Target modules** : Toutes les projections linéaires du langage (`q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj`).
* **Gel strict** : Vision Tower (`visual`) gelée.
* **LoRA $r$** : 16.
* **LoRA $\alpha$** : 32.
* **LoRA Dropout** : 0.05.
* **Optimiseur** : `paged_adamw_8bit`.
* **Learning Rate** : $1\times 10^{-4}$ avec Cosine Decay.
* **Gradient Checkpointing** : Activé.
* **Flash Attention** : `flash_attention_2`.
* **Batch size per device** : 1.
* **Gradient accumulation steps** : 16.
* **Époques** : 3 à 5 époques sur 200 à 300 exemples.

---

## 6. Configuration Expérimentale Minimale (Premier Test de Pipeline)

* **Objectif** : Valider la chaîne complète sans risque financier ni perte de temps.
* **GPU** : 1x GPU distant 24 Go (RTX 4090 ou RTX 3090) ou 16 Go (RTX 4080 / L4).
* **Taille du dataset test** : 20 à 30 paires image/texte.
* **Résolution image** : $512 \times 512$ (`max_pixels = 512 * 512`).
* **Contexte max** : 1 536 tokens.
* **Batch size** : 1 (accumulation = 8).
* **LoRA** : $r = 8, \alpha = 16$.
* **Nombre de steps** : 30 à 50 steps (environ 3 époques).
* **Temps estimé** : 5 à 8 minutes.

---

## 7. Cartographie des Risques d'OOM (Out-Of-Memory)

1. **Le piège de la résolution d'image sans capping** :
   * Une photo de smartphone moderne (4032x3024) sans paramètre `max_pixels` génère plus de 15 000 tokens visuels dans Qwen2-VL.
   * *Conséquence* : OOM immédiat au premier forward pass, même sur un A100 80 Go.
   * *Parade* : Définir impérativement `max_pixels = 768 * 768` (ou `1024 * 768`) dans le processeur.
2. **Le piège de la couche de logits du vocabulaire** :
   * Qwen2 dispose d'un très grand vocabulaire (152 064 tokens).
   * Calculer la cross-entropy sur l'ensemble de la séquence sans gradient checkpointing ou sans chunking de loss fait exploser la VRAM de plusieurs gigaoctets à la dernière couche.
3. **Le piège du dégel de la Vision Tower** :
   * Si les adaptateurs LoRA sont appliqués par erreur sur les modules d'attention du Vision Transformer (`visual.*`), la mémoire requise pour les activations 2D de convolution et de window attention double instantanément.
4. **L'illusion du 8 Go local sous Windows** :
   * Croire que les 8 Go de la 4060 Ti suffiront parce que l'inférence passe à 7.54 Go. L'inférence ne stocke aucun gradient ni état d'optimiseur, et ne recalcule aucune activation. Le moindre backward pass sous Windows fera crasher le pilote graphique ou déclenchera un gel complet du système.

---

## 8. Méthode d'Évaluation de la Progression

Pour certifier objectivement que le modèle fine-tuné surpasse le baseline :

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DATASET D'ÉVALUATION                           │
│             (20 à 30 images de test jamais vues en train)              │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
┌───────────────────────────────┐           ┌────────────────────────────────┐
│      BASELINE ACTUEL          │           │       MODÈLE FINE-TUNÉ         │
│  (Qwen2-VL-7B-Instruct 4-bit) │           │    (LoRA Spécialisé Archi)     │
└──────────────┬────────────────┘           └────────────────┬───────────────┘
               │                                             │
               └───────────────────────┬─────────────────────┘
                                       ▼
                    ┌──────────────────────────────────────┐
                    │      ÉVALUATION COMPARATIVE A/B      │
                    │   - Respect de la grille métier      │
                    │   - Précision des matériaux identifiés│
                    │   - Détection d'hallucinations       │
                    │   - Richesse du vocabulaire archi    │
                    └──────────────────────────────────────┘
```

---

## 9. Recommandation Finale

1. **Entraînement Local sur RTX 4060 Ti 8 Go** : **À PROSCRIRE**.
   * Le GPU local est excellent pour le développement, le prototypage des scripts de préparation de données, le packaging des formats et l'inférence de validation en 4-bit.
   * Mais lancer le fine-tuning sur cette machine sous Windows conduira inévitablement à des erreurs OOM bloquantes et à une perte de temps considérable.
2. **Stratégie Recommandée : Approche Hybride Découplée** :
   * **Local (RTX 4060 Ti)** : Conception, inspection et validation du format du dataset, écriture des scripts de test d'inférence et évaluation des checkpoints.
   * **Distant à la demande (GPU 24 Go type RTX 4090)** : Exécution de l'entraînement via une instance ponctuelle (Linux). Un entraînement complet de 300 exemples prendra moins de 45 minutes pour un coût inférieur à 0,50 €.
   * **Retour en Local** : Rapatriement de l'adaptateur LoRA final (~100 Mo), fusion ou injection dans l'environnement local pour l'inférence quotidienne.
