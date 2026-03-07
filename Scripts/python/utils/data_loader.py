import pandas as pd
import streamlit as st
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

@st.cache_data
def load_pollution_data():
    return pd.read_csv(DATA_DIR / "squid_pollution.csv", encoding="utf-8")


# @st.cache_data
# def load_fishing_data():
#     return pd.read_csv(DATA_DIR / "squid_catch_env.csv")


# @st.cache_data
# def load_pressure_data():
#     return pd.read_csv(DATA_DIR / "pressure_indices_monthly.csv")

@st.cache_data
def load_modeling_dataset():
    return pd.read_csv(DATA_DIR / "final_modeling_dataset.csv", encoding="utf-8")
