"""LLM WRAPPER PRACTICE: Bike-Share Rebalancing Briefing
==========================================================

Trains the exact skills the Final Assessment's Task 5 (GenAI, LLM API use
and ethical assurance, 10 marks) will check: construct a grounded prompt
from an instruction, a validated context and one example; generate a
deterministic offline briefing; check the briefing against critical facts;
and reject any action the briefing mentions that upstream logic never
validated.

Complete every TODO below. Do not rename the functions or their arguments -
the tests and the CI workflow call these functions directly by name.

Nothing in this file requires a network call, an account or a payment of
any kind. `mode="offline"` (the path every test and the CI workflow use)
never leaves your machine. `mode="live"` is an optional, ungraded stretch
covered in `try_local_model()` below and in INSTRUCTOR_SETUP.md - read the
note on that function before you touch it.
"""
from __future__ import annotations

import socket
from typing import Any

DEFAULT_INSTRUCTION = (
    "Write a short briefing for the on-duty bike-share operations officer. "
    "Use only the facts given below. State plainly if a fact is unknown. "
    "Recommend only actions that appear in the validated actions list."
)

DEFAULT_EXAMPLE = (
    "Station STN-010, zone SOUTH-CAMPUS: 1 bike available, 6 free docks, "
    "demand falling. Decision: monitor. Validated actions: none required. "
    "Unknown facts: none. "
    "Briefing: \"Station STN-010 is stable with 1 bike and 6 free docks; "
    "demand is falling. No action is required. Continue routine "
    "monitoring.\""
)


def build_prompt(instruction: str, validated_context: dict[str, Any], example: str) -> str:
    """TODO 1 (Task 5a): return ONE prompt string that clearly labels and
    contains all three required parts, in this order:

      1. the instruction (the `instruction` argument, verbatim)
      2. the example (the `example` argument, verbatim)
      3. the validated context (the `validated_context` argument - you may
         format the dict however you like, but every key/value pair must
         appear somewhere in the resulting string)

    This mirrors the Final Assessment's own build_prompt(): a prompt this
    function returns is never sent anywhere by itself - it exists so a
    human (or a marker) can see exactly what evidence the briefing is
    grounded in, and so `offline_briefing()` and `try_local_model()` both
    work from the same evidence.

    Label each section plainly, for example:
        "Instruction: ...\\nExample: ...\\nValidated context: {...}"
    """
    raise NotImplementedError(
        "build_prompt: combine instruction, example and validated_context into one labelled string"
    )


def offline_briefing(validated_context: dict[str, Any]) -> str:
    """TODO 2 (Task 5a/b): return a short, deterministic briefing built
    ONLY from `validated_context` - no network call, no randomness, no
    invented facts. Calling this twice with the same input must return the
    exact same string (test_offline_briefing_is_deterministic checks this
    directly).

    Your briefing text must:
      - name the station (`station_id`) and zone (`zone`);
      - state `bikes_available` and `docks_available`;
      - state the `decision` and every action in `validated_actions` -
        these two are actually read from `validated_context` too (the
        caller merges the case and the decision trace before calling this
        function - see `run()` in app.py);
      - explicitly say a fact is "unknown" for every field name listed in
        `validated_context.get("unknown_facts", [])`, rather than
        inventing a plausible-sounding number or guessing;
      - end with a line stating that human approval is required before
        any action is taken (never let the briefing itself authorise
        anything).

    Do not mention any action that is not in `validated_context
    ["validated_actions"]` - a later TODO (`reject_unsupported_actions`)
    exists specifically to catch a briefing that breaks this rule, but the
    correct fix is to never generate one that does.
    """
    raise NotImplementedError(
        "offline_briefing: build a deterministic briefing string from validated_context only"
    )


def try_local_model(prompt: str, validated_context: dict[str, Any], host: str = "localhost", port: int = 11434, timeout: float = 0.3) -> str:
    """Provided - optional stretch, not required for any Task 5 mark and
    not exercised by the automated tests or the CI workflow.

    This checks, quickly and safely, whether a fully local Ollama server
    (https://ollama.com) happens to be running on this machine, so a
    genuinely free, zero-account, zero-billing-risk "live" call is
    possible if you want to try one. If no such server answers within
    `timeout` seconds - which is true on almost every student machine by
    default - this falls back to `offline_briefing()` instead of raising,
    because a wrapper that crashes when a live service is unavailable is
    exactly the failure mode Task 5(b)'s offline fallback exists to
    prevent.

    Do NOT point this at a hosted, account-based API. GitHub Models - a
    natural-looking free option for a GitHub-centred course - was retired
    by GitHub on 30 July 2026, mid-course-design, with no replacement free
    tier at the same URL. That is not a hypothetical risk: it is exactly
    why this practice's graded path never depends on any hosted service
    staying available, priced the same, or existing at all. See
    INSTRUCTOR_SETUP.md if you want the full local-model setup steps.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            pass
    except OSError:
        return offline_briefing(validated_context)

    # A local Ollama server answered. Calling it is intentionally left as
    # an exercise for anyone who wants to go further - see
    # INSTRUCTOR_SETUP.md for the exact request shape. It is never
    # required, and this function still returns a safe result even if you
    # never implement that call: without it, this line simply falls back.
    return offline_briefing(validated_context)


def generate_briefing(
    validated_context: dict[str, Any],
    example: str = DEFAULT_EXAMPLE,
    instruction: str = DEFAULT_INSTRUCTION,
    mode: str = "offline",
) -> str:
    """Provided - wires your functions together. You should not need to
    edit this, but read it: it shows exactly what `mode="offline"` (the
    path every test, the CI workflow and full Task 5 marks all use) and
    the optional `mode="live"` stretch each actually do.
    """
    build_prompt(instruction, validated_context, example)  # built for inspection/marking evidence
    if mode == "offline":
        return offline_briefing(validated_context)
    if mode == "live":
        prompt = build_prompt(instruction, validated_context, example)
        return try_local_model(prompt, validated_context)
    raise ValueError(f"Unknown mode {mode!r}: use 'offline' or 'live'")


def check_critical_facts(briefing_text: str, validated_context: dict[str, Any], required_facts: list[str]) -> list[str]:
    """TODO 3 (Task 5c): return the subset of `required_facts` that is
    MISSING from `briefing_text` - that is, for each name in
    `required_facts`, look up `validated_context[name]`, and if that
    value (as a string) does not appear anywhere in `briefing_text`, add
    the fact's name to the list you return.

    An empty list means every required fact was successfully checked
    against the briefing - this is the "check two critical facts" step
    Task 5(c) asks for; call this with at least two entries in
    `required_facts` when you use it in `app.py`.
    """
    raise NotImplementedError(
        "check_critical_facts: return the required_facts whose value is not present in briefing_text"
    )


def reject_unsupported_actions(briefing_text: str, validated_actions: list[str], candidate_actions: list[str]) -> list[str]:
    """TODO 4 (Task 5c): return the subset of `candidate_actions` that
    appears (as text) inside `briefing_text` but is NOT in
    `validated_actions` - i.e. an action the briefing recommends that the
    upstream rule engine and planner never validated for this case.

    An empty list means the briefing recommended nothing it should not
    have. A non-empty list is the exact mechanism Task 5(c) calls
    "reject any action not supported by the rule trace and planner" -
    in `app.py`, a non-empty result must stop that action from ever
    reaching the human officer.
    """
    raise NotImplementedError(
        "reject_unsupported_actions: return candidate_actions mentioned in briefing_text but absent from validated_actions"
    )
