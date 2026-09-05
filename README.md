# LLM Practice: Bike-Share Rebalancing Briefing

Ungraded practice for BCS2143 / BIT3203, built to train the exact skills the
**Final Assessment's Task 5 (GenAI, LLM API use and ethical assurance, 10
marks)** will check: construct a grounded prompt from an instruction, a
validated context and one example; generate a briefing through a supplied
wrapper; check that briefing against critical facts; and reject any action
it recommends that upstream logic never validated.

The scenario (bike-share station rebalancing) and the data are different
from the Final Assessment's own GreenSpace case on purpose - so nobody can
copy an answer across. The wrapper's shape, the offline-first design, and
the checks it must pass are deliberately the same.

**Nothing in this practice costs money, needs an account, or needs the
internet.** Every test and the CI workflow use `mode="offline"` only - a
pure Python function with no network call at all. See "Why offline is the
graded path" below before you assume you need to sign up for anything.

## What you will do

1. Fork this repository and clone your fork.
2. Complete the four `TODO`s in `src/llm_wrapper.py` (see the table below).
3. Run `pytest -v` locally until all checks pass.
4. Push your branch to your fork and open a pull request back to this
   repository. See `HOW_TO_SUBMIT.md` for the exact steps and what happens
   next (a maintainer-approved GitHub Actions run, exactly like the Final
   Assessment's own CI).

## Recommended self-study order

1. Read the theory slides to understand the whole wrapper pipeline.
2. Use the student guide for setup, reasoning prompts and troubleshooting.
3. Complete the four `TODO`s in `src/llm_wrapper.py` from top to bottom.
4. Re-run `pytest -v` after each completed function.
5. Run the full pipeline and complete `REFLECTION.md` using the saved
   `outputs/result.json` and `outputs/briefing.txt`.
6. Use the teaching slides as a checkpoint and self-test before submitting.

| TODO | Mirrors Final Assessment | What to do |
|---|---|---|
| `build_prompt` | Task 5(a) | Combine instruction + validated context + one example into one labelled prompt string |
| `offline_briefing` | Task 5(a)-(b) | Deterministic, offline-only briefing built from validated context, stating unknown facts honestly |
| `check_critical_facts` | Task 5(c) | Detect whether a briefing actually contains required facts |
| `reject_unsupported_actions` | Task 5(c) | Catch a briefing that recommends an action nobody validated |

## Install

```text
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```text
python -m src.app --case data/station_case.json --trace data/decision_trace.json --output outputs/result.json
```

## Check your work

```text
pytest -v
```

Every failing test tells you what is wrong and which Task 5 sub-part it
maps to. Do not edit `tests/test_llm_wrapper.py` - only `src/llm_wrapper.py`
and, once your pipeline runs, `REFLECTION.md`.

When the pipeline runs successfully, `outputs/result.json` and
`outputs/briefing.txt` are produced, in exactly the shape the Final
Assessment's own `outputs/result.json` and `outputs/briefing.txt` are
required to appear. Use them to complete `REFLECTION.md`.

## Why offline is the graded path

The Final Assessment paper says plainly: *"No paid API is required. The
offline LLM fixture is valid for development and marking."* This is not a
lesser option - it is the whole point of a wrapper you can trust: a
deterministic, inspectable function beats a hosted call you cannot fully
control or guarantee will still exist tomorrow.

That last part is not hypothetical. GitHub Models - GitHub's own free
hosted LLM API, and the option a GitHub-centred course like this one might
naturally have pointed you to - was retired on 30 July 2026, with no
replacement free tier at the same URL. Building your Task 5 work so it
never depends on a specific hosted service staying free, or staying online
at all, is exactly the engineering judgement this task rewards.

If you want to see a genuine live call anyway, `src/llm_wrapper.py`'s
provided `try_local_model()` function supports a **fully local** model
through [Ollama](https://ollama.com) - no account, no API key, no billing
risk, because nothing leaves your machine. It is entirely optional, not
covered by any test, and not required for any Task 5 mark.

## Why this matters for the Final Assessment

Task 5 is worth fewer marks than Task 4, but it is the task most students
under-practice, because "call an LLM" sounds like it needs an account and a
credit card. It does not. The pattern you practice here - a grounded
prompt, a deterministic offline fallback, checking the output against
facts you already know, and refusing an action nobody validated - is
exactly what the marking rubric rewards, and it is free, every time, for
everyone.
