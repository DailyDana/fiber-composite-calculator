"""One aligned discontinuous-fiber composite: lc, efficiency and strength."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st  # noqa: E402

from app.charts import figures as F  # noqa: E402
from app.core import formulas as f  # noqa: E402
from app.core.compare import evaluate  # noqa: E402
from app.core.models import CompositeSpec, FiberType, LengthRegime  # noqa: E402
from app.i18n import fmt, pct  # noqa: E402
from app.interpret.steps import critical_length_step, discontinuous_steps  # noqa: E402
from app.ui.common import T, lang, show_figure, show_steps  # noqa: E402

lg = lang()
st.title(T("disc.title"))
st.markdown(T("disc.intro"))

c1, c2, c3 = st.columns(3)
sigma_f = c1.number_input(T("disc.sigma_f"), min_value=1.0, value=3500.0, step=50.0, key="d_sf")
vf = c2.slider(T("disc.vf"), min_value=0.01, max_value=0.95, value=0.30, step=0.01, key="d_vf")
l = c3.number_input(T("disc.l"), min_value=0.001, value=8.0, step=0.5, format="%.3f", key="d_l")

mode = st.radio(
    T("disc.lc_mode"),
    ["direct", "compute"],
    format_func=lambda k: T(f"disc.lc_{k}"),
    horizontal=True,
    key="d_mode",
)
lc_step = None
if mode == "direct":
    lc = st.number_input(
        T("disc.lc"), min_value=0.001, value=0.70, step=0.05, format="%.3f", key="d_lc"
    )
else:
    k1, k2 = st.columns(2)
    d_um = k1.number_input(T("disc.d"), min_value=0.1, value=10.0, step=0.5, key="d_d")
    tau = k2.number_input(T("disc.tau"), min_value=0.1, value=25.0, step=1.0, key="d_tau")
    lc = f.critical_length(sigma_f, d_um / 1000.0, tau)
    lc_step = critical_length_step(sigma_f, d_um / 1000.0, tau, lg)

sigma_m = None
if st.toggle(T("cmp.matrix_toggle"), key="d_use_matrix"):
    sigma_m = st.number_input(
        T("disc.sigma_m"),
        min_value=0.0,
        value=30.0,
        step=5.0,
        help=T("cmp.matrix_help"),
        key="d_sm",
    )

r = evaluate(CompositeSpec("—", FiberType.OTHER, vf, sigma_f, l, lc), sigma_m)
m = st.columns(4)
m[0].metric(T("disc.lc"), f"{fmt(lc, 3, lg)} mm")
m[1].metric(T("disc.ratio"), fmt(r.length_ratio, 1, lg))
m[2].metric(T("disc.eff"), pct(r.efficiency, 1, lg))
m[3].metric(T("disc.strength"), f"{fmt(r.strength, 1, lg)} MPa")

if r.regime is LengthRegime.SHORT:
    st.warning(T("disc.short"))
elif r.near_continuous:
    st.success(T("disc.near"))
else:
    st.info(T("disc.between", eff=pct(r.efficiency, 1, lg)))

st.subheader(T("chart.sl.title"))
show_figure(F.strength_length_chart(sigma_f, vf, lc, l, sigma_m or 0.0, lg), T("chart.sl.title"))

with st.expander(T("steps.title"), expanded=True):
    show_steps(([lc_step] if lc_step else []) + discontinuous_steps(r, sigma_m, lg))
