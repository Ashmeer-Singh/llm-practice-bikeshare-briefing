# Reflection: LLM Practice - Bike-Share Rebalancing Briefing

## 1. Critical Facts
* **Fact 1:** `bikes_available` | **Value:** `2` | **Appears in briefing as:** `"Bikes available: 2."`
* **Fact 2:** `docks_available` | **Value:** `1` | **Appears in briefing as:** `"Docks available: 1."`

## 2. Refused Action
* **Refused Action:** `['close_station']`

* **Evidence:**
When running a test scratch script with a briefing recommending both `dispatch_rebalancing_van` and `close_station`, `reject_unsupported_actions` correctly identified and returned `['close_station']` as the unvalidated action.

* **Why unvalidated actions must be rejected:**
Only the upstream rule engine and system planner have the authority to validate action lists, which a human operator ultimately approves. The LLM is only meant to format and summarize the briefing, not decide on operational policy. If the wrapper doesn't filter out unapproved actions, an AI hallucination could trigger unintended real-world consequences—such as closing down a busy station without authorization and leaving riders stranded.

## 3. Risk and Control
* **Concrete Risk:** 
The LLM could hallucinate incorrect operational data, such as writing that there are 10 bikes available when there are actually only 2, which could cause officers to send vans or resources to the wrong location.

* **Concrete Control:** 
We use the `check_critical_facts` function to verify that essential values appear in the text. If any required fact is missing or incorrect, `app.py` sets `safe_to_show_officer` to `false` so the unsafe briefing isn't shown. Additionally, forcing the model to explicitly state "unknown" for missing data prevents it from inventing numbers.
* **Limit of Control:** 
This control only checks whether the exact required strings and numbers are present in the text. It cannot evaluate whether the broader context surrounding those numbers is fully logical or accurate.
