import json

# ---------------------------
# Part 1: Load JSON Config
# ---------------------------
def load_config(filepath):
    """Load a JSON configuration file with error handling."""
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filepath}': {e}")
        return None


# ---------------------------
# Part 2: DriftResult Class
# ---------------------------
class DriftResult:
    """Represents a single configuration drift finding."""

    CRITICAL_KEYWORDS = ['password', 'secret', 'admin', 'root', 'enabled']

    def __init__(self, path, drift_type, baseline_value, current_value):
        self.path = path
        self.drift_type = drift_type
        self.baseline_value = baseline_value
        self.current_value = current_value
        self.severity = self._calculate_severity()

    def _calculate_severity(self):
        for keyword in self.CRITICAL_KEYWORDS:
            if keyword in self.path.lower():
                return "high"

        if self.drift_type == "missing":
            return "medium"

        return "low"

    def __str__(self):
        icons = {"missing": "[-]", "extra": "[+]", "changed": "[~]"}
        icon = icons.get(self.drift_type, "[?]")
        return f"{icon} {self.path} ({self.severity})"

    def to_dict(self):
        return {
            "path": self.path,
            "type": self.drift_type,
            "baseline_value": self.baseline_value,
            "current_value": self.current_value,
            "severity": self.severity
        }

    def is_critical(self):
        return self.severity == "high"


# ---------------------------
# Part 3: Recursive Compare
# ---------------------------
def compare_configs(baseline, current, path=""):
    """Recursively compare two configurations."""
    results = []

    # CASE 1: Dictionaries
    if isinstance(baseline, dict) and isinstance(current, dict):
        baseline_keys = set(baseline.keys())
        current_keys = set(current.keys())

        # Missing keys
        for key in baseline_keys - current_keys:
            full_path = f"{path}.{key}" if path else key
            results.append(DriftResult(full_path, "missing", baseline[key], None))

        # Extra keys
        for key in current_keys - baseline_keys:
            full_path = f"{path}.{key}" if path else key
            results.append(DriftResult(full_path, "extra", None, current[key]))

        # Compare common keys
        for key in baseline_keys & current_keys:
            full_path = f"{path}.{key}" if path else key
            results.extend(compare_configs(baseline[key], current[key], full_path))

    # CASE 2: Lists
    elif isinstance(baseline, list) and isinstance(current, list):
        max_len = max(len(baseline), len(current))

        for i in range(max_len):
            idx_path = f"{path}[{i}]"

            if i >= len(baseline):
                results.append(DriftResult(idx_path, "extra", None, current[i]))
            elif i >= len(current):
                results.append(DriftResult(idx_path, "missing", baseline[i], None))
            else:
                results.extend(compare_configs(baseline[i], current[i], idx_path))

    # CASE 3: Leaf values
    else:
        if baseline != current:
            results.append(DriftResult(path, "changed", baseline, current))

    return results


# ---------------------------
# Part 4: Report Display
# ---------------------------
def display_drift_report(results):
    """Display a formatted configuration drift report."""

    if not results:
        print("✓ No configuration drift detected!")
        return

    print("=" * 60)
    print("CONFIGURATION DRIFT REPORT")
    print("=" * 60)

    # Count by type
    type_counts = {"missing": 0, "extra": 0, "changed": 0}
    for r in results:
        type_counts[r.drift_type] += 1

    # Count by severity
    severity_counts = {"high": 0, "medium": 0, "low": 0}
    for r in results:
        severity_counts[r.severity] += 1

    # Summary
    print("\nSummary:")
    print(f"  Total Drift Findings: {len(results)}")
    print(f"  By Type - Missing: {type_counts['missing']}, "
          f"Extra: {type_counts['extra']}, "
          f"Changed: {type_counts['changed']}")
    print(f"  By Severity - High: {severity_counts['high']}, "
          f"Medium: {severity_counts['medium']}, "
          f"Low: {severity_counts['low']}")

    print("\nDetailed Findings:")
    print("-" * 60)

    for r in results:
        print(r)

        if r.drift_type == "changed":
            print(f"    Baseline: {r.baseline_value}")
            print(f"    Current:  {r.current_value}")
        elif r.drift_type == "missing":
            print(f"    Expected: {r.baseline_value}")
        else:
            print(f"    Found:    {r.current_value}")


# ---------------------------
# Part 5: Main Function
# ---------------------------
def main():
    print("Loading configurations...")

    baseline = load_config("baseline.json")
    current = load_config("current.json")

    if baseline is None or current is None:
        print("Error: Could not load configuration files.")
        return

    print("Comparing configurations...\n")

    results = compare_configs(baseline, current)

    display_drift_report(results)

    # Save report
    if results:
        output = [r.to_dict() for r in results]
        with open("drift_report.json", "w") as f:
            json.dump(output, f, indent=2)
        print("\n✓ Report saved to drift_report.json")


if __name__ == "__main__":
    main()