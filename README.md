# 🌍 Countries & Continents — EDA Dashboard

**Course:** Exploratory Data Analysis  
**Instructor:** Ali Hassan Sherazi  
**Submission Date:** 05-June-2026  
**Dataset:** `Countries-Continents.csv` (DO NOT rename)

---

## Project Overview

A fully functional, professional-grade data visualization dashboard built with **Streamlit**, analyzing the Countries-Continents dataset. The dashboard presents meaningful insights through 10+ chart types, interactive filters, and a clean dark-themed frontend interface.

---

## Installation & Setup

### 1. Clone / unzip the project folder

```bash
cd dashboard_project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`

---

## Project Structure

```
dashboard_project/
├── data/
│   └── Countries-Continents.csv     ← EXACT original file name
├── notebooks/
│   └── analysis.ipynb               ← EDA notebook
├── app.py                           ← Main Streamlit dashboard
├── charts.py                        ← All 10+ chart functions
├── filters.py                       ← Filter & data processing
├── requirements.txt
└── README.md
```

---

## Features

### Charts Implemented (10 Required + 1 Bonus)
| # | Chart Type | Insight |
|---|-----------|---------|
| 1 | Pie Chart | Proportional share of countries per continent |
| 2 | Histogram | Distribution of country counts |
| 3 | Line Chart | Cumulative country sequence |
| 4 | Bar Chart | Countries per continent comparison |
| 5 | Scatter Plot | Continent rank vs count |
| 6 | Box Plot | Name length spread per continent |
| 7 | Heatmap | First-letter group frequency matrix |
| 8 | Area Chart | Stacked cumulative countries (alphabetical) |
| 9 | Count Plot | Categorical frequency count |
| 10 | Violin Plot | Name length probability distribution |
| ★ | Bubble Chart | Size vs average name length (bonus) |

### Filters (Sidebar)
- **Search / Text Filter** — Filter by country or continent name keyword
- **Multi-Select Filter** — Choose one or more continents
- **Numerical Range Slider** — Filter continents by country count range
- **Reset Button** — Clears all filters to default

All filters are linked — every chart updates dynamically when a filter changes.

### KPI Summary Cards
- Total Countries
- Total Continents
- Average Countries per Continent
- Largest Continent
- Average Country Name Length

---

## Key Insights

- **Africa** has the most countries (54), followed by **Europe** (47) and **Asia** (44).
- **South America** has the fewest (12), closely followed by **Oceania** (14).
- Country name lengths vary widely — "Chad" (4 chars) vs "Central African Republic" (24 chars).
- African country names tend to be shorter on average than European ones.
- The heatmap reveals that most continents have countries starting with letters in the A–D and M–P ranges.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| Pandas | Data loading, cleaning, filtering |
| NumPy | Numerical operations |
| Matplotlib | Core chart creation |
| Seaborn | Statistical visualizations |
| Streamlit | Interactive dashboard frontend |
