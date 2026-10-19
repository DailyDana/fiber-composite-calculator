"""Explain a ranking factor by factor: fiber type, Vf, length, matrix.

Each rule looks at the computed results only; nothing here is specific to the
Concept Check 16.2 data. The order of the returned messages is the order of
the report sections.
"""

from __future__ import annotations

import itertools
from collections.abc import Sequence

from app.core.models import CompositeResult, FiberType, LengthRegime, RankingResult
from app.interpret.messages import Message, Names, Num, Order, Section

__all__ = ["MATRIX_REALISTIC_LIMIT", "SMALL_EFFICIENCY_SPREAD", "explain"]

#: A common σm' above this (MPa) is out of reach for polymer matrices, whose
#: tensile strengths are typically below ~100 MPa; σm' cannot exceed them.
MATRIX_REALISTIC_LIMIT = 200.0

#: Length efficiencies spanning less than this are called "close".
SMALL_EFFICIENCY_SPREAD = 0.05


def _names(rs: Sequence[CompositeResult]) -> Names:
    """Composite names in natural (alphabetical) order: "A and B", not "B and A"."""
    return Names(tuple(sorted(r.spec.name for r in rs)))


def _groups(results: Sequence[CompositeResult]) -> dict[FiberType, list[CompositeResult]]:
    """Fiber-type groups, strongest fiber first; members keep the ranking order."""
    groups: dict[FiberType, list[CompositeResult]] = {}
    for r in results:
        groups.setdefault(r.spec.fiber_type, []).append(r)
    return dict(
        sorted(groups.items(), key=lambda kv: -max(r.spec.sigma_f for r in kv[1])),
    )


def _fiber(results: Sequence[CompositeResult]) -> list[Message]:
    groups = _groups(results)
    out: list[Message] = []
    if len(groups) == 1:
        ((ftype, members),) = groups.items()
        out.append(Message(Section.FIBER, "fiber.single", {"type": ftype}))
        return out

    for ftype, members in groups.items():
        sig = sorted({r.spec.sigma_f for r in members})
        key = "fiber.group" if len(sig) == 1 else "fiber.group_range"
        out.append(
            Message(
                Section.FIBER,
                key,
                {
                    "type": ftype,
                    "names": _names(members),
                    "lo": Num(sig[0], 0),
                    "hi": Num(sig[-1], 0),
                },
            )
        )

    (top_type, top), *_, (low_type, low) = groups.items()
    top_sigma = max(r.spec.sigma_f for r in top)
    low_sigma = max(r.spec.sigma_f for r in low)
    out.append(
        Message(
            Section.FIBER,
            "fiber.ratio",
            {"top": top_type, "low": low_type, "ratio": Num(top_sigma / low_sigma, 2)},
        )
    )

    rank_of = {r.spec.name: i for i, r in enumerate(results)}
    others = [r for r in results if r.spec.fiber_type is not top_type]
    if max(rank_of[r.spec.name] for r in top) < min(rank_of[r.spec.name] for r in others):
        out.append(
            Message(Section.FIBER, "fiber.dominant", {"type": top_type, "names": _names(top)})
        )
    else:
        # A weaker fiber outranks a stronger one: name the first such pair.
        for lower in top:
            above = [r for r in others if rank_of[r.spec.name] < rank_of[lower.spec.name]]
            if above:
                upper = above[-1]
                out.append(
                    Message(
                        Section.FIBER,
                        "fiber.overtaken",
                        {
                            "upper": upper.spec.name,
                            "lower": lower.spec.name,
                            "upper_type": upper.spec.fiber_type,
                            "lower_type": lower.spec.fiber_type,
                            "upper_vf": Num(upper.spec.vf, 2),
                            "lower_vf": Num(lower.spec.vf, 2),
                        },
                    )
                )
                break
    return out


def _vf(results: Sequence[CompositeResult]) -> list[Message]:
    out: list[Message] = []
    for members in _groups(results).values():
        for hi, lo in itertools.pairwise(members):
            params = {
                "hi": hi.spec.name,
                "lo": lo.spec.name,
                "hi_vf": Num(hi.spec.vf, 2),
                "lo_vf": Num(lo.spec.vf, 2),
                "vf_ratio": Num(hi.spec.vf / lo.spec.vf, 2),
                "str_ratio": Num(hi.fiber_term / lo.fiber_term, 2),
            }
            if hi.spec.vf > lo.spec.vf:
                # "Almost all of the gap comes from Vf" only when the two ratios agree.
                agree = abs(params["str_ratio"].value / params["vf_ratio"].value - 1) < 0.05
                key = "vf.follows" if agree else "vf.follows_other"
            elif hi.spec.vf == lo.spec.vf:
                key = "vf.equal"
            else:
                key = "vf.against"
            out.append(Message(Section.VF, key, params))
    if out:
        out.insert(0, Message(Section.VF, "vf.rule"))
    else:
        out.append(Message(Section.VF, "vf.no_pairs"))
    return out


