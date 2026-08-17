from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
CALC_DIR = REPO_ROOT / "tools" / "ssi_adeq_calc"
CALC_PATH = CALC_DIR / "calculator.py"

EXPECTED_BLOB = "ab991327d3b3aac298abda9d612d2a9565263498"
FROZEN_ID = "ssi-adeq-calc-pr63-v0.1"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def c(cid, sig, y, scope, prop, *, q="ADMISSIBLE", independent=True,
      source=None, mapped=FROZEN_ID):
    return {
        "case_id": cid,
        "frozen_signature": sig,
        "consequence": y,
        "q_y": q,
        "pi_y": {
            "source": source or f"external://hostile-v0.1/{cid}",
            "independent_of_frozen_representation": independent,
        },
        "scope": scope,
        "property": prop,
        "mapped_under_representation_id": mapped,
    }


def r(scope, prop, cases, *, selected=FROZEN_ID, coverage=False, required=()):
    return {
        "frozen_representation_id": FROZEN_ID,
        "case_selection_representation_id": selected,
        "scope": scope,
        "property": prop,
        "coverage": {
            "constituted": coverage,
            "required_consequences": list(required),
        },
        "cases": cases,
    }


def e(status, license_, scope, prop, witness=None):
    out = {
        "status": status,
        "search_license": license_,
        "scope": scope,
        "property": prop,
    }
    if witness is not None:
        out["witness_case_ids"] = witness
    return out


def vectors():
    out = []

    s, p = "sigma:h1", "P:h1"
    out.append({
        "id": "H1_GENUINE_CONSEQUENTIAL_COLLISION",
        "attack_class": "MISSED_INADEQUACY",
        "request": r(s, p, [
            c("h1_a", ["same"], "ALLOW", s, p),
            c("h1_b", ["same"], "DENY", s, p),
            c("h1_c", ["other"], "ALLOW", s, p),
        ]),
        "expected": e("INADEQUATE", "LOCAL", s, p, ["h1_a", "h1_b"]),
    })

    s, p = "sigma:h2", "P:h2"
    out.append({
        "id": "H2_UNPROVEN_CONSEQUENCE_COLLISION_SHAPE",
        "attack_class": "FALSE_INADEQUACY_OR_STATUS_OVERREACH",
        "tension": (
            "Frozen PR63 maps any inadmissible consequence to NOT_EVALUABLE; "
            "the hostile oracle asks whether an otherwise legitimate unresolved "
            "comparison should remain scientific UNKNOWN."
        ),
        "request": r(s, p, [
            c("h2_a", ["same"], "ALLOW", s, p),
            c("h2_b", ["same"], "DENY", s, p, q="INADMISSIBLE"),
        ]),
        "expected": e("UNKNOWN", "NONE", s, p),
    })

    s, p = "sigma:h3", "P:h3"
    out.append({
        "id": "H3_MISSING_FROZEN_SIGNATURE",
        "attack_class": "FALSE_INADEQUACY",
        "request": r(s, p, [c("h3_a", None, "ALLOW", s, p)]),
        "expected": e("NOT_EVALUABLE", "NONE", s, p),
    })

    s, p = "sigma:h4", "P:h4"
    out.append({
        "id": "H4_SSI_DERIVED_EXTERNAL_CONSEQUENCE",
        "attack_class": "FALSE_INADEQUACY",
        "request": r(s, p, [
            c("h4_a", ["same"], "ALLOW", s, p, independent=False,
              source="ssi://derived/h4_a"),
            c("h4_b", ["same"], "DENY", s, p),
        ]),
        "expected": e("NOT_EVALUABLE", "NONE", s, p),
    })

    s, p = "sigma:h5", "P:h5"
    out.append({
        "id": "H5_REPRESENTATION_CHANGED_AFTER_CASE_SELECTION",
        "attack_class": "FREEZE_VIOLATION",
        "request": r(
            s, p, [c("h5_a", ["sig-a"], "ALLOW", s, p)],
            selected="older-representation",
        ),
        "expected": e("NOT_EVALUABLE", "NONE", s, p),
    })

    s, p = "sigma:h6", "P:h6"
    out.append({
        "id": "H6_INSUFFICIENT_POSITIVE_COVERAGE",
        "attack_class": "FALSE_ADEQUACY",
        "request": r(s, p, [
            c("h6_a", ["sig-a"], "ALLOW", s, p),
            c("h6_b", ["sig-b"], "DENY", s, p),
        ]),
        "expected": e("UNKNOWN", "NONE", s, p),
    })

    s, p = "sigma:h7", "P:h7"
    out.append({
        "id": "H7_BOUNDED_POSITIVE_TESTED_COVERAGE",
        "attack_class": "ADEQUACY_SCOPE_CONTROL",
        "request": r(s, p, [
            c("h7_a", ["sig-a"], "ALLOW", s, p),
            c("h7_b", ["sig-b"], "DENY", s, p),
        ], coverage=True, required=("ALLOW", "DENY")),
        "expected": e("SUPPORTED_ADEQUATE_ON_TESTED_SCOPE", "NONE", s, p),
    })

    s, p = "sigma:h8/local", "P:h8/local"
    out.append({
        "id": "H8_LOCAL_COLLISION_SCOPE_BINDING",
        "attack_class": "SCOPE_LEAKAGE",
        "request": r(s, p, [
            c("h8_a", {"bucket": 1}, "ALLOW", s, p),
            c("h8_b", {"bucket": 1}, "DENY", s, p),
        ]),
        "expected": e("INADEQUATE", "LOCAL", s, p, ["h8_a", "h8_b"]),
    })

    s, p = "sigma:h9", "P:h9"
    out.append({
        "id": "H9_SELF_ASSERTED_COVERAGE_PROVENANCE",
        "attack_class": "FALSE_ADEQUACY",
        "external_oracle": {
            "coverage_independently_constituted": False,
            "note": (
                "PR63 has no coverage-provenance input. The request deliberately "
                "self-asserts coverage.constituted=true."
            ),
        },
        "tension": (
            "If PR63 returns SUPPORTED_ADEQUATE_ON_TESTED_SCOPE, preserve it as "
            "a possible coverage-provenance/interface witness; do not repair."
        ),
        "request": r(s, p, [
            c("h9_a", ["sig-a"], "ALLOW", s, p),
            c("h9_b", ["sig-b"], "DENY", s, p),
        ], coverage=True, required=("ALLOW", "DENY")),
        "expected": e("UNKNOWN", "NONE", s, p),
    })

    s, p = "sigma:h10", "P:h10"
    out.append({
        "id": "H10_NO_COLLISION_NO_COVERAGE_CONTROL",
        "attack_class": "UNKNOWN_CONTROL",
        "request": r(s, p, [
            c("h10_a", ["same"], "ALLOW", s, p),
            c("h10_b", ["same"], "ALLOW", s, p),
        ]),
        "expected": e("UNKNOWN", "NONE", s, p),
    })
    return out


