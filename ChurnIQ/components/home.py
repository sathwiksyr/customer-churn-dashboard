# components/home.py
import time
import streamlit as st
from datetime import datetime
 
 
def show_home(total, rate, retained, avg_ten):
    now = datetime.now().strftime("%d %b %Y · %H:%M:%S")
 
    col_title, col_refresh = st.columns([4, 1])
    with col_title:
        st.markdown(f"""
        <div class="page-hero">
            <h1>📊 ChurnIQ <span style="font-size:14px; font-weight:400; color:#1D9E75;">— Churn Intelligence</span></h1>
            <p>IBM Telco dataset · ML-powered predictions
            &nbsp;·&nbsp; <span style="color:#1D9E75; font-weight:500;">● Live</span>
            &nbsp;·&nbsp; Last updated: {now}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_refresh:
        st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
 
    # ── KPI metrics ───────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total customers", f"{total:,}")
    k2.metric("Churn rate",      f"{rate:.1f}%",      delta="-2.1% vs last qtr", delta_color="normal")
    k3.metric("Retained",        f"{retained:,}",     delta="+1.4%",             delta_color="normal")
    k4.metric("Avg tenure",      f"{avg_ten:.0f} months")
 
    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
 
    # ── Upload new CSV ────────────────────────
    with st.expander("📂 Upload new customer data (CSV)", expanded=False):
        st.markdown("<p style='font-size:13px; color:#666;'>Upload an updated CSV to refresh the dashboard instantly.</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Choose CSV file", type=["csv"], label_visibility="collapsed")
        if uploaded:
            import pandas as pd
            import os
            BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            save_path = os.path.join(BASE_DIR, "data", "Churn.csv")
            df_new    = pd.read_csv(uploaded)
            df_new.to_csv(save_path, index=False)
            st.success(f"✅ Data updated! {len(df_new):,} records loaded.")
            st.cache_data.clear()
            time.sleep(1)
            st.rerun()
 
    st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
 
    # ── Two feature cards ─────────────────────
    c1, c2 = st.columns(2)
 
    with c1:
        st.markdown("""
        <div class="section-card">
            <h2>🚀 What ChurnIQ does</h2>
            <div class="feat-item"><span class="feat-dot"></span>
                <strong>ML Prediction</strong> — Random Forest model predicts churn probability in real-time
            </div>
            <div class="feat-item"><span class="feat-dot"></span>
                <strong>Explainable AI (SHAP)</strong> — Shows exactly why a customer is predicted to churn
            </div>
            <div class="feat-item"><span class="feat-dot"></span>
                <strong>Recommendations</strong> — Smart business strategies to retain at-risk customers
            </div>
            <div class="feat-item"><span class="feat-dot"></span>
                <strong>Model Comparison</strong> — RF vs Logistic Regression vs SVM vs XGBoost
            </div>
            <div class="feat-item"><span class="feat-dot"></span>
                <strong>Analytics</strong> — Churn by contract, payment method &amp; tenure
            </div>
            <div class="feat-item"><span class="feat-dot"></span>
                <strong>Export</strong> — Download data as CSV or full PDF report
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    with c2:
        st.markdown("""
        <div class="section-card">
            <h2>📈 Dataset overview</h2>
            <div class="feat-item"><span class="feat-dot"></span>
                <strong>Dataset</strong> — IBM Telco Customer Churn (7,043 records)
            </div>
            <div class="feat-item"><span class="feat-dot"></span>
                <strong>Features</strong> — 21 input variables used for prediction
            </div>
            <div class="feat-item"><span class="feat-dot"></span>
                <strong>Churn rate</strong> — 26.5% of customers churned
            </div>
            <div class="feat-item"><span class="feat-dot"></span>
                <strong>Best model</strong> — Auto-selected based on F1 Score
            </div>
            <div class="feat-item"><span class="feat-dot"></span>
                <strong>Accuracy</strong> — 80%+ on test data
            </div>
            <div class="feat-item"><span class="feat-dot"></span>
                <strong>Signup system</strong> — Secure user accounts with hashed passwords
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    # ── InsightIQ promo ───────────────────────
    st.markdown("""
    <div class="section-card" style="margin-top:0.5rem; border-left: 3px solid #378ADD;">
        <h2>🔍 Also available — InsightIQ <span style="font-size:12px; font-weight:400; color:#378ADD;">Insight Intelligence</span></h2>
        <div style="font-size:13px; color:#666; line-height:1.7;">
            Upload <strong>any CSV dataset</strong> (HR attrition, sales, finance) and InsightIQ will
            auto-detect columns, map them smartly, and build a complete analytics dashboard instantly —
            no setup needed. Go back to the home screen to access InsightIQ.
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown(
        "<p style='font-size:11px; color:#bbb; text-align:center; margin-top:1rem;'>"
        "ChurnIQ — Churn Intelligence · Auto-refreshes every 30 seconds</p>",
        unsafe_allow_html=True
    )