import json
import argparse
import logging
from collections import defaultdict
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class BudgetAnalyzer:
    def __init__(self, input_file):
        self.input_file = input_file
        self.transactions = []
        self.category_totals = defaultdict(float)
        self.budget_limits = {}
        self.results = {}

    def transaction_processing(self):
        """Read and parse JSON transaction data"""
        try:
            with open(self.input_file, 'r') as f:
                data = json.load(f)

            self.transactions = data.get("transactions", [])
            self.budget_limits = data.get("budgets", {})

            if not self.transactions:
                logging.warning("No transactions found in input file.")

            logging.info(f"Loaded {len(self.transactions)} transactions.")

        except FileNotFoundError:
            logging.error("Input file not found.")
            exit(1)
        except json.JSONDecodeError:
            logging.error("Invalid JSON format.")
            exit(1)

    def spending_aggregation(self):
        """Calculate total spending per category"""
        for txn in self.transactions:
            try:
                category = txn["category"]
                amount = float(txn["amount"])
                self.category_totals[category] += amount
            except KeyError:
                logging.warning(f"Skipping invalid transaction: {txn}")

        logging.info("Completed spending aggregation.")

    def budget_comparison(self):
        """Compare spending against budgets"""
        comparison = {}

        for category, total in self.category_totals.items():
            budget = self.budget_limits.get(category, 0)
            difference = total - budget

            comparison[category] = {
                "total_spent": total,
                "budget": budget,
                "difference": difference
            }

        self.results["comparison"] = comparison
        logging.info("Completed budget comparison.")

    def overspending_detection(self):
        """Detect categories exceeding budget"""
        alerts = []

        for category, data in self.results["comparison"].items():
            if data["difference"] > 0:
                alerts.append({
                    "category": category,
                    "overspent_by": data["difference"]
                })

        self.results["alerts"] = alerts
        logging.info(f"Detected {len(alerts)} overspending categories.")

    def output_generation(self, output_file="results.json"):
        """Generate output JSON file"""
        total_spent = sum(self.category_totals.values())

        self.results["total_spent"] = total_spent
        self.results["generated_at"] = datetime.now().isoformat()

        try:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=4)

            logging.info(f"Results written to {output_file}")

        except Exception as e:
            logging.error(f"Failed to write output: {e}")

    def run(self):
        self.transaction_processing()
        self.spending_aggregation()
        self.budget_comparison()
        self.overspending_detection()
        self.output_generation()


def main():
    parser = argparse.ArgumentParser(description="CLI Budget Analyzer")
    parser.add_argument("--input", required=True, help="Path to input JSON file")

    args = parser.parse_args()

    analyzer = BudgetAnalyzer(args.input)
    analyzer.run()


if __name__ == "__main__":
    main()