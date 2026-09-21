# 🧭 START HERE

*[English speakers: this file is in French; the same content, in English, lives in the "What is AXIS?" and "Current Research Status" sections of [`README_EN.md`](README_EN.md).]*

Bienvenue sur **AXIS**. Ce document répond en quelques minutes aux questions qu'on se pose en arrivant sur le projet, puis renvoie vers la documentation détaillée.

---

## Qu'est-ce que AXIS ?

**AXIS (Architectural eXpert Intelligence System)** est un projet de recherche open source (licence MIT pour le code) qui développe une intelligence artificielle spécialisée dans le raisonnement spatial, géométrique et architectural : lecture de plans 2D, modèles BIM/IFC 3D, calcul de distances et de zones de dégagement, conformité aux normes d'accessibilité.

AXIS est la suite publique d'un projet mené précédemment en interne sous le nom `ARCHI-AI`. Toute la traçabilité scientifique (identifiants, hashs, journaux de run) a été conservée — voir [`docs/history/project-history.md`](docs/history/project-history.md).

## Pourquoi existe-t-il ?

Les modèles de langage et vision-langage généralistes hallucinent des mesures physiques, confondent murs porteurs et cloisons, et ratent des violations de normes d'accessibilité évidentes pour un architecte. AXIS explore une alternative : une IA spécialisée, entraînée et évaluée avec des garde-fous scientifiques stricts (benchmarks adversariaux, découpages sans fuite de données, Gold Set immuable) plutôt que des affirmations non vérifiées. Voir [`RESEARCH.md`](RESEARCH.md) pour la méthodologie complète.

## Où en est-il ?

En résumé, sans filtre :

- **Validé empiriquement, sur un périmètre étroit :** un checkpoint entraîné atteint 0,0517 m d'erreur moyenne (MAE) sur une tâche de vérification de dégagement (`CLEARANCE_CHECK`), contre 2,7739 m pour une baseline triviale — une réduction relative de 98,14 %. **Ce résultat ne concerne qu'une tâche précise et ne prouve aucune compréhension architecturale générale.**
- **Expérimental :** preuve de concept d'entraînement QLoRA sur un VLM (Qwen2-VL-7B), modèle de vision 2D non encore entraîné.
- **Bloqué :** le pré-entraînement multimodal complet (faute de paires 2D/3D suffisantes), les données ResPlan pour tout calcul métrique (distorsion d'échelle prouvée), FloorPlanCAD (revue légale en attente), le `Pre-Training Gate` formel (`TRAINING_ALLOWED: NO`).
- **Planifié, non commencé :** la piste d'accélération DSpark.

Détail complet et sourcé : [`PROJECT_STATUS.md`](PROJECT_STATUS.md) et [`ROADMAP.md`](ROADMAP.md).

## Comment puis-je l'exécuter ?

```bash
git clone https://github.com/EncoreZaan/AXIS.git
cd AXIS
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest tests
```

Le corpus brut privé, le Gold Set V3 et le checkpoint entraîné ne sont **pas** inclus dans ce dépôt (voir [`DATASET.md` §5](DATASET.md#5-data-access-policy)). Sur un clone neuf, environ 35 des 93 tests collectés passent ; les autres nécessitent ce corpus privé. Détail complet : [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## Comment puis-je contribuer ?

1. Lisez [`docs/CONTRIBUTOR_GUIDE.md`](docs/CONTRIBUTOR_GUIDE.md) pour une orientation détaillée du dépôt (dossiers, scripts, premières contributions par niveau de difficulté).
2. Suivez le processus dans [`CONTRIBUTING.md`](CONTRIBUTING.md) (fork, installation, branche, tests, pull request).
3. Pour proposer une expérience scientifique, suivez [`docs/RESEARCH_CONTRIBUTION_PROTOCOL.md`](docs/RESEARCH_CONTRIBUTION_PROTOCOL.md).

Documentation, tests, datasets légalement redistribuables, benchmarks, outils BIM/IFC, géométrie, vision par ordinateur, ML, optimisation GPU, infrastructure/CI, corrections de bugs, exemples et visualisations sont tous les bienvenus.

## Qu'est-ce qui est réellement validé ?

- Master Dataset v2 : 65 342 assets, 0 fuite SHA256/projet (vérifiable via les scripts de `dataset_tools/master_pipeline/`).
- Gold Set V3 : 200 instances certifiées + 200 négatifs adverses, hash SHA256 documenté.
- Benchmark `CLEARANCE_CHECK` : MAE 0,0517 m, avec les réserves statistiques détaillées dans [`EVALUATION.md` §3.2](EVALUATION.md#32-why-100-accuracy-is-not-a-robustness-proof).
- Suite CI indépendante des données privées : 9/9 tests passants, vérifié sur clone neuf.

## Qu'est-ce qui ne l'est pas encore ?

- Aucune capacité de raisonnement architectural général.
- Le modèle de vision 2D (`ROOM_TOPOLOGY`).
- Le raisonnement multimodal 2D↔3D à l'échelle.
- L'accélération DSpark.
- La reproduction complète (99/99 tests) sans accès au corpus privé du mainteneur.

## Pour aller plus loin

| Question | Document |
| :--- | :--- |
| Vue d'ensemble complète (FR) | [`README.md`](README.md) |
| Full overview (EN) | [`README_EN.md`](README_EN.md) |
| Statut détaillé par sous-système | [`PROJECT_STATUS.md`](PROJECT_STATUS.md) |
| Feuille de route | [`ROADMAP.md`](ROADMAP.md) |
| Méthodologie scientifique | [`RESEARCH.md`](RESEARCH.md) |
| Architecture technique | [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| Dataset & licences tierces | [`DATASET.md`](DATASET.md), [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) |
| Protocole de benchmark | [`EVALUATION.md`](EVALUATION.md) |
| Reproduire les expériences | [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) |
| Contribuer | [`CONTRIBUTING.md`](CONTRIBUTING.md), [`docs/CONTRIBUTOR_GUIDE.md`](docs/CONTRIBUTOR_GUIDE.md) |
| Licence | [`LICENSE`](LICENSE) (MIT, code AXIS) |
