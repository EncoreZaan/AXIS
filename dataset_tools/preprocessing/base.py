# -*- coding: utf-8 -*-
"""
ARCHI-AI — Classe de Base pour les Préprocesseurs de Sources RAW
================================================================
Définit le contrat d'interface pour chaque adaptateur de modalité,
garantissant le streaming, la traçabilité de provenance et les métriques d'exécution.
"""

from abc import ABC, abstractmethod
from typing import Iterator, Dict, Any, Optional
from pathlib import Path
import time
import hashlib

from dataset_tools.preprocessing.schema import (
    MasterCanonicalItem,
    ProvenanceRecord,
    QualityStatus,
    RoutingType,
    ModalityType
)


class BasePreprocessor(ABC):
    """Classe abstraite socle pour tous les adaptateurs de données RAW."""

    def __init__(self, raw_root: Path, processed_root: Path):
        self.raw_root = Path(raw_root)
        self.processed_root = Path(processed_root)
        self.processed_root.mkdir(parents=True, exist_ok=True)
        
        self.items_processed = 0
        self.items_passed = 0
        self.items_warning = 0
        self.items_failed = 0
        self.errors = []
        self.warnings = []
        self.start_time = None
        self.end_time = None

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Nom officiel de la source (ex: CORE_RESPLAN)."""
        pass

    @property
    @abstractmethod
    def modality(self) -> ModalityType:
        """Modalité principale traitée."""
        pass

    @property
    @abstractmethod
    def default_routing(self) -> RoutingType:
        """Destination cognitive par défaut."""
        pass

    @abstractmethod
    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        """
        Transforme la source RAW en flux d'enregistrements canoniques MasterCanonicalItem.
        Doit utiliser yield pour permettre le streaming sans explosion mémoire.
        """
        pass

    _SHA_CACHE: Dict[str, Optional[str]] = {}

    def build_provenance(
        self,
        raw_file_rel: str,
        raw_element_id: str,
        normalized_id: str,
        master_id: str,
        transformation_name: Optional[str] = None,
        notes: Optional[str] = None
    ) -> ProvenanceRecord:
        """Construit l'enregistrement de traçabilité immuable."""
        raw_full = self.raw_root / raw_file_rel
        raw_str = str(raw_full)

        if raw_str in self._SHA_CACHE:
            raw_sha = self._SHA_CACHE[raw_str]
        else:
            raw_sha = None
            if raw_full.exists() and raw_full.is_file() and raw_full.stat().st_size < 100 * 1024 * 1024:
                try:
                    with open(raw_full, "rb") as f:
                        raw_sha = hashlib.sha256(f.read()).hexdigest()
                except Exception:
                    pass
            self._SHA_CACHE[raw_str] = raw_sha

        return ProvenanceRecord(
            source_name=self.source_name,
            dataset_name=self.source_name.replace("CORE_", "").lower(),
            raw_file=raw_file_rel.replace("\\", "/"),
            raw_element_id=str(raw_element_id),
            transformation=transformation_name or f"{self.__class__.__name__}.process",
            normalized_id=normalized_id,
            master_id=master_id,
            raw_sha256=raw_sha,
            notes=notes
        )

    def get_stats(self) -> Dict[str, Any]:
        """Retourne les métriques de traitement de la source."""
        duration = (self.end_time - self.start_time) if (self.start_time and self.end_time) else 0.0
        return {
            "source_name": self.source_name,
            "modality": self.modality.value,
            "default_routing": self.default_routing.value,
            "items_processed": self.items_processed,
            "items_passed": self.items_passed,
            "items_warning": self.items_warning,
            "items_failed": self.items_failed,
            "duration_seconds": round(duration, 3),
            "errors": self.errors[:20],
            "warnings": self.warnings[:20]
        }
