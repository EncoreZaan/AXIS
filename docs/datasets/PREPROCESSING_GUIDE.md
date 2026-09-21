# ARCHI-AI — Guide Pratique de Preprocessing & Extension

## 1. Exécution du Pipeline

Le pipeline peut être lancé en ligne de commande depuis la racine du projet ou depuis le répertoire `ARCHI_AI`.

### Normalisation Complète
Pour exécuter la normalisation de l'intégralité des sources CORE :
```bash
python -m dataset_tools.preprocessing.run --source all
```

### Normalisation Ciblée
Pour ne traiter qu'une seule source ou un groupe de sources :
```bash
# Plans d'architecte ResPlan uniquement
python -m dataset_tools.preprocessing.run --source resplan

# Benchmark MMMU Architecture
python -m dataset_tools.preprocessing.run --source mmmu

# Maquettes numériques IFC
python -m dataset_tools.preprocessing.run --source buildingsmart,ifc_bench_models,resbim_ifc
```

### Mode Test / Échantillon
Pour valider rapidement la chaîne sur un échantillon restreint :
```bash
python -m dataset_tools.preprocessing.run --source all --limit 10
```

---

## 2. Ajouter une Nouvelle Source RAW

Pour intégrer un nouveau jeu de données architectural (ex: un nouveau corpus IFC ou un jeu de relevés de façades) :

1. **Placer les données brutes dans `dataset/raw/external/core/<nom_source>/`** (ne jamais modifier les sources existantes).
2. **Créer un nouvel adaptateur dans `dataset_tools/preprocessing/<modalite>/<nom>_preprocessor.py`** :
   - Hériter de `BasePreprocessor`.
   - Implémenter les propriétés `source_name`, `modality`, `default_routing`.
   - Implémenter le générateur `process(limit=None)`.
   - Utiliser `build_provenance(...)` pour chaque élément émis.
3. **Enregistrer l'adaptateur dans `dataset_tools/preprocessing/registry.py`**.
4. **Ajouter le test unitaire dans `ARCHI_AI/tests/test_preprocessing.py`**.
5. **Exécuter la suite de tests** : `pytest ARCHI_AI/tests`.

---

## 3. Gestion des Statuts & Alertes Forensic

- **`PASS`** : Entité intègre, validée syntaxiquement et sémantiquement, certifiée pour le Master Dataset V1.
- **`WARNING`** : Alerte non bloquante (ex: cotation inconnue, image secondaire manquante).
- **`REVIEW`** : Ambiguïté de métadonnées nécessitant un examen manuel.
- **`FAIL`** : Donnée corrompue ou non conforme. **Exclusion stricte du Master Dataset V1.**
- **`FROZEN (LEGAL_REVIEW_REQUIRED)`** : Source exclue pour motif juridique (ex: `CORE_FLOORPLANCAD`).
