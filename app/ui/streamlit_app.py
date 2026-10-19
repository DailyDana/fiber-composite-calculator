"""Streamlit entry point: language selector and page router.

Run with:  streamlit run app/ui/streamlit_app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st  # noqa: E402

from app import __version__  # noqa: E402
from app.i18n import DEFAULT_LANG, LANGS, t  # noqa: E402

st.set_page_config(page_title="Fiber Composite Calculator", page_icon="🧵", layout="wide")

st.session_state.setdefault("lang", DEFAULT_LANG)
with st.sidebar:
    st.selectbox(t("lang.label"), list(LANGS), format_func=LANGS.__getitem__, key="lang")
lang = st.session_state["lang"]

page = st.navigation(
    [
        st.Page(
            _HERE / "compare_page.py",
            title=t("nav.compare", lang),
            icon="📊",
            default=True,
        ),
        st.Page(
            _HERE / "continuous_page.py",
            title=t("nav.continuous", lang),
            icon="📏",
            url_path="continuous",
        ),
        st.Page(
            _HERE / "discontinuous_page.py",
            title=t("nav.discontinuous", lang),
            icon="✂️",
            url_path="discontinuous",
        ),
        st.Page(
            _HERE / "random_particle_page.py",
            title=t("nav.random_particle", lang),
            icon="🧩",
            url_path="orientation-particles",
        ),
    ]
)

with st.sidebar, st.expander(t("about.title", lang)):
    st.markdown(t("about.body", lang))
    st.caption(f"v{__version__} · Apache-2.0")

page.run()
