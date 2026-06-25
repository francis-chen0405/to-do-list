# 📝 To-Do List App (Phase 1) — Streamlit MVP

A simple, elegant, and functional To-Do List application built as a Minimum Viable Product (MVP) using Python and Streamlit. This project demonstrates how to manage application state, handle user interactions, and build responsive UIs using Streamlit.

![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)

## ✨ Features

*   ➕ **Add Tasks:** Quickly add new tasks using a clean text input interface.
*   ✅ **Track Progress:** Toggle tasks between "Active" and "Completed" states with checkboxes.
*   🗑️ **Delete Tasks:** Remove tasks you no longer need with a single click.
*   🎨 **Visual Feedback:** Completed tasks are automatically styled with a strikethrough and grayed out for clarity.
*   📊 **Two-Column Layout:** Neatly separates "Active" and "Completed" tasks side-by-side.
*   💾 **Session Persistence:** Your tasks are safely stored in the browser session, meaning they won't disappear if you interact with the app (though they will reset if you refresh the page).

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on your local machine:
*   **Python 3.7+** 
*   **pip** (Python package installer)

## 🚀 Installation & Usage

Getting the app running locally takes less than a minute!

1.  **Clone the repository** (or download the source code):
    ```bash
    git clone <your-repository-url>
    cd <your-repository-folder>
    ```

2.  **Install Streamlit:**
    Open your terminal and run:
    ```bash
    pip install streamlit
    ```

3.  **Start the application:**
    ```bash
    streamlit run app.py
    ```

4.  **Open in Browser:**
    The app will automatically open in your default web browser. If it doesn't, simply open your browser and navigate to the local URL provided in your terminal (usually `http://localhost:8501`).

## 🧠 How It Works (Under the Hood)

If you are learning Streamlit, this codebase highlights several core concepts:

*   **The Streamlit Rerun Cycle:** Streamlit reruns your entire Python script from top to bottom every time a user interacts with the UI (e.g., clicks a button or checks a box). 
*   **`st.session_state`:** Because normal Python variables reset on every rerun, this app uses `st.session_state` (a special dictionary) to persist the task list and unique IDs for the duration of the browser session.
*   **Unique Widget Keys:** Every task is assigned a unique ID upon creation. This ID is used to generate unique keys for Streamlit widgets (e.g., `complete_3`, `delete_3`). This ensures the UI correctly maps to the underlying data, even when tasks are added, deleted, or reordered.
*   **Callbacks (`on_change` / `on_click`):** Instead of relying on standard button return values, the app uses callback functions (`add_task`, `toggle_task`, `delete_task`) to update the session state *before* the UI rerenders, ensuring a smooth and bug-free experience.

## 📂 Project Structure

```text
.
├── app.py        # Main application file containing all UI and logic
└── README.md     # Project documentation (this file)
