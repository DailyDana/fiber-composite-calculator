"""Language-neutral message objects.

The interpretation engine decides *what* to say and with which numbers; the
i18n layer decides *how* to say it. Parameters are typed so numbers get the
right decimal separator and fiber types the right label in each language.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from app.core.models import FiberType

__all__ = ["Message", "Names", "Num", "Order", "Section", "Values"]


class Section(StrEnum):
    RANKING = "ranking"
    FIBER = "fiber"
    VF = "vf"
    LENGTH = "length"
    MATRIX = "matrix"
    CONCLUSION = "conclusion"


@dataclass(frozen=True)
class Num:
    """A number to format per language; ``pct`` renders 0.956 as %95,6 / 95.6%."""

    value: float
    nd: int = 1
    pct: bool = False


@dataclass(frozen=True)
class Names:
    """A list of composite names, rendered "A, B" / "A ve B"."""

    items: tuple[str, ...]


@dataclass(frozen=True)
class Order:
    """A ranking, rendered "C > D > B > A"."""

    items: tuple[str, ...]


@dataclass(frozen=True)
class Values:
    """Named values, rendered "C: 2205,0; D: 1668,4"."""

    items: tuple[tuple[str, float], ...]
    nd: int = 1


Param = Num | Names | Order | Values | FiberType | str


@dataclass(frozen=True)
class Message:
    section: Section
    key: str
    params: dict[str, Any] = field(default_factory=dict)
