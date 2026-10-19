"""Step lines parse in mathtext (the PDF renderer); charts build headlessly."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import pytest
from matplotlib.mathtext import MathTextParser

from app.charts import figures as F
from app.core.compare import evaluate, rank
from app.core.models import CompositeSpec, FiberType
from app.core.presets import KK16_2
from app.interpret import steps as S

PARSER = MathTextParser("path")


def _all_steps(lang: str) -> list[S.Step]:
    out: list[S.Step] = []
    for r in rank(KK16_2).results:
        out += S.discontinuous_steps(r, None, lang) + S.discontinuous_steps(r, 80.0, lang)
    out += S.discontinuous_steps(
        evaluate(CompositeSpec("S", FiberType.GLASS, 0.3, 3500, 0.3, 0.6)), None, lang
    )
    out += S.continuous_steps(69, 3.4, 0.4, 3450, 30, 50, 250, lang)
    out.append(S.critical_length_step(3500, 0.010, 25, lang))
    out.append(S.orientation_step(3 / 8, 69, 3.4, 0.4, lang))
    out += S.particle_steps(407, 110, 0.5, lang)
    return out


@pytest.mark.parametrize("lang", ["tr", "en"])
def test_every_step_parses_in_mathtext(lang: str) -> None:
    for step in _all_steps(lang):
        PARSER.parse(f"${step.tex}$")


def test_step_numbers_for_composite_a() -> None:
    a = next(r for r in rank(KK16_2).results if r.spec.name == "A")
    tex = " ".join(s.tex for s in S.discontinuous_steps(a, None, "tr"))
    assert "0{,}9563" in tex
    assert "669{,}4" in tex
    assert r"\geq" in tex


def test_short_regime_step() -> None:
    r = evaluate(CompositeSpec("S", FiberType.GLASS, 0.3, 3500, 0.3, 0.6))
    steps = S.discontinuous_steps(r, None, "en")
    assert steps[0].label == "step.regime_short"
    assert "0.2500" in steps[1].tex


def test_continuous_example_numbers() -> None:
    tex = " ".join(s.tex for s in S.continuous_steps(69, 3.4, 0.4, None, None, 50, 250, "en"))
    assert "29.64" in tex
    assert "13.53" in tex
    assert "11640" in tex and "860" in tex


def _bar_colors(fig) -> list[str]:  # type: ignore[no-untyped-def]
    from matplotlib.colors import to_hex

    return [to_hex(p.get_facecolor()) for p in fig.axes[0].patches]


def test_color_follows_fiber_type_not_rank() -> None:
    fig = F.strength_bars(rank(KK16_2), "tr")
    colors = _bar_colors(fig)
    carbon, glass = F.FIBER_COLORS[FiberType.CARBON], F.FIBER_COLORS[FiberType.GLASS]
    assert colors == [carbon, carbon, glass, glass]  # C, D, B, A


@pytest.mark.parametrize("lang", ["tr", "en"])
def test_all_charts_render(lang: str) -> None:
    ranking = rank(KK16_2, 50.0)
    figures = [
        F.strength_bars(ranking, lang),
        F.ratio_chart(ranking, lang),
        F.efficiency_curve(ranking, lang),
        F.mixture_chart(69, 3.4, 0.4, lang),
        F.strength_length_chart(3500, 0.3, 0.7, 8, 30, lang),
        F.orientation_chart(69, 3.4, 0.4, 3 / 8, lang),
        F.particle_chart(407, 110, 0.5, lang),
    ]
    for fig in figures:
        png = F.figure_to_png(fig, dpi=60)
        assert png.startswith(b"\x89PNG")


def test_turkish_decimal_ticks() -> None:
    fig = F.mixture_chart(69, 3.4, 0.4, "tr")
    fig.canvas.draw()
    labels = [lbl.get_text() for lbl in fig.axes[0].get_xticklabels()]
    assert "0,2" in labels
