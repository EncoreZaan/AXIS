# Rapport d'Audit Environnement Matériel & Logiciel

Date de l'audit : 2026-09-20 22:52 (Heure locale)  
Machine analysée : Environnement local réel

---

## 1. Caractéristiques Détaillées du Système

| Paramètre | Valeur détectée | Détails / Commandes |
| :--- | :--- | :--- |
| **1. GPU NVIDIA exact** | **NVIDIA GeForce RTX 4060 Ti** | Détecté via `nvidia-smi` (Architecture Ada Lovelace) |
| **2. VRAM totale** | **8 188 MiB (~8.00 Go)** | GDDR6 |
| **3. VRAM actuellement disponible** | **~7 193 MiB (~7.02 Go)** | 995 MiB occupés par les processus système et applications en cours |
| **4. Version du pilote NVIDIA** | **616.92** | Version du pilote WDDM |
| **5. Version CUDA supportée** | **CUDA 13.4** (UMD Version) | Niveau maximal supporté par le pilote |
| **6. CPU** | **Intel(R) Core(TM) i5-14400F** | 10 cœurs physiques (6 P-cores + 4 E-cores), 16 processeurs logiques |
| **7. RAM totale et disponible** | **Totale : 15.72 Go** (16 480 368 Ko)<br>**Disponible : 4.72 Go** (4 953 472 Ko) | Mesuré via `Win32_OperatingSystem` |
| **8. Système d'exploitation** | **Microsoft Windows 11 Professionnel** | Version 10.0.26200 (Build 26200) |
| **9. Version Python** | **Python 3.11.9** | Exécutable : `WindowsApps\PythonSoftwareFoundation.Python.3.11` |
| **10. Version PyTorch** | **Non installée** | Aucun module `torch` trouvé dans l'environnement Python |
| **11. Support BF16 du GPU** | **OUI (Matériel natif)** | Architecture Ada Lovelace (Compute Capability 8.9), cœurs Tensor 4e gen |
| **12. Espace disque disponible** | **Lecteur C: : 607.92 Go libres** (sur 952.09 Go)<br>Lecteur D: : 170.88 Go libres (sur 953.85 Go)<br>Lecteur E: : 1 518.04 Go libres (sur 1 863.01 Go) | Mesuré via `Get-PSDrive` |

---

## 2. Analyse de Faisabilité : State-Tuning RWKV-7 2.9B

### Besoins théoriques pour RWKV-7 2.9B
- **Poids du modèle (BF16 / FP16)** : ~5.8 Go de VRAM.
- **États cachés et gradients d'état** : Bien que le state-tuning gèle le réseau et n'entraîne que les états initiaux/appris (très faible empreinte mémoire d'optimiseur), le calcul de la passe avant et de la rétropropagation (backstepping RWKV-7) nécessite de conserver les activations intermédiaires.
- **VRAM requise au minimum** : ~7.5 Go à 9+ Go en BF16 natif (selon la longueur de contexte `ctx_len` et la taille du batch).
- **RAM système requise** : Le chargement initial des poids de 2.9B nécessite au moins 6 à 8 Go de RAM libre avant transfert sur le GPU.

### Évaluation pour cette machine
1. **GPU (8 Go VRAM, ~7 Go libres)** :
   - **En BF16 natif pur** : **Trop juste / Risque critique d'OOM (Out Of Memory)**. Le modèle seul occupera ~5.8 Go sur les ~7 Go libres, ne laissant qu'environ 1.2 Go pour le runtime CUDA, les activations du contexte et le cache PyTorch.
   - **Sous condition d'optimisations** : Faisable uniquement si le modèle est chargé avec une quantification (ex. 8-bit / 4-bit pour le backbone avec états en BF16) ou avec un batch size strict de 1 et une longueur de contexte très courte.
2. **RAM Système (16 Go au total, seulement 4.72 Go libres)** :
   - Le système d'exploitation et les applications en cours occupent ~11 Go de RAM. Charger un modèle 2.9B en RAM sans libérer de mémoire risque de déclencher une forte pagination (swap disque).
3. **Environnement de compilation** :
   - PyTorch, CUDA Toolkit (nvcc) et les compilateurs C++ (MSVC) ne sont pas configurés dans le PATH actuel, ce qui sera indispensable pour compiler les kernels CUDA personnalisés nécessaires à RWKV-7 (`wkv7` / `wind_backstepping`).
