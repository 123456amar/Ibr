import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stablecoins Research Dashboard",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Main background */
  .stApp { background-color: #f5f5f3; }

  /* Hide default Streamlit header / footer */
  #MainMenu, footer, header { visibility: hidden; }

  /* Remove top padding */
  .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

  /* Metric cards */
  .metric-card {
    background: #eeeee9;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.5rem;
  }
  .metric-label { font-size: 12px; color: #777; margin-bottom: 2px; font-family: sans-serif; }
  .metric-value { font-size: 26px; font-weight: 700; color: #1a1a18; font-family: sans-serif; }
  .metric-sub   { font-size: 11px; color: #aaa; margin-top: 2px; font-family: sans-serif; }

  /* Section titles */
  .section-title {
    font-size: 11px;
    font-weight: 700;
    color: #aaa;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 1.4rem;
    margin-bottom: 0.5rem;
    font-family: sans-serif;
  }

  /* Hypothesis badges */
  .badge-green  { background:#EAF3DE; color:#3B6D11; padding:3px 10px; border-radius:6px; font-size:11px; font-weight:700; }
  .badge-amber  { background:#FAEEDA; color:#854F0B; padding:3px 10px; border-radius:6px; font-size:11px; font-weight:700; }
  .badge-red    { background:#FCEBEB; color:#A32D2D; padding:3px 10px; border-radius:6px; font-size:11px; font-weight:700; }

  /* Hyp cards */
  .hyp-card {
    background: #fff;
    border: 0.5px solid rgba(0,0,0,0.1);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    height: 100%;
  }
  .hyp-title { font-size:13px; font-weight:700; color:#1a1a18; margin-bottom:4px; font-family:sans-serif; }
  .hyp-desc  { font-size:12px; color:#777; line-height:1.5; margin-bottom:8px; font-family:sans-serif; }

  /* Reg cards */
  .reg-card {
    background: #fff;
    border: 0.5px solid rgba(0,0,0,0.1);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    height: 100%;
  }
  .reg-country { font-size:14px; font-weight:700; color:#1a1a18; margin-bottom:4px; font-family:sans-serif; }
  .reg-detail  { font-size:11px; color:#777; line-height:1.5; margin-bottom:8px; font-family:sans-serif; }

  /* ANOVA table */
  .anova-card {
    background:#fff;
    border:0.5px solid rgba(0,0,0,0.1);
    border-radius:12px;
    padding:1rem 1.25rem;
  }

  /* Footer */
  .footer {
    margin-top: 2rem;
    font-size: 11px;
    color: #bbb;
    text-align: center;
    font-family: sans-serif;
    padding-bottom: 1rem;
  }
</style>
""", unsafe_allow_html=True)

# ── Colour palette ─────────────────────────────────────────────────────────────
BLUE   = "#378ADD"
GREEN  = "#1D9E75"
PURPLE = "#7F77DD"
ORANGE = "#EF9F27"
RED    = "#E24B4A"
GREY   = "#888780"
TEAL   = "#00B4D8"
NAVY   = "#0D1B3E"

CHART_BG   = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(0,0,0,0.07)"
TICK_COLOR = "#aaa"

def chart_layout(title="", height=260, showlegend=False, ysfx="", xsfx=""):
    return dict(
        title=dict(text=title, font=dict(size=13, color="#1a1a18"), x=0),
        height=height,
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(family="sans-serif", size=11, color=TICK_COLOR),
        showlegend=showlegend,
        margin=dict(l=10, r=10, t=30 if title else 10, b=10),
        xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=TICK_COLOR, size=10),
                   ticksuffix=xsfx),
        yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=TICK_COLOR, size=10),
                   ticksuffix=ysfx),
    )

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<h2 style="font-size:22px;font-weight:700;color:#1a1a18;margin-bottom:2px;font-family:sans-serif;">
  Stablecoins as the Future of Cross-Border Payments
</h2>
<p style="font-size:13px;color:#888;margin-top:0;font-family:sans-serif;">
  Research Dashboard &nbsp;·&nbsp; Amarnath Gowd &nbsp;·&nbsp; MS25GF034
  &nbsp;·&nbsp; SP Jain School of Global Management
</p>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NAV TABS
# ══════════════════════════════════════════════════════════════════════════════
tabs = st.tabs([
    "📊 Overview",
    "📈 Market Growth",
    "⚡ Cost & Speed",
    "🌏 Regional & Regulation",
    "🔬 Statistics",
    "🏢 30-Firm Dataset",
    "🎯 Conclusions",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<p class="section-title">Key numbers at a glance</p>', unsafe_allow_html=True)

    metrics = [
        ("Stablecoin market cap (2025)", "$250B",  "Up from $5B in 2019"),
        ("On-chain volume (2025)",        "$16T",   "16× growth since 2018"),
        ("Avg stablecoin cost",           "1.2%",   "vs 6.6% via banks"),
        ("Best-case settlement",          "0.14h",  "Anchorage Digital (native SC)"),
        ("India remittance inflows",      "$129B",  "World's largest corridor"),
        ("SC firms avg cost",             "1.72%",  "vs 1.96% traditional firms"),
    ]
    cols = st.columns(6)
    for col, (label, value, sub) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">{label}</div>
              <div class="metric-value">{value}</div>
              <div class="metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<p class="section-title">Research at a glance</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        # Adoption barriers
        barriers = pd.DataFrame({
            "Barrier":  ["Regulation unclear", "Trust in reserves", "Cybersecurity", "Bank resistance", "Volatility risk"],
            "Pct":      [65, 55, 40, 35, 30],
            "Color":    [RED, "#D85A30", ORANGE, GREY, PURPLE],
        })
        fig = go.Figure(go.Bar(
            x=barriers["Pct"], y=barriers["Barrier"],
            orientation="h",
            marker_color=barriers["Color"],
            text=[f"{v}%" for v in barriers["Pct"]],
            textposition="outside",
        ))
        fig.update_layout(**chart_layout("Top adoption barriers (survey of 30 firms)",
                                         height=250, xsfx="%"))
        fig.update_xaxes(range=[0, 80])
        fig.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Stablecoin types doughnut
        fig2 = go.Figure(go.Pie(
            labels=["Fiat-backed", "Crypto-based", "Algorithmic"],
            values=[85, 10, 5],
            hole=0.62,
            marker_colors=[BLUE, GREEN, ORANGE],
        ))
        fig2.update_traces(textinfo="label+percent", textfont_size=11)
        fig2.update_layout(**chart_layout("Market share by stablecoin type",
                                          height=250, showlegend=False))
        st.plotly_chart(fig2, use_container_width=True)

    # Use-cases bar
    st.markdown('<p class="section-title">Stablecoin use-case breakdown</p>', unsafe_allow_html=True)
    uc = pd.DataFrame({
        "Use case": ["Trading / DeFi", "Remittance", "B2B Payments", "Savings", "Others"],
        "Pct":      [45, 25, 15, 10, 5],
        "Color":    [BLUE, GREEN, PURPLE, ORANGE, GREY],
    })
    fig3 = go.Figure(go.Bar(
        x=uc["Use case"], y=uc["Pct"],
        marker_color=uc["Color"],
        text=[f"{v}%" for v in uc["Pct"]],
        textposition="outside",
    ))
    fig3.update_layout(**chart_layout("", height=220, ysfx="%"))
    fig3.update_yaxes(range=[0, 55])
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MARKET GROWTH
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<p class="section-title">Stablecoin market cap 2019–2025 (R² = 0.834)</p>', unsafe_allow_html=True)
        mkt = pd.DataFrame({
            "Year":   [2019, 2020, 2021, 2022, 2023, 2024, 2025],
            "Cap_B":  [5, 20, 150, 160, 130, 180, 250],
        })
        fig = go.Figure(go.Bar(
            x=mkt["Year"], y=mkt["Cap_B"],
            marker_color=BLUE,
            marker_line_width=0,
            text=["$"+str(v)+"B" for v in mkt["Cap_B"]],
            textposition="outside",
        ))
        fig.update_layout(**chart_layout("", height=300, ysfx="B"))
        fig.update_yaxes(range=[0, 290])
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<p class="section-title">On-chain stablecoin volume vs SWIFT (R² = 0.992)</p>', unsafe_allow_html=True)
        vol = pd.DataFrame({
            "Year":  [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
            "SC_T":  [1, 2, 4, 7, 9, 11, 13, 16],
            "SWIFT_T": [130, 135, 138, 142, 147, 150, 153, 155],
        })
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=vol["Year"], y=vol["SC_T"],
            name="Stablecoins", line=dict(color=BLUE, width=2.5),
            fill="tozeroy", fillcolor="rgba(55,138,221,0.12)",
            mode="lines+markers", marker=dict(size=5),
        ))
        fig2.add_trace(go.Scatter(
            x=vol["Year"], y=vol["SWIFT_T"],
            name="SWIFT", line=dict(color=GREY, width=2, dash="dash"),
            mode="lines+markers", marker=dict(size=5),
        ))
        fig2.update_layout(**chart_layout("", height=300, showlegend=True, ysfx="T"))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">India remittance corridor</p>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)

    india = pd.DataFrame({
        "Year":   [2019, 2020, 2021, 2022, 2023, 2024],
        "Inflow": [83.3, 83, 87, 100, 115, 129],
        "Cost":   [6.0, 5.8, 5.5, 5.2, 5.0, 4.8],
    })

    with c3:
        fig3 = go.Figure(go.Scatter(
            x=india["Year"], y=india["Inflow"],
            fill="tozeroy", fillcolor="rgba(29,158,117,0.12)",
            line=dict(color=GREEN, width=2.5),
            mode="lines+markers", marker=dict(size=6),
        ))
        fig3.update_layout(**chart_layout("Remittance inflows to India (R² = 0.984)", height=260, ysfx="B"))
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=india["Year"], y=india["Cost"],
            fill="tozeroy", fillcolor="rgba(226,75,74,0.12)",
            line=dict(color=RED, width=2.5),
            mode="lines+markers", marker=dict(size=6),
            name="Actual cost",
        ))
        fig4.add_trace(go.Scatter(
            x=india["Year"], y=[3]*6,
            line=dict(color=GREEN, dash="dash", width=1.5),
            mode="lines", name="UN 3% target",
        ))
        fig4.update_layout(**chart_layout("Avg sending cost to India (R² = 0.984)",
                                          height=260, showlegend=True, ysfx="%"))
        fig4.update_yaxes(range=[0, 8])
        st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — COST & SPEED
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<p class="section-title">Cost of sending $200 internationally</p>', unsafe_allow_html=True)
        cost_df = pd.DataFrame({
            "Method": ["Bank wire", "Western Union", "PayPal", "Stablecoin (avg)", "Stablecoin (best)"],
            "Cost_USD": [18, 14, 10, 2.40, 0.66],
            "Color": [GREY, ORANGE, PURPLE, BLUE, GREEN],
        })
        fig = go.Figure(go.Bar(
            y=cost_df["Method"], x=cost_df["Cost_USD"],
            orientation="h",
            marker_color=cost_df["Color"],
            text=["$"+str(v) for v in cost_df["Cost_USD"]],
            textposition="outside",
        ))
        fig.update_layout(**chart_layout("", height=260, xsfx=""))
        fig.update_xaxes(tickprefix="$", range=[0, 22])
        fig.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<p class="section-title">Settlement time by payment system</p>', unsafe_allow_html=True)
        speed_df = pd.DataFrame({
            "System": ["Correspondent Banking", "SWIFT", "Visa / Mastercard", "Stablecoins (avg SC firm)", "Anchorage Digital"],
            "Hours":  [72, 48, 2, 41.5, 0.14],
            "Color":  ["#D85A30", GREY, PURPLE, BLUE, GREEN],
        })
        fig2 = go.Figure(go.Bar(
            y=speed_df["System"], x=speed_df["Hours"],
            orientation="h",
            marker_color=speed_df["Color"],
            text=[str(v)+"h" for v in speed_df["Hours"]],
            textposition="outside",
        ))
        fig2.update_layout(**chart_layout("", height=260))
        fig2.update_xaxes(ticksuffix="h", range=[0, 85])
        fig2.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

    # Cost % comparison
    st.markdown('<p class="section-title">Transaction cost % — SC firms vs traditional rails</p>', unsafe_allow_html=True)
    pct_df = pd.DataFrame({
        "Category": ["Banks (global avg)", "MTOs (global avg)", "Non-SC firms (study)", "SC firms (study)", "UN 2030 target", "Best SC firm (Adyen)"],
        "Cost_pct":  [8.0, 6.6, 1.96, 1.72, 3.0, 0.33],
        "Color":     [GREY, "#D85A30", ORANGE, BLUE, GREEN, "#1D9E75"],
    })
    fig3 = go.Figure(go.Bar(
        x=pct_df["Category"], y=pct_df["Cost_pct"],
        marker_color=pct_df["Color"],
        text=[str(v)+"%" for v in pct_df["Cost_pct"]],
        textposition="outside",
    ))
    fig3.add_hline(y=3.0, line_dash="dash", line_color=GREEN,
                   annotation_text="UN 3% target", annotation_position="top right")
    fig3.update_layout(**chart_layout("", height=280, ysfx="%"))
    fig3.update_yaxes(range=[0, 10])
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — REGIONAL & REGULATION
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<p class="section-title">Global stablecoin usage by region (Chainalysis 2024)</p>', unsafe_allow_html=True)
    reg_df = pd.DataFrame({
        "Region":  ["North America", "Asia-Pacific", "Europe", "Latin America", "Africa"],
        "Pct":     [35, 30, 20, 10, 5],
        "Color":   [BLUE, GREEN, PURPLE, ORANGE, RED],
    })
    fig = go.Figure(go.Bar(
        x=reg_df["Pct"], y=reg_df["Region"],
        orientation="h",
        marker_color=reg_df["Color"],
        text=[f"{v}%" for v in reg_df["Pct"]],
        textposition="outside",
    ))
    fig.update_layout(**chart_layout("", height=240, xsfx="%"))
    fig.update_xaxes(range=[0, 45])
    fig.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<p class="section-title">Regulatory environment</p>', unsafe_allow_html=True)

    reg_countries = [
        ("🇸🇬", "Singapore",      "MAS Payment Services Act (2023) — clear framework, 1:1 reserves, monthly redemption rights. Leading APAC hub.",                  "badge-green",  "Most progressive"),
        ("🇪🇺", "European Union", "MiCA framework (June 2024) — structured reserve & audit requirements. Growing institutional confidence.",                         "badge-green",  "Well regulated"),
        ("🇺🇸", "United States",  "GENIUS Act (2025) — emerging framework, still pending. North America holds 35% of global stablecoin usage.",                     "badge-amber",  "In progress"),
        ("🇮🇳", "India",          "No formal stablecoin law. 30% crypto tax + e-Rupee CBDC push. Suppressed adoption despite world's largest remittance market.",   "badge-red",    "Restrictive"),
    ]

    cols = st.columns(4)
    for col, (flag, country, detail, badge_cls, badge_txt) in zip(cols, reg_countries):
        with col:
            st.markdown(f"""
            <div class="reg-card">
              <div style="font-size:26px;margin-bottom:6px;">{flag}</div>
              <div class="reg-country">{country}</div>
              <div class="reg-detail">{detail}</div>
              <span class="{badge_cls}">{badge_txt}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown('<p class="section-title">Regulatory timeline</p>', unsafe_allow_html=True)
    timeline = pd.DataFrame({
        "Event": [
            "USDT launched", "USDC launched", "Terra-Luna collapse",
            "FTX crisis", "MAS PSA in force (SG)", "MiCA enacted (EU)", "GENIUS Act proposed (US)"
        ],
        "Year": [2014, 2018, 2022, 2022, 2023, 2024, 2025],
        "Impact": [1, 1, -2, -2, 2, 2, 1],
        "Color": [GREEN, GREEN, RED, RED, GREEN, GREEN, BLUE],
    })
    fig2 = go.Figure(go.Scatter(
        x=timeline["Year"], y=timeline["Impact"],
        mode="markers+text",
        marker=dict(size=14, color=timeline["Color"]),
        text=timeline["Event"],
        textposition="top center",
    ))
    fig2.add_hline(y=0, line_color=GREY, line_width=1)
    fig2.update_layout(**chart_layout("", height=260))
    fig2.update_yaxes(showticklabels=False, showgrid=False)
    fig2.update_xaxes(dtick=1)
    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — STATISTICS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:

    # ANOVA results
    st.markdown('<p class="section-title">ANOVA results</p>', unsafe_allow_html=True)
    anova_df = pd.DataFrame({
        "Test":       ["Cost bands → Transaction cost", "Speed bands → Settlement time", "Cost bands → Cross-border volume"],
        "F-stat":     [90.71, 98.57, 1.099],
        "p-value":    ["< 0.0001", "< 0.0001", "0.348"],
        "Result":     ["✅ Significant", "✅ Significant", "❌ Not significant"],
        "Insight":    [
            "Low (0.61%) vs Med (1.88%) vs High (2.98%) — 5× difference",
            "Fast (3.6 hrs) vs Med (30.9 hrs) vs Slow (60.2 hrs) — 17× difference",
            "High volume does NOT guarantee lower costs",
        ],
    })
    st.dataframe(anova_df, use_container_width=True, hide_index=True)

    # Correlation
    st.markdown('<p class="section-title">Pearson correlation results</p>', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])

    corr_df = pd.DataFrame({
        "Variable pair":          ["SC Support vs Cost", "SC Support vs Speed", "Volume vs Cost", "Market Cap vs Cost"],
        "Pearson r":              [-0.110, 0.051, -0.216, 0.300],
        "Strength":               ["Weak negative", "Negligible", "Moderate negative", "Weak positive"],
        "Hypothesis":             ["H1 — Partial ✓", "H2 — ✗", "H3 — ✓", "H4 — ✗"],
    })
    with c1:
        st.dataframe(corr_df, use_container_width=True, hide_index=True)

    with c2:
        fig_corr = go.Figure(go.Bar(
            x=corr_df["Variable pair"],
            y=corr_df["Pearson r"],
            marker_color=[GREEN if v < 0 else RED for v in corr_df["Pearson r"]],
            text=[str(v) for v in corr_df["Pearson r"]],
            textposition="outside",
        ))
        fig_corr.add_hline(y=0, line_color=GREY, line_width=1)
        fig_corr.update_layout(**chart_layout("", height=220))
        fig_corr.update_yaxes(range=[-0.35, 0.45])
        st.plotly_chart(fig_corr, use_container_width=True)

    # Regression
    st.markdown('<p class="section-title">Regression models</p>', unsafe_allow_html=True)
    reg_df = pd.DataFrame({
        "Model":     [
            "Market cap growth (2019–25)",
            "On-chain volume growth",
            "India remittance cost trend",
            "India remittance inflows",
            "Cost model — 30 firms",
            "Speed model — 30 firms",
        ],
        "R²":        [0.834, 0.992, 0.984, 0.984, 0.057, 0.007],
        "p-value":   ["0.004", "< 0.0001", "< 0.0001", "< 0.0001", "0.456", "0.887"],
        "Slope":     ["+$37B/yr", "+$2.18T/yr", "−0.25%/yr", "+$9.14B/yr", "—", "—"],
        "Significant": ["✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes", "❌ No", "❌ No"],
    })
    st.dataframe(reg_df, use_container_width=True, hide_index=True)

    # R² bar chart
    fig_r2 = go.Figure(go.Bar(
        x=reg_df["Model"],
        y=reg_df["R²"],
        marker_color=[GREEN if v > 0.5 else RED for v in reg_df["R²"]],
        text=[str(v) for v in reg_df["R²"]],
        textposition="outside",
    ))
    fig_r2.add_hline(y=0.05, line_dash="dash", line_color=GREY,
                     annotation_text="Significance threshold ≈ 0.05", annotation_position="top right")
    fig_r2.update_layout(**chart_layout("R² by model", height=260))
    fig_r2.update_yaxes(range=[0, 1.1])
    st.plotly_chart(fig_r2, use_container_width=True)

    # Hypothesis summary
    st.markdown('<p class="section-title">Hypothesis testing results</p>', unsafe_allow_html=True)
    hyps = [
        ("H1 — Cost efficiency",      "SC firms charge less on average (1.72% vs 1.96%). r = −0.110",           "badge-amber", "Partially supported"),
        ("H2 — Settlement speed",     "SC support alone did not reduce average time (41.5h vs 39.1h). p = 0.887","badge-red",   "Not supported"),
        ("H3 — Volume → lower cost",  "Weak economies of scale. r = −0.216, F = 1.099, p = 0.348",              "badge-amber", "Weakly supported"),
        ("H4 — Larger firms cheaper", "Larger firms actually price slightly higher. r = +0.300",                 "badge-red",   "Not supported"),
    ]
    cols = st.columns(4)
    for col, (title, desc, badge_cls, badge_txt) in zip(cols, hyps):
        with col:
            st.markdown(f"""
            <div class="hyp-card">
              <div class="hyp-title">{title}</div>
              <div class="hyp-desc">{desc}</div>
              <span class="{badge_cls}">{badge_txt}</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — 30-FIRM DATASET
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<p class="section-title">Pilot dataset — 30 cross-border payment firms</p>', unsafe_allow_html=True)

    firms = pd.DataFrame({
        "Company":         ["Adyen","Airwallex","Anchorage Digital","Bank of America","Barclays","Binance Pay",
                            "BitPay","Bitso","Circle (USDC)","Coinbase","Deutsche Bank","Gemini",
                            "HSBC","JPMorgan","Kraken","MoneyGram","Moneycorp","Nium","OKX",
                            "PayPal","Paxos","Rapyd","Remitly","Revolut","Ripple (XRP)",
                            "Standard Chartered","Stellar (XLM)","Stripe","Wise","Western Union"],
        "SC Support":      [1,1,1,0,0,1,1,1,1,1,0,1,0,0,1,0,0,1,1,1,1,1,0,1,1,0,1,1,1,0],
        "Cost (%)":        [0.33,1.10,0.50,2.50,2.30,0.10,1.00,1.20,0.80,1.50,2.80,2.50,
                            2.90,2.10,0.90,2.50,2.20,1.00,0.50,2.90,0.50,1.40,1.80,1.10,0.40,
                            2.70,0.30,1.50,0.50,2.80],
        "Settlement (hrs)":[2.0,4.0,0.14,48,48,0.5,1.0,0.5,0.25,1.0,48,68.5,
                            48,24,1.0,48,48,4.0,0.5,24,0.25,6.0,24,2.0,0.08,
                            48,0.08,2.0,3.0,48],
        "CB Volume ($B)":  [50,12,2,200,150,80,5,8,100,60,180,10,
                            220,250,20,30,15,18,70,120,40,25,10,35,90,
                            160,5,80,25,45],
        "Market Cap ($B)": [45,8,3,300,200,60,1,2,10,50,150,5,
                            200,400,10,8,4,5,30,100,5,4,5,25,10,
                            100,2,50,10,12],
    })
    firms["SC Label"] = firms["SC Support"].map({1: "✅ Yes", 0: "❌ No"})

    # Filter
    sc_filter = st.selectbox("Filter by stablecoin support", ["All", "SC firms only", "Non-SC only"])
    if sc_filter == "SC firms only":
        view = firms[firms["SC Support"] == 1]
    elif sc_filter == "Non-SC only":
        view = firms[firms["SC Support"] == 0]
    else:
        view = firms.copy()

    st.dataframe(
        view[["Company", "SC Label", "Cost (%)", "Settlement (hrs)", "CB Volume ($B)", "Market Cap ($B)"]].reset_index(drop=True),
        use_container_width=True, hide_index=True
    )

    st.markdown('<p class="section-title">Cost vs settlement time — all 30 firms</p>', unsafe_allow_html=True)
    fig = px.scatter(
        firms,
        x="Cost (%)", y="Settlement (hrs)",
        color="SC Label",
        size="Market Cap ($B)",
        hover_name="Company",
        hover_data={"CB Volume ($B)": True, "SC Label": False},
        color_discrete_map={"✅ Yes": BLUE, "❌ No": ORANGE},
        size_max=30,
    )
    fig.update_layout(**chart_layout("Bubble size = Market Cap", height=400, showlegend=True))
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<p class="section-title">Cost distribution — SC vs Non-SC</p>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Box(y=firms[firms["SC Support"]==1]["Cost (%)"],
                              name="SC firms", marker_color=BLUE))
        fig2.add_trace(go.Box(y=firms[firms["SC Support"]==0]["Cost (%)"],
                              name="Non-SC firms", marker_color=ORANGE))
        fig2.update_layout(**chart_layout("", height=280, showlegend=True, ysfx="%"))
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        st.markdown('<p class="section-title">Settlement time — SC vs Non-SC</p>', unsafe_allow_html=True)
        fig3 = go.Figure()
        fig3.add_trace(go.Box(y=firms[firms["SC Support"]==1]["Settlement (hrs)"],
                              name="SC firms", marker_color=BLUE))
        fig3.add_trace(go.Box(y=firms[firms["SC Support"]==0]["Settlement (hrs)"],
                              name="Non-SC firms", marker_color=ORANGE))
        fig3.update_layout(**chart_layout("", height=280, showlegend=True, ysfx="h"))
        st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — CONCLUSIONS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<p class="section-title">Key findings</p>', unsafe_allow_html=True)

    findings = [
        (GREEN,  "F1 — Cost advantage confirmed",
         "SC firms avg 1.72% vs 1.96% non-SC. Best-case (Adyen 0.33%) already meets G20/UN <3% target. "
         "Market cap growing $37B/yr (R²=0.834). On-chain volumes = $16T in 2025 — 10.3% of SWIFT."),
        (ORANGE, "F2 — Speed is protocol-specific",
         "Aggregate SC firms: 40.07 hrs avg (vs 39.13 non-SC) — no significant difference. "
         "But Anchorage Digital settles in 0.14 hrs. Protocol-native architecture = transformative. Category alone does not."),
        (BLUE,   "F3 — Volume → cost (H3 supported)",
         "Higher cross-border volume correlates with lower cost (r = −0.216). "
         "Economies of scale are real but modest. Architecture matters more than size."),
        (RED,    "F4 — Regulation is the #1 bottleneck",
         "65% of firms cite regulatory uncertainty as the top barrier. "
         "Singapore (MAS PSA) and EU (MiCA) show clear adoption gains. "
         "India's 30% crypto tax blocks the world's largest remittance corridor."),
    ]

    for color, title, body in findings:
        st.markdown(f"""
        <div style="background:#fff;border-left:4px solid {color};border-radius:10px;
                    padding:0.9rem 1.1rem;margin-bottom:0.7rem;
                    border-top:0.5px solid rgba(0,0,0,0.08);border-right:0.5px solid rgba(0,0,0,0.08);
                    border-bottom:0.5px solid rgba(0,0,0,0.08);">
          <div style="font-size:13px;font-weight:700;color:#1a1a18;margin-bottom:4px;font-family:sans-serif;">{title}</div>
          <div style="font-size:12px;color:#555;line-height:1.6;font-family:sans-serif;">{body}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<p class="section-title">Business implications by stakeholder</p>', unsafe_allow_html=True)
    impl = [
        ("🏦 Banks & FIs",          NAVY,   "Integrate stablecoin rails or partner now. Waiting costs 6% per transaction. Early movers in India–Singapore corridor gain regulatory head start under MAS PSA."),
        ("💻 Fintech Companies",     BLUE,   "Build on/off-ramp infrastructure. The whitespace is in last-mile conversion for India, Philippines, Indonesia — not the stablecoin tech itself."),
        ("🏢 Corporate Treasuries",  TEAL,   "Settle in <1 hr instead of 3 business days. 24/7 operations. Reduced FX costs. Real-time audit trail. These savings are quantifiable today."),
        ("⚖️ Regulators",            ORANGE, "Adopt BIS PDR standard. Countries with clear rules attract capital and companies. India loses $5–6B/yr in potential savings due to policy misalignment."),
        ("🌍 Financial Inclusion",   GREEN,  "Stablecoins at <0.5% vs 6–8% for banks. Smartphone + internet = access to global economy. APAC's 30% share of SC activity reflects the unmet demand."),
    ]
    cols = st.columns(5)
    for col, (title, color, body) in zip(cols, impl):
        with col:
            st.markdown(f"""
            <div style="background:#fff;border-top:3px solid {color};border-radius:10px;
                        padding:0.9rem 1rem;border:0.5px solid rgba(0,0,0,0.1);height:100%;">
              <div style="font-size:13px;font-weight:700;color:#1a1a18;margin-bottom:6px;font-family:sans-serif;">{title}</div>
              <div style="font-size:11px;color:#555;line-height:1.6;font-family:sans-serif;">{body}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<p class="section-title">Way forward — three pillars</p>', unsafe_allow_html=True)
    pillars = [
        (TEAL,   "🔧 Clear & Fair Regulation",       "Adopt the BIS Properly Designed & Regulated (PDR) standard globally. Countries that write the rules first attract the companies and jobs."),
        (GREEN,  "🌐 Better APAC Infrastructure",    "Build on/off-ramp tools for India, Philippines, Indonesia. Close the last-mile gap that prevents migrant workers from accessing stablecoin savings."),
        (ORANGE, "📱 Digital Literacy Programmes",   "Technology is ready. The final barrier is awareness and trust. Targeted education for remittance senders in APAC unlocks the full potential."),
    ]
    cols = st.columns(3)
    for col, (color, title, body) in zip(cols, pillars):
        with col:
            st.markdown(f"""
            <div style="background:{color}18;border:1px solid {color}44;border-radius:12px;
                        padding:1rem 1.1rem;text-align:center;">
              <div style="font-size:14px;font-weight:700;color:#1a1a18;margin-bottom:6px;font-family:sans-serif;">{title}</div>
              <div style="font-size:12px;color:#444;line-height:1.6;font-family:sans-serif;">{body}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
  Stablecoins as the Future of Cross-Border Payments &nbsp;·&nbsp;
  SP Jain School of Global Management &nbsp;·&nbsp; 2025
</div>
""", unsafe_allow_html=True)
