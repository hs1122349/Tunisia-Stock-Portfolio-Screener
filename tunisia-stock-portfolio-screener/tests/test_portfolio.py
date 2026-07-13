"""Unit tests for the portfolio functions. Small in-memory DataFrames only.

Run with: pytest tests/
"""
import pandas as pd
import pytest

from src.portfolio import (
    basket_composition,
    cross_reference_universe,
    equal_weight_allocation,
)


def make_universe():
    return pd.DataFrame({"company_name": ["SFBT", "BIAT", "STAR"], "sector_guess": ["Beverages", "Banking", "Insurance"]})


def make_portfolio():
    return pd.DataFrame({
        "company_name": ["SFBT", "Biat", "Made Up Co"],
        "basket": ["core", "core", "dividend_yield"],
        "rationale": ["a", "b", "c"],
    })


def test_cross_reference_matches_case_insensitive():
    result = cross_reference_universe(make_portfolio(), make_universe())
    assert result.loc[result["company_name"] == "SFBT", "found_in_universe"].iloc[0]
    assert result.loc[result["company_name"] == "Biat", "found_in_universe"].iloc[0]


def test_cross_reference_flags_missing_name():
    result = cross_reference_universe(make_portfolio(), make_universe())
    assert not result.loc[result["company_name"] == "Made Up Co", "found_in_universe"].iloc[0]


def test_basket_composition_counts():
    counts = basket_composition(make_portfolio())
    core_count = counts.loc[counts["basket"] == "core", "count"].iloc[0]
    assert core_count == 2


def test_equal_weight_allocation_sums_to_one():
    weights = equal_weight_allocation(make_portfolio(), basket="core")
    assert weights["weight"].sum() == pytest.approx(1.0)


def test_equal_weight_allocation_rejects_empty_basket():
    with pytest.raises(ValueError):
        equal_weight_allocation(make_portfolio(), basket="not_a_basket")
