import streamlit as st
import pandas as pd
import numpy as np


from pathlib import Path
from utils.data_loader import load_modeling_dataset
from utils.preprocessing import pivot_pollutants, get_confidence_label, convert_coordinates, render_pollutant_header, render_source_legend
from utils.model_loader import list_available_models, load_model
from utils.model_cards import describe_model

import folium
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import box
from datetime import datetime


# ======================================================
# Regulatory reference limits
# ======================================================

METAL_RML = {
    "Metal_A": 100,
    "Metal_B": 0.0016,
    "Metal_C": 0.05,
    "Metal_D": 30,
    "Metal_E": 30,
    "Metal_F": 0.01,
    "Metal_G": 2,
    "Metal_H": 0.1,
    "Metal_I": 0.00001,
    "Metal_J": 8,
}

ORGANIC_RML = {
    "Organic_A": 470,
    "Organic_B": 50,
    "Organic_C": 0.01,
    "Organic_D": 40,
}


# ======================================================
# Feature sets (MODEL CONTRACT)
# ======================================================

FEATURE_SETS = {
    "environment_only": [
        "WaterTemp", "Depth", "SSH", "Chlor_a_mg_m3",
        "WaterTemp_lag1", "SSH_lag1", "Chlor_a_mg_m3_lag1",
    ],

    "env_plus_catch": [
        "WaterTemp", "Depth", "SSH", "Chlor_a_mg_m3",
        "WaterTemp_lag1", "SSH_lag1", "Chlor_a_mg_m3_lag1",
        "SqCatch_Kg", "SqCatch_Kg_lag1",
    ],

    "full_pressures": [
        "WaterTemp", "Depth", "SSH", "Chlor_a_mg_m3",
        "WaterTemp_lag1", "SSH_lag1", "Chlor_a_mg_m3_lag1",
        "SqCatch_Kg", "SqCatch_Kg_lag1",
        "Industrial_Pressure", "Agricultural_Pressure",
    ],

    "full_pressures_plus_censoring": [
        "WaterTemp", "Depth", "SSH", "Chlor_a_mg_m3",
        "WaterTemp_lag1", "SSH_lag1", "Chlor_a_mg_m3_lag1",
        "SqCatch_Kg", "SqCatch_Kg_lag1",
        "Industrial_Pressure", "Agricultural_Pressure",
        "is_censored",
    ],
}


# ======================================================
# Risk classification
# ======================================================

def classify_risk(r):
    if r < 0.5:
        return "Low"
    elif r < 1.0:
        return "Moderate"
    elif r < 2.0:
        return "High"
    else:
        return "Critical"


RISK_COLORS = {
    "Low": "#2ECC71",
    "Moderate": "#F1C40F",
    "High": "#E67E22",
    "Critical": "#E74C3C",
}

# ======================================================
# Plain-language executive summary 
# ======================================================

