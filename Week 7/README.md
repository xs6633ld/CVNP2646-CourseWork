This planner verifies that the json file meets all of the requirements. If something is missing, it will output what ecatly is missing so it quickly can be fixed. It also creates a report on what files will be reported with a output of what would happen if the json script was ran. The python script makes it so the json script can be ran dry, in other words it outputs the results of the json script without changing anything. 

The script can be ran by using the script "python backup_planner.py *config to be scanned*".

I looked through the web app decide how I would structure my json schema. It includes everything needed for the metadata, sources, destination, and options section. These sections are scanned by the python validator and simulator to make sure everything is there and correct. 


At the metadata section it will check for plan_name, version, created_by, and the description. At the sources section it will check for the name as a string, path as a string, to scan subdirectores (true/false), include_patterns as a list, and exclude_patterns as a list. For the destination section it will check for base_path, creates_timpstamped_folders, and retention_days. For the options section it will check for verify_backups, and max_file_size_mb.

Fake random files and sizes are created by this section of the script:
def generate_fake_filename(source_name):
    today = datetime.now()
    random_date = today - timedelta(days=random.randint(0, 30))
    date_str = random_date.strftime("%Y-%m-%d")

    base = source_name.lower().replace(" ", "_")
    return f"{base}_{date_str}.log"
Using the word "random" is what makes the unique fake files to be generated possible. 

To load and parse the json file I used:
 config = load_config(config_file)
To validate the configuration I used:
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
To perform the dry run I used:
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
To generate the report I used:
 t_text = simulate_backup(config)

    # Print to console
    print(report_text)

    # Write to file in same directory
    with open("sample_report.txt", "w") as f:
        f.write(report_text)repor

    print("\nReport successfully saved as 'sample_report.txt'")
To orchestrate the programs flow I used:
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


I used AI to help me create the validation function, the simulation function, and to help format the report output. In each promt I input all of the requirements for each function making sure that my script would be fully functional. I also read through each script that was output to make sure I understood it and to make sure everything was corrent. 

I created another json file that has the plan_name in the metadata section deleted from it and the paths on the sources sections deleted from it. When I can the python checker it found both error and reported them so they could easily be fixed.

A dumb problem that I can into was when I tried to run the script and nothing happened. I put my script into AI and asked it why my script was not working. Everything that AI told me to do did not work so I reverted my script and took a different plan of investigation. I did a cat command on my python script and there was no output. After thinking on why nothing was output for a few seconds, I realized I needed to do a crtl+s so save the file and the script was then successful. 