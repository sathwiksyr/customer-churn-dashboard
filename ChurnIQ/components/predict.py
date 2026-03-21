import time
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from config import RED, GREEN
from utils  import show_shap_chart, show_recommendations
 
 
def show_predict(model, encoders):
    st.markdown("""
    <div class="page-hero">
        <h1>🔍 Predict Churn Risk</h1>
        <p>Enter customer attributes — get prediction, explanation &amp; recommendations</p>
    </div>
    """, unsafe_allow_html=True)
 
    # ── Input form ────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='font-size:15px; font-weight:600; color:#111; margin-bottom:14px;'>Customer details</h2>", unsafe_allow_html=True)
 
    col1, col2 = st.columns(2)
    with col1:
        tenure         = st.slider("Tenure (months)", 0, 72, 12)
        contract       = st.selectbox("Contract type", ["Month-to-month", "One year", "Two year"])
        payment_method = st.selectbox("Payment method", [
            "Electronic check", "Mailed check",
            "Bank transfer (automatic)", "Credit card (automatic)",
        ])
        gender         = st.selectbox("Gender", ["Male", "Female"])
 
    with col2:
        monthly_charges = st.number_input("Monthly charges ($)", 0.0, 200.0, 65.0, step=1.0)
        internet        = st.selectbox("Internet service", ["DSL", "Fiber optic", "No"])
        total_charges   = st.number_input("Total charges ($)", 0.0, 10000.0, float(tenure * 65), step=10.0)
        _               = st.slider("Number of dependents", 0, 5, 0)
 
    st.markdown("<div style='margin-top:0.5rem; font-size:13px; font-weight:600; color:#555;'>Add-ons & flags</div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:0.4rem;'></div>", unsafe_allow_html=True)
 
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        senior_citizen  = st.checkbox("Senior citizen")
        partner         = st.checkbox("Has partner")
    with c2:
        dependents      = st.checkbox("Has dependents")
        phone_service   = st.checkbox("Phone service", value=True)
    with c3:
        multiple_lines  = st.checkbox("Multiple lines")
        online_security = st.checkbox("Online security")
    with c4:
        online_backup   = st.checkbox("Online backup")
        tech_support    = st.checkbox("Tech support")
 
    c5, c6, c7, c8 = st.columns(4)
    with c5:  device_protection = st.checkbox("Device protection")
    with c6:  streaming_tv      = st.checkbox("Streaming TV")
    with c7:  streaming_movies  = st.checkbox("Streaming movies")
    with c8:  paperless_billing = st.checkbox("Paperless billing")
 
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
 
    if st.button("▶  Run prediction", key="run_pred"):
        with st.spinner("Analyzing customer profile..."):
            time.sleep(1.0)
 
            contract_enc = encoders["Contract"].transform([contract])[0]
            internet_enc = encoders["InternetService"].transform([internet])[0]
 
            input_df = pd.DataFrame({
                "tenure":           [tenure],
                "MonthlyCharges":   [monthly_charges],
                "TotalCharges":     [total_charges],
                "Contract":         [contract_enc],
                "InternetService":  [internet_enc],
                "SeniorCitizen":    [int(senior_citizen)],
                "Partner":          [int(partner)],
                "Dependents":       [int(dependents)],
                "PhoneService":     [int(phone_service)],
                "MultipleLines":    [int(multiple_lines)],
                "OnlineSecurity":   [int(online_security)],
                "OnlineBackup":     [int(online_backup)],
                "DeviceProtection": [int(device_protection)],
                "TechSupport":      [int(tech_support)],
                "StreamingTV":      [int(streaming_tv)],
                "StreamingMovies":  [int(streaming_movies)],
                "PaperlessBilling": [int(paperless_billing)],
            })
            input_df = input_df.reindex(columns=model.feature_names_in_, fill_value=0)
 
            prob   = model.predict_proba(input_df)[0][1]
            result = model.predict(input_df)[0]
 
        # ── Result metrics ────────────────────
        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        p1, p2, p3 = st.columns(3)
        p1.metric("Churn probability", f"{prob*100:.1f}%")
        p2.metric("Risk level",        "High risk ⚠️" if result == 1 else "Low risk ✅")
        p3.metric("Confidence",        f"{max(prob, 1-prob)*100:.1f}%")
 
        # ── Gauge ─────────────────────────────
        color = RED if prob > 0.5 else GREEN
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(prob * 100, 1),
            number={"suffix": "%", "font": {"size": 32}},
            gauge={
                "axis":  {"range": [0, 100], "tickfont": {"size": 11}},
                "bar":   {"color": color, "thickness": 0.25},
                "bgcolor": "#f7f8fa",
                "steps": [
                    {"range": [0,  40],  "color": "#E1F5EE"},
                    {"range": [40, 65],  "color": "#FFF8E7"},
                    {"range": [65, 100], "color": "#FCEBEB"},
                ],
                "threshold": {"line": {"color": color, "width": 3},
                              "thickness": 0.75, "value": round(prob * 100, 1)},
            },
        ))
        fig.update_layout(height=260, margin=dict(l=20, r=20, t=20, b=0),
                          paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
 
        badge = ('<span class="badge-high">⚠️ High churn risk</span>'
                 if result == 1 else '<span class="badge-low">✅ Low churn risk</span>')
        st.markdown(f"<div style='text-align:center; margin-top:-10px; margin-bottom:1.5rem;'>{badge}</div>",
                    unsafe_allow_html=True)
 
        # ── Tabs: SHAP | Recommendations ──────
        tab1, tab2 = st.tabs(["🧠 Explainable AI (SHAP)", "💡 Recommendations"])
 
        with tab1:
            st.markdown('<div class="section-card"><h2>Why is this customer predicted to churn?</h2>', unsafe_allow_html=True)
            st.markdown("<p style='font-size:13px; color:#888; margin-bottom:12px;'>SHAP values show how much each feature contributed to this prediction. Red = increases churn risk, Green = reduces it.</p>", unsafe_allow_html=True)
            show_shap_chart(model, input_df)
            st.markdown("</div>", unsafe_allow_html=True)
 
        with tab2:
            st.markdown('<div class="section-card"><h2>💡 Actionable Business Recommendations</h2>', unsafe_allow_html=True)
            st.markdown("<p style='font-size:13px; color:#888; margin-bottom:12px;'>Based on this customer's profile, here are targeted retention strategies:</p>", unsafe_allow_html=True)
            show_recommendations(
                prob, contract, internet, tech_support,
                online_security, tenure, monthly_charges,
                senior_citizen, payment_method
            )
            st.markdown("</div>", unsafe_allow_html=True)