import streamlit as st
 
 
def show_home(total, rate, retained, avg_ten):
    st.markdown("""
    <div class="page-hero">
        <h1>Customer Churn Dashboard</h1>
        <p>IBM Telco dataset · ML-powered predictions · Sathwik S.Y.R</p>
    </div>
    """, unsafe_allow_html=True)
 
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total customers", f"{total:,}")
    k2.metric("Churn rate",      f"{rate:.1f}%", delta="-2.1% vs last qtr", delta_color="normal")
    k3.metric("Retained",        f"{retained:,}", delta="+1.4%",             delta_color="normal")
    k4.metric("Avg tenure", f"{avg_ten:.0f} months")
 
    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
 
    c1, c2 = st.columns([2, 1])
 
    with c1:
        st.markdown("""
        <div class="section-card">
            <h2>🚀 Project overview</h2>
            <div class="feat-item"><span class="feat-dot"></span>Random Forest model trained on IBM Telco Churn dataset (7,043 records)</div>
            <div class="feat-item"><span class="feat-dot"></span>Features: tenure, contract, charges, internet service, payment method &amp; more</div>
            <div class="feat-item"><span class="feat-dot"></span>Real-time churn probability scoring with spinner animation</div>
            <div class="feat-item"><span class="feat-dot"></span>Analytics: contract, gender, payment &amp; tenure breakdowns</div>
            <div class="feat-item"><span class="feat-dot"></span>Export to CSV &amp; PDF for business reporting</div>
        </div>
        """, unsafe_allow_html=True)
 
    with c2:
        st.markdown("""
        <div class="section-card" style="height:100%;">
            <h2>👤 Profile</h2>
            <div class="profile-avatar">SS</div>
            <div style="font-size:15px; font-weight:600; color:#111;">Sathwik S.Y.R</div>
            <div style="font-size:13px; color:#888; margin-top:2px;">Big Data Engineering</div>
            <div style="margin-top:10px;">
                <span class="skill-pill">Python</span>
                <span class="skill-pill">ML</span>
                <span class="skill-pill">Power BI</span>
                <span class="skill-pill">Streamlit</span>
                <span class="skill-pill">Spark</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
 