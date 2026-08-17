import unittest

from calculator import (
    AdequacyRequest,
    ConsequenceAdmissibility,
    ConsequenceProvenance,
    CoverageClaim,
    ExternalCase,
    SearchLicense,
    Status,
    evaluate,
    request_from_dict,
)


FROZEN_ID = "ssi-frozen-v1"
PROPERTY = "P"
SCOPE = "sigma"


def case(
    case_id,
    signature,
    consequence,
    *,
    q_y=ConsequenceAdmissibility.ADMISSIBLE,
    source=None,
    independent=True,
    mapped_under=FROZEN_ID,
):
    return ExternalCase(
        case_id=case_id,
        frozen_signature=signature,
        consequence=consequence,
        q_y=q_y,
        pi_y=ConsequenceProvenance(
            source=source or f"external://{case_id}",
            independent_of_frozen_representation=independent,
        ),
        scope=SCOPE,
        property=PROPERTY,
        mapped_under_representation_id=mapped_under,
    )


def request(*cases, coverage=False, required=(), selected_under=FROZEN_ID):
    return AdequacyRequest(
        frozen_representation_id=FROZEN_ID,
        case_selection_representation_id=selected_under,
        scope=SCOPE,
        property=PROPERTY,
        coverage=CoverageClaim(
            constituted=coverage,
            required_consequences=tuple(required),
        ),
        cases=tuple(cases),
    )


class AdequacyGovernorTests(unittest.TestCase):
    def test_genuine_collision_returns_one_explicit_witness(self):
        result = evaluate(
            request(
                case("a", ["same"], "ALLOW"),
                case("b", ["same"], "DENY"),
                case("c", ["different"], "ALLOW"),
            )
        )

        self.assertEqual(result.status, Status.INADEQUATE)
        self.assertEqual(result.search_license, SearchLicense.LOCAL)
        self.assertIsNotNone(result.witness)
        self.assertEqual((result.witness.case_a, result.witness.case_b), ("a", "b"))
        self.assertEqual(result.witness.external_consequence_a, "ALLOW")
        self.assertEqual(result.witness.external_consequence_b, "DENY")

    def test_positive_constituted_coverage_supports_only_tested_scope(self):
        result = evaluate(
            request(
                case("a", ["sig-a"], "ALLOW"),
                case("b", ["sig-b"], "DENY"),
                coverage=True,
                required=("ALLOW", "DENY"),
            )
        )

        self.assertEqual(
            result.status,
            Status.SUPPORTED_ADEQUATE_ON_TESTED_SCOPE,
        )
        self.assertEqual(result.search_license, SearchLicense.NONE)
        self.assertIsNone(result.witness)

    def test_legitimate_but_inconclusive_run_is_unknown(self):
        result = evaluate(
            request(
                case("a", ["sig-a"], "ALLOW"),
                case("b", ["sig-b"], "DENY"),
                coverage=False,
            )
        )

        self.assertEqual(result.status, Status.UNKNOWN)
        self.assertEqual(result.search_license, SearchLicense.NONE)

    def test_missing_frozen_signature_is_not_evaluable(self):
        result = evaluate(request(case("a", None, "ALLOW")))

        self.assertEqual(result.status, Status.NOT_EVALUABLE)
        self.assertEqual(result.search_license, SearchLicense.NONE)

    def test_missing_external_consequence_is_not_evaluable(self):
        result = evaluate(request(case("a", ["same"], None)))

        self.assertEqual(result.status, Status.NOT_EVALUABLE)
        self.assertEqual(result.search_license, SearchLicense.NONE)

    def test_representation_change_after_case_selection_is_not_evaluable(self):
        result = evaluate(
            request(
                case("a", ["sig-a"], "ALLOW"),
                selected_under="older-representation",
            )
        )

        self.assertEqual(result.status, Status.NOT_EVALUABLE)
        self.assertIn("changed after case selection", result.reason)

    def test_ssi_derived_consequence_cannot_manufacture_inadequacy(self):
        result = evaluate(
            request(
                case("a", ["same"], "ALLOW", independent=False),
                case("b", ["same"], "DENY"),
            )
        )

        self.assertEqual(result.status, Status.NOT_EVALUABLE)
        self.assertEqual(result.search_license, SearchLicense.NONE)

    def test_inadmissible_consequence_cannot_manufacture_collision(self):
        result = evaluate(
            request(
                case(
                    "a",
                    ["same"],
                    "ALLOW",
                    q_y=ConsequenceAdmissibility.INADMISSIBLE,
                ),
                case("b", ["same"], "DENY"),
            )
        )

        self.assertEqual(result.status, Status.NOT_EVALUABLE)
        self.assertEqual(result.search_license, SearchLicense.NONE)

    def test_positive_coverage_claim_requires_required_consequence_classes(self):
        result = evaluate(
            request(
                case("a", ["sig-a"], "ALLOW"),
                coverage=True,
                required=("ALLOW", "DENY"),
            )
        )

        self.assertEqual(result.status, Status.NOT_EVALUABLE)

    def test_case_must_be_mapped_under_frozen_representation(self):
        result = evaluate(
            request(
                case(
                    "a",
                    ["sig-a"],
                    "ALLOW",
                    mapped_under="different-representation",
                )
            )
        )

        self.assertEqual(result.status, Status.NOT_EVALUABLE)

    def test_json_parser_defaults_missing_q_y_to_inadmissible(self):
        raw = {
            "frozen_representation_id": FROZEN_ID,
            "case_selection_representation_id": FROZEN_ID,
            "scope": SCOPE,
            "property": PROPERTY,
            "coverage": {"constituted": False, "required_consequences": []},
            "cases": [
                {
                    "case_id": "a",
                    "frozen_signature": ["sig-a"],
                    "consequence": "ALLOW",
                    "pi_y": {
                        "source": "external://a",
                        "independent_of_frozen_representation": True,
                    },
                    "scope": SCOPE,
                    "property": PROPERTY,
                    "mapped_under_representation_id": FROZEN_ID,
                }
            ],
        }

        parsed = request_from_dict(raw)
        result = evaluate(parsed)

        self.assertEqual(result.status, Status.NOT_EVALUABLE)


if __name__ == "__main__":
    unittest.main()
