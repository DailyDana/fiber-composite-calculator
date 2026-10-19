"""Chart builders. Every function returns a new matplotlib ``Figure``.

Visual rules (kept identical in the app and the PDF):

* Color follows the fiber type (fixed slots, validated categorical palette),
  never the rank, so a composite keeps its color when the order changes.
* Values are labelled directly on the marks; grid and axes are recessive.
* Reference lines (l = lc, l = 15·lc) are neutral ink, dashed/dotted, labelled.
* No in-figure titles: the page heading or the report caption names the chart.
"""

from __future__ import annotations

import io
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")  # headless and deterministic; must precede pyplot
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Patch

from app.core import formulas as f
from app.core.models import FiberType, RankingResult
from app.i18n import DEFAULT_LANG, fiber_label, fmt, t

__all__ = [
    "FIBER_COLORS",
    "efficiency_curve",
    "figure_to_png",
    "mixture_chart",
    "orientation_chart",
    "particle_chart",
    "ratio_chart",
    "strength_bars",
    "strength_length_chart",
]

#: Categorical slots 1–4 of the validated palette, bound to fiber type.
FIBER_COLORS: dict[FiberType, str] = {
    FiberType.GLASS: "#2a78d6",
    FiberType.CARBON: "#eb6834",
    FiberType.ARAMID: "#1baf7a",
    FiberType.OTHER: "#eda100",
}
SERIES = ("#2a78d6", "#eb6834")
INK = "#1B2426"
INK_2 = "#52514e"
GRID = "#e3e5e4"
SURFACE = "#ffffff"
FIGSIZE = (6.4, 3.4)


def _figure(size: tuple[float, float] = FIGSIZE) -> tuple[Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=size, dpi=110, layout="constrained")
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK_2)
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(colors=INK_2, labelsize=9)
    ax.xaxis.label.set_color(INK)
    ax.yaxis.label.set_color(INK)
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    return fig, ax


def _decimal(ax: plt.Axes, lang: str, axis: str = "both") -> None:
    """Tick labels with the language's decimal separator."""
    if lang != "tr":
        return
    from matplotlib.ticker import FuncFormatter

    fmt_tick = FuncFormatter(lambda v, _pos: f"{v:g}".replace(".", ","))
    if axis in ("x", "both"):
        ax.xaxis.set_major_formatter(fmt_tick)
    if axis in ("y", "both"):
        ax.yaxis.set_major_formatter(fmt_tick)


def _fiber_legend(ax: plt.Axes, types: list[FiberType], lang: str, extra: list[Patch]) -> None:
    handles = [
        Patch(facecolor=FIBER_COLORS[ft], label=fiber_label(ft, lang).capitalize()) for ft in types
    ]
    ax.legend(
        handles=handles + extra,
        frameon=False,
        fontsize=8.5,
        loc="upper right",
        labelcolor=INK,
    )


def _present_types(ranking: RankingResult) -> list[FiberType]:
    return [ft for ft in FiberType if any(r.spec.fiber_type is ft for r in ranking.results)]


# ---------------------------------------------------------------------------
# Comparison charts
# ---------------------------------------------------------------------------
def strength_bars(ranking: RankingResult, lang: str = DEFAULT_LANG) -> Figure:
    """Strength per composite in ranking order; matrix term stacked when known."""
    fig, ax = _figure()
    ax.grid(axis="x", visible=False)
    results = ranking.results
    x = np.arange(len(results))
    colors = [FIBER_COLORS[r.spec.fiber_type] for r in results]
    fiber = [r.fiber_term for r in results]
    ax.bar(x, fiber, width=0.58, color=colors, edgecolor=SURFACE, linewidth=1.5, zorder=2)
    extra: list[Patch] = []
    if ranking.sigma_m_prime is not None:
        matrix = [r.matrix_term for r in results]
        ax.bar(
            x,
            matrix,
            width=0.58,
            bottom=fiber,
            color=colors,
            alpha=0.35,
            hatch="////",
            edgecolor=SURFACE,
            linewidth=1.5,
            zorder=2,
        )
        extra.append(
            Patch(facecolor="#bbbbbb", hatch="////", label=t("chart.strength.matrix", lang))
        )
    top = max(r.strength for r in results)
    for xi, r in zip(x, results, strict=True):
        ax.text(
            xi,
            r.strength + top * 0.02,
            fmt(r.strength, 1, lang),
            ha="center",
            va="bottom",
            fontsize=9,
            color=INK,
        )
    ax.set_xticks(x, [r.spec.name for r in results], fontsize=10, color=INK)
    ax.set_ylabel(t("chart.strength.y", lang))
    ax.set_ylim(0, top * 1.15)
    _decimal(ax, lang, "y")
    _fiber_legend(ax, _present_types(ranking), lang, extra)
    return fig


