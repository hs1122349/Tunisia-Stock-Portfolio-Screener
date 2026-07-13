"""Check the Tunisie Valeurs 2025 model portfolio against the live TUNINDEX
universe, and print basket composition and equal-weight allocations.

Usage:
    python run_cross_reference.py
"""
from src.portfolio import (
    basket_composition,
    cross_reference_universe,
    equal_weight_allocation,
    load_model_portfolio,
    load_universe,
)


def main():
    universe = load_universe("data/tunindex_universe.csv")
    portfolio = load_model_portfolio("data/tunisie_valeurs_model_portfolio_2025.csv")

    checked = cross_reference_universe(portfolio, universe)
    print("=== Model portfolio vs live TUNINDEX universe ===")
    print(checked.to_string(index=False))

    missing = checked[~checked["found_in_universe"]]
    if len(missing) > 0:
        print(f"\n{len(missing)} name(s) not matched by exact name in the universe list:")
        print(missing["company_name"].to_string(index=False))
    else:
        print("\nEvery recommended company matches a name in the universe list.")

    print("\n=== Basket composition ===")
    print(basket_composition(portfolio).to_string(index=False))

    print("\n=== Equal-weight allocation, core basket ===")
    print(equal_weight_allocation(portfolio, basket="core").to_string(index=False))

    print("\n=== Equal-weight allocation, dividend_yield basket ===")
    print(equal_weight_allocation(portfolio, basket="dividend_yield").to_string(index=False))


if __name__ == "__main__":
    main()
