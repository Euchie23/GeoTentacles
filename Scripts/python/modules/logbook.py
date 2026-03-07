# =========================================================
# 📦 CORE LIBRARIES
# =========================================================

import io
import os
import time
from datetime import datetime
from utils.notes import format_note_display
import gspread
from google.oauth2.service_account import Credentials

# =========================================================
# 🌊 STREAMLIT FRAMEWORK & SESSION MANAGEMENT
# =========================================================
import streamlit as st

DEFAULT_MAP_CENTER = [-48.0, -55.0]
DEFAULT_MAP_ZOOM = 6
# DEFAULT_POLLUTANT = "Metal_A"
# DEFAULT_TISSUE = "liver"
# DEFAULT_YEAR = 2019
# DEFAULT_MONTH = 3

def set_confirm(delete_key):
    st.session_state[delete_key] = True

def cancel_confirm(delete_key):
    st.session_state[delete_key] = False

def delete_note(tab_name, i, delete_key):
    st.session_state.notes[tab_name].pop(i)
    st.session_state.pop(delete_key)
    
    # keep expander open after deletion
    st.session_state[f"expander_state_{tab_name}"] = True

    st.session_state.toast_message = f"🗑 Deleted note {i+1} from {tab_name}"
    st.session_state.note_deleted = True  # set a flag instead of st.rerun()


