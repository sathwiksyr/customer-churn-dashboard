# ─────────────────────────────────────────────
# config.py  —  shared constants & Plotly theme
# ─────────────────────────────────────────────
 
# Chart colours
BLUE  = "#378ADD"
RED   = "#E24B4A"
GREEN = "#1D9E75"
GRAY  = "#888780"
 
# Login credentials  (change before deploying!)
VALID_USERNAME = "admin"
VALID_PASSWORD = "1234"
 
# Plotly layout helper
def clean_fig(fig, height=280):
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", size=12, color="#555"),
        showlegend=False,
    )
    fig.update_xaxes(showgrid=False, linecolor="#eaeaea", tickfont_size=11)
    fig.update_yaxes(
        showgrid=True, gridcolor="#f0f0f0",
        linecolor="rgba(0,0,0,0)", tickfont_size=11
    )
    return fig