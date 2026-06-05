"""
app.py — La Liga EDA Dashboard
Power BI Style — Professional Light Theme
Run: python -m streamlit run app.py
"""

import streamlit as st
import pandas as pd

from filters import load_data, apply_filters, get_kpi_stats
from charts import (
    chart_pie_results, chart_histogram_goals,
    chart_line_goals_by_month, chart_bar_goals_per_team,
    chart_scatter_shots, chart_box_goals,
    chart_heatmap_team_goals, chart_area_cumulative_goals,
    chart_count_wins, chart_violin_goals_by_result, fig_to_bytes,
)

st.set_page_config(page_title="La Liga EDA Dashboard", page_icon="",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
* { font-family: 'Roboto', sans-serif; }

.stApp { background-color: #F5F7FA; color: #1E2432; }

[data-testid="stSidebar"] {
    background: #1A2E44;
    border-right: none;
}
[data-testid="stSidebar"] * { color: #B8C7E0 !important; font-size: 13px !important; }
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] b { color: #FFFFFF !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div,
[data-testid="stSidebar"] .stTextInput > div > div > input,
[data-testid="stSidebar"] .stNumberInput > div > div > input,
[data-testid="stSidebar"] .stDateInput > div > div > input {
    background: #26375A !important;
    border: 1px solid #3A4E72 !important;
    color: #E8EEF7 !important;
    border-radius: 6px !important;
}

/* Top Bar */
.top-bar {
    background: white; border-radius: 10px;
    padding: 16px 24px; margin-bottom: 16px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.top-bar-title { font-size: 22px; font-weight: 700; color: #1E2432; }
.top-bar-sub   { font-size: 12px; color: #6B7A99; margin-top: 2px; }
.top-bar-badges { display: flex; gap: 8px; flex-wrap: wrap; }
.tb-badge {
    background: #E0E7FF; border: 1px solid #A5B4FC;
    border-radius: 6px; padding: 4px 12px;
    font-size: 11px; color: #3730A3; font-weight: 600;
}

/* KPI Cards */
.kpi-row {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 12px; margin-bottom: 12px;
}
.kpi-row-2 {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 12px; margin-bottom: 20px;
}
.kpi-card {
    background: white; border-radius: 10px;
    padding: 18px 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    border-bottom: 3px solid #1D4ED8;
    min-height: 100px;
}
.kpi-card.c2 { border-bottom-color: #0369A1; }
.kpi-card.c3 { border-bottom-color: #047857; }
.kpi-card.c4 { border-bottom-color: #6D28D9; }
.kpi-card.c5 { border-bottom-color: #B45309; }
.kpi-card.c6 { border-bottom-color: #075985; }
.kpi-card.c7 { border-bottom-color: #15803D; }
.kpi-card.c8 { border-bottom-color: #7E22CE; }
.kpi-label { font-size: 10px; color: #6B7A99; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
.kpi-value { font-size: 26px; font-weight: 700; color: #0F172A; margin: 6px 0 2px 0; }
.kpi-sub   { font-size: 11px; color: #2563EB; font-weight: 500; }
.kpi-card.c2 .kpi-sub { color: #0891B2; }
.kpi-card.c3 .kpi-sub { color: #059669; }
.kpi-card.c4 .kpi-sub { color: #7C3AED; }
.kpi-card.c5 .kpi-sub { color: #D97706; }
.kpi-card.c6 .kpi-sub { color: #0284C7; }
.kpi-card.c7 .kpi-sub { color: #16A34A; }
.kpi-card.c8 .kpi-sub { color: #9333EA; }

/* Section Header */
.sec-head {
    font-size: 14px; font-weight: 700; color: #1E2432;
    margin: 20px 0 12px 0; padding-bottom: 8px;
    border-bottom: 2px solid #E2E8F0;
    text-transform: uppercase; letter-spacing: 0.5px;
}
.sec-head span { color: #1D4ED8; margin-right: 8px; }

/* Chart Cards */
.chart-card {
    background: white; border-radius: 10px;
    padding: 14px 18px 10px 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    margin-bottom: 4px;
}
.chart-title { font-size: 12px; font-weight: 700; color: #0F172A; margin-bottom: 2px; }
.chart-desc  { font-size: 11px; color: #6B7A99; margin-bottom: 8px; line-height: 1.5; }

/* Insight */
.insight {
    background: #DBEAFE; border-left: 3px solid #1D4ED8;
    border-radius: 0 6px 6px 0; padding: 8px 12px;
    margin-top: 8px; font-size: 11px; color: #1E3A8A; line-height: 1.5;
}
.insight b { color: #1D4ED8; }

.divider { height: 1px; background: #E2E8F0; margin: 4px 0 16px 0; }

/* Download Button */
.stDownloadButton > button {
    background: #1D4ED8 !important; border: none !important;
    color: white !important; border-radius: 6px !important;
    font-size: 11px !important; font-weight: 600 !important;
    padding: 6px 14px !important; width: 100% !important;
}
.stDownloadButton > button:hover { background: #1D4ED8 !important; }
.stButton > button[kind="primary"] {
    background: #1D4ED8 !important; border: none !important;
    color: white !important; border-radius: 6px !important; font-weight: 600 !important;
}

.footer {
    background: white; border-radius: 10px;
    padding: 20px 28px; margin-top: 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08); text-align: center;
}
h1,h2,h3,h4 { color: #1E2432 !important; }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data("SP1.csv")
df_raw = get_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 16px 16px 16px; border-bottom:1px solid #2E4270;'>
        <div style='font-size:20px; font-weight:800; color:white; letter-spacing:1px;'>LA LIGA</div>
        <div style='font-size:11px; color:#6B8CC4; margin-top:2px;'>EDA Dashboard 2023-24</div>
    </div>
    <div style='padding:12px 8px 4px 8px;'>
        <div style='font-size:10px; color:#6B8CC4; text-transform:uppercase;
                    letter-spacing:1px; padding:0 8px; margin-bottom:4px;'>Filters</div>
    </div>""", unsafe_allow_html=True)

    search_text = st.text_input("Search Team", placeholder="e.g. Barcelona")

    all_teams = sorted(set(df_raw["HomeTeam"].unique()) | set(df_raw["AwayTeam"].unique()))
    selected_teams = st.multiselect("Select Team(s)", all_teams, default=[])

    selected_results = st.multiselect("Match Result", ["Home Win", "Away Win", "Draw"], default=[])

    st.markdown("<div style='font-size:11px; color:#6B8CC4; margin-top:8px;'>Date Range</div>", unsafe_allow_html=True)
    date_from = st.date_input("From", value=df_raw["Date"].min().date(), key="dfrom")
    date_to   = st.date_input("To",   value=df_raw["Date"].max().date(), key="dto")

    st.markdown("<div style='font-size:11px; color:#6B8CC4; margin-top:8px;'>Stat Ranges</div>", unsafe_allow_html=True)

    gc1, gc2 = st.columns(2)
    with gc1:
        goals_min = st.number_input("Goals Min", min_value=0, max_value=15, value=0, key="gmin")
    with gc2:
        goals_max = st.number_input("Goals Max", min_value=0, max_value=15, value=15, key="gmax")
    goals_range = (goals_min, goals_max)

    sc1, sc2 = st.columns(2)
    with sc1:
        shots_min = st.number_input("Shots Min", min_value=0, max_value=80, value=0, key="smin")
    with sc2:
        shots_max = st.number_input("Shots Max", min_value=0, max_value=80, value=80, key="smax")
    shots_range = (shots_min, shots_max)

    st.markdown("---")
    if st.button("Reset All Filters", use_container_width=True, type="primary"):
        st.rerun()

    st.markdown("""
    <div style='margin-top:16px; padding:12px; background:#152333;
                border-radius:8px; border:1px solid #2E4270;'>
        <div style='font-size:10px; color:#6B8CC4; line-height:1.8;'>
            Exploratory Data Analysis<br>
            <b style='color:#B8C7E0;'>Ali Hassan Sherazi</b><br>
            Submission: 05-June-2026
        </div>
    </div>""", unsafe_allow_html=True)

# ── Apply Filters ─────────────────────────────────────────────────────────────
df = apply_filters(df_raw,
    search_text=search_text,
    selected_teams=selected_teams if selected_teams else None,
    selected_results=selected_results if selected_results else None,
    date_from=date_from,
    date_to=date_to,
    goals_range=goals_range,
    shots_range=shots_range,
)

# ── Top Bar ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-bar">
    <div>
        <div class="top-bar-title">La Liga EDA Dashboard — Season 2023/24</div>
        <div class="top-bar-sub">Spanish Football League · 380 Matches · 20 Teams · 105 Features</div>
    </div>
    <div class="top-bar-badges">
        <span class="tb-badge">Python</span>
        <span class="tb-badge">Pandas</span>
        <span class="tb-badge">Matplotlib</span>
        <span class="tb-badge">Seaborn</span>
        <span class="tb-badge">Streamlit</span>
        <span class="tb-badge">{len(df)} Matches</span>
    </div>
</div>""", unsafe_allow_html=True)

if len(df) == 0:
    st.error("No matches match your current filters. Please reset and try again.")
    st.stop()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
kpi = get_kpi_stats(df)

st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card">
        <div class="kpi-label">Total Matches</div>
        <div class="kpi-value">{kpi["total_matches"]}</div>
        <div class="kpi-sub">matches analyzed</div>
    </div>
    <div class="kpi-card c2">
        <div class="kpi-label">Total Goals</div>
        <div class="kpi-value">{kpi["total_goals"]}</div>
        <div class="kpi-sub">goals scored</div>
    </div>
    <div class="kpi-card c3">
        <div class="kpi-label">Avg Goals/Match</div>
        <div class="kpi-value">{kpi["avg_goals"]}</div>
        <div class="kpi-sub">per match average</div>
    </div>
    <div class="kpi-card c4">
        <div class="kpi-label">Avg Shots/Match</div>
        <div class="kpi-value">{kpi["avg_shots"]}</div>
        <div class="kpi-sub">combined shots</div>
    </div>
</div>
<div class="kpi-row-2">
    <div class="kpi-card c5">
        <div class="kpi-label">Home Wins</div>
        <div class="kpi-value">{kpi["home_wins"]}</div>
        <div class="kpi-sub">home advantage</div>
    </div>
    <div class="kpi-card c6">
        <div class="kpi-label">Away Wins</div>
        <div class="kpi-value">{kpi["away_wins"]}</div>
        <div class="kpi-sub">away victories</div>
    </div>
    <div class="kpi-card c7">
        <div class="kpi-label">Draws</div>
        <div class="kpi-value">{kpi["draws"]}</div>
        <div class="kpi-sub">drawn matches</div>
    </div>
    <div class="kpi-card c8">
        <div class="kpi-label">Most Goals in Match</div>
        <div class="kpi-value">{kpi["most_goals_match"]}</div>
        <div class="kpi-sub">highest scoring game</div>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Helper ────────────────────────────────────────────────────────────────────
def show_chart(fig, filename, title, desc, insight):
    st.markdown(f"""<div class="chart-card">
        <div class="chart-title">{title}</div>
        <div class="chart-desc">{desc}</div>
    </div>""", unsafe_allow_html=True)
    st.pyplot(fig, use_container_width=True)
    st.download_button("Download Chart", fig_to_bytes(fig),
                       filename, "image/png", key=filename)
    st.markdown(f'<div class="insight"><b>Insight:</b> {insight}</div>',
                unsafe_allow_html=True)

# ═══ SECTION 1 ════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-head"><span>01</span>Distribution &amp; Composition</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    show_chart(chart_pie_results(df), "pie_results.png",
        "Pie Chart — Match Result Distribution",
        "Shows proportional split of Home Wins, Away Wins, and Draws across all matches. Reveals whether home advantage is significant in La Liga 2023/24 season.",
        "Home teams win more frequently (~44% of matches), confirming home advantage in La Liga. Away wins (~28%) are less common than draws (~28%), suggesting away games are difficult.")
with col2:
    show_chart(chart_histogram_goals(df), "histogram_goals.png",
        "Histogram — Total Goals per Match Distribution",
        "Frequency distribution of total goals scored in each match. Blue dashed line shows Mean, green shows Median. Reveals the most common scoreline ranges in La Liga.",
        "Most La Liga matches produce 2-3 goals per game. High-scoring games (5+ goals) are rare. The mean around 2.7 goals/match reflects La Liga's competitive, tactical nature.")

# ═══ SECTION 2 ════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-head"><span>02</span>Trends Over The Season</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    show_chart(chart_line_goals_by_month(df), "line_monthly.png",
        "Line Chart — Monthly Goals Trend",
        "Tracks average goals per match and number of matches played each month throughout the season. Reveals whether goal-scoring increases or decreases at different points in the season.",
        "Goal scoring tends to be higher at the start and end of the season. Mid-season months (December-February) show slightly lower averages, possibly due to congested fixture schedules.")
with col4:
    show_chart(chart_area_cumulative_goals(df), "area_cumulative.png",
        "Area Chart — Cumulative Goals Over Season",
        "Shows cumulative total goals (blue) and per-match goals (cyan dashed) as the season progresses. Reveals the pace of goal-scoring throughout all 380 matches.",
        "Goals accumulate steadily throughout the season. Steeper sections of the curve indicate goal-heavy periods. The total of 1000+ goals shows La Liga is an exciting, attacking league.")

# ═══ SECTION 3 ════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-head"><span>03</span>Team Performance Analysis</div>', unsafe_allow_html=True)
show_chart(chart_bar_goals_per_team(df), "bar_goals_team.png",
    "Bar Chart — Total Goals Scored by Each Team",
    "Compares total goals scored (home + away) by every team in La Liga 2023/24. Numbers on top show exact totals. Reveals the most and least prolific attacking teams in the league.",
    "Top attacking teams significantly outscored the bottom teams. The gap between the top scorer and bottom team reveals the quality difference between La Liga's elite clubs and relegation candidates.")

col5, col6 = st.columns(2)
with col5:
    show_chart(chart_count_wins(df), "count_wins.png",
        "Count Plot — Total Wins per Team",
        "Shows total wins (home + away combined) for each team. Teams are sorted by win count. Directly reflects league standing and overall team quality throughout the season.",
        "The top teams in wins closely mirrors the actual La Liga 2023/24 final standings. A clear gap exists between the top 4-5 teams and the rest, showing the elite nature of Spanish football.")
with col6:
    show_chart(chart_violin_goals_by_result(df), "violin_goals.png",
        "Violin Plot — Goals Distribution by Match Result",
        "Shows the full distribution of total goals for Home Win, Away Win, and Draw matches. Wider sections show where most goals are concentrated. Inner lines show quartiles.",
        "Home wins and Away wins tend to have more total goals than Draws. Draw matches cluster around 1-2 goals showing that when both teams are evenly matched, scoring is more conservative.")

# ═══ SECTION 4 ════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-head"><span>04</span>Shots &amp; Tactical Analysis</div>', unsafe_allow_html=True)
col7, col8 = st.columns(2)
with col7:
    show_chart(chart_scatter_shots(df), "scatter_shots.png",
        "Scatter Plot — Home Shots vs Away Shots by Result",
        "Maps every match by Home Shots (x-axis) vs Away Shots (y-axis), colored by match result. Blue = Home Win, Green = Away Win, Amber = Draw. Reveals tactical patterns between attacking and defensive outcomes.",
        "Home wins cluster in the high home shots area, confirming that shot volume leads to victory. Away wins show high away shots. Draws tend to have more balanced shot counts between both teams.")
with col8:
    show_chart(chart_box_goals(df), "box_stats.png",
        "Box Plot — Distribution of Goals and Shots",
        "Shows statistical spread of key match stats simultaneously. Box = middle 50% (IQR), white line = median, whiskers = range, dots = outliers. Compares variability across goals and shots metrics.",
        "Total Shots has the widest spread and most outliers, showing high variability in attacking play. Goal counts are more tightly distributed. Outliers represent extraordinary high-scoring or high-intensity matches.")

# ═══ SECTION 5 ════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-head"><span>05</span>Correlation Heatmap</div>', unsafe_allow_html=True)
show_chart(chart_heatmap_team_goals(df), "heatmap_corr.png",
    "Heatmap — Correlation Matrix of Goals, Shots and Cards",
    "Shows Pearson correlation coefficient between every pair of numerical match features. Values from -1 to +1. Darker blue = stronger positive correlation. Reveals which stats are mathematically related.",
    "Total Goals strongly correlates with Home Goals and Away Goals (expected). Home Shots and Home Goals are moderately correlated (0.4+), confirming shots lead to goals. Yellow cards show low correlation with goals, meaning aggression does not necessarily produce more scoring.")

# ═══ SECTION 6 ════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-head"><span>06</span>Filtered Data Table</div>', unsafe_allow_html=True)
display_cols = ["Date","HomeTeam","AwayTeam","FTHG","FTAG","Result",
                "TotalGoals","TotalShots","HY","AY","HR","AR"]
st.dataframe(df[display_cols].reset_index(drop=True), use_container_width=True, height=300)

col_info, col_dl = st.columns([3,1])
with col_info:
    st.markdown(f"<p style='color:#6B7A99; font-size:12px; margin-top:6px;'>Showing <b style='color:#2563EB;'>{len(df)}</b> of <b style='color:#2563EB;'>{len(df_raw)}</b> matches · All filters applied</p>", unsafe_allow_html=True)
with col_dl:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "filtered_laliga.csv", "text/csv", key="csv_dl")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div style='font-size:15px; font-weight:700; color:#1E2432;'>La Liga EDA Dashboard — Season 2023/24</div>
    <div style='font-size:11px; color:#6B7A99; margin-top:8px; line-height:2;'>
        <b>Course:</b> Exploratory Data Analysis &nbsp;|&nbsp;
        <b>Instructor:</b> Ali Hassan Sherazi &nbsp;|&nbsp;
        <b>Submission:</b> 05-June-2026<br>
        <b>Dataset:</b> SP1.csv · 380 Matches · 20 Teams · 105 Features &nbsp;|&nbsp;
        <b>Stack:</b> Python · Pandas · Matplotlib · Seaborn · Streamlit
    </div>
</div>""", unsafe_allow_html=True)
