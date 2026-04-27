import pytest
from final_budget_analyzer import BudgetAnalyzer


# -------------------------
# Normal case
# -------------------------
def test_validate_transaction_valid():
    analyzer = BudgetAnalyzer("dummy.json")
    txn = {
        "date": "2026-04-01",
        "amount": 100,
        "category": "IT",
        "description": "Test"
    }
    assert analyzer.validate_transaction(txn) is True


# -------------------------
# Edge case: missing field
# -------------------------
def test_validate_transaction_missing_field():
    analyzer = BudgetAnalyzer("dummy.json")
    txn = {
        "date": "2026-04-01",
        "amount": 100,
        "category": "IT"
        # missing description
    }
    assert analyzer.validate_transaction(txn) is False


# -------------------------
# Invalid input type
# -------------------------
def test_validate_transaction_invalid_amount():
    analyzer = BudgetAnalyzer("dummy.json")
    txn = {
        "date": "2026-04-01",
        "amount": "invalid",
        "category": "IT",
        "description": "Test"
    }
    assert analyzer.validate_transaction(txn) is False


# -------------------------
# Budget comparison edge case
# -------------------------
def test_budget_comparison_missing_budget():
    analyzer = BudgetAnalyzer("dummy.json")
    analyzer.category_totals = {"Unknown": 500}

    analyzer.budgets = {}
    analyzer.budget_comparison()

    assert analyzer.results["comparison"]["Unknown"]["budget"] == 0