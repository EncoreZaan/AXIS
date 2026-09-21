# AXIS — Publication Readiness Audit (Remediation Pass)

> **⚠️ Superseded on license status:** this document records a remediation pass in which the code license was left explicitly `TBD` (§2.1, §5) as a decision for the project owner. That decision has since been made: AXIS's original code and documentation are now licensed under the **MIT License** (see [`LICENSE`](LICENSE), [`GOVERNANCE.md`](GOVERNANCE.md), [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md)). The rest of this document — the P0/P1 findings and fixes below — is kept unmodified as an accurate historical record of that remediation pass; do not read its TBD-license passages as the current state.
>
> **Prior audit reference commit:** `42b1f51` — "feat: official migration from ARCHI-AI to AXIS v0.1.0"
> **Prior verdict:** `PUBLICATION READINESS: YELLOW`
> **This document:** records what was actually inspected and changed in response to that audit, and states an updated verdict. It does not claim any metric, dataset, checkpoint, or capability beyond what is verifiable in this repository as of this remediation.

---

## 1. Method

Before changing anything, the repository was inspected directly: `git log`/`git status`/`git branch`, every top-level doc, `pyproject.toml`/`requirements.txt`/`.gitignore`, the dataset/evaluation/training scripts, and a repo-wide search for `ARCHI-AI`/`ARCHI_AI`, absolute/local paths, truncated hashes, and the specific files the prior audit named. The package was then actually installed (`pip install -e .`) and the test suite actually run (`pytest tests/`), rather than trusting the documentation's claims about what would happen — this surfaced several real defects the prior audit's static read did not catch (§4).

---

## 2. P0 Findings — Status

### 2.1. License Contradiction

**Finding confirmed.** `README.md` and `GOVERNANCE.md` both described AXIS as an "open-source... initiative" in prose while simultaneously stating, correctly, that the license is TBD — a direct terminological contradiction a legal reader would flag. `pyproject.toml`'s `license = {text = "TBD — Research Preview Only (All Rights Reserved pending formal license selection)"}` was internally consistent with the TBD framing but used a deprecated TOML table form.

**Fixed:**
- Replaced "open-source" with "publicly-released" / "publicly-visible" in `README.md` and `GOVERNANCE.md` prose describing AXIS itself, everywhere it conflicted with the TBD license status. Third-party dataset descriptions that accurately describe *upstream* sources as open-source were left untouched (they describe someone else's license, not AXIS's).
- Added an explicit terminology table to `README.md` ("License Status") and a "Terminology this project keeps distinct" section to `GOVERNANCE.md`, separating: public repository / open research / open-source code license / third-party dataset & checkpoint licenses.
- `pyproject.toml`: `license` migrated to the non-deprecated string form (`license = "LicenseRef-TBD-Research-Preview"`), removing a setuptools deprecation warning without inventing or selecting an actual license.
- No license was chosen on the maintainer's behalf. The status remains explicitly **TBD** everywhere.

### 2.2. Hardcoded Legacy Paths

**Finding confirmed, and larger than initially scoped.** `configs/qlora_experiment.yaml` did hardcode `ARCHI_AI/dataset/...` / `ARCHI_AI/outputs/...`. Searching beyond that one file (as instructed) found the same `ARCHI_AI/`-prefixed convention pervasively used across `dataset_tools/experiments/micro_pilot/` (the scripts that actually trained/evaluated checkpoint `ARCHI-AI-P4-005` and ran the Gold Set V3 evaluation) and several standalone Wave-1 audit scripts (`gold_set_builder.py`, `audit_calculator.py`, `decision_classifier.py`, `deep_audit.py`, `audit_diagnostics.py`), including `sys.path.insert(0, os.path.abspath("ARCHI_AI"))` / `from ARCHI_AI.dataset_tools... import ...` constructs. A `.gitignore` entry (`# Legacy junctions` / `ARCHI_AI`) confirms this was a deliberate local directory-junction convention on the maintainer's machine, never documented for outside readers.

**Fixed:**
- `scripts/train_qlora.py` + `configs/qlora_experiment.yaml` (the prototype with hardcoded paths) were moved, unmodified, to `docs/history/legacy_qlora_prototype/` with a README explaining why, and `experiment_package/train_qlora.py` — which already resolves every path relative to its own package root — was designated the single canonical, portable reproduction path. `REPRODUCIBILITY.md` and `docs/research/QLORA_PIPELINE.md` were updated to point to it.
- The wider `ARCHI_AI/`-junction convention used by `dataset_tools/experiments/micro_pilot/` and the standalone audit scripts was **documented, not blindly rewritten** — see `DATASET.md` §6 for the reasoning. Rewriting a dozen files that directly produced the headline checkpoint/Gold-Set results, without the private data available to verify the rewrite didn't change behavior, was judged riskier than being explicit about the current requirement (create the documented directory/symlink layout) and tracking the real fix (path parameterization matching `dataset_tools/master_pipeline/config.py`, which already does this correctly) as follow-up work in `ROADMAP.md`.
- `dataset_tools/master_pipeline/` (the module that actually built Master Dataset v2, and the one covered by passing tests) was already portable — it resolves paths relative to the repo root via `Path(__file__).resolve()`. This was verified, not assumed.

