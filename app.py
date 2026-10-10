
import streamlit as st

from agent import run_agent
from database import initialize_database, get_all_invoices

st.set_page_config(
    page_title="AI Office Worker",
    page_icon="🤖",
    layout="wide",
)

initialize_database()

if "task_runs" not in st.session_state:
    st.session_state.task_runs = []

st.title("🤖 AI Office Worker")
st.caption("Autonomous invoice processing, execution logs, and verification")

st.info(
    "Prototype mode: rule-based planning with local PDF and SQLite tools. "
    "No external AI API is required."
)

st.subheader("Give your agent a task")

task = st.text_area(
    "Describe the outcome you want",
    placeholder=(
        "Find the latest invoice and save its amount and due date."
    ),
)

if st.button("Start Task", type="primary"):
    if not task.strip():
        st.warning("Please enter a task.")
    else:
        with st.spinner("Agent is executing the task..."):
            try:
                result = run_agent(task)
                st.session_state.task_runs.insert(0, {
                    "task": task.strip(),
                    "result": result,
                })
            except Exception as exc:
                st.session_state.task_runs.insert(0, {
                    "task": task.strip(),
                    "result": {
                        "status": "failed",
                        "logs": [
                            f"Unexpected error: {type(exc).__name__}: {exc}"
                        ],
                        "results": [],
                    },
                })

for run in st.session_state.task_runs:
    with st.container(border=True):
        st.subheader("Execution report")
        st.write("**Task:**", run["task"])

        result = run["result"]
        status = result["status"]

        if status == "completed":
            st.success("Task completed and saved records verified.")
        elif status == "extracted":
            st.success("Extraction completed; no database writes requested.")
        elif status == "needs_review":
            st.warning("Task incomplete. Review the execution log.")
        elif status == "unsupported":
            st.warning("This task is outside the current prototype's scope.")
        else:
            st.error("Task failed. Review the execution log.")

        with st.expander("View execution trace", expanded=True):
            for index, message in enumerate(result["logs"], start=1):
                st.write(f"{index}. {message}")

        if result["results"]:
            st.write("**Extracted invoice information**")
            st.dataframe(
                result["results"],
                use_container_width=True,
                hide_index=True,
            )

st.divider()
st.subheader("📋 Saved Invoice Records")

records = get_all_invoices()

if records:
    st.dataframe(
    records,
    width="stretch",
    hide_index=True,
)
else:
    st.info("No invoices have been saved yet.")
