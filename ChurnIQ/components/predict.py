# components/predict.py
import time
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from Config import RED, GREEN
 
 
def show_predict(model, encoders):
    st.markdown("""
    <div class="page-hero">
        <h1>Predict churn risk</h1>
        <p>Enter customer attributes to get a real-time probability estimate</p>
    </div>
    """, unsafe_allow_html=True)
 
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
 
    st.markdown(
        "<div style='margin-top:0.5rem; font-size:13px; font-weight:600; color:#555;'>"
        "Add-ons & account flags</div>",
        unsafe_allow_html=True
    )
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
    with c5:
        device_protection = st.checkbox("Device protection")
    with c6:
        streaming_tv      = st.checkbox("Streaming TV")
    with c7:
        streaming_movies  = st.checkbox("Streaming movies")
    with c8:
        paperless_billing = st.checkbox("Paperless billing")
 
    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
 
    if st.button("▶  Run prediction"):
        with st.spinner("Analyzing customer profile..."):
            time.sleep(1.2)
 
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
 
        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        p1, p2, p3 = st.columns(3)
        p1.metric("Churn probability", f"{prob*100:.1f}%")
        p2.metric("Risk level",        "High risk ⚠️" if result == 1 else "Low risk ✅")
        p3.metric("Confidence",        f"{max(prob, 1-prob)*100:.1f}%")
 
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
                "threshold": {
                    "line": {"color": color, "width": 3},
                    "thickness": 0.75,
                    "value": round(prob * 100, 1),
                },
            },
        ))
        fig.update_layout(height=260, margin=dict(l=20, r=20, t=20, b=0), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
 
        badge = (
            '<span class="badge-high">⚠️ High churn risk</span>'
            if result == 1 else
            '<span class="badge-low">✅ Low churn risk</span>'
        )
        st.markdown(f"<div style='text-align:center; margin-top:-10px;'>{badge}</div>", unsafe_allow_html=True)
 
        st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-card"><h2>🔎 Key factors driving this prediction</h2>', unsafe_allow_html=True)
        factors = []
        if contract == "Month-to-month":  factors.append(("▲ Month-to-month contract", RED))
        if tenure < 12:                   factors.append(("▲ Short tenure (< 12 months)", RED))
        if monthly_charges > 80:          factors.append(("▲ High monthly charges", RED))
        if internet == "Fiber optic":     factors.append(("▲ Fiber optic service", RED))
        if not tech_support:              factors.append(("▲ No tech support", "#E59400"))
        if not online_security:           factors.append(("▲ No online security", "#E59400"))
        if senior_citizen:                factors.append(("▲ Senior citizen", "#E59400"))
        if contract == "Two year":        factors.append(("▼ Two-year contract", GREEN))
        if tenure > 36:                   factors.append(("▼ Long-term customer", GREEN))
        if tech_support:                  factors.append(("▼ Has tech support", GREEN))
        if partner:                       factors.append(("▼ Has partner", GREEN))
        for label, color_f in factors[:6]:
            st.markdown(
                f"<div class='feat-item'>"
                f"<span style='color:{color_f}; font-weight:600;'>{label[:1]}</span>"
                f"<span>{label[2:]}</span></div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
 