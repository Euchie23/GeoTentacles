import streamlit as st
import plotly.express as px
import numpy as np
from datetime import datetime

from utils.data_loader import load_pollution_data
from utils.preprocessing import preprocess_pollution_data, convert_coordinates
from utils.index_utils import compute_ecopulse_index
from utils.notes import notes_panel


# ======================================================
# Dynamic executive insights
# ======================================================

def generate_ecopulse_insights( df, year, tissue, view_mode, maturity_levels, gender_filter):
    if df.empty:
        return "No data available for the selected filter configuration."

    mean_index = df["EcoPulse"].mean()

    # ----------------------------
    # New: data scope counts
    # ----------------------------
    n_samples = len(df)
    n_locations = df[["longitude_dd", "latitude_dd"]].drop_duplicates().shape[0]
    low_pct = (df["EcoPulse"] < 0.4).mean() * 100
    high_pct = (df["EcoPulse"] > 0.7).mean() * 100

    # ----------------------------------
    # Overall ecosystem condition label
    # ----------------------------------
    status = (
        "generally resilient"
        if mean_index > 0.6
        else "under moderate stress"
        if mean_index > 0.4
        else "potentially degraded"
    )

    # ----------------------------------
    # Maturity interpretation (dynamic)
    # ----------------------------------
    #Defining ordered maturity labels
    MATURITY_MAP = {
    1: "Juvenile",
    2: "Immature",
    3: "Maturing",
    4: "Mature",
    5: "Spawning"
}


    #Deriving slected maturity context dynamically
    selected_stages = [MATURITY_MAP[k] for k in sorted(maturity_levels)]

