from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable, Optional


class Status(str, Enum):
    SUPPORTED_ADEQUATE_ON_TESTED_SCOPE = "SUPPORTED_ADEQUATE_ON_TESTED_SCOPE"
    UNKNOWN = "UNKNOWN"
    INADEQUATE = "INADEQUATE"
    NOT_EVALUABLE = "NOT_EVALUABLE"


class SearchLicense(str, Enum):
    NONE = "NONE"
    LOCAL = "LOCAL"


class ConsequenceAdmissibility(str, Enum):
    ADMISSIBLE = "ADMISSIBLE"
    INADMISSIBLE = "INADMISSIBLE"


@dataclass(frozen=True)
class ConsequenceProvenance:
    source: str
    independent_of_frozen_representation: bool


@dataclass(frozen=True)
class ExternalCase:
    case_id: str
    frozen_signature: Any
    consequence: Any
    q_y: ConsequenceAdmissibility
    pi_y: ConsequenceProvenance
    scope: str
    property: str
    mapped_under_representation_id: str


@dataclass(frozen=True)
class CoverageClaim:
    constituted: bool
    required_consequences: tuple[Any, ...] = ()


@dataclass(frozen=True)
class AdequacyRequest:
    frozen_representation_id: str
    case_selection_representation_id: str
    scope: str
    property: str
    coverage: CoverageClaim
    cases: tuple[ExternalCase, ...]


@dataclass(frozen=True)
class CollisionWitness:
    case_a: str
    case_b: str
    frozen_signature: Any
    external_consequence_a: Any
    external_consequence_b: Any
    consequence_provenance_a: str
    consequence_provenance_b: str


@dataclass(frozen=True)
class AdequacyResult:
    status: Status
    witness: Optional[CollisionWitness]
    scope: str
    property: str
    search_license: SearchLicense
    ceiling: str = "ADEQUACY_ONLY"
    reason: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "status": self.status.value,
            "witness": None,
            "scope": self.scope,
            "property": self.property,
            "search_license": self.search_license.value,
            "ceiling": self.ceiling,
        }
        if self.witness is not None:
            out["witness"] = {
                "case_a": self.witness.case_a,
                "case_b": self.witness.case_b,
                "frozen_signature_a_equals_b": self.witness.frozen_signature,
                "external_consequence_a": self.witness.external_consequence_a,
                "external_consequence_b": self.witness.external_consequence_b,
                "consequence_provenance_a": self.witness.consequence_provenance_a,
                "consequence_provenance_b": self.witness.consequence_provenance_b,
            }
        if self.reason is not None:
            out["reason"] = self.reason
        return out


def _canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _not_evaluable(request: AdequacyRequest, reason: str) -> AdequacyResult:
    return AdequacyResult(
        status=Status.NOT_EVALUABLE,
        witness=None,
        scope=request.scope,
        property=request.property,
        search_license=SearchLicense.NONE,
        reason=reason,
    )


def _validate_constitution(request: AdequacyRequest) -> Optional[AdequacyResult]:
    if not request.frozen_representation_id:
        return _not_evaluable(request, "missing frozen_representation_id")

    if request.case_selection_representation_id != request.frozen_representation_id:
        return _not_evaluable(
            request,
            "representation changed after case selection",
        )

    if not request.scope or not request.property:
        return _not_evaluable(request, "scope and property must be constituted")

    if not request.cases:
        return _not_evaluable(request, "no external cases supplied")

    seen_case_ids: set[str] = set()
    for case in request.cases:
        if not case.case_id:
            return _not_evaluable(request, "case_id is required")
        if case.case_id in seen_case_ids:
            return _not_evaluable(request, f"duplicate case_id: {case.case_id}")
        seen_case_ids.add(case.case_id)

        if case.scope != request.scope or case.property != request.property:
            return _not_evaluable(
                request,
                f"case {case.case_id} is outside the constituted scope/property",
            )

        if case.mapped_under_representation_id != request.frozen_representation_id:
            return _not_evaluable(
                request,
                f"case {case.case_id} was not mapped under the frozen representation",
            )

        if case.consequence is None:
            return _not_evaluable(
                request,
                f"case {case.case_id} is missing an external consequence",
            )

        if case.q_y is not ConsequenceAdmissibility.ADMISSIBLE:
            return _not_evaluable(
                request,
                f"case {case.case_id} consequence is not an admissible discriminator",
            )

        if not case.pi_y.source.strip():
            return _not_evaluable(
                request,
                f"case {case.case_id} is missing consequence provenance",
            )

        if not case.pi_y.independent_of_frozen_representation:
            return _not_evaluable(
                request,
                f"case {case.case_id} consequence is not independently constituted",
            )

    if request.coverage.constituted:
        present = {_canon(case.consequence) for case in request.cases}
        required = {_canon(value) for value in request.coverage.required_consequences}
        if not required:
            return _not_evaluable(
                request,
                "positive coverage was claimed without required consequence classes",
            )
        if not required.issubset(present):
            return _not_evaluable(
                request,
                "positive coverage claim is not discharged by the supplied cases",
            )

    return None


