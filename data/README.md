# Practice case: bike-share rebalancing briefing

`station_case.json` is the validated context for one bike-share station,
already checked and cleaned - this practice is not about auditing data
(that is Task 4's job), it is about safely turning a validated result into
a short, grounded briefing for a human operations officer.

| Field | Meaning |
|---|---|
| `case_id` | Identifier for this briefing case. Not a fact to report. |
| `station_id`, `zone`, `period` | Where and when this observation was taken. |
| `bikes_available`, `docks_available`, `dock_capacity` | The core station state: how many bikes can be picked up, how many free docks exist to return one. |
| `demand_trend` | `rising`, `falling` or `stable` - short-term direction, not a prediction. |
| `last_rebalanced_hours_ago` | How long since a van last visited this station. |
| `current_temperature_c` | **Deliberately `null`.** The sensor feed for this field was unavailable when this case was captured. Your briefing must say this is unknown, not guess a plausible number. |
| `staff_on_shift` | How many rebalancing staff are currently on duty campus-wide. |

`decision_trace.json` is the already-validated output of the upstream rule
engine and planner (the Topics 5-6 half of this course) for this same case:

| Field | Meaning |
|---|---|
| `decision` | The one policy conclusion already reached - `rebalance_now`. |
| `triggered_rules` | Which rules fired to reach that decision. |
| `validated_actions` | The **only** actions your briefing is allowed to recommend. |
| `unknown_facts` | Fields the upstream system also could not confirm - currently just `current_temperature_c`, matching the case file. |

This is shared, ungraded practice data - everyone works from the same two
files. The deliberately missing `current_temperature_c` and the
deliberately narrow `validated_actions` list are not oversights: they are
exactly the two traps Task 5 marks you on catching - reporting an unknown
fact honestly, and refusing to let a briefing recommend an action nobody
validated.
