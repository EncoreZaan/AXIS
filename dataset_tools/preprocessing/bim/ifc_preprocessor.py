# -*- coding: utf-8 -*-
"""
ARCHI-AI — Préprocesseur Canonique BIM / IFC
============================================
Normalise les 95 maquettes numériques IFC réelles du corpus ARCHI-AI :
- 35 modèles buildingSMART certifiés (IFC 2x3, IFC 4, IFC 4.3)
- 50 modèles complets IFC-Bench V2 (21 projets réels)
- 10 maquettes 3D résidentielles ResBIM

Optimisation industrielle :
- Utilise IfcOpenShell pour les maquettes <= 15 Mo
- Utilise un parseur STEP streaming ultra-rapide pour les grandes maquettes (> 15 Mo, ex: hôpital 342 Mo)
- Routage : MULTIUSE (FINETUNE + TOOL + RAG)
"""

from typing import Iterator, Dict, Any, List, Optional
from pathlib import Path
import time
import re
import ifcopenshell

from dataset_tools.preprocessing.base import BasePreprocessor
from dataset_tools.preprocessing.schema import (
    MasterCanonicalItem,
    ModalityType,
    RoutingType,
    QualityStatus,
    BimModelSummary
)


class GenericIfcPreprocessor(BasePreprocessor):
    """Adaptateur de base réutilisable pour les maquettes IFC."""

    def __init__(self, raw_root: Path, processed_root: Path, source_name: str, ifc_dir_rel: str, license_str: str):
        super().__init__(raw_root, processed_root)
        self._source_name = source_name
        self._ifc_dir_rel = ifc_dir_rel
        self._license_str = license_str

    @property
    def source_name(self) -> str:
        return self._source_name

    @property
    def modality(self) -> ModalityType:
        return ModalityType.BIM_IFC

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.MULTIUSE

    def _extract_ifc_summary_fast_step(self, file_path: Path) -> BimModelSummary:
        """Parseur STEP streaming ultra-rapide pour les gros fichiers IFC (>15 Mo)."""
        schema = "IFC2X3"
        counts = {}
        proj_name = None
        storeys = []
        spaces = []
        materials = set()

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if "FILE_SCHEMA" in line:
                    m = re.search(r"FILE_SCHEMA\s*\(\s*\(\s*'([^']+)'", line)
                    if m:
                        schema = m.group(1).upper()

                if "=" in line and "(" in line:
                    idx_eq = line.find("=")
                    idx_p = line.find("(", idx_eq)
                    if idx_eq > 0 and idx_p > idx_eq:
                        raw_cls = line[idx_eq + 1:idx_p].strip().upper()
                        if raw_cls.startswith("IFC"):
                            counts[raw_cls] = counts.get(raw_cls, 0) + 1
                            if raw_cls == "IFCPROJECT" and not proj_name:
                                # Essayer d'extraire le nom du projet
                                m_name = re.search(r"'([^']+)'", line[idx_p:])
                                if m_name:
                                    proj_name = m_name.group(1)
                            elif raw_cls == "IFCBUILDINGSTOREY":
                                m_st = re.search(r"'([^']+)'", line[idx_p:])
                                if m_st and len(storeys) < 20:
                                    storeys.append(m_st.group(1))
                            elif raw_cls == "IFCSPACE":
                                m_sp = re.search(r"'([^']+)'", line[idx_p:])
                                if m_sp and len(spaces) < 50:
                                    spaces.append(m_sp.group(1))
                            elif raw_cls == "IFCMATERIAL":
                                m_mat = re.search(r"'([^']+)'", line[idx_p:])
                                if m_mat and len(materials) < 30:
                                    materials.add(m_mat.group(1))

        walls_count = counts.get("IFCWALL", 0) + counts.get("IFCWALLSTANDARDCASE", 0)
        doors_count = counts.get("IFCDOOR", 0)
        windows_count = counts.get("IFCWINDOW", 0)
        slabs_count = counts.get("IFCSLAB", 0)
        columns_count = counts.get("IFCCOLUMN", 0)
        furnishing_count = counts.get("IFCFURNISHINGELEMENT", 0)

        return BimModelSummary(
            model_id=file_path.stem,
            ifc_schema=schema,
            project_name=proj_name or file_path.stem,
            site_name=None,
            building_name=file_path.stem,
            storeys=storeys,
            spaces=spaces,
            element_counts=counts,
            walls_count=walls_count,
            doors_count=doors_count,
            windows_count=windows_count,
            slabs_count=slabs_count,
            columns_count=columns_count,
            furnishing_count=furnishing_count,
            materials_declared=list(materials)
        )

    def _extract_ifc_summary(self, file_path: Path) -> BimModelSummary:
        """Parse le fichier IFC (IfcOpenShell pour <= 15 Mo, streaming STEP au-delà)."""
        file_size = file_path.stat().st_size
        if file_size > 15 * 1024 * 1024:
            return self._extract_ifc_summary_fast_step(file_path)

        model = ifcopenshell.open(str(file_path))
        schema = model.schema

        proj_name, site_name, bldg_name = None, None, None
        projs = model.by_type("IfcProject")
        if projs and projs[0].Name:
            proj_name = str(projs[0].Name)
        sites = model.by_type("IfcSite")
        if sites and sites[0].Name:
            site_name = str(sites[0].Name)
        bldgs = model.by_type("IfcBuilding")
        if bldgs and bldgs[0].Name:
            bldg_name = str(bldgs[0].Name)

        storeys = [str(s.Name) for s in model.by_type("IfcBuildingStorey") if s.Name]
        spaces = [str(sp.Name) for sp in model.by_type("IfcSpace") if sp.Name]

        element_types = [
            "IfcWall", "IfcWallStandardCase", "IfcDoor", "IfcWindow",
            "IfcSlab", "IfcColumn", "IfcBeam", "IfcStair", "IfcRoof",
            "IfcFurnishingElement", "IfcFlowTerminal"
        ]
        counts = {}
        for et in element_types:
            try:
                c = len(model.by_type(et))
                if c > 0:
                    counts[et] = c
            except Exception:
                pass

        walls_count = counts.get("IfcWall", 0) + counts.get("IfcWallStandardCase", 0)
        doors_count = counts.get("IfcDoor", 0)
        windows_count = counts.get("IfcWindow", 0)
        slabs_count = counts.get("IfcSlab", 0)
        columns_count = counts.get("IfcColumn", 0)
        furnishing_count = counts.get("IfcFurnishingElement", 0)

        materials = []
        try:
            for mat in model.by_type("IfcMaterial"):
                if mat.Name and str(mat.Name) not in materials:
                    materials.append(str(mat.Name))
        except Exception:
            pass

        return BimModelSummary(
            model_id=file_path.stem,
            ifc_schema=schema,
            project_name=proj_name,
            site_name=site_name,
            building_name=bldg_name,
            storeys=storeys,
            spaces=spaces,
            element_counts=counts,
            walls_count=walls_count,
            doors_count=doors_count,
            windows_count=windows_count,
            slabs_count=slabs_count,
            columns_count=columns_count,
            furnishing_count=furnishing_count,
            materials_declared=materials[:30]
        )

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        target_dir = self.raw_root / self._ifc_dir_rel
        if not target_dir.exists():
            self.errors.append(f"Répertoire introuvable: {target_dir}")
            self.end_time = time.time()
            return

        ifc_files = sorted(list(target_dir.rglob("*.ifc")))
        if limit is not None:
            ifc_files = ifc_files[:limit]

        for ifc_path in ifc_files:
            self.items_processed += 1
            rel_path = ifc_path.relative_to(self.raw_root).as_posix()
            model_id = ifc_path.stem

            try:
                bim_summary = self._extract_ifc_summary(ifc_path)
            except Exception as e:
                self.warnings.append(f"Erreur parsing IFC {ifc_path.name}: {e}")
                self.items_warning += 1
                continue

            norm_id = f"NORM_{self.source_name}_{model_id}"
            master_id = f"ARCHI_MASTER_{self.source_name}_{model_id}"

            provenance = self.build_provenance(
                raw_file_rel=rel_path,
                raw_element_id=model_id,
                normalized_id=norm_id,
                master_id=master_id,
                transformation_name="GenericIfcPreprocessor.ifcopenshell_extractor",
                notes=f"Modèle {bim_summary.ifc_schema} avec {bim_summary.walls_count} murs, {bim_summary.doors_count} portes"
            )

            item = MasterCanonicalItem(
                id=master_id,
                source_id=model_id,
                source_name=self.source_name,
                source_license=self._license_str,
                modality=self.modality,
                data_type="bim_ifc_model",
                domain="bim",
                routing=self.default_routing,
                quality_status=QualityStatus.PASS,
                provenance=provenance,
                bim=bim_summary,
                metadata={
                    "file_size_bytes": ifc_path.stat().st_size,
                    "rel_path": rel_path
                }
            )

            self.items_passed += 1
            yield item

        self.end_time = time.time()


