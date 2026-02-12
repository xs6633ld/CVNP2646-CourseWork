#!/usr/bin/env python3

from pathlib import Path
import shutil
import argparse
import logging
from collections import defaultdict
from datetime import datetime
import json


# ==============================
# Configuration
# ==============================

EXTENSION_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar.gz" ],
    "Executables": [".exe", ".msi", ".sh"],
    "Other": [".scg", ".file", "README", "noextension" ],
}

# ==============================
# Scanner
# ==============================

def scan_directory(base_path: Path) -> list[Path]:
    """Recursively scan directory and return all files."""
    logging.info(f"Scanning directory: {base_path}")
    return [file for file in base_path.rglob("*") if file.is_file()]


# ==============================
# Categorizer
# ==============================

def categorize_files(files: list[Path]) -> dict[str, list[Path]]:
    """Categorize files by extension."""
    categorized = defaultdict(list)

    for file in files:
        extension = file.suffix.lower()
        matched = False

        for category, extensions in EXTENSION_MAP.items():
            if extension in extensions:
                categorized[category].append(file)
                matched = True
                break

        if not matched:
            categorized["Other"].append(file)

    return categorized


# ==============================
# File Mover
# ==============================

def resolve_duplicate(destination: Path) -> Path:
    """Avoid overwriting existing files by renaming duplicates."""
    counter = 1
    new_destination = destination

    while new_destination.exists():
        new_destination = destination.with_stem(
            f"{destination.stem}_{counter}"
        )
        counter += 1

    return new_destination


def move_files(categorized_files: dict[str, list[Path]], base_path: Path, dry_run: bool):
    """Move files into category folders."""
    total_moved = 0

    for category, files in categorized_files.items():
        category_folder = base_path / category
        category_folder.mkdir(exist_ok=True)

        for file in files:
            destination = category_folder / file.name
            destination = resolve_duplicate(destination)

            logging.info(f"Moving: {file} → {destination}")

            if not dry_run:
                shutil.move(str(file), str(destination))

            total_moved += 1

    return total_moved


# ==============================
# Reporter
# ==============================

def generate_report(categorized_files: dict[str, list[Path]], total_moved: int):
    """Generate summary report in console, JSON, and TXT formats."""

    summary = {
        "timestamp": str(datetime.now()),
        "total_files_processed": total_moved,
        "categories": {
            category: len(files)
            for category, files in categorized_files.items()
        }
    }

    # Console Output
    print("\n====== File Organization Report ======")
    for category, count in summary["categories"].items():
        print(f"{category}: {count} files")
    print(f"\nTotal files processed: {total_moved}")
    print(f"Completed at: {summary['timestamp']}")
    print("=======================================\n")

    # JSON Report
    with open("organization_report.json", "w") as json_file:
        json.dump(summary, json_file, indent=4)

    # TXT Report
    with open("organization_report.txt", "w") as txt_file:
        txt_file.write("====== File Organization Report ======\n")
        for category, count in summary["categories"].items():
            txt_file.write(f"{category}: {count} files\n")
        txt_file.write(f"\nTotal files processed: {total_moved}\n")
        txt_file.write(f"Completed at: {summary['timestamp']}\n")
        txt_file.write("=======================================\n")


# ==============================
# Main Orchestrator
# ==============================

def organize_directory(dry_run: bool):
    base_path = Path("test_downloads").resolve()

    if not base_path.exists() or not base_path.is_dir():
        print("Folder 'test_downloads' does not exist.")
        return

    files = scan_directory(base_path)
    categorized = categorize_files(files)
    total_moved = move_files(categorized, base_path, dry_run)
    generate_report(categorized, total_moved)


# ==============================
# CLI Setup
# ==============================

def main():
    parser = argparse.ArgumentParser(description="Organize files by extension.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files"
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    organize_directory(args.dry_run)


if __name__ == "__main__":
    main()
