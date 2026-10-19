"""Headless page tests with Streamlit's AppTest (no browser)."""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

UI = Path(__file__).resolve().parent.parent / "app" / "ui"
TIMEOUT = 60


def _run(page: str, **state: object) -> AppTest:
    at = AppTest.from_file(str(UI / page), default_timeout=TIMEOUT)
    for key, value in state.items():
        at.session_state[key] = value
    at.run()
    assert not at.exception, [e.message for e in at.exception]
    return at


def _metrics(at: AppTest) -> dict[str, str]:
    return {m.label: m.value for m in at.metric}


def test_router_starts_on_compare_page() -> None:
    at = _run("streamlit_app.py")
    assert at.title[0].value == "Kompozit karşılaştırma ve sıralama"


def test_compare_page_turkish_results() -> None:
    at = _run("compare_page.py")
    metrics = _metrics(at)
    assert metrics["En yüksek dayanım"] == "C: 2145,0 MPa"
    assert metrics["Sıralama"] == "C > D > B > A"
    assert metrics["Sırayı bozan σm' eşiği"] == "3449 MPa (B–A)"
    assert any("Kavram" in str(o) for o in at.selectbox[0].options)


def test_compare_page_english() -> None:
    at = _run("compare_page.py", lang="en")
    assert at.title[0].value == "Compare and rank composites"
    assert _metrics(at)["Highest strength"] == "C: 2145.0 MPa"


def test_compare_page_with_matrix() -> None:
    at = _run("compare_page.py")
    at.toggle(key="cmp_use_matrix").set_value(True).run()
    at.number_input(key="cmp_sigma_m").set_value(100.0).run()
    assert not at.exception
    assert _metrics(at)["En yüksek dayanım"] == "C: 2205,0 MPa"


def test_compare_page_blank_preset_loads() -> None:
    at = _run("compare_page.py")
    at.selectbox(key="cmp_preset").set_value("preset.blank").run()
    at.button[0].click().run()
    assert not at.exception
    assert _metrics(at)["Sıralama"] == "A"


def test_continuous_page_example_16_1() -> None:
    at = _run("continuous_page.py")
    metrics = _metrics(at)
    assert metrics["Ecl (boyuna)"] == "29,64 GPa"
    assert metrics["Ect (enine)"] == "5,49 GPa"
    assert metrics["Ff / Fm"] == "13,53"
    at.toggle(key="cont_use_load").set_value(True).run()
    assert _metrics(at)["Elyaf yükü Ff"] == "11640 N"


def test_discontinuous_page_compute_mode() -> None:
    at = _run("discontinuous_page.py")
    assert _metrics(at)["Kritik uzunluk lc (mm)"] == "0,700 mm"
    at.radio(key="d_mode").set_value("compute").run()
    assert not at.exception
    # 3500 MPa · 0.010 mm / (2 · 25 MPa) = 0.700 mm
    assert _metrics(at)["Kritik uzunluk lc (mm)"] == "0,700 mm"


@pytest.mark.parametrize("lang", ["tr", "en"])
def test_orientation_particle_page(lang: str) -> None:
    at = _run("random_particle_page.py", lang=lang)
    values = list(_metrics(at).values())
    assert any(v.startswith("12") for v in values)  # random 2D Ecd ≈ 12.4 GPa


def test_language_from_query_param() -> None:
    at = AppTest.from_file(str(UI / "streamlit_app.py"), default_timeout=TIMEOUT)
    at.query_params["lang"] = "en"
    at.run()
    assert not at.exception
    assert at.title[0].value == "Compare and rank composites"


def test_chart_html_ships_both_themes() -> None:
    from app.ui.common import chart_html

    out = chart_html(b"\x89PNGlight", b"\x89PNGdark", 'Strength "σ" <chart>')
    assert out.count("<img") == 2
    assert 'class="fcc-light"' in out and 'class="fcc-dark"' in out
    assert "prefers-color-scheme: dark" in out
    assert "&lt;chart&gt;" in out and "<chart>" not in out  # alt text escaped
