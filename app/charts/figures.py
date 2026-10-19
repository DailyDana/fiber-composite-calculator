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
from dataclasses import dataclass, field

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
    "DARK",
    "FIBER_COLORS",
    "LIGHT",
    "THEMES",
    "Theme",
    "efficiency_curve",
    "figure_to_png",
    "mixture_chart",
    "orientation_chart",
    "particle_chart",
    "ratio_chart",
    "strength_bars",
    "strength_length_chart",
]


@dataclass(frozen=True)
class Theme:
    """Chart colors for one UI theme. The PDF always uses LIGHT."""

    name: str
    surface: str
    ink: str
    ink_2: str
    grid: str
    muted: str  # de-emphasised bars (orientation chart)
    fill_alpha: float
    #: Categorical slots 1–4 of the validated palette, bound to fiber type.
    fiber: dict[FiberType, str] = field(default_factory=dict)

    @property
    def series(self) -> tuple[str, str]:
        return (self.fiber[FiberType.GLASS], self.fiber[FiberType.CARBON])


LIGHT = Theme(
    name="light",
    surface="#ffffff",
    ink="#1B2426",
    ink_2="#52514e",
    grid="#e3e5e4",
    muted="#b9cbe0",
    fill_alpha=0.08,
    fiber={
        FiberType.GLASS: "#2a78d6",
        FiberType.CARBON: "#eb6834",
        FiberType.ARAMID: "#1baf7a",
        FiberType.OTHER: "#eda100",
    },
)
#: Same hues stepped for the dark surface (validated against #14191b, the app's
#: dark background, so charts sit flush with the page).
DARK = Theme(
    name="dark",
    surface="#14191b",
    ink="#e8ecec",
    ink_2="#a9b2b2",
    grid="#2a3235",
    muted="#34465c",
    fill_alpha=0.16,
    fiber={
        FiberType.GLASS: "#3987e5",
        FiberType.CARBON: "#d95926",
        FiberType.ARAMID: "#199e70",
        FiberType.OTHER: "#c98500",
    },
)
THEMES = {"light": LIGHT, "dark": DARK}
FIBER_COLORS = LIGHT.fiber
FIGSIZE = (6.4, 3.4)


def _figure(th: Theme, size: tuple[float, float] = FIGSIZE) -> tuple[Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=size, dpi=110, layout="constrained")
    fig.patch.set_facecolor(th.surface)
    ax.set_facecolor(th.surface)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(th.ink_2)
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(colors=th.ink_2, labelsize=9)
    ax.xaxis.label.set_color(th.ink)
    ax.yaxis.label.set_color(th.ink)
    ax.grid(True, color=th.grid, linewidth=0.8)
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


def _fiber_legend(
    ax: plt.Axes, types: list[FiberType], lang: str, extra: list[Patch], th: Theme
) -> None:
    handles = [
        Patch(facecolor=th.fiber[ft], label=fiber_label(ft, lang).capitalize()) for ft in types
    ]
    ax.legend(
        handles=handles + extra,
        frameon=False,
        fontsize=8.5,
        loc="upper right",
        labelcolor=th.ink,
    )


def _present_types(ranking: RankingResult) -> list[FiberType]:
    return [ft for ft in FiberType if any(r.spec.fiber_type is ft for r in ranking.results)]


# ---------------------------------------------------------------------------
# Comparison charts
# ---------------------------------------------------------------------------
def strength_bars(
    ranking: RankingResult, lang: str = DEFAULT_LANG, *, theme: Theme = LIGHT
) -> Figure:
    """Strength per composite in ranking order; matrix term stacked when known."""
    th = theme
    fig, ax = _figure(th)
    ax.grid(axis="x", visible=False)
    results = ranking.results
    x = np.arange(len(results))
    colors = [th.fiber[r.spec.fiber_type] for r in results]
    fiber = [r.fiber_term for r in results]
    ax.bar(x, fiber, width=0.58, color=colors, edgecolor=th.surface, linewidth=1.5, zorder=2)
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
            edgecolor=th.surface,
            linewidth=1.5,
            zorder=2,
        )
        extra.append(
            Patch(facecolor=th.muted, hatch="////", label=t("chart.strength.matrix", lang))
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
            color=th.ink,
        )
    ax.set_xticks(x, [r.spec.name for r in results], fontsize=10, color=th.ink)
    ax.set_ylabel(t("chart.strength.y", lang))
    ax.set_ylim(0, top * 1.15)
    _decimal(ax, lang, "y")
    _fiber_legend(ax, _present_types(ranking), lang, extra, th)
    return fig


