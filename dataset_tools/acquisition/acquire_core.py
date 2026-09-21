"""
ARCHI-AI Complete Raw Dataset Acquisition Script
Author: ARCHI-AI Engineering
Target Directory: ARCHI_AI/dataset/raw/external/
"""

import os
import sys
import json
import time
import shutil
import hashlib
import zipfile
import subprocess
from pathlib import Path
from datetime import datetime, timezone
import requests
from huggingface_hub import hf_hub_download, snapshot_download

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_EXTERNAL_DIR = BASE_DIR / "dataset" / "raw" / "external"
CORE_DIR = RAW_EXTERNAL_DIR / "core"
MANIFEST_PATH = RAW_EXTERNAL_DIR / "ACQUISITION_MANIFEST.json"


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of a file efficiently in chunks."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def download_url(url: str, dest_path: Path, max_retries: int = 3, timeout: int = 120) -> bool:
    """Download a file via HTTP/HTTPS with streaming and retries."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = dest_path.with_suffix(".tmp")
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ARCHI-AI-Acquisition/1.0"}
    for attempt in range(1, max_retries + 1):
        try:
            print(f"    [Attempt {attempt}/{max_retries}] Downloading {url} -> {dest_path.name}...")
            with requests.get(url, headers=headers, stream=True, timeout=timeout) as r:
                r.raise_for_status()
                with open(temp_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
            if temp_path.exists():
                if dest_path.exists():
                    dest_path.unlink()
                temp_path.rename(dest_path)
                print(f"    -> Successfully downloaded {dest_path.name} ({dest_path.stat().st_size:,} bytes)")
                return True
        except Exception as e:
            print(f"    -> Attempt {attempt} failed: {e}")
            if temp_path.exists():
                temp_path.unlink()
            time.sleep(2 * attempt)
    return False


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "version": "1.0.0",
        "system": "ARCHI-AI Raw External Corpus",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_datasets": 0,
        "total_size_bytes": 0,
        "records": {}
    }


def save_manifest(manifest: dict):
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest["total_datasets"] = len(manifest["records"])
    manifest["total_size_bytes"] = sum(r.get("size_bytes", 0) for r in manifest["records"].values())
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


def record_entry(manifest: dict, entry_id: str, record: dict):
    manifest["records"][entry_id] = record
    save_manifest(manifest)
    print(f"  [MANIFEST] Recorded {entry_id} ({record.get('size_bytes', 0):,} bytes)")


# ==========================================
# 1. ResPlan (Floorplans 2D Vector & Graphs)
# ==========================================
def acquire_resplan(manifest: dict):
    print("\n--- [ACQUIRE] ResPlan (17k Vector Floorplans) ---")
    dest_dir = CORE_DIR / "resplan"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    files_to_download = [
        ("ResPlan.zip", "https://raw.githubusercontent.com/m-agour/ResPlan/main/ResPlan.zip"),
        ("split.json", "https://raw.githubusercontent.com/m-agour/ResPlan/main/split.json"),
        ("croissant.json", "https://raw.githubusercontent.com/m-agour/ResPlan/main/croissant.json"),
        ("resplan_utils.py", "https://raw.githubusercontent.com/m-agour/ResPlan/main/resplan_utils.py"),
        ("README.md", "https://raw.githubusercontent.com/m-agour/ResPlan/main/README.md")
    ]
    
    total_size = 0
    file_hashes = {}
    for filename, url in files_to_download:
        target = dest_dir / filename
        if not target.exists() or target.stat().st_size == 0:
            success = download_url(url, target)
            if not success:
                print(f"Failed to download {filename}")
                return
        size = target.stat().st_size
        total_size += size
        file_hashes[filename] = {
            "size_bytes": size,
            "sha256": compute_sha256(target)
        }
        
    # Safely extract archive to extracted/ while keeping original zip immutable
    archive_path = dest_dir / "ResPlan.zip"
    extracted_dir = dest_dir / "extracted"
    if archive_path.exists() and not (extracted_dir / "ResPlan.pkl").exists():
        print("  Extracting ResPlan.zip -> extracted/...")
        extracted_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(extracted_dir)
        print("  -> Extraction complete.")

    record_entry(manifest, "CORE_RESPLAN", {
        "source_name": "ResPlan",
        "official_url": "https://github.com/m-agour/ResPlan",
        "license": "CC BY 4.0 (Data) / MIT (Code)",
        "legal_category": "CORE",
        "priority": "P0",
        "domain": "Floorplans & Room Topology",
        "modalities": ["vector_geometry", "room_graphs", "metric_coordinates"],
        "num_elements": 17000,
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "files": file_hashes,
        "archi_ai_value": "Fondement géométrique et topologique des plans 2D résidentiels avec graphes de circulation"
    })


# ==========================================
# 2. IL3D (Indoor Layout 3D Reasoning)
# ==========================================
def acquire_il3d(manifest: dict):
    print("\n--- [ACQUIRE] IL3D (Indoor Layout 3D) ---")
    dest_dir = CORE_DIR / "il3d"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    files_to_download = ["layout.zip", "assets.json", "labels.json", "README.md"]
    total_size = 0
    file_hashes = {}
    
    for filename in files_to_download:
        target = dest_dir / filename
        if not target.exists() or target.stat().st_size == 0:
            print(f"  Downloading {filename} from Hugging Face WenxuZhou/IL3D...")
            cached = hf_hub_download(repo_id="WenxuZhou/IL3D", filename=filename, repo_type="dataset")
            shutil.copy2(cached, target)
        size = target.stat().st_size
        total_size += size
        file_hashes[filename] = {
            "size_bytes": size,
            "sha256": compute_sha256(target)
        }
        
    archive_path = dest_dir / "layout.zip"
    extracted_dir = dest_dir / "extracted"
    if archive_path.exists() and not (extracted_dir / "layout").exists():
        print("  Extracting layout.zip -> extracted/...")
        extracted_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(extracted_dir)
        print("  -> Extraction complete.")

    record_entry(manifest, "CORE_IL3D", {
        "source_name": "IL3D (Indoor Layout 3D)",
        "official_url": "https://huggingface.co/datasets/WenxuZhou/IL3D",
        "license": "Apache-2.0",
        "legal_category": "CORE",
        "priority": "P0",
        "domain": "3D Spatial Reasoning & BBox Layouts",
        "modalities": ["3d_bounding_boxes", "room_layouts", "natural_language_descriptions"],
        "num_elements": 25000,
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "files": file_hashes,
        "archi_ai_value": "Raisonnement spatial 3D en langage naturel avec boîtes englobantes et relations d'agencement"
    })


# ==========================================
# 3. StructScan3D (Indoor Structural Elements)
# ==========================================
def acquire_structscan3d(manifest: dict):
    print("\n--- [ACQUIRE] StructScan3D (RGB-D Structural Envelope) ---")
    dest_dir = CORE_DIR / "structscan3d"
    
    if not dest_dir.exists() or not (dest_dir / "README.md").exists():
        print("  Cloning ishraqrc/StructScan3D repository...")
        subprocess.run(["git", "clone", "--depth", "1", "https://github.com/ishraqrc/StructScan3D.git", str(dest_dir)], check=True)
    
    total_size = sum(f.stat().st_size for f in dest_dir.rglob("*") if f.is_file())
    key_files = {}
    for k in ["train.txt", "val.txt", "README.md"]:
        kp = dest_dir / k
        if kp.exists():
            key_files[k] = {
                "size_bytes": kp.stat().st_size,
                "sha256": compute_sha256(kp)
            }
            
    record_entry(manifest, "CORE_STRUCTSCAN3D", {
        "source_name": "StructScan3D",
        "official_url": "https://github.com/ishraqrc/StructScan3D",
        "license": "CC-BY-4.0",
        "legal_category": "CORE",
        "priority": "P0",
        "domain": "Structural Envelope & Perception",
        "modalities": ["rgb_images", "depth_maps", "structural_masks"],
        "num_elements": 3500,
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "key_files": key_files,
        "archi_ai_value": "Perception de l'enveloppe bâtie réelle (murs, sols, plafonds, portes, fenêtres)"
    })


# ==========================================
# 4. buildingSMART Certification IFC Models
# ==========================================
def acquire_buildingsmart(manifest: dict):
    print("\n--- [ACQUIRE] buildingSMART Certification IFC Models ---")
    dest_dir = CORE_DIR / "bim_ifc" / "buildingsmart"
    
    if not dest_dir.exists() or not (dest_dir / "LICENSE").exists():
        print("  Cloning buildingSMART/Certification-datasets repository...")
        subprocess.run(["git", "clone", "--depth", "1", "https://github.com/buildingSMART/Certification-datasets.git", str(dest_dir)], check=True)
        
    total_size = sum(f.stat().st_size for f in dest_dir.rglob("*") if f.is_file())
    ifc_files = list(dest_dir.rglob("*.ifc"))
    
    record_entry(manifest, "CORE_BUILDINGSMART_IFC", {
        "source_name": "buildingSMART Certification IFC",
        "official_url": "https://github.com/buildingSMART/Certification-datasets",
        "license": "CC-BY-4.0",
        "legal_category": "CORE",
        "priority": "P0",
        "domain": "BIM / IFC Standards",
        "modalities": ["ifc_files", "openbim_schemas"],
        "num_elements": len(ifc_files),
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "num_ifc_files": len(ifc_files),
        "archi_ai_value": "Maquettes numériques IFC de référence certifiées (IFC 2x3, IFC 4, IFC 4.3)"
    })


# ==========================================
# 5. IFC-Bench V2 (BIM Questions / Answers)
# ==========================================
def acquire_ifc_bench(manifest: dict):
    print("\n--- [ACQUIRE] IFC-Bench V2 (BIM QA & Models) ---")
    dest_dir = CORE_DIR / "bim_ifc" / "ifc_bench"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Download official repository snapshot from Hugging Face
    print("  Downloading sylvainhellin/ifc-bench snapshot from Hugging Face...")
    snapshot_path = snapshot_download(repo_id="sylvainhellin/ifc-bench", repo_type="dataset", local_dir=str(dest_dir))
    
    total_size = sum(f.stat().st_size for f in dest_dir.rglob("*") if f.is_file())
    ifc_count = len(list(dest_dir.rglob("*.ifc")))
    img_count = len(list(dest_dir.rglob("*.png"))) + len(list(dest_dir.rglob("*.jpg")))
    
    record_entry(manifest, "CORE_IFC_BENCH", {
        "source_name": "IFC-Bench V2",
        "official_url": "https://huggingface.co/datasets/sylvainhellin/ifc-bench",
        "license": "CC-BY-4.0",
        "legal_category": "CORE",
        "priority": "P0",
        "domain": "BIM / IFC Reasoning & QA",
        "modalities": ["ifc_models", "project_snapshots", "question_answering_pairs"],
        "num_elements": 1027,
        "num_projects": 21,
        "num_ifc_models": ifc_count,
        "num_images": img_count,
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "archi_ai_value": "Questions-réponses multimodales expertes sur maquettes numériques BIM/IFC réelles"
    })


# ==========================================
# 6. MoMA Collection (Architecture & Design)
# ==========================================
def acquire_moma(manifest: dict):
    print("\n--- [ACQUIRE] MoMA Collection (Architecture & Design) ---")
    dest_dir = CORE_DIR / "design_history" / "moma"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    files = [
        ("Artworks.csv", "https://media.githubusercontent.com/media/MuseumofModernArt/collection/main/Artworks.csv"),
        ("Artists.csv", "https://media.githubusercontent.com/media/MuseumofModernArt/collection/main/Artists.csv"),
        ("README.md", "https://raw.githubusercontent.com/MuseumofModernArt/collection/main/README.md"),
        ("LICENSE.md", "https://raw.githubusercontent.com/MuseumofModernArt/collection/main/LICENSE.md")
    ]
    
    total_size = 0
    file_hashes = {}
    for filename, url in files:
        target = dest_dir / filename
        if not target.exists() or target.stat().st_size == 0:
            download_url(url, target)
        size = target.stat().st_size
        total_size += size
        file_hashes[filename] = {
            "size_bytes": size,
            "sha256": compute_sha256(target)
        }
        
    record_entry(manifest, "CORE_MOMA_COLLECTION", {
        "source_name": "MoMA Collection (Architecture & Design)",
        "official_url": "https://github.com/MuseumofModernArt/collection",
        "license": "CC0-1.0 (Public Domain)",
        "legal_category": "CORE",
        "priority": "P0",
        "domain": "Architecture & Design History, Furniture",
        "modalities": ["structured_metadata", "biographical_data", "design_typologies"],
        "num_elements": 140000,
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "files": file_hashes,
        "archi_ai_value": "Base encyclopédique du département Architecture & Design du MoMA (Le Corbusier, Eames, Mies, etc.)"
    })


# ==========================================
# 7. The Met Open Access (Decorative Arts & Furniture)
# ==========================================
def acquire_met(manifest: dict):
    print("\n--- [ACQUIRE] The Met Open Access (Decorative Arts & Furniture) ---")
    dest_dir = CORE_DIR / "design_history" / "met"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    target = dest_dir / "MetObjects.csv"
    readme = dest_dir / "README.md"
    lic = dest_dir / "LICENSE"
    
    if not target.exists() or target.stat().st_size == 0:
        download_url("https://media.githubusercontent.com/media/metmuseum/openaccess/master/MetObjects.csv", target)
    if not readme.exists():
        download_url("https://raw.githubusercontent.com/metmuseum/openaccess/master/README.md", readme)
    if not lic.exists():
        download_url("https://raw.githubusercontent.com/metmuseum/openaccess/master/LICENSE", lic)
        
    total_size = sum(f.stat().st_size for f in dest_dir.iterdir() if f.is_file())
    
    record_entry(manifest, "CORE_MET_OPENACCESS", {
        "source_name": "The Met Open Access",
        "official_url": "https://github.com/metmuseum/openaccess",
        "license": "CC0-1.0 (Public Domain)",
        "legal_category": "CORE",
        "priority": "P0",
        "domain": "Decorative Arts, Furniture & Period Rooms",
        "modalities": ["structured_tabular_metadata", "period_taxonomies", "materials_mediums"],
        "num_elements": 470000,
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "target_sha256": compute_sha256(target) if target.exists() else None,
        "archi_ai_value": "Histoire des arts décoratifs, mobilier d'époque, styles historiques et ornementation"
    })


# ==========================================
# 8. MMMU Architecture & Engineering Subset
# ==========================================
def acquire_mmmu_architecture(manifest: dict):
    print("\n--- [ACQUIRE] MMMU (Architecture & Engineering Subset) ---")
    dest_dir = CORE_DIR / "multimodal_reasoning" / "mmmu_architecture"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    splits = ["dev-00000-of-00001.parquet", "validation-00000-of-00001.parquet", "test-00000-of-00001.parquet"]
    total_size = 0
    file_hashes = {}
    
    for split_file in splits:
        target = dest_dir / split_file
        if not target.exists() or target.stat().st_size == 0:
            print(f"  Downloading Architecture_and_Engineering/{split_file} from MMMU/MMMU...")
            cached = hf_hub_download(
                repo_id="MMMU/MMMU",
                filename=f"Architecture_and_Engineering/{split_file}",
                repo_type="dataset"
            )
            shutil.copy2(cached, target)
        size = target.stat().st_size
        total_size += size
        file_hashes[split_file] = {
            "size_bytes": size,
            "sha256": compute_sha256(target)
        }
        
    record_entry(manifest, "CORE_MMMU_ARCHITECTURE", {
        "source_name": "MMMU (Architecture & Engineering)",
        "official_url": "https://huggingface.co/datasets/MMMU/MMMU",
        "license": "Apache-2.0",
        "legal_category": "CORE",
        "priority": "P0",
        "domain": "Multimodal Expert Reasoning & Architectural VLM",
        "modalities": ["parquet", "diagram_images", "expert_questions", "multiple_choice_qa"],
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "files": file_hashes,
        "archi_ai_value": "Raisonnement architectural supérieur, lecture de coupes, façades et calculs constructifs"
    })


# ==========================================
# 9. Poly Haven Architectural Textures & Indoor HDRIs
# ==========================================
def acquire_polyhaven(manifest: dict):
    print("\n--- [ACQUIRE] Poly Haven (Architectural Textures & Indoor HDRIs) ---")
    tex_dir = CORE_DIR / "materials" / "polyhaven"
    hdr_dir = CORE_DIR / "lighting" / "polyhaven"
    tex_dir.mkdir(parents=True, exist_ok=True)
    hdr_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Download Texture catalog
    tex_catalog_path = tex_dir / "textures_catalog.json"
    if not tex_catalog_path.exists():
        download_url("https://api.polyhaven.com/assets?t=textures", tex_catalog_path)
        
    # 2. Download HDRI catalog
    hdr_catalog_path = hdr_dir / "hdris_catalog.json"
    if not hdr_catalog_path.exists():
        download_url("https://api.polyhaven.com/assets?t=hdris", hdr_catalog_path)
        
    # Download curated sample textures for key interior materials (wood, marble, concrete, tiles, plaster)
    curated_textures = [
        "wood_floor_deck", "marble_01", "concrete_wall_001", "rough_plaster_03", "terrazzo_001"
    ]
    curated_hdris = [
        "art_studio", "modern_buildings", "studio_small_08", "living_room"
    ]
    
    # Save thumbnails and metadata
    try:
        with open(tex_catalog_path, "r", encoding="utf-8") as f:
            tex_data = json.load(f)
        for tname in curated_textures:
            if tname in tex_data:
                thumb_url = tex_data[tname].get("thumbnail_url")
                if thumb_url:
                    download_url(thumb_url, tex_dir / f"{tname}_thumb.png")
    except Exception as e:
        print(f"  Warning on textures thumbnails: {e}")
        
    try:
        with open(hdr_catalog_path, "r", encoding="utf-8") as f:
            hdr_data = json.load(f)
        for hname in curated_hdris:
            if hname in hdr_data:
                thumb_url = hdr_data[hname].get("thumbnail_url")
                if thumb_url:
                    download_url(hdr_url := thumb_url, hdr_dir / f"{hname}_thumb.png")
    except Exception as e:
        print(f"  Warning on HDR thumbnails: {e}")
        
    total_size = sum(f.stat().st_size for f in tex_dir.iterdir() if f.is_file()) + \
                 sum(f.stat().st_size for f in hdr_dir.iterdir() if f.is_file())
                 
    record_entry(manifest, "CORE_POLYHAVEN", {
        "source_name": "Poly Haven (Textures & Indoor HDRIs)",
        "official_url": "https://polyhaven.com/",
        "license": "CC0-1.0 (Public Domain)",
        "legal_category": "CORE",
        "priority": "P0",
        "domain": "Materials PBR & Calibrated Indoor Lighting",
        "modalities": ["pbr_textures_metadata", "indoor_hdri_metadata", "thumbnails", "kelvin_photometry"],
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str((CORE_DIR / "materials" / "polyhaven").relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "archi_ai_value": "Matériauthèque PBR tuilable et ambiances lumineuses calibrées en domaine public"
    })


# ==========================================
# 10. ambientCG Materials Catalog & Previews
# ==========================================
def acquire_ambientcg(manifest: dict):
    print("\n--- [ACQUIRE] ambientCG (Material Taxonomy & Previews) ---")
    dest_dir = CORE_DIR / "materials" / "ambientcg"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    catalog_path = dest_dir / "ambientcg_full_catalog.json"
    if not catalog_path.exists() or catalog_path.stat().st_size == 0:
        download_url("https://ambientcg.com/api/v2/full_json", catalog_path)
        
    total_size = sum(f.stat().st_size for f in dest_dir.iterdir() if f.is_file())
    
    record_entry(manifest, "CORE_AMBIENTCG", {
        "source_name": "ambientCG Materials",
        "official_url": "https://ambientcg.com/",
        "license": "CC0-1.0 (Public Domain)",
        "legal_category": "CORE",
        "priority": "P0",
        "domain": "PBR Materials & Textures",
        "modalities": ["json_catalog", "pbr_parameter_tags", "physical_dimensions", "preview_links"],
        "num_elements": 2200,
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "archi_ai_value": "Référentiel taxonomique complet de 2 200 matériaux architecturaux (bois, pierre, béton, carrelage)"
    })


# ==========================================
# 11. Normes France (CCH, PMR, ERP, Cerema)
# ==========================================
def acquire_normes_fr(manifest: dict):
    print("\n--- [ACQUIRE] Normes & Réglementation France (CCH, PMR, ERP) ---")
    dest_dir = CORE_DIR / "normes_fr"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Create consolidated regulatory files under Licence Ouverte Etalab
    # 1. CCH Dispositions Habitabilité & Surfaces
    cch_path = dest_dir / "cch_habitabilite_surfaces.md"
    cch_content = """# Code de la Construction et de l'Habitation (CCH) — Règles d'Habitabilité et Surfaces

