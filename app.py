"""
app.py — Main Streamlit Dashboard Application
Countries & Continents — EDA Dashboard
Course: Exploratory Data Analysis | Instructor: Ali Hassan Sherazi
"""

import os
import streamlit as st
import pandas as pd

from filters import load_data, apply_all_filters
from charts import (
    pie_chart, histogram, line_chart, bar_chart, scatter_plot,
    box_plot, heatmap, area_chart, count_plot, violin_plot, bubble_chart,
)

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Countries & Continents Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400;600&display=swap');

  html, body, [class*="css"] {
      font-family: 'Inter', sans-serif;
      background-color: #0F1923;
      color: #E8EDF2;
  }
  .main { background-color: #0F1923; }
  section[data-testid="stSidebar"] {
      background-color: #101D2C !important;
      border-right: 1px solid #1e3148;
  }
  .block-container { padding: 1.5rem 2rem; }

  /* KPI Cards */
  .kpi-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
  .kpi-card {
      background: linear-gradient(135deg, #182533 0%, #1e3148 100%);
      border: 1px solid #2a4060;
      border-radius: 12px;
      padding: 1rem 1.4rem;
      flex: 1;
      min-width: 150px;
      text-align: center;
  }
  .kpi-value { font-family: 'Space Mono', monospace; font-size: 2rem; font-weight: 700; color: #2EC4B6; }
  .kpi-label { font-size: 0.75rem; color: #8aa0b8; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }

  /* Section headers */
  .section-title {
      font-family: 'Space Mono', monospace;
      font-size: 0.85rem;
      color: #2EC4B6;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      border-left: 3px solid #2EC4B6;
      padding-left: 10px;
      margin: 1.5rem 0 0.8rem;
  }

  /* Chart cards */
  .chart-card {
      background: #182533;
      border: 1px solid #1e3148;
      border-radius: 10px;
      padding: 0.8rem;
      margin-bottom: 1rem;
  }

  /* Dashboard title */
  .dash-title {
      font-family: 'Space Mono', monospace;
      font-size: 1.8rem;
      font-weight: 700;
      color: #E8EDF2;
      line-height: 1.2;
  }
  .dash-sub {
      color: #5a7a96;
      font-size: 0.85rem;
      margin-top: 0.25rem;
  }
  .accent { color: #2EC4B6; }
</style>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "Countries-Continents.csv")

@st.cache_data
def get_data():
    return load_data(DATA_PATH)

df_raw = get_data()
all_continents = sorted(df_raw["Continent"].unique().tolist())
max_count = int(df_raw["Continent"].value_counts().max())
min_count = int(df_raw["Continent"].value_counts().min())

# ── Sidebar Filters ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 Filters")
    st.divider()

    # Search / Text Filter
    search_kw = st.text_input("🔍 Search Country or Continent", placeholder="e.g. Africa, Brazil…")

    # Category / Multi-Select Filter
    selected_continents = st.multiselect(
        "🌐 Select Continents",
        options=all_continents,
        default=all_continents,
    )

    # Numerical Range Slider
    country_range = st.slider(
        "📊 Filter by Country Count per Continent",
        min_value=0,
        max_value=max_count,
        value=(min_count, max_count),
        step=1,
    )

    st.divider()

    # Reset button
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

    st.markdown("""
    <div style='margin-top:2rem; color:#3a5a76; font-size:0.7rem; line-height:1.6'>
    <b style='color:#2EC4B6'>Dataset</b><br>Countries-Continents.csv<br><br>
    <b style='color:#2EC4B6'>Course</b><br>Exploratory Data Analysis<br><br>
    <b style='color:#2EC4B6'>Instructor</b><br>Ali Hassan Sherazi
    </div>""", unsafe_allow_html=True)

# ── Apply Filters ──────────────────────────────────────────────────────────
df = apply_all_filters(
    df_raw,
    continents=selected_continents if selected_continents else all_continents,
    search=search_kw,
    min_countries=country_range[0],
    max_countries=country_range[1],
)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-title">🌍 Countries &amp; <span class="accent">Continents</span> Dashboard</div>
<div class="dash-sub">
  Exploratory Data Analysis · 194 countries · 6 continents · Interactive visualizations
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────────────────
total_countries   = len(df)
total_continents  = df["Continent"].nunique()
avg_per_continent = round(df["Continent"].value_counts().mean(), 1) if total_continents else 0
largest_continent = df["Continent"].value_counts().idxmax() if total_countries else "—"
largest_count     = df["Continent"].value_counts().max() if total_countries else 0
avg_name_len      = round(df["Country"].str.len().mean(), 1) if total_countries else 0

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-value">{total_countries}</div>
    <div class="kpi-label">Total Countries</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-value">{total_continents}</div>
    <div class="kpi-label">Continents</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-value">{avg_per_continent}</div>
    <div class="kpi-label">Avg Countries/Continent</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-value">{largest_continent}</div>
    <div class="kpi-label">Largest Continent ({largest_count})</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-value">{avg_name_len}</div>
    <div class="kpi-label">Avg Name Length (chars)</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Guard empty DataFrame ──────────────────────────────────────────────────
if df.empty:
    st.warning("⚠️ No data matches your current filters. Please adjust the sidebar filters.")
    st.stop()

# ── Section 1: Distribution ────────────────────────────────────────────────
st.markdown('<div class="section-title">Distribution Overview</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.pyplot(pie_chart(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.pyplot(bar_chart(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Section 2: Frequency & Count ──────────────────────────────────────────
st.markdown('<div class="section-title">Frequency & Count Analysis</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)
with c3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.pyplot(histogram(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.pyplot(count_plot(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Section 3: Trends & Sequences ─────────────────────────────────────────
st.markdown('<div class="section-title">Trends & Sequences</div>', unsafe_allow_html=True)
c5, c6 = st.columns(2)
with c5:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.pyplot(line_chart(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c6:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.pyplot(area_chart(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Section 4: Statistical Depth ──────────────────────────────────────────
st.markdown('<div class="section-title">Statistical Depth</div>', unsafe_allow_html=True)
c7, c8 = st.columns(2)
with c7:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.pyplot(box_plot(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c8:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.pyplot(violin_plot(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Section 5: Correlation & Relationships ────────────────────────────────
st.markdown('<div class="section-title">Correlation & Relationships</div>', unsafe_allow_html=True)
c9, c10 = st.columns(2)
with c9:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.pyplot(heatmap(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c10:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.pyplot(scatter_plot(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Bonus: Bubble Chart ────────────────────────────────────────────────────
st.markdown('<div class="section-title">Bonus — Bubble Chart</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.pyplot(bubble_chart(df), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Raw Data Table ─────────────────────────────────────────────────────────
with st.expander("📋 View Filtered Raw Data"):
    st.dataframe(
        df.reset_index(drop=True),
        use_container_width=True,
        height=300,
    )
    st.caption(f"Showing {len(df)} of {len(df_raw)} records")

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; color:#2a4060; font-size:0.7rem; margin-top:2rem; padding-top:1rem; border-top:1px solid #1e3148'>
  Countries &amp; Continents EDA Dashboard · Exploratory Data Analysis · Ali Hassan Sherazi
</div>
""", unsafe_allow_html=True)
