"""Continuous aligned fibers: moduli, load sharing and longitudinal strength."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st  # noqa: E402

from app.charts import figures as F  # noqa: E402
from app.core import formulas as f  # noqa: E402
from app.core.presets import CONTINUOUS_EXAMPLE as EX  # noqa: E402
from app.core.presets import FIBERS, MATRICES  # noqa: E402
from app.i18n import fmt  # noqa: E402
from app.interpret.steps import continuous_steps  # noqa: E402
from app.ui.common import T, lang, show_figure, show_steps  # noqa: E402

DEFAULTS = {"cont_ef": EX.ef, "cont_em": EX.em, "cont_vf": EX.vf}


def _reset() -> None:
    st.session_state.update(DEFAULTS)


def _apply_materials() -> None:
    ss = st.session_state
    fiber, matrix = FIBERS[ss.cont_fiber_pick], MATRICES[ss.cont_matrix_pick]
    ss.cont_ef = fiber.modulus
    ss.cont_em = matrix.modulus
    ss.cont_sf = fiber.strength


for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)
st.session_state.setdefault("cont_sf", 3450.0)

lg = lang()
st.title(T("cont.title"))
st.markdown(T("cont.intro"))

with st.expander(T("cont.fill")):
    a, b, c = st.columns([2, 2, 1], vertical_alignment="bottom")
    a.selectbox(
        T("cont.fiber"),
        list(FIBERS),
        format_func=lambda k: T(f"material.{k}"),
        key="cont_fiber_pick",
    )
    b.selectbox(
        T("cont.matrix"),
        list(MATRICES),
        format_func=lambda k: T(f"material.{k}"),
        key="cont_matrix_pick",
    )
    c.button(T("cont.apply"), on_click=_apply_materials, width="stretch")
    st.button(T("cont.reset"), on_click=_reset)

c1, c2, c3 = st.columns(3)
ef = c1.number_input(T("cont.ef"), min_value=0.1, max_value=1000.0, step=1.0, key="cont_ef")
em = c2.number_input(T("cont.em"), min_value=0.1, max_value=1000.0, step=0.1, key="cont_em")
vf = c3.slider(T("cont.vf"), min_value=0.0, max_value=0.95, step=0.01, key="cont_vf")

sigma_f = sigma_m = None
if st.toggle(T("cont.sigma_cl"), key="cont_use_strength"):
    s1, s2 = st.columns(2)
    sigma_f = s1.number_input(T("cont.sigma_f"), min_value=1.0, step=50.0, key="cont_sf")
    sigma_m = s2.number_input(T("cont.sigma_m"), min_value=0.0, value=30.0, step=5.0, key="cont_sm")

stress = area = None
if st.toggle(T("cont.load"), key="cont_use_load"):
    l1, l2 = st.columns(2)
    stress = l1.number_input(T("cont.stress"), min_value=0.1, value=EX.stress, key="cont_stress")
    area = l2.number_input(T("cont.area"), min_value=0.1, value=EX.area, key="cont_area")

ecl = f.continuous_longitudinal_modulus(ef, em, vf)
ect = f.continuous_transverse_modulus(ef, em, vf)
m = st.columns(4)
m[0].metric(T("cont.ecl"), f"{fmt(ecl, 2, lg)} GPa")
m[1].metric(T("cont.ect"), f"{fmt(ect, 2, lg)} GPa")
m[2].metric(T("cont.ratio"), fmt(f.load_ratio(ef, em, vf), 2, lg))
if sigma_f is not None and sigma_m is not None:
    scl = f.continuous_longitudinal_strength(sigma_f, vf, sigma_m)
    m[3].metric(T("cont.sigma_cl"), f"{fmt(scl, 1, lg)} MPa")

if stress is not None and area is not None and vf > 0:
    ls = f.load_sharing(ef, em, vf, stress, area)
    n = st.columns(5)
    n[0].metric(T("cont.ff"), f"{fmt(ls.ff, 0, lg)} N")
    n[1].metric(T("cont.fm"), f"{fmt(ls.fm, 0, lg)} N")
    n[2].metric(T("cont.sf"), f"{fmt(ls.sigma_f, 1, lg)} MPa")
    n[3].metric(T("cont.sm"), f"{fmt(ls.sigma_m, 2, lg)} MPa")
    n[4].metric(T("cont.strain"), f"{fmt(ls.strain * 1000, 3, lg)}·10⁻³")

st.subheader(T("chart.mix.title"))
show_figure(F.mixture_chart(ef, em, vf, lg), T("chart.mix.title"))

with st.expander(T("steps.title"), expanded=True):
    show_steps(continuous_steps(ef, em, vf, sigma_f, sigma_m, stress, area, lg))
