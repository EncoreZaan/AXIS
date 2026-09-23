# AXIS — Policy on Scientific Documentation & Experimental Archival

> **Document ID:** `AXIS-POL-2026-001`  
> **Effective Date:** 2026-09-23  
> **Status:** **MANDATORY & ENFORCED**  
> **Authority:** AXIS Scientific Governance & Core Maintainers  

---

## 1. Foundational Axiom

> [!IMPORTANT]
> **"Scientific execution without archival documentation is not considered complete."**

In the AXIS project, running code on a GPU, observing a loss decrease, or calculating evaluation metrics does **not** constitute finished work. An experiment is only scientifically valid and officially recognized when its entire audit trail—code, environment, configuration, execution logs, numeric outputs, cryptographic hashes, limitations, and falsification analysis—is permanently documented, verified, and committed to the authoritative repository.

---

## 2. Daily Documentation Policy

Every meaningful work session, training pilot, evaluation benchmark, or ablation study **must** conclude with a dedicated documentation synchronization before any subsequent experiment is authorized.

Under no circumstances may undocumented experimental artifacts accumulate on remote compute instances (e.g., RunPod, local workstations, or cloud storage) without synchronized repository reflection.

### Mandatory Post-Experiment Synchronization Checklist

At the conclusion of every experiment, the following steps are obligatory:

1. **Canonical Experiment Directory Updated:** All metrics files (`.json`, `.jsonl`), run manifests, logs, and sample summaries must be placed in the designated `RUN-XXX/` directory.
2. **Cryptographic Sealing:** Compute and record SHA-256 checksums and exact file sizes for every critical artifact in `hashes.json`.
3. **Execution Telemetry Captured:** Hardware details (GPU model, driver, CUDA, VRAM), library stack versions (`transformers`, `peft`, `torch`, `bitsandbytes`), and execution durations must be recorded in `environment_snapshot.json` and the run report.
4. **Honest Falsification & Limitations:** The experiment report must document all observed flaws, unexpected behaviors, evaluation metric sensitivities, and methodological boundaries. Negative results must never be concealed or minimized.
5. **Formal Gate Audit:** Verify that all pre-conditions and post-conditions have been evaluated and recorded in a gate document.
6. **Chronological Timeline Updated:** Register the milestone in `docs/SCIENTIFIC_TIMELINE.md`.
7. **Project Status Synchronized:** Update `docs/PROJECT_STATUS.md` and root `PROJECT_STATUS.md`.
8. **Navigation Layer Updated:** Add or update the corresponding entry in `docs/experiments/RUN-XXX/README.md`.
9. **Public README Synchronized:** Update `README.md` and `README_EN.md` whenever public milestone or capability claims are affected.
10. **Dedicated Git Commit:** Stage and commit the documentation and artifact updates under a clear, conventional commit message (e.g., `docs: archive RUN-XXX scientific progress`).

---

## 3. Strict Archival & Scientific Integrity Rules

To preserve complete scientific reproducibility and prevent epistemic corruption, all contributors and automated agents must adhere to the following 10 invariants:

1. **Zero Retrofitting:** Never modify an experimental protocol, evaluation threshold, or scoring metric after observing the evaluation output.
2. **Zero Smoothing of Unfavorable Data:** Unfavorable, inconclusive, or failing results (such as visual ablation failure, low VDI, or zero accuracy on a sub-task) must be presented with the exact same visibility and prominence as positive results.
3. **Strict Terminology Invariants:**
   - Never label an automated programmatic script check as a "human evaluation" or "manual audit".
   - If an evaluation was performed programmatically, label it `AUTOMATED_GEOMETRIC_AUDIT` or `AUTOMATED_SIDE_BY_SIDE`.
   - Explicitly record `MANUAL_AUDIT_HUMAN: NOT_PERFORMED` unless a vetted human annotator conducted a documented review.
4. **Visual Grounding Standard:**
   - Never claim visual dependency or spatial grounding based solely on training or evaluation loss convergence.
   - Grounding requires formal empirical proof via counterfactual visual perturbation benchmarks (e.g., Visual Dependency Index $\text{VDI} \ge 3.0$).
   - If VDI threshold is not met, the record must state: `VDI_PASS: NO`.
5. **Sanctuary Asset Immutability:** Sanctuarized assets (`Master Dataset v2`, `Gold Set V3`, frozen training splits, locked adapter weights) must be verified via SHA-256 before and after each execution. No experiment may mutate a sanctuary.
6. **No Fabrication of Missing Records:** If an artifact, log, or hash was lost or unrecorded, state explicitly: `MISSING_FROM_REPOSITORY` or `NOT_RECORDED`. Never invent plausible numbers or reconstruct simulated outputs.
7. **Historical Preservation:** Never delete an older experimental report merely because a newer run supersedes it. Add explicit supersession banners and cross-references instead.
8. **Traceability Guarantee:** Every numerical claim in a Markdown document or paper must be directly traceable to a specific JSON record, log file, or script in the repository.
9. **Large Binary Separation:** Base model weights, multi-gigabyte optimizer states, and large checkpoint files (>100 MB) must not be pushed to Git. They must be ignored via `.gitignore`, documented with their exact SHA-256 hash and physical location, and represented by lightweight configuration/manifest files.
10. **Zero Secrets in Repository:** SSH private keys, cloud tokens, API keys, and environment passwords must never be staged or committed.

---

## 4. Canonical Documentation Hierarchy

```text
AXIS/
├── README.md                           # Public executive overview, status, and entry points
├── README_EN.md                        # English public executive overview
├── PROJECT_STATUS.md                   # Authoritative current scientific and technical status
├── docs/
│   ├── DOCUMENTATION_POLICY.md         # This policy document
│   ├── PROJECT_STATUS.md               # Detailed scientific status mirroring root
│   ├── SCIENTIFIC_TIMELINE.md          # Chronological record of all phases and runs
│   ├── GATES_AND_DECISIONS.md          # Decision records and formal stage gates
│   ├── datasets/                       # Dataset architecture, provenance, and license audits
│   ├── evaluation/                     # Evaluation protocols, metrics, and holdout specifications
│   ├── experiments/                    # Readable experiment overviews and analysis
│   │   ├── RUN-019/README.md           # First Real-Data QLoRA
│   │   ├── RUN-020/README.md           # Scientific Generalization & Falsification
│   │   ├── RUN-021/README.md           # Spatial Supervision Dataset Engineering
│   │   ├── RUN-022/README.md           # Spatial Grounding Scientific Pilot
│   │   └── RUN-023/README.md           # Spatial Generalization & Visual Grounding Evaluation
│   └── research/                       # Foundational research notes and architecture studies
└── RUN-XXX/                            # Canonical experiment evidence directories
    ├── manifest.json / hashes.json     # Cryptographic integrity manifests
    ├── *metrics.json / *.jsonl         # Empirical outputs and prediction logs
    └── *REPORT.md                      # Detailed technical and scientific run reports
```

---

## 5. Enforcement

Any pull request, commit, or sub-agent execution that claims completion of an experiment without satisfying the requirements of this policy shall be automatically rejected during gate review.
