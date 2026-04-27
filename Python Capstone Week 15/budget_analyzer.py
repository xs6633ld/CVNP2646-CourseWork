import json
import argparse
import logging
from collections import defaultdict
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


class BudgetAnalyzer:
    def __init__(self, input_file):
        self.input_file = input_file
        self.transactions = []
        self.budgets = {}
        self.category_totals = defaultdict(float)
        self.results = {}

    # ----------------------------
    # VALIDATION
    # ----------------------------
    def validate_transaction(self, txn):
        required_fields = ["date", "amount", "category", "description"]

        for field in required_fields:
            if field not in txn:
                logging.warning(f"Missing field '{field}' in transaction: {txn}")
                return False

        # Type checks
        if not isinstance(txn["amount"], (int, float)):
            logging.warning(f"Invalid amount type: {txn}")
            return False

        return True

    # ----------------------------
    # INPUT HANDLING
    # ----------------------------
    def transaction_processing(self):
        try:
            with open(self.input_file, "r") as f:
                data = json.load(f)

            if "transactions" not in data or "budgets" not in data:
                raise ValueError("JSON must contain 'transactions' and 'budgets' keys")

            self.budgets = data["budgets"]

            raw_transactions = data["transactions"]

            for txn in raw_transactions:
                if self.validate_transaction(txn):
                    self.transactions.append(txn)

            logging.info(f"Loaded {len(self.transactions)} valid transactions")

        except FileNotFoundError:
            logging.error("Input file not found.")
            raise
        except json.JSONDecodeError:
            logging.error("Invalid JSON format.")
            raise
        except ValueError as e:
            logging.error(str(e))
            raise

    # ----------------------------
    # PROCESSING
    # ----------------------------
    def spending_aggregation(self):
        for txn in self.transactions:
            self.category_totals[txn["category"]] += txn["amount"]

        logging.info("Spending aggregation complete.")

    def budget_comparison(self):
        comparison = {}

        for category, total in self.category_totals.items():
            budget = self.budgets.get(category)

            if budget is None:
                logging.warning(f"No budget defined for category: {category}")
                budget = 0

            diff = total - budget

            comparison[category] = {
                "total_spent": total,
                "budget": budget,
                "difference": diff
            }

        self.results["comparison"] = comparison

    def overspending_detection(self):
        alerts = []

        for category, data in self.results["comparison"].items():
            if data["difference"] > 0:
                msg = f"🚨 URGENT: Overspending detected in {category} by ${data['difference']}"
                logging.warning(msg)

                alerts.append({
                    "category": category,
                    "overspent_by": data["difference"]
                })

        self.results["alerts"] = alerts

    # ----------------------------
    # OUTPUT
    # ----------------------------
    def output_generation(self, output_file="results.json"):
        total_spent = sum(self.category_totals.values())

        self.results["total_spent"] = total_spent
        self.results["generated_at"] = datetime.now().isoformat()

        try:
            with open(output_file, "w") as f:
                json.dump(self.results, f, indent=4)

            logging.info(f"Results written to {output_file}")

        except PermissionError:
            logging.error("Permission denied when writing output file.")
            raise

    # ----------------------------
    # RUN PIPELINE
    # ----------------------------
    def run(self):
        self.transaction_processing()
        self.spending_aggregation()
        self.budget_comparison()
        self.overspending_detection()
        self.output_generation()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)

    args = parser.parse_args()

    analyzer = BudgetAnalyzer(args.input)
    analyzer.run()


if __name__ == "__main__":
    main()