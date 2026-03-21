# components/smart_upload.py  —  DataLens: Universal Analytics Studio
import streamlit as st
import pandas as pd
import plotly.express as px
 
RED   = "#E24B4A"
BLUE  = "#378ADD"
GREEN = "#1D9E75"
AMBER = "#EF9F27"
COLS  = [BLUE, RED, GREEN, AMBER, "#9B59B6", "#E67E22"]
 
 
def detect_columns(df):
    info = {"target": None, "numeric": [], "categorical": [], "id": None}
    churn_kw = ["churn","attrition","left","exit","cancel","churned","outcome","target","label"]
    id_kw    = ["id","customerid","userid","accountid","customer_id","empid","employeeid"]
 
    for col in df.columns:
        cl = col.lower().replace(" ","").replace("_","")
        if any(k in cl for k in id_kw):
            info["id"] = col
        elif any(k in cl for k in churn_kw):
            info["target"] = col
        elif pd.api.types.is_numeric_dtype(df[col]):
            info["numeric"].append(col)
        elif df[col].nunique() <= 20:
            info["categorical"].append(col)
    return info
 
 
def smart_map(df, info):
    tenure_kw  = ["tenure","months","duration","age","length","period","years","experience"]
    charge_kw  = ["charge","revenue","amount","price","fee","cost","payment","bill","salary","income"]
    segment_kw = ["contract","plan","type","subscription","tier","department","role","jobrole","division"]
    mapping    = {"tenure": None, "charges": None, "contract": None}
 
    for col in df.columns:
        cl = col.lower()
        if not mapping["tenure"]   and any(k in cl for k in tenure_kw)  and pd.api.types.is_numeric_dtype(df[col]):
            mapping["tenure"] = col
        if not mapping["charges"]  and any(k in cl for k in charge_kw)  and pd.api.types.is_numeric_dtype(df[col]):
            mapping["charges"] = col
        if not mapping["contract"] and any(k in cl for k in segment_kw):
            mapping["contract"] = col
 
    nums = info["numeric"]
    if not mapping["tenure"]   and len(nums) > 0: mapping["tenure"]   = nums[0]
    if not mapping["charges"]  and len(nums) > 1: mapping["charges"]  = nums[1]
    if not mapping["contract"] and info["categorical"]: mapping["contract"] = info["categorical"][0]
    return mapping
 
 
def _clean(fig, h=260):
    fig.update_layout(
        height=h, margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", size=12, color="#555"),
        showlegend=False,
    )
    fig.update_xaxes(showgrid=False, linecolor="#eaeaea", tickfont_size=11)
    fig.update_yaxes(showgrid=True, gridcolor="#f0f0f0",
                     linecolor="rgba(0,0,0,0)", tickfont_size=11)
    return fig
 
 
