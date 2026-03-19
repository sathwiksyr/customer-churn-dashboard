# ─────────────────────────────────────────────
# pages/about.py  —  About tab
# ─────────────────────────────────────────────
import streamlit as st
 
 
def show_about():
    st.markdown("""
    <div class="page-hero">
        <h1>About</h1>
        <p>Project details and developer profile</p>
    </div>
    """, unsafe_allow_html=True)
 
    c1, c2 = st.columns([2, 1])
 
    with c1:
        st.markdown("""
        <div class="section-card">
            <h2>🛠 Tech stack</h2>
            <div class="feat-item"><span class="feat-dot"></span><strong>Streamlit</strong> — dashboard framework</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>scikit-learn</strong> — Random Forest classifier</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>Pandas &amp; NumPy</strong> — data wrangling</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>Plotly</strong> — interactive visualisations</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>ReportLab</strong> — PDF generation</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>IBM Telco dataset</strong> — 7,043 customer records</div>
        </div>
        """, unsafe_allow_html=True)
 
    with c2:
        st.markdown("""
        <div class="section-card">
            <h2>👤 Developer</h2>
            <div class="profile-avatar">SS</div>
            <div style="font-size:16px; font-weight:600; color:#111;">Sathwik S.Y.R</div>
            <div style="font-size:13px; color:#888; margin-top:3px;">Big Data Engineering Student</div>
            <div style="font-size:13px; color:#555; margin-top:12px; line-height:1.6;">
                Building end-to-end ML dashboards with real business applications.
                Open to data engineering and analytics roles.
            </div>
            <div style="margin-top:12px;">
                <span class="skill-pill">Python</span>
                <span class="skill-pill">ML</span>
                <span class="skill-pill">Power BI</span>
                <span class="skill-pill">SQL</span>
                <span class="skill-pill">Spark</span>
            </div>
        </div>
        """, unsafe_allow_html=True)