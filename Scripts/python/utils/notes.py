
import streamlit as st
from datetime import datetime

def notes_panel(tab_name, current_inputs):
    """
    Notes panel for any tab.
    Saves notes + snapshot of current_inputs into session_state.notes[tab_name]
    """

    st.subheader("📝 Notes")

    # Ensure tab key exists
    if tab_name not in st.session_state.notes:
        st.session_state.notes[tab_name] = []

    with st.expander("➕ Add / Edit Notes", expanded=st.session_state.auto_expand_notes):

        note_text = st.text_area(
            "Write your note here:",
            value=st.session_state.note_input,
            height=120,
            placeholder="Observations, interpretations, questions..."
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("💾 Save Note"):
                entry = {
                    "timestamp": datetime.now(),
                    "notes": note_text,
                    "inputs": current_inputs.copy()
                }

                # Edit existing note
                if st.session_state.edit_mode.get("active"):
                    idx = st.session_state.edit_mode["index"]
                    st.session_state.notes[tab_name][idx] = entry
                    st.session_state.edit_mode = {"active": False}
                else:
                    st.session_state.notes[tab_name].append(entry)

                st.session_state.note_input = ""
                st.session_state.auto_expand_notes = False
                st.session_state.toast_message = f"✅ Note saved to {tab_name}"
                st.rerun()

        with col2:
            if st.button("🧹 Clear"):
                st.session_state.note_input = ""
                st.rerun()

def _format_list_readable(items):
    """Convert list into human-readable string."""
    if not items:
        return ""
    if len(items) == 1:
        return str(items[0])
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(map(str, items[:-1])) + f" and {items[-1]}"


def format_note_display(note, tab_name):
    timestamp = note.get("timestamp")
    timestamp_str = (
        timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(timestamp, datetime)
        else str(timestamp)
    )

    inputs = note.get("inputs", {})
    content = note.get("notes", "")

    # Fields we NEVER show to the user
    hidden_fields = {"map_center", "map_zoom_level"}

    formatted_inputs = []

    for key, value in inputs.items():
        if key in hidden_fields or value is None:
            continue

        # Clean label formatting
        label = key.replace("_", " ").title()

        # Format lists nicely
        if isinstance(value, list):
            value = _format_list_readable(value)

        formatted_inputs.append(f"{label}: {value}")

    snapshot_text = " |  ".join(formatted_inputs) if formatted_inputs else "N/A"

    formatted = (
        f"🕒 {timestamp_str}\n"
        f"📍 Source: {tab_name}\n\n"
        f"🔧 Snapshot Inputs:\n"
        f"{snapshot_text}\n\n"
        f"🗒️ Notes:\n"
        f"{content}\n\n"
        f"{'-'*60}\n"
    )

    return formatted

# Helper function to save notes
def save_note(tab):
    note = st.session_state.get("current_note", "").strip()
    if note:
        st.session_state.notes[tab].append(
            {"timestamp": datetime.now(), "note": note}
        )
        st.session_state.current_note = ""
    

