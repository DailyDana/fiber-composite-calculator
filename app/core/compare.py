"""Evaluate and rank aligned discontinuous-fiber composites.

The textbook exercise behind this module (Callister, Concept Check 16.2) gives
fiber type, Vf, σf*, mean fiber length and critical length, but no matrix
data. The ranking is therefore made on the fiber term, and its robustness is
proven by computing the smallest common matrix stress σm' that could change it
(:func:`flip_threshold`). When the user does supply σm', it is included.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.core.formulas import NEAR_CONTINUOUS_RATIO, length_efficiency
from app.core.models import (
    CompositeResult,
    CompositeSpec,
    FlipThreshold,
    LengthRegime,
    RankingResult,
)

__all__ = ["evaluate", "flip_threshold", "rank"]


def evaluate(spec: CompositeSpec, sigma_m_prime: float | None = None) -> CompositeResult:
    """Strength of one composite with all intermediate values."""
    if sigma_m_prime is not None and sigma_m_prime < 0:
        raise ValueError("sigma_m_prime must be non-negative")
    eff = length_efficiency(spec.l, spec.lc)
    fiber = spec.sigma_f * spec.vf * eff
    matrix = (sigma_m_prime or 0.0) * (1.0 - spec.vf)
    ratio = spec.l / spec.lc
    return CompositeResult(
        spec=spec,
        regime=LengthRegime.LONG if spec.l >= spec.lc else LengthRegime.SHORT,
        length_ratio=ratio,
        efficiency=eff,
        fiber_term=fiber,
        matrix_term=matrix,
        strength=fiber + matrix,
        near_continuous=ratio >= NEAR_CONTINUOUS_RATIO,
    )


def _sorted(results: Sequence[CompositeResult], key: str) -> list[CompositeResult]:
    # Ties keep input order (sorted is stable) so equal composites stay as entered.
    return sorted(results, key=lambda r: -getattr(r, key))


def flip_threshold(results: Sequence[CompositeResult]) -> FlipThreshold | None:
    """Smallest common σm' that reorders any pair ranked on the fiber term.

    For composites i above j: ``total_i - total_j = ΔF - σm' (Vf_i - Vf_j)``,
    so the pair can only swap when ``Vf_i > Vf_j``, at
    ``σm' = ΔF / (Vf_i - Vf_j)``. Returns ``None`` when no pair can swap
    (the order is then independent of the matrix).
    """
    ordered = _sorted(results, "fiber_term")
    best: FlipThreshold | None = None
    for i, upper in enumerate(ordered):
        for lower in ordered[i + 1 :]:
            dvf = upper.spec.vf - lower.spec.vf
            if dvf <= 0:
                continue
            value = (upper.fiber_term - lower.fiber_term) / dvf
            if best is None or value < best.sigma_m:
                best = FlipThreshold(value, upper.spec.name, lower.spec.name)
    return best


def rank(specs: Sequence[CompositeSpec], sigma_m_prime: float | None = None) -> RankingResult:
    """Evaluate every composite and sort strongest first.

    ``sigma_m_prime`` is a common matrix stress at fiber failure (same matrix
    for all composites) or ``None`` when unknown.
    """
    if not specs:
        raise ValueError("at least one composite is required")
    names = [s.name for s in specs]
    if len(set(names)) != len(names):
        raise ValueError("composite names must be unique")
    results = [evaluate(s, sigma_m_prime) for s in specs]
    return RankingResult(
        results=tuple(_sorted(results, "strength")),
        sigma_m_prime=sigma_m_prime,
        flip_threshold=flip_threshold(results),
        fiber_only_order=tuple(r.spec.name for r in _sorted(results, "fiber_term")),
    )