def generate_toxic_tide_insights(metrics, pollutant, df):
    r2 = metrics.get("R2_log", None)
    rmse = metrics.get("RMSE_log", None)

    exceed_pct = (df["risk_ratio"] > 1).mean() * 100
    confidence = get_confidence_label(pollutant)

    # ----------------------------------
    # Confidence-based reliability framing
    # ----------------------------------
    if confidence == "High confidence":
        reliability_text = (
            "The model demonstrates consistent performance and captures meaningful "
            "relationships between environmental conditions and observed concentrations. "
            "Results are suitable for identifying broad spatial patterns and relative differences."
        )
        limitation_text = (
            "While overall patterns are reliable, individual location estimates may still "
            "be affected by local factors not represented in the data."
        )

    elif confidence == "Moderate screening":
        reliability_text = (
            "The model identifies indicative spatial signals that are useful for screening "
            "and prioritization, but with notable uncertainty in magnitude and local detail."
        )
        limitation_text = (
            "Model performance varies across locations, and predictions should be interpreted "
            "as relative indicators rather than precise estimates."
        )

    elif confidence == "Exploratory":
        reliability_text = (
            "The model outputs are exploratory and reflect weak or unstable relationships "
            "in the available data."
        )
        limitation_text = (
            "Results are sensitive to data limitations and should be used only to guide "
            "future data collection or exploratory analysis."
        )

    else:  # Insufficient data
        reliability_text = (
            "The available data and model performance do not support reliable spatial "
            "interpretation for this pollutant."
        )
        limitation_text = (
            "Patterns shown may reflect noise or data artefacts rather than real-world behaviour."
        )

    # ----------------------------------
    # Risk signal phrasing (tier-aware)
    # ----------------------------------
    if confidence in ["High confidence", "Moderate screening"]:
        if exceed_pct > 75:
            risk_text = (
                "A large proportion of mapped locations show model-estimated concentrations "
                "above reference guideline levels, indicating areas that may warrant closer attention."
            )
        elif exceed_pct > 25:
            risk_text = (
                "Some locations show model-estimated concentrations above reference guideline levels."
            )
        else:
            risk_text = (
                "Only limited areas show model-estimated concentrations above reference guideline levels."
            )
    else:
        risk_text = (
            "Apparent exceedances reflect model-based estimates only and should not be interpreted "
            "as confirmed guideline exceedances."
        )

    # ----------------------------------
    # Final executive narrative
    # ----------------------------------
    return f"""
    **What this analysis indicates**

    This map combines predictive modeling with environmental conditions and
    human-pressure indicators to highlight **areas where {pollutant} may be elevated
    relative to typical background levels**.

    The results are intended to support **early-stage screening and spatial
    prioritization**, not definitive assessment.

    ---

    **Confidence context**

    - Confidence tier: **{confidence}**
    - {reliability_text}

    ---

    **Observed risk signal (screening-level)**

    - {risk_text}

    These patterns represent **model-based estimates**, not direct field measurements.

    ---

    **Important limitations**

    ⚠ {limitation_text}  
    ⚠ Absolute concentration values may be uncertain, particularly at local scales  
    ⚠ Results should **not** be used for regulatory enforcement or compliance decisions  

    ---

    **Appropriate uses of this analysis**

    ✔ Identifying locations for follow-up monitoring  
    ✔ Prioritizing sampling or mitigation efforts  
    ✔ Supporting hypothesis generation and planning  

    This output is best interpreted as a **decision-support and screening tool**.
    """

# ======================================================
# MAIN TAB
# ======================================================

