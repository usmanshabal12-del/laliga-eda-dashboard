"""
filters.py — Filter & Data Processing Functions
La Liga EDA Dashboard
"""

import pandas as pd


def load_data(filepath: str = "data/SP1.csv") -> pd.DataFrame:
    """Load and clean La Liga dataset."""
    df = pd.read_csv(filepath)

    # Convert Date to datetime
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

    # Add useful derived columns
    df["TotalGoals"]  = df["FTHG"] + df["FTAG"]
    df["TotalShots"]  = df["HS"]   + df["AS"]
    df["TotalYellow"] = df["HY"]   + df["AY"]
    df["TotalRed"]    = df["HR"]   + df["AR"]
    df["Month"]       = df["Date"].dt.month_name()
    df["MonthNum"]    = df["Date"].dt.month

    # Full result labels
    df["Result"] = df["FTR"].map({"H": "Home Win", "A": "Away Win", "D": "Draw"})
    df["HTResult"] = df["HTR"].map({"H": "Home Win", "A": "Away Win", "D": "Draw"})

    return df


def apply_filters(
    df: pd.DataFrame,
    search_text: str = "",
    selected_teams: list = None,
    selected_results: list = None,
    date_from=None,
    date_to=None,
    goals_range: tuple = (0, 20),
    shots_range: tuple = (0, 100),
) -> pd.DataFrame:
    """Apply all filters and return filtered dataframe."""
    filtered = df.copy()

    # Search filter — team name
    if search_text:
        mask = (
            filtered["HomeTeam"].str.contains(search_text, case=False, na=False) |
            filtered["AwayTeam"].str.contains(search_text, case=False, na=False)
        )
        filtered = filtered[mask]

    # Category filter — teams
    if selected_teams:
        mask = (
            filtered["HomeTeam"].isin(selected_teams) |
            filtered["AwayTeam"].isin(selected_teams)
        )
        filtered = filtered[mask]

    # Result filter
    if selected_results:
        filtered = filtered[filtered["Result"].isin(selected_results)]

    # Date range filter
    if date_from:
        filtered = filtered[filtered["Date"] >= pd.Timestamp(date_from)]
    if date_to:
        filtered = filtered[filtered["Date"] <= pd.Timestamp(date_to)]

    # Numerical range — total goals
    filtered = filtered[
        (filtered["TotalGoals"] >= goals_range[0]) &
        (filtered["TotalGoals"] <= goals_range[1])
    ]

    # Numerical range — total shots
    filtered = filtered[
        (filtered["TotalShots"] >= shots_range[0]) &
        (filtered["TotalShots"] <= shots_range[1])
    ]

    return filtered


def get_kpi_stats(df: pd.DataFrame) -> dict:
    """Compute KPI summary values."""
    if len(df) == 0:
        return {k: 0 for k in ["total_matches","total_goals","avg_goals",
                                "home_wins","away_wins","draws",
                                "avg_shots","most_goals_match"]}
    return {
        "total_matches":    len(df),
        "total_goals":      int(df["TotalGoals"].sum()),
        "avg_goals":        round(df["TotalGoals"].mean(), 2),
        "home_wins":        int((df["FTR"] == "H").sum()),
        "away_wins":        int((df["FTR"] == "A").sum()),
        "draws":            int((df["FTR"] == "D").sum()),
        "avg_shots":        round(df["TotalShots"].mean(), 1),
        "most_goals_match": int(df["TotalGoals"].max()),
    }
