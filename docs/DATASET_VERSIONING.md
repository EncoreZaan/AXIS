# Versionnement et Traçabilité des Datasets (ARCHI-AI)

## 1. Principes de Reproductibilité

Chaque itération du dataset ARCHI-AI constitue une version immuable enregistrée dans `dataset/versions/<version_tag>/` :
- Un fichier `master_annotations.jsonl` figé contenant les métadonnées complètes.
- Un manifeste d'intégrité avec les SHA-256 de chaque document.
- Un tag sémantique explicite.

---

## 2. Version Historique de Référence : `v0.1-micro-baseline`

- **Date :** Septembre 2026
- **Objectif :** Servir de référentiel historique issu du micro-entraînement initial de 25 exemples.
- **Répartition :**
  - `train` : 20 exemples (`archi_001` à `archi_025`, sauf validation)
  - `validation` : 5 exemples (`archi_005`, `archi_010`, `archi_015`, `archi_020`, `archi_025`)
  - `test` : 0 exemple (sanctuarisé pour éviter d'inventer des données synthétiques artificielles ou de contaminer la validation).
- **Emplacement :** `dataset/versions/v0.1-micro-baseline/`

---

## 3. Règle de Non-Régression pour les Versions Futures

Toute future version (`v0.2`, `v1.0`) devra :
1. Être créée dans un répertoire dédié sous `dataset/versions/`.
2. Passer avec succès l'ensemble de la suite QA (`pytest tests/`).
3. Démontrer l'absence totale de fuite vers les partitions `validation` et `test` via `SplitLeakageDetector`.
4. Faire l'objet d'un export traçable via `export_qwen_vl.py`.
