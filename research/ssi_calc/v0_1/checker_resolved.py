#!/usr/bin/env python3
"""SSI-CALC v0.1 successor-v3: path-aware obligation resolution.

R1..R11 are unchanged. This layer preserves the typed live-authority membrane from
checker_live.py and changes only obligation resolution:

- represented history may create an obligation;
- live, typed, independently sufficient routes may discharge it;
- inactive/unresolved alternative routes may not veto an already discharged goal;
- explicit mandatory historical gates still run before discharge;
- active counterevidence remains visible to the live-only evaluator.

Derivation never reads benchmark family metadata or case['expected'].
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import jsonschema
import checker_live as prior

RULES = prior.RULES
Certificate = prior.Certificate
AUTHORIZED = {"AUTHORIZED", "AUTHORIZED_SCOPED"}


@dataclass(frozen=True)
class Resolution:
    state: Literal["DISCHARGED", "UNRESOLVED", "REFUSED"]
    certificate: Certificate
    source: str


def _live_candidate(view: prior.AuthorityView, schema: dict) -> Certificate:
    """Evaluate only currently live authority through the existing R1..R11 engine."""
    return prior._rebase_preservation(
        view,
        prior.prior.derive(view.projected_raw(), schema),
    )


def resolve_goal(view: prior.AuthorityView, schema: dict) -> Resolution:
    """Resolve one current obligation without treating alternatives as conjunctions.

    Ordering is deliberate:
    1. Mandatory historical gates may create non-optional obligations. These are
       not alternative proof channels and therefore retain priority.
    2. Provenance-to-semantic gates remain explicit bridge obligations.
    3. The live-only evaluator searches for an independently sufficient route.
       If one exists, the goal is discharged even if some *alternative* represented
       route is inactive or unresolved.
    4. Only when no live sufficient route exists may represented-but-inactive
       premises determine NOT_IDENTIFIED.
    5. Otherwise return the live evaluator's refusal/non-identification result.

    Active counterevidence is not filtered here: it remains in projected_raw() and
    therefore participates in the live-only evaluator. This layer does not turn
    authorization into a blanket override of active negative evidence.
    """
    mandatory = prior._historical_obligation_gate(view)
    if mandatory is not None:
        return Resolution("REFUSED", mandatory, "mandatory_historical_gate")

    provenance = prior._provenance_goal(view)
    if provenance is not None:
        state = "DISCHARGED" if provenance.status in AUTHORIZED else "REFUSED"
        return Resolution(state, provenance, "typed_provenance_gate")

    live = _live_candidate(view, schema)
    if live.status in AUTHORIZED:
        return Resolution("DISCHARGED", live, "live_sufficient_path")

    inactive = prior._inactive_obligation(view)
    if inactive is not None:
        return Resolution("UNRESOLVED", inactive, "inactive_or_unresolved_alternative")

    return Resolution("REFUSED", live, "live_evaluator")


def derive(raw: dict, schema: dict) -> Certificate:
    jsonschema.Draft202012Validator(schema).validate(raw)
    view = prior.AuthorityView(raw)
    return resolve_goal(view, schema).certificate


def load_json(path):
    return prior.load_json(path)
