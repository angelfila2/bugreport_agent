"""Launch with: streamlit run app.py (after installing the project)."""
import streamlit as st

from bugpilot.agent import investigate
from bugpilot.config import INCIDENTS_DIR
from bugpilot.tools import read_log

st.set_page_config(page_title="BugPilot", page_icon="🐛")
st.title("🐛 BugPilot")
st.caption("Investigate an incident using logs and troubleshooting notes.")
incident = st.selectbox("Sample incident", sorted(p.name for p in INCIDENTS_DIR.glob("*.log")))
question = st.text_area("What happened?", "Why did this request fail?")
with st.expander("Inspect the log"):
    st.code(read_log(incident), language="text")
if st.button("Investigate", disabled=not question.strip()):
    try:
        with st.spinner("Investigating..."):
            report = investigate(question, incident)
        st.json(report.model_dump())
    except NotImplementedError as exc:
        st.info(str(exc))
    except Exception:
        st.error("Investigation failed. Check your configuration and local terminal output.")
