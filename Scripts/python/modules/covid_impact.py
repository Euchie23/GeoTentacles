import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

from utils.data_loader import load_modeling_dataset
from utils.preprocessing import convert_coordinates
from utils.index_utils import compute_ecopulse_index


# ======================================================
# Narrative generators
# ======================================================

def generate_covid_insights(pre_df, post_df, tissue):
    pre_mean = pre_df["EcoPulse"].mean()
    post_mean = post_df["EcoPulse"].mean()
    delta = post_mean - pre_mean

    pre_pressure = pre_df[["Industrial_Pressure", "Agricultural_Pressure"]].mean().mean()
    post_pressure = post_df[["Industrial_Pressure", "Agricultural_Pressure"]].mean().mean()
    pressure_delta = post_pressure - pre_pressure

    eco_direction = (
        "improved" if delta > 0.05
        else "declined" if delta < -0.05
        else "remained relatively stable"
    )

    pressure_direction = (
        "decreased" if pressure_delta < -0.05
        else "increased" if pressure_delta > 0.05
        else "remained relatively stable"
    )

    return f"""
**What is being compared**

This analysis contrasts marine ecosystem condition **before and after COVID-related disruptions**
using the EcoPulse Index for **{tissue} tissue samples**.

---

**Observed ecosystem response**

- Average ecosystem condition **{eco_direction}**
- Pre-COVID mean EcoPulse: **{pre_mean:.3f}**
- Post-COVID mean EcoPulse: **{post_mean:.3f}**

---

**Human-pressure context**

- Combined industrial and agricultural pressure **{pressure_direction}**
- Pressure indicators represent **relative intensity**, not emissions or loads

---

**Important limitations**

⚠ Results show **associations, not causation**  
⚠ Pressure indicators are proxies  
⚠ Sampling coverage differs by year  
⚠ Interpretation is valid at **regional scale**, not individual sites  
⚠ Pre- and post-COVID periods cover different numbers of years (pre: 2019 only; post: 2020–2021), which may slightly bias mean comparisons (mainly when 2020 is included) or dampen/average out year-to-year fluctuations. 
"""


def generate_covid_conclusion(pre_df, post_df):
    pre_mean = pre_df["EcoPulse"].mean()
    post_mean = post_df["EcoPulse"].mean()
    delta = post_mean - pre_mean

    if delta > 0.05:
        outcome = "improved"
        framing = "suggesting a positive ecosystem response during the COVID period."
    elif delta < -0.05:
        outcome = "declined"
        framing = "indicating potential ecosystem stress or delayed ecological response."
    else:
        outcome = "remained broadly stable"
        framing = "indicating relative ecosystem stability during the COVID period."

    pre_pressure = pre_df[["Industrial_Pressure", "Agricultural_Pressure"]].mean().mean()
    post_pressure = post_df[["Industrial_Pressure", "Agricultural_Pressure"]].mean().mean()
    pressure_delta = post_pressure - pre_pressure

    if pressure_delta < -0.05:
        pressure_text = "Human pressure indicators decreased during the COVID period."
    elif pressure_delta > 0.05:
        pressure_text = "Human pressure indicators increased during the COVID period."
    else:
        pressure_text = "Human pressure indicators remained relatively stable during the COVID period."

    return f"""
---

### **Overall conclusion for this selection**

For the selected scenario, marine ecosystem condition **{outcome}**
from pre-COVID (mean EcoPulse = {pre_mean:.3f}) to post-COVID
(mean EcoPulse = {post_mean:.3f}), {framing}

{pressure_text}

These results suggest that observed changes likely reflect a combination of
**human activity dynamics, ecological buffering, and natural variability**.
This module is intended for **decision support and comparative analysis**, not
formal impact attribution.

---
"""


# ======================================================
# Main render function
# ======================================================

