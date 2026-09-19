import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.scoring.aggregator import ScoreAggregator
from tests.golden_set.samples import GOLDEN_SET_SAMPLES

def run_golden_set_tests():
    print("=" * 80)
    print("RUNNING ITEM #3: GOLDEN-SET REGRESSION TEST SUITE (8 SAMPLES)")
    print("=" * 80)

    total_checks = 0
    passed_checks = 0
    test_results = []

    for sample in GOLDEN_SET_SAMPLES:
        sample_id = sample["id"]
        sample_name = sample["name"]
        slides = sample["slides"]
        ps_title = sample["ps_title"]
        ps_desc = sample["ps_description"]
        expected_ranges = sample["expected_ranges"]

        print(f"\nEvaluating Sample: [{sample_id}] — {sample_name}")
        report = ScoreAggregator.process_submission(
            slides=slides,
            ps_title=ps_title,
            ps_description=ps_desc
        )

        overall_score = report.get("overall_score")
        breakdown = report.get("category_breakdown", {})

        sample_passed = True
        category_outcomes = []

        # Check category ranges
        for cat_key, (min_exp, max_exp) in expected_ranges.items():
            total_checks += 1
            if cat_key == "overall_score":
                actual_score = overall_score
            else:
                actual_score = breakdown.get(cat_key, {}).get("score")

            if actual_score is not None and min_exp <= actual_score <= max_exp:
                passed_checks += 1
                outcome_str = f"PASS ({actual_score:.1f} in [{min_exp}, {max_exp}])"
            else:
                sample_passed = False
                outcome_str = f"FAIL ({actual_score} NOT in [{min_exp}, {max_exp}])"
            
            category_outcomes.append(f"  - {cat_key}: {outcome_str}")

        status_flag = "PASS" if sample_passed else "FAIL"
        print(f"Sample Status: [{status_flag}] | Overall Score: {overall_score}")
        for outcome in category_outcomes:
            print(outcome)

        test_results.append({
            "sample_id": sample_id,
            "name": sample_name,
            "passed": sample_passed,
            "overall_score": overall_score
        })

    print("\n" + "=" * 80)
    print("GOLDEN SET REGRESSION SUITE SUMMARY:")
    print(f"Total Category Checks Asserted: {total_checks}")
    print(f"Passed Checks: {passed_checks}/{total_checks}")
    all_passed = all(r["passed"] for r in test_results)
    if all_passed:
        print("FINAL RESULT: PASS — All 8 golden-set samples satisfied expected score bounds!")
    else:
        print("FINAL RESULT: FAIL — Some golden-set score bounds were violated.")
    print("=" * 80)

if __name__ == "__main__":
    run_golden_set_tests()
