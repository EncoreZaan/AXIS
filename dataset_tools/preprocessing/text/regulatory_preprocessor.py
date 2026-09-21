# -*- coding: utf-8 -*-
"""
ARCHI-AI — Préprocesseur Réglementation Française (Normes CCH / PMR / ERP)
===========================================================================
Normalise les textes de loi et arrêtés officiels français :
- Arrêté du 20 avril 2017 (Accessibilité PMR Habitation)
- Arrêté du 25 juin 1980 (Sécurité incendie et dégagements ERP)
- Code de la Construction et de l'Habitation (CCH - Surfaces et habitabilité)

RÈGLES ABSOLUES APPLIQUÉES :
- Ne jamais fabriquer de règles artificielles : texte officiel inaltéré
- Destiné prioritairement au RAG (Recherche documentaire augmentée)
- Routage : RAG
"""

from typing import Iterator, Dict, Any, List, Optional
from pathlib import Path
import re
import time

from dataset_tools.preprocessing.base import BasePreprocessor
from dataset_tools.preprocessing.schema import (
    MasterCanonicalItem,
    ModalityType,
    RoutingType,
    QualityStatus,
    RegulatoryArticle
)


class RegulatoryPreprocessor(BasePreprocessor):
    """Adaptateur de normalisation pour CORE_NORMES_FR."""

    FILES_CONFIG = [
        {
            "rel_path": "core/normes_fr/arrete_pmr_20_avril_2017.md",
            "document": "Arrêté du 20 avril 2017 relatif à l'accessibilité aux personnes handicapées",
            "theme": "Accessibilité Universelle PMR",
            "date": "2017-04-20",
            "jurisdiction": "France"
        },
        {
            "rel_path": "core/normes_fr/arrete_erp_25_juin_1980_degagements.md",
            "document": "Arrêté du 25 juin 1980 modifié portant règlement de sécurité contre l'incendie (ERP)",
            "theme": "Sécurité Incendie & Dégagements ERP",
            "date": "1980-06-25",
            "jurisdiction": "France"
        },
        {
            "rel_path": "core/normes_fr/cch_habitabilite_surfaces.md",
            "document": "Code de la Construction et de l'Habitation (CCH)",
            "theme": "Habitabilité et Surfaces Légales",
            "date": "2024-01-01",
            "jurisdiction": "France"
        }
    ]

    @property
    def source_name(self) -> str:
        return "CORE_NORMES_FR"

    @property
    def modality(self) -> ModalityType:
        return ModalityType.REGULATORY_TEXT

    @property
    def default_routing(self) -> RoutingType:
        return RoutingType.RAG

    def process(self, limit: Optional[int] = None) -> Iterator[MasterCanonicalItem]:
        self.start_time = time.time()
        self.items_processed = 0
        self.items_passed = 0

        for cfg in self.FILES_CONFIG:
            f_path = self.raw_root / cfg["rel_path"]
            if not f_path.exists():
                self.warnings.append(f"Fichier manquant: {f_path}")
                continue

            with open(f_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Découpage par sections (titres ##)
            sections = re.split(r"\n(?=##\s+)", content)
            
            for s_idx, sec_text in enumerate(sections):
                if limit is not None and self.items_processed >= limit:
                    break
                sec_text = sec_text.strip()
                if not sec_text:
                    continue

                self.items_processed += 1
                lines = sec_text.splitlines()
                title_line = lines[0].replace("#", "").strip() if lines else f"Section {s_idx+1}"
                body_text = "\n".join(lines[1:]).strip() if len(lines) > 1 else sec_text

                art_id = f"{Path(cfg['rel_path']).stem}_sec_{s_idx+1}"
                norm_id = f"NORM_REG_{art_id}"
                master_id = f"ARCHI_MASTER_REG_{art_id}"

                reg_article = RegulatoryArticle(
                    article_id=art_id,
                    document=cfg["document"],
                    theme=cfg["theme"],
                    jurisdiction=cfg["jurisdiction"],
                    section=title_line,
                    article_number=None,  # Pas de numéro inventé
                    official_source="Légifrance / Journal Officiel de la République Française",
                    version_date=cfg["date"],
                    text=sec_text,
                    references=[],
                    language="fr"
                )

                provenance = self.build_provenance(
                    raw_file_rel=cfg["rel_path"],
                    raw_element_id=art_id,
                    normalized_id=norm_id,
                    master_id=master_id,
                    transformation_name="RegulatoryPreprocessor.section_chunker",
                    notes=f"Extraction inaltérée: {title_line}"
                )

                item = MasterCanonicalItem(
                    id=master_id,
                    source_id=art_id,
                    source_name=self.source_name,
                    source_license="Licence Ouverte v2.0 (Etalab)",
                    modality=self.modality,
                    data_type="regulatory_article",
                    domain="regulatory",
                    routing=self.default_routing,
                    quality_status=QualityStatus.PASS,
                    provenance=provenance,
                    regulatory=reg_article,
                    metadata={
                        "title": title_line,
                        "document": cfg["document"]
                    }
                )

                self.items_passed += 1
                yield item

        self.end_time = time.time()
