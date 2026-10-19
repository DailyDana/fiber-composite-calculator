"""PDF report: text survives extraction (Turkish glyphs), sections and numbers present."""

from __future__ import annotations

import io

import pytest
from pypdf import PdfReader

from app.core import formulas as f
from app.core.presets import CONTINUOUS_EXAMPLE as EX
from app.core.presets import KK16_2
from app.i18n import t
from app.reporting.pdf_report import ReportMeta, build_compare_report


def _text(pdf: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf))
    return "\n".join(page.extract_text() for page in reader.pages)


@pytest.fixture(scope="module")
def turkish_pdf() -> bytes:
    meta = ReportMeta(
        lang="tr",
        course="Malzeme Bilimi",
        title=t("rep.title_default", "tr"),
        question=t("rep.question_default", "tr"),
        student="Öğrenci Şahıs",
        number="123",
        date="19.10.2026",
    )
    return build_compare_report(KK16_2, None, meta)


def test_is_pdf(turkish_pdf: bytes) -> None:
    assert turkish_pdf.startswith(b"%PDF")
    assert 3 <= len(PdfReader(io.BytesIO(turkish_pdf)).pages) <= 8


def test_turkish_glyphs_extract(turkish_pdf: bytes) -> None:
    text = _text(turkish_pdf)
    for word in ("Öğrenci Şahıs", "Sıralamanın doğruluğunun gösterilmesi", "İki kompozitin"):
        assert word in text


def test_sections_and_numbers(turkish_pdf: bytes) -> None:
    text = _text(turkish_pdf)
    for key in (
        "rep.sec.question",
        "rep.sec.theory",
        "rep.sec.calc",
        "rep.sec.results",
        "rep.sec.discussion",
        "rep.sec.verification",
        "rep.sec.conclusion",
    ):
        assert t(key, "tr") in text
    for number in ("2145,0", "1598,4", "1186,7", "669,4", "3449"):
        assert number in text
    assert "C > D > B > A" in text


def test_footer_is_optional(turkish_pdf: bytes) -> None:
    assert "fiber-composite-calculator" not in _text(turkish_pdf)
    with_footer = build_compare_report(KK16_2, None, ReportMeta(lang="tr", footer=True))
    assert "fiber-composite-calculator" in _text(with_footer)


def test_english_with_matrix() -> None:
    pdf = build_compare_report(KK16_2, 80.0, ReportMeta(lang="en"))
    text = _text(pdf)
    assert "Verifying the ranking" in text
    assert "2193.0" in text  # C: 2145.0 + 80 · 0.60
    assert "Matrix term" in text


def test_load_sharing_example_16_1() -> None:
    ls = f.load_sharing(EX.ef, EX.em, EX.vf, EX.stress, EX.area)
    assert ls.fc == pytest.approx(12500)
    assert ls.ff == pytest.approx(11640, abs=1)
    assert ls.sigma_m == pytest.approx(5.73, abs=0.01)
    assert ls.strain == pytest.approx(1.69e-3, abs=0.01e-3)
