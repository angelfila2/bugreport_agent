"""Failure and trace checks without requiring a running model."""
from pathlib import Path

import httpx
import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.errors import GraphRecursionError
from streamlit.testing.v1 import AppTest

import bugpilot.agent as agent


@pytest.mark.parametrize("error, message", [
    (httpx.ConnectError("offline"), "Cannot connect to Ollama"),
    (httpx.ReadTimeout("slow"), "too long"),
    (GraphRecursionError("limit"), "execution limit"),
    (ValueError("bad citation"), "validation"),
])
def test_actionable_failure(monkeypatch, error, message):
    def fail(*args):
        raise error
    monkeypatch.setattr(agent, "_investigate", fail)
    with pytest.raises(agent.InvestigationError, match=message):
        agent.investigate("Why?", "01_database_unavailable.log")


def test_missing_file_preserves_attempted_tool_call():
    events = []
    with pytest.raises(agent.InvestigationError, match="not found"):
        agent.investigate("Why?", "missing.log", on_event=events.append)
    assert events[0]["type"] == "tool_call"


def test_streamed_tool_events_survive_agent_failure(monkeypatch):
    class FakeAgent:
        def stream(self, *args, **kwargs):
            messages = [HumanMessage(content="Why?")]
            yield {"messages": messages[:]}
            messages.append(AIMessage(content="", tool_calls=[
                {"name": "search_notes", "args": {"query": "connection refused"}, "id": "call-1"}
            ]))
            yield {"messages": messages[:]}
            messages.append(ToolMessage(content="matching note", name="search_notes", tool_call_id="call-1"))
            yield {"messages": messages[:]}
            raise httpx.ConnectError("offline")

    monkeypatch.setattr(agent, "create_agent", lambda **kwargs: FakeAgent())
    events = []
    with pytest.raises(agent.InvestigationError, match="Cannot connect"):
        agent.investigate("Why?", "01_database_unavailable.log", events.append)
    calls = [event for event in events if event.get("call_id") == "call-1"]
    assert [event["type"] for event in calls] == ["tool_call", "tool_result"]
    assert calls[0]["input"] == {"query": "connection refused"}
    assert calls[1]["output"] == "matching note"


def test_interface_fallback_and_persistence():
    app = AppTest.from_file(Path(agent.__file__).resolve().parents[2] / "app.py").run()
    app.selectbox[0].select("03_insufficient_evidence.log")
    app.button[0].click().run()
    assert not app.exception
    assert app.success
    run = app.session_state["last_run"]
    assert run["report"]["likely_cause"] is None
    assert [event["type"] for event in run["events"]] == ["tool_call", "tool_result", "status"]
    app.run()
    assert app.success
    assert not app.exception


def test_interface_connection_error(monkeypatch):
    def fail(question, incident, on_event=None):
        on_event({"type": "status", "message": "Starting investigation"})
        raise agent.InvestigationError("Cannot connect to Ollama. Open Ollama and retry.")
    monkeypatch.setattr(agent, "investigate", fail)
    app = AppTest.from_file(Path(agent.__file__).resolve().parents[2] / "app.py").run()
    app.button[0].click().run()
    assert not app.exception
    assert "Cannot connect to Ollama" in app.error[0].value
    assert app.session_state["last_run"]["events"]
    assert app.session_state["last_run"]["report"] is None