def _length(results: Sequence[CompositeResult], fiber_order: Sequence[str]) -> list[Message]:
    out: list[Message] = []
    short = [r for r in results if r.regime is LengthRegime.SHORT]
    if short:
        out.append(Message(Section.LENGTH, "len.short", {"names": _names(short)}))
    else:
        worst = min(results, key=lambda r: r.length_ratio)
        out.append(
            Message(
                Section.LENGTH,
                "len.all_long",
                {"name": worst.spec.name, "ratio": Num(worst.length_ratio, 1)},
            )
        )

    lo = min(results, key=lambda r: r.efficiency)
    hi = max(results, key=lambda r: r.efficiency)
    out.append(
        Message(
            Section.LENGTH,
            "len.efficiency",
            {
                "lo": lo.spec.name,
                "lo_eff": Num(lo.efficiency, 1, pct=True),
                "hi": hi.spec.name,
                "hi_eff": Num(hi.efficiency, 1, pct=True),
            },
        )
    )

    longest = max(results, key=lambda r: r.spec.l)
    if len({r.spec.l for r in results}) > 1:
        out.append(
            Message(
                Section.LENGTH,
                "len.longest",
                {
                    "name": longest.spec.name,
                    "l": Num(longest.spec.l, 1),
                    "lc": Num(longest.spec.lc, 2),
                    "ratio": Num(longest.length_ratio, 1),
                },
            )
        )

    product_order = tuple(
        r.spec.name for r in sorted(results, key=lambda r: -(r.spec.sigma_f * r.spec.vf))
    )
    if product_order == tuple(fiber_order):
        spread = hi.efficiency - lo.efficiency
        key = (
            "len.no_order_change"
            if spread < SMALL_EFFICIENCY_SPREAD
            else "len.no_order_change_wide"
        )
        out.append(Message(Section.LENGTH, key, {"product_order": Order(product_order)}))
    else:
        out.append(
            Message(
                Section.LENGTH,
                "len.order_change",
                {"product_order": Order(product_order), "fiber_order": Order(tuple(fiber_order))},
            )
        )

    near = [r for r in results if r.near_continuous]
    far = [r for r in results if not r.near_continuous]
    if near and far:
        out.append(
            Message(
                Section.LENGTH,
                "len.near_continuous_some",
                {"near": _names(near), "far": _names(far)},
            )
        )
    elif near:
        out.append(Message(Section.LENGTH, "len.near_continuous_all"))
    else:
        out.append(Message(Section.LENGTH, "len.near_continuous_none"))
    return out


def _matrix(ranking: RankingResult) -> list[Message]:
    out: list[Message] = []
    th = ranking.flip_threshold
    if ranking.sigma_m_prime is None:
        out.append(Message(Section.MATRIX, "mat.unknown"))
    else:
        out.append(
            Message(Section.MATRIX, "mat.included", {"value": Num(ranking.sigma_m_prime, 1)})
        )
        if ranking.matrix_changed_order:
            out.append(
                Message(
                    Section.MATRIX,
                    "mat.changed_order",
                    {
                        "fiber_order": Order(ranking.fiber_only_order),
                        "order": Order(ranking.order),
                    },
                )
            )
    if th is None:
        out.append(Message(Section.MATRIX, "mat.no_flip"))
        return out
    out.append(
        Message(
            Section.MATRIX,
            "mat.threshold",
            {"value": Num(th.sigma_m, 0), "upper": th.upper, "lower": th.lower},
        )
    )
    key = "mat.unrealistic" if th.sigma_m > MATRIX_REALISTIC_LIMIT else "mat.sensitive"
    out.append(
        Message(
            Section.MATRIX,
            key,
            {"limit": Num(MATRIX_REALISTIC_LIMIT, 0), "value": Num(th.sigma_m, 0)},
        )
    )
    return out


def _conclusion(
    ranking: RankingResult,
    fiber_msgs: Sequence[Message],
    length_msgs: Sequence[Message],
    matrix_msgs: Sequence[Message],
) -> list[Message]:
    top, bottom = ranking.results[0], ranking.results[-1]
    out = [
        Message(
            Section.CONCLUSION,
            "concl.summary",
            {
                "order": Order(ranking.order),
                "top": top.spec.name,
                "top_value": Num(top.strength, 1),
                "bottom": bottom.spec.name,
                "bottom_value": Num(bottom.strength, 1),
            },
        )
    ]
    keys = {m.key for m in fiber_msgs}
    if "fiber.dominant" in keys:
        out.append(Message(Section.CONCLUSION, "concl.driver_type_then_vf"))
    elif "fiber.single" in keys:
        out.append(Message(Section.CONCLUSION, "concl.driver_vf"))
    else:
        out.append(Message(Section.CONCLUSION, "concl.driver_product"))
    length_keys = {m.key for m in length_msgs}
    out.append(
        Message(
            Section.CONCLUSION,
            "concl.length_major" if "len.order_change" in length_keys else "concl.length_minor",
        )
    )
    matrix_keys = {m.key for m in matrix_msgs}
    robust = matrix_keys & {"mat.unrealistic", "mat.no_flip"}
    out.append(
        Message(
            Section.CONCLUSION,
            "concl.matrix_robust" if robust else "concl.matrix_sensitive",
        )
    )
    return out


def explain(ranking: RankingResult) -> list[Message]:
    """All interpretation messages for a ranking, grouped by section in order."""
    results = ranking.results
    ordered_by_fiber = sorted(results, key=lambda r: -r.fiber_term)
    fiber_msgs = _fiber(results)
    rank_msg = Message(
        Section.RANKING,
        "rank.order" if ranking.sigma_m_prime is None else "rank.order_with_matrix",
        {"order": Order(ranking.order)},
    )
    length_msgs = _length(ordered_by_fiber, ranking.fiber_only_order)
    matrix_msgs = _matrix(ranking)
    return [
        rank_msg,
        *fiber_msgs,
        *_vf(results),
        *length_msgs,
        *matrix_msgs,
        *_conclusion(ranking, fiber_msgs, length_msgs, matrix_msgs),
    ]
