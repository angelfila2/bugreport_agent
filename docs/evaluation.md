# Incident investigation evaluation

Run each scenario through BugPilot and inspect the final report alongside the original log and tool trace.

| Scenario | Expected behavior |
| --- | --- |
| `01_database_unavailable.log` | Cite line 2; identify connection refusal without asserting an unobserved service or network cause. Recommend checking service availability and endpoint configuration. |
| `02_misleading_warning.log` | Cite line 4; associate req-201 with the duplicate-email constraint. Do not blame the cache warning on successful req-200 or infer that the constraint is misconfigured. |
| `03_insufficient_evidence.log` | Return an unknown cause and request correlated error details. The format-specific Python fallback handles this case without calling the model. |

## Acceptance criteria

- Evidence references the selected file and an existing line.
- Stored evidence excerpts match the complete original log line.
- Summary, cause, and recommendations follow the evidence.
- No invented source files, functions, or code locations appear.
- Missing information is absent from the supplied log and relevant to diagnosis.
- Tool calls and results appear in the trace; partial traces remain visible after failures.

## Failure scenarios

Verify useful messages for an unavailable Ollama server, model timeout, missing model, missing log, invalid report, and execution-limit failure. Automated tests simulate several of these conditions without requiring a model.

## Scope of evidence

The three sample scenarios have each produced acceptable reports during manual checks. This is a small regression set, not a reliability benchmark. Automated checks cover software behavior rather than semantic accuracy. Review investigation drafts separately from final reports: the formatter uses the original log independently, and draft reasoning can remain inaccurate.
