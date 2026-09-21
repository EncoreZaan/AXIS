# Governance and Scientific Leadership

## Overview

**AXIS (Architectural eXpert Intelligence System)** is a publicly-visible scientific research initiative aimed at developing specialized artificial intelligence for spatial, geometric, and architectural reasoning. "Publicly visible" describes the repository's hosting on GitHub, not a software license grant — see [License Status (TBD)](#license-status-tbd) below.

The project is initiated and maintained by **EncoreZaan** (`teobarreau7@gmail.com`).

---

## Decision-Making Process

The project operates under a **Benevolent Dictator for Life (BDFL) / Scientific Lead** model, supported by community consensus and empirical peer review.

### 1. Scientific Truth Over Consensus
In AXIS, empirical falsifiability and rigorous benchmarking always supersede opinion or convenience:
- No capability is considered acquired without an adversarial holdout benchmark (e.g., Gold Set verification).
- No synthetic metric shortcut is tolerated (e.g., pixel-to-m² heuristics without physical calibration).
- The Gold Set is read-only and immutable. Post-hoc fine-tuning on evaluation sets is prohibited.

### 2. Roles & Responsibilities

| Role | Responsibilities | Current Members |
| :--- | :--- | :--- |
| **Project Lead & Architecture** | Roadmap definition, final architectural decisions, release gating, security | **EncoreZaan** |
| **ML & Evaluation Contributors** | Model architectures, training pipelines, ablation studies, baseline calibration | Community / Open to contributors |
| **Dataset & Forensic Engineers** | Corpus acquisition, license audits, deduplication, geometric verification | Community / Open to contributors |
| **Domain Specialists (BIM/CAD/Architects)**| Normative rules (`CORE_NORMES_FR`, Neufert, PMR), ground truth annotation validation | Community / Open to contributors |

---

## License Status (TBD)

> [!IMPORTANT]
> **Formal License Selection is Currently TBD (To Be Determined).**
> - The code and documentation are made publicly available for scientific inspection, peer review, and academic collaboration.
> - Making this repository public on GitHub does **not** automatically grant unrestricted commercial reuse until a formal open-source license (such as Apache 2.0, MIT, or a specialized research license) is selected and ratified by the maintainer.
> - Third-party datasets referenced in documentation (`RPLAN`, `IL3D`, `FloorPlanCAD`, etc.) retain their respective individual licenses and terms of service. AXIS does not redistribute proprietary data.

### Terminology this project keeps distinct

These four terms describe different things and are not interchangeable:

- **Public repository / publicly visible:** anyone can read this code and documentation on GitHub. This is the current state.
- **Open research:** the project's methodology, results, and negative findings are documented openly, including failures and blockers (`Pre-Training Gate`, quarantined datasets, etc.). This is the current state.
- **Open-source (code license):** a formal license grant (MIT, Apache-2.0, etc.) permitting reuse, modification, and redistribution of the code under stated terms. This is **not yet the state** — see above.
- **Third-party dataset / checkpoint licenses:** governed independently by their own upstream terms (per-source table in `DATASET.md`) or, for model checkpoints, not currently released at all. AXIS's own (TBD) license does not and will not retroactively change these.

---

## Proposal & RFC Workflow

1. **Idea / Feature Proposal:** Open an issue using the `experiment_proposal.md` or `research_question.md` template.
2. **Discussion & Review:** Maintainers and domain experts provide feedback on scientific validity and feasibility.
3. **Pull Request:** Once approved, implementation proceeds via PR adhering to the strict anti-leakage and testing standards.
