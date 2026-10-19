"""Composite mechanics formulas of Callister & Rethwisch, chapter 16.

Every function is pure and unit-agnostic as long as the caller is consistent.
The application uses one convention throughout:

* stresses / strengths in **MPa**
* elastic moduli in **GPa**
* lengths in **mm** (fiber diameter too, so ``lc`` comes out in mm)
* fractions (``vf``, ``vp``) as plain numbers in [0, 1]

Section references are to the "Composites" chapter; equation numbers are
deliberately not quoted because they shift between editions and translations.
docs/FORMULAS.md lists every formula with its derivation notes.
"""

from __future__ import annotations

import math
from typing import NamedTuple

__all__ = [
    "NEAR_CONTINUOUS_RATIO",
    "LoadSharing",
    "check_fraction",
    "check_positive",
    "continuous_longitudinal_modulus",
    "continuous_longitudinal_strength",
    "continuous_transverse_modulus",
    "critical_length",
    "density_mixture",
    "discontinuous_aligned_strength",
    "discontinuous_modulus",
    "length_efficiency",
    "load_ratio",
    "load_sharing",
    "particle_bounds",
]

#: Fibers with l >= 15 * lc behave practically as continuous ones (sec. 16.4).
NEAR_CONTINUOUS_RATIO = 15.0


def check_fraction(name: str, value: float) -> float:
    """Validate a volume fraction in [0, 1]."""
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1], got {value!r}")
    return float(value)


def check_positive(name: str, value: float, *, allow_zero: bool = False) -> float:
    """Validate a finite positive (or non-negative) quantity."""
    ok = math.isfinite(value) and (value >= 0.0 if allow_zero else value > 0.0)
    if not ok:
        kind = "non-negative" if allow_zero else "positive"
        raise ValueError(f"{name} must be a finite {kind} number, got {value!r}")
    return float(value)


# ---------------------------------------------------------------------------
# Fiber length (sec. 16.4)
# ---------------------------------------------------------------------------
def critical_length(sigma_f: float, d: float, tau_c: float) -> float:
    """Critical fiber length ``lc = σf* · d / (2 τc)``.

    ``sigma_f`` fiber tensile strength, ``d`` fiber diameter, ``tau_c`` the
    smaller of the fiber–matrix bond strength and the matrix shear yield
    strength. ``sigma_f`` and ``tau_c`` must share a unit; ``lc`` has the unit
    of ``d``.
    """
    check_positive("sigma_f", sigma_f)
    check_positive("d", d)
    check_positive("tau_c", tau_c)
    return sigma_f * d / (2.0 * tau_c)


def length_efficiency(l: float, lc: float) -> float:
    """Fraction of the fiber strength a discontinuous aligned fiber delivers.

    * ``l >= lc``: ``1 - lc / (2 l)``  (the fiber term of σcd*)
    * ``l <  lc``: ``l / (2 lc)``      (the fiber term of σcd*', written with
      ``τc/d = σf*/(2 lc)`` so only ``l`` and ``lc`` are needed)

    Both branches give 1/2 at ``l = lc`` and the result tends to 1 as
    ``l / lc`` grows, i.e. towards a continuous fiber.
    """
    check_positive("l", l)
    check_positive("lc", lc)
    if l >= lc:
        return 1.0 - lc / (2.0 * l)
    return l / (2.0 * lc)


def discontinuous_aligned_strength(
    sigma_f: float,
    vf: float,
    l: float,
    lc: float,
    sigma_m_prime: float = 0.0,
) -> float:
    """Longitudinal strength of an aligned discontinuous-fiber composite.

    ``σcd* = σf* Vf (1 - lc/2l) + σm' (1 - Vf)``   for ``l > lc``
    ``σcd*' = (l τc / d) Vf + σm' (1 - Vf)``        for ``l < lc``

    ``sigma_m_prime`` is the matrix stress at fiber failure (not the matrix
    tensile strength); pass 0 to get the fiber contribution alone.
    """
    check_positive("sigma_f", sigma_f)
    check_fraction("vf", vf)
    check_positive("sigma_m_prime", sigma_m_prime, allow_zero=True)
    return sigma_f * vf * length_efficiency(l, lc) + sigma_m_prime * (1.0 - vf)