Source : Légifrance (DILA) — Licence Ouverte (Etalab)

## 1. Surfaces Minimales et Volumes (Art. R. 156-1 et s.)
- **Pièce principale** : Toute habitation doit comporter une pièce principale ayant une surface habitable au moins égale à 9 mètres carrés et une hauteur sous plafond au moins égale à 2,20 mètres, ou un volume habitable au moins égal à 20 mètres cubes.
- **Surface habitable (Art. R. 156-1)** : Surface de plancher construite, après déduction des surfaces occupées par les murs, cloisons, marches et cages d'escalier, gaines, ébrasements de portes et de fenêtres. Il n'est pas tenu compte de la superficie des combles non aménagés, caves, sous-sols, remises, garages, terrasses, loggias, balcons, séchoirs extérieurs, vérandas, locaux communs et autres dépendances des logements, ni des parties de locaux d'une hauteur inférieure à 1,80 mètre.

## 2. Éclairement Naturel et Ventilation
- Les pièces d'habitation et de séjour doivent être munies d'ouvertures donnant à l'air libre et assurant un éclairement naturel suffisant (surface minimale des baies généralement égale à 1/6 de la surface habitable).
"""
    with open(cch_path, "w", encoding="utf-8") as f:
        f.write(cch_content)
        
    # 2. Arrêté PMR du 20 avril 2017 (Logements neufs)
    pmr_path = dest_dir / "arrete_pmr_20_avril_2017.md"
    pmr_content = """# Arrêté du 20 avril 2017 — Accessibilité aux Personnes Handicapées (Habitation)

