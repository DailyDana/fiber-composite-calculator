"""Ranking tests; the golden values are Concept Check 16.2 worked by hand."""

from __future__ import annotations

import pytest

from app.core.compare import evaluate, flip_threshold, rank
from app.core.models import CompositeSpec, FiberType, LengthRegime
from app.core.presets import KK16_2

GOLDEN_FIBER_TERM = {"A": 669.375, "B": 1186.71875, "C": 2145.0, "D": 1598.4375}


class TestConceptCheck16_2:
    def test_order(self) -> None:
        assert rank(KK16_2).order == ("C", "D", "B", "A")

    def test_strengths(self) -> None:
        for r in rank(KK16_2).results:
            assert r.strength == pytest.approx(GOLDEN_FIBER_TERM[r.spec.name])
            assert r.matrix_term == 0.0

    def test_all_long_fibers(self) -> None:
        assert all(r.regime is LengthRegime.LONG for r in rank(KK16_2).results)

    def test_near_continuous_flags(self) -> None:
        flags = {r.spec.name: r.near_continuous for r in rank(KK16_2).results}
        assert flags == {"A": False, "B": True, "C": True, "D": True}

    def test_length_ratios(self) -> None:
        ratios = {r.spec.name: r.length_ratio for r in rank(KK16_2).results}
        assert ratios["A"] == pytest.approx(8 / 0.7)
        assert ratios["B"] == pytest.approx(16)
        assert ratios["C"] == pytest.approx(20)
        assert ratios["D"] == pytest.approx(16)

    def test_flip_threshold_is_b_over_a(self) -> None:
        th = rank(KK16_2).flip_threshold
        assert th is not None
        assert (th.upper, th.lower) == ("B", "A")
        assert th.sigma_m == pytest.approx((1186.71875 - 669.375) / 0.15)

    def test_threshold_is_where_order_changes(self) -> None:
        th = rank(KK16_2).flip_threshold
        assert th is not None
        below = rank(KK16_2, th.sigma_m * 0.99).order
        above = rank(KK16_2, th.sigma_m * 1.01).order
        assert below == ("C", "D", "B", "A")
        assert above.index("A") < above.index("B")

    def test_realistic_matrix_keeps_order(self) -> None:
        result = rank(KK16_2, 80.0)
        assert result.order == ("C", "D", "B", "A")
        assert not result.matrix_changed_order
        c = next(r for r in result.results if r.spec.name == "C")
        assert c.strength == pytest.approx(2145.0 + 80 * 0.6)


class TestEdgeCases:
    def test_short_fiber_regime(self) -> None:
        r = evaluate(CompositeSpec("S", FiberType.GLASS, 0.3, 3500, l=0.3, lc=0.6))
        assert r.regime is LengthRegime.SHORT
        assert r.efficiency == pytest.approx(0.25)

    def test_no_flip_possible(self) -> None:
        # Stronger AND lower Vf: the matrix only widens the gap.
        specs = [
            CompositeSpec("X", FiberType.CARBON, 0.3, 5500, 8, 0.5),
            CompositeSpec("Y", FiberType.GLASS, 0.4, 3500, 8, 0.5),
        ]
        assert flip_threshold([evaluate(s) for s in specs]) is None

    def test_single_composite(self) -> None:
        result = rank([KK16_2[0]])
        assert result.order == ("A",)
        assert result.flip_threshold is None

    def test_duplicate_names_rejected(self) -> None:
        with pytest.raises(ValueError, match="unique"):
            rank([KK16_2[0], KK16_2[0]])

    def test_empty_rejected(self) -> None:
        with pytest.raises(ValueError):
            rank([])

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"vf": 1.0},
            {"vf": -0.1},
            {"sigma_f": 0.0},
            {"l": 0.0},
            {"lc": -1.0},
            {"name": "  "},
        ],
    )
    def test_spec_validation(self, kwargs: dict[str, object]) -> None:
        base: dict[str, object] = {
            "name": "Z",
            "fiber_type": "glass",
            "vf": 0.3,
            "sigma_f": 3500.0,
            "l": 8.0,
            "lc": 0.5,
        }
        base.update(kwargs)
        with pytest.raises(ValueError):
            CompositeSpec(**base)  # type: ignore[arg-type]

    def test_fiber_type_from_string(self) -> None:
        spec = CompositeSpec("Z", "carbon", 0.3, 5500, 8, 0.5)  # type: ignore[arg-type]
        assert spec.fiber_type is FiberType.CARBON

    def test_negative_matrix_rejected(self) -> None:
        with pytest.raises(ValueError):
            rank(KK16_2, -1.0)
