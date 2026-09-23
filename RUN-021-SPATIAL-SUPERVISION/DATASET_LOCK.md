# AXIS — Cryptographic Dataset Lock (`RUN-021-SPATIAL-SUPERVISION`)

> **Lock Date:** 2026-09-23  
> **Dataset Target:** `RUN-021-SPATIAL-SUPERVISION/`  
> **Statut Invariant:** **DATASET_HASH_LOCK: PASS** | **SCELLÉ & IMMUABLE**

---

## 1. Table des Empreintes Cryptographiques (SHA-256)

| Artefact Critique | Chemin Relatif | Taille (Octets) | Empreinte SHA-256 |
| :--- | :--- | :---: | :--- |
| **Manifeste Global** | `manifest.jsonl` | 12 008 657 | `6560747bccaa696a2ac7488bd5594d3c7a482c2aa4eb58460fcbcc99f830ea06` |
| **Dataset Manifest** | `dataset_manifest.jsonl` | 12 008 657 | `6560747bccaa696a2ac7488bd5594d3c7a482c2aa4eb58460fcbcc99f830ea06` |
| **Train Split** | `train.jsonl` | 9 302 614 | `227ba7db7769e3f25d365a33efd03126e18612cf5821f1f23dcd2342a701e849` |
| **Validation Split** | `validation.jsonl` | 1 187 887 | `c543a319321534f016c94aeb8ee74503bc8f01511c232ec91394d69a307467d2` |
| **Test Split** | `test.jsonl` | 1 518 156 | `aaba73433c9ccea7a5c6134154577ea80591e23755665794bec603ebdf53053f` |
| **Dataset Config** | `dataset_config.json` | 1 556 | `9c0908c4c2bc25c647cfde7d885e4d8fe9ba507fb00fb79ce42852942ea60d6c` |
| **Audit Forensique** | `DATA_CAPABILITY_AUDIT.md` | 8 588 | `826db52b3a1b015e11c65eb101abb1c673bdbaef8f62354b7c482cd2db8149b2` |
| **Spécifications Spatiales** | `SPATIAL_RELATION_DEFINITIONS.md` | 7 068 | `75fd23aa072ef9f3a5866e58edec80cf788d652221f47ee2e987efac06bc49b8` |
| **Rapport de Split** | `SPLIT_REPORT.md` | 2 548 | `18977a6f1bfbf8f24c033723debd94c4c600eac39c7a480188375474284ebf49` |
| **Rapport d'Étanchéité**| `LEAKAGE_REPORT.md` | 2 912 | `4da1829cd14ed3d2439645ad9c19fcaa6b37b58de8a8ae159e9d06a710323aba` |
| **Rapport Qualité** | `DATA_QUALITY_REPORT.md` | 3 244 | `b4bb16307f96e718598eaf3819cb969435ec675b0b1de2b6de9922ab337afdea` |
| **Audit Manuel (50 ech.)**| `MANUAL_AUDIT.md` | 8 962 | `2c4ca1ae1b5d21f488b858ee25176f11cec33e1d8bab5587eca5b8343f9ac3bb` |

---

## 2. Déclaration d'Immuabilité

Ce jeu de données de supervision spatiale expérimentale est scellé cryptographiquement et immuable.
Toute modification ultérieure des contenus d'actifs, des découpages, des schémas conversationnels ou des relations dérivées nécessite une incrémentation de version et une régénération intégrale des empreintes de contrôle.

```text
TRAINING_ALLOWED: NO
TRAINING_MAY_BEGIN: NO
```
