# app.py  —  entry point
import os
import streamlit as st
 
from loader import load_model, load_data
from components.login     import show_login
from components.home      import show_home
from components.predict   import show_predict
from components.analytics import show_analytics
from components.about     import show_about
 
# ── Page config ──────────────────────────────
st.set_page_config(
    page_title="ChurnIQ · Dashboard",
    page_icon="📊",
    layout="wide",
)
 
# ── Inject CSS (absolute path fix) ───────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(BASE_DIR, "assets", "style.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
 
# ── Auth gate ────────────────────────────────
if "login" not in st.session_state:
    st.session_state["login"] = False
 
if not st.session_state["login"]:
    show_login()
    st.stop()
 
# ── Load data & model ────────────────────────
model, encoders = load_model()
df = load_data()
 
total    = len(df)
churned  = df[df["Churn"] == "Yes"].shape[0]
retained = total - churned
rate     = churned / total * 100
avg_ten  = df["tenure"].mean()
 
# ── Top nav bar ──────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">
        <span class="logo-dot"></span> ChurnIQ
    </div>
    <span style="font-size:13px; color:#aaa;">Customer Churn Intelligence</span>
</div>
""", unsafe_allow_html=True)
 
menu = st.radio(
    "", ["🏠  Home", "🔍  Predict", "📊  Analytics", "👤  About"],
    horizontal=True, label_visibility="collapsed",
)
st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
 
# ── Route to page ────────────────────────────
if   menu == "🏠  Home":      show_home(total, rate, retained, avg_ten)
elif menu == "🔍  Predict":   show_predict(model, encoders)
elif menu == "📊  Analytics": show_analytics(df, total, churned, retained, rate)
elif menu == "👤  About":     show_about()