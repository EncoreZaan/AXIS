# ARCHI-AI - Rapport de Baseline & Première Inférence Multimodale

Date : 21 Septembre 2026  
Projet : **ARCHI-AI** (Assistant multimodal spécialisé en architecture d'intérieur)  
Objectif : Valider le fonctionnement de l'inférence multimodale (Vision-Language) sur la machine cible sans fine-tuning.

---

## 1. Configuration Matérielle

| Composant | Spécification | Détails / Mesures |
| :--- | :--- | :--- |
| **GPU** | **NVIDIA GeForce RTX 4060 Ti** | 8 188 MiB GDDR6 (~8.00 Go VRAM), Architecture Ada Lovelace (Compute Capability 8.9) |
| **VRAM disponible initiale** | ~7.0 Go | ~1.2 Go occupés par les processus système de bureau Windows |
| **Processeur (CPU)** | Intel(R) Core(TM) i5-14400F | 10 cœurs physiques (16 threads) |
| **Mémoire Vive (RAM)** | 16 Go | ~5.2 Go libres lors du lancement |
| **Stockage** | SSD NVMe (Lecteur C:) | > 600 Go libres |
| **Système d'exploitation** | Windows 11 Professionnel | Version 64-bit |

---

## 2. Environnement Logiciel

Un environnement Python isolé a été créé spécifiquement pour le projet dans `ARCHI_AI/.venv` sans impacter les autres projets ni modifier les packages globaux du système.

| Outil / Bibliothèque | Version installée | Rôle |
| :--- | :--- | :--- |
| **Python** | 3.11.9 | Runtime Python de base |
| **PyTorch** | `2.6.0+cu124` | Framework de Deep Learning avec support CUDA 12.4 |
| **Torchvision** | `0.21.0+cu124` | Utilitaires et traitement d'image |
| **CUDA Driver / Runtime** | Pilote 616.92 / CUDA 13.4 UMD / CUDA 12.4 PyTorch | Accélération matérielle Tensor Cores |
| **Transformers** | `5.17.0` | Implémentation du modèle Qwen2-VL |
| **Accelerate** | `1.15.0` | Gestion du placement des poids et de la mémoire GPU |
| **BitsAndBytes** | `0.50.2` | Moteur de quantification 4-bit NF4 sous Windows |
| **Qwen-VL-Utils** | `0.0.14` | Découpage et encodage des patchs visuels pour Qwen2-VL |
| **Pillow (PIL)** | `12.3.0` | Chargement et manipulation de l'image de test |

---

## 3. Modèle Utilisé et Quantification

- **Modèle de départ** : `Qwen/Qwen2-VL-7B-Instruct`
  - Poids complets natifs (BF16) : ~14.5 Go (non exécutable en direct sur un GPU 8 Go).
- **Quantification appliquée** : **4-bit NormalFloat (NF4)** via `bitsandbytes`.
  - Type de calcul (`bnb_4bit_compute_dtype`) : `torch.bfloat16` (support matériel natif Ada Lovelace).
  - Double quantification (`bnb_4bit_use_double_quant`) : Activée (`True`), réduisant encore l'empreinte mémoire des constantes de quantification.
  - Résolution d'image encadrée : min 256x28x28 pixels, max 1024x768 pixels pour garantir une allocation maîtrisée des tokens visuels (1 064 tokens d'entrée au total).

---

## 4. Métriques Mémoire (VRAM / RAM) et Audit de Reproductibilité

### A. Empreinte Mémoire Vérifiée (Mesures réelles nvidia-smi & PyTorch)

| Étape de l'Inférence | VRAM PyTorch Allouée | VRAM PyTorch Réservée | VRAM Système Totale (NVIDIA) | Marge VRAM Libre | RAM Système (Total: 15.7 Go) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Avant chargement** | 0.0 Mo (0.00 Go) | 0.0 Mo (0.00 Go) | 1 120.0 Mo (1.09 Go) | 7 068.0 Mo (6.90 Go) | 11.38 Go (Process RSS: 514 Mo) |
| **Après chargement (Modèle 4-bit)** | 5 657.7 Mo (5.53 Go) | 5 708.0 Mo (5.57 Go) | 6 953.0 Mo (6.79 Go) | 1 235.0 Mo (1.21 Go) | 11.72 Go (Process RSS: 847 Mo) |
| **Pendant Inférence #1 (Pic)** | **6 125.1 Mo (5.98 Go)** | 6 458.0 Mo (6.31 Go) | **7 721.0 Mo (7.54 Go)** | **467.0 Mo (0.46 Go)** | 11.75 Go |
| **Après Inférence #1 (avant cleanup)** | 5 683.8 Mo (5.55 Go) | 6 458.0 Mo (6.31 Go) | 7 721.0 Mo (7.54 Go) | 467.0 Mo (0.46 Go) | 11.75 Go |
| **Après cleanup (`empty_cache`)** | 5 665.9 Mo (5.53 Go) | 5 708.0 Mo (5.57 Go) | 7 003.0 Mo (6.84 Go) | 1 185.0 Mo (1.16 Go) | 11.73 Go |
| **Pendant Inférence #2 (Pic)** | **6 128.5 Mo (5.99 Go)** | 6 458.0 Mo (6.31 Go) | **7 713.0 Mo (7.53 Go)** | **475.0 Mo (0.46 Go)** | 11.75 Go |
| **Après cleanup Inférence #2** | 5 665.9 Mo (5.53 Go) | 5 708.0 Mo (5.57 Go) | 7 003.0 Mo (6.84 Go) | 1 185.0 Mo (1.16 Go) | 11.73 Go |

