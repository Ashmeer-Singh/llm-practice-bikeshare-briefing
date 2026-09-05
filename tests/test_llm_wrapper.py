"""Automated practice checks.

These run locally (`pytest -v`) and again in GitHub Actions once your pull
request's workflow run is approved. They check that your wrapper is built
correctly and safely, not that your briefing text uses any particular
wording - there is no single correct sentence, only a correctly grounded
one. This is exactly the kind of technical check the Final Assessment's
own workflow will run on your submission, so treat a red test here as a
preview of what a marker's CI would flag.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.app import (
    CANDIDATE_ACTIONS,
    REQUIRED_FACTS,
    build_validated_context,
    load_json,
    run,
)
from src.llm_wrapper import (
    DEFAULT_EXAMPLE,
    DEFAULT_INSTRUCTION,
    build_prompt,
    check_critical_facts,
    generate_briefing,
    offline_briefing,
    reject_unsupported_actions,
)

CASE_PATH = "data/station_case.json"
TRACE_PATH = "data/decision_trace.json"


@pytest.fixture(scope="module")
def validated_context():
    case = load_json(CASE_PATH)
    trace = load_json(TRACE_PATH)
    return build_validated_context(case, trace)


def test_build_prompt_contains_all_three_parts(validated_context):
    prompt = build_prompt(DEFAULT_INSTRUCTION, validated_context, DEFAULT_EXAMPLE)
    assert DEFAULT_INSTRUCTION in prompt, "the instruction must appear in the prompt, verbatim"
    assert DEFAULT_EXAMPLE in prompt, "the example must appear in the prompt, verbatim"
    assert validated_context["station_id"] in prompt, (
        "the validated context must appear in the prompt - station_id is a quick way to check "
        "the whole dict was actually included, not just summarised"
    )


def test_offline_briefing_is_deterministic(validated_context):
    first = offline_briefing(validated_context)
    second = offline_briefing(validated_context)
    assert first == second, (
        "offline_briefing must be deterministic - the same input must always produce the same "
        "output, with no randomness and no network call involved"
    )


def test_offline_briefing_reports_required_numbers(validated_context):
    briefing = offline_briefing(validated_context)
    assert str(validated_context["bikes_available"]) in briefing
    assert str(validated_context["docks_available"]) in briefing
    assert validated_context["station_id"] in briefing


def test_offline_briefing_states_unknown_facts_explicitly(validated_context):
    briefing = offline_briefing(validated_context)
    assert "unknown" in briefing.lower(), (
        "current_temperature_c is null in station_case.json - your briefing must say this fact "
        "is unknown rather than silently omitting it or inventing a plausible-sounding number"
    )


def test_offline_briefing_never_mentions_unvalidated_action(validated_context):
    briefing = offline_briefing(validated_context)
    for action in CANDIDATE_ACTIONS:
        if action not in validated_context["validated_actions"]:
            assert action not in briefing, (
                f"'{action}' is not in validated_actions - a correct briefing must never "
                "recommend an action the rule engine and planner did not validate"
            )


def test_check_critical_facts_flags_a_genuinely_missing_fact(validated_context):
    briefing = offline_briefing(validated_context)
    missing = check_critical_facts(briefing, validated_context, REQUIRED_FACTS)
    assert missing == [], f"expected all required facts present in a correct briefing, got missing={missing}"

    incomplete_briefing = "Nothing useful to report."
    missing_from_bad_briefing = check_critical_facts(incomplete_briefing, validated_context, REQUIRED_FACTS)
    assert set(REQUIRED_FACTS).issubset(set(missing_from_bad_briefing)), (
        "check_critical_facts must actually detect a fact that is missing, not always return []"
    )


def test_reject_unsupported_actions_catches_a_hallucinated_action(validated_context):
    validated_actions = validated_context["validated_actions"]

    clean_briefing = "Recommended action: dispatch_rebalancing_van. Human approval is required."
    assert reject_unsupported_actions(clean_briefing, validated_actions, CANDIDATE_ACTIONS) == []

    hallucinating_briefing = (
        "Recommended action: dispatch_rebalancing_van and close_station immediately."
    )
    rejected = reject_unsupported_actions(hallucinating_briefing, validated_actions, CANDIDATE_ACTIONS)
    assert "close_station" in rejected, (
        "close_station is not in validated_actions - reject_unsupported_actions must catch a "
        "briefing that recommends it anyway, exactly the way a marker's unseen-mutation check would"
    )
    assert "dispatch_rebalancing_van" not in rejected, (
        "dispatch_rebalancing_van IS validated - it must not be rejected"
    )


def test_generate_briefing_offline_mode_matches_offline_briefing(validated_context):
    assert generate_briefing(validated_context, mode="offline") == offline_briefing(validated_context)


def test_generate_briefing_rejects_unknown_mode(validated_context):
    with pytest.raises(ValueError):
        generate_briefing(validated_context, mode="paid-api-please")


def test_run_writes_briefing_and_result_files(tmp_path):
    output_path = tmp_path / "result.json"
    result = run(CASE_PATH, TRACE_PATH, str(output_path))

    assert output_path.exists(), "run() must write its result to --output"
    briefing_path = output_path.parent / "briefing.txt"
    assert briefing_path.exists(), "run() must also write outputs/briefing.txt, exactly like the Final Assessment's own outputs/ convention"

    with open(output_path) as f:
        saved = json.load(f)
    assert saved == result
    assert saved["safe_to_show_officer"] is True, (
        "with the supplied case and a correct offline_briefing(), nothing should be missing or "
        "rejected - if this is False, re-check offline_briefing() before your check functions"
    )
