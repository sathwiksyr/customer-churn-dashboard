
import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
 
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model")
 
RED   = "#E24B4A"
GREEN = "#1D9E75"
BLUE  = "#378ADD"
AMBER = "#EF9F27"
 
 
# ── Load extras ───────────────────────────────
@st.cache_resource
def load_metrics():
    path = os.path.join(MODEL_DIR, "metrics.pkl")
    if os.path.exists(path):
        return pickle.load(open(path, "rb"))
    return {}
 
@st.cache_resource
def load_best_name():
    path = os.path.join(MODEL_DIR, "best_name.pkl")
    if os.path.exists(path):
        return pickle.load(open(path, "rb"))
    return "Random Forest"
 
@st.cache_resource
def load_feature_names():
    path = os.path.join(MODEL_DIR, "feature_names.pkl")
    if os.path.exists(path):
        return pickle.load(open(path, "rb"))
    return []
 
 
# ── SHAP explainer ────────────────────────────
def get_shap_values(model, input_df):
    try:
        import shap
        explainer   = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(input_df)
 
        # Handle all possible shapes:
        # Case 1: list of arrays (binary classification) → take index 1
        if isinstance(shap_values, list):
            sv = np.array(shap_values[1])
        else:
            sv = np.array(shap_values)
 
        # Case 2: 3D array (n_samples, n_features, n_classes) → take last class
        if sv.ndim == 3:
            sv = sv[:, :, 1]
 
        # Case 3: 2D array (n_samples, n_features) → already correct
        # Case 4: 1D array → reshape
        if sv.ndim == 1:
            sv = sv.reshape(1, -1)
 
        # Now sv should be (n_samples, n_features)
        base = explainer.expected_value
        if isinstance(base, (list, np.ndarray)):
            base = base[1] if len(base) > 1 else base[0]
 
        return sv, base
 
    except Exception as e:
        return None, str(e)
 
 
