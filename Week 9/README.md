This script analyzes the os, os version, last patch date, croticality, environment, department, owner, and tags of a workstation and creates risk level score based on what it analyzes. It creates three reports, a json report, text report, and an html report. The json report lists all of what the script scanned with a risk level score with the highest scroes being listed frist. The text report lists the total reports scanned with how many came back as critical, high, medium, and low. The html report creates a color coded report based on the risk level with critical being red, high being orange, and medium being yellow. Patch management is super important for the integrity of your business. The lack of patch management creates an opening for attackers to easily get into your system which you do not want!



This script can be ran by being in the directory of the script and running python patch_tracker.py. If it ran successfuly, you will see this output:
Script ran successfully!
Reports generated: high_risk_report.json, patch_summary.txt, patch_report.html.



Here is the table on how the risk score is calculated:

Factor                         Condition                                    Points


Criticality                    critical / high / medium / low               40 / 25 / 10 / 5

Patch Age                      >90 days / >60 days / >30 days               30 / 20 / 10

Environment                    production / staging / development           +10

PCI Scope                      "pci-scope" in tags                          +10

HIPPAA                         "hippa" in tags                              +10

Internet Facing                "internet-facing" in tags                    +15



This script analyses the most recent patches on workstations and alerts when systems have not been patched in their requirement. It then creates actionable reports which list the critical reports first as that is what you need to prioritse. 



Here is what a successful text report will look like after running the script:

================================================================
WEEKLY PATCH COMPLIANCE SUMMARY REPORT
================================================================
Generated: 2026-03-19 15:15:11.725881

EXECUTIVE SUMMARY
----------------------------------------------------------------
Total Systems: 20
High Risk Systems: 13 (65.0%)

RISK DISTRIBUTION
----------------------------------------------------------------
Critical  : 10
High      : 3
Medium    : 7
Low       : 0

TOP 5 HIGH RISK SYSTEMS
----------------------------------------------------------------
1. WEB-SRV-001 (Score: 100, critical)
   696 days | production | internet-facing, pci-scope
2. WEB-SRV-002 (Score: 100, critical)
   535 days | production | internet-facing
3. DB-SRV-001 (Score: 100, critical)
   609 days | production | pci-scope, hipaa
4. SEC-SRV-001 (Score: 100, critical)
   411 days | production | internet-facing
5. IT-SRV-DC01 (Score: 100, critical)
   674 days | production | internet-facing, pci-scope

RECOMMENDED ACTIONS
----------------------------------------------------------------
� Patch critical systems within 48 hours
� Patch high-risk systems within 7 days
� Review patching automation



Major functions:

load_inventory(filepath) - Load JSON, return list of host dicts

calculate_days_since_patch(host) - Parse date, calculate days

filter_by_os(hosts, os_type) - Filter by OS (partial match)

filter_by_criticality(hosts, level) - Filter by criticality

filter_by_environment(hosts, env) - Filter by environment

calculate_risk_score(host) - Multi-factor scoring (0-100)

get_risk_level(score) - Convert score to level string

get_high_risk_hosts(hosts, threshold) - Filter and sort

analyze_inventory(hosts) - Main pipeline

generate_json_report(hosts, high_risk_hosts) - JSON output

generate_text_summary(hosts, high_risk_hosts) - Text output

generate_html_report(hosts) - HTML table output




Challenges: What was difficult? How did you solve it?

With my test data, I found 10 critical, 3 high, 7 medium, and 0 low risk hosts. The top three prioritie hosts were WEB-SRV-001, WEB-SRV-002, and DB-SRV-001 all with a risk score of 100.



ChatGPT helped me with creating the json and html reports as well as creating the part of the script where it calculated the risk score. 



The biggest challenge with this project was figuring out how to do the risk score calculation. I started trying to do this on my own and was on the right track but got stuck. With the help of AI I was able to complete this part of the script and everything worked sucessfully. 