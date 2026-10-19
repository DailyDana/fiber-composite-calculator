"""Data models for the multi-composite comparison."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from app.core.formulas import check_fraction, check_positive

__all__ = [
    "CompositeResult",
    "CompositeSpec",
    "FiberType",
    "FlipThreshold",
    "LengthRegime",
    "RankingResult",
]


class FiberType(StrEnum):
    """Fiber families; the value is the stable key used by i18n and presets."""

    GLASS = "glass"
    CARBON = "carbon"
    ARAMID = "aramid"
    OTHER = "other"


class LengthRegime(StrEnum):
    """Which branch of the discontinuous-fiber strength formula applies."""

    LONG = "long"  # l >= lc
    SHORT = "short"  # l < lc


@dataclass(frozen=True)
class CompositeSpec:
    """One aligned discontinuous-fiber composite to compare.

    Units: ``sigma_f`` MPa, ``l`` and ``lc`` mm.
    """

    name: str
    fiber_type: FiberType
    vf: float
    sigma_f: float
    l: float
    lc: float

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("composite name must not be empty")
        object.__setattr__(self, "fiber_type", FiberType(self.fiber_type))
        check_fraction("vf", self.vf)
        if self.vf >= 1.0:
            raise ValueError("vf must be < 1 (a composite needs a matrix)")
        check_positive("sigma_f", self.sigma_f)
        check_positive("l", self.l)
        check_positive("lc", self.lc)


@dataclass(frozen=True)
class CompositeResult:
    """Evaluated strength of one composite, with every intermediate value."""

    spec: CompositeSpec
    regime: LengthRegime
    length_ratio: float  # l / lc
    efficiency: float  # fiber length efficiency (1 - lc/2l or l/2lc)
    fiber_term: float  # σf · Vf · efficiency, MPa
    matrix_term: float  # σm' · (1 - Vf), MPa (0 when σm' unknown)
    strength: float  # fiber_term + matrix_term, MPa
    near_continuous: bool  # l >= 15 lc


@dataclass(frozen=True)
class FlipThreshold:
    """Smallest common matrix stress σm' that would reorder two composites.

    ``upper`` ranks above ``lower`` on the fiber term alone, but has the higher
    Vf, so its matrix term ``σm'(1 - Vf)`` is smaller. Above ``sigma_m`` MPa the
    matrix term would close the gap.
    """

    sigma_m: float
    upper: str
    lower: str


@dataclass(frozen=True)
class RankingResult:
    """Composites sorted strongest first, plus the robustness check."""

    results: tuple[CompositeResult, ...]
    sigma_m_prime: float | None
    flip_threshold: FlipThreshold | None
    fiber_only_order: tuple[str, ...] = field(default=())

    @property
    def order(self) -> tuple[str, ...]:
        return tuple(r.spec.name for r in self.results)

    @property
    def matrix_changed_order(self) -> bool:
        """True when adding σm' produced a different order than the fiber term."""
        return self.order != self.fiber_only_order