> [!NOTE]
> **Dérive mémoire (Memory Leak)** : La dérive VRAM au repos entre l'inférence #1 et l'inférence #2 après nettoyage est de **+0.00 Mo**. Aucune fuite de mémoire n'a été constatée au niveau des couches BitsAndBytes ou du modèle.

### B. Performances Temporelles & Reproductibilité

- **Temps de chargement modèle (depuis cache local HF)** : **25.60 s à 26.32 s** (contre 665 s lors du téléchargement initial).
- **Inférence #1** :
  - Durée : **8.57 s**
  - Tokens générés : **145 tokens**
  - Vitesse : **16.91 tokens/s**
- **Inférence #2 (Reproductibilité)** :
  - Durée : **7.80 s**
  - Tokens générés : **145 tokens**
  - Vitesse : **18.59 tokens/s** (gain de ~9% grâce au pré-chauffage des buffers et caches CUDA).
- **Conformité textuelle** : **100% identique** (reproductibilité déterministe stricte confirmée en décodage glouton).

---

## 5. Test Multimodal : Question et Réponse Obtenue

- **Image de test** : `ARCHI_AI/test_images/sample_interior.jpg` (Résolution: 1024x768 JPEG, salon contemporain ouvert).
- **Gestion de l'image** : Capping de résolution via `AutoProcessor(min_pixels=256*28*28, max_pixels=1024*768)`. L'image de test produit 1 064 tokens d'entrée (texte prompt + patchs visuels).
- **Nombre max de tokens configuré** : `max_new_tokens=350` (la génération s'arrête naturellement à 145 tokens sur `<|im_end|>`).
- **Question posée (Français)** :
  > *"Décris cette pièce en tant qu'architecte d'intérieur : précise le type d'espace, le style décoratif dominant, les matériaux identifiables et l'ambiance lumineuse."*

- **Réponse générée par le modèle (identique sur les deux runs)** :
  > *"Cette pièce est un espace de salon ouvert, conçu avec un style décoratif contemporain. Le style est marqué par une esthétique minimaliste, avec une combinaison de meubles modernes et des éléments naturels. Les matériaux identifiables comprennent du bois, du cuir, du métal et des plantes vertes. L'ambiance lumineuse est naturelle et accueillante, grâce à la présence d'une grande fenêtre qui laisse entrer beaucoup de lumière naturelle. Les couleurs dominantes sont le blanc, le beige et le marron, ce qui crée un espace chaleureux et relaxant."*

---

## 6. Analyse des Risques et Robustesse

1. **Marge VRAM restante (~467 Mo)** :
   - *Risque* : Le GPU RTX 4060 Ti 8 Go fonctionne à 94.3% de sa capacité mémoire totale (7.72 Go utilisés sur 8.18 Go).
   - *Conséquence* : Si la résolution de l'image est augmentée au-delà de 1024x768 sans capping, ou si un contexte de conversation multi-tours dépasse ~2 000 tokens, un crash CUDA Out-Of-Memory (OOM) surviendra.
2. **Impact de l'environnement Windows hôte** :
   - *Risque* : Windows 11 et l'accélération matérielle de l'interface occupent ~1.12 Go de VRAM de base.
   - *Recommandation* : Ne pas exécuter d'autres logiciels graphiques intensifs (navigateurs avec onglets 3D, jeux, logiciels CAO) en parallèle lors de l'inférence.
3. **Absence de fuite mémoire** :
   - Le test multi-passes confirme que le garbage collection et `torch.cuda.empty_cache()` rétablissent exactement l'empreinte au repos (5.66 Go PyTorch / 7.00 Go système). Le modèle peut donc être sollicité de manière répétée sans dégradation.

---

## 7. Prochaines Étapes Recommandées (Après Validation Audit)

1. **Conservation stricte du capping de résolution** (`max_pixels <= 1024*768`) pour tout prompt image.
2. **Nettoyage explicite du cache CUDA** après chaque inférence dans les wrappers de service interactif.
3. **Maintien du format NF4 4-bit** comme base de référence sur cette carte 8 Go.
