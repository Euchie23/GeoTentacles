"""
Executive Overview Module

Provides high-level KPIs and spatial visualization to identify pollution
hotspots and temporal trends. Designed for non-technical decision-makers.
"""

import streamlit as st
import pydeck as pdk
import pandas as pd
import calendar
from datetime import datetime

from utils.data_loader import load_pollution_data
from utils.preprocessing import convert_coordinates, render_pollutant_header, render_source_legend

# Loading Data
DATA_FILE = "squid_pollution.csv"

# ---------------------------------------------------
# RENDER FUNCTION
# ---------------------------------------------------

def render():


    # ---------------------------------------------------
    # TAB CONFIG
    # ---------------------------------------------------

    TAB_NAME = "Overview"

    DEFAULT_MAP_CENTER = [-48.0, -55.0]
    DEFAULT_MAP_ZOOM = 3


    # ---------------------------------------------------
    # SESSION STATE INITIALIZATION (SAFE ORDER)
    # ---------------------------------------------------

    if "map_zoom_level" not in st.session_state:
        st.session_state.map_zoom_level = DEFAULT_MAP_ZOOM

    if "notes" not in st.session_state:
        st.session_state.notes = {}

    if TAB_NAME not in st.session_state.notes:
        st.session_state.notes[TAB_NAME] = []

    if "params" not in st.session_state:
        st.session_state.params = {}

    if TAB_NAME not in st.session_state.params:
        st.session_state.params[TAB_NAME] = {}

    if "current_map_center" not in st.session_state:
        st.session_state.current_map_center = DEFAULT_MAP_CENTER

    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = {"active": False, "tab": None, "index": None}

    # Track if the user has saved the note while in edit mode
    if "edit_mode_saved" not in st.session_state:
        st.session_state.edit_mode_saved = False

    if "force_map_view" not in st.session_state:
        st.session_state.force_map_view = False


    st.subheader("Executive Overview")

    st.markdown(
        """
        ## Decision Context
    
        Marine ecosystems are exposed to spatially heterogeneous pollution driven by
        anthropogenic activity, biological uptake, and environmental transport.
        This overview supports rapid identification of pollution hotspots and
        priority areas for further investigation.
    
        *Methods demonstrated using squid tissue chemistry are fully transferable
        to other marine bioindicator species.*
    
        ### What does the full analytical journey look like?
    
        - 🌐 **Overview** → What did we measure?
        - 🌊 **Seafloor Signals** → What’s happening between measurements?
        - 🔮 **Toxic Tide Mapping** → Where might risk emerge next?
        - 🌿 **EcoPulse Index** → What does this mean for ecosystem condition?
        - 📉 **Disruption Dynamics** → What changed — and why does it matter?
        - 📘 **Logbook** → So what overall conclusions can we draw?
        """,
        unsafe_allow_html=True
    )

    st.markdown(
    """
    <div style='margin-top:25px; padding:18px; border-left:4px solid #39FF14; background-color:rgba(57,255,20,0.05);'>

    <b>Analytical Validation Note</b><br>

    Trace metal measurements were evaluated using Certified Reference Materials (CRMs). 
    Most metals achieved acceptable recovery rates (80–120%), supporting overall analytical reliability.

    However:
    - <b>Metal_H</b> and <b>Metal_J</b> showed elevated recoveries, potentially reflecting matrix effects or analytical interferences.
    - <b>Metal_I</b> was not certified in the CRM used and therefore could not be formally validated.

    For these three metals, interpretations should emphasize <b>relative differences between samples</b> rather than absolute concentration values.

    <b>Organic compounds (Organic_A, Organic_B, Organic_C, Organic_D)</b> were <u>not validated using CRMs</u> due to matrix complexity and the absence of suitable certified reference materials within project time constraints. 
    For these compounds, only <b>relative comparisons between samples</b> are recommended.

    For full validation documentation, visit the 
    <a href="https://github.com/Euchie23/SquidStack/tree/main/Foundation" target="_blank">
    Foundation module</a> in the SquidStack Repository.

    </div>
    """,
    unsafe_allow_html=True
    )

    df = load_pollution_data()
    df = convert_coordinates(df)
    # 1️⃣ Rename the column
    df = df.rename(columns={"Month_of_Capture": "Month"})


    # "Year" column conversion to integer
    df["Year"] = (
        pd.to_numeric(
            df["Year"].astype(str).str.replace(",", "", regex=False),
            errors="coerce"
        )
        .astype("Int64")
    )
  
    tab_params = st.session_state.params[TAB_NAME]

    # -----------------------------
    # Sidebar filters
    # -----------------------------
    with st.sidebar:
        st.subheader("Filters")

        with st.expander("Expand to adjust Filters 👉 ", expanded=False):


            # At the top of render():
            tab_params = st.session_state.params.get(TAB_NAME, {})

            # Tissue
            tissue_options = sorted(df["Tissue"].unique())
           
            if "tissue_selector" not in st.session_state:
                st.session_state.tissue_selector = tissue_options[0]
            if st.session_state.tissue_selector not in tissue_options:
                st.session_state.tissue_selector = tissue_options[0]

            previous_tissue = tab_params.get("tissue")

            tissue = st.selectbox(
                "Tissue",
                tissue_options,
                key="tissue_selector"
            )
            # saved_tissue = tab_params.get("tissue", tissue)
            tissue_changed = (
                previous_tissue is not None and
                tissue != previous_tissue
            )
            tab_params["tissue"] = tissue

            # Year
            available_years = sorted(df[df["Tissue"] == tissue]["Year"].unique())

            saved_years = tab_params.get("years", available_years)

            # If tissue changed → reset years
            if tissue_changed:
                valid_saved_years = available_years
            else:
                valid_saved_years = [y for y in saved_years if y in available_years]
                if not valid_saved_years:
                    valid_saved_years = available_years

            selected_years = st.multiselect(
                "Year",
                available_years,
                default=valid_saved_years
            )

            tab_params["years"] = selected_years

            # Month
            available_months = sorted(df[df["Tissue"]==tissue]["Month"].unique())
            month_options = [calendar.month_name[m] for m in available_months]
            saved_months = tab_params.get("months", month_options)
            valid_saved_months = [m for m in saved_months if m in month_options]
            if not valid_saved_months:
                valid_saved_months = month_options

            selected_months = st.multiselect(
                "Month",
                month_options,
                default=valid_saved_months
            )
            tab_params["months"] = selected_months

            # Pollutant
            available_pollutants = sorted(df["pollutant"].unique())
            saved_pollutant = tab_params.get("pollutant", available_pollutants[0])
            pollutant = st.selectbox("Pollutant", available_pollutants, index=available_pollutants.index(saved_pollutant))
            tab_params["pollutant"] = pollutant

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
                            See validation notes in the main panel for more details.
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
                            See validation notes in the main panel for more details.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # Convert selected month names back to numbers for filtering
            selected_month_numbers = [list(calendar.month_name).index(m) for m in selected_months]


            # 4️⃣ Pollutants available for tissue + years + months
          
            df_month_filtered = df[
                (df["Tissue"] == tissue) &
                (df["Year"].isin(selected_years)) &
                (df["Month"].isin(selected_month_numbers))
            ]

            # 5️⃣ Final filtered dataframe
            filtered = df_month_filtered[
                (df_month_filtered["pollutant"] == pollutant) &
                (df_month_filtered["status"] == "Detected")
            ]

        render_source_legend()

        # --- Divider Line ---
        st.sidebar.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)


        # Capture the inputs (example)
      
        inputs_to_save = {
            "tissue": st.session_state.params[TAB_NAME].get("tissue"),
            "years": st.session_state.params[TAB_NAME].get("years"),
            "months": st.session_state.params[TAB_NAME].get("months"),
            "pollutant": st.session_state.params[TAB_NAME].get("pollutant"),
            "map_center": st.session_state.current_map_center,
            "map_zoom_level": st.session_state.map_zoom_level
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



    # ----------------------------------
    # Pollutant Context Header
    # ----------------------------------
    st.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)
    render_pollutant_header(pollutant)
    st.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

    # -----------------------------
    # KPIs
    # -----------------------------
    col1, col2, col3, col4 = st.columns(4)

    if filtered.empty:
        col1.metric("Mean Concentration", "N/A")
        col2.metric("Max Concentration", "N/A")
        col3.metric("Detected Samples", 0)
        col4.metric("Time Span", "No data selected")
    else:
        # Numeric metrics
        col1.metric("Mean Concentration", f"{filtered['concentration'].mean():.2f} mg/kg")
        col2.metric("Max Concentration", f"{filtered['concentration'].max():.2f} mg/kg")
        col3.metric("Detected Samples", len(filtered))

        # Time Span calculation based on filtered data ONLY
        # ---- Improved Time Span Logic ----

        # Months (from user selection, not filtered data)
        selected_month_nums = sorted(selected_month_numbers)
        selected_years_sorted = sorted(selected_years)

        # ---- MONTH TEXT ----
        if len(selected_month_nums) == 1:
            month_text = calendar.month_name[selected_month_nums[0]]
        else:
            # Check if consecutive
            is_consecutive_months = all(
                selected_month_nums[i] + 1 == selected_month_nums[i + 1]
                for i in range(len(selected_month_nums) - 1)
            )

            if is_consecutive_months:
                month_text = f"{calendar.month_name[selected_month_nums[0]]} – {calendar.month_name[selected_month_nums[-1]]}"
            else:
                month_text = ", ".join(calendar.month_name[m] for m in selected_month_nums)

        # ---- YEAR TEXT ----
        if len(selected_years_sorted) == 1:
            year_text = f"{selected_years_sorted[0]}"
        else:
            # Check if consecutive
            is_consecutive_years = all(
                selected_years_sorted[i] + 1 == selected_years_sorted[i + 1]
                for i in range(len(selected_years_sorted) - 1)
            )

            if is_consecutive_years:
                year_text = f"{selected_years_sorted[0]}–{selected_years_sorted[-1]}"
            else:
                year_text = ", ".join(str(y) for y in selected_years_sorted)

        # Final Time Span
        time_span_text = f"{month_text}, {year_text}"

        with col4:
            st.markdown(f"""
                <div style="font-size:14px; line-height:1.4; font-weight:500;">
                    Time Span<br>
                    <span style="font-size:20px; font-weight:600;">
                        Months:<br>{month_text}<br>
                        Years:<br>{year_text}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
    st.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)


    # -----------------------------
    # Spatial visualization
    # -----------------------------
    st.subheader("Spatial Distribution of Pollution Observations")

    # NOTE: Coordinates will be properly parsed in preprocessing step
    # -----------------------------
    # Compute Map Center Early
    # -----------------------------
    map_df = filtered.dropna(subset=["longitude_dd", "latitude_dd"]).copy()

    if "current_map_center" not in st.session_state:

        if not map_df.empty:
            lat_center = map_df["latitude_dd"].mean()
            lng_center = map_df["longitude_dd"].mean()
        else:
            lat_center = -48.0
            lng_center = -55.0

        st.session_state.current_map_center = [lat_center, lng_center]


    if map_df.empty:
        st.warning("No data available for selected filters.")
        return
    
    import folium
    from streamlit_folium import st_folium

    # Center map on mean coordinates
    # lat_center = map_df["latitude_dd"].mean()
    # lng_center = map_df["longitude_dd"].mean()

    # Define colors for each year
    year_colors = {
        2019: "red",
        2020: "green",
        2021: "blue"
    }

    # Wrap the map rendering in a spinner
    with st.spinner("Rendering map, please wait..."):

        m = folium.Map(
            location=DEFAULT_MAP_CENTER,  # static initial
            zoom_start=DEFAULT_MAP_ZOOM   # static initial
        )


        # Add base tiles
        folium.TileLayer("Esri.WorldImagery", name="Satellite", control=True).add_to(m)
        
        folium.TileLayer("CartoDB.PositronOnlyLabels", name="Labels", overlay=True, control=True).add_to(m)

        # Add circle markers
        for _, row in map_df.iterrows():
            color = year_colors.get(row["Year"], "gray")  # default gray if year not in dic
            folium.CircleMarker(
                location=[row["latitude_dd"], row["longitude_dd"]],
                radius=5,
                color=color,
                fill=True,
                fill_opacity=0.7,
                tooltip=(
                    f"Year: {row['Year']}<br>"
                    f"Latitude (dd): {row['latitude_dd']:.4f}<br>"
                    f"Longitude (dd): {row['longitude_dd']:.4f}<br>"
                    f"Concentration: {row['concentration']:.2f} mg/kg"
                )
            ).add_to(m)

        # Add layer control to toggle tiles
        folium.LayerControl(collapsed=False).add_to(m)

        folium_kwargs = {
            "width": None,
            "height": 500,
            "key": f"folium_map_{TAB_NAME}",
            "returned_objects": ["center", "zoom"]
        }

        # Only push center/zoom when explicitly restoring
        if st.session_state.force_map_view:
            folium_kwargs["center"] = st.session_state.current_map_center
            folium_kwargs["zoom"] = st.session_state.map_zoom_level
            st.session_state.force_map_view = False

        map_state = st_folium(m, **folium_kwargs)


    if map_state:

        new_center = map_state.get("center")
        new_zoom = map_state.get("zoom")

        if new_center:
            rounded_center = [
                round(new_center["lat"], 6),
                round(new_center["lng"], 6),
            ]

            old_center = st.session_state.get("current_map_center")

            if old_center != rounded_center:
                st.session_state.current_map_center = rounded_center

        if new_zoom is not None:
            if new_zoom != st.session_state.get("map_zoom_level"):
                st.session_state.map_zoom_level = new_zoom


    st.caption(
        "Points represent detected pollutant concentrations. "
        "Subsequent modules interpolate and model these observations spatially."
    )

    st.markdown("----")

    # -----------------------------
    # Additional Info Message
    # -----------------------------

   # ⚓ Centered title for navigation
    st.markdown(
        "<h3 style='text-align: center; color: #E1EAF2;'>⚓ Continue Your Journey</h3>",
        unsafe_allow_html=True
    )

    html_links = """
    <div style="text-align: center; color: #E1EAF2; font-size: 20px; line-height: 1.6;">
    Dive deeper into the datasets, spatial analysis workflows, and predictive modeling that power this application.<br>
    🌊 <a href="https://github.com/Euchie23/GeoTentacles" target="_blank" style="color:#FFD700; font-weight:bold; text-decoration: underline;">Visit the GeoTentacles Repository</a>
    </div>
    """
    st.markdown(html_links, unsafe_allow_html=True)

    st.markdown("----")



    # -----------------------------
    # Transition Message
    # -----------------------------
    st.markdown(
        """
        <div style='text-align:center; margin-top: 30px;'>
            <span style='color:#39FF14; font-weight:bold; font-size:28px;'>
                🌐 We've reviewed pollution levels at individual monitoring sites — but can we confidently assess risk across the entire marine area based on discrete samples alone? 
                Move to the Seafloor Signals tab to evaluate how contamination may extend between these observed locations.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