def render():

    # ---------------------------------------------------
    # TAB CONFIG
    # ---------------------------------------------------

    TAB_NAME = "Toxic Tide Mapping"

    DEFAULT_MAP_CENTER = [-48.0, -55.0]
    DEFAULT_MAP_ZOOM = 4


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

    # Initialize flag at top of render_overview()
    # if "just_saved_note" not in st.session_state:
    #     st.session_state.just_saved_note = False

    if "force_map_view" not in st.session_state:
        st.session_state.force_map_view = False


    st.title("🌊 Toxic Tide Mapping — Predictive Pollution Risk")

    # --------------------------------------------------
    # INTRO — PURPOSE & LAYERS
    # --------------------------------------------------

    st.markdown("""
    This module estimates spatial pollution risk using machine-learning models
    informed by oceanography, fisheries activity, and upstream human pressures.
    
    Predictions are intended for screening and prioritization, not regulatory
    confirmation or site-level compliance decisions.

    The analysis progresses through four interpretive layers:
    1. **Prediction** — Where concentrations may be elevated  
    2. **Risk Translation** — How predictions compare to safety thresholds  
    3. **Attribution** — What may be driving elevated risk  
    4. **Decision Support** — How results should be interpreted in practice
    """)
    st.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

    # --------------------------------------------------
    # DATA
    # --------------------------------------------------

    df = load_modeling_dataset()
    df = convert_coordinates(df)
    available_models = list_available_models()

    # --------------------------------------------------
    # SIDEBAR — MODEL SELECTION
    # --------------------------------------------------

    with st.sidebar:
        st.subheader("Prediction Controls")

        with st.expander("🌊 Expand to adjust Prediction Controls", expanded=False):


            tab_params = st.session_state.params.setdefault(TAB_NAME, {})

            pollutant_options = sorted(available_models.keys())
        
            pollutant = st.selectbox(
                "Target Pollutant",
                pollutant_options,
                index=pollutant_options.index(
                    tab_params.get("pollutant", pollutant_options[0])
                )
            )

            model_type_options = available_models[pollutant]

            model_type = st.selectbox(
                "Model configuration",
                model_type_options,
                index=model_type_options.index(
                    tab_params.get("model_type", model_type_options[0])
                )
            )

            tab_params["pollutant"] = pollutant
            tab_params["model_type"] = model_type

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
            "pollutant": st.session_state.params[TAB_NAME].get("pollutant"),
            "model_type": st.session_state.params[TAB_NAME].get("model_type"),
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


    # --------------------------------------------------
    # FILTER FOR PRESSURE MODELS
    # --------------------------------------------------

    if model_type.startswith("full_pressures"):
        df = df.dropna(subset=["Industrial_Pressure", "Agricultural_Pressure"])

    # --------------------------------------------------
    # FILTER DATA FOR SELECTED POLLUTANT
    # --------------------------------------------------

    model_df = df[df["pollutant"] == pollutant].copy()

    if model_df.empty:
        st.warning("No data available for selected pollutant.")
        return


    # --------------------------------------------------
    # MODEL PERFORMANCE
    # --------------------------------------------------

    BASE_DIR = Path(__file__).resolve()

    REPO_ROOT = BASE_DIR.parents[3]  
    # modules -> python -> Scripts -> repo root
    
    OUTPUT_FILE = REPO_ROOT / "outputs" / "marine_toxic_tide" / "model_comparison_table.csv"

    if not OUTPUT_FILE.exists():
        st.error(f"Metrics file not found: {OUTPUT_FILE}")
        return
    
    metrics_df = pd.read_csv(OUTPUT_FILE)

    # metrics_df = pd.read_csv("output/model_comparison_table.csv")
    filtered = metrics_df.query("pollutant == @pollutant and model == @model_type")
    if filtered.empty:
        st.error("No performance metrics found for this configuration.")
        return
    metrics = filtered.iloc[0]

    st.subheader("🔍 Layer 1 — Model & Credibility")

    c1, c2, c3 = st.columns(3)
    c1.metric("R² (log scale)", f"{metrics['R2_log']:.3f}")
    c2.metric("RMSE (log scale)", f"{metrics['RMSE_log']:.3f}")
    c3.metric("Model type", model_type)
    

    st.markdown(f"**Confidence tier:** {get_confidence_label(pollutant)}")

    # --------------------------------------------------
    # PREDICTION
    # --------------------------------------------------

    model = load_model(pollutant, model_type)
    #features = FEATURE_SETS[model_type]
    features = FEATURE_SETS.get(model_type)
    if not features:
        st.error(f"No feature set for model: {model_type}")
        return
    
    card = describe_model(model_type)


    st.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

    render_pollutant_header(pollutant)

    st.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

    st.markdown(card["description"])


    # missing = [f for f in features if f not in model_df.columns]
    # if missing:
    #     st.error(f"Missing features: {missing}")
    #     return

    #model_df["predicted"] = model.predict(model_df[features])
    missing = [f for f in features if f not in model_df.columns]
    if missing:
        st.error(f"Missing features: {missing}")
        return
    
    X = model_df[features].astype(float).to_numpy()
    
    log_preds = model.predict(X)
    log_preds = np.clip(log_preds, a_min=-20, a_max=None) 
    model_df["predicted_concentration"] = np.expm1(log_preds)
    model_df["predicted_concentration"] = model_df["predicted_concentration"].clip(lower=0)

    # --------------------------------------------------
    # RISK TRANSLATION
    # --------------------------------------------------

    limit = METAL_RML.get(pollutant, ORGANIC_RML.get(pollutant, np.nan))
    if np.isnan(limit):
        st.error(f"No regulatory limit defined for {pollutant}")
        return
    model_df["risk_ratio"] = model_df["predicted_concentration"] / limit
    model_df["risk_level"] = model_df["risk_ratio"].apply(classify_risk)



    # --------------------------------------------------
    # MAP — LAYER 2
    # --------------------------------------------------
    st.subheader("🗺️ Layer 2 — Spatial Risk Screening")


    # NOTE: Coordinates will be properly parsed in preprocessing step
    # -----------------------------
    # Compute Map Center Early
    # -----------------------------
    map_df = df.dropna(subset=["longitude_dd", "latitude_dd"]).copy()

    if "current_map_center" not in st.session_state:

        if not map_df.empty:
            lat_center = map_df["latitude_dd"].mean()
            lng_center = map_df["longitude_dd"].mean()
        else:
            # Default: north of Falkland Islands, SW Atlantic
            lat_center = -48.0
            lng_center = -55.0

        #st.session_state.current_map_center = [lat_center, lng_center]
        st.session_state.current_map_center = [lat_center, lng_center]


    if map_df.empty:
        st.warning("No data available for selected filters.")
        return



    lat_center = model_df["latitude_dd"].mean()
    lon_center = model_df["longitude_dd"].mean()

    # Create the grid and join the data
    grid_size = 0.5
    minx, miny = model_df["longitude_dd"].min(), model_df["latitude_dd"].min()
    maxx, maxy = model_df["longitude_dd"].max(), model_df["latitude_dd"].max()

    polygons = []
    x = minx
    while x < maxx:
        y = miny
        while y < maxy:
            polygons.append(box(x, y, x + grid_size, y + grid_size))
            y += grid_size
        x += grid_size

    grid = gpd.GeoDataFrame({"geometry": polygons}, crs="EPSG:4326")
    points = gpd.GeoDataFrame(
        model_df,
        geometry=gpd.points_from_xy(model_df["longitude_dd"], model_df["latitude_dd"]),
        crs="EPSG:4326"
    )

    joined = gpd.sjoin(points, grid, how="left", predicate="within")

    # ⚡ Compute mean predicted & risk per grid cell
    summary = joined.groupby("index_right").agg(
       predicted_concentration =("predicted_concentration", "mean"),
        risk_ratio=("risk_ratio", "mean")
    )
    summary["risk_level"] = summary["risk_ratio"].apply(classify_risk)

    grid = grid.join(summary).dropna()

    # Friendly polygon labels
    grid["grid_label"] = [f"Grid {i+1}" for i in range(len(grid))]


    # -----------------------------
    # Render map with spinner, basemap, and tooltips
    # -----------------------------
    with st.spinner("Rendering map, please wait..."):

        m = folium.Map(
            location=DEFAULT_MAP_CENTER,  # static initial
            zoom_start=DEFAULT_MAP_ZOOM   # static initial
        )

        # Add realistic base tiles
        folium.TileLayer("Esri.WorldImagery", name="Satellite", control=True).add_to(m)
        folium.TileLayer("CartoDB.PositronOnlyLabels", name="Labels", overlay=True, control=True).add_to(m)

        # Add grid polygons with proper tooltips
        for _, row in grid.iterrows():
            tooltip_text = (
                f"{row['grid_label']}<br>"
                f"Esimated Concentration (Model-Derived): {row['predicted_concentration']:.2f} mg/kg<br>"
                f"Risk ratio: {row['risk_ratio']:.2f} (Predicted / Safety Limit)<br>"
                f"Risk level: {row['risk_level']}"
            )
            folium.GeoJson(
                row.geometry,
                name=row['grid_label'], 
                style_function=lambda f, col=RISK_COLORS[row["risk_level"]]: {
                    "fillColor": col,
                    "color": "black",
                    "weight": 0.5,
                    "fillOpacity": 0.6,
                },
                tooltip=folium.Tooltip(tooltip_text, sticky=True)
            ).add_to(m)
            

        # Layer control
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


    st.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

    # --------------------------------------------------
    # LAYER 3 — ATTRIBUTION
    # --------------------------------------------------

    st.subheader("🧩 Layer 3 — What Is Driving Risk?")

    if model_type == "environment_only":
        st.markdown("""
    **Model interpretation context**

    This model reflects **natural environmental and oceanographic variability only**.

    Observed patterns are primarily influenced by:
    - Water circulation and mixing
    - Temperature and salinity structure
    - Broad-scale natural background conditions

    Human activities are **not explicitly represented** in this model.
    """)

    elif model_type == "env_plus_catch":
        st.markdown("""
    **Model interpretation context**

    This model reflects **natural environmental conditions**, with additional context
    from biological sampling and catch-related indicators.

    Observed patterns may reflect:
    - Oceanographic variability
    - Ecosystem and food-web structure
    - Sampling and biological distribution effects

    Human pressure is **not directly modeled**, but may be indirectly reflected
    through biological signals.
    """)

    elif model_type == "full_pressures":
        st.markdown("""
    **Model interpretation context**

    This model incorporates **environmental conditions together with distance-weighted
    industrial and agricultural pressure indicators**.

    Elevated predicted risk may reflect:
    - Proximity to industrial or urban activity
    - Agricultural runoff or land-based inputs
    - Interaction between human pressures and oceanographic transport

    These results suggest **potential anthropogenic influence**, but do not establish
    direct causation.
    """)

    elif model_type == "full_pressures_plus_censoring":
        st.markdown("""
    **Model interpretation context**

    This model incorporates **environmental conditions, human-pressure indicators, and
    improved handling of low or uncertain concentration measurements**.

    Compared to other models, this approach:
    - Reduces bias from non-detects or low measurements
    - Produces more stable large-scale patterns
    - Improves reliability where data are sparse or uneven

    Elevated risk still reflects **potential combined effects** of human pressures
    and environmental transport, not confirmed sources.
    """)

        
    st.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)