def show_shap_chart(model, input_df):
    """Show SHAP feature importance bar chart for prediction."""
    shap_vals, base = get_shap_values(model, input_df)
 
    if shap_vals is None:
        st.info(f"SHAP not available: {base}\n\nInstall with: `pip install shap`")
        return
 
    try:
        cols = list(input_df.columns)
        # Get values for first (only) sample
        vals = shap_vals[0]
 
        # Ensure lengths match
        if len(vals) != len(cols):
            st.warning(f"SHAP shape mismatch: {len(vals)} values for {len(cols)} features.")
            return
 
        pairs  = sorted(zip(cols, vals), key=lambda x: abs(x[1]), reverse=True)[:10]
        features = [p[0] for p in pairs]
        values   = [float(p[1]) for p in pairs]
        colors   = [RED if v > 0 else GREEN for v in values]
 
        fig = go.Figure(go.Bar(
            x=values,
            y=features,
            orientation="h",
            marker_color=colors,
            text=[f"{v:+.3f}" for v in values],
            textposition="outside",
        ))
        fig.update_layout(
            height=380,
            margin=dict(l=0, r=80, t=10, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", size=12, color="#555"),
            xaxis=dict(showgrid=True, gridcolor="#f0f0f0",
                       zeroline=True, zerolinecolor="#ccc", tickfont_size=11),
            yaxis=dict(showgrid=False, tickfont_size=11, autorange="reversed"),
        )
        st.plotly_chart(fig, use_container_width=True)
 
        # Plain English explanation
        top_pos = [(f, v) for f, v in pairs if v > 0][:3]
        top_neg = [(f, v) for f, v in pairs if v < 0][:2]
 
        lines = []
        if top_pos:
            factors = ", ".join([f"<strong>{f}</strong>" for f, _ in top_pos])
            lines.append(f"🔴 <strong>Increasing churn risk:</strong> {factors}")
        if top_neg:
            factors = ", ".join([f"<strong>{f}</strong>" for f, _ in top_neg])
            lines.append(f"🟢 <strong>Reducing churn risk:</strong> {factors}")
 
        if lines:
            st.markdown(f"""
            <div style="background:#f7f8fa; border-radius:10px; padding:14px 18px;
                        margin-top:8px; font-size:13px; color:#555; line-height:1.8;">
                {"<br>".join(lines)}
            </div>
            """, unsafe_allow_html=True)
 
    except Exception as e:
        st.error(f"Could not render SHAP chart: {e}")
 
 
# ── Recommendation engine ─────────────────────
def get_recommendations(prob, contract, internet, tech_support,
                         online_security, tenure, monthly_charges,
                         senior_citizen, payment_method):
    recs = []
 
    if prob > 0.65:
        level, color, tc = "🔴 High Risk",   "#FCEBEB", "#A32D2D"
    elif prob > 0.35:
        level, color, tc = "🟡 Medium Risk", "#FAEEDA", "#854F0B"
    else:
        level, color, tc = "🟢 Low Risk",    "#E1F5EE", "#0F6E56"
 
    if contract == "Month-to-month":
        recs.append(("📋 Offer Long-Term Contract",
                     "Customer is on month-to-month. Offer 10–20% discount for switching to a 1 or 2-year contract.",
                     "High Impact"))
    if tenure < 12:
        recs.append(("🎁 New Customer Loyalty Reward",
                     "Customer is new (< 12 months). Send a welcome loyalty reward or first-year discount.",
                     "High Impact"))
    if monthly_charges > 80:
        recs.append(("💰 Review Pricing Plan",
                     "Monthly charges are high. Offer a more affordable bundle or loyalty pricing.",
                     "High Impact"))
    if internet == "Fiber optic":
        recs.append(("🌐 Fiber Service Quality Check",
                     "Fiber optic customers churn more. Proactively reach out to check satisfaction.",
                     "Medium Impact"))
    if not tech_support:
        recs.append(("🛠 Offer Free Tech Support Trial",
                     "Customers without tech support churn more. Offer a free 3-month trial.",
                     "Medium Impact"))
    if not online_security:
        recs.append(("🔒 Add Online Security Bundle",
                     "Adding online security increases retention. Offer a discounted bundle.",
                     "Medium Impact"))
    if senior_citizen:
        recs.append(("👴 Senior Citizen Care Plan",
                     "Senior customers need dedicated support. Offer a senior-friendly plan.",
                     "Medium Impact"))
    if payment_method == "Electronic check":
        recs.append(("💳 Switch to Auto-Pay",
                     "Electronic check users churn more. Offer a small discount for auto-payment.",
                     "Low Impact"))
    if not recs:
        recs.append(("✅ Keep Engagement High",
                     "Low churn risk. Continue regular engagement and satisfaction checks.",
                     "Maintenance"))
 
    return level, color, tc, recs
 
 
def show_recommendations(prob, contract, internet, tech_support,
                          online_security, tenure, monthly_charges,
                          senior_citizen, payment_method):
    level, bg, tc, recs = get_recommendations(
        prob, contract, internet, tech_support,
        online_security, tenure, monthly_charges,
        senior_citizen, payment_method
    )
 
    st.markdown(f"""
    <div style="background:{bg}; border-radius:12px; padding:12px 20px;
                margin-bottom:1rem; display:inline-block;">
        <span style="font-size:15px; font-weight:600; color:{tc};">{level}</span>
        <span style="font-size:13px; color:{tc}; margin-left:8px;">
            — {len(recs)} recommendation{'s' if len(recs) != 1 else ''}
        </span>
    </div>
    """, unsafe_allow_html=True)
 
    impact_color = {"High Impact": "#E1F5EE", "Medium Impact": "#FAEEDA",
                    "Low Impact": "#E6F1FB",  "Maintenance":   "#f0f0f0"}
    impact_text  = {"High Impact": "#0F6E56", "Medium Impact": "#854F0B",
                    "Low Impact": "#0C447C",  "Maintenance":   "#555"}
 
    for title, desc, impact in recs:
        ic = impact_color.get(impact, "#f0f0f0")
        it = impact_text.get(impact,  "#555")
        st.markdown(f"""
        <div style="background:#fff; border:1px solid #eaeaea; border-radius:12px;
                    padding:14px 18px; margin-bottom:10px;">
            <div style="display:flex; align-items:center; justify-content:space-between;
                        margin-bottom:6px;">
                <span style="font-size:14px; font-weight:600; color:#111;">{title}</span>
                <span style="background:{ic}; color:{it}; font-size:11px;
                             padding:3px 10px; border-radius:20px;">{impact}</span>
            </div>
            <div style="font-size:13px; color:#666; line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
 
 
# ── Model comparison chart ────────────────────
def show_model_comparison(metrics: dict):
    if not metrics:
        st.info("Run `python model.py` to generate model comparison metrics.")
        return
 
    models       = list(metrics.keys())
    metric_names = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC AUC"]
    colors       = [GREEN, BLUE, AMBER, RED, "#9B59B6"]
 
    fig = go.Figure()
    for i, m in enumerate(metric_names):
        fig.add_trace(go.Bar(
            name=m,
            x=models,
            y=[metrics[mdl].get(m, 0) for mdl in models],
            marker_color=colors[i],
            text=[f"{metrics[mdl].get(m, 0):.1f}%" for mdl in models],
            textposition="outside",
        ))
 
    fig.update_layout(
        barmode="group", height=380,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", size=12, color="#555"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(range=[0, 115], showgrid=True, gridcolor="#f0f0f0", ticksuffix="%"),
        xaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True)
 
    best = max(metrics, key=lambda m: metrics[m].get("F1 Score", 0))
    st.markdown(f"""
    <div style="text-align:center; margin-top:8px;">
        <span style="background:#E1F5EE; color:#0F6E56; padding:6px 20px;
                     border-radius:20px; font-size:13px; font-weight:600;">
            🏆 Best model: {best} — F1 Score: {metrics[best]['F1 Score']}%
        </span>
    </div>
    """, unsafe_allow_html=True)
 
 
# ── PDF report ────────────────────────────────
def create_pdf_report(total, churned, retained, rate, metrics=None, best_name=""):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors as rl_colors
 
    doc    = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    story  = []
 
    story.append(Paragraph("ChurnIQ — Churn Intelligence Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Customer Summary", styles["Heading2"]))
    story.append(Paragraph(f"Total customers : {total:,}",   styles["Normal"]))
    story.append(Paragraph(f"Churned         : {churned:,}", styles["Normal"]))
    story.append(Paragraph(f"Retained        : {retained:,}",styles["Normal"]))
    story.append(Paragraph(f"Churn rate      : {rate:.2f}%", styles["Normal"]))
    story.append(Spacer(1, 12))
 
    if metrics and best_name:
        story.append(Paragraph("Model Comparison", styles["Heading2"]))
        story.append(Paragraph(f"Best model: {best_name}", styles["Normal"]))
        story.append(Spacer(1, 6))
        data = [["Model", "Accuracy", "Precision", "Recall", "F1 Score", "ROC AUC"]]
        for name, m in metrics.items():
            data.append([name,
                         f"{m.get('Accuracy',0)}%",  f"{m.get('Precision',0)}%",
                         f"{m.get('Recall',0)}%",    f"{m.get('F1 Score',0)}%",
                         f"{m.get('ROC AUC',0)}%"])
        t = Table(data)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), rl_colors.HexColor("#1D9E75")),
            ("TEXTCOLOR",  (0,0), (-1,0), rl_colors.white),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0,1), (-1,-1),
             [rl_colors.white, rl_colors.HexColor("#f7f8fa")]),
            ("GRID",    (0,0), (-1,-1), 0.5, rl_colors.HexColor("#eaeaea")),
            ("FONTSIZE",(0,0), (-1,-1), 9),
            ("PADDING", (0,0), (-1,-1), 6),
        ]))
        story.append(t)
 
    doc.build(story)
    with open("report.pdf", "rb") as f:
        return f.read()