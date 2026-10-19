"""Helpers shared by the Streamlit pages."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any

import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.figure import Figure

from app.i18n import DEFAULT_LANG, LANGS, render, t
from app.interpret.messages import Message, Section
from app.interpret.steps import Step

__all__ = ["T", "lang", "show_figure", "show_messages", "show_steps"]


def lang() -> str:
    value = st.session_state.get("lang", DEFAULT_LANG)
    return value if value in LANGS else DEFAULT_LANG


def T(key: str, **params: Any) -> str:
    return t(key, lang(), **params)


#: Charts stretch on narrow screens but stop growing here on wide ones.
CHART_MAX_WIDTH = 780


def show_figure(fig: Figure, alt: str) -> None:
    st.pyplot(fig, width=CHART_MAX_WIDTH, alt=alt)
    plt.close(fig)


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