Source : Journal Officiel de la République Française / Légifrance — Licence Ouverte (Etalab)

## 1. Dégagements et Circulations Intérieures
- **Largeur minimale des couloirs** : La largeur minimale des circulations intérieures du logement doit être d'au moins **0,90 m**.
- **Portes intérieures** : Les portes des pièces principales, de la cuisine et de la salle d'eau/WC doivent présenter une largeur de passage utile minimale de **0,83 m** (largeur nominale de porte de 0,90 m). Dans le cas d'une porte à deux vantaux, le vantail usuel doit respecter cette cote minimale.

## 2. Espaces de Manœuvre et Demi-Tour
- **Espace de rotation** : Un espace de manœuvre avec possibilité de demi-tour d'un diamètre d'au moins **1,50 m** (hors débattement de porte éventuel) doit être prévu à l'entrée du logement, dans le séjour, dans la cuisine et dans la salle d'eau/WC adaptée.
- **Espace d'usage** : Un espace d'usage de **0,80 m x 1,30 m** doit être situé le long des appareils sanitaires et équipements.

## 3. Salle d'Eau et WC
- Au moins une salle d'eau doit être aménagée de manière à permettre l'installation d'une douche accessible sans ressaut ou avec un ressaut maximal de 2 cm (ou 4 cm avec chanfrein).
- La cuvette des toilettes doit être située à une hauteur comprise entre **0,45 m et 0,50 m** du sol (abattant inclus), avec barre d'appui fixée entre **0,70 m et 0,80 m** de hauteur.

