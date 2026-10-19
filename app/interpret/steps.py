"""Step-by-step ("show your work") formula lines.

Each step is a label key plus one TeX line: the symbolic formula, the numbers
substituted and the result. The TeX uses only the subset shared by KaTeX
(Streamlit's ``st.latex``) and matplotlib mathtext (the PDF report), so the
same line renders identically in both; a test parses every line with mathtext.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core import formulas as f
from app.core.models import CompositeResult, LengthRegime, RankingResult
from app.i18n import DEFAULT_LANG, tex_auto, tex_num

__all__ = [
    "Step",
    "continuous_steps",
    "critical_length_step",
    "discontinuous_steps",
    "orientation_step",
    "particle_steps",
    "threshold_step",
]

SF = r"\sigma^{*}_{f}"
SM = r"\sigma^{\prime}_{m}"
MPA = r"\,\mathrm{MPa}"
GPA = r"\,\mathrm{GPa}"
MM = r"\,\mathrm{mm}"
N = r"\,\mathrm{N}"


@dataclass(frozen=True)
class Step:
    label: str  # i18n key
    tex: str


def discontinuous_steps(
    r: CompositeResult, sigma_m_prime: float | None = None, lang: str = DEFAULT_LANG
) -> list[Step]:
    s = r.spec
    a = lambda x: tex_auto(x, lang)  # noqa: E731 - local shorthand keeps lines readable
    vf = tex_num(s.vf, 2, lang)
    lc = tex_num(s.lc, 2, lang)
    eta = tex_num(r.efficiency, 4, lang)
    fiber = tex_num(r.fiber_term, 1, lang)
    steps: list[Step] = []
    if r.regime is LengthRegime.LONG:
        steps.append(Step("step.regime_long", rf"l = {a(s.l)}{MM} \geq l_c = {lc}{MM}"))
        steps.append(
            Step(
                "step.efficiency",
                rf"\eta = 1 - \dfrac{{l_c}}{{2l}} = "
                rf"1 - \dfrac{{{lc}}}{{2 \cdot {a(s.l)}}} = {eta}",
            )
        )
    else:
        steps.append(Step("step.regime_short", rf"l = {a(s.l)}{MM} < l_c = {lc}{MM}"))
        steps.append(
            Step(
                "step.efficiency",
                rf"\eta = \dfrac{{l}}{{2 l_c}} = "
                rf"\dfrac{{{a(s.l)}}}{{2 \cdot {lc}}} = {eta}",
            )
        )
    steps.append(
        Step(
            "step.fiber_term",
            rf"{SF} V_f \eta = {a(s.sigma_f)} \cdot {vf} \cdot {eta} = {fiber}{MPA}",
        )
    )
    if sigma_m_prime is None:
        steps.append(Step("step.total", rf"\sigma^{{*}}_{{cd}} \approx {fiber}{MPA}"))
        return steps
    vm = tex_num(1 - s.vf, 2, lang)
    matrix = tex_num(r.matrix_term, 1, lang)
    steps.append(
        Step(
            "step.matrix_term",
            rf"{SM} (1 - V_f) = {a(sigma_m_prime)} \cdot {vm} = {matrix}{MPA}",
        )
    )
    steps.append(
        Step(
            "step.total",
            rf"\sigma^{{*}}_{{cd}} = {fiber} + {matrix} = {tex_num(r.strength, 1, lang)}{MPA}",
        )
    )
    return steps


def critical_length_step(
    sigma_f: float, d_mm: float, tau_c: float, lang: str = DEFAULT_LANG
) -> Step:
    lc = f.critical_length(sigma_f, d_mm, tau_c)
    a = lambda x: tex_auto(x, lang)  # noqa: E731
    return Step(
        "step.lc",
        rf"l_c = \dfrac{{{SF} d}}{{2 \tau_c}} = \dfrac{{{a(sigma_f)} \cdot {a(d_mm)}}}"
        rf"{{2 \cdot {a(tau_c)}}} = {tex_num(lc, 3, lang)}{MM}",
    )


def continuous_steps(
    ef: float,
    em: float,
    vf: float,
    sigma_f: float | None = None,
    sigma_m_prime: float | None = None,
    stress: float | None = None,
    area: float | None = None,
    lang: str = DEFAULT_LANG,
) -> list[Step]:
    a = lambda x: tex_auto(x, lang)  # noqa: E731
    v = tex_num(vf, 2, lang)
    vm = tex_num(1 - vf, 2, lang)
    ecl = f.continuous_longitudinal_modulus(ef, em, vf)
    ect = f.continuous_transverse_modulus(ef, em, vf)
    steps = [
        Step(
            "step.ecl",
            rf"E_{{cl}} = E_m (1 - V_f) + E_f V_f = {a(em)} \cdot {vm} + {a(ef)} \cdot {v}"
            rf" = {tex_num(ecl, 2, lang)}{GPA}",
        ),
        Step(
            "step.ect",
            rf"E_{{ct}} = \dfrac{{E_m E_f}}{{(1 - V_f) E_f + V_f E_m}} = "
            rf"\dfrac{{{a(em)} \cdot {a(ef)}}}{{{vm} \cdot {a(ef)} + {v} \cdot {a(em)}}}"
            rf" = {tex_num(ect, 2, lang)}{GPA}",
        ),
    ]
    if vf < 1.0:
        ratio = f.load_ratio(ef, em, vf)
        steps.append(
            Step(
                "step.load_ratio",
                rf"\dfrac{{F_f}}{{F_m}} = \dfrac{{E_f V_f}}{{E_m V_m}} = "
                rf"\dfrac{{{a(ef)} \cdot {v}}}{{{a(em)} \cdot {vm}}} = {tex_num(ratio, 2, lang)}",
            )
        )
    if sigma_f is not None and sigma_m_prime is not None:
        scl = f.continuous_longitudinal_strength(sigma_f, vf, sigma_m_prime)
        steps.append(
            Step(
                "step.sigma_cl",
                rf"\sigma^{{*}}_{{cl}} = {SM} (1 - V_f) + {SF} V_f = {a(sigma_m_prime)} \cdot {vm}"
                rf" + {a(sigma_f)} \cdot {v} = {tex_num(scl, 1, lang)}{MPA}",
            )
        )
    if stress is not None and area is not None and 0.0 < vf < 1.0:
        ls = f.load_sharing(ef, em, vf, stress, area)
        steps.append(
            Step(
                "step.forces",
                rf"F_c = \sigma_c A = {a(stress)} \cdot {a(area)} = {tex_num(ls.fc, 0, lang)}{N};"
                rf"\; F_m = \dfrac{{F_c}}{{1 + F_f/F_m}} = {tex_num(ls.fm, 0, lang)}{N};"
                rf"\; F_f = {tex_num(ls.ff, 0, lang)}{N}",
            )
        )
        steps.append(
            Step(
                "step.stresses",
                rf"\sigma_f = \dfrac{{F_f}}{{V_f A}} = {tex_num(ls.sigma_f, 1, lang)}{MPA};"
                rf"\; \sigma_m = \dfrac{{F_m}}{{V_m A}} = {tex_num(ls.sigma_m, 2, lang)}{MPA}",
            )
        )
        steps.append(
            Step(
                "step.strain",
                rf"\varepsilon = \dfrac{{\sigma_m}}{{E_m}} = "
                rf"\dfrac{{{tex_num(ls.sigma_m, 2, lang)}}}{{{a(em * 1000)}}} = "
                rf"{tex_num(ls.strain * 1000, 3, lang)} \times 10^{{-3}}",
            )
        )
    return steps


def orientation_step(k: float, ef: float, em: float, vf: float, lang: str = DEFAULT_LANG) -> Step:
    a = lambda x: tex_auto(x, lang)  # noqa: E731
    e = f.discontinuous_modulus(k, ef, em, vf)
    return Step(
        "step.ecd",
        rf"E_{{cd}} = K E_f V_f + E_m V_m = {a(k)} \cdot {a(ef)} \cdot {tex_num(vf, 2, lang)}"
        rf" + {a(em)} \cdot {tex_num(1 - vf, 2, lang)} = {tex_num(e, 2, lang)}{GPA}",
    )


def particle_steps(ep: float, em: float, vp: float, lang: str = DEFAULT_LANG) -> list[Step]:
    a = lambda x: tex_auto(x, lang)  # noqa: E731
    up, low = f.particle_bounds(ep, em, vp)
    v = tex_num(vp, 2, lang)
    vm = tex_num(1 - vp, 2, lang)
    return [
        Step(
            "step.particle_upper",
            rf"E_c(u) = E_m V_m + E_p V_p = {a(em)} \cdot {vm} + {a(ep)} \cdot {v}"
            rf" = {tex_num(up, 1, lang)}{GPA}",
        ),
        Step(
            "step.particle_lower",
            rf"E_c(l) = \dfrac{{E_m E_p}}{{V_m E_p + V_p E_m}} = "
            rf"\dfrac{{{a(em)} \cdot {a(ep)}}}{{{vm} \cdot {a(ep)} + {v} \cdot {a(em)}}}"
            rf" = {tex_num(low, 1, lang)}{GPA}",
        ),
    ]


def threshold_step(ranking: RankingResult, lang: str = DEFAULT_LANG) -> Step | None:
    """The matrix flip threshold written out: σm' = ΔF / ΔVf for the critical pair."""
    th = ranking.flip_threshold
    if th is None:
        return None
    by_name = {r.spec.name: r for r in ranking.results}
    up, low = by_name[th.upper], by_name[th.lower]
    u, w = th.upper, th.lower
    return Step(
        "step.threshold",
        rf"{SM} = \dfrac{{F_{{{u}}} - F_{{{w}}}}}{{V_{{f,{u}}} - V_{{f,{w}}}}} = "
        rf"\dfrac{{{tex_num(up.fiber_term, 1, lang)} - {tex_num(low.fiber_term, 1, lang)}}}"
        rf"{{{tex_num(up.spec.vf, 2, lang)} - {tex_num(low.spec.vf, 2, lang)}}}"
        rf" = {tex_num(th.sigma_m, 0, lang)}{MPA}",
    )