# ----------------------------------
# Maturity interpretation (robust)
# ----------------------------------

    if len(selected_stages) == 1:
        maturity_note = (
            f"This view focuses exclusively on the **{selected_stages[0]}** life stage, "
            "providing a targeted snapshot of ecosystem condition for this specific "
            "phase of biological development."
        )

    elif len(selected_stages) == 2:
        maturity_note = (
            f"This view focuses on **{selected_stages[0]}–{selected_stages[1]}** life stages, "
            "capturing ecosystem condition across closely related phases of development."
        )

    elif max(maturity_levels) <= 2:
        maturity_note = (
            "This view emphasizes **early life stages (Juvenile–Immature)**, which are "
            "typically more sensitive to environmental stressors and may signal future "
            "population-level impacts."
        )

    elif min(maturity_levels) >= 3:
        maturity_note = (
            "This view emphasizes **later life stages (Maturing–Spawning)**, reflecting "
            "ecosystem condition closer to peak reproductive investment."
        )

    else:
        maturity_note = (
            "This view includes a **broad range of maturity stages**, from juvenile to "
            "spawning individuals, providing an integrated picture of ecosystem condition "
            "across the life cycle."
        )


    # ----------------------------------
    # Gender context (non-causal)
    # ----------------------------------
    if len(gender_filter) == 1:
        gender_note = (
            f"This view includes **{gender_filter[0].lower()} individuals only**. "
            "Observed patterns reflect this subset but EcoPulse scores are **not sex-adjusted**."
        )
    else:
        gender_note = (
            "This view includes **both female and male individuals**. "
            "EcoPulse scores are **not stratified by sex** and represent combined ecosystem condition."
        )

    # ----------------------------------
    # View-mode interpretation
    # ----------------------------------
    view_note = {
        "Overall ecosystem stress": (
            "This perspective integrates pollution exposure and biological condition "
            "to highlight **general ecosystem stress patterns** across the study area."
        ),
        "Juvenile sensitivity focus": (
            "This perspective emphasizes **juvenile vulnerability**, where environmental "
            "stress may have long-term consequences for population resilience."
        ),
        "High contamination focus": (
            "This perspective highlights areas where **contamination pressure is relatively elevated** "
            "compared to the rest of the study area."
        )
    }[view_mode]

    # ----------------------------------
    # Distribution interpretation (robust logic)
    # ----------------------------------

    if low_pct == 0:
        low_statement = (
            "No sampled locations fall into the low-health category, "
            "indicating no areas of severe ecosystem degradation under the current threshold."
        )
    elif low_pct < 10:
        low_statement = (
            f"Only about {low_pct:.0f}% of sampled locations fall into the low-health category, "
            "suggesting limited but localized areas of elevated ecological stress."
        )
    else:
        low_statement = (
            f"Approximately {low_pct:.0f}% of sampled locations fall into the low-health category, "
            "indicating more widespread areas of ecological stress."
        )

    if high_pct == 0:
        high_statement = (
            "No locations fall into the highest health category, suggesting resilience may be constrained "
            "under current environmental pressures."
        )
    elif high_pct > 70:
        high_statement = (
            f"Roughly {high_pct:.0f}% of locations indicate strong ecosystem condition, "
            "suggesting broadly resilient environmental performance."
        )
    else:
        high_statement = (
            f"Roughly {high_pct:.0f}% of locations indicate relatively strong ecosystem condition "
            "compared to the rest of the study area."
    )
    return f"""
**How to read this visualization**

This figure is a **spatially referenced index map**, designed to visually resemble a
geographic map while remaining a data-driven analytical view.

It represents a portion of the **Southwest Atlantic Ocean**, located **east of Argentina
and north of the Falkland Islands**.

- The horizontal axis shows **longitude (decimal degrees)**  
  - Moving **right** corresponds to traveling **eastward**, farther offshore  
  - Moving **left** corresponds to traveling **westward**, toward the South American
    continental margin
- The vertical axis shows **latitude (decimal degrees)**  
  - Moving **upward** corresponds to traveling **northward**, toward the Equator  
  - Moving **downward** corresponds to traveling **southward**, toward colder
    sub-Antarctic waters

Negative values are expected for this region and simply reflect locations **south of
the Equator** and **west of the Prime Meridian**.

Each point represents a sampling location, and its color reflects the EcoPulse Index.

The color scale follows a **stress-to-resilience gradient**:

- **Red** indicates higher ecological stress and lower EcoPulse values  
- **Yellow** indicates moderate ecosystem condition  
- **Orange** indicates improving ecological condition  
- **Green** indicates higher ecological resilience and stronger ecosystem performance

Depending on the selected filters, multiple biological samples collected at the
same location are aggregated into a single point. 
Circle size reflects the number of samples contributing to the EcoPulse estimate.
Larger circles therefore represent locations with greater sampling coverage.


This is **not a navigation map**, but a spatial framework for interpreting regional patterns.

---

**What the EcoPulse Index represents**

The EcoPulse Index provides an **integrated snapshot of marine ecosystem condition** by
combining pollution exposure, biological condition, and tissue-specific relevance.

This view summarizes results for **{tissue} tissue in {year}**.

The index ranges from **0 (higher ecological stress)** to **1 (higher ecological resilience)**.

---

**Data scope for this view**

This summary is based on **{n_samples} biological samples** collected across  
**{n_locations} sampling locations** under the current filter configuration.

Results reflect only the selected **year, tissue type, maturity stages, and gender filters**.

---

**Key findings from this view**

- Overall ecosystem condition appears **{status}**
- The average EcoPulse score across sampled locations is **{mean_index:.2f}**
- {low_statement}
- {high_statement}

{maturity_note}

{gender_note}

---

**Interpretation context**

{view_note}

Together, these patterns highlight **spatial contrasts in ecosystem condition**, rather
than precise conditions at individual sites.

---

**How this information should be used**

✔ To understand **broad spatial patterns in ecosystem health**  
✔ To compare **relative stress and resilience across locations**  
✔ To support **screening, prioritization, and planning decisions**

⚠️ EcoPulse values reflect **relative condition**, not regulatory thresholds  
⚠️ Results are influenced by sampling coverage and weighting choices  
⚠️ This index is intended as a **decision-support and exploratory tool**, not a compliance metric
"""



# ======================================================
# Main render function
# ======================================================

