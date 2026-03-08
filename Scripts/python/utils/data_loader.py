import pandas as pd
import streamlit as st
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]  # up 3 levels from utils/data_loader.py
DATA_DIR = REPO_ROOT / "data" 

@st.cache_data
def load_pollution_data():
    return pd.read_csv(DATA_DIR / "raw"/ "squid_pollution.csv", encoding="utf-8")

@st.cache_data
def load_modeling_dataset():
    return pd.read_csv(DATA_DIR /"processed" / "final_modeling_dataset.csv", encoding="utf-8")
