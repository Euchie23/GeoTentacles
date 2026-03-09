import streamlit as st
import numpy as np
import plotly.express as px
from datetime import datetime

from utils.data_loader import load_pollution_data
from utils.preprocessing import preprocess_pollution_data, aggregate_pollution, convert_coordinates,render_pollutant_header, render_source_legend
from utils.spatial_utils import create_grid, idw_interpolation





def generate_interpolation_insights(z, pollutant, tissue, year, unit="mg/kg"):
    mean_val = np.nanmean(z)
    max_val = np.nanmax(z)
    min_val = np.nanmin(z)

    return f"""
**How to read this visualization**

This figure is a **spatially referenced concentration surface**, designed to
*visually resemble a map* while remaining a data-driven analytical view.

It represents a portion of the **Southwest Atlantic Ocean**, located
**east of Argentina and north of the Falkland Islands**.

- The horizontal axis shows **longitude (decimal degrees)**  
  - Moving **right** corresponds to traveling **eastward**, farther offshore  
  - Moving **left** corresponds to traveling **westward**, toward the South
    American continental margin
- The vertical axis shows **latitude (decimal degrees)**  
  - Moving **upward** corresponds to traveling **northward**, toward the Equator  
  - Moving **downward** corresponds to traveling **southward**, toward colder
    sub-Antarctic and Antarctic waters

Negative latitude and longitude values are expected for this region and simply
reflect positions **south of the Equator** and **west of the Prime Meridian**.

Colors represent **estimated concentration levels**, with warmer colors
indicating relatively higher values and cooler colors indicating lower values.

---

**What this surface represents**

This visualization shows an **interpolated concentration surface** for
**{pollutant}** in **{tissue} tissue for {year}**.

Values are expressed in **{unit}**, consistent with laboratory-reported
measurements.  
The surface is generated using **distance-weighted interpolation**, meaning
estimates are informed by nearby observed samples.

Importantly, this is **not a navigation map** and does not imply continuous
measurement coverage.

---

**Key spatial insights**

- Typical estimated concentrations across the area are approximately
  **{mean_val:.2f} {unit}**
- Some locations display higher estimated values (up to **{max_val:.2f} {unit}**),
  suggesting **localized zones of elevated concentration**
- Lower estimated values (around **{min_val:.2f} {unit}**) indicate areas with
  comparatively reduced levels

These patterns describe **regional gradients and hotspots**, not precise
conditions at individual points.

---

**How this information should be used**

✔ To understand **broad spatial patterns** across the study area  
✔ To support **sampling prioritization and monitoring design**  
✔ To guide **screening-level decision-making**

⚠️ Estimates are influenced by sampling density and spatial distribution  
⚠️ Uncertainty increases in areas farther from observed data points  
⚠️ This surface should not be interpreted as direct measurement or used for
regulatory compliance

This visualization is intended as a **decision-support and exploratory tool**.
"""


