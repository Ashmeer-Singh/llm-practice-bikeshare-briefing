"""Wires the four TODOs in src/llm_wrapper.py into one runnable briefing
pipeline - provided, you should not need to edit this file, but read it so
you know exactly what your functions are called with.

Run it with:
    python -m src.app --case data/station_case.json --trace data/decision_trace.json --output outputs/result.json

Check your work with:
    pytest -v
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.llm_wrapper import (
    check_critical_facts,
    generate_briefing,
    reject_unsupported_actions,
)

# The two critical facts every briefing must get right (Task 5c: "check two
# critical facts"). Chosen because they are the numbers a human officer
# would act on immediately.
REQUIRED_FACTS = ["bikes_available", "docks_available"]

# One validated action plus one DELIBERATELY unsupported action, so the
# reject_unsupported_actions() TODO has something real to catch if a
# briefing ever mentions it. A correct offline_briefing() never mentions
# "close_station" - it is not in validated_actions.
CANDIDATE_ACTIONS = ["dispatch_rebalancing_van", "notify_zone_supervisor", "close_station"]


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_validated_context(case: dict, trace: dict) -> dict:
    """Merge the station case and the (already-validated) decision trace
    into the single validated_context your llm_wrapper.py functions
    consume. Provided - this merge step is not one of your TODOs.
    """
    context = dict(case)
    context["decision"] = trace["decision"]
    context["validated_actions"] = trace["validated_actions"]
    context["unknown_facts"] = trace["unknown_facts"]
    return context


def run(case_path: str = "data/station_case.json", trace_path: str = "data/decision_trace.json", output_path: str = "outputs/result.json") -> dict:
    case = load_json(case_path)
    trace = load_json(trace_path)
    validated_context = build_validated_context(case, trace)

    briefing_text = generate_briefing(validated_context, mode="offline")

    missing_facts = check_critical_facts(briefing_text, validated_context, REQUIRED_FACTS)
    rejected_actions = reject_unsupported_actions(
        briefing_text, validated_context["validated_actions"], CANDIDATE_ACTIONS
    )

    result = {
        "case_id": case["case_id"],
        "station_id": case["station_id"],
        "briefing": briefing_text,
        "required_facts_checked": REQUIRED_FACTS,
        "missing_facts": missing_facts,
        "candidate_actions_checked": CANDIDATE_ACTIONS,
        "rejected_actions": rejected_actions,
        "safe_to_show_officer": not missing_facts and not rejected_actions,
    }

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")

    briefing_path = output.parent / "briefing.txt"
    briefing_path.write_text(briefing_text + "\n", encoding="utf-8")

    print(briefing_text)
    print()
    if missing_facts:
        print(f"MISSING FACTS (fix offline_briefing): {missing_facts}")
    if rejected_actions:
        print(f"REJECTED ACTIONS (fix offline_briefing): {rejected_actions}")
    if not missing_facts and not rejected_actions:
        print("All required facts present; no unsupported action recommended.")

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", default="data/station_case.json")
    parser.add_argument("--trace", default="data/decision_trace.json")
    parser.add_argument("--output", default="outputs/result.json")
    args = parser.parse_args()
    run(args.case, args.trace, args.output)


if __name__ == "__main__":
    main()
