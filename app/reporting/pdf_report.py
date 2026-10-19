"""A4 PDF report for a composite comparison.

Structure: purpose and input data → theory → step-by-step calculations →
results table and charts → discussion per factor → verification of the
ranking (matrix threshold) → conclusion → reference.

Text is set in DejaVu Sans (shipped in ``assets/fonts``) because the PDF
base-14 fonts cannot print Turkish ğ, ş, ı. Formula lines are the same TeX the
app shows, rendered with matplotlib mathtext (also DejaVu) into images.
"""

from __future__ import annotations

import io
from collections.abc import Sequence
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from xml.sax.saxutils import escape

import matplotlib

matplotlib.use("Agg")
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import math_to_image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.charts import figures as F
from app.core.compare import rank
from app.core.models import CompositeSpec, RankingResult
from app.i18n import capitalize, fiber_label, fmt, fmt_auto, pct, render, t
from app.interpret.engine import explain
from app.interpret.messages import Message, Section
from app.interpret.steps import discontinuous_steps, threshold_step

__all__ = ["ReportMeta", "build_compare_report"]

FONT_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "fonts"
ACCENT = colors.HexColor("#1F6F78")
INK = colors.HexColor("#1B2426")
INK_2 = colors.HexColor("#52514e")
HEADER_BG = colors.HexColor("#E6F0F0")
RULE = colors.HexColor("#C9D3D3")
CONTENT_WIDTH = A4[0] - 4 * cm


@dataclass(frozen=True)
class ReportMeta:
    lang: str = "tr"
    title: str = ""
    date: str = ""
    footer: bool = False


@cache
def _register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("DejaVu", str(FONT_DIR / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(FONT_DIR / "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Oblique", str(FONT_DIR / "DejaVuSans-Oblique.ttf")))
    pdfmetrics.registerFontFamily(
        "DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu-Oblique"
    )


def _styles() -> dict[str, ParagraphStyle]:
    base = ParagraphStyle("body", fontName="DejaVu", fontSize=10, leading=14.5, textColor=INK)
    return {
        "body": base,
        "title": ParagraphStyle(
            "title", parent=base, fontName="DejaVu-Bold", fontSize=15, leading=19, spaceAfter=4
        ),
        "meta": ParagraphStyle("meta", parent=base, fontSize=9.5, textColor=INK_2),
        "h1": ParagraphStyle(
            "h1",
            parent=base,
            fontName="DejaVu-Bold",
            fontSize=12,
            leading=16,
            textColor=ACCENT,
            spaceBefore=12,
            spaceAfter=5,
            keepWithNext=1,  # never strand a heading at the foot of a page
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base,
            fontName="DejaVu-Bold",
            fontSize=10.5,
            spaceBefore=7,
            spaceAfter=2,
            keepWithNext=1,
        ),
        "step": ParagraphStyle(
            "step", parent=base, fontName="DejaVu-Oblique", fontSize=8.5, textColor=INK_2
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base,
            fontName="DejaVu-Oblique",
            fontSize=8.5,
            alignment=TA_CENTER,
            textColor=INK_2,
            spaceAfter=8,
        ),
        "cell": ParagraphStyle("cell", parent=base, fontSize=8.8, leading=11),
        "cell_head": ParagraphStyle(
            "cell_head", parent=base, fontName="DejaVu-Bold", fontSize=8.8, leading=11
        ),
    }


def _p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(text), style)


def _tex_image(tex: str, size: float = 10.5, max_width: float = CONTENT_WIDTH) -> Image:
    """One formula line as a crisp PNG, scaled down only if wider than the page."""
    dpi = 300
    buf = io.BytesIO()
    math_to_image(f"${tex}$", buf, prop=FontProperties(size=size), dpi=dpi, format="png")
    buf.seek(0)
    w_px, h_px = ImageReader(buf).getSize()
    buf.seek(0)
    w, h = w_px * 72 / dpi, h_px * 72 / dpi
    if w > max_width:
        w, h = max_width, h * max_width / w
    img = Image(buf, width=w, height=h)
    img.hAlign = "LEFT"
    return img


