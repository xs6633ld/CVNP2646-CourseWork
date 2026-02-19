#!/usr/bin/env python3
"""
Authentication Log Analyzer
SOC-Ready Log Parser & Brute Force Detector
"""

import os
import json
import logging
from collections import Counter
from datetime import datetime

# -------------------------
# Automatically Detect Script Directory
# -------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "auth_test.log")
JSON_REPORT = os.path.join(BASE_DIR, "incident_report.json")
TEXT_REPORT = os.path.join(BASE_DIR, "incident_report.txt")

ALERT_THRESHOLD = 5  # Brute force threshold

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------
# Log Parsing
# -------------------------

def parse_log_line_safe(line):
    """Safely parse key=value authentication log lines."""
    try:
        line = line.strip()
        if not line:
            return None

        parts = line.split()

        if len(parts) < 2:
            logging.warning(f"Line too short: {line}")
            return None

        timestamp = parts[0] + " " + parts[1]
        data = {"timestamp": timestamp}

        for pair in parts[2:]:
            if "=" not in pair:
                logging.warning(f"Malformed field skipped: {pair}")
                continue

            key, value = pair.split("=", 1)
            data[key] = value

        return data

    except Exception as e:
        logging.error(f"Failed to parse line: {line}")
        logging.error(f"Exception: {e}")
        return None


# -------------------------
# Detection Logic
# -------------------------

def is_failed_login(data):
    return (
        data.get("event") == "LOGIN" and
        data.get("status") == "FAIL"
    )


# -------------------------
# Log Analysis
# -------------------------

def analyze_log_file(file_path):
    failed_by_user = Counter()
    failed_by_ip = Counter()
    total_failed = 0
    malformed_lines = 0

    if not os.path.exists(file_path):
        logging.error(f"Log file not found at: {file_path}")
        return None

    with open(file_path, "r") as f:
        for line in f:
            data = parse_log_line_safe(line)

            if not data:
                malformed_lines += 1
                continue

            if is_failed_login(data):
                total_failed += 1
                failed_by_user[data.get("user", "UNKNOWN")] += 1
                failed_by_ip[data.get("ip", "UNKNOWN")] += 1

    return {
        "total_failed": total_failed,
        "failed_by_user": failed_by_user,
        "failed_by_ip": failed_by_ip,
        "malformed_lines": malformed_lines
    }


# -------------------------
# Brute Force Detection
# -------------------------

def detect_brute_force(counter, threshold):
    return {
        key: count
        for key, count in counter.items()
        if count >= threshold
    }


# -------------------------
# JSON Report (SIEM Ready)
# -------------------------

def generate_json_report(results):
    report = {
        "report_generated_utc": datetime.utcnow().isoformat() + "Z",
        "log_file": LOG_FILE,
        "summary": {
            "total_failed_logins": results["total_failed"],
            "malformed_lines": results["malformed_lines"]
        },
        "failures_by_user": dict(results["failed_by_user"]),
        "failures_by_ip": dict(results["failed_by_ip"]),
        "suspected_bruteforce_users": detect_brute_force(
            results["failed_by_user"], ALERT_THRESHOLD
        ),
        "suspected_bruteforce_ips": detect_brute_force(
            results["failed_by_ip"], ALERT_THRESHOLD
        )
    }

    with open(JSON_REPORT, "w") as f:
        json.dump(report, f, indent=2)

    logging.info(f"JSON report saved to {JSON_REPORT}")


# -------------------------
# SOC Human-Readable Report
# -------------------------

def generate_text_report(results):
    with open(TEXT_REPORT, "w") as f:
        f.write("=========================================\n")
        f.write("   AUTHENTICATION FAILURE INCIDENT REPORT\n")
        f.write("=========================================\n\n")

        f.write(f"Log File Analyzed: {LOG_FILE}\n")
        f.write(f"Total Failed Logins: {results['total_failed']}\n")
        f.write(f"Malformed Log Entries: {results['malformed_lines']}\n\n")

        f.write("Top Targeted Users:\n")
        for user, count in results["failed_by_user"].most_common():
            f.write(f"  {user}: {count}\n")

        f.write("\nTop Attack Source IP Addresses:\n")
        for ip, count in results["failed_by_ip"].most_common():
            f.write(f"  {ip}: {count}\n")

        f.write(f"\nBrute Force Threshold: {ALERT_THRESHOLD}\n")

    logging.info(f"Text report saved to {TEXT_REPORT}")


# -------------------------
# Main
# -------------------------

def main():
    logging.info("Starting authentication log analysis...")
    logging.info(f"Looking for log file at: {LOG_FILE}")

    results = analyze_log_file(LOG_FILE)

    if not results:
        logging.error("Analysis stopped due to missing log file.")
        return

    generate_json_report(results)
    generate_text_report(results)

    logging.info("Analysis complete.")


if __name__ == "__main__":
    main()