def ratio_chart(ranking: RankingResult, lang: str = DEFAULT_LANG) -> Figure:
    """Horizontal l/lc bars against the l = lc and l = 15·lc references."""
    fig, ax = _figure()
    ax.grid(axis="y", visible=False)
    results = list(reversed(ranking.results))  # strongest on top
    y = np.arange(len(results))
    ratios = [r.length_ratio for r in results]
    ax.barh(
        y,
        ratios,
        height=0.55,
        color=[FIBER_COLORS[r.spec.fiber_type] for r in results],
        edgecolor=SURFACE,
        linewidth=1.5,
        zorder=2,
    )
    xmax = max(max(ratios) * 1.18, f.NEAR_CONTINUOUS_RATIO * 1.25)
    for yi, v in zip(y, ratios, strict=True):
        ax.text(v + xmax * 0.01, yi, fmt(v, 1, lang), va="center", fontsize=9, color=INK)
    ax.axvline(1.0, color=INK, linestyle="--", linewidth=1, zorder=3)
    ax.axvline(f.NEAR_CONTINUOUS_RATIO, color=INK_2, linestyle=":", linewidth=1.3, zorder=3)
    ax.text(1.0, len(results) - 0.45, " " + t("chart.ratio.critical", lang), fontsize=8, color=INK)
    ax.text(
        f.NEAR_CONTINUOUS_RATIO,
        len(results) - 0.45,
        " " + t("chart.ratio.continuous", lang),
        fontsize=8,
        color=INK_2,
    )
    ax.set_yticks(y, [r.spec.name for r in results], fontsize=10, color=INK)
    ax.set_xlim(0, xmax)
    ax.set_ylim(-0.6, len(results) - 0.1)
    ax.set_xlabel(t("chart.ratio.x", lang))
    _decimal(ax, lang, "x")
    return fig


def efficiency_curve(ranking: RankingResult, lang: str = DEFAULT_LANG) -> Figure:
    """Universal η(l/lc) curve with every composite placed on it."""
    fig, ax = _figure()
    ratios = [r.length_ratio for r in ranking.results]
    xmax = max(30.0, max(ratios) * 1.2)
    xs = np.linspace(0.05, xmax, 600)
    eta = np.where(xs >= 1.0, 1.0 - 1.0 / (2.0 * xs), xs / 2.0)
    ax.plot(xs, eta, color=INK_2, linewidth=2, zorder=2)
    ax.axvline(1.0, color=INK, linestyle="--", linewidth=1)
    ax.axvline(f.NEAR_CONTINUOUS_RATIO, color=INK_2, linestyle=":", linewidth=1.3)
    ax.text(1.0, 0.04, " " + t("chart.ratio.critical", lang), fontsize=8, color=INK)
    ax.text(
        f.NEAR_CONTINUOUS_RATIO,
        0.04,
        " " + t("chart.ratio.continuous", lang),
        fontsize=8,
        color=INK_2,
    )
    # Composites that sit on the same point share one label ("B, D").
    groups: dict[tuple[float, float], list] = defaultdict(list)
    for r in ranking.results:
        groups[(round(r.length_ratio, 3), round(r.efficiency, 4))].append(r)
    for (x, y), members in groups.items():
        for k, r in enumerate(members):
            ax.scatter(
                x,
                y,
                s=130 if k == 0 else 45,  # later members sit inside the first as a ring
                color=FIBER_COLORS[r.spec.fiber_type],
                edgecolor=SURFACE,
                linewidth=1.5,
                zorder=4 + k,
            )
        label = ", ".join(sorted(m.spec.name for m in members))
        ax.annotate(
            label,
            (x, y),
            xytext=(0, -16),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            color=INK,
        )
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel(t("chart.eff.x", lang))
    ax.set_ylabel(t("chart.eff.y", lang))
    _decimal(ax, lang)
    _fiber_legend(ax, _present_types(ranking), lang, [])
    ax.get_legend().set_loc("center right")
    return fig


