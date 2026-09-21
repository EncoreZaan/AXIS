# -*- coding: utf-8 -*-
"""
ARCHI-AI — Préprocesseur Canonique IL3D
=======================================
Normalise les 27 816 scènes d'agencement intérieur 3D d'IL3D :
- Objets 3D avec boîtes englobantes métriques (position, rotation, échelle, dimensions)
- Typologie des pièces et assignation spatiale (roomId)
- Construction d'un scene graph relationnel (ROOM contains OBJECT, co-présence)
- Routage : FINETUNE (Raisonnement spatial 3D)
"""

from typing import Iterator, Dict, Any, List, Optional
from pathlib import Path
import json
import time
from collections import defaultdict

from dataset_tools.preprocessing.base import BasePreprocessor
from dataset_tools.preprocessing.schema import (
    MasterCanonicalItem,
    ModalityType,
    RoutingType,
    QualityStatus,
    SpatialScene,
    SpatialObject
)


class IL3DPreprocessor(BasePreprocessor):
    """Adaptateur de normalisation pour CORE_IL3D."""

    @property
    def source_name(self) -> str:
        return "CORE_IL3D"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.SPATIAL_3D

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.FINETUNE

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        layout_dir = self.raw_root / "core/il3d/extracted/layout"
        if not layout_dir.exists():
            self.errors.append(f"Répertoire introuvable: {layout_dir}")
            self.end_time = time.time()
            return

        json_files = sorted(list(layout_dir.glob("*.json")))
        if limit is not None:
            json_files = json_files[:limit]

        for json_path in json_files:
            self.items_processed += 1
            scene_id = json_path.stem

            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    scene_data = json.load(f)
            except Exception as e:
                self.warnings.append(f"Erreur lecture {json_path.name}: {e}")
                continue

            raw_objects = scene_data.get("objects", [])
            spatial_objects: List[SpatialObject] = []
            rooms_set = set()
            room_to_objects = defaultdict(list)

            for obj_idx, obj in enumerate(raw_objects):
                obj_name = obj.get("object_name", f"obj_{obj_idx}")
                cat = obj.get("category", "furniture")
                label = obj.get("label")
                pos = [round(float(v), 3) for v in obj.get("position", [0.0, 0.0, 0.0])]
                rot = [round(float(v), 3) for v in obj.get("rotation", [0.0, 0.0, 0.0])]
                bbox = [round(float(v), 3) for v in obj.get("bbox", [0.0, 0.0, 0.0])]
                room_id = obj.get("roomId", "UnknownRoom")
                rooms_set.add(room_id)
                room_to_objects[room_id].append(obj_name)

                spatial_objects.append(SpatialObject(
                    object_id=obj_name,
                    category=cat,
                    label=label,
                    position=pos,
                    rotation=rot,
                    dimensions=bbox,
                    room_id=room_id,
                    kinematic=obj.get("kinematic"),
                    asset_id=obj.get("assetId")
                ))

            # Construction du scene graph relationnel
            scene_graph = {
                "rooms": list(rooms_set),
                "room_contains": dict(room_to_objects),
                "spatial_co_presence": {
                    room: [
                        {"pair": [spatial_objects[i].object_id, spatial_objects[j].object_id], "relation": "co_located_in_room"}
                        for i in range(len(spatial_objects))
                        for j in range(i + 1, len(spatial_objects))
                        if spatial_objects[i].room_id == room and spatial_objects[j].room_id == room
                    ][:20]  # Limite de sécurité sur le graphe relationnel dense
                    for room in rooms_set
                }
            }

            spatial_scene = SpatialScene(
                scene_id=scene_id,
                rooms=list(rooms_set),
                objects=spatial_objects,
                scene_graph=scene_graph,
                total_objects=len(spatial_objects),
                coordinate_convention="Y-up, meters"
            )

            norm_id = f"NORM_IL3D_{scene_id}"
            master_id = f"ARCHI_MASTER_IL3D_{scene_id}"

            provenance = self.build_provenance(
                raw_file_rel=f"core/il3d/extracted/layout/{json_path.name}",
                raw_element_id=scene_id,
                normalized_id=norm_id,
                master_id=master_id,
                transformation_name="IL3DPreprocessor.spatial_scene_extractor",
                notes=f"Scène 3D avec {len(spatial_objects)} objets dans {len(rooms_set)} pièces"
            )

            item = MasterCanonicalItem(
                id=master_id,
                source_id=scene_id,
                source_name=self.source_name,
                source_license="Apache-2.0",
                modality=self.modality,
                data_type="3d_scene_layout_graph",
                domain="interior_design",
                routing=self.default_routing,
                quality_status=QualityStatus.PASS,
                provenance=provenance,
                spatial=spatial_scene,
                metadata={
                    "total_objects": len(spatial_objects),
                    "rooms": list(rooms_set),
                    "dataset_origin": scene_data.get("dataset", "HSSD")
                }
            )

            self.items_passed += 1
            yield item

        self.end_time = time.time()