# --------------------------------------------------
# LAYER 4 — ANOMALIES
# --------------------------------------------------

    st.subheader("⚠️ Layer 4 — Decision Flags")

    if "log_concentration" not in model_df.columns:
        st.warning("Skipping anomaly detection (log_concentration missing).")
        return

    # Residual-based anomaly detection
    residuals = model_df["log_concentration"] - np.log1p(model_df["predicted_concentration"])
    mad = np.median(np.abs(residuals))
    threshold = 3 * mad * 1.4826

    model_df["model_anomaly"] = residuals.abs() > threshold

    # Filter by selected pollutant (row-level, not column-level)
    anomaly_df = model_df[
        (model_df["model_anomaly"]) &
        (model_df["pollutant"] == pollutant)
    ]

    with st.expander("View flagged samples"):
        if anomaly_df.empty:
            st.success("No decision flags triggered for this pollutant.")
        else:
            st.warning(f"{len(anomaly_df)} samples flagged for further review.")

            st.dataframe(
                anomaly_df[
                    [
                        "Year",
                        "latitude_dd",
                        "longitude_dd",
                        "concentration",
                        "predicted_concentration",
                        "risk_level"
                    ]
                ].rename(columns={
                    "latitude_dd": "Latitude (decimal degrees)",
                    "longitude_dd": "Longitude (decimal degrees)",
                    "concentration": "Observed concentration",
                    "predicted_concentration": "Model-predicted concentration"
                }),
                use_container_width=True
            )

    st.markdown("<hr style='border-top: 2px solid #39FF14; margin-top: 50px 0;'>", unsafe_allow_html=True)


    # --------------------------------------------------
    # EXECUTIVE SUMMARY
    # --------------------------------------------------

    # Collapsible panel
    with st.expander("🧠 Executive Interpretation — Click to see full analysis"):
        # Your existing content goes inside the expander
        render_pollutant_header(pollutant, size=50)
        st.markdown(generate_toxic_tide_insights(metrics, pollutant, model_df))


    # -----------------------------
    # Transition Message
    # -----------------------------

    st.markdown(
    """
    <div style='text-align:center; margin-top: 30px;'>
        <span style='color:#39FF14; font-weight:bold; font-size:28px;'>
            🌐 We’ve identified where pollution risk may concentrate — but how do these projected risks translate into overall ecosystem condition? 
            Move to the EcoPulse Index tab to evaluate how contamination patterns interact with biological context to shape marine health.
        </span>
    </div>
    """,
    unsafe_allow_html=True
    )
    
