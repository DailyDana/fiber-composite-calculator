"""Language tables must stay in sync; formatting must follow each language."""

from __future__ import annotations

import string

import pytest

from app.core.compare import rank
from app.core.models import CompositeSpec, FiberType
from app.core.presets import KK16_2
from app.i18n import en, fmt, fmt_auto, render, t, tex_num, tr
from app.interpret.engine import explain


def _placeholders(template: str) -> set[str]:
    return {name for _, name, _, _ in string.Formatter().parse(template) if name}


def test_same_keys() -> None:
    assert set(tr.STRINGS) == set(en.STRINGS)


@pytest.mark.parametrize("key", sorted(tr.STRINGS))
def test_same_placeholders(key: str) -> None:
    assert _placeholders(tr.STRINGS[key]) == _placeholders(en.STRINGS[key])


def test_number_formats() -> None:
    assert fmt(2145.0, 1, "tr") == "2145,0"
    assert fmt(2145.0, 1, "en") == "2145.0"
    assert fmt(-0.0001, 2, "tr") == "0,00"
    assert fmt_auto(0.70, "tr") == "0,7"
    assert fmt_auto(8.0, "en") == "8"
    assert tex_num(0.2, 2, "tr") == "0{,}20"


def test_unknown_language() -> None:
    with pytest.raises(ValueError):
        t("app.title", "de")


SCENARIOS = {
    "kk16_2": (KK16_2, None),
    "kk16_2_matrix": (KK16_2, 80.0),
    "overtaken": (
        (
            CompositeSpec("G", FiberType.GLASS, 0.60, 3500, 12, 0.5),
            CompositeSpec("K", FiberType.CARBON, 0.15, 5500, 8, 0.4),
        ),
        None,
    ),
    "short": ((CompositeSpec("S", FiberType.ARAMID, 0.3, 3600, 0.2, 0.6),), 30.0),
}


@pytest.mark.parametrize("lang", ["tr", "en"])
@pytest.mark.parametrize("name", sorted(SCENARIOS))
def test_every_message_renders(name: str, lang: str) -> None:
    specs, sigma_m = SCENARIOS[name]
    for message in explain(rank(specs, sigma_m)):
        text = render(message, lang)
        assert text and text[0].isupper()
        assert "{" not in text and "}" not in text


def test_turkish_rendering_of_kk16_2() -> None:
    texts = [render(m, "tr") for m in explain(rank(KK16_2))]
    joined = "\n".join(texts)
    assert "C > D > B > A" in joined
    assert "Cam elyaflı kompozitlerde (A ve B)" in joined
    assert "%95,6 (A) ile %97,5 (C)" in joined
    assert "3449 MPa" in joined


def test_turkish_capital_i() -> None:
    from app.interpret.messages import Message, Section

    message = Message(Section.MATRIX, "mat.threshold", {"value": "1", "upper": "X", "lower": "Y"})
    assert render(message, "tr").startswith("İki")
