# components/about.py
import streamlit as st
 
 
def show_about():
    st.markdown("""
    <div class="page-hero">
        <h1>About ChurnIQ</h1>
        <p>Churn Intelligence · Customer Churn Prediction &amp; Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
 
    # ── Row 1 ─────────────────────────────────
    c1, c2 = st.columns(2)
 
    with c1:
        st.markdown("""
        <div class="section-card">
            <h2>🛠 Tech stack</h2>
            <div class="feat-item"><span class="feat-dot"></span><strong>Streamlit</strong> — web dashboard framework</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>scikit-learn</strong> — Random Forest, Logistic Regression, SVM</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>XGBoost</strong> — gradient boosting classifier</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>SHAP</strong> — explainable AI &amp; feature importance</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>Pandas &amp; NumPy</strong> — data wrangling</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>Plotly</strong> — interactive charts</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>ReportLab</strong> — PDF report generation</div>
        </div>
        """, unsafe_allow_html=True)
 
    with c2:
        st.markdown("""
        <div class="section-card">
            <h2>🚀 Features</h2>
            <div class="feat-item"><span class="feat-dot"></span>Real-time churn prediction with probability gauge</div>
            <div class="feat-item"><span class="feat-dot"></span>Explainable AI — SHAP values show why customer churns</div>
            <div class="feat-item"><span class="feat-dot"></span>Smart recommendations to retain at-risk customers</div>
            <div class="feat-item"><span class="feat-dot"></span>Model comparison — RF vs LR vs SVM vs XGBoost</div>
            <div class="feat-item"><span class="feat-dot"></span>Analytics dashboard with churn breakdowns</div>
            <div class="feat-item"><span class="feat-dot"></span>InsightIQ — auto-dashboard for any CSV dataset</div>
            <div class="feat-item"><span class="feat-dot"></span>Secure signup &amp; login with hashed passwords</div>
        </div>
        """, unsafe_allow_html=True)
 
    # ── Row 2 ─────────────────────────────────
    c3, c4 = st.columns(2)
 
    with c3:
        st.markdown("""
        <div class="section-card">
            <h2>📊 Model details</h2>
            <div class="feat-item"><span class="feat-dot"></span><strong>Algorithm</strong> — Best model auto-selected by F1 Score</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>Dataset</strong> — IBM Telco Customer Churn (7,043 records)</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>Features</strong> — 21 input variables</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>Churn rate</strong> — ~26.5% in dataset</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>Accuracy</strong> — 80%+ on test data</div>
            <div class="feat-item"><span class="feat-dot"></span><strong>Metric used</strong> — F1 Score (best for imbalanced data)</div>
        </div>
        """, unsafe_allow_html=True)
 
    with c4:
        st.markdown("""
        <div class="section-card">
            <h2>🔍 InsightIQ</h2>
            <div class="feat-item"><span class="feat-dot"></span>Upload any CSV dataset instantly</div>
            <div class="feat-item"><span class="feat-dot"></span>Auto-detects target, tenure, charges, segment columns</div>
            <div class="feat-item"><span class="feat-dot"></span>Builds full analytics dashboard automatically</div>
            <div class="feat-item"><span class="feat-dot"></span>Works with HR, Sales, Finance, any tabular data</div>
            <div class="feat-item"><span class="feat-dot"></span>Override column mapping manually if needed</div>
            <div class="feat-item"><span class="feat-dot"></span>Export processed data as CSV</div>
        </div>
        """, unsafe_allow_html=True)
 
    # ── Row 3 ─────────────────────────────────
    st.markdown("""
    <div class="section-card" style="border-left: 3px solid #1D9E75;">
        <h2>📬 Project info</h2>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
            <div class="feat-item"><span class="feat-dot"></span>Built for academic &amp; portfolio use</div>
            <div class="feat-item"><span class="feat-dot"></span>IBM Telco open-source dataset (Kaggle)</div>
            <div class="feat-item"><span class="feat-dot"></span>Deployed on Streamlit Cloud (free tier)</div>
            <div class="feat-item"><span class="feat-dot"></span>Open source — feel free to fork &amp; extend</div>
        </div>
    </div>
    """, unsafe_allow_html=True)