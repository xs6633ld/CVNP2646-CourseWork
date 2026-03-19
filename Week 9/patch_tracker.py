import json
from datetime import datetime
from collections import Counter

# =========================
# Part 1: Data Loading
# =========================

def load_inventory(filepath):
    """
    Load host inventory from JSON file.
    Returns a list of host dictionaries.
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def calculate_days_since_patch(host):
    """
    Calculate days since last patch for a host.
    """
    patch_date = datetime.strptime(host['last_patch_date'], '%Y-%m-%d')
    return (datetime.now() - patch_date).days


# =========================
# Part 2: Filtering
# =========================

def filter_by_os(hosts, os_type):
    return [h for h in hosts if os_type.lower() in h['os'].lower()]


def filter_by_criticality(hosts, level):
    return [h for h in hosts if h['criticality'] == level]


def filter_by_environment(hosts, env):
    return [h for h in hosts if h['environment'] == env]


def filter_critical_production(hosts):
    return [
        h for h in hosts
        if h['criticality'] == 'critical' and h['environment'] == 'production'
    ]


# =========================
# Part 3: Risk Scoring
# =========================

def calculate_risk_score(host):
    score = 0

    # Criticality
    crit_map = {
        "critical": 40,
        "high": 25,
        "medium": 10,
        "low": 5
    }
    score += crit_map.get(host['criticality'], 0)

    # Patch age
    days = host['days_since_patch']
    if days > 90:
        score += 30
    elif days > 60:
        score += 20
    elif days > 30:
        score += 10

    # Environment
    env_map = {
        "production": 15,
        "staging": 8,
        "development": 3
    }
    score += env_map.get(host['environment'], 0)

    # Tags
    tags = host.get('tags', [])
    if "pci-scope" in tags:
        score += 10
    if "hipaa" in tags:
        score += 10
    if "internet-facing" in tags:
        score += 15

    return min(score, 100)


def get_risk_level(score):
    if score >= 70:
        return "critical"
    elif score >= 50:
        return "high"
    elif score >= 25:
        return "medium"
    else:
        return "low"


# =========================
# Part 4: High-Risk Hosts
# =========================

def get_high_risk_hosts(hosts, threshold=50):
    filtered = [h for h in hosts if h['risk_score'] >= threshold]
    return sorted(filtered, key=lambda h: h['risk_score'], reverse=True)


# =========================
# Part 5: Report Generation
# =========================

def generate_json_report(hosts, high_risk_hosts):
    risk_counts = Counter(h['risk_level'] for h in hosts)

    report = {
        "report_date": datetime.now().isoformat(),
        "report_type": "High Risk Host Assessment",
        "total_hosts": len(hosts),
        "total_high_risk": len(high_risk_hosts),
        "risk_distribution": dict(risk_counts),
        "high_risk_hosts": [
            {
                "hostname": h['hostname'],
                "risk_score": h['risk_score'],
                "risk_level": h['risk_level'],
                "days_since_patch": h['days_since_patch'],
                "criticality": h['criticality'],
                "environment": h['environment'],
                "tags": h.get('tags', [])
            }
            for h in high_risk_hosts
        ]
    }

    return report


def generate_text_summary(hosts, high_risk_hosts):
    risk_counts = Counter(h['risk_level'] for h in hosts)
    total_hosts = len(hosts)
    high_count = len(high_risk_hosts)

    text = []
    text.append("="*64)
    text.append("WEEKLY PATCH COMPLIANCE SUMMARY REPORT")
    text.append("="*64)
    text.append(f"Generated: {datetime.now()}")
    text.append("\nEXECUTIVE SUMMARY")
    text.append("-"*64)
    text.append(f"Total Systems: {total_hosts}")
    text.append(f"High Risk Systems: {high_count} ({(high_count/total_hosts)*100:.1f}%)")

    text.append("\nRISK DISTRIBUTION")
    text.append("-"*64)
    for level in ["critical", "high", "medium", "low"]:
        text.append(f"{level.title():<10}: {risk_counts.get(level,0)}")

    text.append("\nTOP 5 HIGH RISK SYSTEMS")
    text.append("-"*64)

    for i, h in enumerate(high_risk_hosts[:5], 1):
        text.append(f"{i}. {h['hostname']} (Score: {h['risk_score']}, {h['risk_level']})")
        text.append(f"   {h['days_since_patch']} days | {h['environment']} | {', '.join(h.get('tags', []))}")

    text.append("\nRECOMMENDED ACTIONS")
    text.append("-"*64)
    text.append("• Patch critical systems within 48 hours")
    text.append("• Patch high-risk systems within 7 days")
    text.append("• Review patching automation")

    return "\n".join(text)


def generate_html_report(hosts):
    color_map = {
        "critical": "#ff4d4d",
        "high": "#ff944d",
        "medium": "#ffd24d",
        "low": "#70db70"
    }

    html = """
    <html>
    <head>
    <style>
    table {border-collapse: collapse; width: 100%;}
    th, td {padding: 8px; border: 1px solid #ddd;}
    th {background-color: #333; color: white;}
    </style>
    </head>
    <body>
    <h2>Patch Compliance Report</h2>
    <table>
    <tr>
        <th>Hostname</th>
        <th>Score</th>
        <th>Level</th>
        <th>Days</th>
    </tr>
    """

    for h in hosts:
        color = color_map.get(h['risk_level'], "#ffffff")
        html += f"""
        <tr style="background-color:{color}">
            <td>{h['hostname']}</td>
            <td>{h['risk_score']}</td>
            <td>{h['risk_level']}</td>
            <td>{h['days_since_patch']}</td>
        </tr>
        """

    html += "</table></body></html>"
    return html


# =========================
# Part 6: Main Pipeline
# =========================

def analyze_inventory(hosts):
    for host in hosts:
        host['days_since_patch'] = calculate_days_since_patch(host)
        host['risk_score'] = calculate_risk_score(host)
        host['risk_level'] = get_risk_level(host['risk_score'])
    return hosts


# =========================
# Main Execution
# =========================

if __name__ == "__main__":
    inventory = load_inventory("host_inventory.json")
    analyzed_hosts = analyze_inventory(inventory)
    high_risk = get_high_risk_hosts(analyzed_hosts)

    # JSON Report
    json_report = generate_json_report(analyzed_hosts, high_risk)
    with open("high_risk_report.json", "w") as f:
        json.dump(json_report, f, indent=4)

    # Text Report
    with open("patch_summary.txt", "w") as f:
        f.write(generate_text_summary(analyzed_hosts, high_risk))

    # HTML Report
    with open("patch_report.html", "w") as f:
        f.write(generate_html_report(analyzed_hosts))

    print("Script ran successfully!")
    print("Reports generated: high_risk_report.json, patch_summary.txt, patch_report.html")