def render():

    # ---------------------------------------------------
    # TAB CONFIG
    # ---------------------------------------------------

    TAB_NAME = "EcoPulse Index"


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


    st.title("🌿 EcoPulse Index — Integrated Marine Health")

    st.markdown("""
The **EcoPulse Index** provides a high-level view of marine ecosystem condition by
integrating **pollution exposure and biological context**.

It is designed as a **decision-support and screening tool** to help identify
areas that may be **resilient, stressed, or potentially vulnerable**.
""")

    # -----------------------------
    # Load and prepare data
    # -----------------------------
    df = preprocess_pollution_data(load_pollution_data())
    df = convert_coordinates(df)

    # Maturity level labels
    MATURITY_MAP = {
        1: "Juvenile",
        2: "Immature",
        3: "Maturing",
        4: "Mature",
        5: "Spawning"
    }

    df["Maturity_label"] = df["Maturity_level"].map(MATURITY_MAP)

    # -----------------------------
    # Sidebar controls
    # -----------------------------
    with st.sidebar:
        st.subheader("EcoPulse Controls")

        with st.expander("🌿 Expand to adjust EcoPulse Controls", expanded=False):

            
            # At the top of render():
            tab_params = st.session_state.params.get(TAB_NAME, {})

            year_options = sorted(df["Year"].unique())

            tissue_options = sorted(df["Tissue"].unique())

            tissue = st.selectbox(
                "Tissue type",
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

            maturity_options = [MATURITY_MAP[k] for k in sorted(MATURITY_MAP)]

            maturity_labels = st.multiselect(
                "Maturity stage",
                options=maturity_options,
                default=tab_params.get("maturity_labels", maturity_options),
                help="Select at least one life stage to enable biological interpretation."
            )


            if not maturity_labels:
                st.warning(
                    "Please select at least one **maturity stage** to continue with the EcoPulse analysis."
                )
                st.stop()
                
            # --------------------------------------------------
            # Gender label mapping (readability)
            # --------------------------------------------------
            GENDER_MAP = {
                0: "Female",
                1: "Male"
            }

            df["Gender_label"] = df["Gender"].map(GENDER_MAP).fillna("Unknown")

            gender_options = sorted(df["Gender_label"].unique())

            gender_filter = st.multiselect(
                "Gender",
                options=gender_options,
                default=tab_params.get("gender_filter", gender_options),
                help="Used for comparison only. Gender does not affect the EcoPulse score."
            )


            if not gender_filter:
                st.warning(
                    "Please select at least one **gender category** to continue with the analysis."
                )
                st.stop()


            view_options = [
                "Overall ecosystem stress",
                "Juvenile sensitivity focus",
                "High contamination focus"
            ]

            view_mode = st.radio(
                "Analysis view",
                view_options,
                index=view_options.index(
                    tab_params.get("view_mode", view_options[0])
                )
            )
            
            tab_params["tissue"] = tissue
            tab_params["year"] = year
            tab_params["maturity_labels"] = maturity_labels
            tab_params["gender_filter"] = gender_filter
            tab_params["view_mode"] = view_mode

            # Finally save back to session state
            st.session_state.params[TAB_NAME] = tab_params
            

        with st.expander("ℹ️ About biological factors"):
            st.markdown("""
            <div style="font-size:18px; line-height:1.5;"></br>
            - Maturity stage reflects physiological development and exposure potential</br></br>    
            - Filtering by maturity helps avoid comparing juveniles and spawning adults directly</br></br>    
            - Labels are adapted from Lipinski et al. for interpretability </br></br>   
            - Gender is shown for <b>contextual comparison only</b></br></br>    
            - EcoPulse scores are <b>not adjusted by sex</b></br></br>    
            - Observed differences may reflect life-history stage rather than ecosystem condition
            </div>
            """, unsafe_allow_html=True)

        st.info("""
        EcoPulse views change **how results are interpreted**, not how they are calculated.
        Model structure and assumptions remain fixed for consistency and defensibility.
        """)

        
        # Convert selected labels back to numeric levels
        maturity_levels = [
            k for k, v in MATURITY_MAP.items() if v in maturity_labels
        ]


        # --- Divider Line ---
        st.sidebar.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

        # Capture the inputs (example)
        inputs_to_save = {
            "tissue": st.session_state.params[TAB_NAME].get("tissue"),
            "year": st.session_state.params[TAB_NAME].get("year"),
            "maturity_labels": st.session_state.params[TAB_NAME].get("maturity_labels"),
            "gender_filter": st.session_state.params[TAB_NAME].get("gender_filter"),
            "view_mode": st.session_state.params[TAB_NAME].get("view_mode")
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


    # -----------------------------
    # Apply filters
    # -----------------------------
    subset = df[
        (df["Year"] == year) &
        (df["Tissue"] == tissue) &
        (df["Maturity_level"].isin(maturity_levels)) &
        (df["Gender_label"].isin(gender_filter))
    ]

    if subset.empty:
        st.warning("No data available for the selected filters.")
        return


    
    # -----------------------------
    # Compute EcoPulse Index
    # -----------------------------
    indexed = compute_ecopulse_index(subset)

    # -----------------------------
    # Apply view logic (lens, not math)
    # -----------------------------
    if view_mode == "Juvenile sensitivity focus":
        indexed = indexed[indexed["Maturity_level"] <= 2]

    elif view_mode == "High contamination focus":
        threshold = indexed["pollution_score"].quantile(0.75)
        indexed = indexed[indexed["pollution_score"] >= threshold]

    # NEW SAFETY CHECK
    if indexed.empty:
        st.warning(
            "⚠️ The selected **view mode** combined with the current filters produced **no available data**.\n\n"
            "Try adjusting the **year, tissue, maturity stage, gender filter, or analysis view**."
        )
        return

    # Data aggregation before plotting
    spatial_summary = (
        indexed
        .groupby(["longitude_dd", "latitude_dd"], as_index=False)
        .agg(
            EcoPulse_mean=("EcoPulse", "mean"),
            n_samples=("EcoPulse", "count")
        )
    )

    # Inform user if few points are visible
    if len(spatial_summary) <= 2:
        st.info(
            "Only a small number of sampling locations are visible under the current filter configuration."
        )

    # Round for clean visualization
    spatial_summary["EcoPulse_mean"] = spatial_summary["EcoPulse_mean"].round(2)
    
    custom_scale = [
    [0.0, "red"],   # lowest value
    [0.33, "orange"],
    [0.66, "yellow"],
    [1.0, "green"]      # highest value
]


    # -----------------------------
    # Spatial visualization
    # -----------------------------
    fig = px.scatter(
        spatial_summary,
        x="longitude_dd",
        y="latitude_dd",
        color="EcoPulse_mean",
        size="n_samples",
        color_continuous_scale=custom_scale,
        range_color=[0, 1],
        labels={
            "EcoPulse_mean": "EcoPulse Index",
            "longitude_dd": "Longitude (decimal degrees)",
            "latitude_dd": "Latitude (decimal degrees)",
            "n_samples": "Number of samples"
        },
        title= "EcoPulse Index by Sampling Location"
    )


    fig.update_layout(
    coloraxis_colorbar=dict(
        title="EcoPulse Index",
        tickvals=[0.0, 0.33, 0.66, 1.0],
        ticktext=[
            "0.0  ┤ High stress (Red)",
            "0.33 ┤ Moderate stress (Orange)",
            "0.66 ┤ Moderate resilience (Yellow)",
            "1.0  ┤ High resilience (Green)"
        ],
        ticks="outside",
        ticklabelposition="outside",
        len=0.8,
        thickness=18
    ),
    font=dict(family="monospace")
    )

    st.plotly_chart(fig, use_container_width=True)

    

      # ---------------- Snapshot ----------------
    snapshot_inputs = {
        "tissue": tissue,
        "maturity_levels": maturity_levels,
        "maturity_labels": maturity_labels
    }

    # ---------------- Notes ----------------
    with st.sidebar:
        notes_panel("Disruption Dynamics", snapshot_inputs)

    # -----------------------------
    # Executive interpretation
    # -----------------------------
    with st.expander("🧭 Executive Interpretation"):
        st.markdown(
            generate_ecopulse_insights(
                indexed,
                year,
                tissue,
                view_mode,
                maturity_levels,
                gender_filter
            )
        )



    # -----------------------------
    # Transition Message
    # -----------------------------

    st.markdown(
        """
        <div style='text-align:center; margin-top: 30px;'>
            <span style='color:#39FF14; font-weight:bold; font-size:28px;'>
                🌿 We’ve assessed ecosystem condition across the region — but how resilient are these patterns under real-world disruption? 
                Visit the Disruption Dynamics tab to explore how marine pollution and ecosystem health shifted during the pandemic period.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