# ---------------------------------------------------------------------------
# Continuous aligned fibers (sec. 16.5)
# ---------------------------------------------------------------------------
def continuous_longitudinal_modulus(ef: float, em: float, vf: float) -> float:
    """Isostrain rule of mixtures ``Ecl = Em (1 - Vf) + Ef Vf``."""
    check_positive("ef", ef)
    check_positive("em", em)
    check_fraction("vf", vf)
    return em * (1.0 - vf) + ef * vf


def continuous_transverse_modulus(ef: float, em: float, vf: float) -> float:
    """Isostress bound ``Ect = Em Ef / ((1 - Vf) Ef + Vf Em)``."""
    check_positive("ef", ef)
    check_positive("em", em)
    check_fraction("vf", vf)
    return em * ef / ((1.0 - vf) * ef + vf * em)


def load_ratio(ef: float, em: float, vf: float) -> float:
    """Fiber-to-matrix load ratio under longitudinal load ``Ff/Fm = Ef Vf / (Em Vm)``."""
    check_positive("ef", ef)
    check_positive("em", em)
    check_fraction("vf", vf)
    if vf >= 1.0:
        raise ValueError("vf must be < 1 for a load ratio (no matrix left)")
    return ef * vf / (em * (1.0 - vf))


class LoadSharing(NamedTuple):
    """Longitudinal load split of a continuous aligned composite (isostrain)."""

    fc: float  # total load, N
    ff: float  # fiber load, N
    fm: float  # matrix load, N
    sigma_f: float  # fiber stress, MPa
    sigma_m: float  # matrix stress, MPa
    strain: float  # common strain (dimensionless)


def load_sharing(ef: float, em: float, vf: float, stress: float, area: float) -> LoadSharing:
    """Split ``Fc = σc·A`` between fibers and matrix with ``Ff/Fm = Ef Vf / (Em Vm)``.

    ``stress`` MPa, ``area`` mm² (so loads are in N), moduli GPa.
    """
    check_positive("stress", stress)
    check_positive("area", area)
    ratio = load_ratio(ef, em, vf)
    fc = stress * area
    fm = fc / (1.0 + ratio)
    ff = fc - fm
    if vf == 0.0:
        raise ValueError("vf must be > 0 for a load split")
    sigma_f = ff / (vf * area)
    sigma_m = fm / ((1.0 - vf) * area)
    return LoadSharing(fc, ff, fm, sigma_f, sigma_m, sigma_m / (em * 1000.0))


def continuous_longitudinal_strength(sigma_f: float, vf: float, sigma_m_prime: float) -> float:
    """Longitudinal tensile strength ``σcl* = σm' (1 - Vf) + σf* Vf``."""
    check_positive("sigma_f", sigma_f)
    check_fraction("vf", vf)
    check_positive("sigma_m_prime", sigma_m_prime, allow_zero=True)
    return sigma_m_prime * (1.0 - vf) + sigma_f * vf


# ---------------------------------------------------------------------------
# Orientation efficiency and particles (secs. 16.2, 16.5)
# ---------------------------------------------------------------------------
def discontinuous_modulus(k: float, ef: float, em: float, vf: float) -> float:
    """Modulus with a fiber efficiency parameter ``Ecd = K Ef Vf + Em Vm``.

    Typical ``K``: 1 aligned (parallel to fibers), 0 aligned (perpendicular),
    3/8 random in a plane, 1/5 random in three dimensions.
    """
    check_fraction("k", k)
    check_positive("ef", ef)
    check_positive("em", em)
    check_fraction("vf", vf)
    return k * ef * vf + em * (1.0 - vf)


def particle_bounds(ep: float, em: float, vp: float) -> tuple[float, float]:
    """Upper and lower rule-of-mixtures bounds for a particle composite.

    Upper ``Ec(u) = Em Vm + Ep Vp``; lower ``Ec(l) = Em Ep / (Vm Ep + Vp Em)``.
    """
    check_positive("ep", ep)
    check_positive("em", em)
    check_fraction("vp", vp)
    vm = 1.0 - vp
    return em * vm + ep * vp, em * ep / (vm * ep + vp * em)


def density_mixture(rho_f: float, rho_m: float, vf: float) -> float:
    """Composite density ``ρc = ρf Vf + ρm Vm``."""
    check_positive("rho_f", rho_f)
    check_positive("rho_m", rho_m)
    check_fraction("vf", vf)
    return rho_f * vf + rho_m * (1.0 - vf)