def render():

    # ---------------------------------------------------
    # TAB CONFIG
    # ---------------------------------------------------

    TAB_NAME = "Disruption Dynamics"


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

    st.title("🔬 Disruption Dynamics — COVID Impact on Marine Health")

    st.markdown("""
This module evaluates how marine ecosystem condition changed during
**COVID-related disruptions in human activity**, using integrated ecological
and pressure indicators.

The focus is on **system sensitivity**, not direct causation.
""")

    # -----------------------------
    # Load & validate data
    # -----------------------------
    df = load_modeling_dataset()
    df = convert_coordinates(df)

    required_cols = {"Industrial_Pressure", "Agricultural_Pressure"}
    missing = required_cols - set(df.columns)
    if missing:
        st.error(
            f"Missing required pressure indicators: {missing}. "
            "COVID impact analysis requires pressure-enabled data."
        )
        return

    # -----------------------------
    # Sidebar controls
    # -----------------------------
    with st.sidebar:
        st.subheader("Scenario Controls")

        # At the top of render():
        tab_params = st.session_state.params.get(TAB_NAME, {})

        tissue_options = sorted(df["Tissue"].unique())

        tissue = st.selectbox(
            "Tissue type",
            tissue_options,
            index=tissue_options.index(
                tab_params.get("tissue", tissue_options[0])
            )
        )


        include_2020 = st.checkbox(
            "Include 2020 (pandemic year)",
            value=tab_params.get("include_2020", True),
            help="2020 represents active COVID conditions in this dataset"
        )

        tab_params["tissue"] = tissue
        tab_params["include_2020"] = include_2020

        # Finally save back to session state
        st.session_state.params[TAB_NAME] = tab_params

         # --- Divider Line ---
        st.sidebar.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

        # Capture the inputs (example)
        inputs_to_save = {
            "tissue": st.session_state.params[TAB_NAME].get("tissue"),
            "include_2020": st.session_state.params[TAB_NAME].get("include_2020")
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
    # Define comparison windows
    # -----------------------------
    pre_years = [2019]
    post_years = [2020, 2021] if include_2020 else [2021]

    subset = df[df["Tissue"] == tissue]
    indexed = compute_ecopulse_index(subset)

    pre_df = indexed[indexed["Year"].isin(pre_years)]
    post_df = indexed[indexed["Year"].isin(post_years)]

   # -----------------------------
    # Handle missing pre-COVID data
    # -----------------------------
    if pre_df.empty:
        st.warning(f"No pre-COVID data available for **{tissue}** tissue. "
                "Comparison cannot be performed.")
        return

    if post_df.empty:
        st.warning(f"No post-COVID data available for **{tissue}** tissue. "
                "Comparison cannot be performed.")
        return

    # -----------------------------
    # Summary comparison plot
    # -----------------------------
    summary_df = pd.DataFrame({
        "Period": ["Pre-COVID", "Post-COVID"],
        "EcoPulse": [
            pre_df["EcoPulse"].mean(),
            post_df["EcoPulse"].mean()
        ]
    })

    fig = px.bar(
        summary_df,
        x="Period",
        y="EcoPulse",
        color="Period",
        title="Average Ecosystem Condition Before vs After COVID
    )
    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Pressure diagnostics
    # -----------------------------
    st.subheader("📊 Human Pressure Diagnostics")

    pressure_summary = pd.DataFrame({
        "Period": ["Pre-COVID", "Post-COVID"],
        "Industrial Pressure": [
            pre_df["Industrial_Pressure"].mean(),
            post_df["Industrial_Pressure"].mean()
        ],
        "Agricultural Pressure": [
            pre_df["Agricultural_Pressure"].mean(),
            post_df["Agricultural_Pressure"].mean()
        ],
    })

    st.dataframe(pressure_summary.round(4), use_container_width=True)

    fig_pressure = px.bar(
        pressure_summary.melt(
            id_vars="Period",
            var_name="Pressure Type",
            value_name="Mean Intensity"
        ),
        x="Period",
        y="Mean Intensity",
        color="Pressure Type",
        barmode="group",
        title="Relative Change in Human Pressure Indicators"
    )
    st.plotly_chart(fig_pressure, use_container_width=True)



    # -----------------------------
    # Dynamic interpretation
    # -----------------------------
    with st.expander("🧭 Executive Interpretation - Click to see full analysis"):
        st.markdown(generate_covid_insights(pre_df, post_df, tissue))
        st.markdown(generate_covid_conclusion(pre_df, post_df))



    # -----------------------------
    # Transition Message
    # -----------------------------

    st.markdown(
        """
        <div style='text-align:center; margin-top: 30px;'>
            <span style='color:#39FF14; font-weight:bold; font-size:28px;'>
                🌐 We’ve explored measurements, spatial patterns, predictions, ecosystem health, and disruption effects — so what overall story emerges? 
                Head to the Logbook tab to review your saved insights and consolidate your findings into a clear strategic conclusion.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
