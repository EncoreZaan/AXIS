## Description of Changes

Please provide a summary of the changes made and the motivation behind them.

- Fixes #(issue)
- Type of change:
  - [ ] Bug fix (non-breaking change fixing an issue)
  - [ ] New feature (non-breaking change adding functionality)
  - [ ] Research artifact / report update
  - [ ] Dataset pipeline enhancement
  - [ ] Documentation improvement
  - [ ] Breaking change

---

## Scientific & Data Integrity Checklist

Before opening this PR, ensure all scientific guidelines of the AXIS project are respected:

- [ ] **No Fabricated Data or Metrics:** All reported numbers, baselines, and errors are extracted from verified run logs or reproducible evaluation scripts.
- [ ] **Gold Set Sanctity:** The Gold Set V3 remains strictly read-only and unpolluted. No training or tuning was conducted on the Gold Set.
- [ ] **Anti-Leakage Verification:** No asset or project crosses train/validation/test splits.
- [ ] **No Secret / Private Data:** No API keys, passwords, personal tokens, or proprietary datasets under restrictive licenses are introduced.
- [ ] **Automated Tests:** All unit and integration tests pass (`pytest tests`).
- [ ] **Documentation:** Any new pipeline or tool is accompanied by clear documentation in `docs/`.
