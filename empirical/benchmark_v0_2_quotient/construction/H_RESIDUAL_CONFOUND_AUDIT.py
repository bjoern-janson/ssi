#!/usr/bin/env python3
"""Predicate-H material-rival completeness and residual-veto audit.

Authorization-side only. This script reads only the frozen H rival manifest and
checks ledger completeness, evidence requirements, and the preregistered veto.
It does not access a future obligation, activate G, or evaluate DeltaPi.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = json.loads((HERE / "H_MATERIAL_RIVAL_MANIFEST.json").read_text())
OUT = HERE / "h_residual_confound_audit.json"

MANDATORY_BASE = {
    "H_capacity",
    "H_information",
    "H_ordinary_adapt",
    "H_current_distribution",
    "H_future_distribution",
    "H_resources",
    "H_implementation",
    "H_label_leakage",
    "H_future_selection",
    "H_differential_exposure",
    "H_evaluator",
    "H_missingness",
}

QUOTIENT_SPECIFIC = {
    "H_quotient_interpretation",
    "H_challenge_recognizability",
}

ALLOWED = set(MANIFEST["allowed_dispositions"])


def main() -> None:
    rivals = MANIFEST["rivals"]
    ids = [r["id"] for r in rivals]
    id_set = set(ids)

    duplicate_ids = sorted(k for k, v in Counter(ids).items() if v != 1)
    missing_mandatory = sorted((MANDATORY_BASE | QUOTIENT_SPECIFIC) - id_set)
    unclassified = sorted(
        r["id"] for r in rivals if r.get("disposition") not in ALLOWED
    )
    missing_required_fields = sorted(
        r.get("id", "<missing-id>")
        for r in rivals
        if not {
            "id", "entry", "material", "disposition", "unbounded",
            "effect_explaining", "evidence", "bound", "direction_alignment"
        } <= set(r)
    )
    evidence_gaps = sorted(
        r["id"] for r in rivals
        if r["disposition"] in {"BLOCKED", "MEASURED", "RANDOMIZED"}
        and not r["evidence"]
    )

    residual = [r for r in rivals if r["disposition"] == "RESIDUAL"]
    veto_rows = [
        r for r in residual
        if r["material"] and r["unbounded"] and r["effect_explaining"]
    ]

    pass_completeness = not (
        duplicate_ids or missing_mandatory or unclassified
        or missing_required_fields or evidence_gaps
    )
    h_pass = pass_completeness and not veto_rows

    out = {
        "benchmark_id": MANIFEST["benchmark_id"],
        "audit_identity": "VFA-0.2-H-RESIDUAL-CONFOUND-AUDIT-1",
        "future_obligation_accessed": False,
        "G_activation": "PROHIBITED",
        "ledger": {
            "rival_count": len(rivals),
            "mandatory_base_count": len(MANDATORY_BASE),
            "quotient_specific_required_count": len(QUOTIENT_SPECIFIC),
            "duplicate_ids": duplicate_ids,
            "missing_mandatory": missing_mandatory,
            "unclassified": unclassified,
            "missing_required_fields": missing_required_fields,
            "evidence_gaps_for_nonresidual_dispositions": evidence_gaps,
            "disposition_counts": dict(sorted(Counter(r["disposition"] for r in rivals).items())),
            "residual_ids": [r["id"] for r in residual],
            "residual_veto_ids": [r["id"] for r in veto_rows],
            "completeness_pass": pass_completeness,
        },
        "veto_rows": [
            {
                "id": r["id"],
                "entry": r["entry"],
                "material": r["material"],
                "unbounded": r["unbounded"],
                "effect_explaining": r["effect_explaining"],
                "bound": r["bound"],
                "direction_alignment": r["direction_alignment"],
            }
            for r in veto_rows
        ],
        "H_adjudication": "PASS" if h_pass else "FAIL",
        "failure_code": None if h_pass else (
            "RESIDUAL_CONFOUND_VETO" if pass_completeness and veto_rows
            else "LEDGER_INCOMPLETE"
        ),
        "authority_boundary": {
            "Delta_Pi": "NOT_EVALUATED",
            "kernel_q_subset_kernel_T_future": "NOT_EVALUATED",
            "freeze_packet": "NOT_FROZEN",
            "authorization_certificate": "NOT_ISSUED",
            "future_run": "NOT_AUTHORIZED",
        },
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "H": out["H_adjudication"],
        "rivals": len(rivals),
        "unclassified": len(unclassified),
        "residual_veto_count": len(veto_rows),
        "residual_veto_ids": [r["id"] for r in veto_rows],
        "future_obligation_accessed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