def ratio_chart(
    ranking: RankingResult, lang: str = DEFAULT_LANG, *, theme: Theme = LIGHT
) -> Figure:
    """Horizontal l/lc bars against the l = lc and l = 15·lc references."""
    th = theme
    fig, ax = _figure(th)
    ax.grid(axis="y", visible=False)
    results = list(reversed(ranking.results))  # strongest on top
    y = np.arange(len(results))
    ratios = [r.length_ratio for r in results]
    ax.barh(
        y,
        ratios,
        height=0.55,
        color=[th.fiber[r.spec.fiber_type] for r in results],
        edgecolor=th.surface,
        linewidth=1.5,
        zorder=2,
    )
    xmax = max(max(ratios) * 1.18, f.NEAR_CONTINUOUS_RATIO * 1.25)
    for yi, v in zip(y, ratios, strict=True):
        ax.text(v + xmax * 0.01, yi, fmt(v, 1, lang), va="center", fontsize=9, color=th.ink)
    ax.axvline(1.0, color=th.ink, linestyle="--", linewidth=1, zorder=3)
    ax.axvline(f.NEAR_CONTINUOUS_RATIO, color=th.ink_2, linestyle=":", linewidth=1.3, zorder=3)
    ax.text(
        1.0, len(results) - 0.45, " " + t("chart.ratio.critical", lang), fontsize=8, color=th.ink
    )
    ax.text(
        f.NEAR_CONTINUOUS_RATIO,
        len(results) - 0.45,
        " " + t("chart.ratio.continuous", lang),
        fontsize=8,
        color=th.ink_2,
    )
    ax.set_yticks(y, [r.spec.name for r in results], fontsize=10, color=th.ink)
    ax.set_xlim(0, xmax)
    ax.set_ylim(-0.6, len(results) - 0.1)
    ax.set_xlabel(t("chart.ratio.x", lang))
    _decimal(ax, lang, "x")
    return fig


def efficiency_curve(
    ranking: RankingResult, lang: str = DEFAULT_LANG, *, theme: Theme = LIGHT
) -> Figure:
    """Universal η(l/lc) curve with every composite placed on it."""
    th = theme
    fig, ax = _figure(th)
    ratios = [r.length_ratio for r in ranking.results]
    xmax = max(30.0, max(ratios) * 1.2)
    xs = np.linspace(0.05, xmax, 600)
    eta = np.where(xs >= 1.0, 1.0 - 1.0 / (2.0 * xs), xs / 2.0)
    ax.plot(xs, eta, color=th.ink_2, linewidth=2, zorder=2)
    ax.axvline(1.0, color=th.ink, linestyle="--", linewidth=1)
    ax.axvline(f.NEAR_CONTINUOUS_RATIO, color=th.ink_2, linestyle=":", linewidth=1.3)
    ax.text(1.0, 0.04, " " + t("chart.ratio.critical", lang), fontsize=8, color=th.ink)
    ax.text(
        f.NEAR_CONTINUOUS_RATIO,
        0.04,
        " " + t("chart.ratio.continuous", lang),
        fontsize=8,
        color=th.ink_2,
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
                color=th.fiber[r.spec.fiber_type],
                edgecolor=th.surface,
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
            color=th.ink,
        )
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel(t("chart.eff.x", lang))
    ax.set_ylabel(t("chart.eff.y", lang))
    _decimal(ax, lang)
    _fiber_legend(ax, _present_types(ranking), lang, [], th)
    ax.get_legend().set_loc("center right")
    return fig


# ---------------------------------------------------------------------------
# Single-calculation charts
# ---------------------------------------------------------------------------
def mixture_chart(
    ef: float, em: float, vf: float, lang: str = DEFAULT_LANG, *, theme: Theme = LIGHT
) -> Figure:
    """Longitudinal (isostrain) and transverse (isostress) modulus versus Vf."""
    th = theme
    fig, ax = _figure(th)
    v = np.linspace(0, 1, 201)
    ecl = em * (1 - v) + ef * v
    ect = em * ef / ((1 - v) * ef + v * em)
    ax.plot(v, ecl, color=th.series[0], linewidth=2, label=t("chart.mix.long", lang))
    ax.plot(v, ect, color=th.series[1], linewidth=2, label=t("chart.mix.trans", lang))
    cur_l = f.continuous_longitudinal_modulus(ef, em, vf)
    cur_t = f.continuous_transverse_modulus(ef, em, vf)
    ax.axvline(vf, color=th.ink_2, linestyle=":", linewidth=1.2)
    for y, c in ((cur_l, th.series[0]), (cur_t, th.series[1])):
        ax.scatter(vf, y, s=60, color=c, edgecolor=th.surface, linewidth=1.5, zorder=4)
        # Up-left of the point: both curves rise to the right, so that side is clear.
        ax.annotate(
            fmt(y, 1, lang),
            (vf, y),
            xytext=(-8, 5),
            textcoords="offset points",
            fontsize=9,
            ha="right",
            color=th.ink,
        )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, ef * 1.05)
    ax.set_xlabel(t("chart.mix.x", lang))
    ax.set_ylabel(t("chart.mix.y", lang))
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", labelcolor=th.ink)
    _decimal(ax, lang)
    return fig


