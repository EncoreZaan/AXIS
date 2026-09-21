## Résumé / Summary

<!-- Que fait cette PR, en 2-3 phrases ? / What does this PR do, in 2-3 sentences? -->

Fixes #(issue)

## Type de changement / Type of Change

- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Research artifact / report update
- [ ] Dataset pipeline enhancement
- [ ] Documentation improvement
- [ ] Breaking change

## Motivation

<!-- Pourquoi ce changement est-il nécessaire ? Quel problème résout-il ?
     Why is this change needed? What problem does it solve? -->

## Tests effectués / Tests Performed

<!-- Commandes exécutées et résultats. Précisez si des tests dépendant de
     données privées n'ont pas pu être exécutés, et pourquoi.
     Commands run and their results. State explicitly if any tests requiring
     the private dataset corpus could not be run, and why. -->

- [ ] `pytest tests/test_audit_validators.py tests/test_master_pipeline.py` passes (CI gate, no private data required)
- [ ] Full `pytest tests` run, if the private dataset corpus was available locally
- [ ] Manually verified affected functionality

## Impact scientifique / Scientific Impact

<!-- Ce changement affecte-t-il une métrique, un split, un dataset, un
     benchmark documenté ? Si oui, lequel, et comment le nouveau chiffre a-t-il
     été obtenu ?
     Does this change affect a documented metric, split, dataset, or
     benchmark? If so, which one, and how was the new number obtained? -->

## Reproductibilité / Reproducibility

<!-- Si cette PR introduit ou modifie une expérience, suit-elle
     docs/RESEARCH_CONTRIBUTION_PROTOCOL.md ? Un autre contributeur peut-il
     reproduire ce résultat à partir de cette PR seule ?
     If this PR introduces or changes an experiment, does it follow
     docs/RESEARCH_CONTRIBUTION_PROTOCOL.md? Can another contributor reproduce
     this result from this PR alone? -->

## Données utilisées / Data Used

<!-- Quelles sources de données (voir DATASET.md) sont concernées ?
     S'agit-il de nouvelles données ?
     Which data sources (see DATASET.md) are involved? Is any new data introduced? -->

## Licence des nouvelles données / License of New Data

<!-- Si cette PR ajoute des données, images, checkpoints ou tout autre asset :
     sous quelle licence sont-ils publiés, et avez-vous le droit de les
     redistribuer ? Voir THIRD_PARTY_LICENSES.md. N'ajoutez jamais un asset
     tiers que vous n'êtes pas autorisé à redistribuer.
     If this PR adds any data, images, checkpoints, or other assets: under
     what license are they released, and do you have the right to
     redistribute them? See THIRD_PARTY_LICENSES.md. Never add a third-party
     asset you are not licensed to redistribute. -->

- [ ] N/A — this PR introduces no new data/assets
- [ ] New data/assets included, with license stated above and redistribution rights confirmed

---

## Checklist scientifique et d'intégrité des données / Scientific & Data Integrity Checklist

- [ ] **No Fabricated Data or Metrics:** All reported numbers, baselines, and errors are extracted from verified run logs or reproducible evaluation scripts.
- [ ] **Gold Set Sanctity:** The Gold Set V3 remains strictly read-only and unpolluted. No training or tuning was conducted on the Gold Set.
- [ ] **Anti-Leakage Verification:** No asset or project crosses train/validation/test splits.
- [ ] **No Secret / Private Data:** No API keys, passwords, personal tokens, or proprietary datasets under restrictive licenses are introduced.
- [ ] **Documentation:** Any new pipeline or tool is accompanied by clear documentation in `docs/`.
- [ ] **License Compliance:** Any new file respects the MIT license for AXIS code, or is clearly marked and licensed separately per `THIRD_PARTY_LICENSES.md` if it is third-party data.
