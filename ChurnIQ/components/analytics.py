# components/analytics.py  —  Analytics + Model Comparison
import streamlit as st
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from config import RED, BLUE, clean_fig
from utils  import show_model_comparison, load_metrics, load_best_name, create_pdf_report
 
 
def show_analytics(df, total, churned, retained, rate):
    st.markdown("""
    <div class="page-hero">
        <h1>📊 Analytics</h1>
        <p>Churn patterns, model comparison &amp; accuracy metrics</p>
    </div>
    """, unsafe_allow_html=True)
 
    # ── KPI row ───────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total",      f"{total:,}")
    k2.metric("Churned",    f"{churned:,}")
    k3.metric("Retained",   f"{retained:,}")
    k4.metric("Churn rate", f"{rate:.1f}%")
 
    st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
 
    # ── Tabs ──────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📈 Churn Analytics", "🤖 Model Comparison", "📋 Accuracy Metrics"])
 
    # ════ TAB 1: Churn Analytics ═════════════
    with tab1:
        r1c1, r1c2 = st.columns(2)
 
        with r1c1:
            st.markdown('<div class="section-card"><h2>Churn by contract type</h2>', unsafe_allow_html=True)
            ctdf = df.groupby(["Contract", "Churn"]).size().reset_index(name="count")
            fig1 = px.bar(ctdf, x="Contract", y="count", color="Churn",
                          barmode="group", color_discrete_map={"Yes": RED, "No": BLUE})
            st.plotly_chart(clean_fig(fig1), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
        with r1c2:
            st.markdown('<div class="section-card"><h2>Overall churn distribution</h2>', unsafe_allow_html=True)
            pie_df = df["Churn"].value_counts().reset_index()
            pie_df.columns = ["Churn", "count"]
            fig2 = px.pie(pie_df, names="Churn", values="count",
                          color="Churn", color_discrete_map={"Yes": RED, "No": BLUE}, hole=0.6)
            fig2.update_traces(textinfo="percent+label", textfont_size=12)
            st.plotly_chart(clean_fig(fig2), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
        r2c1, r2c2 = st.columns(2)
 
        with r2c1:
            st.markdown('<div class="section-card"><h2>Churn by payment method</h2>', unsafe_allow_html=True)
            pmdf = df.groupby(["PaymentMethod", "Churn"]).size().reset_index(name="count")
            fig3 = px.bar(pmdf, x="count", y="PaymentMethod", color="Churn",
                          orientation="h", barmode="group",
                          color_discrete_map={"Yes": RED, "No": BLUE})
            st.plotly_chart(clean_fig(fig3), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
        with r2c2:
            with st.container(border=True):
                st.markdown("<h5 style='font-size:15px; font-weight:600; color:#111; margin:0 0 10px;'>Tenure distribution by churn</h5>", unsafe_allow_html=True)
                fig4 = px.histogram(df, x="tenure", color="Churn", nbins=24,
                                    barmode="overlay", opacity=0.75,
                                    color_discrete_map={"Yes": RED, "No": BLUE},
                                    labels={"tenure": "Tenure (months)", "count": "Customers"})
                fig4.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                                   paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   font=dict(family="DM Sans", size=12, color="#555"),
                                   legend=dict(title="Churn", orientation="h",
                                               yanchor="bottom", y=1.02, xanchor="right", x=1))
                fig4.update_xaxes(showgrid=False, linecolor="#eaeaea", tickfont_size=11)
                fig4.update_yaxes(showgrid=True, gridcolor="#f0f0f0", tickfont_size=11)
                st.plotly_chart(fig4, use_container_width=True)
 
    # ════ TAB 2: Model Comparison ════════════
    with tab2:
        metrics   = load_metrics()
        best_name = load_best_name()
 
        st.markdown('<div class="section-card"><h2>🤖 Model Comparison — Random Forest vs Logistic Regression vs SVM vs XGBoost</h2>', unsafe_allow_html=True)
 
        if not metrics:
            st.warning("⚠️ No model metrics found. Run `python model.py` first to train and compare all models.")
        else:
            st.markdown(f"<p style='font-size:13px; color:#888; margin-bottom:12px;'>Comparing all models on Accuracy, Precision, Recall, F1 Score and ROC AUC. Best model selected automatically.</p>", unsafe_allow_html=True)
            show_model_comparison(metrics)
 
        st.markdown('</div>', unsafe_allow_html=True)
 
        # Suggestion card
        if metrics:
            best = max(metrics, key=lambda m: metrics[m].get("F1 Score", 0))
            st.markdown(f"""
            <div class="section-card">
                <h2>💡 Model Recommendation</h2>
                <div style="font-size:13px; color:#555; line-height:1.8;">
                    Based on F1 Score (best for imbalanced churn data), <strong>{best}</strong> is recommended as the production model.<br>
                    F1 Score balances both precision and recall — important when false negatives (missed churners) are costly.<br><br>
                    <strong>When to use each model:</strong><br>
                    • <strong>Random Forest</strong> — Best overall, handles missing data, no scaling needed<br>
                    • <strong>XGBoost</strong> — Best accuracy, great for large datasets<br>
                    • <strong>Logistic Regression</strong> — Most explainable, fastest training<br>
                    • <strong>SVM</strong> — Good for small datasets, slower on large data
                </div>
            </div>
            """, unsafe_allow_html=True)
 
    # ════ TAB 3: Accuracy Metrics ════════════
    with tab3:
        metrics   = load_metrics()
        best_name = load_best_name()
 
        if not metrics:
            st.warning("⚠️ Run `python model.py` to generate accuracy metrics.")
        else:
            st.markdown('<div class="section-card"><h2>📋 Detailed Accuracy Metrics</h2>', unsafe_allow_html=True)
 
            metric_names = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC AUC"]
            cols = st.columns(len(metric_names))
            best_m = metrics.get(best_name, {})
            for i, m in enumerate(metric_names):
                cols[i].metric(m, f"{best_m.get(m, 0):.1f}%",
                               help=f"{best_name} — {m}")
 
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
 
            # Full metrics table
            st.markdown('<div class="section-card"><h2>All models — full metrics table</h2>', unsafe_allow_html=True)
            import pandas as pd
            rows = []
            for name, m in metrics.items():
                rows.append({"Model": name, **m,
                             "Recommended": "✅ Best" if name == best_name else ""})
            df_m = pd.DataFrame(rows)
            st.dataframe(df_m.set_index("Model"), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
 
    # ── Exports ───────────────────────────────
    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    ex1, ex2 = st.columns(2)
 
    with ex1:
        csv = df.to_csv(index=False).encode()
        st.download_button("⬇️ Download CSV", csv, "churn_data.csv", use_container_width=True)
 
    with ex2:
        metrics   = load_metrics()
        best_name = load_best_name()
        pdf = create_pdf_report(total, churned, retained, rate, metrics, best_name)
        st.download_button("📄 Download PDF Report", pdf, "churniq_report.pdf", use_container_width=True)