# BugPilot

**An AI incident investigation MVP built with Python, LangChain, Ollama, and Streamlit.**

BugPilot helps developers investigate failed API requests from local logs. It produces structured reports with cited evidence, suggested next steps, and missing diagnostic information.

## Features

- Investigates logs with a local Llama model and troubleshooting-note search.
- Returns structured reports containing a summary, likely cause, evidence, suggested fixes, and missing information.
- Checks evidence filenames, line numbers, and excerpts against the original log.
- Displays tool inputs, tool results, and execution status in an expandable trace.
- Preserves partial traces when an investigation fails.
- Shows actionable messages for Ollama connection failures, timeouts, missing models or files, execution limits, and invalid reports.
- Returns an explicit unknown-cause report for the supported status-only HTTP error format.

## Quick start

Requires Python 3.10+ compatible with the dependencies, [Ollama](https://ollama.com/download), and sufficient memory for `llama3.2`.

Run from the project directory in Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
ollama pull llama3.2
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Keep Ollama running. If it is not running, start the Ollama application or run `ollama serve` in a separate terminal. No cloud API key is required for the default local setup.

Select an incident, enter a question, and click **Investigate**. Expand **Investigation trace** to inspect tool calls and their results.

### Add an incident

Place a UTF-8 `.log` file in `data/incidents/` and refresh the interface. Add troubleshooting guidance as Markdown files in `data/notes/`.

Logs should include timestamps, severity, request IDs, and error details. The deterministic status-only fallback recognizes this specific format:

```text
2026-10-22T10:10:02Z ERROR request_id=req-301 POST /users status=500
```

Other logs use the model-driven path. This MVP does not upload files or connect to live services.

### Terminal usage

```powershell
.\.venv\Scripts\python.exe -c "from bugpilot.agent import investigate; report = investigate('Why did creating a user fail?', '02_misleading_warning.log'); print(report.model_dump_json(indent=2))"
```

Check the model connection independently:

```powershell
.\.venv\Scripts\python.exe try_model.py
```

The model tag is currently `llama3.2` in `src/bugpilot/agent.py` and `try_model.py`. Update both and download the matching model when changing it.

## Architecture

1. **Precheck:** read the selected log and apply the narrowly defined status-only uncertainty rule where applicable.
2. **Investigate:** a LangChain agent calls `read_log` and `search_notes`. Observable tool events are streamed to the interface.
3. **Format:** a separate model call creates a `DebugReport` directly from the original log. It does not consume the investigation draft, avoiding propagation of unsupported draft claims.
4. **Validate:** Pydantic checks the schema; application checks verify citations and reject some unsupported file references. One correction attempt is allowed when validation fails.

The investigation trace helps inspect agent behavior. The final report is generated independently from the log; the investigation is not an input to report generation. Status-only fallback reports bypass the model entirely.

## Report format

| Field | Meaning |
| --- | --- |
| `summary` | Brief description of the incident |
| `likely_cause` | Observed immediate failure, or `null` when unknown |
| `evidence` | Source filename, line number, and original log excerpt |
| `suggested_fixes` | Proposed checks or corrective steps |
| `missing_information` | Additional diagnostic evidence needed |

## Verification

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The automated suite covers log access, keyword retrieval, failure messages, tool events, and Streamlit interactions, including report persistence and error display. It does not require a running model.

Three sample scenarios have also been checked manually: database connection refusal, a misleading warning beside a duplicate-email failure, and insufficient diagnostic evidence. See [the evaluation checklist](docs/evaluation.md) for expectations and limitations.

## Project structure

```text
app.py                         Streamlit interface and trace display
try_model.py                   Local model connection check
pyproject.toml                 Package metadata and dependencies
src/bugpilot/
  agent.py                     Investigation, events, reports, failure handling
  config.py                    Local data paths
  models.py                    Report and evidence schemas
  tools/logs.py                Numbered incident-log reader
  tools/notes.py               Keyword-based troubleshooting search
data/incidents/                Sample logs and additional local incidents
data/notes/                    Troubleshooting guidance
tests/                         Automated tool, failure, and interface checks
docs/evaluation.md             Agent behavior acceptance criteria
```

## MVP limitations

- Model outputs can contain unsupported claims; schema and citation checks do not prove diagnostic accuracy.
- Investigation drafts can include irrelevant suggestions even when the final report is grounded.
- Keyword retrieval may return unrelated guidance for broad queries.
- The status-only fallback is format-specific and does not infer the user's target request across arbitrary logs.
- The interface timeout applies to model HTTP operations, not a guaranteed total wall-clock deadline.
- BugPilot reads local logs and recommends next steps; it does not apply fixes or monitor production systems.