def evaluate(request: AdequacyRequest) -> AdequacyResult:
    """
    Evaluate only the frozen-representation adequacy/reopening gate.

    Scientific branches:
      1. admissible consequential collision -> INADEQUATE + LOCAL search license
      2. constituted positive tested coverage with all required consequence
         distinctions preserved -> SUPPORTED_ADEQUATE_ON_TESTED_SCOPE
      3. otherwise -> UNKNOWN

    Invalid experiment constitution returns NOT_EVALUABLE and does not
    participate in the adequacy ordering.
    """
    constitution_failure = _validate_constitution(request)
    if constitution_failure is not None:
        return constitution_failure

    ordered_cases = sorted(request.cases, key=lambda case: case.case_id)

    for case_a, case_b in combinations(ordered_cases, 2):
        same_signature = _canon(case_a.frozen_signature) == _canon(case_b.frozen_signature)
        different_consequence = _canon(case_a.consequence) != _canon(case_b.consequence)
        if same_signature and different_consequence:
            witness = CollisionWitness(
                case_a=case_a.case_id,
                case_b=case_b.case_id,
                frozen_signature=case_a.frozen_signature,
                external_consequence_a=case_a.consequence,
                external_consequence_b=case_b.consequence,
                consequence_provenance_a=case_a.pi_y.source,
                consequence_provenance_b=case_b.pi_y.source,
            )
            return AdequacyResult(
                status=Status.INADEQUATE,
                witness=witness,
                scope=request.scope,
                property=request.property,
                search_license=SearchLicense.LOCAL,
            )

    if request.coverage.constituted:
        for case_a, case_b in combinations(ordered_cases, 2):
            different_consequence = _canon(case_a.consequence) != _canon(case_b.consequence)
            same_signature = _canon(case_a.frozen_signature) == _canon(case_b.frozen_signature)
            if different_consequence and same_signature:
                raise AssertionError("collision branch must dominate adequacy branch")

        return AdequacyResult(
            status=Status.SUPPORTED_ADEQUATE_ON_TESTED_SCOPE,
            witness=None,
            scope=request.scope,
            property=request.property,
            search_license=SearchLicense.NONE,
        )

    return AdequacyResult(
        status=Status.UNKNOWN,
        witness=None,
        scope=request.scope,
        property=request.property,
        search_license=SearchLicense.NONE,
    )


def request_from_dict(data: dict[str, Any]) -> AdequacyRequest:
    coverage_data = data.get("coverage") or {}
    cases: list[ExternalCase] = []

    for raw in data.get("cases", []):
        pi_y_data = raw.get("pi_y") or {}
        q_y_raw = raw.get("q_y", ConsequenceAdmissibility.INADMISSIBLE.value)
        try:
            q_y = ConsequenceAdmissibility(q_y_raw)
        except ValueError:
            q_y = ConsequenceAdmissibility.INADMISSIBLE

        cases.append(
            ExternalCase(
                case_id=str(raw.get("case_id", "")),
                frozen_signature=raw.get("frozen_signature"),
                consequence=raw.get("consequence"),
                q_y=q_y,
                pi_y=ConsequenceProvenance(
                    source=str(pi_y_data.get("source", "")),
                    independent_of_frozen_representation=bool(
                        pi_y_data.get("independent_of_frozen_representation", False)
                    ),
                ),
                scope=str(raw.get("scope", "")),
                property=str(raw.get("property", "")),
                mapped_under_representation_id=str(
                    raw.get("mapped_under_representation_id", "")
                ),
            )
        )

    return AdequacyRequest(
        frozen_representation_id=str(data.get("frozen_representation_id", "")),
        case_selection_representation_id=str(
            data.get("case_selection_representation_id", "")
        ),
        scope=str(data.get("scope", "")),
        property=str(data.get("property", "")),
        coverage=CoverageClaim(
            constituted=bool(coverage_data.get("constituted", False)),
            required_consequences=tuple(
                coverage_data.get("required_consequences", [])
            ),
        ),
        cases=tuple(cases),
    )


def _read_json(path: Optional[str]) -> dict[str, Any]:
    if path is None or path == "-":
        return json.load(__import__("sys").stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate the frozen SSI adequacy/reopening governor."
    )
    parser.add_argument(
        "request",
        nargs="?",
        default="-",
        help="JSON request path, or '-' / omitted for stdin",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        request = request_from_dict(_read_json(args.request))
        result = evaluate(request)
    except (OSError, json.JSONDecodeError) as exc:
        result = AdequacyResult(
            status=Status.NOT_EVALUABLE,
            witness=None,
            scope="",
            property="",
            search_license=SearchLicense.NONE,
            reason=f"invalid request input: {exc}",
        )

    print(json.dumps(result.to_dict(), indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