def show_smart_upload():
    # ── Header ────────────────────────────────
    st.markdown("""
    <div class="page-hero">
        <h1>🔭 DataLens
            <span style="font-size:14px; font-weight:400; color:#378ADD;">
                — Universal Analytics Studio
            </span>
        </h1>
        <p>Upload any CSV dataset — auto-detect columns &amp; build a full analytics dashboard instantly</p>
    </div>
    """, unsafe_allow_html=True)
 
    uploaded = st.file_uploader(
        "Drop any CSV file here", type=["csv"],
        label_visibility="collapsed"
    )
 
    if not uploaded:
        st.markdown("""
        <div class="section-card" style="text-align:center; padding:48px 30px;">
            <div style="font-size:48px; margin-bottom:16px;">🔭</div>
            <div style="font-size:18px; font-weight:600; color:#111; margin-bottom:8px;">
                Drop any CSV to get started
            </div>
            <div style="font-size:13px; color:#888; margin-top:8px; line-height:1.8;">
                DataLens automatically detects your columns, maps them intelligently,<br>
                and builds a complete analytics dashboard — no configuration needed.
            </div>
            <div style="margin-top:20px; display:flex; justify-content:center;
                        gap:10px; flex-wrap:wrap;">
                <span style="background:#E1F5EE; color:#0F6E56; padding:4px 14px;
                             border-radius:20px; font-size:12px;">✅ Churn datasets</span>
                <span style="background:#E1F5EE; color:#0F6E56; padding:4px 14px;
                             border-radius:20px; font-size:12px;">✅ HR attrition</span>
                <span style="background:#E6F1FB; color:#0C447C; padding:4px 14px;
                             border-radius:20px; font-size:12px;">✅ Sales data</span>
                <span style="background:#E6F1FB; color:#0C447C; padding:4px 14px;
                             border-radius:20px; font-size:12px;">✅ Finance data</span>
                <span style="background:#FAEEDA; color:#854F0B; padding:4px 14px;
                             border-radius:20px; font-size:12px;">✅ Any CSV</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
 
    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Could not read file: {e}")
        return
 
    st.success(f"✅ Loaded **{len(df):,} rows** · **{len(df.columns)} columns**")
 
    info    = detect_columns(df)
    mapping = smart_map(df, info)
    target  = info["target"]
 
    # ── Column mapping ────────────────────────
    with st.expander("🔍 Auto-detected column mapping — click to override", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"**Target column**\n\n`{target or 'Not found'}`")
        c2.markdown(f"**Tenure / Duration**\n\n`{mapping['tenure'] or 'Not found'}`")
        c3.markdown(f"**Charges / Amount**\n\n`{mapping['charges'] or 'Not found'}`")
        c4.markdown(f"**Segment / Type**\n\n`{mapping['contract'] or 'Not found'}`")
 
        st.markdown("<div style='margin-top:0.4rem; font-size:12px; color:#aaa;'>Override if needed:</div>", unsafe_allow_html=True)
        all_cols = ["None"] + list(df.columns)
        oc1,oc2,oc3,oc4 = st.columns(4)
        with oc1: sel_t = st.selectbox("Target",  all_cols, index=all_cols.index(target) if target in all_cols else 0, key="ot")
        with oc2: sel_n = st.selectbox("Tenure",  all_cols, index=all_cols.index(mapping["tenure"]) if mapping["tenure"] in all_cols else 0, key="ote")
        with oc3: sel_c = st.selectbox("Charges", all_cols, index=all_cols.index(mapping["charges"]) if mapping["charges"] in all_cols else 0, key="och")
        with oc4: sel_s = st.selectbox("Segment", all_cols, index=all_cols.index(mapping["contract"]) if mapping["contract"] in all_cols else 0, key="ocon")
 
        if sel_t != "None": target              = sel_t
        if sel_n != "None": mapping["tenure"]   = sel_n
        if sel_c != "None": mapping["charges"]  = sel_c
        if sel_s != "None": mapping["contract"] = sel_s
 
    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
 
    # ── KPI cards ─────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total records",   f"{len(df):,}")
    k2.metric("Total columns",   f"{len(df.columns)}")
    if target and target in df.columns:
        vc = df[target].value_counts()
        k3.metric(f"{target} = {vc.index[0]}", f"{vc.iloc[0]:,}")
        k4.metric(f"{target} rate",             f"{vc.iloc[0]/len(df)*100:.1f}%")
    else:
        k3.metric("Numeric cols",     f"{len(info['numeric'])}")
        k4.metric("Categorical cols", f"{len(info['categorical'])}")
 
    st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
 
    # ── Charts row 1 ──────────────────────────
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        if target and target in df.columns:
            st.markdown(f'<div class="section-card"><h2>Distribution of {target}</h2>', unsafe_allow_html=True)
            vc  = df[target].value_counts().reset_index()
            vc.columns = [target, "count"]
            fig = px.pie(vc, names=target, values="count", hole=0.6,
                         color_discrete_sequence=[GREEN, RED, BLUE, AMBER])
            fig.update_traces(textinfo="percent+label", textfont_size=12)
            st.plotly_chart(_clean(fig), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
    with r1c2:
        seg = mapping["contract"]
        if seg and seg in df.columns and target and target in df.columns:
            st.markdown(f'<div class="section-card"><h2>{target} by {seg}</h2>', unsafe_allow_html=True)
            gdf = df.groupby([seg, target]).size().reset_index(name="count")
            fig = px.bar(gdf, x=seg, y="count", color=target, barmode="group",
                         color_discrete_sequence=[GREEN, RED, BLUE, AMBER])
            st.plotly_chart(_clean(fig), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
    # ── Charts row 2 ──────────────────────────
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        ten = mapping["tenure"]
        if ten and ten in df.columns:
            with st.container(border=True):
                st.markdown(f"<h5 style='font-size:15px;font-weight:600;color:#111;margin:0 0 10px;'>Distribution of {ten}</h5>",
                            unsafe_allow_html=True)
                fig = px.histogram(
                    df, x=ten,
                    color=target if target and target in df.columns else None,
                    nbins=24, barmode="overlay", opacity=0.75,
                    color_discrete_sequence=[GREEN, RED]
                )
                fig.update_layout(height=280, margin=dict(l=0,r=0,t=10,b=0),
                                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font=dict(family="DM Sans", size=12, color="#555"),
                                  showlegend=bool(target))
                fig.update_xaxes(showgrid=False, tickfont_size=11)
                fig.update_yaxes(showgrid=True, gridcolor="#f0f0f0", tickfont_size=11)
                st.plotly_chart(fig, use_container_width=True)
 
    with r2c2:
        chg = mapping["charges"]
        if chg and chg in df.columns:
            st.markdown(f'<div class="section-card"><h2>Distribution of {chg}</h2>', unsafe_allow_html=True)
            if target and target in df.columns:
                fig = px.box(df, x=target, y=chg, color=target,
                             color_discrete_sequence=[GREEN, RED])
            else:
                fig = px.histogram(df, x=chg, nbins=20, color_discrete_sequence=[AMBER])
            st.plotly_chart(_clean(fig), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
    # ── All categorical breakdowns ─────────────
    cats = [c for c in info["categorical"] if c != target and c != mapping["contract"]][:6]
    if cats:
        st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-card"><h2>📊 All categorical breakdowns</h2>', unsafe_allow_html=True)
        cols_ui = st.columns(min(3, len(cats)))
        for i, cat in enumerate(cats):
            with cols_ui[i % 3]:
                vc  = df[cat].value_counts().reset_index()
                vc.columns = [cat, "count"]
                fig = px.bar(vc.head(8), x=cat, y="count",
                             color_discrete_sequence=[COLS[i % len(COLS)]])
                fig.update_layout(height=200, margin=dict(l=0,r=0,t=20,b=0),
                                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  title=dict(text=cat, font=dict(size=13)), showlegend=False)
                fig.update_xaxes(showgrid=False, tickfont_size=9, tickangle=20)
                fig.update_yaxes(showgrid=True, gridcolor="#f0f0f0", tickfont_size=9)
                st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    # ── Preview + export ──────────────────────
    st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
    with st.expander("👁 Preview raw data"):
        st.dataframe(df.head(20), use_container_width=True)
 
    csv = df.to_csv(index=False).encode()
    st.download_button("⬇️ Download processed CSV", csv, "datalens_export.csv")