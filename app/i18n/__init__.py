"""Turkish / English strings, number formatting and message rendering."""

from __future__ import annotations

from typing import Any

from app.core.models import FiberType
from app.i18n import en, tr
from app.interpret.messages import Message, Names, Num, Order

__all__ = ["DEFAULT_LANG", "LANGS", "fiber_label", "fmt", "render", "t", "tex_num"]

LANGS: dict[str, str] = {"tr": "Türkçe", "en": "English"}
DEFAULT_LANG = "tr"
_TABLES: dict[str, dict[str, str]] = {"tr": tr.STRINGS, "en": en.STRINGS}


def _table(lang: str) -> dict[str, str]:
    try:
        return _TABLES[lang]
    except KeyError:
        raise ValueError(f"unsupported language {lang!r}") from None


def fmt(value: float, nd: int = 1, lang: str = DEFAULT_LANG) -> str:
    """Fixed-point number with the language's decimal separator, no grouping.

    Grouping is left out on purpose: engineering values such as 2145,0 read
    better without it, and "2.145,0" would be ambiguous to English readers.
    """
    text = f"{value:.{nd}f}"
    if text.startswith("-") and float(text) == 0:
        text = text[1:]
    return text.replace(".", ",") if lang == "tr" else text


def fmt_auto(value: float, lang: str = DEFAULT_LANG, max_nd: int = 4) -> str:
    """An input value as typed: up to ``max_nd`` decimals, trailing zeros dropped."""
    text = f"{value:.{max_nd}f}".rstrip("0").rstrip(".")
    if text in ("-0", ""):
        text = "0"
    return text.replace(".", ",") if lang == "tr" else text


def tex_num(value: float, nd: int = 1, lang: str = DEFAULT_LANG) -> str:
    """Number for TeX/mathtext: the comma is braced so it gets no extra space."""
    return fmt(value, nd, lang).replace(",", "{,}")


def tex_auto(value: float, lang: str = DEFAULT_LANG, max_nd: int = 4) -> str:
    return fmt_auto(value, lang, max_nd).replace(",", "{,}")


def pct(value: float, nd: int = 1, lang: str = DEFAULT_LANG) -> str:
    number = fmt(value * 100, nd, lang)
    return f"%{number}" if lang == "tr" else f"{number}%"


def fiber_label(ftype: FiberType | str, lang: str = DEFAULT_LANG) -> str:
    return t(f"fiber.{FiberType(ftype).value}", lang)


def t(key: str, lang: str = DEFAULT_LANG, **params: Any) -> str:
    """Look up ``key`` and format it with ``params`` (already strings)."""
    template = _table(lang)[key]
    return template.format(**params) if params else template


def _render_param(value: Any, lang: str) -> str:
    if isinstance(value, Num):
        return pct(value.value, value.nd, lang) if value.pct else fmt(value.value, value.nd, lang)
    if isinstance(value, Names):
        items = list(value.items)
        if len(items) == 1:
            return items[0]
        return ", ".join(items[:-1]) + t("list.and", lang) + items[-1]
    if isinstance(value, Order):
        return " > ".join(value.items)
    if isinstance(value, FiberType):
        return fiber_label(value, lang)
    return str(value)


def _capitalize(text: str, lang: str) -> str:
    if not text:
        return text
    first = text[0]
    # Turkish dotted/dotless i: str.upper() would turn "i" into "I".
    upper = {"i": "İ", "ı": "I"}.get(first) if lang == "tr" else None
    return (upper or first.upper()) + text[1:]


def render(message: Message, lang: str = DEFAULT_LANG) -> str:
    params = {k: _render_param(v, lang) for k, v in message.params.items()}
    return _capitalize(t(message.key, lang, **params), lang)
