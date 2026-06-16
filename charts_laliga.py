"""
charts.py — Chart / Visualization Functions
La Liga EDA Dashboard — Power BI Style, Blue Color Scheme
All 10 required chart types
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import io

# ── Professional Color Palette ────────────────────────────────────────────────
PALETTE = [
    "#1D4ED8", "#0369A1", "#047857", "#6D28D9", "#B45309",
    "#DC2626", "#0284C7", "#16A34A", "#9333EA", "#CA8A04",
    "#1D4ED8", "#0E7490", "#047857", "#6D28D9", "#B45309",
    "#1E40AF", "#155E75", "#065F46", "#4C1D95", "#92400E",
]

BG      = "#FFFFFF"
CARD_BG = "#F1F5F9"
GRID_C  = "#E2E8F0"
TEXT_C  = "#0F172A"
SUB_C   = "#475569"
BLUE    = "#1D4ED8"
CYAN    = "#0369A1"
GREEN   = "#047857"
PURPLE  = "#6D28D9"
AMBER   = "#B45309"


def _style_ax(ax, title, xlabel="", ylabel=""):
    ax.set_facecolor(CARD_BG)
    ax.set_title(title, color=TEXT_C, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, color=SUB_C, fontsize=10, labelpad=6)
    ax.set_ylabel(ylabel, color=SUB_C, fontsize=10, labelpad=6)
    ax.tick_params(colors=SUB_C, labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_C)
    ax.grid(color=GRID_C, linestyle="-", linewidth=0.8, alpha=1)
    ax.set_axisbelow(True)


def _make_fig(figsize=(11, 5)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(BG)
    return fig, ax


def fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor=BG)
    buf.seek(0)
    return buf.getvalue()


# ── 1. Pie Chart — Match Result Distribution ──────────────────────────────────
def chart_pie_results(df):
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    counts = df["Result"].value_counts()
    colors = [BLUE, CYAN, GREEN]
    wedges, texts, autotexts = ax.pie(
        counts, labels=counts.index, autopct="%1.1f%%",
        colors=colors[:len(counts)], startangle=140,
        wedgeprops=dict(edgecolor="white", linewidth=3),
    )
    for t in texts:
        t.set_color(TEXT_C); t.set_fontsize(11); t.set_fontweight("bold")
    for at in autotexts:
        at.set_color("white"); at.set_fontsize(11); at.set_fontweight("bold")
    ax.set_title("Match Result Distribution (Home Win / Away Win / Draw)",
                 color=TEXT_C, fontsize=13, fontweight="bold", pad=14)
    plt.tight_layout()
    return fig


# ── 2. Histogram — Total Goals Distribution ───────────────────────────────────
def chart_histogram_goals(df):
    fig, ax = _make_fig()
    n, bins, patches = ax.hist(df["TotalGoals"], bins=range(0, 12),
                                edgecolor="white", linewidth=1.2)
    cm = plt.cm.Blues
    norm_vals = (n - n.min()) / (n.max() - n.min() + 1e-9)
    for frac, patch in zip(norm_vals, patches):
        patch.set_facecolor(cm(0.4 + frac * 0.5))
    ax.axvline(df["TotalGoals"].mean(), color=CYAN, linestyle="--",
               linewidth=2, label=f"Mean: {df['TotalGoals'].mean():.2f}")
    ax.axvline(df["TotalGoals"].median(), color=GREEN, linestyle="--",
               linewidth=2, label=f"Median: {df['TotalGoals'].median():.0f}")
    _style_ax(ax, "Distribution of Total Goals per Match", "Total Goals", "Number of Matches")
    ax.legend(fontsize=9, framealpha=0.95)
    plt.tight_layout()
    return fig


# ── 3. Line Chart — Goals Trend Over Months ───────────────────────────────────
def chart_line_goals_by_month(df):
    fig, ax = _make_fig(figsize=(11, 5))
    monthly = df.groupby("MonthNum").agg(
        AvgGoals=("TotalGoals", "mean"),
        AvgShots=("TotalShots", "mean"),
        Matches=("TotalGoals", "count"),
    ).reset_index()
    monthly = monthly.sort_values("MonthNum")
    month_labels = {8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec",
                    1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun"}
    monthly["Label"] = monthly["MonthNum"].map(month_labels)

    ax.plot(monthly["Label"], monthly["AvgGoals"], marker="o", color=BLUE,
            linewidth=2.5, markersize=8, markerfacecolor="white",
            markeredgewidth=2.5, label="Avg Goals/Match")
    ax.plot(monthly["Label"], monthly["Matches"] / 10, marker="s", color=CYAN,
            linewidth=2, markersize=6, linestyle="--", markerfacecolor="white",
            markeredgewidth=2, label="Matches / 10")
    _style_ax(ax, "Monthly Trend — Avg Goals & Match Count", "Month", "Value")
    ax.legend(fontsize=9, framealpha=0.95)
    plt.tight_layout()
    return fig


# ── 4. Bar Chart — Goals per Team ─────────────────────────────────────────────
def chart_bar_goals_per_team(df):
    fig, ax = _make_fig(figsize=(13, 5))
    home_goals = df.groupby("HomeTeam")["FTHG"].sum()
    away_goals = df.groupby("AwayTeam")["FTAG"].sum()
    total_goals = (home_goals.add(away_goals, fill_value=0)
                   .sort_values(ascending=False))

    bars = ax.bar(total_goals.index, total_goals.values,
                  color=PALETTE[:len(total_goals)], edgecolor="white", linewidth=0.8)
    _style_ax(ax, "Total Goals Scored by Each Team", "Team", "Total Goals")
    ax.tick_params(axis="x", rotation=45)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"{bar.get_height():.0f}", ha="center", va="bottom",
                color=SUB_C, fontsize=7, fontweight="bold")
    plt.tight_layout()
    return fig


# ── 5. Scatter Plot — Home Shots vs Away Shots ────────────────────────────────
def chart_scatter_shots(df):
    fig, ax = _make_fig(figsize=(10, 6))
    result_colors = {"Home Win": BLUE, "Away Win": GREEN, "Draw": AMBER}
    for result, color in result_colors.items():
        sub = df[df["Result"] == result]
        ax.scatter(sub["HS"], sub["AS"], c=color, label=result,
                   alpha=0.7, s=50, edgecolors="white", linewidth=0.5)
    _style_ax(ax, "Home Shots vs Away Shots by Match Result", "Home Shots", "Away Shots")
    ax.legend(fontsize=9, framealpha=0.95)
    plt.tight_layout()
    return fig


# ── 6. Box Plot — Goals Distribution by Result ────────────────────────────────
def chart_box_goals(df):
    fig, ax = _make_fig(figsize=(11, 5))
    stats = ["FTHG", "FTAG", "TotalGoals", "HS", "AS", "TotalShots"]
    labels = ["Home\nGoals", "Away\nGoals", "Total\nGoals",
              "Home\nShots", "Away\nShots", "Total\nShots"]
    data = [df[c].dropna().values for c in stats]
    bp = ax.boxplot(data, tick_labels=labels, patch_artist=True,
                    medianprops=dict(color="white", linewidth=2.5),
                    whiskerprops=dict(color=SUB_C, linewidth=1.2),
                    capprops=dict(color=BLUE, linewidth=1.5),
                    flierprops=dict(marker="o", alpha=0.4, markersize=4))
    box_colors = [BLUE, CYAN, GREEN, PURPLE, AMBER, "#0284C7"]
    for patch, color in zip(bp["boxes"], box_colors):
        patch.set_facecolor(color); patch.set_alpha(0.75)
    _style_ax(ax, "Distribution of Goals & Shots (Box Plot)", "Stat", "Value")
    plt.tight_layout()
    return fig


# ── 7. Heatmap — Team Goals Scored ────────────────────────────────────────────
def chart_heatmap_team_goals(df):
    fig, ax = _make_fig(figsize=(11, 7))
    num_cols = ["FTHG", "FTAG", "TotalGoals", "HS", "AS",
                "TotalShots", "HY", "AY", "TotalYellow"]
    corr = df[num_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues",
                linewidths=1, linecolor="white", ax=ax,
                annot_kws={"size": 9, "weight": "bold"},
                vmin=-1, vmax=1)
    ax.set_title("Correlation Heatmap — Goals, Shots & Cards",
                 color=TEXT_C, fontsize=13, fontweight="bold", pad=14)
    ax.tick_params(colors=TEXT_C, labelsize=8)
    plt.tight_layout()
    return fig


# ── 8. Area Chart — Cumulative Goals Over Time ────────────────────────────────
def chart_area_cumulative_goals(df):
    fig, ax = _make_fig(figsize=(11, 5))
    daily = df.sort_values("Date").copy()
    daily["CumGoals"] = daily["TotalGoals"].cumsum()
    daily["MatchNum"] = range(1, len(daily)+1)

    ax.fill_between(daily["MatchNum"], daily["CumGoals"],
                    color=BLUE, alpha=0.15)
    ax.plot(daily["MatchNum"], daily["CumGoals"], color=BLUE,
            linewidth=2.5, label="Cumulative Goals")
    ax.fill_between(daily["MatchNum"], daily["TotalGoals"],
                    color=CYAN, alpha=0.3)
    ax.plot(daily["MatchNum"], daily["TotalGoals"], color=CYAN,
            linewidth=1, linestyle="--", alpha=0.7, label="Goals per Match")
    _style_ax(ax, "Cumulative Goals Over the Season", "Match Number", "Goals")
    ax.legend(fontsize=9, framealpha=0.95)
    plt.tight_layout()
    return fig


# ── 9. Count Plot — Wins per Team ─────────────────────────────────────────────
def chart_count_wins(df):
    fig, ax = _make_fig(figsize=(12, 5))
    home_wins = df[df["FTR"] == "H"]["HomeTeam"].value_counts()
    away_wins = df[df["FTR"] == "A"]["AwayTeam"].value_counts()
    total_wins = home_wins.add(away_wins, fill_value=0).sort_values(ascending=False)

    bars = ax.bar(total_wins.index, total_wins.values,
                  color=PALETTE[:len(total_wins)], edgecolor="white", linewidth=0.8)
    _style_ax(ax, "Total Wins per Team (Home + Away)", "Team", "Wins")
    ax.tick_params(axis="x", rotation=45)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f"{bar.get_height():.0f}", ha="center", va="bottom",
                color=SUB_C, fontsize=7, fontweight="bold")
    plt.tight_layout()
    return fig


# ── 10. Violin Plot — Goals Distribution by Result ────────────────────────────
def chart_violin_goals_by_result(df):
    fig, ax = _make_fig(figsize=(10, 6))
    result_order = ["Home Win", "Away Win", "Draw"]
    result_order = [r for r in result_order if r in df["Result"].unique()]
    sns.violinplot(data=df, x="Result", y="TotalGoals", order=result_order,
                   hue="Result", palette=[BLUE, GREEN, AMBER][:len(result_order)],
                   ax=ax, inner="quartile", linewidth=1.5, legend=False)
    _style_ax(ax, "Goals Distribution by Match Result (Violin Plot)",
              "Result", "Total Goals")
    plt.tight_layout()
    return fig