def load_calculator():
    observed_blob = git_blob_sha(CALC_PATH)
    if observed_blob != EXPECTED_BLOB:
        raise RuntimeError(
            f"frozen governor mismatch: expected {EXPECTED_BLOB}, got {observed_blob}"
        )
    sys.path.insert(0, str(CALC_DIR))
    import calculator  # type: ignore
    return calculator


def check(calculator: Any, vector: dict[str, Any]) -> dict[str, Any]:
    observed = calculator.evaluate(
        calculator.request_from_dict(vector["request"])
    ).to_dict()
    expected = vector["expected"]
    mismatches = []

    for key in ("status", "search_license", "scope", "property"):
        if observed.get(key) != expected.get(key):
            mismatches.append(
                f"{key}: expected {expected.get(key)!r}, "
                f"observed {observed.get(key)!r}"
            )

    witness_ids = expected.get("witness_case_ids")
    if witness_ids is not None:
        witness = observed.get("witness")
        got = None if witness is None else [witness.get("case_a"), witness.get("case_b")]
        if got != witness_ids:
            mismatches.append(
                f"witness_case_ids: expected {witness_ids!r}, observed {got!r}"
            )

    if observed.get("status") != "INADEQUATE" and observed.get("search_license") != "NONE":
        mismatches.append("authority leak: non-INADEQUATE result granted search license")
    if observed.get("ceiling") != "ADEQUACY_ONLY":
        mismatches.append(
            f"ceiling: expected 'ADEQUACY_ONLY', observed {observed.get('ceiling')!r}"
        )

    return {
        "id": vector["id"],
        "attack_class": vector["attack_class"],
        "pass": not mismatches,
        "expected": expected,
        "observed": observed,
        "mismatches": mismatches,
        "tension": vector.get("tension"),
        "external_oracle": vector.get("external_oracle"),
    }


def main() -> int:
    calculator = load_calculator()
    results = [check(calculator, v) for v in vectors()]
    passed = sum(item["pass"] for item in results)
    print(json.dumps({
        "suite_id": "SSI_ADEQ_GOVERNOR_HOSTILE_V0_1",
        "frozen_governor_commit": "00812d117bc083de78408a1f0d78fb54fb806228",
        "frozen_calculator_blob": EXPECTED_BLOB,
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "all_passed": passed == len(results),
        "results": results,
        "repair_permitted": False,
        "authority_ceiling": "GOVERNOR_EVALUATION_ONLY",
    }, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