def render():
    st.title("📓 Logbook")
    # If a note was deleted in the previous run, clear the flag
    if st.session_state.get("note_deleted", False):
        st.session_state.note_deleted = False


    notes_exist = any(st.session_state.notes[tab] for tab in st.session_state.notes)
    if not notes_exist:
        st.info("No notes yet. Go to any tab to add some notes!")
    else:
        for tab_name, notes in st.session_state.notes.items():
            if not notes:
                continue

             # Check if the expander should be open
            expander_state_key = f"expander_state_{tab_name}"
            if expander_state_key not in st.session_state:
                st.session_state[expander_state_key] = False  # Default state is collapsed

            with st.expander(f"🗂 {tab_name} ({len(notes)} notes)",expanded=st.session_state[expander_state_key]):
            # with st.expander(f"🗂 {tab_name} ({len(notes)} notes)", expanded=False):
                for i, note in enumerate(notes):
                    col1, col2, col3 = st.columns([6, 1, 1])
                    with col1:
                        st.markdown(format_note_display(note, tab_name))
                    with col2:
                        if st.button("✏️", key=f"edit_{tab_name}_{i}"):
                            #entry = note
                            entry = st.session_state.notes[tab_name][i]

                             # Restore inputs for this tab
                            st.session_state.params[tab_name] = entry["inputs"].copy()

                            st.session_state.tissue_selector = entry["inputs"].get("tissue")

                            # Restore map state separately if available
                            saved_inputs = entry.get("inputs", {})

                            if "map_center" in saved_inputs:
                                st.session_state.current_map_center = saved_inputs["map_center"]

                            if "map_zoom_level" in saved_inputs:
                                st.session_state.map_zoom_level = saved_inputs["map_zoom_level"]

                            st.session_state.force_map_view = True

                            #Restore note text
                            st.session_state.preload_note_input = entry["notes"]

                            # Restore tab inputs from snapshot
                            # for k, v in entry["inputs"].items():
                            #     st.session_state.params[k] = v

                            # Restore all tab inputs from snapshot (generic, works for any tab)
                            #st.session_state.params[tab_name] = entry["inputs"].copy()

                            # Restore map state
                            # ✅ Reset saved flag so panel is active on new edit
                            #st.session_state.edit_mode_saved = False

  

                            # Restore note text
                            #st.session_state.preload_note_input = entry["notes"]

                            # Set edit mode
                            st.session_state.edit_mode = {"active": True, "tab": tab_name, "index": i}
                            # ✅ Force notes panel to auto-expand after rerun
                            st.session_state.edit_mode_saved = False
                            st.session_state.auto_expand_notes = True
                            st.session_state.toast_message = f"📸 Snapshot reloaded for {tab_name}. Please save changes after editing."

                            #st.session_state.page = tab_name

                            st.rerun()
                    with col3:
                        delete_key = f"delete_confirm_{tab_name}_{i}"

                        # initialize confirm state if missing
                        if delete_key not in st.session_state:
                            st.session_state[delete_key] = False

                        c1, c2 = st.columns(2)

                        if not st.session_state[delete_key]:
                            # Show delete button
                            c1.button(
                                "🗑",
                                key=f"delete_{tab_name}_{i}",
                                on_click=set_confirm,
                                args=(delete_key,)
                            )
                        else:
                            # Show confirm / cancel buttons
                            c1.button(
                                "✅",
                                key=f"confirm_{tab_name}_{i}",
                                on_click=delete_note,
                                args=(tab_name, i, delete_key)
                            )
                            c2.button(
                                "❌",
                                key=f"cancel_{tab_name}_{i}",
                                on_click=cancel_confirm,
                                args=(delete_key,)
                            )

                # Handle the expander's open/close state across reruns
                if 'auto_expand_notes' in st.session_state:
                    st.session_state[expander_state_key] = st.session_state.auto_expand_notes

    # --- Final Observation + Download ---
    st.subheader("🧾 Final Observation")
    st.session_state.final_observation = st.text_area(
        "Write your final observation here:",
        value=st.session_state.get("final_observation", ""),
        height=150,
        placeholder="Summarize your findings..."
    )

    st.markdown("---")
    st.warning(
        "⚠️ **Important:** Your notes are stored only for this session. "
        "If you leave or refresh the app, they will be lost.\n\n"
        "💾 Please download them to your computer if you wish to keep a copy."
    )

    # --- Step 1: Prepare content only when clicked ---
    if st.button("🧩 Prepare Logbook for Download"):
        all_notes_text = f"📝 FINAL OBSERVATION:\n{st.session_state.final_observation}\n\n📔 INDIVIDUAL NOTES:\n\n"
        for tab, notes in st.session_state.notes.items():
            if notes:
                all_notes_text += f"{tab} ({len(notes)} notes):\n"
                for note in notes:
                    all_notes_text += format_note_display(note, tab)
                all_notes_text += "\n"

        st.session_state.all_notes_text = all_notes_text
        st.success("✅ Logbook is ready to download!")

    if "all_notes_text" in st.session_state and st.session_state.all_notes_text:
        buffer = io.BytesIO(st.session_state.all_notes_text.encode("utf-8"))

        # Current datetime string
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"logbook_{timestamp}.txt"
        st.download_button(
            label="📥 Download Logbook (.txt)",
            data=buffer,
            file_name=file_name,
            mime="text/plain"
        )
    
    # --- Define the function ---
    def send_notes_to_host(all_notes_text, tab_name="MarineScope"):
        try:
            # Authenticate with Google Sheets
            creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"],  scopes=["https://www.googleapis.com/auth/spreadsheets"])
            client = gspread.authorize(creds)

            # Open the target sheet by ID (no need for an extra ["google_sheets"] key)
            sheet = client.open_by_key("193Sgwcbx8sX6lF5i94XKTR_RzCx-SpQg4af_4-WBziA").worksheet(tab_name)

            # Append a new anonymous submission
            sheet.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), all_notes_text])

            return True
        except Exception as e:
            st.error(f"Error sending notes: {e}")
            return False


    # --- In your Logbook section, keep all this under the same indentation ---
    st.markdown("---")
    st.subheader("📤 Send to Host (Optional)")
    st.info(
        "🧠 By sharing your notes *anonymously*, you help the host improve their "
        "data interpretation, statistical analysis, and app development skills.\n\n"
        "No personal information is collected — only your text notes are shared.\n\n"
        "*It may take a few seconds to confirm whether your notes were successfully sent to the host. Thank you for your patience 🙂*"
    )

    send_to_host = st.checkbox("Send my notes to the host (optional)")

    if send_to_host:
        if st.button("📤 Confirm & Send"):
            # Gather all notes + final observation into one text block
            all_notes_text = "📝 FINAL OBSERVATION:\n" + st.session_state.final_observation + "\n\n"
            all_notes_text += "📔 INDIVIDUAL NOTES:\n\n"
            for tab_name, notes in st.session_state.notes.items():
                if notes:
                    all_notes_text += f"[{tab_name}] ({len(notes)} notes):\n"
                    for note in notes:
                        all_notes_text += format_note_display(note, tab_name)
                    all_notes_text += "\n"
            
            
            # Show spinner while sending
            with st.spinner("⏳ Connecting to Google Sheets... This may take a few seconds."):
                    # Send to Google Sheets
                    success = send_notes_to_host(all_notes_text)

            if success:
                st.success("✅ Upload to Google Sheets successful! Your notes were sent anonymously. Thank you!")
            else:
                st.error("❌ Failed to send notes. Please try again later.")


     # -----------------------------
    # Sidebar filters
    # -----------------------------
    with st.sidebar:
  
    # -----------------------------
    # Footer Contact Information
    # -----------------------------

        # --- Contact Block ---
        st.sidebar.markdown("""
        <div style="margin-top: 10px; color: white;">
        <p style="color: #39FF14; font-weight: bold; font-size: 22px;">📬 Want to connect or collaborate?</p>
        <ul style="list-style-type: none; padding-left: 0; line-height: 1.7;">
            <li style="font-size: 16px; font-weight: bold;">📧 Email: 
            <a href="mailto:euchiejnpierre@gmail.com" style="color: #39FF14; text-decoration: none;">Euchie</a>
            </li>
            <li style="font-size: 16px; font-weight: bold;">💼 LinkedIn: 
            <a href="https://www.linkedin.com/in/euchiejnpierre/" target="_blank" style="color: #39FF14; text-decoration: none;">Visit Profile</a>
            </li>
            <li style="font-size: 16px; font-weight: bold;">🌍 GitHub: 
            <a href="https://github.com/Euchie23" target="_blank" style="color: #39FF14; text-decoration: none;">More About Me</a>
            </li>
            <li style="font-size: 16px; font-weight: bold;">💬 Share Your Thoughts: 
            <a href="https://github.com/Euchie23/SquidStock/issues/new" target="_blank" style="color: #39FF14; text-decoration: none;">Open an Issue</a>
            </li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-top: 2px solid #39FF14; margin: 10px 0;'>", unsafe_allow_html=True)

    st.markdown(
    """
    <div style='text-align:center; margin-top: 40px;'>

    <span style='color:#39FF14; font-weight:bold; font-size:26px;'>
    🌊 Where do these insights lead us?
    </span>
    <br>
    Through spatial interpolation, predictive modeling, ecosystem indexing, 
    and disruption analysis, MarineScope brings together concentration dynamics 
    and fisheries intelligence into a unified spatial narrative.

    This tentatively concludes the GeoTentacles analytical suite — 
    the spatial chapter of the SquidFest trilogy.
    <br>
    If you’d like to explore further, please check out the:

    🔬 <a href="https://github.com/Euchie23/SquidStack" target="_blank"><u>SquidStack Repository</u></a>  
    where we explore concentration dynamics, bioindicator analysis, time-lag effects, and human health risk evaluation.

    OR the

    🎣 <a href="https://github.com/Euchie23/SquidStock" target="_blank"><u>SquidStock Repository</u></a>  
    where we dive into CPUE standardization, biomass estimation, climate-driven fisheries modeling, and stock dynamics.
    <br>
    📘 Before leaving, take a moment to review your notes in the Logbook.

    What overall conclusion emerges from your analytical journey?
    <br>
    Thank you for your time, curiosity, and participation.

    Stay tuned for future interactive decision tools. 👋🏾🙂🤓

    </div>
    """,
    unsafe_allow_html=True
    )