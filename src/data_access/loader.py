"""Data loading and verification functions."""
import os
import pandas as pd
import streamlit as st
from src.config.constants import REQUIRED_COLUMNS, ENHANCED_COLUMNS
from src.config.settings import DATA_FILE

@st.cache_data(show_spinner=False)
def load_data(filepath=None):
    if filepath is None:
        filepath = DATA_FILE
    try:
        df = pd.read_csv(filepath)
    except Exception:
        try:
            df = pd.read_csv("disease_dataset.csv")
        except Exception:
            st.error("⚠️ Could not read disease_dataset.csv.")
            st.stop()
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        st.error(f"Missing required columns: {', '.join(missing)}")
        st.stop()
    for col in ENHANCED_COLUMNS:
        if col not in df.columns:
            df[col] = None
    return df