# ---------------------------------------------------------------------------
# Single-calculation charts
# ---------------------------------------------------------------------------
def mixture_chart(ef: float, em: float, vf: float, lang: str = DEFAULT_LANG) -> Figure:
    """Longitudinal (isostrain) and transverse (isostress) modulus versus Vf."""
    fig, ax = _figure()
    v = np.linspace(0, 1, 201)
    ecl = em * (1 - v) + ef * v
    ect = em * ef / ((1 - v) * ef + v * em)
    ax.plot(v, ecl, color=SERIES[0], linewidth=2, label=t("chart.mix.long", lang))
    ax.plot(v, ect, color=SERIES[1], linewidth=2, label=t("chart.mix.trans", lang))
    cur_l = f.continuous_longitudinal_modulus(ef, em, vf)
    cur_t = f.continuous_transverse_modulus(ef, em, vf)
    ax.axvline(vf, color=INK_2, linestyle=":", linewidth=1.2)
    for y, c in ((cur_l, SERIES[0]), (cur_t, SERIES[1])):
        ax.scatter(vf, y, s=60, color=c, edgecolor=SURFACE, linewidth=1.5, zorder=4)
        # Up-left of the point: both curves rise to the right, so that side is clear.
        ax.annotate(
            fmt(y, 1, lang),
            (vf, y),
            xytext=(-8, 5),
            textcoords="offset points",
            fontsize=9,
            ha="right",
            color=INK,
        )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, ef * 1.05)
    ax.set_xlabel(t("chart.mix.x", lang))
    ax.set_ylabel(t("chart.mix.y", lang))
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", labelcolor=INK)
    _decimal(ax, lang)
    return fig


def strength_length_chart(
    sigma_f: float,
    vf: float,
    lc: float,
    l: float,
    sigma_m_prime: float = 0.0,
    lang: str = DEFAULT_LANG,
) -> Figure:
    """σcd versus fiber length with the lc and 15·lc references."""
    fig, ax = _figure()
    xmax = max(l * 1.25, lc * 20)
    ls = np.linspace(xmax / 800, xmax, 800)
    sig = np.array(
        [f.discontinuous_aligned_strength(sigma_f, vf, x, lc, sigma_m_prime) for x in ls]
    )
    limit = f.continuous_longitudinal_strength(sigma_f, vf, sigma_m_prime)
    ax.plot(ls, sig, color=SERIES[0], linewidth=2, zorder=2)
    ax.axhline(limit, color=INK_2, linestyle="--", linewidth=1)
    ax.annotate(
        f"σcl* = {fmt(limit, 1, lang)}",
        (xmax, limit),
        xytext=(-4, 4),
        textcoords="offset points",
        ha="right",
        fontsize=8.5,
        color=INK_2,
    )
    ax.axvline(lc, color=INK, linestyle="--", linewidth=1)
    ax.axvline(lc * f.NEAR_CONTINUOUS_RATIO, color=INK_2, linestyle=":", linewidth=1.3)
    ax.text(lc, limit * 0.05, " lc", fontsize=8.5, color=INK)
    ax.text(lc * f.NEAR_CONTINUOUS_RATIO, limit * 0.05, " 15·lc", fontsize=8.5, color=INK_2)
    cur = f.discontinuous_aligned_strength(sigma_f, vf, l, lc, sigma_m_prime)
    ax.scatter(l, cur, s=70, color=SERIES[1], edgecolor=SURFACE, linewidth=1.5, zorder=4)
    ax.annotate(
        fmt(cur, 1, lang),
        (l, cur),
        xytext=(6, -14),
        textcoords="offset points",
        fontsize=9,
        color=INK,
    )
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, limit * 1.12)
    ax.set_xlabel(t("chart.sl.x", lang))
    ax.set_ylabel(t("chart.sl.y", lang))
    _decimal(ax, lang)
    return fig


