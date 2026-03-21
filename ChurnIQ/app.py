# app.py  —  entry point
import os
import streamlit as st
 
from loader import load_model, load_data
from components.auth         import show_auth, is_logged_in, current_user, logout
from components.home         import show_home
from components.predict      import show_predict
from components.analytics    import show_analytics
from components.about        import show_about
from components.smart_upload import show_smart_upload
 
# ── Page config ──────────────────────────────
st.set_page_config(
    page_title="ChurnIQ & DataLens Platform",
    page_icon="📊",
    layout="wide",
)
 
# ── Inject CSS ───────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(BASE_DIR, "assets", "style.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
 
# ── Extra CSS for mode switcher ───────────────
st.markdown("""
<style>
.mode-card {
    background: #ffffff;
    border: 1.5px solid #eaeaea;
    border-radius: 16px;
    padding: 36px 28px;
    text-align: center;
    transition: border-color 0.2s;
    cursor: pointer;
    height: 100%;
}
.mode-card:hover { border-color: #1D9E75; }
.mode-card .icon { font-size: 52px; margin-bottom: 14px; }
.mode-card .title { font-size: 22px; font-weight: 600; margin-bottom: 4px; }
.mode-card .subtitle { font-size: 12px; font-style: italic; margin-bottom: 12px; }
.mode-card .desc { font-size: 13px; color: #888; line-height: 1.7; }
.mode-card .tags { margin-top: 18px; display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; }
.tag-green { background:#E1F5EE; color:#0F6E56; padding:3px 10px; border-radius:20px; font-size:11px; }
.tag-blue  { background:#E6F1FB; color:#0C447C; padding:3px 10px; border-radius:20px; font-size:11px; }
.welcome-text {
    text-align: center;
    margin: 2.5rem 0 2rem;
}
.welcome-text h1 { font-size: 26px; font-weight: 600; color: #111; margin-bottom: 6px; }
.welcome-text p  { font-size: 15px; color: #888; }
.platform-badge {
    text-align: center;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)
 
# ── Auth gate ────────────────────────────────
if not is_logged_in():
    show_auth()
    st.stop()
 
# ── Mode state ────────────────────────────────
if "mode" not in st.session_state:
    st.session_state["mode"] = None
 
# ── Top nav bar ──────────────────────────────
if st.session_state["mode"] == "churniq":
    brand = '<span style="color:#1D9E75; font-weight:600;">ChurnIQ</span> <span style="color:#ccc; font-size:11px;">Churn Intelligence</span>'
elif st.session_state["mode"] == "datalens":
    brand = '<span style="color:#378ADD; font-weight:600;">DataLens</span> <span style="color:#ccc; font-size:11px;">Universal Analytics Studio</span>'
else:
    brand = '<span style="color:#1D9E75; font-weight:600;">ChurnIQ</span> <span style="color:#ccc; font-size:11px;">×</span> <span style="color:#378ADD; font-weight:600;">DataLens</span>'
 
st.markdown(f"""
<div class="topbar">
    <div class="topbar-logo">
        <span class="logo-dot"></span>
        <span>{brand}</span>
    </div>
    <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:13px; color:#aaa;">👤 {current_user()}</span>
    </div>
</div>
""", unsafe_allow_html=True)
 
# ── Back + Sign out row ───────────────────────
col_back, col_space, col_out = st.columns([1, 4, 1])
with col_back:
    if st.session_state["mode"] is not None:
        if st.button("← Switch tool", use_container_width=True):
            st.session_state["mode"] = None
            st.rerun()
with col_out:
    if st.button("Sign out", use_container_width=True):
        logout()
 
st.markdown("<div style='margin-top:0.3rem;'></div>", unsafe_allow_html=True)
 
# ════════════════════════════════════════════
# LANDING PAGE — mode selector
# ════════════════════════════════════════════
if st.session_state["mode"] is None:
 
    st.markdown(f"""
    <div class="welcome-text">
        <h1>Welcome back, {current_user()} 👋</h1>
        <p>Choose a tool to get started</p>
    </div>
    <div class="platform-badge">
        <span style="background:#f7f8fa; border:1px solid #eaeaea; border-radius:20px;
                     padding:6px 20px; font-size:12px; color:#888;">
            Intelligence Platform &nbsp;·&nbsp;
            <span style="color:#1D9E75; font-weight:500;">ChurnIQ</span>
            &nbsp;×&nbsp;
            <span style="color:#378ADD; font-weight:500;">DataLens</span>
        </span>
    </div>
    """, unsafe_allow_html=True)
 
    c1, gap, c2 = st.columns([5, 1, 5])
 
    with c1:
        st.markdown("""
        <div class="mode-card">
            <div class="icon">📊</div>
            <div class="title" style="color:#1D9E75;">ChurnIQ</div>
            <div class="subtitle" style="color:#aaa;">Churn Intelligence</div>
            <div class="desc">
                Predict customer churn using Machine Learning.<br>
                Explainable AI with SHAP, smart retention recommendations,
                model comparison (RF vs LR vs SVM vs XGBoost) and analytics.
            </div>
            <div class="tags">
                <span class="tag-green">ML Predict</span>
                <span class="tag-green">SHAP</span>
                <span class="tag-green">Analytics</span>
                <span class="tag-green">Recommendations</span>
                <span class="tag-green">Export PDF</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        if st.button("Open ChurnIQ →", use_container_width=True, key="btn_churn"):
            st.session_state["mode"] = "churniq"
            st.rerun()
 
    with c2:
        st.markdown("""
        <div class="mode-card">
            <div class="icon">🔭</div>
            <div class="title" style="color:#378ADD;">DataLens</div>
            <div class="subtitle" style="color:#aaa;">Universal Analytics Studio</div>
            <div class="desc">
                Upload any CSV dataset and get an instant auto-generated
                analytics dashboard. Smart column detection, auto-built charts
                for HR, Sales, Finance or any tabular data.
            </div>
            <div class="tags">
                <span class="tag-blue">Any CSV</span>
                <span class="tag-blue">Auto Charts</span>
                <span class="tag-blue">Smart Detect</span>
                <span class="tag-blue">HR &amp; Finance</span>
                <span class="tag-blue">Export CSV</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        if st.button("Open DataLens →", use_container_width=True, key="btn_lens"):
            st.session_state["mode"] = "datalens"
            st.rerun()
 
    st.stop()
 
# ════════════════════════════════════════════
# CHURNIQ MODE
# ════════════════════════════════════════════
if st.session_state["mode"] == "churniq":
    model, encoders = load_model()
    df = load_data()
 
    total    = len(df)
    churned  = df[df["Churn"] == "Yes"].shape[0]
    retained = total - churned
    rate     = churned / total * 100
    avg_ten  = df["tenure"].mean()
 
    menu = st.radio(
        "", ["🏠  Home", "🔍  Predict", "📊  Analytics", "👤  About"],
        horizontal=True, label_visibility="collapsed",
    )
    st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
 
    if   menu == "🏠  Home":      show_home(total, rate, retained, avg_ten)
    elif menu == "🔍  Predict":   show_predict(model, encoders)
    elif menu == "📊  Analytics": show_analytics(df, total, churned, retained, rate)
    elif menu == "👤  About":     show_about()
 
# ════════════════════════════════════════════
# DATALENS MODE
# ════════════════════════════════════════════
elif st.session_state["mode"] == "datalens":
    show_smart_upload()
 