---

## 3. P1 Findings — Status

| Finding | Status | What was done |
| :--- | :--- | :--- |
| EVALUATION.md incomplete/truncated | Partially confirmed | The file was not literally truncated, but lacked the required statistical caveat on the 100% accuracy figure, conflated "review queue" into the 65,342 total, and used an imprecise "Generalization Gap" label. Rewrote with a Dataset/Split Context section, an explicit §3.2 "Why '100% Accuracy' Is Not a Robustness Proof" section, and an Artifact Availability section. See `EVALUATION.md`. |
| "100% accuracy" presented without context | Confirmed | Fixed — see above. The 99-positive/1-negative imbalance, the 99% trivial-baseline floor, and the fragility of a specificity estimate from n=1 are now stated explicitly in both `EVALUATION.md` and cross-referenced from `README.md`/`PROJECT_STATUS.md`. |
| Gold Set / checkpoint difficult to access for reproduction | Confirmed | Neither is present in this repository (`.gitignore` excludes `dataset/`, `*.pt`, `outputs/`). This was previously implied but not stated plainly. `EVALUATION.md` §4 and `REPRODUCIBILITY.md` §2 now say **NOT PUBLIC** explicitly for each artifact, with the reason. |
| Potential issue with `accel` dependency | Partially confirmed, different issue than the name suggested | No literal broken `accel` import exists. The real issues found: (1) `requirements.txt`/`pyproject.toml` were missing `shapely`, `pyarrow`, and `ifcopenshell` entirely, even though `dataset_tools` imports them unconditionally — this made test collection fail outright; (2) `accelerate` is loosely pinned (`>=0.30.0`) at the top level but exactly pinned (`==1.15.0`) in `experiment_package/requirements.txt`, with no explanation of which to trust for exact reproduction. Both fixed — see §4. |
| Git history incomplete/inconsistent | Confirmed | The repository has exactly one commit; there is no incremental history for Phases 0–4. This is now stated explicitly in `docs/history/project-history.md` §4 ("Git History Limitation") instead of being left for a reader to notice on their own. No artificial history was fabricated. |
| ARCHI-AI branding residue | Confirmed, narrowly | Fixed in document titles/prose (`experiment_package/README.md`, `docs/research/QLORA_PIPELINE.md`) where it was simple leftover branding. Historical scientific identifiers (`ARCHI-AI-P4-005`, `ARCHI-AI-P4-GOLD-001`, etc.) and the `ARCHIVisionDataset` class name in active code were deliberately left unchanged — renaming identifiers or code symbols was out of scope and risked breaking traceability or working code without a way to verify the change. |
| Two divergent `train_qlora.py` implementations | Confirmed | Diffed both. `experiment_package/train_qlora.py`'s software stack (`torch==2.6.0`, `transformers==5.17.0`, `peft==0.21.0`, `bitsandbytes==0.50.2`) matches exactly what `EXPERIMENTS.md` reports for the actual VLM PoC run, confirming it is the script that produced the published results. `scripts/train_qlora.py` used hardcoded local paths and does not match the reported stack — archived as historical (§2.2). |
| Absence of CI/CD | Confirmed | Added `.github/workflows/tests.yml`: an install/import smoke test, a hard-gated job running the two test files verified to pass without the private dataset (`test_audit_validators.py`, `test_master_pipeline.py`), and an informational (non-blocking) job running the full suite, labeled as such — a full-suite hard gate would be permanently and misleadingly red given the private-data dependency (§4). |
| "generalization gap" / "improvement" terminology | Confirmed | "Generalization Gap" (Validation MAE → Gold MAE difference) renamed to "Validation → Gold Set MAE Difference" with an explanatory footnote distinguishing it from a classical train/test generalization gap, in `README.md`, `EVALUATION.md`, and `EXPERIMENTS.md`. The "+98.14%" figure is now explicitly labeled as an arithmetic fact about two MAE values, not an independent generalization claim. |
| Ambiguities about splits | Confirmed | The 53,720/5,724/5,898/1,563 figures were presented as if additive (implying 66,905 total) without stating that the 1,563-item review queue is isolated and excluded from the certified 65,342 total. Fixed in `README.md`, `PROJECT_STATUS.md`, and `EVALUATION.md`, all now cross-referencing `DATASET.md` §2 as the source of truth. |
| Truncated SHA256 in a configuration/doc | Confirmed | `README.md`'s Current Status table showed `81561fae5b524fa2...` (truncated) for the Gold Set V3 manifest hash while the full hash appeared correctly elsewhere. Replaced with the full 64-character hash, matching all other occurrences. |
| "Academic Research Only" license wording too vague | Confirmed | Added a footnote in `DATASET.md` clarifying this is the maintainer's paraphrase of upstream terms (non-commercial research use, no raw redistribution), not an SPDX identifier, and that a contributor must consult the actual upstream license text rather than rely on the paraphrase. |

---

## 4. Findings Not In The Prior Audit