def _figure(fig, caption: str, styles: dict[str, ParagraphStyle]) -> KeepTogether:  # type: ignore[no-untyped-def]
    png = F.figure_to_png(fig, dpi=200)
    reader = ImageReader(io.BytesIO(png))
    w_px, h_px = reader.getSize()
    width = CONTENT_WIDTH * 0.8
    img = Image(io.BytesIO(png), width=width, height=width * h_px / w_px)
    return KeepTogether([img, _p(caption, styles["caption"])])


def _table(rows: list[list[str]], styles: dict[str, ParagraphStyle], widths: list[float]) -> Table:
    data = [[_p(c, styles["cell_head"]) for c in rows[0]]]
    data += [[_p(c, styles["cell"]) for c in row] for row in rows[1:]]
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
                ("LINEABOVE", (0, 0), (-1, 0), 0.8, ACCENT),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, ACCENT),
                ("LINEBELOW", (0, -1), (-1, -1), 0.8, ACCENT),
                ("LINEBELOW", (0, 1), (-1, -2), 0.3, RULE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def _given_rows(specs: Sequence[CompositeSpec], lang: str) -> list[list[str]]:
    head = [
        t(k, lang) for k in ("col.name", "col.fiber", "col.vf", "col.sigma_f", "col.l", "col.lc")
    ]
    rows = [head]
    for s in specs:
        rows.append(
            [
                s.name,
                fiber_label(s.fiber_type, lang),
                fmt(s.vf, 2, lang),
                fmt_auto(s.sigma_f, lang),
                fmt_auto(s.l, lang),
                fmt(s.lc, 2, lang),
            ]
        )
    return rows


def _result_rows(ranking: RankingResult, lang: str) -> list[list[str]]:
    with_matrix = ranking.sigma_m_prime is not None
    keys = ["col.rank", "col.name", "col.ratio", "col.regime", "col.eff", "col.fiber_term"]
    if with_matrix:
        keys.append("col.matrix_term")
    keys += ["col.strength", "col.near"]
    rows = [[t(k, lang) for k in keys]]
    for i, r in enumerate(ranking.results, start=1):
        row = [
            str(i),
            r.spec.name,
            fmt(r.length_ratio, 1, lang),
            t(f"regime.{r.regime.value}", lang),
            pct(r.efficiency, 1, lang),
            fmt(r.fiber_term, 1, lang),
        ]
        if with_matrix:
            row.append(fmt(r.matrix_term, 1, lang))
        row += [fmt(r.strength, 1, lang), "✓" if r.near_continuous else "–"]
        rows.append(row)
    return rows


def _section_paragraphs(
    messages: Sequence[Message], section: Section, lang: str, style: ParagraphStyle
) -> list[Paragraph]:
    return [_p(render(m, lang), style) for m in messages if m.section is section]


def _prose(
    messages: Sequence[Message], section: Section, lang: str, style: ParagraphStyle
) -> Paragraph:
    """A section's sentences as one flowing paragraph, the way a report reads."""
    return _p(" ".join(render(m, lang) for m in messages if m.section is section), style)


def build_compare_report(
    specs: Sequence[CompositeSpec], sigma_m_prime: float | None, meta: ReportMeta
) -> bytes:
    """Render the full comparison report and return the PDF bytes."""
    _register_fonts()
    lang = meta.lang
    st = _styles()
    ranking = rank(specs, sigma_m_prime)
    messages = explain(ranking)
    story: list = []  # type: ignore[type-arg]

    # --- heading ---------------------------------------------------------
    story.append(_p(meta.title or t("rep.title_default", lang), st["title"]))
    if meta.date:
        story.append(_p(meta.date, st["meta"]))
    story.append(Spacer(1, 6))

    # --- 1. question and data -----------------------------------------------
    story.append(_p(t("rep.sec.question", lang), st["h1"]))
    story.append(_p(t("rep.purpose", lang), st["body"]))
    story.append(Spacer(1, 6))
    w = CONTENT_WIDTH
    story.append(
        _table(
            _given_rows(specs, lang),
            st,
            [w * 0.16, w * 0.18, w * 0.14, w * 0.2, w * 0.16, w * 0.16],
        )
    )
    story.append(_p(t("rep.given.table", lang), st["caption"]))
    if sigma_m_prime is not None:
        story.append(
            _p(
                capitalize(t("mat.included", lang, value=fmt(sigma_m_prime, 1, lang)), lang),
                st["body"],
            )
        )

    # --- 2. theory ----------------------------------------------------------
    story.append(_p(t("rep.sec.theory", lang), st["h1"]))
    for key in ("rep.theory.p1", "rep.theory.p2", "rep.theory.p3"):
        story.append(_p(t(key, lang), st["body"]))
        story.append(Spacer(1, 4))

    # --- 3. calculations ----------------------------------------------------
    story.append(_p(t("rep.sec.calc", lang), st["h1"]))
    story.append(_p(t("rep.calc.intro", lang), st["body"]))
    for r in sorted(ranking.results, key=lambda r: r.spec.name):
        block: list = [  # type: ignore[type-arg]
            _p(
                t(
                    "rep.calc.composite",
                    lang,
                    name=r.spec.name,
                    fiber=fiber_label(r.spec.fiber_type, lang),
                ),
                st["h2"],
            )
        ]
        for step in discontinuous_steps(r, sigma_m_prime, lang):
            block.append(_p(t(step.label, lang), st["step"]))
            block.append(_tex_image(step.tex))
            block.append(Spacer(1, 2))
        story.append(KeepTogether(block))

    # --- 4. results and charts ----------------------------------------------
    story.append(_p(t("rep.sec.results", lang), st["h1"]))
    story += _section_paragraphs(messages, Section.RANKING, lang, st["body"])
    story.append(Spacer(1, 6))
    rows = _result_rows(ranking, lang)
    n = len(rows[0])
    story.append(_table(rows, st, [w / n] * n))
    story.append(_p(t("rep.results.table", lang), st["caption"]))

    def figure(fig, n: int, key: str) -> KeepTogether:  # type: ignore[no-untyped-def]
        return _figure(fig, t("rep.fig", lang, n=n, title=t(key, lang)), st)

    story.append(figure(F.strength_bars(ranking, lang), 1, "chart.strength.title"))
    story.append(figure(F.ratio_chart(ranking, lang), 2, "chart.ratio.title"))

    # --- 5. discussion per factor -------------------------------------------
    story.append(_p(t("rep.sec.discussion", lang), st["h1"]))
    for k, section in enumerate((Section.FIBER, Section.VF, Section.LENGTH), start=1):
        story.append(_p(f"5.{k}. {t(f'sec.{section.value}', lang)}", st["h2"]))
        story.append(_prose(messages, section, lang, st["body"]))
    # The efficiency curve illustrates the length discussion it follows.
    story.append(Spacer(1, 6))
    story.append(figure(F.efficiency_curve(ranking, lang), 3, "chart.eff.title"))

    # --- 6. verification ----------------------------------------------------
    story.append(_p(t("rep.sec.verification", lang), st["h1"]))
    # The threshold formula goes right after the sentence that states it.
    matrix = [m for m in messages if m.section is Section.MATRIX]
    cut = next((i + 1 for i, m in enumerate(matrix) if m.key == "mat.threshold"), len(matrix))
    story.append(_prose(matrix[:cut], Section.MATRIX, lang, st["body"]))
    step = threshold_step(ranking, lang)
    if step is not None:
        story.append(Spacer(1, 3))
        story.append(_p(t(step.label, lang), st["step"]))
        story.append(_tex_image(step.tex))
        story.append(Spacer(1, 5))
    if matrix[cut:]:
        story.append(_prose(matrix[cut:], Section.MATRIX, lang, st["body"]))

    # --- 7. conclusion ------------------------------------------------------
    story.append(_p(t("rep.sec.conclusion", lang), st["h1"]))
    story.append(_prose(messages, Section.CONCLUSION, lang, st["body"]))

    story.append(_p(t("rep.sec.references", lang), st["h1"]))
    story.append(_p(t("rep.references.callister", lang), st["body"]))

    def _footer(canvas, doc) -> None:  # type: ignore[no-untyped-def]
        canvas.saveState()
        canvas.setFont("DejaVu", 8)
        canvas.setFillColor(INK_2)
        canvas.drawCentredString(A4[0] / 2, 1.2 * cm, t("rep.page", lang, n=doc.page))
        if meta.footer:
            canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, t("rep.footer", lang))
        canvas.restoreState()

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=2 * cm,
        title=meta.title or t("rep.title_default", lang),
        author="",
        creator="fiber-composite-calculator" if meta.footer else "",
    )
    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return buf.getvalue()
