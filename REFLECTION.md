# Reflection (Task 5c/5d practice)

Fill this in after `python -m src.app` runs successfully and
`outputs/result.json` shows `"safe_to_show_officer": true`.

## Two critical facts you checked

Open `outputs/result.json`. `required_facts_checked` lists the two facts
`check_critical_facts()` verified against your briefing.

1. Fact: ____________________ Value in the data: ____________________
   Where does it appear, worded or numbered, in your briefing text?

2. Fact: ____________________ Value in the data: ____________________
   Where does it appear, worded or numbered, in your briefing text?

## The action your wrapper correctly refused

`candidate_actions_checked` includes one action, `close_station`, that is
deliberately **not** in `decision_trace.json`'s `validated_actions`. Confirm
`reject_unsupported_actions()` catches it if it ever appeared in a
briefing (you can test this yourself by temporarily editing a briefing
string in a scratch script - not in `src/llm_wrapper.py` itself).

Explain in your own words: why must a wrapper reject an action a
human officer never asked the system to validate, even if the action
sounds reasonable on its face?

## One bias, hallucination, privacy or responsible-use risk

State one specific risk this kind of wrapper could pose if it were used
for real, and one specific control (already in this wrapper, or one you
would add) that reduces it. Not "the AI could be wrong" - name a concrete
failure and a concrete control, the way `offline_briefing()`'s explicit
"unknown" handling is a concrete control for the specific risk of a
confident-sounding invented number.
