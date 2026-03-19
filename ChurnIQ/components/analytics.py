import streamlit as st
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from Config import RED, BLUE, clean_fig
 
 
def show_analytics(df, total, churned, retained, rate):
    st.markdown("""
    <div class="page-hero">
        <h1>Analytics</h1>
        <p>Churn patterns by contract, gender, payment method, and tenure</p>
    </div>
    """, unsafe_allow_html=True)
 
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total",      f"{total:,}")
    k2.metric("Churned",    f"{churned:,}")
    k3.metric("Retained",   f"{retained:,}")
    k4.metric("Churn rate", f"{rate:.1f}%")
 
    st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
 
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
            st.markdown(
                "<h5 style='font-size:15px; font-weight:600; color:#111; margin:0 0 10px;'>"
                "Tenure distribution by churn</h5>",
                unsafe_allow_html=True,
            )
            fig4 = px.histogram(
                df, x="tenure", color="Churn",
                nbins=24, barmode="overlay", opacity=0.75,
                color_discrete_map={"Yes": RED, "No": BLUE},
                labels={"tenure": "Tenure (months)", "count": "Customers"},
            )
            fig4.update_layout(
                height=300, margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans", size=12, color="#555"),
                legend=dict(title="Churn", orientation="h",
                            yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            fig4.update_xaxes(showgrid=False, linecolor="#eaeaea", tickfont_size=11)
            fig4.update_yaxes(showgrid=True, gridcolor="#f0f0f0",
                              linecolor="rgba(0,0,0,0)", tickfont_size=11)
            st.plotly_chart(fig4, use_container_width=True)
 
    st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
    ex1, ex2 = st.columns(2)
 
    with ex1:
        csv = df.to_csv(index=False).encode()
        st.download_button("⬇️ Download CSV", csv, "churn_data.csv", use_container_width=True)
 
    with ex2:
        pdf_bytes = _create_pdf(total, churned, retained, rate)
        st.download_button("📄 Download PDF", pdf_bytes, "churn_report.pdf", use_container_width=True)
 
 
def _create_pdf(total, churned, retained, rate):
    doc    = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    content = [
        Paragraph("Churn Intelligence Report", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"Total customers : {total:,}",   styles["Normal"]),
        Paragraph(f"Churned         : {churned:,}",  styles["Normal"]),
        Paragraph(f"Retained        : {retained:,}", styles["Normal"]),
        Paragraph(f"Churn rate      : {rate:.2f}%",  styles["Normal"]),
    ]
    doc.build(content)
    with open("report.pdf", "rb") as f:
        return f.read()