"""
filters.py — Filter and data processing functions
"""

import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    """Load and clean the Countries-Continents dataset."""
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()
    df = df.dropna()
    df["Continent"] = df["Continent"].str.strip()
    df["Country"] = df["Country"].str.strip()
    return df


def get_continent_counts(df: pd.DataFrame) -> pd.Series:
    return df["Continent"].value_counts()


def get_country_counts_by_continent(df: pd.DataFrame) -> pd.DataFrame:
    """Return the number of countries per continent as a tidy DataFrame."""
    return (
        df.groupby("Continent", as_index=False)["Country"]
        .count()
        .rename(columns={"Country": "Count"})
    )


def filter_by_continents(df: pd.DataFrame, continents: list) -> pd.DataFrame:
    if not continents:
        return df
    return df[df["Continent"].isin(continents)]


def filter_by_search(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
    if not keyword:
        return df
    kw = keyword.lower()
    mask = (
        df["Country"].str.lower().str.contains(kw, na=False) |
        df["Continent"].str.lower().str.contains(kw, na=False)
    )
    return df[mask]


def filter_by_country_range(df: pd.DataFrame, min_c: int, max_c: int) -> pd.DataFrame:
    """Filter continents that have country count in [min_c, max_c]."""
    counts = df["Continent"].value_counts()
    valid = counts[(counts >= min_c) & (counts <= max_c)].index.tolist()
    return df[df["Continent"].isin(valid)]


def apply_all_filters(
    df: pd.DataFrame,
    continents: list,
    search: str,
    min_countries: int,
    max_countries: int,
) -> pd.DataFrame:
    df = filter_by_continents(df, continents)
    df = filter_by_search(df, search)
    df = filter_by_country_range(df, min_countries, max_countries)
    return df
