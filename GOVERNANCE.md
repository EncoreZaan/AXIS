# Governance and Scientific Leadership

## Overview

**AXIS (Architectural eXpert Intelligence System)** is an open-source scientific research initiative aimed at developing specialized artificial intelligence for spatial, geometric, and architectural reasoning. The original AXIS code and documentation are licensed under the **MIT License** — see [License Status](#license-status) below. Third-party datasets and model checkpoints are governed separately and are not covered by this grant.

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

## License Status

> [!IMPORTANT]
> **The AXIS original code and documentation are licensed under the MIT License.** See [`LICENSE`](LICENSE) for the full text.
> - This grant applies to the code, scripts, configuration, and prose documentation authored in this repository.
> - It does **not** apply to third-party datasets, pretrained checkpoints, or other assets AXIS references or processes — those retain their own upstream terms. See [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) for the full breakdown.
> - Third-party datasets referenced in documentation (`RPLAN`, `IL3D`, `FloorPlanCAD`, etc.) retain their respective individual licenses and terms of service. AXIS does not redistribute proprietary data and does not sublicense or override upstream terms.

### Terminology this project keeps distinct

These terms describe different things and are not interchangeable:

- **Public repository / publicly visible:** anyone can read this code and documentation on GitHub.
- **Open research:** the project's methodology, results, and negative findings are documented openly, including failures and blockers (`Pre-Training Gate`, quarantined datasets, etc.).
- **Open-source (code license):** the AXIS code itself is licensed under MIT, permitting reuse, modification, and redistribution of the *code* under MIT's terms.
- **Third-party dataset / checkpoint licenses:** governed independently by their own upstream terms (per-source table in `DATASET.md` and `THIRD_PARTY_LICENSES.md`) or, for model checkpoints, not currently released publicly at all. AXIS's MIT license does not and cannot retroactively change these — MIT covers what AXIS itself wrote, not data or models AXIS does not own.

---

## Proposal & RFC Workflow

1. **Idea / Feature Proposal:** Open an issue using the `experiment_proposal.md` or `research_question.md` template.
2. **Discussion & Review:** Maintainers and domain experts provide feedback on scientific validity and feasibility.
3. **Pull Request:** Once approved, implementation proceeds via PR adhering to the strict anti-leakage and testing standards.
