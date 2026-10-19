"""Preset data: textbook exercises (for verification) and typical materials.

Typical material values are representative mid-range figures for quick
exploration, not design allowables. Carbon fibers in particular span a wide
range (modulus roughly 230–720 GPa); the preset is a standard-modulus grade.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.models import CompositeSpec, FiberType

__all__ = [
    "CONTINUOUS_EXAMPLE",
    "FIBERS",
    "KK16_2",
    "MATRICES",
    "PARTICLE_EXAMPLE",
    "ContinuousExample",
    "Material",
    "ParticleExample",
]


@dataclass(frozen=True)
class Material:
    """Typical properties: modulus GPa, tensile strength MPa, density g/cm³."""

    key: str
    modulus: float
    strength: float
    density: float


@dataclass(frozen=True)
class ContinuousExample:
    """Continuous aligned glass/polyester example (Callister, Example 16.1)."""

    ef: float = 69.0  # GPa, glass fiber
    em: float = 3.4  # GPa, polyester resin
    vf: float = 0.40
    stress: float = 50.0  # MPa, applied longitudinal stress (part c)
    area: float = 250.0  # mm², cross-section (part c)


@dataclass(frozen=True)
class ParticleExample:
    """Copper matrix with tungsten particles (Callister, large-particle bounds figure)."""

    em: float = 110.0  # GPa, copper
    ep: float = 407.0  # GPa, tungsten


#: Concept Check 16.2 — four hypothetical aligned discontinuous composites.
KK16_2: tuple[CompositeSpec, ...] = (
    CompositeSpec("A", FiberType.GLASS, vf=0.20, sigma_f=3.5e3, l=8.0, lc=0.70),
    CompositeSpec("B", FiberType.GLASS, vf=0.35, sigma_f=3.5e3, l=12.0, lc=0.75),
    CompositeSpec("C", FiberType.CARBON, vf=0.40, sigma_f=5.5e3, l=8.0, lc=0.40),
    CompositeSpec("D", FiberType.CARBON, vf=0.30, sigma_f=5.5e3, l=8.0, lc=0.50),
)

CONTINUOUS_EXAMPLE = ContinuousExample()
PARTICLE_EXAMPLE = ParticleExample()

FIBERS: dict[str, Material] = {
    "e_glass": Material("e_glass", modulus=72.5, strength=3450.0, density=2.58),
    "carbon_sm": Material("carbon_sm", modulus=230.0, strength=4000.0, density=1.78),
    "aramid": Material("aramid", modulus=131.0, strength=3600.0, density=1.44),
}

MATRICES: dict[str, Material] = {
    "epoxy": Material("epoxy", modulus=2.4, strength=70.0, density=1.20),
    "polyester": Material("polyester", modulus=3.4, strength=55.0, density=1.25),
}
