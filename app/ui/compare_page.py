"""Compare and rank aligned discontinuous-fiber composites (the main page)."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import math  # noqa: E402

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from app.charts import figures as F  # noqa: E402
from app.core.compare import rank  # noqa: E402
from app.core.models import CompositeSpec, FiberType, RankingResult  # noqa: E402
from app.core.presets import KK16_2  # noqa: E402
from app.i18n import fiber_label, fmt, pct  # noqa: E402
from app.interpret.engine import explain  # noqa: E402
from app.interpret.steps import discontinuous_steps, threshold_step  # noqa: E402
from app.reporting.pdf_report import ReportMeta, build_compare_report  # noqa: E402
from app.ui.common import T, lang, show_figure, show_messages, show_steps  # noqa: E402

COLUMNS = ("name", "fiber", "vf", "sigma_f", "l", "lc")
PRESETS = {
    "preset.kk16_2": KK16_2,
    "preset.blank": (CompositeSpec("A", FiberType.GLASS, 0.30, 3500.0, 8.0, 0.5),),
}


def _frame(specs: tuple[CompositeSpec, ...]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "name": s.name,
                "fiber": s.fiber_type.value,
                "vf": s.vf,
                "sigma_f": s.sigma_f,
                "l": s.l,
                "lc": s.lc,
            }
            for s in specs
        ],
        columns=list(COLUMNS),
    )


def _init_state() -> None:
    ss = st.session_state
    ss.setdefault("cmp_preset", "preset.kk16_2")
    ss.setdefault("cmp_base", _frame(KK16_2))
    ss.setdefault("cmp_version", 0)


def _load_preset() -> None:
    ss = st.session_state
    ss.cmp_base = _frame(PRESETS[ss.cmp_preset])
    ss.cmp_version += 1  # a new editor key discards the old edits


def _blank(value: object) -> bool:
    return value is None or (isinstance(value, float) and math.isnan(value)) or value == ""


def _parse(frame: pd.DataFrame) -> tuple[list[CompositeSpec], list[str]]:
    specs: list[CompositeSpec] = []
    errors: list[str] = []
    for i, row in enumerate(frame.to_dict("records"), start=1):
        if all(_blank(row.get(c)) for c in COLUMNS):
            continue
        try:
            missing = [c for c in COLUMNS if _blank(row.get(c))]
            if missing:
                raise ValueError(", ".join(T(f"col.{c}") for c in missing))
            specs.append(
                CompositeSpec(
                    name=str(row["name"]).strip(),
                    fiber_type=FiberType(row["fiber"]),
                    vf=float(row["vf"]),
                    sigma_f=float(row["sigma_f"]),
                    l=float(row["l"]),
                    lc=float(row["lc"]),
                )
            )
        except (ValueError, TypeError) as exc:
            errors.append(T("error.row", row=i, error=exc))
    return specs, errors


def _results_table(ranking: RankingResult) -> pd.DataFrame:
    lg = lang()
    rows = []
    for i, r in enumerate(ranking.results, start=1):
        row = {
            T("col.rank"): i,
            T("col.name"): r.spec.name,
            T("col.fiber"): fiber_label(r.spec.fiber_type, lg).capitalize(),
            T("col.ratio"): fmt(r.length_ratio, 1, lg),
            T("col.regime"): T(f"regime.{r.regime.value}"),
            T("col.eff"): pct(r.efficiency, 1, lg),
            T("col.fiber_term"): fmt(r.fiber_term, 1, lg),
        }
        if ranking.sigma_m_prime is not None:
            row[T("col.matrix_term")] = fmt(r.matrix_term, 1, lg)
        row[T("col.strength")] = fmt(r.strength, 1, lg)
        row[T("col.near")] = "✓" if r.near_continuous else "–"
        rows.append(row)
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False, max_entries=16)
def _report_pdf(specs: tuple[CompositeSpec, ...], sigma_m: float | None, meta: ReportMeta) -> bytes:
    return build_compare_report(specs, sigma_m, meta)


# ---------------------------------------------------------------------------
_init_state()
lg = lang()
st.title(T("cmp.title"))
st.caption(T("app.caption"))
st.markdown(T("cmp.intro"))

c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
c1.selectbox(T("cmp.preset"), list(PRESETS), format_func=T, key="cmp_preset")
c2.button(T("cmp.load"), on_click=_load_preset, width="stretch")

edited = st.data_editor(
    st.session_state.cmp_base,
    key=f"cmp_editor_{st.session_state.cmp_version}",
    num_rows="dynamic",
    hide_index=True,
    column_config={
        "name": st.column_config.TextColumn(T("col.name"), required=True, max_chars=12),
        "fiber": st.column_config.SelectboxColumn(
            T("col.fiber"),
            options=[ft.value for ft in FiberType],
            format_func=lambda v: fiber_label(v, lg).capitalize(),
            required=True,
            default=FiberType.GLASS.value,
        ),
        "vf": st.column_config.NumberColumn(
            T("col.vf"), min_value=0.0, max_value=0.99, step=0.01, format="%.2f", required=True
        ),
        "sigma_f": st.column_config.NumberColumn(
            T("col.sigma_f"), min_value=0.0, step=50.0, format="%.0f", required=True
        ),
        "l": st.column_config.NumberColumn(
            T("col.l"), min_value=0.0, step=0.1, format="%.2f", required=True
        ),
        "lc": st.column_config.NumberColumn(
            T("col.lc"), min_value=0.0, step=0.01, format="%.2f", required=True
        ),
    },
)

use_matrix = st.toggle(T("cmp.matrix_toggle"), key="cmp_use_matrix")
sigma_m: float | None = None
if use_matrix:
    sigma_m = st.number_input(
        T("cmp.matrix_value"),
        min_value=0.0,
        max_value=1000.0,
        value=30.0,
        step=5.0,
        help=T("cmp.matrix_help"),
        key="cmp_sigma_m",
    )

specs, errors = _parse(edited)
for message in errors:
    st.error(message)
if not specs:
    st.info(T("cmp.need_rows"))
    st.stop()
try:
    ranking = rank(specs, sigma_m)
except ValueError as exc:
    st.error(T("error.input", error=exc))
    st.stop()

# --- results -------------------------------------------------------------
st.header(T("cmp.results"))
top = ranking.results[0]
th = ranking.flip_threshold
m1, m2, m3 = st.columns(3)
m1.metric(T("cmp.metric_top"), f"{top.spec.name}: {fmt(top.strength, 1, lg)} MPa")
m2.metric(T("cmp.metric_order"), " > ".join(ranking.order))
m3.metric(
    T("cmp.metric_threshold"),
    f"{fmt(th.sigma_m, 0, lg)} MPa ({th.upper}–{th.lower})"
    if th
    else T("cmp.metric_threshold_none"),
)
st.dataframe(_results_table(ranking), hide_index=True, width="stretch")

st.subheader(T("cmp.charts"))
tab1, tab2, tab3 = st.tabs(
    [T("chart.strength.title"), T("chart.ratio.title"), T("chart.eff.title")]
)
with tab1:
    show_figure(lambda th: F.strength_bars(ranking, lg, theme=th), T("chart.strength.title"))
with tab2:
    show_figure(lambda th: F.ratio_chart(ranking, lg, theme=th), T("chart.ratio.title"))
with tab3:
    show_figure(lambda th: F.efficiency_curve(ranking, lg, theme=th), T("chart.eff.title"))

st.subheader(T("cmp.interpretation"))
show_messages(explain(ranking))

st.subheader(T("steps.title"))
for r in ranking.results:
    label = T("rep.calc.composite", name=r.spec.name, fiber=fiber_label(r.spec.fiber_type, lg))
    with st.expander(label):
        show_steps(discontinuous_steps(r, sigma_m, lg))
threshold = threshold_step(ranking, lg)
if threshold is not None:
    with st.expander(T(threshold.label)):
        show_steps([threshold])

# --- report --------------------------------------------------------------
st.header(T("cmp.report"))
with st.container(border=True):
    r1, r2 = st.columns([3, 1])
    title = r1.text_input(T("rep.title"), value=T("rep.title_default"), key=f"rep_title_{lg}")
    when = r2.date_input(T("rep.date"), value=date.today(), key="rep_date", format="DD.MM.YYYY")
    footer = st.checkbox(T("rep.footer_toggle"), value=False, key="rep_footer")
    meta = ReportMeta(lang=lg, title=title, date=when.strftime("%d.%m.%Y"), footer=footer)
    st.download_button(
        T("rep.download"),
        data=_report_pdf(tuple(specs), sigma_m, meta),
        file_name=T("rep.filename"),
        mime="application/pdf",
        type="primary",
        icon=":material/picture_as_pdf:",
    )
