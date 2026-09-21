# Project History & Scientific Traceability: ARCHI-AI → AXIS

> **Date:** September 2026  
> **Official Public Identity:** `AXIS` (Architectural eXpert Intelligence System)  
> **Historical Research Codename:** `ARCHI-AI`  
> **Repository:** [https://github.com/EncoreZaan/AXIS.git](https://github.com/EncoreZaan/AXIS.git)

---

## 1. Context and Rationale of the Evolution

The project originated under the research codename **ARCHI-AI**. In its earliest exploration (Phase 0), the project evaluated state-tuning architectures (including RWKV-7 2.9B on local hardware) before shifting toward multimodal architectures (QLoRA VLM fine-tuning on Qwen2-VL-7B) and deep geometric spatial reasoning models.

As the project established its formal scientific foundations—specifically:
1. The construction and multi-dimensional audit of **Master Dataset v2** (65,342 records across 19 physical sources);
2. The forensic audit of the RAW corpus (confirming the exact rarity of 2D/3D floorplan-to-BIM pairs);
3. The quarantining of uncalibrated metric vectors (ResPlan scale anomalies) and legal risk assets (FloorPlanCAD);
4. The execution and peer-audited verification of **Phase 4 Controlled Unimodal Micro-Pilot** (achieving 0.0517 m MAE on Gold Set V3 and 100% normative accuracy);

the project transitioned from an exploratory working prototype into a formal, publicly-released research initiative (code license status: TBD — see `GOVERNANCE.md`). The official, permanent identity was designated as:

$$\textbf{AXIS} \quad \text{—} \quad \textbf{Architectural eXpert Intelligence System}$$

---

## 2. Scientific Traceability & Preserved Identifiers

To guarantee unbroken provenance and falsifiability in academic peer review, **historical identifiers from the ARCHI-AI phase are deliberately preserved and are NOT renamed retroactively**.

| Category | Historical Identifier | Current AXIS Role / Description |
| :--- | :--- | :--- |
| **Model Checkpoint** | `ARCHI-AI-P4-005` | Selected best validation checkpoint on Dataset A (A-Full, seed 42). Certified SHA256: `69f00c211e1db63181bf7c6f4ae624c3aa312856f7d8b2191bc9c8b84a680d54`. |
| **Model Checkpoint** | `ARCHI-AI-P4-001` | Reference comparison checkpoint on Dataset A (A-Small, seed 42). |
| **Gold Set Manifest** | `GOLD_V3_MANIFEST.jsonl` | Read-only immutable Gold benchmark. Certified SHA256: `81561fae5b524fa26622e5fac27d612f7d75a11e6ff0be774448fef04b9f2aca`. |
| **Counterexamples** | `counterexamples.jsonl` | 200 adversarial hard negatives. Certified SHA256: `a7991b378e46205e6e639961a9d634dd95661daa22129a89ab0744b73c9414e0`. |
| **Evaluation Run** | `ARCHI-AI-P4-GOLD-001` | Formal evaluation execution on Gold Set V3. |
| **Ablation Runs** | `ARCHI-AI-P4-ABL-B`, `ARCHI-AI-P4-ABL-C` | Metadata sanitization and input scrambling ablation benchmarks. |
| **Micro-Experiment** | `outputs/archi_ai_micro_experiment` | Dry-run and 6-step proof-of-concept LoRA on Qwen2-VL-7B-Instruct. |

---

## 3. Phase Continuity

| Research Phase | Period | Core Focus | Official Status |
| :--- | :--- | :--- | :--- |
| **Phase 0** | Early Sept 2026 | Environment audit, local VRAM constraints, RWKV-7 & QLoRA feasibility | **COMPLETED** |
| **Phase 1** | Mid Sept 2026 | Dataset infrastructure, 19 sources ingestion, Master Dataset v2 (65,342 assets) | **COMPLETED & AUDITED** |
| **Phase 2** | Sept 2026 | Supervision engine v1, Gold Set V2, red-team harm & shortcut audit | **COMPLETED & CERTIFIED** |
| **Phase 3** | Sept 2026 | RAW forensic audit (66,847 files), ResPlan calibration audit, FloorPlanCAD legal quarantine | **COMPLETED & GATED** |
| **Phase 4** | Sept 2026 | Task catalog gating (4/69 tasks), Dataset A build, Baseline 0, Gold Set V3 evaluation | **COMPLETED & SCIENTIFICALLY VALIDATED** |
| **AXIS v0.1.0** | Current | Public GitHub publication, openly-published documentation, community engagement | **CURRENT MILESTONE** |
| **Phase 5** | Upcoming | Acquisition of 50-100 OpenBIM IFC pairs, metric plan generation, pre-training gate | **PLANNED** |

---

## 4. Git History Limitation

This public repository was initialized with a single commit (`feat: official migration from ARCHI-AI to AXIS v0.1.0`) that already contains the full Phase 0–4 codebase and documentation described above. **The public Git history does not contain the incremental commit-by-commit development history of Phases 0 through 4** — that history exists only in the maintainer's private local/working repository and was not carried over when this public repository was created.

This is stated explicitly rather than implied, per the project's commitment to scientific traceability: the phase-by-phase narrative in §3 above and the identifiers in §2 are the available record of that work, backed by the artifacts and hashes documented throughout this repository — not by a granular commit log. No attempt has been made to fabricate or backfill an artificial multi-commit history to simulate one; doing so would misrepresent the actual provenance of the published code.