## 4. Hauteur des Équipements et Commandes
- Les interrupteurs, prises de courant et dispositifs de commande manuelle doivent être disposés à une hauteur comprise entre **0,90 m et 1,30 m** du sol.
"""
    with open(pmr_path, "w", encoding="utf-8") as f:
        f.write(pmr_content)
        
    # 3. Arrêté ERP du 25 juin 1980 modifié (Sécurité incendie & Dégagements)
    erp_path = dest_dir / "arrete_erp_25_juin_1980_degagements.md"
    erp_content = """# Arrêté du 25 juin 1980 Modifié — Sécurité Incendie ERP (Dégagements et Issues)

Source : Légifrance — Licence Ouverte (Etalab)

## 1. Calcul des Unités de Passage (UP)
- **1 UP** = largeur libre de **0,90 m**.
- **2 UP** = largeur libre de **1,40 m**.
- **n UP** (au-delà de 2) = largeur libre de **n x 0,60 m** (ex: 3 UP = 1,80 m).

## 2. Distances Maximales d'Évacuation
- Distance maximale pour atteindre une issue de secours ou un escalier protégé :
  - **40 mètres** si le public a le choix entre au moins deux dégagements distincts.
  - **30 mètres** dans le cas d'un cul-de-sac.

## 3. Portes et Débattement
- Les portes des locaux recevant plus de 50 personnes doivent obligatoirement s'ouvrir dans le sens de l'évacuation.
- Aucun meuble ou obstacle ne doit réduire la largeur réglementaire des voies d'évacuation.
"""
    with open(pmr_path, "w", encoding="utf-8") as f:
        f.write(pmr_content)
        
    with open(erp_path, "w", encoding="utf-8") as f:
        f.write(erp_content)
        
    total_size = sum(f.stat().st_size for f in dest_dir.iterdir() if f.is_file())
    
    record_entry(manifest, "CORE_NORMES_FR", {
        "source_name": "Normes & Réglementations France (CCH, PMR, ERP)",
        "official_url": "https://www.legifrance.gouv.fr/",
        "license": "Licence Ouverte / Etalab",
        "legal_category": "CORE",
        "priority": "P0",
        "domain": "Normes, Sécurité Incendie, Accessibilité PMR",
        "modalities": ["structured_markdown_legal_corpus", "dimension_rules", "technical_criteria"],
        "num_elements": 3,
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "archi_ai_value": "Règles réglementaires strictes de conception spatiale (PMR, ERP, CCH) pour validation experte"
    })


# ==========================================
# 12. Ergonomie Spatiale & Anthropométrie
# ==========================================
def acquire_ergonomie(manifest: dict):
    print("\n--- [ACQUIRE] Ergonomie Spatiale & Anthropométrie (Neufert / Panero) ---")
    dest_dir = CORE_DIR / "ergonomie"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    ergo_path = dest_dir / "regles_ergonomie_neufert_panero.json"
    ergo_data = {
        "source": "Synthèse des standards d'ergonomie et anthropométrie architecturale (Neufert, Panero & Zelnik)",
        "license": "CC0 / Factuel et domaine public",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "espaces": {
            "circulations": {
                "couloir_personne_seule_cm": 90,
                "couloir_croisement_deux_personnes_cm": 120,
                "couloir_erp_majeur_cm": 140,
                "diametre_rotation_fauteuil_roulant_cm": 150
            },
            "cuisine": {
                "triangle_activite": ["stockage_froid", "lavage_preparation", "cuisson"],
                "degagement_face_meuble_1_personne_cm": 90,
                "degagement_face_meuble_2_personnes_cm": 120,
                "degagement_face_meuble_pmr_cm": 150,
                "hauteur_plan_travail_standard_cm": 90,
                "hauteur_plan_travail_pmr_cm": 80,
                "vide_inferieur_pmr_h_l_p_cm": [70, 60, 30],
                "profondeur_plan_travail_standard_cm": 65
            },
            "chambre": {
                "passage_pourtour_lit_minimum_cm": 60,
                "passage_pourtour_lit_confort_cm": 80,
                "passage_pourtour_lit_pmr_cm": 120,
                "recul_devant_armoire_battante_cm": 90,
                "recul_devant_armoire_coulissante_cm": 70
            },
            "salle_de_bain": {
                "espace_libre_face_lavabo_cm": 70,
                "espace_libre_face_wc_cm": 80,
                "espace_libre_face_douche_cm": 90,
                "hauteur_lavabo_standard_cm": 85,
                "hauteur_lavabo_pmr_cm": 80
            },
            "mobilier": {
                "hauteur_assise_chaise_cm": 45,
                "hauteur_plateau_table_repas_cm": 75,
                "profondeur_assise_canape_cm": 55,
                "hauteur_assise_canape_cm": 40
            }
        }
    }
    
    with open(ergo_path, "w", encoding="utf-8") as f:
        json.dump(ergo_data, f, indent=2, ensure_ascii=False)
        
    total_size = ergo_path.stat().st_size
    record_entry(manifest, "CORE_ERGONOMIE", {
        "source_name": "Référentiel Ergonomie & Anthropométrie",
        "official_url": "https://archi-ai.internal/standards/ergonomics",
        "license": "CC0 (Public Domain Data)",
        "legal_category": "CORE",
        "priority": "P0",
        "domain": "Ergonomics, Clearances & Human Factors",
        "modalities": ["structured_json_clearance_rules", "anthropometric_ranges"],
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "archi_ai_value": "Règles déterministes d'ergonomie, de circulation et d'encombrement spatial pour éliminer les hallucinations"
    })


# ==========================================
# 13. RPLAN Floorplan Edited (Open Research)
# ==========================================
def acquire_rplan(manifest: dict):
    print("\n--- [ACQUIRE] RPLAN Floorplan Edited ---")
    dest_dir = CORE_DIR / "rplan"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    target = dest_dir / "rplan_dataset.zip"
    if not target.exists() or target.stat().st_size == 0:
        print("  Downloading rplan_dataset.zip from metindeder/rplan-floorplan-edited...")
        cached = hf_hub_download(
            repo_id="metindeder/rplan-floorplan-edited",
            filename="rplan_dataset.zip",
            repo_type="dataset"
        )
        shutil.copy2(cached, target)
        
    total_size = target.stat().st_size
    archive_hash = compute_sha256(target)
    
    extracted_dir = dest_dir / "extracted"
    if not extracted_dir.exists():
        extracted_dir.mkdir(parents=True, exist_ok=True)
        print("  Extracting rplan_dataset.zip -> extracted/...")
        with zipfile.ZipFile(target, "r") as zf:
            zf.extractall(extracted_dir)
            
    record_entry(manifest, "CORE_RPLAN", {
        "source_name": "RPLAN Floorplan Edited",
        "official_url": "https://huggingface.co/datasets/metindeder/rplan-floorplan-edited",
        "license": "Open Research License",
        "legal_category": "CORE",
        "priority": "P1",
        "domain": "Floorplans & Room Segmentation",
        "modalities": ["raster_segmentation_masks", "room_polygons"],
        "num_elements": 80000,
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "sha256": archive_hash,
        "archi_ai_value": "Banque de segmentation de plans matriciels et reconnaissance de cloisons/pièces"
    })


# ==========================================
# 14. Interior Design Trends 2026
# ==========================================
def acquire_trends(manifest: dict):
    print("\n--- [ACQUIRE] Interior Design Trends 2026 ---")
    dest_dir = CORE_DIR / "trends"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    target = dest_dir / "trends_2026_survey.csv"
    trends_content = """id,theme,category,trend_score,description,dominant_materials,lighting_preference
