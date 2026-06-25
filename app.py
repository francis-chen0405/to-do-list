"""
To-Do List App (Phase 2) — Streamlit MVP
=========================================

New in Phase 2:
    - Due dates
    - Priority levels (High / Medium / Low)
    - Tags / categories
    - Per-task notes

How to install and run:
    1. Open a terminal in this folder.
    2. Install Streamlit (once):
           pip install streamlit
    3. Start the app:
           streamlit run app.py
    4. Your browser will open automatically. If not, visit the URL shown in the terminal.
"""

import streamlit as st
from datetime import date

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PRIORITIES = ["🔴 High", "🟡 Medium", "🟢 Low"]
PRIORITY_ORDER = {"🔴 High": 0, "🟡 Medium": 1, "🟢 Low": 2}

# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------

def init_session_state():
    if "tasks" not in st.session_state:
        st.session_state.tasks = []
    if "next_id" not in st.session_state:
        st.session_state.next_id = 1
    if "expand_task_id" not in st.session_state:
        st.session_state.expand_task_id = None


def add_task(text, priority, due_date, tags, notes):
    if not text.strip():
        return
    st.session_state.tasks.append({
        "id": st.session_state.next_id,
        "text": text.strip(),
        "completed": False,
        "priority": priority,
        "due_date": due_date,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "notes": notes.strip(),
    })
    st.session_state.next_id += 1


def toggle_task(task_id):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            break


def delete_task(task_id):
    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task_id]


def update_task(task_id, field, value):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task[field] = value
            break


# ---------------------------------------------------------------------------
# Render helpers
# ---------------------------------------------------------------------------

def due_date_label(due_date):
    if due_date is None:
        return ""
    today = date.today()
    delta = (due_date - today).days
    if delta < 0:
        return f"<span style='color:#e05252'>⚠️ Overdue ({due_date})</span>"
    elif delta == 0:
        return f"<span style='color:#e09a52'>📅 Due today</span>"
    elif delta <= 3:
        return f"<span style='color:#e0c452'>📅 Due {due_date}</span>"
    else:
        return f"<span style='color:#888'>📅 {due_date}</span>"


def tags_label(tags):
    if not tags:
        return ""
    return " ".join(f"<span style='background:#2a4a6b;padding:1px 7px;border-radius:10px;font-size:0.8em'>{t}</span>" for t in tags)


def render_task_row(task):
    is_done = task["completed"]
    text_style = "color:#888;text-decoration:line-through" if is_done else "font-weight:500"

    with st.container():
        cols = st.columns([0.05, 0.55, 0.18, 0.14, 0.08])

        with cols[0]:
            st.checkbox(
                "",
                value=is_done,
                key=f"complete_{task['id']}",
                on_change=toggle_task,
                args=(task["id"],),
                label_visibility="collapsed",
            )

        with cols[1]:
            label_parts = [f"<span style='{text_style}'>{task['text']}</span>"]
            due = due_date_label(task.get("due_date"))
            if due:
                label_parts.append(due)
            tags = tags_label(task.get("tags", []))
            if tags:
                label_parts.append(tags)
            if task.get("notes"):
                label_parts.append(f"<span style='color:#aaa;font-size:0.82em'>📝 {task['notes'][:60]}{'…' if len(task['notes']) > 60 else ''}</span>")
            st.markdown(" &nbsp;".join(label_parts), unsafe_allow_html=True)

        with cols[2]:
            st.markdown(f"<div style='padding-top:4px'>{task.get('priority','🟢 Low')}</div>", unsafe_allow_html=True)

        with cols[3]:
            # Inline edit expander toggle
            expand_key = f"expand_{task['id']}"
            if st.button("✏️ Edit", key=expand_key):
                if st.session_state.expand_task_id == task["id"]:
                    st.session_state.expand_task_id = None
                else:
                    st.session_state.expand_task_id = task["id"]

        with cols[4]:
            st.button("🗑️", key=f"delete_{task['id']}", on_click=delete_task, args=(task["id"],))

    # Inline edit panel
    if st.session_state.expand_task_id == task["id"]:
        with st.container():
            st.markdown("---")
            e1, e2, e3 = st.columns([2, 1, 1])
            with e1:
                new_text = st.text_input("Task text", value=task["text"], key=f"edit_text_{task['id']}")
                new_notes = st.text_area("Notes", value=task.get("notes", ""), key=f"edit_notes_{task['id']}", height=80)
                new_tags = st.text_input("Tags (comma-separated)", value=", ".join(task.get("tags", [])), key=f"edit_tags_{task['id']}")
            with e2:
                new_priority = st.selectbox("Priority", PRIORITIES, index=PRIORITIES.index(task.get("priority", "🟢 Low")), key=f"edit_pri_{task['id']}")
            with e3:
                new_due = st.date_input("Due date", value=task.get("due_date"), key=f"edit_due_{task['id']}")
            if st.button("Save changes", key=f"save_{task['id']}"):
                update_task(task["id"], "text", new_text.strip())
                update_task(task["id"], "notes", new_notes.strip())
                update_task(task["id"], "tags", [t.strip() for t in new_tags.split(",") if t.strip()])
                update_task(task["id"], "priority", new_priority)
                update_task(task["id"], "due_date", new_due)
                st.session_state.expand_task_id = None
                st.rerun()
            st.markdown("---")


# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------

st.set_page_config(page_title="To-Do List", layout="wide")
init_session_state()

st.title("📋 To-Do List")
st.caption("Phase 2 — Due dates, priorities, tags, and notes.")

# ---------------------------------------------------------------------------
# Add a task
# ---------------------------------------------------------------------------

with st.expander("➕ Add a new task", expanded=True):
    a1, a2, a3 = st.columns([3, 1, 1])
    with a1:
        new_text = st.text_input("Task description", placeholder="What do you need to do?", key="new_text")
        new_notes = st.text_area("Notes (optional)", placeholder="Any extra details...", key="new_notes", height=70)
        new_tags = st.text_input("Tags (comma-separated, optional)", placeholder="e.g. school, debate, urgent", key="new_tags")
    with a2:
        new_priority = st.selectbox("Priority", PRIORITIES, index=1, key="new_priority")
    with a3:
        new_due = st.date_input("Due date (optional)", value=None, key="new_due")

    if st.button("Add Task", use_container_width=True):
        add_task(new_text, new_priority, new_due, new_tags, new_notes)
        st.rerun()

st.divider()

# ---------------------------------------------------------------------------
# Filter + sort bar
# ---------------------------------------------------------------------------

filter_cols = st.columns([2, 2, 1])
with filter_cols[0]:
    all_tags = sorted({tag for t in st.session_state.tasks for tag in t.get("tags", [])})
    tag_filter = st.multiselect("Filter by tag", all_tags, key="tag_filter")
with filter_cols[1]:
    pri_filter = st.multiselect("Filter by priority", PRIORITIES, key="pri_filter")
with filter_cols[2]:
    sort_by = st.selectbox("Sort by", ["Added order", "Priority", "Due date"], key="sort_by")

def apply_filters(tasks):
    if tag_filter:
        tasks = [t for t in tasks if any(tag in t.get("tags", []) for tag in tag_filter)]
    if pri_filter:
        tasks = [t for t in tasks if t.get("priority") in pri_filter]
    if sort_by == "Priority":
        tasks = sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.get("priority", "🟢 Low"), 2))
    elif sort_by == "Due date":
        tasks = sorted(tasks, key=lambda t: t.get("due_date") or date.max)
    return tasks

st.divider()

# ---------------------------------------------------------------------------
# Task lists
# ---------------------------------------------------------------------------

active_tasks = apply_filters([t for t in st.session_state.tasks if not t["completed"]])
completed_tasks = apply_filters([t for t in st.session_state.tasks if t["completed"]])

if not st.session_state.tasks:
    st.info("No tasks yet — add one above!")
else:
    col_active, col_completed = st.columns(2)

    with col_active:
        st.subheader(f"Active ({len(active_tasks)})")
        if not active_tasks:
            st.caption("No active tasks.")
        else:
            for task in active_tasks:
                render_task_row(task)

    with col_completed:
        st.subheader(f"Completed ({len(completed_tasks)})")
        if not completed_tasks:
            st.caption("No completed tasks.")
        else:
            for task in completed_tasks:
                render_task_row(task)