def render():

    # ---------------------------------------------------
    # TAB CONFIG
    # ---------------------------------------------------

    TAB_NAME = "Seafloor Signals"

    # ---------------------------------------------------
    # SESSION STATE INITIALIZATION (SAFE ORDER)
    # ---------------------------------------------------

    if "notes" not in st.session_state:
        st.session_state.notes = {}

    if TAB_NAME not in st.session_state.notes:
        st.session_state.notes[TAB_NAME] = []

    if "params" not in st.session_state:
        st.session_state.params = {}

    if TAB_NAME not in st.session_state.params:
        st.session_state.params[TAB_NAME] = {}

    st.header("🌊 Seafloor Signals — Pollution Interpolation")

    # --------------------------------------------------
    # INTRO — PURPOSE & LAYERS
    # --------------------------------------------------

    st.markdown("""
    This module helps you **see where pollutants are most concentrated on the seafloor**. 
    It takes measurements from individual samples and creates a **continuous map of potential hotspots** across the study area.

    **Why it matters:**  
    - Identifies areas that may need **additional monitoring or management**  
    - Helps prioritize where to **collect more samples or focus interventions**  
    - Offers a clear, visual way to interpret **spatial patterns of pollution**
    """)

    df = preprocess_pollution_data(load_pollution_data())
    df = convert_coordinates(df)


    with st.sidebar:
        st.subheader("Interpolation Controls")

        with st.expander("🌊 Expand to adjust Interpolation Controls", expanded=False):

            tab_params = st.session_state.params.setdefault(TAB_NAME, {})

            pollutant_options = sorted(df["pollutant"].unique())
            tissue_options = sorted(df["Tissue"].unique())
            year_options = sorted(df["Year"].unique())

            # pollutant = st.selectbox(
            #     "Pollutant",
            #     pollutant_options,
            #     index=pollutant_options.index(
            #         tab_params.get("pollutant", pollutant_options[0])
            #     )
            # )

            pollutant = st.selectbox(
                "Pollutant",
                pollutant_options,
                index=pollutant_options.index(tab_params.get("pollutant", pollutant_options[0])),
                label_visibility="visible"  # ensures label is clear
            )

            tissue = st.selectbox(
                "Tissue",
                tissue_options,
                index=tissue_options.index(
                    tab_params.get("tissue", tissue_options[0])
                )
            )

            year = st.selectbox(
                "Year",
                year_options,
                index=year_options.index(
                    tab_params.get("year", year_options[0])
                )
            )

            resolution = st.slider(
                "Map resolution",
                50,
                200,
                tab_params.get("resolution", 100),
                10,
                help="Higher values produce smoother surfaces but increase computation time."
)

            tab_params["pollutant"] = pollutant
            tab_params["tissue"] = tissue
            tab_params["year"] = year
            tab_params["resolution"] = resolution

            # Finally save back to session state
            st.session_state.params[TAB_NAME] = tab_params

               # # Show validation notes
            problem_metals = ["Metal_H", "Metal_I", "Metal_J"]
            problem_organics = ["Organic_A", "Organic_B", "Organic_C", "Organic_D"]
            problem_pollutants = problem_metals + problem_organics

            if pollutant in problem_pollutants:
                # Metals
                if pollutant in problem_metals:
                    st.markdown(
                        f"""
                        <div style="
                            background-color:#fff3e0;
                            color:#ff6600;
                            padding:10px;
                            border-radius:5px;
                            border:1px solid #ff9900;
                        ">
                            ⚠️ Note: {pollutant} should be interpreted using relative comparisons between samples rather than absolute concentration values.
                            See analytical validation notes in the Overview tab for more details.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:  # Organic compound
                    st.markdown(
                        f"""
                        <div style="
                            background-color:#fff3e0;
                            color:#ff6600;
                            padding:10px;
                            border-radius:5px;
                            border:1px solid #ff9900;
                        ">
                            ⚠️ Note: {pollutant} is an organic compound that was not validated with CRMs due to time constraints and matrix complexity.
                            Focus on relative differences rather than absolute values.
                            See analytical validation notes in the Overview tab for more details.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        render_source_legend()

        # --- Divider Line ---
        st.sidebar.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

        # Capture the inputs (example)
      
        inputs_to_save = {
            "tissue": st.session_state.params[TAB_NAME].get("tissue"),
            "year": st.session_state.params[TAB_NAME].get("year"),
            "pollutant": st.session_state.params[TAB_NAME].get("pollutant"),
            "resolution": st.session_state.params[TAB_NAME].get("resolution")
        }


        # ---------------------------------------------------
        # NOTES PANELS
        # ---------------------------------------------------

   
        st.markdown("### 🗒️ Notes Panel")

        with st.expander(
            f"💬 Notes for {TAB_NAME}",
            expanded=st.session_state.get("auto_expand_notes", False)
        ):

            # persistent success message (does not disappear until Exit Edit Mode)
            # at the top of overview.py expander
            msg_container = st.empty()

            if st.session_state.get("edit_success_message", False):
                msg_container.success("✅ Changes Saved! please click '❌ Exit Edit Mode' to unlock tabs.")
            else:
                msg_container.empty()  # ensures message disappears immediately
                

            note_key = f"{TAB_NAME}_note_input"
            if note_key not in st.session_state:
                st.session_state[note_key] = ""

            in_edit_mode = st.session_state.edit_mode.get("active", False)
            edit_saved = st.session_state.get("edit_mode_saved", False)

            if in_edit_mode and not edit_saved and "preload_note_input" in st.session_state:
                st.session_state[note_key] = st.session_state.pop("preload_note_input")

            # ----------------- EDIT MODE, NOT SAVED -----------------
            if in_edit_mode and not edit_saved:
                with st.form(f"edit_note_form_{TAB_NAME}", clear_on_submit=False):
                    note_text = st.text_area(
                        "Edit your note here:",
                        key=note_key,
                        height=150,
                        disabled=edit_saved
                    )
                    submitted = st.form_submit_button("💾 Save Changes")
                    if submitted:
                        content = st.session_state[note_key].strip()
                        if content:
                            edit_index = st.session_state.edit_mode.get("index", 0)
                            st.session_state.notes[TAB_NAME][edit_index] = {
                                "timestamp": datetime.now(),
                                "notes": content,
                                "inputs": inputs_to_save
                            }
                            st.session_state.edit_mode_saved = True
                            st.session_state.edit_success_message = True
                            st.session_state.auto_expand_notes = True  # keep expander open
                            st.rerun()
                        else:
                            st.warning("⚠️ Nothing to save (note is empty).")

            # ----------------- EDIT MODE, ALREADY SAVED -----------------
            elif in_edit_mode and edit_saved:
                st.text_area(
                    "Edit your note (saved):",
                    key=note_key,
                    height=150,
                    disabled=True
                )
                st.button("💾 Save Note", disabled=True)

            # ----------------- NORMAL NOTE -----------------
            else:
                with st.form("normal_note_form", clear_on_submit=True):
                    note_text = st.text_area(
                        "Write your note here:",
                        key=note_key,
                        height=150,
                        placeholder="Type your note..."
                    )
                    submitted = st.form_submit_button("💾 Save Note")
                    if submitted:
                        content = st.session_state[note_key].strip()
                        if content:
                            st.session_state.notes[TAB_NAME].append({
                                "timestamp": datetime.now(),
                                "notes": content,
                                "inputs": inputs_to_save
                            })
                            st.success("✅ Note saved to Logbook!")
                        else:
                            st.warning("⚠️ Nothing to save (note is empty).")

        # -----------------------------
        # Footer Contact Information
        # -----------------------------

        # --- Divider Line ---
        st.sidebar.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

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

    st.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

    render_pollutant_header(pollutant)

    st.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

    subset = df[
        (df["pollutant"] == pollutant) &
        (df["Tissue"] == tissue) &
        (df["Year"] == year)
    ]

    if subset.empty:
        st.warning("No data available for this selection.")
        return

    agg = aggregate_pollution(subset)
    #st.dataframe(agg[["longitude_dd", "latitude_dd", "concentration"]].head().reset_index(drop=True), width='stretch')


    x = agg["longitude_dd"].astype(float).values
    y = agg["latitude_dd"].astype(float).values
    z = agg["concentration"].astype(float).values


    xi, yi = create_grid(x, y, resolution)
    zi = idw_interpolation(x, y, z, xi, yi)

    custom_scale = [
    [0.0, "green"],   # lowest value
    [0.33, "yellow"],
    [0.66, "orange"],
    [1.0, "red"]      # highest value
]
    
     # Wrap the map rendering in a spinner
    with st.spinner("Rendering map, please wait..."):

        fig = px.imshow(
            zi,
            x=xi[0],
            y=yi[:, 0],
            origin="lower",
            aspect="equal",
            color_continuous_scale=custom_scale,
            labels={
                "color": f"{pollutant} concentration (mg/kg)",
                "x": "Longitude (decimal degrees)",
                "y": "Latitude (decimal degrees)"
            }
        )

        fig.update_layout(
        xaxis_title="Longitude (decimal degrees)",
        yaxis_title="Latitude (decimal degrees)"
        )

        fig.update_xaxes(
            tickangle=0,
            tickformat=".2f",
            dtick=0.5,  # show every 0.5 degrees
            automargin=True
        )


        # ---- Hover formatting ----
        fig.update_traces(
            hovertemplate=
            "Longitude: %{x:.3f}<br>" +
            "Latitude: %{y:.3f}<br>" +
            f"{pollutant} concentration: %{z:.3f} mg/kg<extra></extra>"
        )

    st.plotly_chart(fig, width='stretch')

    st.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

    with st.expander("🧭 What this means - Click here to see full analysis"):
        st.markdown(generate_interpolation_insights(zi, pollutant, tissue, year))


    # -----------------------------
    # Transition Message
    # -----------------------------
    st.markdown(
    """
    <div style='text-align:center; margin-top: 30px;'>
        <span style='color:#39FF14; font-weight:bold; font-size:28px;'>
            🌐 We’ve mapped estimated pollution distribution across the marine area — but how might these contamination patterns evolve over time? 
            Proceed to the Toxic Tide Mapping tab to forecast where future hotspots may emerge.
        </span>
    </div>
    """,
    unsafe_allow_html=True
    )

