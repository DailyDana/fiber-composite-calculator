"""Interpretation rules decide from the results, not from the preset."""

from __future__ import annotations

from app.core.compare import rank
from app.core.models import CompositeSpec, FiberType
from app.core.presets import KK16_2
from app.interpret.engine import explain
from app.interpret.messages import Section


def _keys(specs, sigma_m=None) -> list[str]:  # type: ignore[no-untyped-def]
    return [m.key for m in explain(rank(specs, sigma_m))]


def test_kk16_2_story() -> None:
    keys = _keys(KK16_2)
    assert keys[0] == "rank.order"
    for expected in (
        "fiber.dominant",
        "vf.rule",
        "len.all_long",
        "len.longest",
        "len.no_order_change",
        "len.near_continuous_some",
        "mat.unknown",
        "mat.threshold",
        "mat.unrealistic",
        "concl.driver_type_then_vf",
        "concl.length_minor",
        "concl.matrix_robust",
    ):
        assert expected in keys, expected
    assert keys.count("vf.follows") == 2  # C vs D and B vs A


def test_sections_are_in_report_order() -> None:
    order = [m.section for m in explain(rank(KK16_2))]
    seen = list(dict.fromkeys(order))
    assert seen == list(Section)


def test_weaker_fiber_overtakes() -> None:
    specs = [
        CompositeSpec("G", FiberType.GLASS, 0.60, 3500, 12, 0.5),
        CompositeSpec("K", FiberType.CARBON, 0.15, 5500, 8, 0.4),
    ]
    keys = _keys(specs)
    assert "fiber.overtaken" in keys
    assert "fiber.dominant" not in keys
    assert "concl.driver_product" in keys
    assert "vf.no_pairs" in keys


def test_length_changes_order() -> None:
    # Same σf·Vf, but Y has short fibers: length decides.
    specs = [
        CompositeSpec("X", FiberType.GLASS, 0.30, 3500, 0.4, 0.5),
        CompositeSpec("Y", FiberType.GLASS, 0.31, 3500, 0.2, 0.5),
    ]
    keys = _keys(specs)
    assert "len.short" in keys
    assert "len.order_change" in keys
    assert "concl.length_major" in keys
    assert "vf.against" in keys


def test_single_fiber_type() -> None:
    specs = [s for s in KK16_2 if s.fiber_type is FiberType.GLASS]
    keys = _keys(specs)
    assert "fiber.single" in keys
    assert "concl.driver_vf" in keys


def test_matrix_sensitive_when_threshold_low() -> None:
    # Fiber terms 1400 vs 1395 (×η), ΔVf = 0.10: σm' ≈ 48 MPa already swaps them.
    specs = [
        CompositeSpec("P", FiberType.GLASS, 0.40, 3500, 8, 0.5),
        CompositeSpec("Q", FiberType.GLASS, 0.30, 4650, 8, 0.5),
    ]
    keys = _keys(specs)
    assert "mat.sensitive" in keys
    assert "concl.matrix_sensitive" in keys


def test_matrix_included_and_order_changed() -> None:
    specs = [
        CompositeSpec("P", FiberType.GLASS, 0.40, 3500, 8, 0.5),
        CompositeSpec("Q", FiberType.GLASS, 0.30, 4650, 8, 0.5),
    ]
    keys = _keys(specs, 150.0)
    assert keys[0] == "rank.order_with_matrix"
    assert "mat.included" in keys
    assert "mat.changed_order" in keys


def test_no_flip_possible() -> None:
    specs = [
        CompositeSpec("X", FiberType.CARBON, 0.3, 5500, 8, 0.5),
        CompositeSpec("Y", FiberType.GLASS, 0.4, 3500, 8, 0.5),
    ]
    keys = _keys(specs)
    assert "mat.no_flip" in keys
    assert "concl.matrix_robust" in keys


def test_equal_vf_pair() -> None:
    specs = [
        CompositeSpec("X", FiberType.GLASS, 0.3, 3500, 12, 0.5),
        CompositeSpec("Y", FiberType.GLASS, 0.3, 3500, 4, 0.5),
    ]
    assert "vf.equal" in _keys(specs)
