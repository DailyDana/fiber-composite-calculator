"""Formula tests against hand calculations and textbook examples."""

from __future__ import annotations

import itertools
import math

import pytest

from app.core import formulas as f
from app.core.presets import CONTINUOUS_EXAMPLE as EX


class TestLengthEfficiency:
    def test_long_branch(self) -> None:
        assert f.length_efficiency(8.0, 0.70) == pytest.approx(1 - 0.70 / 16)

    def test_short_branch(self) -> None:
        assert f.length_efficiency(0.3, 0.6) == pytest.approx(0.25)

    def test_branches_meet_at_critical_length(self) -> None:
        assert f.length_efficiency(1.0, 1.0) == pytest.approx(0.5)
        assert f.length_efficiency(1.0 - 1e-12, 1.0) == pytest.approx(0.5)

    def test_tends_to_one(self) -> None:
        assert f.length_efficiency(1e6, 1.0) == pytest.approx(1.0, abs=1e-6)

    def test_monotonic(self) -> None:
        values = [f.length_efficiency(x / 10, 1.0) for x in range(1, 400)]
        assert all(a < b for a, b in itertools.pairwise(values))

    @pytest.mark.parametrize(("l", "lc"), [(0.0, 1.0), (1.0, 0.0), (-1.0, 1.0), (math.nan, 1.0)])
    def test_rejects_bad_lengths(self, l: float, lc: float) -> None:
        with pytest.raises(ValueError):
            f.length_efficiency(l, lc)


class TestDiscontinuous:
    def test_concept_check_c(self) -> None:
        # C: carbon, Vf 0.40, 5500 MPa, l 8, lc 0.40 -> 2200 * 0.975
        assert f.discontinuous_aligned_strength(5500, 0.40, 8, 0.40) == pytest.approx(2145.0)

    def test_matrix_term_added(self) -> None:
        base = f.discontinuous_aligned_strength(5500, 0.40, 8, 0.40)
        with_m = f.discontinuous_aligned_strength(5500, 0.40, 8, 0.40, sigma_m_prime=30)
        assert with_m - base == pytest.approx(30 * 0.60)

    def test_short_branch_matches_tau_form(self) -> None:
        # σcd*' = (l τc / d) Vf with lc = σf d / (2 τc)
        sigma_f, d, tau_c, l, vf = 3500.0, 0.010, 20.0, 0.5, 0.3
        lc = f.critical_length(sigma_f, d, tau_c)
        assert l < lc
        expected = l * tau_c / d * vf
        assert f.discontinuous_aligned_strength(sigma_f, vf, l, lc) == pytest.approx(expected)

    def test_critical_length(self) -> None:
        assert f.critical_length(3500, 0.010, 25) == pytest.approx(0.70)


class TestContinuousExample16_1:
    """Callister Example 16.1: glass/polyester, Vf = 0.4."""

    def test_longitudinal_modulus(self) -> None:
        # Book rounds to 30 GPa.
        e = f.continuous_longitudinal_modulus(EX.ef, EX.em, EX.vf)
        assert e == pytest.approx(29.64)
        assert round(e) == 30

    def test_load_ratio(self) -> None:
        assert f.load_ratio(EX.ef, EX.em, EX.vf) == pytest.approx(13.53, abs=0.01)

    def test_transverse_modulus(self) -> None:
        assert f.continuous_transverse_modulus(EX.ef, EX.em, EX.vf) == pytest.approx(5.49, abs=0.01)

    def test_load_split_and_stresses(self) -> None:
        # Part (c): 50 MPa over 250 mm² -> Ff ≈ 11640 N, Fm ≈ 860 N,
        # σf ≈ 116 MPa, σm ≈ 5.73 MPa.
        fc = EX.stress * EX.area
        ratio = f.load_ratio(EX.ef, EX.em, EX.vf)
        fm = fc / (1 + ratio)
        ff = fc - fm
        assert ff == pytest.approx(11640, abs=1)
        assert fm == pytest.approx(860, abs=1)
        assert ff / (EX.vf * EX.area) == pytest.approx(116.4, abs=0.1)
        assert fm / ((1 - EX.vf) * EX.area) == pytest.approx(5.73, abs=0.01)

    def test_longitudinal_strength(self) -> None:
        assert f.continuous_longitudinal_strength(3450, 0.4, 30) == pytest.approx(1398.0)


class TestOtherRules:
    def test_modulus_efficiency_limits(self) -> None:
        assert f.discontinuous_modulus(1.0, 69, 3.4, 0.4) == pytest.approx(
            f.continuous_longitudinal_modulus(69, 3.4, 0.4)
        )
        assert f.discontinuous_modulus(3 / 8, 69, 3.4, 0.4) == pytest.approx(
            3 / 8 * 69 * 0.4 + 3.4 * 0.6
        )

    def test_particle_bounds_order_and_ends(self) -> None:
        up, low = f.particle_bounds(407, 110, 0.5)
        assert up >= low
        assert f.particle_bounds(407, 110, 0.0) == pytest.approx((110, 110))
        assert f.particle_bounds(407, 110, 1.0) == pytest.approx((407, 407))

    def test_density(self) -> None:
        assert f.density_mixture(2.58, 1.25, 0.4) == pytest.approx(1.782)

    @pytest.mark.parametrize("vf", [-0.1, 1.1, math.inf])
    def test_fraction_validation(self, vf: float) -> None:
        with pytest.raises(ValueError):
            f.continuous_longitudinal_modulus(69, 3.4, vf)

    def test_load_ratio_needs_matrix(self) -> None:
        with pytest.raises(ValueError):
            f.load_ratio(69, 3.4, 1.0)
