# ARCHI-AI : Package d'Entraînement Distant QLoRA (GPU 24 Go)

Ce package autonome et reproductible contient l'ensemble des scripts, configurations et données nécessaires pour exécuter le micro-test d'entraînement QLoRA de **Qwen2-VL-7B-Instruct** sur une instance distante Linux équipée d'un GPU de 24 Go (RTX 3090, RTX 4090, A10G, etc.).

---

## 1. Structure du Package

```text
experiment_package/
├── README.md                      # Guide d'installation et d'utilisation
├── EXPERIMENT_PLAN.md             # Protocole expérimental et critères de validation
├── requirements.txt               # Dépendances Python épinglées
├── check_environment.py           # Diagnostic matériel et logiciel (GPU / VRAM / CUDA)
├── train_qlora.py                 # Pipeline d'entraînement QLoRA avec garde-fous
├── config/
│   └── qlora_experiment.yaml      # Configuration hyperparamètres (chemins relatifs)
└── dataset/
    ├── train.jsonl                # 20 exemples validés V2
    ├── validation.jsonl           # 5 exemples de validation V2
    └── images/                    # 25 photographies d'architecture réalignées
```

---

## 2. Installation sur Instance Linux Distante

### Étape 2.1 : Créer et activer l'environnement virtuel
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

### Étape 2.2 : Installer PyTorch avec support CUDA 12.4
```bash
pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124
```

### Étape 2.3 : Installer les dépendances du package
```bash
pip install -r requirements.txt
```

---

## 3. Procédure de Vérification (Sans Entraînement)

### Étape 3.1 : Diagnostic de l'environnement matériel et logiciel
Vérifie la version de Python, la détection CUDA, le modèle de GPU, les 24 Go de VRAM et les bibliothèques PEFT / BitsAndBytes :
```bash
python check_environment.py
```
*Le script doit afficher `STATUS : READY FOR TRAINING`.*

### Étape 3.2 : Validation de l'intégrité du dataset et des chemins
Vérifie les 25 exemples JSONL et la lisibilité des 25 images sans télécharger ni charger le modèle 7B :
```bash
python train_qlora.py --validate-only
```
*Le script doit afficher `STATUS VALIDATION : PASS`.*

---

## 4. Lancement de l'Entraînement (Sur GPU 24 Go Uniquement)

> **IMPORTANT :** Le script refuse de s'exécuter si l'argument explicite `--train` n'est pas fourni.

```bash
python train_qlora.py --train
```

Le script exécutera :
1. Le chargement en 4-bit NF4 du modèle `Qwen/Qwen2-VL-7B-Instruct`
2. Le gel de la tour visuelle et la greffe LoRA sur les projections LLM
3. L'entraînement sur 2 époques (~5 steps d'accumulation de gradient)
4. L'évaluation sur le split validation
5. La sauvegarde complète des artefacts dans `outputs/archi_ai_micro_experiment/`
6. Le test de rechargement de l'adaptateur pour certifier son intégrité