def strength_length_chart(
    sigma_f: float,
    vf: float,
    lc: float,
    l: float,
    sigma_m_prime: float = 0.0,
    lang: str = DEFAULT_LANG,
    *,
    theme: Theme = LIGHT,
) -> Figure:
    """σcd versus fiber length with the lc and 15·lc references."""
    th = theme
    fig, ax = _figure(th)
    xmax = max(l * 1.25, lc * 20)
    ls = np.linspace(xmax / 800, xmax, 800)
    sig = np.array(
        [f.discontinuous_aligned_strength(sigma_f, vf, x, lc, sigma_m_prime) for x in ls]
    )
    limit = f.continuous_longitudinal_strength(sigma_f, vf, sigma_m_prime)
    ax.plot(ls, sig, color=th.series[0], linewidth=2, zorder=2)
    ax.axhline(limit, color=th.ink_2, linestyle="--", linewidth=1)
    ax.annotate(
        f"σcl* = {fmt(limit, 1, lang)}",
        (xmax, limit),
        xytext=(-4, 4),
        textcoords="offset points",
        ha="right",
        fontsize=8.5,
        color=th.ink_2,
    )
    ax.axvline(lc, color=th.ink, linestyle="--", linewidth=1)
    ax.axvline(lc * f.NEAR_CONTINUOUS_RATIO, color=th.ink_2, linestyle=":", linewidth=1.3)
    ax.text(lc, limit * 0.05, " lc", fontsize=8.5, color=th.ink)
    ax.text(lc * f.NEAR_CONTINUOUS_RATIO, limit * 0.05, " 15·lc", fontsize=8.5, color=th.ink_2)
    cur = f.discontinuous_aligned_strength(sigma_f, vf, l, lc, sigma_m_prime)
    ax.scatter(l, cur, s=70, color=th.series[1], edgecolor=th.surface, linewidth=1.5, zorder=4)
    ax.annotate(
        fmt(cur, 1, lang),
        (l, cur),
        xytext=(6, -14),
        textcoords="offset points",
        fontsize=9,
        color=th.ink,
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
    ef: float,
    em: float,
    vf: float,
    selected_k: float | None = None,
    lang: str = DEFAULT_LANG,
    *,
    theme: Theme = LIGHT,
) -> Figure:
    """Modulus for the textbook orientation efficiencies; the selected one is emphasised."""
    th = theme
    fig, ax = _figure(th, (6.4, 2.9))
    ax.grid(axis="y", visible=False)
    labels = [t(key, lang) for key, _ in ORIENTATIONS][::-1]
    values = [f.discontinuous_modulus(k, ef, em, vf) for _, k in ORIENTATIONS][::-1]
    ks = [k for _, k in ORIENTATIONS][::-1]
    colors = [
        th.series[0] if selected_k is None or abs(k - selected_k) < 1e-9 else th.muted for k in ks
    ]
    y = np.arange(len(values))
    ax.barh(y, values, height=0.55, color=colors, edgecolor=th.surface, linewidth=1.5, zorder=2)
    xmax = max(values) * 1.18
    for yi, v in zip(y, values, strict=True):
        ax.text(v + xmax * 0.01, yi, fmt(v, 1, lang), va="center", fontsize=9, color=th.ink)
    ax.set_yticks(y, labels, fontsize=8.5, color=th.ink)
    ax.set_xlim(0, xmax)
    ax.set_xlabel(t("chart.orient.x", lang))
    _decimal(ax, lang, "x")
    return fig


def particle_chart(
    ep: float, em: float, vp: float, lang: str = DEFAULT_LANG, *, theme: Theme = LIGHT
) -> Figure:
    """Upper and lower rule-of-mixtures bounds versus particle fraction."""
    th = theme
    fig, ax = _figure(th)
    v = np.linspace(0, 1, 201)
    upper = em * (1 - v) + ep * v
    lower = em * ep / ((1 - v) * ep + v * em)
    ax.fill_between(v, lower, upper, color=th.series[0], alpha=th.fill_alpha, linewidth=0)
    ax.plot(v, upper, color=th.series[0], linewidth=2, label=t("chart.particle.upper", lang))
    ax.plot(v, lower, color=th.series[1], linewidth=2, label=t("chart.particle.lower", lang))
    up, low = f.particle_bounds(ep, em, vp)
    ax.axvline(vp, color=th.ink_2, linestyle=":", linewidth=1.2)
    for y, c in ((up, th.series[0]), (low, th.series[1])):
        ax.scatter(vp, y, s=60, color=c, edgecolor=th.surface, linewidth=1.5, zorder=4)
        ax.annotate(
            fmt(y, 1, lang),
            (vp, y),
            xytext=(-8, 5),
            textcoords="offset points",
            fontsize=9,
            ha="right",
            color=th.ink,
        )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, max(ep, em) * 1.05)
    ax.set_xlabel(t("chart.particle.x", lang))
    ax.set_ylabel(t("chart.mix.y", lang))
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", labelcolor=th.ink)
    _decimal(ax, lang)
    return fig


def figure_to_png(fig: Figure, dpi: int = 200) -> bytes:
    """PNG bytes; closes the figure so long Streamlit sessions do not leak memory."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, facecolor=fig.get_facecolor())
    plt.close(fig)
    return buf.getvalue()
