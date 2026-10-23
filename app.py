"""Launch with: python -m streamlit run app.py."""
import logging
import streamlit as st
from bugpilot.agent import InvestigationError, investigate
from bugpilot.config import INCIDENTS_DIR
from bugpilot.tools import read_log

st.set_page_config(page_title="BugPilot", page_icon="🐛")
st.title("🐛 BugPilot")
st.caption("Investigate an incident using logs and troubleshooting notes.")
incidents = sorted(path.name for path in INCIDENTS_DIR.glob("*.log"))
if not incidents:
    st.warning("No logs found in data/incidents. Add a .log file to begin.")
    st.stop()
incident = st.selectbox("Sample incident", incidents)
question = st.text_area("What happened?", "Why did this request fail?")
with st.expander("Inspect the log"):
    try:
        st.code(read_log(incident), language="text")
    except (OSError, ValueError):
        st.error("This log could not be read. Refresh or select another incident.")
        st.stop()


def show_event(event: dict) -> None:
    """Show observable tool activity and status, not private reasoning."""
    if event["type"] == "tool_call":
        st.markdown(f"**Tool call: `{event['name']}`** ({event['stage']})")
        if event.get("call_id"):
            st.caption(f"Call ID: {event['call_id']}")
        st.json(event["input"])
    elif event["type"] == "tool_result":
        st.markdown(f"**Tool result: `{event['name']}`** ({event['stage']})")
        if event.get("call_id"):
            st.caption(f"Call ID: {event['call_id']}")
        st.code(str(event["output"]), language="text")
    else:
        st.caption(event["message"])


if st.button("Investigate", disabled=not question.strip()):
    st.session_state["last_run"] = {
        "incident": incident, "question": question, "events": [],
        "report": None, "error": None,
    }
    run = st.session_state["last_run"]
    st.caption(f"Investigation: {incident}")
    trace = st.expander("Investigation trace", expanded=True)

    def record_event(event: dict) -> None:
        run["events"].append(event)
        with trace:
            show_event(event)

    try:
        with st.spinner("Investigating..."):
            report = investigate(question, incident, on_event=record_event)
        run["report"] = report.model_dump()
    except InvestigationError as exc:
        run["error"] = str(exc)
    except Exception:
        logging.exception("Unexpected investigation failure")
        run["error"] = "An unexpected error occurred. Check the terminal for details and retry."
else:
    run = st.session_state.get("last_run")
    if run:
        st.caption(f"Previous investigation: {run['incident']} — {run['question']}")
        with st.expander("Investigation trace"):
            for event in run["events"]:
                show_event(event)

if run:
    if run["error"]:
        st.error(run["error"])
    elif run["report"] is not None:
        st.success("Report generated and citation checks passed.")
        st.json(run["report"])
