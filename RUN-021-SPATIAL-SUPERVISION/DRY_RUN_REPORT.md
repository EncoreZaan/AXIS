# AXIS — Rapport de Validation du Dry Run (`DRY_RUN_REPORT.md`)

> **Run Identifier:** `RUN-021-SPATIAL-SUPERVISION`  
> **Date:** 2026-09-23  
> **Jeu de Données Testé:** `RUN-021-SPATIAL-SUPERVISION/train.jsonl` (6 160 exemples)  
> **Verdict Global:** **DRY_RUN: PASS** | **POIDS STRICTEMENT INCHANGÉS**

---

## 1. Objectif du Dry Run

Conformément à la Règle §28, le dry-run valide :
1. Le chargement sans faille du nouveau jeu de données spatial via un `Dataset` PyTorch.
2. La collation multimodale (assemblage simultané des tenseurs images $[B, 3, 256, 256]$ et des tokens textuels $[B, \text{seq\_len}]$).
3. Le passage avant (Forward Pass) et la dérivation des gradients (Backward Pass).
4. **L'INVARIANT ABSOLU :** `optimizer.step()` est **STRICTEMENT DÉSACTIVÉ**, et les poids du modèle restent **100 % IDENTIQUES** avant et après l'exécution.

---

## 2. Métriques Mesurées

| Métrique | Valeur Observée | Seuil / Invariant | Verdict |
| :--- | :---: | :---: | :---: |
| **Exemples d'entraînement chargés** | **6 160** | $\ge 1\,000$ | **PASS** |
| **Pas de simulation exécutés** | **8 pas** | $\ge 5$ pas | **PASS** |
| **Taille de lot (Batch Size)** | **2** (16 exemples testés) | $\ge 1$ | **PASS** |
| **Perte moyenne (Loss)** | **6.4716** | Valeur finie ($\neq \text{NaN}, \neq \text{Inf}$) | **PASS** |
| **Norme moyenne de gradient** | **0.6726** | Flux de gradient sain | **PASS** |
| **Appel à `optimizer.step()`** | **FALSE (DÉSACTIVÉ)** | Strictement `FALSE` | **PASS** |
| **Mise à jour des poids** | **FALSE (AUCUNE)** | Strictement `FALSE` | **PASS** |
| **Empreinte SHA-256 initiale des poids**| `69d0872fa01b1144596e80a3c61ad3fea7f976d80f698dec553440c92a73018f` | Conforme | **PASS** |
| **Empreinte SHA-256 finale des poids** | `69d0872fa01b1144596e80a3c61ad3fea7f976d80f698dec553440c92a73018f` | Identique à l'initiale | **PASS** |
| **Poids strictement non modifiés** | **TRUE** | Strictement `TRUE` | **PASS** |
| **Erreurs d'accès disque / images** | **0** | Strictement 0 | **PASS** |

---

## 3. Détail des Pas d'Exécution

```text
Step 1/8: Loss = 6.4981, GradNorm = 0.6795, Time = 9.1 ms [Batch: archi_pilot_0002_RESBIM_DOOR_COUNT, archi_pilot_0002_RESBIM_WINDOW_COUNT]
Step 2/8: Loss = 6.4757, GradNorm = 0.6675, Time = 3.6 ms [Batch: archi_pilot_0002_RESBIM_WALL_COUNT, archi_pilot_0003_RESBIM_DOOR_COUNT]
Step 3/8: Loss = 6.4486, GradNorm = 0.6700, Time = 3.4 ms [Batch: archi_pilot_0003_RESBIM_WINDOW_COUNT, archi_pilot_0003_RESBIM_WALL_COUNT]
Step 4/8: Loss = 6.4906, GradNorm = 0.6795, Time = 3.1 ms [Batch: archi_pilot_0004_RESBIM_DOOR_COUNT, archi_pilot_0004_RESBIM_WINDOW_COUNT]
Step 5/8: Loss = 6.4713, GradNorm = 0.6675, Time = 3.4 ms [Batch: archi_pilot_0004_RESBIM_WALL_COUNT, archi_pilot_0006_RESBIM_DOOR_COUNT]
Step 6/8: Loss = 6.4527, GradNorm = 0.6696, Time = 4.5 ms [Batch: archi_pilot_0006_RESBIM_WINDOW_COUNT, archi_pilot_0006_RESBIM_WALL_COUNT]
Step 7/8: Loss = 6.4981, GradNorm = 0.6795, Time = 4.9 ms [Batch: archi_pilot_0007_RESBIM_DOOR_COUNT, archi_pilot_0007_RESBIM_WINDOW_COUNT]
Step 8/8: Loss = 6.4775, GradNorm = 0.6677, Time = 4.8 ms [Batch: archi_pilot_0007_RESBIM_WALL_COUNT, archi_pilot_0008_RESBIM_DOOR_COUNT]
```

---

## 4. Conclusion

Le pipeline multimodal charge et traite parfaitement le jeu de données `RUN-021-SPATIAL-SUPERVISION`.
L'assemblage des images matricielles avec les questions et réponses concises s'effectue sans aucune anomalie.
Le système est prêt pour une future phase d'entraînement lorsque celle-ci sera formellement autorisée.