class BuildingSmartIfcPreprocessor(GenericIfcPreprocessor):
    """Adaptateur spécialisé pour CORE_BUILDINGSMART_IFC."""
    def __init__(self, raw_root: Path, processed_root: Path):
        super().__init__(
            raw_root=raw_root,
            processed_root=processed_root,
            source_name="CORE_BUILDINGSMART_IFC",
            ifc_dir_rel="core/bim_ifc/buildingsmart",
            license_str="CC-BY-4.0"
        )


class IfcBenchModelsPreprocessor(GenericIfcPreprocessor):
    """Adaptateur spécialisé pour les maquettes de CORE_IFC_BENCH."""
    def __init__(self, raw_root: Path, processed_root: Path):
        super().__init__(
            raw_root=raw_root,
            processed_root=processed_root,
            source_name="CORE_IFC_BENCH_MODELS",
            ifc_dir_rel="core/bim_ifc/ifc_bench/projects",
            license_str="CC-BY-4.0"
        )


class ResBimIfcPreprocessor(GenericIfcPreprocessor):
    """Adaptateur spécialisé pour les maquettes 3D de CORE_RESBIM_PAIRED."""
    def __init__(self, raw_root: Path, processed_root: Path):
        super().__init__(
            raw_root=raw_root,
            processed_root=processed_root,
            source_name="CORE_RESBIM_IFC",
            ifc_dir_rel="core/resbim",
            license_str="MIT"
        )