ORIENTATIONS: tuple[tuple[str, float], ...] = (
    ("rp.k.aligned_par", 1.0),
    ("rp.k.random_2d", 3 / 8),
    ("rp.k.random_3d", 1 / 5),
    ("rp.k.aligned_perp", 0.0),
)


def orientation_chart(
    ef: float, em: float, vf: float, selected_k: float | None = None, lang: str = DEFAULT_LANG
) -> Figure:
    """Modulus for the textbook orientation efficiencies; the selected one is emphasised."""
    fig, ax = _figure((6.4, 2.9))
    ax.grid(axis="y", visible=False)
    labels = [t(key, lang) for key, _ in ORIENTATIONS][::-1]
    values = [f.discontinuous_modulus(k, ef, em, vf) for _, k in ORIENTATIONS][::-1]
    ks = [k for _, k in ORIENTATIONS][::-1]
    colors = [
        SERIES[0] if selected_k is None or abs(k - selected_k) < 1e-9 else "#b9cbe0" for k in ks
    ]
    y = np.arange(len(values))
    ax.barh(y, values, height=0.55, color=colors, edgecolor=SURFACE, linewidth=1.5, zorder=2)
    xmax = max(values) * 1.18
    for yi, v in zip(y, values, strict=True):
        ax.text(v + xmax * 0.01, yi, fmt(v, 1, lang), va="center", fontsize=9, color=INK)
    ax.set_yticks(y, labels, fontsize=8.5, color=INK)
    ax.set_xlim(0, xmax)
    ax.set_xlabel(t("chart.orient.x", lang))
    _decimal(ax, lang, "x")
    return fig


def particle_chart(ep: float, em: float, vp: float, lang: str = DEFAULT_LANG) -> Figure:
    """Upper and lower rule-of-mixtures bounds versus particle fraction."""
    fig, ax = _figure()
    v = np.linspace(0, 1, 201)
    upper = em * (1 - v) + ep * v
    lower = em * ep / ((1 - v) * ep + v * em)
    ax.fill_between(v, lower, upper, color=SERIES[0], alpha=0.08, linewidth=0)
    ax.plot(v, upper, color=SERIES[0], linewidth=2, label=t("chart.particle.upper", lang))
    ax.plot(v, lower, color=SERIES[1], linewidth=2, label=t("chart.particle.lower", lang))
    up, low = f.particle_bounds(ep, em, vp)
    ax.axvline(vp, color=INK_2, linestyle=":", linewidth=1.2)
    for y, c in ((up, SERIES[0]), (low, SERIES[1])):
        ax.scatter(vp, y, s=60, color=c, edgecolor=SURFACE, linewidth=1.5, zorder=4)
        ax.annotate(
            fmt(y, 1, lang),
            (vp, y),
            xytext=(-8, 5),
            textcoords="offset points",
            fontsize=9,
            ha="right",
            color=INK,
        )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, max(ep, em) * 1.05)
    ax.set_xlabel(t("chart.particle.x", lang))
    ax.set_ylabel(t("chart.mix.y", lang))
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", labelcolor=INK)
    _decimal(ax, lang)
    return fig


def figure_to_png(fig: Figure, dpi: int = 200) -> bytes:
    """PNG bytes; closes the figure so long Streamlit sessions do not leak memory."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, facecolor=fig.get_facecolor())
    plt.close(fig)
    return buf.getvalue()
