# Third-Party Licenses & Data Provenance

This document exists to keep two things that are easy to conflate strictly
separate:

1. **The AXIS original code** — the Python source in `dataset_tools/`,
   `evaluation/`, `experiment_package/`, `scripts/`, `tests/`, and the
   documentation in this repository — which is licensed under the
   **MIT License** (see [`LICENSE`](LICENSE)).
2. **Third-party datasets, images, pretrained weights, and other assets**
   that AXIS *references, processes, or evaluates against* — which are
   **not** owned by this project and are **not** relicensed by it. Each
   keeps its own upstream license.

Publishing the AXIS code under MIT does not, and legally cannot, grant any
rights over data or models the project does not own. If you plan to reuse
anything beyond the AXIS code itself, check the specific source below and
consult its original license text — the summaries here are for orientation
only and are not a substitute for the upstream terms.

---

## 1. Scope of the MIT License

The MIT License in [`LICENSE`](LICENSE) covers:

- All Python packages and modules under `dataset_tools/`, `evaluation/`,
  `experiment_package/` (code, not its `README.md`-documented example data),
  `scripts/`, `tests/`.
- Configuration files (`configs/`, `pyproject.toml`, `.github/workflows/`).
- Original prose documentation authored for AXIS (`README.md`, `README_EN.md`,
  `ROADMAP.md`, `DATASET.md`, `EVALUATION.md`, files under `docs/`, etc.).

It does **not** cover anything listed in §2–§4 below.

---

## 2. Third-Party Datasets (Referenced or Processed, Never Redistributed)

None of the raw datasets below are committed to or redistributed by this
repository (see [`DATASET.md` §5, Data Access Policy](DATASET.md#5-data-access-policy)
and the `dataset/` exclusion in [`.gitignore`](.gitignore)). AXIS ships
ingestion/validation code and metadata schemas that operate on these sources
once a contributor acquires them independently from their original
publishers, under the original publishers' terms.

| Source | Role in AXIS | License (as documented by upstream) | Notes |
| :--- | :--- | :--- | :--- |
| `CORE_RPLAN` (RPLAN) | Plan topology & room reading | Academic Research Only [^1] | Non-commercial, research use, no raw redistribution |
| `CORE_IL3D` (IL3D) | 3D Cartesian coordinates & clearance | Academic Research Only [^1] | Same as above |
| `CORE_STRUCTSCAN3D` | Subjective perspective & depth | Open Research | See upstream release for exact terms |
| `CORE_FLOORPLANCAD` | Quarantined (`LEGAL_REVIEW_REQUIRED`) | CC-BY-SA 4.0 | Not used in any trained/evaluated pathway pending legal review — see [`DATASET.md` §3.2](DATASET.md#32-floorplancad-legal-quarantine) |
| `CORE_IFC_BENCH` | BIM schema entities & axonometric views | CC-BY 4.0 / Open | |
| `CORE_BUILDINGSMART_IFC` | IFC schema validation & testbeds | Open Standard (buildingSMART) | |
| `CORE_RESBIM_PAIRED` | Ground-truth multimodal 2D/3D pairs | CC-BY 4.0 / MIT (per sub-source) | Only 10 genuine pairs exist in RAW |
| `CORE_RESPLAN` (ResPlan) | Quarantined for metric (m²) use; safe for topology | CC-BY 4.0 / MIT | Scale-distortion quarantine, see [`DATASET.md` §3.1](DATASET.md#31-resplan-metric-quarantine) |
| `CORE_POLYHAVEN_MATERIALS` / `CORE_POLYHAVEN_LIGHTING` | Material & lighting reasoning | CC0 | Poly Haven |
| `CORE_MOMA_COLLECTION` | Design history & typology | Public Domain | MoMA Open Access |
| `CORE_MET_OPENACCESS` | Architectural history & styles | CC0 | The Met Open Access |
| `CORE_MMMU_ARCHITECTURE` | Multimodal architecture evaluation subset | CC-BY 4.0 | MMMU benchmark subset |
| `CORE_NORMES_FR` | Ergonomic clearance thresholds (PMR) | Public Domain (Légifrance) | French public regulatory text |
| `CORE_ERGONOMIE` | Standard passage & furniture tolerances | Open Reference | Paraphrased from Neufert-style standards |
| `CORE_AMBIENTCG` | Material textures | CC0 | ambientCG |
| `CORE_TRENDS_2026` | Stylistic reference | Public Reference | |

[^1]: "Academic Research Only" is the maintainer's short paraphrase of the
upstream terms for RPLAN and IL3D, not a formal SPDX identifier. It means:
non-commercial use for research/academic purposes, no redistribution of raw
assets. AXIS does not alter or sublicense these terms — see
[`DATASET.md` footnote 1](DATASET.md#1-physical-sources--distribution) for
the full text of this caveat.

This table is a convenience index, not a legal opinion. See
[`DATASET.md`](DATASET.md) §1 for the authoritative, actively maintained
source registry and [`docs/datasets/DATASET_LICENSE_AUDIT.md`](docs/datasets/DATASET_LICENSE_AUDIT.md)
for the historical per-source audit trail.

---

## 3. Model Checkpoints / Weights

No trained model checkpoint or weight file is currently published by this
repository (see [`EVALUATION.md` §4, Artifact Availability](EVALUATION.md#4-artifact-availability)).
Historical internal checkpoint identifiers (e.g. `ARCHI-AI-P4-005`) and their
SHA256 hashes are documented for scientific traceability only — they do not
imply the binary weights are downloadable, and no license for them has been
decided. If/when a checkpoint is released publicly, its license will be
stated explicitly at that time, in the release notes and in `EVALUATION.md`.

---

## 4. Third-Party Software Dependencies

AXIS depends on third-party Python packages listed in `requirements.txt` and
`pyproject.toml` (`torch`, `transformers`, `peft`, `shapely`, `ifcopenshell`,
etc.). Each is distributed under its own upstream open-source license by its
respective maintainers (Apache-2.0, BSD, MIT, LGPL, and others depending on
the package) and is not modified, forked, or relicensed by AXIS. Consult each
package's own repository for its exact license.

---

## 5. If You Are Unsure

If a specific file, dataset, or asset is not clearly covered above, do not
assume it is MIT-licensed. Open an issue (`dataset_issue.md` template) and
ask — this keeps the project's licensing posture accurate rather than
guessed at.
