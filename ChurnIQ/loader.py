# ─────────────────────────────────────────────
# loader.py  —  model & dataset loading
# ─────────────────────────────────────────────
import os
import pickle
import pandas as pd
import streamlit as st
 
 
@st.cache_resource
def load_model():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model    = pickle.load(open(os.path.join(BASE_DIR, "model", "churn_model.pkl"), "rb"))
    encoders = pickle.load(open(os.path.join(BASE_DIR, "model", "encoders.pkl"),    "rb"))
    return model, encoders
 
 
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return pd.read_csv(os.path.join(BASE_DIR, "data", "Churn.csv"))
 