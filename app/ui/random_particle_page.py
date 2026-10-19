"""Fiber orientation efficiency (K) and large-particle composite bounds."""

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
from app.core.presets import PARTICLE_EXAMPLE as PX  # noqa: E402
from app.i18n import fmt  # noqa: E402
from app.interpret.steps import orientation_step, particle_steps  # noqa: E402
from app.ui.common import T, lang, show_figure, show_steps  # noqa: E402

lg = lang()
st.title(T("rp.title"))

# --- orientation ---------------------------------------------------------
st.header(T("rp.orient"))
st.markdown(T("rp.orient_intro"))
c1, c2, c3 = st.columns(3)
ef = c1.number_input(T("cont.ef"), min_value=0.1, value=EX.ef, step=1.0, key="rp_ef")
em = c2.number_input(T("cont.em"), min_value=0.1, value=EX.em, step=0.1, key="rp_em")
vf = c3.slider(T("cont.vf"), min_value=0.0, max_value=0.95, value=EX.vf, step=0.01, key="rp_vf")
choice = st.radio(
    "K",
    F.ORIENTATIONS,
    format_func=lambda item: T(item[0]),
    index=1,
    horizontal=True,
    key="rp_k",
)
k = choice[1]
st.metric("Ecd", f"{fmt(f.discontinuous_modulus(k, ef, em, vf), 2, lg)} GPa")
show_figure(F.orientation_chart(ef, em, vf, k, lg), T("chart.orient.title"))
st.caption(T("rp.k_note"))
with st.expander(T("steps.title")):
    show_steps([orientation_step(k, ef, em, vf, lg)])

# --- particles -------------------------------------------------------------
st.header(T("rp.particle"))
st.markdown(T("rp.particle_intro"))
p1, p2, p3 = st.columns(3)
ep = p1.number_input(T("rp.ep"), min_value=0.1, value=PX.ep, step=1.0, key="rp_ep")
em_p = p2.number_input(T("rp.em"), min_value=0.1, value=PX.em, step=1.0, key="rp_em_p")
vp = p3.slider(T("rp.vp"), min_value=0.0, max_value=1.0, value=0.50, step=0.01, key="rp_vp")
upper, lower = f.particle_bounds(ep, em_p, vp)
q1, q2 = st.columns(2)
q1.metric(T("rp.upper"), f"{fmt(upper, 1, lg)} GPa")
q2.metric(T("rp.lower"), f"{fmt(lower, 1, lg)} GPa")
show_figure(F.particle_chart(ep, em_p, vp, lg), T("chart.particle.title"))
with st.expander(T("steps.title")):
    show_steps(particle_steps(ep, em_p, vp, lg))
