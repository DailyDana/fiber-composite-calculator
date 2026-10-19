"""Helpers shared by the Streamlit pages."""

from __future__ import annotations

import base64
import html
from collections.abc import Callable, Iterable, Sequence
from typing import Any

import streamlit as st
from matplotlib.figure import Figure

from app.charts.figures import DARK, LIGHT, Theme, figure_to_png
from app.i18n import DEFAULT_LANG, LANGS, render, t
from app.interpret.messages import Message, Section
from app.interpret.steps import Step

__all__ = ["T", "chart_html", "lang", "show_figure", "show_messages", "show_steps"]


def lang() -> str:
    value = st.session_state.get("lang", DEFAULT_LANG)
    return value if value in LANGS else DEFAULT_LANG


def T(key: str, **params: Any) -> str:
    return t(key, lang(), **params)


#: Charts stretch on narrow screens but stop growing here on wide ones.
CHART_MAX_WIDTH = 780

# Charts are drawn server-side, and Streamlit does not rerun when the viewer
# switches theme, so a single image would keep the old colors until the next
# click. Each chart therefore ships in both themes and the browser shows the one
# that matches: first by the OS preference (no flash on load), then by the
# app's actual background, which also covers the theme picker in the ⋮ menu.
_CHART_CSS = """
<style>
.fcc-chart img { width: 100%; max-width: __MAXW__px; height: auto; display: block; }
.fcc-chart .fcc-dark { display: none; }
@media (prefers-color-scheme: dark) {
  html:not([data-fcc-theme="light"]) .fcc-chart .fcc-light { display: none; }
  html:not([data-fcc-theme="light"]) .fcc-chart .fcc-dark { display: block; }
}
html[data-fcc-theme="dark"] .fcc-chart .fcc-light { display: none; }
html[data-fcc-theme="dark"] .fcc-chart .fcc-dark { display: block; }
</style>
""".replace("__MAXW__", str(CHART_MAX_WIDTH))

_THEME_WATCH_JS = r"""
<script>
(() => {
  if (window.__fccThemeWatch) return;
  window.__fccThemeWatch = true;
  const sync = () => {
    const app = document.querySelector(".stApp");
    if (!app) return;
    const m = getComputedStyle(app).backgroundColor.match(/\d+/g);
    if (!m) return;
    const lum = (0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]) / 255;
    document.documentElement.dataset.fccTheme = lum < 0.5 ? "dark" : "light";
  };
  sync();
  setInterval(sync, 400);
})();
</script>
"""


def _data_uri(png: bytes) -> str:
    return "data:image/png;base64," + base64.b64encode(png).decode("ascii")


def chart_html(light_png: bytes, dark_png: bytes, alt: str) -> str:
    """Both theme variants of one chart plus the CSS/JS that picks between them."""
    a = html.escape(alt, quote=True)
    return (
        _CHART_CSS
        + '<div class="fcc-chart" role="img" aria-label="'
        + a
        + '">'
        + f'<img class="fcc-light" src="{_data_uri(light_png)}" alt="{a}">'
        + f'<img class="fcc-dark" src="{_data_uri(dark_png)}" alt="{a}">'
        + "</div>"
        + _THEME_WATCH_JS
    )


def show_figure(build: Callable[[Theme], Figure], alt: str) -> None:
    """Render ``build(theme)`` for both themes and show the matching one."""
    light = figure_to_png(build(LIGHT), dpi=150)
    dark = figure_to_png(build(DARK), dpi=150)
    st.html(chart_html(light, dark, alt), unsafe_allow_javascript=True)


def show_steps(steps: Sequence[Step]) -> None:
    for step in steps:
        st.caption(T(step.label))
        st.latex(step.tex)


def show_messages(messages: Iterable[Message], skip: Iterable[Section] = ()) -> None:
    """Interpretation grouped under one heading per section."""
    skipped = set(skip)
    current: Section | None = None
    lines: list[str] = []

    def flush() -> None:
        if current is not None and lines:
            st.markdown(f"**{T(f'sec.{current.value}')}**")
            st.markdown("\n".join(f"- {line}" for line in lines))

    for message in messages:
        if message.section in skipped:
            continue
        if message.section is not current:
            flush()
            current, lines = message.section, []
        lines.append(render(message, lang()))
    flush()
