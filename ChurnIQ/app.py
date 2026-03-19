import os
import streamlit as st
 
from loader import load_model, load_data
from components.auth      import show_auth, is_logged_in, current_user, logout
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
 
# ── Inject CSS ───────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(BASE_DIR, "assets", "style.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
 
# ── Auth gate ────────────────────────────────
if not is_logged_in():
    show_auth()
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
st.markdown(f"""
<div class="topbar">
    <div class="topbar-logo">
        <span class="logo-dot"></span> ChurnIQ
    </div>
    <div style="display:flex; align-items:center; gap:16px;">
        <span style="font-size:13px; color:#aaa;">👤 {current_user()}</span>
    </div>
</div>
""", unsafe_allow_html=True)
 
# ── Nav menu + logout ─────────────────────────
col_menu, col_logout = st.columns([5, 1])
with col_menu:
    menu = st.radio(
        "", ["🏠  Home", "🔍  Predict", "📊  Analytics", "👤  About"],
        horizontal=True, label_visibility="collapsed",
    )
with col_logout:
    if st.button("Sign out", use_container_width=True):
        logout()
 
st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
 
# ── Route to page ────────────────────────────
if   menu == "🏠  Home":      show_home(total, rate, retained, avg_ten)
elif menu == "🔍  Predict":   show_predict(model, encoders)
elif menu == "📊  Analytics": show_analytics(df, total, churned, retained, rate)
elif menu == "👤  About":     show_about()