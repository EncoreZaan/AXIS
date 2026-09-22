#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARCHI-AI: Migration des 25 exemples historiques vers le Master Schema
====================================================================
Migre train.jsonl (20) et validation.jsonl (5) vers dataset/master/annotations/master_annotations.jsonl
sans altérer le contenu textuel ni les conversations existantes.
Versionnée : v0.1-micro-baseline.
"""

import os
import sys
import json
from typing import Dict, Any, List

# Assurer l'accès aux modules internes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dataset_tools.validation.taxonomy import (
    DocumentType,
    Domain,
    DifficultyLevel,
    LearningType,
    Skill,
    QAStatus,
    SplitName,
    LEGACY_CATEGORY_TO_SKILLS
)
from dataset.master.schema.models import MasterAnnotation, ImageItem, Provenance
from dataset_tools.deduplication.hasher import get_image_info


def parse_answer_sections(answer_text: str) -> Dict[str, List[str]]:
    """Extrait facultativement les sections si présentes sans rien casser."""
    sections = {
        "observables": [],
        "interpretations": [],
        "unknowns": [],
        "constraints": []
    }
    current_key = None
    lines = answer_text.splitlines()
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
        if line_clean == "OBSERVATION":
            current_key = "observables"
        elif line_clean == "ANALYSE":
            current_key = "interpretations"
        elif line_clean == "POINTS DE VIGILANCE":
            current_key = "unknowns"
        elif line_clean == "POINTS FORTS":
            current_key = "constraints"
        elif line_clean == "RECOMMANDATION":
            current_key = None
        else:
            if current_key and line_clean.startswith("- "):
                sections[current_key].append(line_clean[2:].strip())
    return sections


def infer_learning_type(category: str, question: str) -> LearningType:
    """Déduit le type d'apprentissage principal."""
    q_lower = question.lower()
    cat_upper = category.upper()
    
    if "critique" in cat_upper or "critiquez" in q_lower:
        return LearningType.CRITIQUE
    elif "ergonomie" in cat_upper or "usage" in cat_upper or "norme" in q_lower or "circulation" in q_lower:
        return LearningType.CONSTRAINT_REASONING
    elif "matériaux" in cat_upper or "style" in cat_upper:
        return LearningType.ANALYSIS
    elif "observation" in q_lower or "décrivez" in q_lower:
        return LearningType.OBSERVATION
    elif "pédagogie" in cat_upper:
        return LearningType.PEDAGOGY
    return LearningType.ANALYSIS


def migrate_historical_dataset(base_dir: str):
    """Effectue la migration des 25 exemples historiques vers le Master Dataset."""
    dataset_dir = os.path.join(base_dir, "dataset")
    train_path = os.path.join(dataset_dir, "train.jsonl")
    val_path = os.path.join(dataset_dir, "validation.jsonl")
    
    master_ann_dir = os.path.join(dataset_dir, "master", "annotations")
    os.makedirs(master_ann_dir, exist_ok=True)
    master_file = os.path.join(master_ann_dir, "master_annotations.jsonl")
    
    version_dir = os.path.join(dataset_dir, "versions", "v0.1-micro-baseline")
    os.makedirs(version_dir, exist_ok=True)
    version_master_file = os.path.join(version_dir, "master_annotations.jsonl")
    
    migrated_records: List[MasterAnnotation] = []
    
    files_to_migrate = [
        (train_path, SplitName.TRAIN),
        (val_path, SplitName.VALIDATION)
    ]
    
    for file_path, assigned_split in files_to_migrate:
        if not os.path.exists(file_path):
            print(f"[ERREUR] Fichier introuvable: {file_path}")
            continue
        
        with open(file_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                
                # Image processing
                img_rel = data.get("image", "")
                full_img_path = os.path.join(base_dir, "dataset", img_rel) if not os.path.exists(os.path.join(base_dir, img_rel)) else os.path.join(base_dir, img_rel)
                w, h, sha256, phash = get_image_info(full_img_path)
                
                # Normalize relative path standard inside the repository
                norm_img_rel = f"dataset/{img_rel}" if not img_rel.startswith("dataset/") else img_rel
                
                image_item = ImageItem(
                    path=norm_img_rel,
                    document_type=DocumentType.PHOTOGRAPHY,
                    caption=data.get("context", ""),
                    role="primary",
                    width=w,
                    height=h,
                    sha256=sha256,
                    phash=phash
                )
                
                cat = data.get("category", "ANALYSE D'ESPACE")
                skills = LEGACY_CATEGORY_TO_SKILLS.get(cat, [Skill.ESPACE, Skill.VISION])
                learning_type = infer_learning_type(cat, data.get("question", ""))
                parsed_sections = parse_answer_sections(data.get("answer", ""))
                
                # Scene / image family estimation to protect against split leak
                scene_id = f"scene_{data.get('id', 'unknown')}"
                img_family = f"family_{data.get('space_type', 'gen')}"
                
                prov = Provenance(
                    source_name="historical_micro_dataset",
                    source_url=None,
                    license="proprietary_experimental_reference",
                    project_name=f"Project_{data.get('id')}",
                    scene_id=scene_id,
                    image_family=img_family,
                    collector="audit_baseline_pipeline"
                )
                
                master_entry = MasterAnnotation(
                    id=data["id"],
                    images=[image_item],
                    document_type=DocumentType.PHOTOGRAPHY,
                    domain=Domain.INTERIOR_DESIGN,
                    category=cat,
                    subcategory=data.get("space_type"),
                    space_type=data.get("space_type"),
                    style=data.get("style"),
                    learning_type=learning_type,
                    difficulty=DifficultyLevel.INTERMEDIATE,
                    skills=skills,
                    context=data.get("context", ""),
                    question=data.get("question", ""),
                    answer=data.get("answer", ""),
                    observables=parsed_sections["observables"],
                    interpretations=parsed_sections["interpretations"],
                    unknowns=parsed_sections["unknowns"],
                    constraints=parsed_sections["constraints"],
                    source="archi_historical_25",
                    license="reference_baseline",
                    provenance=prov,
                    qa_status=QAStatus.PASS_STATUS,
                    qa_flags=["HISTORICAL_BASELINE_PROTECTED"],
                    version="v0.1-micro-baseline",
                    assigned_split=assigned_split,
                    metadata={
                        "legacy_category": cat,
                        "legacy_image_path": img_rel,
                        "original_split": assigned_split.value
                    }
                )
                migrated_records.append(master_entry)

    # Sauvegarde des annotations
    with open(master_file, "w", encoding="utf-8") as out_m, open(version_master_file, "w", encoding="utf-8") as out_v:
        for entry in migrated_records:
            line_str = entry.model_dump_json() + "\n"
            out_m.write(line_str)
            out_v.write(line_str)
            
    print(f"Migration réussie : {len(migrated_records)} exemples migrés vers {master_file} et {version_master_file}")
    return len(migrated_records)


if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    migrate_historical_dataset(base_dir)