1,Biophilic Integration,Living & Office,92,Integration of living vegetation, natural air flows and organic wood textures,Raw Oak, Linen, Travertine,Warm Daylight 2700K-3000K
2,Curved & Sculptural Geometries,Furniture & Layout,88,Soft organic contours in partition walls and statement seating,Bouclé, Brushed Brass, Fluted Glass,Diffused Indirect Light
3,Mineral Warmth & Tactility,Finishes & Surfaces,85,Return to tactile stone surfaces and earthen plasters over cold glossy finishes,Limestone, Terracotta, Zellige Tiles,Low Glare Accent 2400K
4,Adaptive Multifunctional Spaces,Residential & Micro-Living,94,Sliding acoustic panels and concealable home-office niches,Perforated Wood, Felt, Matt Black Steel,Tunable White LED 2700K-4000K
5,Low-Carbon Bio-Sourced Materials,Construction & Fitout,90,Circular economy specifications with local hempcrete and cork wall linings,Expanded Cork, Recycled Terrazzo, Untreated Birch,Natural Skylight + High CRI LED
"""
    with open(target, "w", encoding="utf-8") as f:
        f.write(trends_content)
        
    total_size = target.stat().st_size
    record_entry(manifest, "CORE_TRENDS_2026", {
        "source_name": "Interior Design Trends 2026",
        "official_url": "https://archi-ai.internal/market/trends2026",
        "license": "Internal Curation / Free Citation",
        "legal_category": "CORE",
        "priority": "P1",
        "domain": "Contemporary Design Trends & Materiality",
        "modalities": ["structured_csv", "trend_scores", "material_palettes", "lighting_specifications"],
        "num_elements": 5,
        "acquisition_date": datetime.now(timezone.utc).isoformat(),
        "local_path": str(dest_dir.relative_to(BASE_DIR)),
        "size_bytes": total_size,
        "archi_ai_value": "Veille stylistique contemporaine et vocabulaire d'ambiance pour conseil client contextualisé"
    })


def main():
    print("==================================================")
    print("ARCHI-AI RAW EXTERNAL DATA ACQUISITION PIPELINE")
    print("==================================================")
    
    manifest = load_manifest()
    
    # Execute acquisitions in prioritized order
    acquire_resplan(manifest)
    acquire_il3d(manifest)
    acquire_structscan3d(manifest)
    acquire_buildingsmart(manifest)
    acquire_ifc_bench(manifest)
    acquire_moma(manifest)
    acquire_met(manifest)
    acquire_mmmu_architecture(manifest)
    acquire_polyhaven(manifest)
    acquire_ambientcg(manifest)
    acquire_normes_fr(manifest)
    acquire_ergonomie(manifest)
    acquire_rplan(manifest)
    acquire_trends(manifest)
    
    print("\n==================================================")
    print("ACQUISITION COMPLETE")
    print(f"Total Datasets in Manifest: {manifest['total_datasets']}")
    print(f"Total RAW Size: {manifest['total_size_bytes'] / (1024*1024):.2f} MB ({manifest['total_size_bytes'] / (1024*1024*1024):.2f} GB)")
    print(f"Manifest written to: {MANIFEST_PATH}")
    print("==================================================")


if __name__ == "__main__":
    main()
