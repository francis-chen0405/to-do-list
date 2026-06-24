"""
To-Do List App (Phase 1) — Streamlit MVP
=========================================

How to install and run:
    1. Open a terminal in this folder.
    2. Install Streamlit (once):
           pip install streamlit
    3. Start the app:
           streamlit run app.py
    4. Your browser will open automatically. If not, visit the URL shown in the terminal.

How it works:
    Streamlit reruns this entire script every time you click a button or checkbox.
    Normal Python variables would reset on each rerun, so we store tasks in
    st.session_state — a special dictionary that persists for your browser session.
"""

import streamlit as st


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------

def init_session_state():
    """
    Initialize session state on first load.

    The guard `if "tasks" not in st.session_state` ensures this block runs only
    once per browser tab. On every later rerun, the existing task list is kept.
    """
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    if "next_id" not in st.session_state:
        # Each task gets a unique id used for widget keys (see render_task_row).
        st.session_state.next_id = 1
    if "new_task_text" not in st.session_state:
        st.session_state.new_task_text = ""


def add_task():
    """Append a new task from the text input and clear the input."""
    text = st.session_state.new_task_text.strip()
    if not text:
        return

    st.session_state.tasks.append(
        {
            "id": st.session_state.next_id,
            "text": text,
            "completed": False,
        }
    )
    st.session_state.next_id += 1
    st.session_state.new_task_text = ""


def toggle_task(task_id):
    """Flip the completed flag for the task with the given id."""
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break


def delete_task(task_id):
    """Remove the task with the given id from the list."""
    st.session_state.tasks = [
        task for task in st.session_state.tasks if task["id"] != task_id
    ]


def render_task_row(task, completed_style=False):
    """
    Render one task row: checkbox, label, delete button.

    Each widget needs a unique `key` string so Streamlit can tell widgets apart
    across reruns. We use the task id (e.g. "complete_3", "delete_3") so keys
    stay stable even when the list order changes.

    `on_change` / `on_click` callbacks update session state before the next rerun,
    so the UI always reflects the stored task data.
    """
    cols = st.columns([0.08, 0.77, 0.15])

    with cols[0]:
        st.checkbox(
            "",
            value=task["completed"],
            key=f"complete_{task['id']}",
            on_change=toggle_task,
            args=(task["id"],),
            label_visibility="collapsed",
        )

    with cols[1]:
        if completed_style:
            st.markdown(
                f"<span style='color:#888;text-decoration:line-through'>"
                f"{task['text']}</span>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(task["text"])

    with cols[2]:
        st.button(
            "Delete",
            key=f"delete_{task['id']}",
            on_click=delete_task,
            args=(task["id"],),
        )


# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------

st.set_page_config(page_title="To-Do List", layout="wide")

init_session_state()

st.title("To-Do List")
st.caption("Phase 1 — Add, complete, and delete tasks. Data lives in your browser session.")

# ---------------------------------------------------------------------------
# Add a task
# ---------------------------------------------------------------------------

st.subheader("Add a task")

add_cols = st.columns([4, 1])
with add_cols[0]:
    # key="new_task_text" binds this input to st.session_state.new_task_text
    st.text_input(
        "Task description",
        placeholder="What do you need to do?",
        key="new_task_text",
        label_visibility="collapsed",
    )
with add_cols[1]:
    st.button("Add", on_click=add_task, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# View tasks — split into Active and Completed columns
# ---------------------------------------------------------------------------

active_tasks = [t for t in st.session_state.tasks if not t["completed"]]
completed_tasks = [t for t in st.session_state.tasks if t["completed"]]

if not st.session_state.tasks:
    st.info("No tasks yet. Add one above!")
else:
    col_active, col_completed = st.columns(2)

    with col_active:
        st.subheader("Active")
        if not active_tasks:
            st.caption("No active tasks.")
        else:
            for task in active_tasks:
                render_task_row(task, completed_style=False)

    with col_completed:
        st.subheader("Completed")
        if not completed_tasks:
            st.caption("No completed tasks.")
        else:
            for task in completed_tasks:
                render_task_row(task, completed_style=True)
