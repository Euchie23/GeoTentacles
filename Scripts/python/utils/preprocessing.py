import pandas as pd
import numpy as np
import re
import base64
from pathlib import Path
import streamlit as st


# --------------------------------------------------
# Coordinate utilities
# --------------------------------------------------

def dms_to_dd(value):
    """
    Convert strings like 60°51'W or 49°42'S to decimal degrees
    """
    if pd.isna(value):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    match = re.match(r"(\d+)[°](\d+)'([NSEW])", str(value))
    if not match:
        return None

    degrees, minutes, direction = match.groups()
    dd = float(degrees) + float(minutes) / 60

    if direction in ["S", "W"]:
        dd *= -1

    return dd


def convert_coordinates(df):
    if "longitude_dd" not in df.columns:
        df["longitude_dd"] = df["Longitude"].apply(dms_to_dd)

    if "latitude_dd" not in df.columns:
        df["latitude_dd"] = df["Latitude"].apply(dms_to_dd)

    return df



# --------------------------------------------------
# Pollution concentration handling
# --------------------------------------------------

def handle_detection_limits(df, concentration_col="concentration", status_col="status"):
    """
    Convert BLOD / BLOQ to numeric values.
    Strategy:
    - BLOD -> 0
    - BLOQ -> 0.5 * min detected value for that pollutant
    """

    df = df.copy()

    df[concentration_col] = pd.to_numeric(df[concentration_col], errors="coerce")

    for pollutant in df["pollutant"].unique():
        mask = df["pollutant"] == pollutant
        detected = df.loc[mask & df[concentration_col].notna(), concentration_col]

        if detected.empty:
            continue

        half_lod = detected.min() * 0.5

        df.loc[mask & (df[status_col] == "BLOQ"), concentration_col] = half_lod
        df.loc[mask & (df[status_col] == "BLOD"), concentration_col] = 0

    return df


# --------------------------------------------------
# Aggregation utilities
# --------------------------------------------------

def aggregate_pollution(
    df,
    group_cols=("Year", "latitude_dd", "longitude_dd", "Tissue"),
    agg_func="mean"
):
    """
    Aggregate pollution concentrations spatially & temporally.
    """

    agg_df = (
        df
        .groupby(list(group_cols) + ["pollutant"], as_index=False)
        .agg({"concentration": agg_func})
    )

    return agg_df


def pivot_pollutants(df):

    """
    Pivot pollutants into wide format for ML models.
    """
    # Pivot pollutants as usual
    pivoted = df.pivot_table(
        index=["Year", "Latitude", "Longitude", "Tissue"],
        columns="pollutant",
        values="concentration"
    ).reset_index()

    # Keep other features from original df
    features_to_keep = [
        "Industrial_Pressure",
        "Agricultural_Pressure",
        "SqCatch_Kg",
        "WaterTemp",
        "Depth",
        "SSH",
        "Chlor_a_mg_m3",
        "SqCatch_Kg_lag1",
        "WaterTemp_lag1",
        "SSH_lag1",
        "Chlor_a_mg_m3_lag1"
    ]

    for f in features_to_keep:
        if f in df.columns:
            pivoted[f] = df[f]

    return pivoted

# --------------------------------------------------
# Fishing activity preprocessing
# --------------------------------------------------

def preprocess_fishing_data(df):
    df = df.copy()

    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

    return df


# --------------------------------------------------
# Master preprocessing pipeline
# --------------------------------------------------

def preprocess_pollution_data(df, env_df=None):
    #df = convert_coordinates(df)
    df = handle_detection_limits(df)

    if env_df is not None:
        df = df.merge(env_df, on=["Year", "Month"], how="left")

    return df


# --------------------------------------------------
# Confidence Tier Integration
# --------------------------------------------------

CONFIDENCE_TIERS = {
    "High confidence": [
        "Metal_B",
        "Metal_E",
        "Organic_B"
    ],

    "Moderate screening": [
        "Metal_A",
        "Metal_C",
        "Metal_F",
        "Metal_G",
        "Organic_C"
    ],

    "Exploratory": [
        "Metal_D",
        "Metal_H",
        "Organic_A",
        "Organic_D"
    ],

    "Insufficient data": [
        "Metal_I",
        "Metal_J"
    ]
}


def get_confidence_label(pollutant):
    for tier, pollutants in CONFIDENCE_TIERS.items():
        if pollutant in pollutants:
            return tier
    return "Standard"



#ICON_DIR = Path(__file__).parent.parent / "assets" / "icons"
# Base directory is where app.py lives
BASE_DIR = Path(__file__).resolve().parents[1]

# Path to the icon
ICON_DIR = BASE_DIR / "assets" / "icons" 

def get_pollutant_icons(pollutant_name):
    icons = []
    for i in range(1, 4):
        path = ICON_DIR / f"{pollutant_name}{i}.png"
        if path.exists():
            icons.append(path)
    fallback = ICON_DIR / f"{pollutant_name}.png"
    if not icons and fallback.exists():
        icons.append(fallback)
    return icons

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def render_pollutant_header(pollutant_name, size=50):
    icons = get_pollutant_icons(pollutant_name)
    if not icons:
        st.markdown(
            f"<h2 style='color:#39FF14; text-align:center;'>{pollutant_name}</h2>",
            unsafe_allow_html=True
        )
        return

    icons_html = ""
    for icon in icons:
        encoded = image_to_base64(icon)
        icons_html += f"<img src='data:image/png;base64,{encoded}' width='{size}' style='margin-right:4px;'/>"

    st.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:center;
            align-items:center;
            gap:4px;
        ">
            {icons_html}
            <span style="color:#39FF14; font-size:32px; font-weight:bold;">{pollutant_name}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------
# CSS to style the expander label
# ------------------------------
st.markdown("""
<style>
/* Target all Streamlit expanders */
button[data-baseweb="accordion"] {
    font-size: 28px !important;     /* bigger text */
    color: #39FF14 !important;      /* neon green */
    font-weight: bold !important;   /* bold text */
}

/* Make the little arrow also neon green */
button[data-baseweb="accordion"] svg {
    fill: #39FF14 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Your source legend expander
# ------------------------------
# Update SOURCE_ICONS to store full Paths using ICON_DIR
SOURCE_ICONS = {
    "Industrial / Manufacturing": ICON_DIR / "Metal_A1.png",
    "Mining": ICON_DIR / "Metal_A.png",
    "Pharmaceutical": ICON_DIR / "Metal_H2.png",
    "Agricultural": ICON_DIR / "Metal_G2.png",
}

def render_source_legend():
    with st.expander("💡 Curious where this pollutant comes from? Click to find out!", expanded=False):
        for label, icon_path in SOURCE_ICONS.items():
            cols = st.columns([1, 5])
            with cols[0]:
                if icon_path.exists():
                    encoded = image_to_base64(icon_path)
                    st.markdown(
                        f"<img src='data:image/png;base64,{encoded}' width='24'>",
                        unsafe_allow_html=True
                    )
                else:
                    st.warning(f"Icon not found: {icon_path}")
            with cols[1]:
                st.markdown(
                    f"<p style='margin:0; font-size:18px;'>{label}</p>",
                    unsafe_allow_html=True
                )
