"""
charts.py — Chart and visualization functions
All 10 required chart types implemented.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

# ── Consistent colour palette ──────────────────────────────────────────────
PALETTE = ["#1A6B8A", "#F4A261", "#2EC4B6", "#E9C46A", "#E76F51",
           "#264653", "#A8DADC"]

CONTINENT_COLORS = {
    "Africa":        "#E76F51",
    "Asia":          "#1A6B8A",
    "Europe":        "#2EC4B6",
    "North America": "#F4A261",
    "Oceania":       "#A8DADC",
    "South America": "#E9C46A",
}

BG      = "#0F1923"
SURFACE = "#182533"
TEXT    = "#E8EDF2"
ACCENT  = "#2EC4B6"

def _style(fig, ax):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(SURFACE)
    ax.tick_params(colors=TEXT, labelsize=9)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(TEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a3a4a")

def _continent_colors(categories):
    return [CONTINENT_COLORS.get(c, PALETTE[i % len(PALETTE)])
            for i, c in enumerate(categories)]


# 1. PIE CHART ──────────────────────────────────────────────────────────────
def pie_chart(df: pd.DataFrame):
    counts = df["Continent"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor(BG)
    colors = _continent_colors(counts.index.tolist())
    wedges, texts, autotexts = ax.pie(
        counts, labels=None, autopct="%1.1f%%",
        colors=colors, startangle=140,
        wedgeprops=dict(edgecolor=BG, linewidth=2),
        pctdistance=0.82
    )
    for at in autotexts:
        at.set_color(BG); at.set_fontsize(8); at.set_fontweight("bold")
    ax.legend(wedges, counts.index, loc="lower center",
              bbox_to_anchor=(0.5, -0.12), ncol=3,
              fontsize=8, framealpha=0, labelcolor=TEXT)
    ax.set_title("Countries by Continent", color=TEXT, fontsize=13, pad=10)
    plt.tight_layout()
    return fig


# 2. HISTOGRAM ──────────────────────────────────────────────────────────────
def histogram(df: pd.DataFrame):
    counts = df["Continent"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    _style(fig, ax)
    bins = np.arange(0, counts.max() + 10, 5)
    ax.hist(counts.values, bins=bins, color=ACCENT, edgecolor=BG, linewidth=1.5)
    ax.set_xlabel("Number of Countries", color=TEXT)
    ax.set_ylabel("Frequency", color=TEXT)
    ax.set_title("Distribution of Country Counts per Continent", color=TEXT, fontsize=12)
    plt.tight_layout()
    return fig


# 3. LINE CHART ─────────────────────────────────────────────────────────────
def line_chart(df: pd.DataFrame):
    """Alphabetical cumulative count of countries (acts as sequence trend)."""
    sorted_countries = df["Country"].sort_values().reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    _style(fig, ax)
    ax.plot(sorted_countries.index + 1, range(1, len(sorted_countries) + 1),
            color=ACCENT, linewidth=2)
    ax.set_xlabel("Alphabetical Rank", color=TEXT)
    ax.set_ylabel("Cumulative Country Count", color=TEXT)
    ax.set_title("Cumulative Countries (Alphabetical Sequence)", color=TEXT, fontsize=12)
    plt.tight_layout()
    return fig


# 4. BAR CHART ──────────────────────────────────────────────────────────────
def bar_chart(df: pd.DataFrame):
    counts = df["Continent"].value_counts().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    _style(fig, ax)
    colors = _continent_colors(counts.index.tolist())
    bars = ax.barh(counts.index, counts.values, color=colors,
                   edgecolor=BG, linewidth=1)
    for bar, val in zip(bars, counts.values):
        ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", color=TEXT, fontsize=9)
    ax.set_xlabel("Number of Countries", color=TEXT)
    ax.set_title("Countries per Continent", color=TEXT, fontsize=12)
    plt.tight_layout()
    return fig


# 5. SCATTER PLOT ───────────────────────────────────────────────────────────
def scatter_plot(df: pd.DataFrame):
    """Scatter: continent index vs country count — shows spread."""
    counts = df["Continent"].value_counts().reset_index()
    counts.columns = ["Continent", "Count"]
    counts = counts.sort_values("Continent")
    counts["Rank"] = range(1, len(counts) + 1)
    fig, ax = plt.subplots(figsize=(6, 4))
    _style(fig, ax)
    colors = _continent_colors(counts["Continent"].tolist())
    ax.scatter(counts["Rank"], counts["Count"], c=colors, s=120, zorder=3)
    for _, row in counts.iterrows():
        ax.annotate(row["Continent"], (row["Rank"], row["Count"]),
                    textcoords="offset points", xytext=(5, 4),
                    color=TEXT, fontsize=7)
    ax.set_xlabel("Continent (Alphabetical Rank)", color=TEXT)
    ax.set_ylabel("Country Count", color=TEXT)
    ax.set_title("Continent Rank vs Country Count", color=TEXT, fontsize=12)
    plt.tight_layout()
    return fig


# 6. BOX PLOT ───────────────────────────────────────────────────────────────
def box_plot(df: pd.DataFrame):
    """Box plot of name-length distribution per continent."""
    df = df.copy()
    df["NameLength"] = df["Country"].str.len()
    fig, ax = plt.subplots(figsize=(7, 4))
    _style(fig, ax)
    continents = sorted(df["Continent"].unique())
    data = [df[df["Continent"] == c]["NameLength"].values for c in continents]
    colors = _continent_colors(continents)
    bp = ax.boxplot(data, patch_artist=True, notch=False,
                    medianprops=dict(color=BG, linewidth=2))
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color); patch.set_alpha(0.8)
    for element in ["whiskers", "caps", "fliers"]:
        for item in bp[element]:
            item.set_color(TEXT)
    ax.set_xticklabels(continents, rotation=20, ha="right", color=TEXT, fontsize=8)
    ax.set_ylabel("Country Name Length (chars)", color=TEXT)
    ax.set_title("Country Name Length Distribution by Continent", color=TEXT, fontsize=11)
    plt.tight_layout()
    return fig


# 7. HEATMAP ────────────────────────────────────────────────────────────────
def heatmap(df: pd.DataFrame):
    """Heatmap: continents × first-letter groups."""
    df = df.copy()
    df["FirstLetter"] = df["Country"].str[0]
    letter_groups = {
        "A–D": list("ABCD"),
        "E–H": list("EFGH"),
        "I–L": list("IJKL"),
        "M–P": list("MNOP"),
        "Q–T": list("QRST"),
        "U–Z": list("UVWXYZ"),
    }
    continents = sorted(df["Continent"].unique())
    matrix = pd.DataFrame(0, index=continents, columns=letter_groups.keys())
    for grp, letters in letter_groups.items():
        sub = df[df["FirstLetter"].isin(letters)]
        for cont, cnt in sub["Continent"].value_counts().items():
            if cont in matrix.index:
                matrix.loc[cont, grp] = cnt
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor(BG)
    sns.heatmap(matrix, annot=True, fmt="d", cmap="YlOrRd",
                linewidths=0.5, linecolor=BG,
                ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_facecolor(SURFACE)
    ax.set_title("Country Name First-Letter Groups per Continent", color=TEXT, fontsize=11)
    ax.tick_params(colors=TEXT, labelsize=9)
    ax.xaxis.label.set_color(TEXT); ax.yaxis.label.set_color(TEXT)
    plt.tight_layout()
    return fig


# 8. AREA CHART ─────────────────────────────────────────────────────────────
def area_chart(df: pd.DataFrame):
    """Stacked area: cumulative countries added alphabetically, by continent."""
    sorted_df = df.sort_values("Country").reset_index(drop=True)
    sorted_df["Index"] = range(1, len(sorted_df) + 1)
    continents = sorted(df["Continent"].unique())
    fig, ax = plt.subplots(figsize=(8, 4))
    _style(fig, ax)
    cum_base = np.zeros(len(sorted_df))
    colors = _continent_colors(continents)
    for cont, color in zip(continents, colors):
        vals = (sorted_df["Continent"] == cont).astype(int).cumsum().values
        ax.fill_between(sorted_df["Index"], cum_base, cum_base + vals,
                        alpha=0.75, color=color, label=cont)
    ax.set_xlabel("Alphabetical Order of Countries", color=TEXT)
    ax.set_ylabel("Cumulative Country Count", color=TEXT)
    ax.set_title("Cumulative Area — Countries Added Alphabetically by Continent",
                 color=TEXT, fontsize=10)
    ax.legend(fontsize=7, framealpha=0, labelcolor=TEXT, ncol=3,
              loc="upper left")
    plt.tight_layout()
    return fig


# 9. COUNT PLOT ─────────────────────────────────────────────────────────────
def count_plot(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    _style(fig, ax)
    order = df["Continent"].value_counts().index.tolist()
    colors = _continent_colors(order)
    sns.countplot(data=df, y="Continent", order=order, hue="Continent",
                  palette=dict(zip(order, colors)), ax=ax, legend=False)
    ax.set_xlabel("Count", color=TEXT)
    ax.set_ylabel("Continent", color=TEXT)
    ax.set_title("Count of Countries per Continent", color=TEXT, fontsize=12)
    for p in ax.patches:
        ax.annotate(f"{int(p.get_width())}",
                    (p.get_width() + 0.3, p.get_y() + p.get_height() / 2),
                    va="center", color=TEXT, fontsize=9)
    plt.tight_layout()
    return fig


# 10. VIOLIN PLOT ───────────────────────────────────────────────────────────
def violin_plot(df: pd.DataFrame):
    df = df.copy()
    df["NameLength"] = df["Country"].str.len()
    fig, ax = plt.subplots(figsize=(8, 4))
    _style(fig, ax)
    continents = sorted(df["Continent"].unique())
    colors = _continent_colors(continents)
    palette = dict(zip(continents, colors))
    sns.violinplot(data=df, x="Continent", y="NameLength", hue="Continent",
                   palette=palette, ax=ax, linewidth=1,
                   inner="box", legend=False)
    ax.set_xticks(range(len(continents)))
    ax.set_xticklabels(continents, rotation=20, ha="right",
                       color=TEXT, fontsize=8)
    ax.set_xlabel("Continent", color=TEXT)
    ax.set_ylabel("Country Name Length", color=TEXT)
    ax.set_title("Distribution of Country Name Lengths by Continent",
                 color=TEXT, fontsize=11)
    plt.tight_layout()
    return fig


# BONUS: PAIR / BUBBLE CHART ────────────────────────────────────────────────
def bubble_chart(df: pd.DataFrame):
    counts = df["Continent"].value_counts().reset_index()
    counts.columns = ["Continent", "Count"]
    counts = counts.sort_values("Continent").reset_index(drop=True)
    counts["AvgNameLen"] = counts["Continent"].apply(
        lambda c: df[df["Continent"] == c]["Country"].str.len().mean()
    )
    fig, ax = plt.subplots(figsize=(7, 5))
    _style(fig, ax)
    colors = _continent_colors(counts["Continent"].tolist())
    scatter = ax.scatter(
        counts["AvgNameLen"], counts["Count"],
        s=counts["Count"] * 20, c=colors, alpha=0.85, edgecolors=BG, linewidth=1.5
    )
    for _, row in counts.iterrows():
        ax.annotate(row["Continent"],
                    (row["AvgNameLen"], row["Count"]),
                    textcoords="offset points", xytext=(6, 4),
                    color=TEXT, fontsize=8)
    ax.set_xlabel("Avg Country Name Length (chars)", color=TEXT)
    ax.set_ylabel("Number of Countries", color=TEXT)
    ax.set_title("Bubble Chart: Continent Size vs. Avg Name Length",
                 color=TEXT, fontsize=11)
    plt.tight_layout()
    return fig
