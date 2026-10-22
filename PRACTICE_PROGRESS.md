# Practice stopping point

## Thursday, 22 October 2026 — two-hour session

Today's objective: run one incident end to end and return a validated `DebugReport`.

Stop the guided practice once this objective is demonstrated. Tell the user that today's objective is complete and leave Friday's tasks for tomorrow, unless the user explicitly chooses to continue.

Status: COMPLETE, confirmed by the user's successful terminal output on 22 October 2026. Stop Thursday's guided practice here.

Completed:
- Local Llama model responds successfully through Ollama.
- Agent reads an incident log and searches troubleshooting notes.
- Keyword retrieval and prompting were refined to reduce unrelated incident claims.
- A separate structured-output model call formats the investigation into a validated `DebugReport`.
- The database-unavailable sample returned a report citing the exact log excerpt at line 2, with relevant service/host/port checks.
- `likely_cause` was null, appropriately leaving the underlying reason for connection refusal unconfirmed.

Scope of confirmation: one successful sample, not a reliability evaluation across all incidents. Friday's tasks remain outstanding.

## Friday, 23 October 2026 — two-hour session

- Evaluate all three incidents, including misleading and insufficient evidence.
- Add failure handling and a visible tool trace.
- Improve the Streamlit report display.
- Finish portfolio documentation/demo and rehearse explaining design choices.

Do not begin these Friday tasks automatically during Thursday's guided practice.
