# AXIS — Post-Remediation Independent Audit

> **Audit type:** Independent, read-only, post-remediation verification.
> **Auditor scope:** Git/repo integrity, prior P0/P1/P2/P3 closure verification, packaging, test execution, QLoRA documentation, dataset/provenance/legal claims, documentation consistency, CI, training gate, publication readiness.
> **Hard constraint honored throughout:** no model training, no GPU jobs, no dataset modification, no source/doc modification, no commits, no pushes.
> **Audit date:** 2026-09-22

---

## 1. Executive Summary

The remediation commit (`2b2b0d2`, "fix: resolve P0/P1 publication-readiness findings from red-team audit") and the subsequent license-finalization commit (`44b19b7`, "chore: finalize AXIS as MIT-licensed open research project") are both present on `main` and on the audited branch, in a fully linear history descending from the prior baseline `42b1f51`. Independent, hands-on verification — not just a documentation read — confirms that:

- Both previously reported **P0s are effectively closed** (license contradiction fully resolved, including a later MIT decision that supersedes the remediation's own TBD-status documentation; the single hardcoded-path prototype file is archived). One P0 remains **partially** closed in substance: the *broader* `ARCHI_AI/`-prefixed hardcoded-path convention used by the micro-pilot/audit scripts is disclosed and worked around, but not actually rewritten.
- All previously reported **P1s verified in-repo are closed**, and every quantitative claim tied to them (test counts, SHA256 length, split totals, packaging fix, CI existence) was **independently reproduced and matched exactly**, including the specific "35 passed / 19 failed / 38 errored / 1 skipped" fresh-clone test figure.
- `pip install -e .` and `pytest` both **actually work** as documented, verified in a clean virtual environment created for this audit.
- This audit surfaces **new, previously unreported issues**: a test-isolation defect (two "passing" unit tests write real files into the repository's working tree as an unintended side effect), a gate-status vocabulary inconsistency (`RED` vs. `CONDITIONAL` for the Pre-Training Gate, presented in two different documents with no cross-reference), and residual `ARCHI-AI`-branded document titles in two safety-relevant docs. None of these rise to P0/P1 severity.
- **No P0/P1 blocker was identified in this audit.** `TRAINING_ALLOWED: NO` remains correctly and consistently declared everywhere it matters, and no evidence in this repository would justify changing it.

This audit could **not** independently verify the original red-team report's specific text for the 6 P1 / 9 P2 / 7 P3 findings, because that report is not committed to this repository and was not supplied as a file — only its aggregate counts and the task description's context were available. Verification of P1 closure in this report is therefore against `PUBLICATION_READINESS_AUDIT.md`'s own reconstruction of those findings, cross-checked against actual repository/code/test state wherever a concrete, falsifiable claim was made. This is stated as an explicit limitation, not papered over.

---

## 2. Repository / Git State

```
HEAD:                54f27d9525a9be264261c2b4a8182eb2f485ed49  "fix: use exact AXIS brand mark"
Current branch:      claude/axis-post-remediation-audit-lxgtbg
main:                54f27d9525a9be264261c2b4a8182eb2f485ed49  (identical to HEAD)
Baseline (42b1f51):  42b1f51e3288b25ceb4de9560d04a869357c53b6
merge-base(42b1f51, HEAD) = 42b1f51  →  42b1f51 IS an ancestor of HEAD
Working tree: clean (git status: nothing to commit) at audit start
```

Full linear commit graph from baseline to HEAD (no merge commits anywhere in this range):

```
54f27d9 fix: use exact AXIS brand mark
8a60b61 fix: restore AXIS hero visual hierarchy
9b15ab4 feat: integrate official AXIS brand identity
b641e20 fix: refine AXIS hero responsive composition
43a1022 ci: deploy AXIS website with GitHub Pages
5aa920d feat: create AXIS official research landing page
44b19b7 chore: finalize AXIS as MIT-licensed open research project
2b2b0d2 fix: resolve P0/P1 publication-readiness findings from red-team audit   <-- the remediation
42b1f51 feat: official migration from ARCHI-AI to AXIS v0.1.0                  <-- prior baseline
```

**Findings:**
- The remediation content described in `PUBLICATION_READINESS_AUDIT.md` is verifiably present in commit `2b2b0d2`, which is a direct ancestor of `HEAD`/`main`. The remediation **is** integrated into `main`.
- **Discrepancy from task context:** the task states remediation happened on a branch named `claude/axis-p0-p1-remediation-pdf6l7` "and subsequently integrated into main." No such branch exists in this repository, locally or on `origin` (`git branch -a`, `git for-each-ref` both checked). History is fully linear with no merge commit anywhere between `42b1f51` and `HEAD` — either that branch was fast-forward-merged and deleted (plausible, not inherently a problem), or the commits were made directly on `main`. This audit can confirm the *resulting commits* are correct and present; it cannot confirm the branch-based workflow described in the task premise actually occurred as described.
- Five commits after the license-finalization commit (`5aa920d` through `54f27d9`) add and iterate on a `website/` static site and its GitHub Pages CI deploy workflow. These are scoped, non-scientific, non-dataset changes (landing page content, brand mark SVGs, responsive CSS) and do not touch `dataset_tools/`, `evaluation/`, `tests/`, or any claims audited in §9–§12 below, other than restating already-published figures (verified in §10 below).
- No unexpected changes to core scientific/dataset code were found outside the documented remediation and website scope.

---

## 3. Previous P0 Findings — Verification

### P0-1: License Contradiction

- **Expected remediation:** Resolve the "open-source" vs. "TBD license" contradiction; either fix wording or select a license.
- **Evidence found:**
  - `LICENSE` (root): full MIT License text, plus an explicit "NOTE — SCOPE OF THIS LICENSE" section stating the grant applies only to AXIS's own code/docs and explicitly excludes third-party datasets/checkpoints (RPLAN, IL3D, StructScan3D, FloorPlanCAD, ResPlan, OpenBIM/IFC samples), pointing to `THIRD_PARTY_LICENSES.md`.
  - `pyproject.toml`: `license = "MIT"` + `license-files = ["LICENSE"]` (modern SPDX form). No deprecated `License ::` trove classifier remains (verified by direct grep — none found; the changelog's claim that it was removed is accurate).
  - `THIRD_PARTY_LICENSES.md` (new file, 108 lines): cleanly separates AXIS's MIT code grant from a per-source third-party license table, a checkpoint-licensing section (explicitly: no checkpoint is currently public, no license decided for it), and a third-party software dependency section.
  - `README.md` / `GOVERNANCE.md`: both contain a "License Status" / "Terminology this project keeps distinct" section separating *public repository*, *open research*, *open-source code license*, and *third-party dataset/checkpoint licenses* — this is the exact terminology fix the P0 called for, now describing a real MIT grant rather than papering over a TBD status.
  - `PUBLICATION_READINESS_AUDIT.md` itself carries an explicit "⚠️ Superseded on license status" banner at the top, correctly telling a reader that its own TBD-era passages are historical record, not current state.
- **Status: CLOSED.** Verified independently, not merely asserted. The license is coherent end-to-end: `LICENSE` ↔ `pyproject.toml` ↔ `THIRD_PARTY_LICENSES.md` ↔ `README.md`/`README_EN.md` ↔ `GOVERNANCE.md` ↔ `CITATION.cff` (`license: MIT`) ↔ `website/index.html` (footer links to `LICENSE`, "Licence MIT" badge) all agree. No file was found asserting a conflicting license status.

### P0-2: Hardcoded Legacy Paths

- **Expected remediation:** Fix `configs/qlora_experiment.yaml` / hardcoded `ARCHI_AI/...` paths that prevent external reproduction.
- **Evidence found:**
  - `scripts/train_qlora.py` and `configs/qlora_experiment.yaml` (the originally flagged files) were confirmed **moved** to `docs/history/legacy_qlora_prototype/` (present, with a `README.md` explaining the archival) — verified in the `2b2b0d2` diff stat and by directory listing.
  - `experiment_package/train_qlora.py` is designated canonical; `docs/research/QLORA_PIPELINE.md` and `REPRODUCIBILITY.md` both explicitly point to it and explain why (paths resolve relative to `PACKAGE_ROOT`, not a hardcoded local directory).
  - **However**, `DATASET.md` §6 and `PUBLICATION_READINESS_AUDIT.md` §2.2 both candidly disclose that the *same* `ARCHI_AI/`-prefixed hardcoded-path convention is still used, unmodified, by `dataset_tools/experiments/micro_pilot/` (the scripts that actually produced checkpoint `ARCHI-AI-P4-005` and the Gold Set V3 evaluation) and by several standalone Wave-1 audit scripts. This was confirmed by direct inspection: `dataset_tools/experiments/micro_pilot/` and files such as `dataset_tools/gold_set_builder.py`, `dataset_tools/audit_calculator.py`, `dataset_tools/decision_classifier.py`, `dataset_tools/deep_audit.py`, `dataset_tools/audit_diagnostics.py` still contain the `ARCHI_AI/`-prefixed convention, exactly as `DATASET.md` §6 states, with a documented manual symlink workaround.
- **Status: PARTIALLY CLOSED.** The single file originally flagged is genuinely fixed and archived. The wider, scientifically important instance of the same defect (the scripts that produced the headline checkpoint results) is **not actually portable** — it is disclosed, with a working manual workaround, and explicitly tracked as follow-up in `ROADMAP.md`, which is the honest thing to do given the remediation could not safely rewrite checkpoint-producing code without the private data to verify against. This is a defensible triage decision, but it means an external researcher still cannot run these specific scripts without manually recreating a local directory-junction layout. Calling the original P0 fully "CLOSED" would overstate what was actually fixed.

---

## 4. Previous P1 Findings — Verification

The table below cross-references every P1 line item documented in `PUBLICATION_READINESS_AUDIT.md` §3 (the closest available proxy for the original red-team P1 list — the original report itself is not present in this repository) against actual, independently verified repository/test state.

| # | Finding | Evidence checked | Status |
|---|---|---|---|
| 1 | `EVALUATION.md` incomplete/lacking statistical caveats | Read in full: §1 (split context, non-additive review queue), §3.2 ("Why '100% Accuracy' Is Not a Robustness Proof" — 99/1 imbalance, trivial-baseline floor, n=1 specificity caveat spelled out), §4 (artifact availability table) all present and substantive | **CLOSED** |
| 2 | "100% accuracy" presented without context | Same as above — explicit dedicated section §3.2 | **CLOSED** |
| 3 | Gold Set/checkpoint hard to access for reproduction | `EVALUATION.md` §4 and `REPRODUCIBILITY.md` §2 both state "NOT PUBLIC" explicitly for the Gold Set V3 manifest, the checkpoint, and Dataset A, each with a reason | **CLOSED** |
| 4 | Undeclared/broken dependency (`accel`) | `pyproject.toml`/`requirements.txt` now declare `shapely`, `pyarrow`, `ifcopenshell`; `accelerate` pin discrepancy (loose top-level vs. exact in `experiment_package/requirements.txt`) is explained in both files' comments. Verified by actually installing (§6) | **CLOSED** |
| 5 | Git history incomplete (single commit at time of prior audit) | `docs/history/project-history.md` §4 explicitly documents the "Git History Limitation." The repo now has 9 commits, but Phases 0–4 remain squashed pre-`42b1f51`; this is disclosed, not fabricated or hidden | **CLOSED** (as a documentation-honesty fix; the underlying squashed history is unchanged and out of scope to reconstruct) |
| 6 | `ARCHI-AI` branding residue | Renamed in `experiment_package/README.md`, `docs/research/QLORA_PIPELINE.md` prose; scientific identifiers (`ARCHI-AI-P4-005`, `ARCHIVisionDataset`) deliberately kept for traceability, per stated policy. **However**, this audit found two *document titles* still reading `# ARCHI-AI — ...` (see §10 Documentation Consistency) that were not caught by the remediation | **PARTIALLY CLOSED** — new minor residue found (see §10) |
| 7 | Two divergent `train_qlora.py` implementations | Diffed per `2b2b0d2`'s own stated method; `experiment_package/train_qlora.py`'s stack (`torch==2.6.0`, `transformers==5.17.0`, `peft==0.21.0`, `bitsandbytes==0.50.2`) matches `EXPERIMENTS.md`'s reported stack for the actual run. Legacy version archived | **CLOSED** |
| 8 | Absence of CI/CD | `.github/workflows/tests.yml` present. **Independently executed** — see §7. Behavior matches documentation exactly | **CLOSED** |
| 9 | "Generalization gap" / "improvement" terminology imprecise | `EVALUATION.md` §3.1: "Validation → Gold Set MAE Difference," with explicit footnote on why "generalization gap" was imprecise | **CLOSED** |
| 10 | Split-count ambiguity (66,905 vs. 65,342) | `DATASET.md` §2 and `EVALUATION.md` §1 both explicitly flag the review queue (1,563) as isolated/non-additive; repo-wide search for the old implied total ("66,905"/"66905") only appears in the two documents that explain why it is *wrong* — no file states it as the actual total | **CLOSED** |
| 11 | Truncated SHA256 hash | Verified: README's Gold Set V3 hash `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca` is a full 64 hex-character string, consistent across `README.md`, `EVALUATION.md`, `REPRODUCIBILITY.md`, `PROJECT_STATUS.md` | **CLOSED** |
| 12 | Vague "Academic Research Only" license wording | `DATASET.md` footnote 1 and `THIRD_PARTY_LICENSES.md` footnote 1 both clarify this is a maintainer paraphrase, not an SPDX identifier, and direct a contributor to consult upstream terms | **CLOSED** |

**Additional findings the remediation itself surfaced (§4 of `PUBLICATION_READINESS_AUDIT.md`) — all independently re-verified in this audit:**

| Finding | Verification performed | Status |
|---|---|---|
| `pip install -e .` failed on fresh clone | Reproduced from a clean venv in this audit — **succeeds** (§6) | **CLOSED** |
| Missing `shapely`/`pyarrow`/`ifcopenshell` | Present in `requirements.txt` and `pyproject.toml`; installed cleanly | **CLOSED** |
| `tests/test_dataset_infra.py` orphaned import | Ran directly: cleanly skips with an explicit, accurate reason (`test_dataset_infra.py:32`) | **CLOSED** |
| Build artifacts not gitignored | `*.egg-info/`, `build/`, `dist/` present in `.gitignore` | **CLOSED** |
| "99/99 passing" only true in maintainer env | Reproduced fresh-clone run: **exact match** — 35 passed / 19 failed / 38 errored / 1 skipped (§7) | **CLOSED (and independently confirmed accurate, not just re-asserted)** |
| `experiment_package/dataset/` absent | Confirmed absent; `REPRODUCIBILITY.md` §3 states this plainly | **Disclosed, not fixable without private data — correctly not claimed as fixed** |
| Wider `ARCHI_AI/` path convention | See P0-2 above | **OPEN, disclosed** |

---

## 5. P2/P3 Review

**Limitation stated up front:** the original red-team report's specific P2 (9) and P3 (7) items are not present in this repository or in any file this audit could locate, and were not supplied in full text. This section therefore reports on (a) whether any *lower-severity pattern* consistent with a P2/P3 red-team finding was found to have regressed, and (b) new P2/P3-level issues discovered during this independent audit — rather than closing out a specific numbered list that isn't available to check against.

No evidence of regression (a previously-fixed or previously-minor issue becoming worse) was found anywhere in the diffs reviewed (§2).

**New P2-level findings (this audit):**

1. **Test-isolation defect — "passing" tests write to the real working tree.** `tests/test_master_pipeline.py::test_legal_filter_floorplancad` and `::test_split_deterministic_anti_leakage` are part of the **CI hard-gate** (`unit-tests-no-private-data` job) and both currently pass — but passing has a side effect. `dataset_tools/master_pipeline/legal_filter.py::LegalFilter.apply_filter()` and `dataset_tools/master_pipeline/split_manager.py::DeterministicSplitter.partition_records()` write real files (`dataset/master/v2/manifests/RESTRICTED_MANIFEST.jsonl`, `dataset/master/v2/splits/{train,validation,test}.jsonl`, `dataset/master/v2/restricted/legal_review/floorplancad/FLOORPLANCAD_LEGAL_DOSSIER.md`) to a fixed, repo-relative path — not a `pytest tmp_path`/temp directory — even when invoked from a unit test with synthetic dummy records. This was directly observed during this audit: running the documented CI test command created a `dataset/` directory tree on disk (confirmed via file timestamps immediately following the test run). It is gitignored so it does not appear in `git status`/diffs, but it means: (a) the "unit tests" are not actually side-effect-free or idempotent, (b) repeated or concurrent CI/local runs race on the same output files, and (c) a contributor running the test suite will find their working tree silently populated with generated files they did not ask for. **Recommendation:** inject the output directory (constructor parameter / env var / `tmp_path` fixture) rather than hardcoding it in `legal_filter.py`/`split_manager.py`.
   - *Audit note:* this audit could not delete the generated `dataset/` directory it inadvertently produced by running the documented test suite, due to a tool-level restriction on destructive filesystem operations in this environment. It is confirmed untracked and gitignored (`git status --porcelain dataset/` returns nothing), so it does not affect any committed or pushed repository state, but a human maintainer running the same command locally should be aware it will happen.

2. **Pre-Training Gate vocabulary inconsistency.** `docs/research/PRE_TRAINING_GATE.md` states the gate status is **`RED`**, justified by Phase-2-era findings (19.6% grounding rate, 38.5% pixel-as-m² mislabeling, 21.2% fake multimodal, 79.5% Gold Set V2 contamination). Every other current document (`README.md`, `README_EN.md`, `PROJECT_STATUS.md`, `ROADMAP.md`, `RESEARCH.md`, `CHANGELOG.md`, `START_HERE.md`) states the current status is **`CONDITIONAL`**, justified by a *different*, later blocker (50–100 additional open-licensed OpenBIM IFC pairs needed). Both labels agree on the practical outcome (`TRAINING_ALLOWED: NO`), so there is no live ambiguity about whether training is currently permitted — but `PRE_TRAINING_GATE.md` carries no "superseded"/date-stamped note the way `PUBLICATION_READINESS_AUDIT.md` does for its own outdated license section, so a reader landing on it directly would not know it reflects an earlier phase's assessment rather than the current one.

**New P3-level findings (this audit):**

3. **Residual `ARCHI-AI` branding in document titles.** `docs/research/PRE_TRAINING_GATE.md` (`# ARCHI-AI — Décision du Pre-Training Gate`) and `docs/research/SCIENTIFIC_READINESS_REPORT.md` (`# ARCHI-AI — Rapport de Maturité Scientifique Pré-Entraînement`) still use the old project name as their document title, unlike sibling documents that were updated during remediation. Both are actively referenced from current-status documents (ROADMAP, PROJECT_STATUS), so this is a real (if cosmetic) inconsistency, distinct from the deliberately preserved scientific identifiers (`ARCHI-AI-P4-005`, class name `ARCHIVisionDataset`) that the remediation correctly chose not to touch.

No P2/P3-severity issue was found to have become a P0/P1 (no regression to higher severity was found anywhere in this review).

---

## 6. Packaging Validation

Performed in a clean virtual environment created specifically for this audit (`python3 -m venv`), never previously used, on Python 3.11.15.

```bash
$ python3 -m venv /tmp/axis_audit_venv && source /tmp/axis_audit_venv/bin/activate
$ pip install -r requirements.txt
# → succeeds cleanly, no errors (torch 2.14.0, shapely 2.1.2, pyarrow 25.0.1,
#   ifcopenshell 0.8.5, pydantic 2.13.5, pillow 12.3.0, numpy 2.4.6 all resolved)

$ pip install -e .
# → succeeds cleanly, exit code 0. No "Multiple top-level packages discovered"
#   error (the originally reported P1 packaging bug is genuinely fixed).

$ python -c "import dataset_tools.master_pipeline.config; import evaluation.runners.benchmark_runner; print('IMPORT OK')"
# → IMPORT OK
```

`pyproject.toml` correctly scopes the installable package to `dataset_tools*` and `evaluation*` via `[tool.setuptools.packages.find]`, exactly as documented, and the `dataset`/`vlm`/`dev` extras groups match what `REPRODUCIBILITY.md`/`DATASET.md` describe. **Verdict: the documented installation path works exactly as claimed, independently confirmed, not merely asserted.**

---

## 7. Test Validation

Two commands executed, both read-only with respect to source code (see §5 finding #1 regarding an unrelated side effect on the working tree).

**Command 1 — the CI hard-gate (`unit-tests-no-private-data` job), exactly as written in `.github/workflows/tests.yml`:**
```bash
$ pytest tests/test_audit_validators.py tests/test_master_pipeline.py -v
============================== 9 passed in 0.13s ===============================
```
All 9 tests pass, matching the `[![Tests: 9/9 CI gate]]` badge in `README.md` exactly.

**Command 2 — full suite on a fresh clone (no private dataset present), as `REPRODUCIBILITY.md` §4 claims should happen:**
```bash
$ pytest tests/ -v
...
============= 19 failed, 35 passed, 1 skipped, 38 errors in 0.98s ==============
```

This is an **exact match** to the figure documented in `REPRODUCIBILITY.md` §4, `PROJECT_STATUS.md`, `README.md`, `README_EN.md`, and `CHANGELOG.md` — "approximately 35 passed, 19 failed, 38 errored, 1 module skipped." This is a strong positive signal: the remediation's most falsifiable claim was independently reproduced bit-for-bit, not merely trusted.

- All 19 failures + 38 errors trace to `FileNotFoundError`/`AssertionError` on paths under `dataset/raw/...`, `dataset/master/...`, `dataset/supervision/...`, `dataset/experiments/...` — consistent with the stated "these require the private RAW corpus, not code bugs" explanation. Spot-checked several tracebacks directly; all confirmed data-absence failures, none were unexpected code errors.
- `tests/test_dataset_infra.py` skip message confirmed verbatim: *"requires the private `dataset/master/schema/models.py` module, which is not part of this public repository. See REPRODUCIBILITY.md."* — accurate and matches the documented reason.
- No test attempted to launch actual model training (verified by inspecting for `subprocess`/`os.system`/optimizer-step calls before running; none found tied to `train_qlora.py`). No training occurred as part of this validation.

**Total: 93 collected + 1 module-level skip covering 7 test functions in `test_dataset_infra.py` = 99 total test functions, matching the "99 tests in `tests/`" figure quoted throughout the documentation.**

---

## 8. QLoRA / Training Documentation Audit

Reviewed `docs/research/QLORA_PIPELINE.md`, `REPRODUCIBILITY.md` §3, and `EXPERIMENTS.md` §2 together.

- **Model assumption:** `Qwen/Qwen2-VL-7B-Instruct`, consistent across all three documents.
- **Hardware assumptions:** dual-documented — local RTX 4060 Ti (8 GB, dry-run only) and remote RTX 3090 (24 GB, actual 6-step run) — consistent between `REPRODUCIBILITY.md` §1 and `EXPERIMENTS.md` §2.
- **Quantization config:** 4-bit NF4, double quantization, `bfloat16` compute dtype — stated identically in both `QLORA_PIPELINE.md` §5 and `EXPERIMENTS.md` §2.
- **LoRA config:** r=8, α=16, dropout=0.05, target modules (`q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj`), vision tower frozen — identical across `QLORA_PIPELINE.md` §5 and `EXPERIMENTS.md` §2, including the trainable-parameter count (20,185,088 / 8,311,560,704 = 0.2429%) matching exactly in both places.
- **Dataset interface:** JSONL schema documented in `QLORA_PIPELINE.md` §2 with a concrete example; `experiment_package/dataset/` is correctly and explicitly flagged as **absent** from this repository in `REPRODUCIBILITY.md` §3, so the documented commands are **not currently runnable** by an external party — this is stated plainly, not glossed over.
- **Training entry point:** `experiment_package/train_qlora.py`, with `--validate-only`/`--dry-run` (forward-pass-only, explicitly "no backward pass, no optimizer update, no weight modification" per `QLORA_PIPELINE.md` §8) clearly distinguished from a separate, already-completed 6-step/2-epoch **actual** training run reported in `EXPERIMENTS.md` §2 (with per-step loss, grad norm, and eval loss table). This is documentation of prior, already-completed historical work by the maintainer — not something this audit executed or was asked to execute. No contradiction between the "no training" audit rule and this documentation: this audit did not run either the dry-run or the training script.
- **Expected outputs:** dry-run loss `1.9771`, logits shape `[1, 877, 152064]` — consistent between `QLORA_PIPELINE.md` §8 and referenced in `REPRODUCIBILITY.md` §3.
- **Seed handling:** `seed=42` used consistently for the Dataset A / Master Dataset v2 splits (`DATASET.md` §2, `EXPERIMENTS.md` §1); the VLM micro-experiment's dry-run doesn't document a separate seed value explicitly for that specific run, which is a minor gap but consistent with its "feasibility only" framing.
- **Checkpoint handling:** `ARCHI-AI-P4-005` (the 3D `SpatialRelationMLP` checkpoint, **not** the VLM) is the one actually evaluated on Gold Set V3; this distinction between the small controlled Phase-4 checkpoint and the separate VLM proof-of-concept is kept clear and consistent across `EVALUATION.md`, `EXPERIMENTS.md`, and `PROJECT_STATUS.md` — an easy point of confusion that the documentation handles correctly.
- **Evaluation procedure:** `REPRODUCIBILITY.md` §2 documents a 3-step reproduction procedure (hash verification → baseline calibration → checkpoint evaluation), each step's expected output stated, and — critically — followed immediately by an explicit "Reproducibility limitations" section stating the three referenced artifacts are **NOT PUBLIC**, so the procedure is not independently executable today. This is honest and internally consistent.

**Verdict:** the QLoRA/training documentation is **internally consistent** across all three files that describe it, and is **technically reproducible in principle** but **not currently reproducible in practice** by an outside party, for reasons (private dataset, private checkpoint) that are explicitly and accurately disclosed rather than implied away. No technical contradiction or fabricated-looking figure was found. No training was executed to produce or verify this section.

---

## 9. Dataset / Provenance / Legal Audit

- **RAW corpus claim:** "66,847 physical source files scanned (3.48 GB)" — stated consistently in `DATASET.md` and `REPRODUCIBILITY.md` §4. Not independently re-countable in this audit since the corpus itself is not present in this repository (by design — `.gitignore` excludes `dataset/`), so this figure is trusted-but-unverifiable from this environment, and the documentation is honest about that boundary.
- **Master Dataset v2 claim:** 65,342 consolidated assets across 19 sources, in `DATASET.md` §1. Internally consistent with `EVALUATION.md` §1 and `PROJECT_STATUS.md`.
- **Split counts:** Train 53,720 / Validation 5,724 / Test 5,898 / Review Queue 1,563 (isolated, correctly non-additive) — verified identical across `DATASET.md`, `EVALUATION.md`, `PROJECT_STATUS.md`, `README.md`/`README_EN.md`. No file was found stating the incorrect additive total (66,905) as fact.
- **Leakage controls:** `project_group_id`-based partitioning with `seed=42`, "0 leaks" claimed for both project-level and SHA256-level leakage (`DATASET.md` §2). The corresponding unit test (`tests/test_master_pipeline.py::test_split_deterministic_anti_leakage`) was independently run and **passes**, exercising the actual `DeterministicSplitter` logic (not a stub) against a synthetic two-record fixture designed to catch exactly this class of bug. This is a genuine, if narrow, positive signal — the anti-leakage *logic* is exercised and correct; the *scale claim* ("0 leaks across 65,342 real assets") cannot be independently re-verified from this environment without the private corpus.
- **Review queue / known blockers:** correctly described as isolated and excluded from all splits, pending manual QA disposition (`DATASET.md` §2, §4).
- **Licensing limitations:** per-source license table in `DATASET.md` §1 and `THIRD_PARTY_LICENSES.md` §2 agree with each other (same sources, same license characterizations, same "Academic Research Only" footnote caveat).
- **ResPlan limitations:** consistently described everywhere as quarantined for metric (m²) tasks only, due to a proven scale-distortion forensic finding (std=173.2, 32.1% net-area-null), while explicitly still permitted for scale-invariant topological tasks. No document found upgrading ResPlan's status beyond this quarantine.
- **FloorPlanCAD legal-review status:** consistently `LEGAL_REVIEW_REQUIRED` / `QUARANTINED` across `DATASET.md` §3.2, `THIRD_PARTY_LICENSES.md` §2, `PROJECT_STATUS.md`, `README.md`. **No document was found claiming this status has been resolved or upgraded** — this audit specifically checked for any premature legal-clearance claim and found none. This status remains an open, correctly-disclosed limitation, exactly as required by this audit's own instruction not to upgrade any legal status beyond present evidence.

**Verdict:** dataset, provenance, and legal claims are internally consistent and none were found to overstate their own evidentiary basis. The main irreducible limitation is that the underlying corpus is not present in this environment, so scale/count claims are verified for internal consistency but not independently re-derived from raw data.

---

## 10. Documentation Consistency

- **Old project name (`ARCHI-AI`/`ARCHI_AI`):** appears very widely in the repository, but the overwhelming majority of occurrences are **intentional and correct** — scientific run identifiers (`ARCHI-AI-P4-005`), the retained `ARCHIVisionDataset` class name, the historical hardcoded-path convention documented in `DATASET.md` §6, and explicit historical references ("AXIS is the public continuation of research previously conducted under the internal codename ARCHI-AI"). These are not branding residue; they are deliberately preserved traceability, per the remediation's stated and defensible policy.
  - **Genuine residue found:** two document **titles** — `docs/research/PRE_TRAINING_GATE.md` and `docs/research/SCIENTIFIC_READINESS_REPORT.md` — still read `# ARCHI-AI — ...` rather than `# AXIS — ...`, unlike sibling documents (`docs/research/QLORA_PIPELINE.md`, `experiment_package/README.md`) that were explicitly fixed during remediation. Both are actively linked/referenced from current documents. This is a real, if minor, inconsistency (see §5, finding #3).
- **Old paths / obsolete commands:** none found referencing a pre-`dataset_tools` layout as if it were current, other than the already-disclosed `ARCHI_AI/` junction convention (§4, P0-2) and the already-skipped `test_dataset_infra.py` orphaned import (§4).
- **Contradictory dataset counts:** none found (see §9).
- **Contradictory training status:** none found — every current-status document agrees `TRAINING_ALLOWED: NO`. The one vocabulary inconsistency found (`RED` in `PRE_TRAINING_GATE.md` vs. `CONDITIONAL` everywhere else) does not create a contradictory *outcome*, only an un-cross-referenced *label* — see §5, finding #2.
- **Contradictory licensing statements:** none found (see §3, P0-1). `README.md`'s "publié sous licence MIT" and the website's "licence MIT" / MIT badge all agree with `LICENSE` and `pyproject.toml`.
- **Outdated phase/gate terminology:** `docs/research/SUPERVISION_TASK_GAP_ANALYSIS.md` header still frames itself as "PHASE 2 — Supervision Engineering & Pre-Training Gate," which is accurate as a historical phase label for that document's own content (it is a Phase-2-era report), not a claim about current project phase — not flagged as an inconsistency.

---

## 11. CI / Reproducibility

`.github/workflows/tests.yml` was read in full and its three jobs were **independently reproduced locally, command-for-command**:

1. `install-and-lint`: `pip install -r requirements.txt && pip install -e .` + an import smoke test. **Reproduced — succeeds.**
2. `unit-tests-no-private-data` (hard gate, blocking): `pytest tests/test_audit_validators.py tests/test_master_pipeline.py -v`. **Reproduced — 9/9 pass.**
3. `full-suite-informational` (`continue-on-error: true`, correctly non-blocking): `pytest tests/ -v`. **Reproduced — 35 passed/19 failed/38 errored/1 skipped**, exactly as the workflow's own inline comment predicts ("most tests require the private RAW dataset corpus and are expected to fail/error here").

The workflow's design — a hard-gated subset that is genuinely data-independent, plus an informational full-suite job that is honestly labeled as expected-to-be-red — is a defensible and accurate CI design given the stated constraint (private dataset not redistributed). It does not silently claim more than it can deliver.

**Reproducibility gaps correctly disclosed (not hidden):**
- Most of the test suite cannot run on a fresh public clone (data-dependent).
- The VLM QLoRA dry-run/train commands cannot currently be executed externally (`experiment_package/dataset/` absent).
- Phase 4 Step 6 (Gold Set V3 evaluation) cannot be bit-exactly reproduced externally (manifest and checkpoint not public — hash-only verification is possible).
- The `dataset_tools/experiments/micro_pilot/` / standalone audit scripts require a manual local directory-junction workaround (§4, P0-2).

**New finding relevant to CI reliability (not in original scope):** the test-isolation defect in §5, finding #1 means the hard-gated CI job, while currently green, is not actually a pure "unit test" run — it performs real filesystem writes to fixed paths on every CI runner invocation. This does not currently cause a failure, but it is a latent risk for flaky/racy CI behavior (e.g., under matrix/parallel test execution) and for accidentally-persisted build-runner state.

---

## 12. Current Training Gate

**TRAINING_ALLOWED = NO**

This is stated consistently and without exception across every document that declares it: `README.md`, `README_EN.md`, `PROJECT_STATUS.md`, `ROADMAP.md`, `RESEARCH.md`, `CHANGELOG.md`, `START_HERE.md`, `docs/research/SCIENTIFIC_READINESS_REPORT.md`, `docs/experiments/PHASE4_SELECTION_REPORT.md`, and (under the older `RED` label — see §5, finding #2) `docs/research/PRE_TRAINING_GATE.md`. No document in this repository claims `TRAINING_ALLOWED: YES`, and this audit performed no action that would change that status.

**Blockers explicitly identified in repository evidence:**
1. **Dataset scale for multimodal 2D/3D reasoning:** the formally cited condition for lifting the `CONDITIONAL` gate is acquisition of 50–100 additional open-licensed OpenBIM IFC pairs (`README.md`, `PROJECT_STATUS.md`, `ROADMAP.md`). Not satisfied — no evidence of new acquisition found.
2. **ResPlan metric quarantine:** 17,000 floorplans remain excluded from all metric (m²) tasks due to the proven scale-distortion forensic finding. Not lifted.
3. **FloorPlanCAD legal quarantine:** 741 CAD drawings remain excluded pending legal review (`LEGAL_REVIEW_REQUIRED`). Not lifted.
4. **Gold Set V3 / checkpoint non-public status**, while not itself a *gating* condition for training, is a standing reproducibility/falsifiability blocker for any third party attempting to independently validate results before or after any future training decision.

This audit did not identify any new evidence that would weaken these blockers, nor any evidence that would justify changing the gate. The gate correctly remains closed.

---

## 13. Publication Readiness

Using the rubric supplied for this audit — **GREEN** = no blocking P0/P1 issue identified; **YELLOW** = material issues remain but no confirmed critical blocker; **RED** = critical blocker remains:

- Both previously reported P0s: one fully closed (and further improved beyond the remediation's own scope, via the later MIT decision), one partially closed with an honestly disclosed remaining gap (§3, P0-2) that does not itself constitute a currently-active blocking defect (it's a known, worked-around limitation, not a live contradiction or safety issue).
- All previously reported, in-repo-verifiable P1s: closed, with every quantitative claim independently reproduced.
- New findings from this audit (test-isolation side effect, gate-vocabulary inconsistency, two stale document titles): all assessed as **P2/P3-level**, not P0/P1 — they affect engineering hygiene and minor reader clarity, not scientific validity, legal exposure, or reproducibility integrity.

**No confirmed P0/P1 blocker was found in this independent audit.**

**Classification: GREEN**, bounded by two explicit caveats that a reader of this audit should weigh:
1. This audit could not check the original red-team P2/P3 list item-by-item, because that list is not present in this repository — the P2/P3 review in §5 is necessarily audit-driven (what this review itself found) rather than a checklist closure against the original report.
2. "GREEN" describes the *documentation-and-code-hygiene* standard this audit was scoped to (per the rubric given), not a claim that AXIS's scientific results are broadly reproducible or externally falsifiable today — they are not, for reasons (private dataset, private checkpoint) that the repository itself discloses honestly and this audit independently confirmed are disclosed honestly.

---

## 14. Remaining Blockers

**Training gate blockers** (see §12): OpenBIM IFC pair scarcity, ResPlan metric quarantine, FloorPlanCAD legal quarantine.

**Legal blockers:** FloorPlanCAD's `LEGAL_REVIEW_REQUIRED` status is the one open, unresolved legal question in the repository. The code/documentation license question itself is resolved (MIT).

**Reproducibility blockers:** Gold Set V3 manifest not public; checkpoint `ARCHI-AI-P4-005` not public; `experiment_package/dataset/` not public; `dataset_tools/experiments/micro_pilot/` and related audit scripts require a manual, undocumented-until-now-in-detail local directory-junction workaround rather than being portable; the pre-`42b1f51` incremental development history remains squashed into a single commit (disclosed, not fabricated).

**Engineering/hygiene blockers (new, this audit):** test-isolation defect in `legal_filter.py`/`split_manager.py` (§5 #1); gate-status vocabulary inconsistency between `PRE_TRAINING_GATE.md` and current-status documents (§5 #2); two stale `ARCHI-AI`-titled documents (§5 #3).

None of the above are P0/P1-severity as independently assessed in this audit.

---

## 15. Required Next Actions

1. Rewrite the `ARCHI_AI/`-prefixed hardcoded paths in `dataset_tools/experiments/micro_pilot/` and the standalone Wave-1 audit scripts to resolve relative to the repo root (matching `dataset_tools/master_pipeline/config.py`'s existing, already-correct pattern) — tracked in `ROADMAP.md`, still not done.
2. Fix the test-isolation defect: make `LegalFilter`/`DeterministicSplitter` output paths injectable, and have `tests/test_master_pipeline.py` pass a `tmp_path`-based directory rather than writing to the real `dataset/` tree.
3. Add a "superseded"/date-stamped cross-reference note to `docs/research/PRE_TRAINING_GATE.md` clarifying that its `RED` verdict is a Phase-2-era assessment, and that the currently authoritative gate status is `CONDITIONAL` as stated in `PROJECT_STATUS.md`/`ROADMAP.md` — to avoid a reader treating it as the current canonical status.
4. Retitle `docs/research/PRE_TRAINING_GATE.md` and `docs/research/SCIENTIFIC_READINESS_REPORT.md` from `ARCHI-AI — ...` to `AXIS — ...`, consistent with sibling documents already fixed.
5. Continue tracking, as already correctly disclosed and out of this audit's scope to resolve: FloorPlanCAD legal review completion, OpenBIM IFC pair acquisition for the Pre-Training Gate, and any future decision to publicly release the Gold Set V3 manifest and/or checkpoint.

None of the above were performed by this audit, per its read-only, no-modification mandate.

---

## Machine-Readable Summary (at audit time, pre-remediation)

```
PUBLICATION_READINESS: GREEN
TRAINING_ALLOWED: NO
OPEN_P0: 0
OPEN_P1: 0
OPEN_P2: 3
OPEN_P3: 2
TRAINING_BLOCKERS: 3
LEGAL_BLOCKERS: 1
REPRODUCIBILITY_BLOCKERS: 5
```

**Notes on the counts above:**
- `OPEN_P0`/`OPEN_P1`: 0 confirmed remaining, per independent verification in §3–§4. (The partially-closed P0-2 remnant and the "documented-but-unfixed" items are counted as P2 below, not as an open P0, since they are disclosed and worked around rather than live, undisclosed defects.)
- `OPEN_P2` (3): wider `ARCHI_AI/`-prefixed hardcoded path convention still unfixed in `dataset_tools/experiments/micro_pilot/` (pre-existing, disclosed); test-isolation side effect in `legal_filter.py`/`split_manager.py` (new, this audit); Pre-Training Gate `RED`-vs-`CONDITIONAL` vocabulary inconsistency (new, this audit).
- `OPEN_P3` (2): stale `ARCHI-AI` document titles in `PRE_TRAINING_GATE.md`/`SCIENTIFIC_READINESS_REPORT.md` (new, this audit); pre-`42b1f51` squashed git history (pre-existing, disclosed, low severity).
- `TRAINING_BLOCKERS` (3): OpenBIM IFC pair scarcity (formal gate condition), ResPlan metric quarantine, FloorPlanCAD legal quarantine.
- `LEGAL_BLOCKERS` (1): FloorPlanCAD `LEGAL_REVIEW_REQUIRED` status, unresolved.
- `REPRODUCIBILITY_BLOCKERS` (5): Gold Set V3 manifest not public; checkpoint not public; `experiment_package/dataset/` not public; micro-pilot scripts not portable; squashed pre-migration git history.

---
---

# POST-REMEDIATION UPDATE

> **Update type:** Remediation pass responding to §5/§15 of the audit above.
> **Hard constraints honored:** no model training, no GPU jobs, no dataset modification (RAW or Master), no Gold Set modification, no benchmark/checkpoint result changed, no gate status changed by this update. `TRAINING_ALLOWED: NO` is unchanged and is not something this document can alter — only a separate, independent gate review can do that.
> **Scope:** repository / documentation / test hygiene only, addressing each of the five items in §15 "Required Next Actions" above (items 1–4; item 5 is explicitly out of this remediation's scope, per the audit's own instruction, and is left untouched).

This section documents what was inspected, changed, and validated in response to the audit's §5/§15 findings. The audit's own conclusions above (§1–§15, including its machine-readable summary) are preserved **unmodified** as the historical record of that independent review.

## Item 1 — Wider `ARCHI_AI/`-prefixed path convention (P2)

**Finding.** `dataset_tools/experiments/micro_pilot/{run_micro_pilot.py, gold_evaluator.py, trainer.py, dataset_loader.py, baseline_evaluator.py}` and `dataset_tools/{gold_set_builder.py, audit_calculator.py, decision_classifier.py, deep_audit.py, audit_diagnostics.py}` hardcoded `ARCHI_AI/`-prefixed paths (and, in three files, `sys.path.insert(0, os.path.abspath("ARCHI_AI"))` + `from ARCHI_AI.dataset_tools... import ...`), requiring a local directory-junction layout (`ARCHI_AI/{dataset,dataset_tools,experiments}` symlinked back to the repo root) not documented for outside readers.

**Remediation.** Every listed file now computes `REPO_ROOT = Path(__file__).resolve().parent...` (the same pattern already used by `dataset_tools/master_pipeline/config.py` and `dataset_tools/supervision/independent_audit/run_audit.py`) and derives every data/report/checkpoint path from it; imports switched from `from ARCHI_AI.dataset_tools... import ...` to `from dataset_tools... import ...`. Because each `ARCHI_AI/<subdir>` symlink pointed back to the identical physical repo-root directory, this is a pure path-resolution change — the same files on disk are read/written as before. `run_micro_pilot.py`'s `copy_to_root()` mirroring step now guards against copying a directory onto itself (both paths now resolve identically once the indirection is removed) — this affects only an auxiliary report-mirroring step, not checkpoint or benchmark data. Two further files with the same historical pattern in their `if __name__ == "__main__":` blocks, found during this pass and not on the audit's explicit list — `dataset_tools/resplan/resplan_forensic_auditor.py`, `dataset_tools/pairing/pairing_detector.py` — were fixed identically, along with `tests/test_phase3_scientific_readiness.py`'s now-unneeded `ARCHI_AI/`-junction fallback candidates in its `_resolve_candidate_path()` helper (removed; only the repo-root-relative candidate remains). `DATASET.md` §6, `ROADMAP.md`, `README.md`/`README_EN.md`, and `docs/CONTRIBUTOR_GUIDE.md` were updated to stop instructing contributors to recreate the symlink layout, and now record the limitation as fixed.

No experiment was rerun; no benchmark number, checkpoint hash, or scientific conclusion was touched.

**Files changed:** `dataset_tools/experiments/micro_pilot/{run_micro_pilot.py, gold_evaluator.py, trainer.py, dataset_loader.py, baseline_evaluator.py}`, `dataset_tools/{gold_set_builder.py, audit_calculator.py, decision_classifier.py, deep_audit.py, audit_diagnostics.py}`, `dataset_tools/resplan/resplan_forensic_auditor.py`, `dataset_tools/pairing/pairing_detector.py`, `dataset_tools/preprocessing/{run.py, schema.py}`, `dataset_tools/acquisition/acquire_core.py`, `dataset_tools/validation/migrate_historical.py`, `dataset_tools/supervision/independent_audit/run_audit.py`, `scripts/rebuild_dataset.py`, `tests/test_phase3_scientific_readiness.py`, `DATASET.md`, `ROADMAP.md`, `README.md`, `README_EN.md`, `docs/CONTRIBUTOR_GUIDE.md`.

**Validation performed.** All edited files byte-compile cleanly (`py_compile`). For every file newly computing `REPO_ROOT`, an independent script walked the same number of `.parent` hops and confirmed it lands exactly on the repository root. `pytest tests/test_master_pipeline.py tests/test_audit_validators.py` (the CI hard gate) passes 9/9 after the change. The private RAW/Dataset A corpus is not present in this environment, so the checkpoint-producing scripts could not be executed end-to-end — consistent with "do not rerun expensive experiments."

**Resulting status: CLOSED.**

## Item 2 — Test-isolation defect in `legal_filter.py`/`split_manager.py` (P2)

**Finding.** `tests/test_master_pipeline.py::test_legal_filter_floorplancad` instantiated `LegalFilter()` with no arguments, defaulting `restricted_root` to a real repo path and unconditionally calling `.mkdir()`, then `apply_filter()` wrote `RESTRICTED_MANIFEST.jsonl` and `FLOORPLANCAD_LEGAL_DOSSIER.md` there via the module-level `MANIFEST_RESTRICTED` constant. `::test_split_deterministic_anti_leakage` called `DeterministicSplitter().partition_records(...)`, which writes real `train/validation/test.jsonl` and `SPLIT_MANIFEST.jsonl` to the module-level `SPLITS_DIR`/`MANIFEST_SPLIT` constants. Reproduced live in this remediation pass: running just these two hard-gated CI tests from a checkout with no `dataset/` directory present creates `dataset/master/v2/{restricted/legal_review/floorplancad/, manifests/, splits/}` containing real files — confirmed via `git status --porcelain --ignored` before/after.

**Remediation.** Both tests now accept `tmp_path` (and `monkeypatch` for the module-level constants that aren't constructor parameters): `LegalFilter(restricted_root=tmp_path / ...)` plus `monkeypatch.setattr(legal_filter_module, "MANIFEST_RESTRICTED", tmp_path / ...)`, and `monkeypatch.setattr(split_manager_module, "SPLITS_DIR"/"MANIFEST_SPLIT", tmp_path / ...)`. `tests/test_preprocessing.py`'s six preprocessor-instantiating tests (same root cause: `BasePreprocessor.__init__` unconditionally does `self.processed_root.mkdir(...)`, and all six tests passed it a real `dataset/processed` path) were fixed the same way, using `tmp_path` for `processed_root`. No production code was modified — `LegalFilter` already supported an injectable `restricted_root`; `monkeypatch` is the standard pytest idiom for redirecting a module-level constant. Test intent and every existing assertion are unchanged.

**Files changed:** `tests/test_master_pipeline.py`, `tests/test_preprocessing.py`.

**Validation performed.** `git status --porcelain --ignored` captured before and after running (a) the hard-gated subset and (b) the full suite (`pytest tests/`: 92 collected + 1 module-skip = 99 total test functions → 35 passed / 19 failed / 38 errored / 1 skipped, identical to the audit's own §7 figure). In both cases the only diff is `__pycache__/` bytecode-cache directories (routine interpreter output, already `.gitignore`d) — no `dataset/` directory or any other persistent artifact is created.

**Resulting status: CLOSED.**

## Item 3 — Pre-Training Gate `RED` vs `CONDITIONAL` vocabulary inconsistency (P2)

**Finding.** `docs/research/PRE_TRAINING_GATE.md` (Phase 2, based on `docs/evaluation/INDEPENDENT_AUDIT_REPORT.md`) stated the gate status as `RED`, with no cross-reference to the fact that Phase 3 (`docs/research/SCIENTIFIC_READINESS_REPORT.md`) later investigated and resolved each of its three blocking reasons (ResPlan pixel/m² anomaly → formally `QUARANTINED`; Gold Set V2 contamination → replaced by independently-sanctuarized Gold Set V3; incomplete multimodal dependency → scope narrowed and documented) and rendered a superseding formal decision of `CONDITIONAL` (`TRAINING_ALLOWED: NO`) — the terminology used by every other current document.

**Remediation.** Added an explicit banner to both `docs/research/PRE_TRAINING_GATE.md` and `docs/evaluation/INDEPENDENT_AUDIT_REPORT.md` (its source audit) marking them as superseded Phase-2 historical records, pointing to `SCIENTIFIC_READINESS_REPORT.md` as the current, authoritative gate decision (`CONDITIONAL`, `TRAINING_ALLOWED: NO`). The original `RED` verdict, its stated reasons, and all of its figures are left completely unmodified — only a forward-pointing banner was added, per "preserve historical audit records where the historical status is meaningful." A repo-wide search confirmed `TRAINING_ALLOWED` is `NO` everywhere (14 files) with zero contradictions, and that no document claims or implies the gate is currently `GREEN` or training-authorized.

**Files changed:** `docs/research/PRE_TRAINING_GATE.md`, `docs/evaluation/INDEPENDENT_AUDIT_REPORT.md`.

**Validation performed.** Repo-wide grep for `TRAINING_ALLOWED` (14 files, all `NO`) and for `Pre-Training Gate`/`PRE_TRAINING_GATE` (13 files) confirmed every current-facing document says `CONDITIONAL` and both Phase-2 documents are now explicitly marked historical/superseded with a forward reference.

**Resulting status: CLOSED.**

## Item 4 — Stale `ARCHI-AI` document titles in `PRE_TRAINING_GATE.md` / `SCIENTIFIC_READINESS_REPORT.md` (P3)

**Finding.** Both documents' H1 titles read `# ARCHI-AI — ...` rather than `# AXIS — ...`, unlike sibling documents (`docs/research/QLORA_PIPELINE.md`, `experiment_package/README.md`) already fixed in the prior remediation pass. `SCIENTIFIC_READINESS_REPORT.md` is the current, authoritative gate-decision document (not a dated historical snapshot), so per the "current vs. historical" test this remediation applied throughout: it should carry current AXIS branding. `PRE_TRAINING_GATE.md` is a historical, superseded record (see Item 3) but is actively linked from current-status documents, and the audit itself (§15 item 4) explicitly called for retitling it alongside its sibling — its already-added historical-context banner (Item 3) makes the distinction between "this document's title is AXIS-branded" and "this document's *content* is a preserved Phase-2 verdict" unambiguous to a reader.

**Remediation.** Changed both H1 titles from `# ARCHI-AI — ...` to `# AXIS — ...`. No other content in either file was altered (their bodies, including all historical figures, verdicts, and the Item 3 banner, are unchanged). Separately, during the earlier pass of this remediation, two *other* documents were identified and fixed on the same "current documentation, not historical, should be AXIS-branded" reasoning: `docs/datasets/ARCHI_AI_CAPABILITY_MATRIX.md` → `docs/datasets/AXIS_CAPABILITY_MATRIX.md` and `docs/datasets/DATASET_ARCHI_AI_ROLES.md` → `docs/datasets/DATASET_AXIS_ROLES.md` (both renamed via `git mv`, with all internal `ARCHI-AI` references rebranded to `AXIS`; no other file referenced either old filename). These are additional, harmless scope beyond what this specific audit finding named, not a substitute for it — both are now fixed.

**Files changed:** `docs/research/PRE_TRAINING_GATE.md`, `docs/research/SCIENTIFIC_READINESS_REPORT.md` (title only); `docs/datasets/ARCHI_AI_CAPABILITY_MATRIX.md` → `docs/datasets/AXIS_CAPABILITY_MATRIX.md`, `docs/datasets/DATASET_ARCHI_AI_ROLES.md` → `docs/datasets/DATASET_AXIS_ROLES.md` (renamed + content, additional scope).

**Validation performed.** `grep -n "^# ARCHI-AI"` against both files now returns zero hits; `grep -rn "ARCHI"` against the two renamed files also returns zero hits. `grep -rln` for both old filenames across the repository returns zero hits (no dangling references).

**Resulting status: CLOSED.**

## Item 5 — Pre-`42b1f51` squashed git history (P3)

**Finding.** The audit's machine-readable summary (line `OPEN_P3 (2)`) separately names, as the second P3 item, "pre-`42b1f51` squashed git history (pre-existing, disclosed, low severity)" — the incremental Phase 0–4 development history is squashed into the single `42b1f51` baseline commit rather than present as granular commits. This was *not* among the audit's §15 "Required Next Actions" (items 1–4 above); the audit itself treats it as already correctly disclosed (`docs/history/project-history.md` §4, "Git History Limitation") rather than something to act on.

**Why this remains open, by design.** Reconstructing granular history for `42b1f51` and earlier would require either (a) rewriting existing repository history — forbidden by this remediation's hard rules ("never rewrite history on someone else's branch," and more fundamentally, altering committed history to manufacture an incremental-looking past is itself a form of fabricating historical record — exactly what "do not fabricate or change scientific results" and "preserve historical audit records" are meant to prevent — or (b) fabricating synthetic intermediate commits that never actually happened, which would misrepresent the project's real development timeline. Neither is a legitimate remediation. `docs/history/project-history.md` §4 already states this limitation plainly, which is the correct fix available: tell the truth about it, not manufacture a fictional history to paper over it.

**Resulting status: OPEN (correctly, by design — not actionable without fabricating history; already honestly disclosed).**

## Additional item discovered during this pass — invalid escape sequences (forward-compatibility hygiene)

Not named in the audit above; found via a `compile()`-based `DeprecationWarning` scan while reviewing files touched by Item 1. Four files (`dataset_tools/master_pipeline/reporter.py`, `dataset_tools/supervision/independent_audit/audit_reporter.py`, `dataset_tools/experiments/micro_pilot/{gold_evaluator.py, baseline_evaluator.py}`) used non-raw f-strings containing LaTeX-style `\ge`/`\le` inside Markdown report templates — not recognized Python escapes; currently a `DeprecationWarning`, documented to become a `SyntaxError` in a future Python version, which would break these report generators outright. Fixed by escaping exactly the invalid single-backslash sequences (`\ge` → `\\ge`, `\le` → `\\le`), leaving already-correct `\\ge`/`\\le` occurrences elsewhere untouched. This is a source-level-only change: directly verified that `\ge` (kept literal by Python) and `\\ge` (explicit escape) evaluate to the identical runtime string, so generated report content is byte-for-byte unchanged. Re-scan after the fix: zero `DeprecationWarning`s remain repository-wide (down from 12 instances across 4 files). Hard-gated CI subset re-verified passing 9/9 after the change. **Resulting status: CLOSED** (not counted against the audit's own P2/P3 tally above, since it was not one of its named findings).

---

## Final Validation Summary (post-remediation)

**A. Relevant unit tests.** `pytest tests/`: 92 collected + 1 module-skip = 99 total → 35 passed / 19 failed / 38 errored / 1 skipped. Identical to the audit's own §7 baseline; every non-passing result traces to the intentionally non-redistributed private dataset corpus, not to anything introduced by this remediation.

**B. Hard-gated CI subset.** `pytest tests/test_audit_validators.py tests/test_master_pipeline.py` → **9/9 passed.**

**C. Test isolation from a clean state.** `git status --porcelain --ignored`, captured before and after running both the hard-gated subset and the full suite from a checkout with no `dataset/` directory present: the only difference in both cases is `__pycache__/` bytecode-cache directories (already `.gitignore`d, produced by the interpreter, not by test logic). No `dataset/` directory, and no other persistent artifact, is created — the exact defect the audit reported in §5 finding #1 is fixed and directly re-verified.

**D. Package installation.** `pip install -e .` succeeds cleanly (verified before and after all changes). `pip install -e ".[dataset]"` (the `shapely`/`pyarrow`/`ifcopenshell` extras) also succeeds with no network-dependent workaround.

**E. Stale reference search.** Repository-wide search for `ARCHI_AI`, `ARCHI-AI`, old `ARCHI_AI/`-prefixed paths, old gate terminology, contradictory `TRAINING_ALLOWED` values, obsolete setup commands, and stale dataset/test counts. Every material hit was reviewed individually. The pervasive `ARCHI-AI` branding remaining in docstrings, `print()` banners, and `argparse` descriptions across ~50 other files was reviewed and deliberately left unchanged — the same category of "historical scientific identifiers / code symbols" the original remediation pass explicitly ruled out of scope, not filename- or reference-bearing the way the Item 4 documents were, and a blind global rename across that many files (unverifiable against the private dataset in this environment) would carry materially more risk than benefit for a documentation/hygiene pass.

---

## Final State

```text
OPEN_P0: 0
OPEN_P1: 0
OPEN_P2: 0
OPEN_P3: 1
TRAINING_ALLOWED: NO
TEST_ISOLATION: PASS
PACKAGE_INSTALL: PASS
HARD_GATED_TESTS: PASS
LEGACY_PATHS: CLEAN
GATE_STATUS_CONSISTENCY: PASS
```

The one remaining `OPEN_P3` is the pre-`42b1f51` squashed git history (Item 5 above), left open by design: it cannot be closed without either rewriting committed history or fabricating commits that never occurred, both of which this remediation's hard rules and the project's own scientific-integrity standard forbid. It is honestly disclosed in `docs/history/project-history.md` §4, which is the correct and complete remediation available for this specific item.

This remediation did not train any model, launch any GPU job, download any weights, or modify the RAW dataset, the Master Dataset, the Gold Set, any benchmark result, or any checkpoint metadata. `TRAINING_ALLOWED: NO` remains in force. The pre-training gate itself is governed by `docs/research/SCIENTIFIC_READINESS_REPORT.md` and is unaffected by this update; only a separate, independent pre-training gate review may change it.
