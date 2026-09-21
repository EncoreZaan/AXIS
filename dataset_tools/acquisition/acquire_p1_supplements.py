"""
Acquire FloorPlanCAD and sample ResBIM-IFC models
"""
import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from huggingface_hub import snapshot_download, hf_hub_download

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_EXTERNAL_DIR = BASE_DIR / "dataset" / "raw" / "external"
CORE_DIR = RAW_EXTERNAL_DIR / "core"
MANIFEST_PATH = RAW_EXTERNAL_DIR / "ACQUISITION_MANIFEST.json"


def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def load_manifest() -> dict:
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_manifest(manifest: dict):
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest["total_datasets"] = len(manifest["records"])
    manifest["total_size_bytes"] = sum(r.get("size_bytes", 0) for r in manifest["records"].values())
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


def acquire_floorplancad():
    print("\n--- [ACQUIRE] FloorPlanCAD (CAD Symbols & Object Detection) ---")
    dest_dir = CORE_DIR / "floorplancad"
    dest_dir.mkdir(parents=True, exist_ok=True)
    # Download curated subset of CAD drawings + README
    snapshot_download(
        repo_id="Voxel51/FloorPlanCAD",
        repo_type="dataset",
        local_dir=str(dest_dir),
        allow_patterns=["README.md", "data/000*"]
    )
    
    total_size = sum(f.stat().st_size for f in dest_dir.rglob("*") if f.is_file())
    img_files = list(dest_dir.rglob("*.png"))
    
    manifest = load_manifest()
    manifest["records"]["CORE_FLOORPLANCAD"] = {
        "source_name": "FloorPlanCAD (Voxel51)",
        "official_url": "https://huggingface.co/datasets/Voxel51/FloorPlanCAD",
        "license": "CC-BY-SA-4.0",
        "legal_category": "CORE",
        "priority": "P1",
        "domain": "Architectural CAD Drawings & Symbol Spotting",
        "modalities": ["png_raster_drawings", "object_detection_annotations", "cad_symbol_classes"],
        "num_elements": len(img_files),
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "archi_ai_value": "Reconnaissance et segmentation sémantique des symboles architecturaux normalisés (portes, fenêtres, mobilier)"
    }
    save_manifest(manifest)
    print(f"  [MANIFEST] Recorded CORE_FLOORPLANCAD ({total_size:,} bytes, {len(img_files)} images)")


def acquire_resbim_sample():
    print("\n--- [ACQUIRE] ResBIM-IFC Paired Sample (2D Floorplans <-> 3D IFC) ---")
    dest_dir = CORE_DIR / "resbim"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Download sample paired cases (0 to 15)
    sample_indices = [0, 1, 2, 3, 4, 5, 10, 100, 101, 102]
    total_downloaded = 0
    downloaded_files = {}
    
    for idx in sample_indices:
        for ext in [".jpg", ".ifc"]:
            filename = f"data/{idx}/{idx}{ext}"
            try:
                cached = hf_hub_download(repo_id="tsesterh/ResBIM-IFC", filename=filename, repo_type="dataset")
                target = dest_dir / f"unit_{idx:03d}{ext}"
                with open(cached, "rb") as src, open(target, "wb") as dst:
                    dst.write(src.read())
                sz = target.stat().st_size
                total_downloaded += sz
                downloaded_files[target.name] = {
                    "size_bytes": sz,
                    "sha256": compute_sha256(target)
                }
            except Exception as e:
                print(f"  Skipping {filename}: {e}")
                
    manifest = load_manifest()
    manifest["records"]["CORE_RESBIM_PAIRED"] = {
        "source_name": "ResBIM-IFC (Paired 2D/3D BIM Sample)",
        "official_url": "https://huggingface.co/datasets/tsesterh/ResBIM-IFC",
        "license": "MIT",
        "legal_category": "CORE",
        "priority": "P1",
        "domain": "2D Floorplan to 3D BIM Alignment",
        "modalities": ["2d_floorplan_images", "3d_openbim_ifc"],
        "num_elements": len(downloaded_files) // 2,
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_downloaded,
        "files": downloaded_files,
        "archi_ai_value": "Couplage exact entre plans 2D d'architectes et maquettes 3D IFC natives"
    }
    save_manifest(manifest)
    print(f"  [MANIFEST] Recorded CORE_RESBIM_PAIRED ({total_downloaded:,} bytes)")


if __name__ == "__main__":
    acquire_floorplancad()
    acquire_resbim_sample()
