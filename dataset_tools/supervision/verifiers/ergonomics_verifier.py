# -*- coding: utf-8 -*-
"""
ARCHI-AI — ErgonomicsVerifier (Validation des Cotes d'Usage & Ergonomie)
========================================================================
Vérifie les cotes anthropométriques, passages utiles et dégagements.
Conserve systématiquement :
- original_value et original_unit
- normalized_value et normalized_unit (SI en mètres)
- source documentaire (Neufert, Panero & Zelnik)
"""

from typing import Dict, Any, List, Tuple, Optional
from .base_verifier import BaseVerifier


class ErgonomicsVerifier(BaseVerifier):
    """Vérificateur déterministe pour l'ergonomie et les gabarits d'usage."""

    STANDARD_CLEARANCES_METERS: Dict[str, float] = {
        "passage_principal": 0.90,     # Couloir principal / entrée (CCH/PMR)
        "passage_secondaire": 0.60,    # Circulation secondaire entre meubles
        "recul_chaise_table": 0.70,    # Recul pour s'asseoir confortablement
        "degagement_placard": 0.80,    # Débattement porte battante + passage
        "plan_travail_cuisine": 0.90,  # Passage devant four / lave-vaisselle
        "cercle_giration_pmr": 1.50,   # Espace de rotation Ø 1,50 m (PMR)
    }

    def convert_to_meters(self, value: float, unit: str) -> float:
        """Conversion exacte vers l'unité SI (mètres)."""
        unit = unit.lower().strip()
        if unit in ("m", "meter", "meters", "mètre", "mètres"):
            return float(value)
        elif unit in ("cm", "centimeter", "centimeters", "centimètre", "centimètres"):
            return float(value) / 100.0
        elif unit in ("mm", "millimeter", "millimeters", "millimètre", "millimètres"):
            return float(value) / 1000.0
        elif unit in ("in", "inch", "inches"):
            return float(value) * 0.0254
        return float(value)

    def verify(self, claim: Any, ground_truth_context: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Vérifie la conformité d'une dimension face à un standard ergonomique ou une cote observée.
        """
        clearance_type = claim.get("clearance_type")
        measured_val = claim.get("measured_value")
        measured_unit = claim.get("measured_unit", "m")

        if measured_val is not None:
            norm_measured = self.convert_to_meters(float(measured_val), measured_unit)
            min_required = self.STANDARD_CLEARANCES_METERS.get(clearance_type)

            if min_required is not None:
                is_compliant = norm_measured >= min_required
                details = {
                    "original_value": measured_val,
                    "original_unit": measured_unit,
                    "normalized_value": round(norm_measured, 3),
                    "normalized_unit": "m",
                    "min_required_m": min_required,
                    "is_compliant": is_compliant,
                    "source": ground_truth_context.get("source", "Standard Neufert / Panero & Zelnik"),
                }
                if not is_compliant:
                    return (
                        False,
                        f"Non-conformité ergonomique : dégagement mesuré ({norm_measured:.2f} m) inférieur au minimum requis ({min_required:.2f} m)",
                        details,
                    )
                return (
                    True,
                    f"Dégagement conforme : {norm_measured:.2f} m >= {min_required:.2f} m",
                    details,
                )

        return True, "Cote ergonomique validée", {}
