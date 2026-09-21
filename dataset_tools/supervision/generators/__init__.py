# -*- coding: utf-8 -*-
"""
ARCHI-AI — Package des Générateurs de Supervision
=================================================
"""

from .base_generator import BaseGenerator
from .floorplan_gen import FloorplanGenerator
from .spatial_gen import SpatialGenerator
from .bim_gen import BimGenerator
from .materials_gen import MaterialsGenerator
from .lighting_gen import LightingGenerator
from .ergonomics_gen import ErgonomicsGenerator
from .design_history_gen import DesignHistoryGenerator
from .critique_pedagogy_gen import CritiquePedagogyGenerator
from .multimodal_cross_gen import MultimodalCrossGenerator

ALL_GENERATORS = [
    FloorplanGenerator(),
    SpatialGenerator(),
    BimGenerator(),
    MaterialsGenerator(),
    LightingGenerator(),
    ErgonomicsGenerator(),
    DesignHistoryGenerator(),
    CritiquePedagogyGenerator(),
    MultimodalCrossGenerator(),
]

__all__ = [
    "BaseGenerator",
    "FloorplanGenerator",
    "SpatialGenerator",
    "BimGenerator",
    "MaterialsGenerator",
    "LightingGenerator",
    "ErgonomicsGenerator",
    "DesignHistoryGenerator",
    "CritiquePedagogyGenerator",
    "MultimodalCrossGenerator",
    "ALL_GENERATORS",
]
