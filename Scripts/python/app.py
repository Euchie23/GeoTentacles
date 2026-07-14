import sys
import streamlit as st
from pathlib import Path
import time

# Add the current folder (scripts/python) and its subfolders to Python path
base_path = Path(__file__).parent
sys.path.append(str(base_path))
sys.path.append(str(base_path / "modules"))
sys.path.append(str(base_path / "utils"))

st.set_page_config(layout="wide")

from modules.overview import render as overview_render
from modules.interpolation import render as interpolation_render
from modules.pollution_prediction import render as prediction_render
from modules.marine_health_index import render as mci_render
from modules.covid_impact import render as covid_render
from modules.logbook import render as logbook_render


# ============================================================
# 🔹 Session State Initialization (GLOBAL, ONCE)
# ============================================================

PAGES = {
    "Overview": overview_render,
    "Seafloor Signals": interpolation_render,
    "Toxic Tide Mapping": prediction_render,
    "EcoPulse Index": mci_render,
    "Disruption Dynamics": covid_render,
    "Logbook": logbook_render,
}

NOTE_TABS = [k for k in PAGES.keys() if k != "Logbook"]

# 🔹 Track current active page in sidebar navigation
# Used by st.radio to know which module is selected
if "page" not in st.session_state:
    st.session_state.page = list(PAGES.keys())[0]


# 🔹 Store saved notes per analytical tab
# Structure:
# {
#   "Overview": [ {timestamp, notes, inputs}, ... ],
#   "Seafloor Signals": [ ... ],
#   ...
# }
# Logbook reads from this
if "notes" not in st.session_state or not isinstance(st.session_state.notes, dict):
    st.session_state.notes = {tab: [] for tab in NOTE_TABS}

# 🔹 Store sidebar filter parameters per tab
# Each module saves its filter selections here
# Structure:
# {
#   "Overview": {tissue, years, months, pollutant, ...},
#   ...
# }
if "params" not in st.session_state:
    st.session_state.params = {}


# 🔹 (Legacy / Optional)
# Holds generic note input if needed globally
# Not required if each tab uses its own keyed note input
if "note_input" not in st.session_state:
    st.session_state.note_input = ""


# 🔹 Controls edit mode lock system
# active = True → navigation locked to that tab
# tab = which tab the edit belongs to
# index = which note in that tab is being edited
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = {"active": False, "tab": None, "index": None}

# 🔹 Tracks delete confirmations per note
# Prevents accidental deletion
# Structure:
# { "Overview_0": True, "Overview_1": False, ... }
if "delete_confirm" not in st.session_state:
    st.session_state.delete_confirm = {}

# 🔹 Controls whether Notes panel auto-expands
# Used when reloading a note for editing
if "auto_expand_notes" not in st.session_state:
    st.session_state.auto_expand_notes = False

# 🔹 Controls whether Logbook expander is open
# UI-only state for user convenience
if "notes_expanded" not in st.session_state:
    st.session_state.notes_expanded = False

# ============================================================
# 🔹 Load custom CSS
# ============================================================

def load_css():
    css_path = Path(__file__).parent / "assets" / "styles.css"
    if css_path.exists():
        with css_path.open("r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#load_css()


# ============================================================
# 🔹 Sidebar Header
# ============================================================

st.sidebar.markdown("""
<h1 style="font-size:32px; font-weight:800; text-align:center;">
🌐 MarineScope
</h1>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    "<hr style='border-top: 2px solid #39FF14; margin: 10px 0;'>",
    unsafe_allow_html=True
)

# ============================================================
# 🔹 Navigation (WITH EDIT LOCK)
# ============================================================

# Handle redirect before radio is built
if "redirect_page" in st.session_state:
    st.session_state.page = st.session_state.redirect_page
    del st.session_state.redirect_page

# 🔹 Determine available pages AFTER state changes
if st.session_state.edit_mode["active"]:
    available_pages = [st.session_state.edit_mode["tab"]]
    disabled = True
else:
    available_pages = list(PAGES.keys())
    disabled = False


with st.sidebar:
   # Custom "Tabs" header in the sidebar
    st.sidebar.markdown("""
    <div style="
        font-size: 23px;
        font-weight: 800;
        color: #FFD700;
        text-align: justify;
        margin-bottom: 12px;
    ">
        Tabs:
    </div>
    """, unsafe_allow_html=True)
    page = st.radio(
        "Select module",
        available_pages,
        key="page",
        disabled=disabled
    )



# ---------------- Reminders Section ----------------
with st.sidebar:
        # Only show reminders if NOT Logbook
    if page != "Logbook":

        st.sidebar.markdown(
            "<hr style='border-top: 2px solid #39FF14; margin: 10px 0;'>",
            unsafe_allow_html=True
        )
        st.subheader("📝 Reminders")

        with st.expander(f"Reminders for {page} 👉", expanded=True):
            # Reminder 1
            st.markdown(
                """
                <div style="
                    background-color:#fff3e0;
                    color:#ff6600;
                    padding:10px;
                    border-radius:5px;
                    border:1px solid #ff9900;
                    margin-bottom:10px;
                ">
                    📌 Take a moment to capture your observations or interpretations 
                    in the sidebar notes panel below. When you're done, click Save to store them in the Logbook tab.
                </div>
                """,
                unsafe_allow_html=True
            )

            # Reminder 2
            st.markdown(
                """
                <div style="
                    background-color:#fff3e0;
                    color:#ff6600;
                    padding:10px;
                    border-radius:5px;
                    border:1px solid #ff9900;
                    margin-bottom:10px;
                ">
                    ⚠️ Please remember to save your observations or interpretations before switching tabs 🙂
                </div>
                """,
                unsafe_allow_html=True
            )

# --- Divider Line ---
st.sidebar.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

# Optional warning while editing
if st.session_state.get("edit_mode", {}).get("active", False):

    st.warning(
        "⚠️ You are editing a reloaded note. "
        "Please remember to save any changes before exiting edit mode."
    )

    if st.button("❌ Exit Edit Mode"):
        tab = st.session_state.edit_mode["tab"]
        #st.session_state.redirect_page = st.session_state.edit_mode["tab"]

        st.session_state.edit_mode = {"active": False, "tab": None, "index": None}
        st.session_state.edit_mode_saved = False
        st.session_state.edit_success_message = False  # ✅ clear the success message
        
        st.session_state.preload_note_input = ""

        st.session_state.auto_expand_notes = False

         # Optionally redirect to the tab you were editing
        st.session_state.redirect_page = tab

        st.rerun()

# ---------------- Toast Message Handler ----------------
if "toast_message" in st.session_state and st.session_state.toast_message:
    st.toast(st.session_state.toast_message)
    st.session_state.toast_message = ""


# ============================================================
# 🔹 Render Selected Page
# ============================================================

PAGES[page]()

