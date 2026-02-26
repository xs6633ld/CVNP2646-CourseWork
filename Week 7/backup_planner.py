import json
import sys
import random
import os
from datetime import datetime, timedelta


# -------------------------------------------------
# LOAD CONFIGURATION
# -------------------------------------------------
def load_config(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File '{filepath}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON format - {e}")
        return None


# -------------------------------------------------
# VALIDATE CONFIGURATION
# -------------------------------------------------
def validate_config(config):
    errors = []

    if "metadata" not in config:
        errors.append("Missing required field: 'metadata'")
    if "sources" not in config:
        errors.append("Missing required field: 'sources'")
    if "destination" not in config:
        errors.append("Missing required field: 'destination'")

    if errors:
        return False, errors

    metadata = config["metadata"]
    sources = config["sources"]
    destination = config["destination"]

    if not isinstance(metadata.get("plan_name"), str):
        errors.append("'plan_name' must be a string")

    if not isinstance(sources, list):
        errors.append("'sources' must be a list")

    if not isinstance(destination, dict):
        errors.append("'destination' must be a dictionary")

    if isinstance(sources, list):
        if len(sources) == 0:
            errors.append("'sources' list cannot be empty")

        for i, source in enumerate(sources):
            if "path" not in source:
                errors.append(f"Source {i}: missing 'path' field")
            elif not source["path"]:
                errors.append(f"Source {i}: 'path' cannot be empty")

    if "base_path" not in destination:
        errors.append("Missing required field: 'destination.base_path'")
    elif not destination["base_path"]:
        errors.append("'destination.base_path' cannot be empty")

    return len(errors) == 0, errors


# -------------------------------------------------
# FAKE FILE NAME GENERATOR
# -------------------------------------------------
def generate_fake_filename(source_name):
    today = datetime.now()
    random_date = today - timedelta(days=random.randint(0, 30))
    date_str = random_date.strftime("%Y-%m-%d")

    base = source_name.lower().replace(" ", "_")
    return f"{base}_{date_str}.log"


# -------------------------------------------------
# DRY-RUN SIMULATION
# -------------------------------------------------
def simulate_backup(config):
    report_lines = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plan_name = config["metadata"]["plan_name"]
    destination = config["destination"]["base_path"]

    total_files = 0
    total_size = 0

    report_lines.append("=" * 60)
    report_lines.append(f"Backup Plan: {plan_name}")
    report_lines.append("Mode: DRY-RUN")
    report_lines.append(f"Timestamp: {timestamp}")
    report_lines.append("=" * 60)
    report_lines.append("")

    for source in config["sources"]:
        report_lines.append(f"Source: {source.get('name', 'Unnamed Source')}")
        report_lines.append(f"Source Path: {source['path']}")
        report_lines.append(f"Destination Path: {destination}")
        report_lines.append("Files:")

        num_files = random.randint(5, 15)

        for _ in range(num_files):
            file_name = generate_fake_filename(source["name"])
            file_size = round(random.uniform(1, 100), 2)

            report_lines.append(f"  - {file_name} ({file_size} MB)")

            total_files += 1
            total_size += file_size

        report_lines.append("")

    report_lines.append("SUMMARY")
    report_lines.append(f"Total Sources: {len(config['sources'])}")
    report_lines.append(f"Total Files: {total_files}")
    report_lines.append(f"Total Size (MB): {round(total_size, 2)}")
    report_lines.append("=" * 60)

    return "\n".join(report_lines)


# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    print("Starting Backup Planner...\n")

    if len(sys.argv) != 2:
        print("Usage: python backup_planner.py <config_file.json>")
        return

    config_file = sys.argv[1]

    config = load_config(config_file)
    if config is None:
        return

    is_valid, errors = validate_config(config)

    if not is_valid:
        print("\nCONFIGURATION VALIDATION FAILED:")
        for error in errors:
            print(f"- {error}")
        return

    print("Configuration validated successfully!\n")

    report_text = simulate_backup(config)

    # Print to console
    print(report_text)

    # Write to file in same directory
    with open("sample_report.txt", "w") as f:
        f.write(report_text)

    print("\nReport successfully saved as 'sample_report.txt'")


if __name__ == "__main__":
    main()
    