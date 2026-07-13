"""Build and check a stock portfolio against the live TUNINDEX universe.

Every function here works on plain pandas DataFrames, so it runs on the
committed CSV files and on any updated file with the same columns.
"""
from __future__ import annotations

import pandas as pd


def load_universe(path: str) -> pd.DataFrame:
    """Load the list of companies on the Tunis Stock Exchange."""
    return pd.read_csv(path)


def load_model_portfolio(path: str) -> pd.DataFrame:
    """Load the recommended portfolio, split into core and dividend baskets."""
    return pd.read_csv(path)


def cross_reference_universe(portfolio: pd.DataFrame, universe: pd.DataFrame) -> pd.DataFrame:
    """Flag which recommended companies show up in the live universe list.

    Matching is done on a normalized name (lowercase, spaces and punctuation
    stripped) since the two sources spell some names a bit differently.
    """
    def normalize(name: str) -> str:
        return "".join(ch for ch in name.lower() if ch.isalnum())

    universe_names = {normalize(n) for n in universe["company_name"]}
    result = portfolio.copy()
    result["found_in_universe"] = result["company_name"].apply(
        lambda name: normalize(name) in universe_names
    )
    return result


def basket_composition(portfolio: pd.DataFrame) -> pd.DataFrame:
    """Count how many names sit in each basket (core vs dividend_yield)."""
    return portfolio.groupby("basket").size().reset_index(name="count")


def equal_weight_allocation(portfolio: pd.DataFrame, basket: str | None = None) -> pd.DataFrame:
    """Assign an equal weight to every stock in a basket, or the full list.

    Weights sum to 1.0. Use this as a starting point, not a recommendation.
    """
    subset = portfolio if basket is None else portfolio[portfolio["basket"] == basket]
    n = len(subset)
    if n == 0:
        raise ValueError("no rows match the requested basket")
    weights = subset.copy()
    weights["weight"] = round(1.0 / n, 6)
    return weights[["company_name", "basket", "weight"]]