These were found only by actually installing the package and running the test suite — a static documentation read would not surface them:

1. **`pip install -e .` failed outright** on a completely fresh checkout with "Multiple top-level packages discovered in a flat-layout" — `pyproject.toml` had no explicit package configuration, and setuptools' auto-discovery flagged `configs/`, `dataset/`, `evaluation/`, `test_images/`, `dataset_tools/`, `experiment_package/` as ambiguous candidates. **Fixed:** added `[tool.setuptools.packages.find]` restricting the installable package to `dataset_tools*` and `evaluation*`. Verified working.
2. **Undeclared dependencies:** `shapely`, `pyarrow`, and `ifcopenshell` are imported unconditionally by `dataset_tools/preprocessing/` and `dataset_tools/resplan/` but were absent from `requirements.txt` and `pyproject.toml`, so test collection failed with `ModuleNotFoundError` before ever reaching a real test. **Fixed:** added to both files, plus a new `dataset` extras group in `pyproject.toml`.
3. **A genuinely broken, orphaned test import:** `tests/test_dataset_infra.py` imports `dataset.master.schema.models.MasterAnnotation` — a module that does not exist anywhere in this repository (confirmed by search) and was evidently never migrated from a pre-`dataset_tools` local layout. This is not a missing-data issue (unlike the rest of §5 below); the class definition itself is absent from version control. **Fixed conservatively:** wrapped in a guarded `pytest.skip(..., allow_module_level=True)` with an explanation, rather than fabricating the missing schema module. Not inventing that module was a direct application of the "never invent" rule governing this remediation.
4. **Package build artifacts were not gitignored** (`*.egg-info/`, `build/`, `dist/`) — every `pip install -e .` a contributor runs would leave untracked clutter. Fixed in `.gitignore`.
5. **The "99/99 passing tests" claim is only true in the maintainer's full local environment.** On a fresh clone with no private dataset present, after fixing items 1–2 above, the suite yields approximately **35 passed / 19 failed / 38 errored / 1 module skipped** — all 57 non-passing results trace to files under `dataset/...` that are intentionally not redistributed (per `DATASET.md`'s own Data Access Policy), except the one skipped module (item 3). This was not previously stated anywhere. **Fixed:** `REPRODUCIBILITY.md` §4 now documents this breakdown in full, and the README badge/table entries were reworded to stop implying a fresh clone gets 99/99.
6. **`experiment_package/dataset/` does not exist**, even though `experiment_package/README.md` documents its expected structure (20 train / 5 validation examples, 25 photographs). The VLM QLoRA dry-run command therefore cannot currently be executed by an external researcher as-is. Documented explicitly in `REPRODUCIBILITY.md` §3.
7. **The systemic `ARCHI_AI/`-prefixed path convention** described in §2.2 — larger in scope than the single file the prior audit named.

---

## 5. What Remains Open (Honestly Stated)

This remediation did not, and could not, resolve everything — some of what remains open requires decisions or data outside the scope of a documentation/code-hygiene pass:

- **License selection itself** is a decision for the project owner (EncoreZaan), not something this remediation can or should make. It remains TBD.
- **The Gold Set V3 manifest and the `ARCHI-AI-P4-005` checkpoint are not public.** Making them public — or formally deciding not to — is a maintainer decision with real legal/scientific weight (dataset licensing, model release policy) that this remediation does not make on the maintainer's behalf.
- **The `ARCHI_AI/`-prefixed path convention in `dataset_tools/experiments/micro_pilot/`** is documented, with a working manual workaround, but not rewritten to be automatically portable — see §2.2 and `ROADMAP.md`.
- **Most of the automated test suite still cannot run against a fresh public clone**, because it correctly validates a private dataset corpus that is not redistributed. This is a consequence of the (reasonable) data access policy, not a defect to "fix" by publishing restricted data.
- **`Pre-Training Gate` remains `CONDITIONAL` / `TRAINING_ALLOWED: NO`, and DSpark remains `PLANNED`.** Neither was touched — improving documentation quality is not evidence of new scientific readiness, and this remediation did not treat it as such.

---

## 6. Updated Verdict

**PUBLICATION READINESS: YELLOW → GREEN-WITH-DOCUMENTED-LIMITATIONS.**

The specific P0 blockers named in the prior audit (license/open-source contradiction, hardcoded legacy paths preventing external reproduction) are resolved for the code and documentation that ship in this repository, and the packaging bug that would have stopped *any* external researcher at `pip install -e .` — not previously identified — is also fixed and verified. The repository is no longer internally contradictory about its licensing status, and no longer silently claims reproducibility it cannot deliver: every gap between what is documented and what is actually runnable/public (Gold Set, checkpoint, the `experiment_package/dataset/` example set, most of `tests/`, the micro-pilot scripts' path convention) is now stated plainly, in the relevant document, with a reason.

This is not a claim that everything is reproducible — a meaningful fraction of the experimental pipeline still depends on private data and on a manual local directory convention. It is a claim that the repository now tells the truth about which parts those are, rather than presenting a facade of full reproducibility. That distinction is the standard this remediation was held to throughout.
