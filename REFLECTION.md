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
The LLM could hallucinate incorrect operational data, such as writing that there are 10 bikes available when there are actually only 2. An officer might then skip a rebalancing van that is really needed, or send resources to the wrong place, because of a made-up number.

* **Concrete Control:**
We use the `check_critical_facts` function to verify that each required value appears in the briefing. If one is missing, `app.py` sets `safe_to_show_officer` to `false` so the briefing isn't shown to the officer. In addition, the briefing states that facts such as `current_temperature_c` are "unknown" instead of inventing a value, which reduces the risk of made-up numbers.

* **Limit of Control:**
The check only confirms that the correct values appear. A briefing that says "Bikes available: 2" and also claims "10 bikes are free" would still pass. A stronger control would compare every number in the text against the validated context.
