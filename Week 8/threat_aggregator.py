import json
from collections import Counter
from datetime import datetime

# -------------------------
# CONFIGURATION
# -------------------------
CONFIDENCE_THRESHOLD = 85
ALLOWED_TYPES = ["ip", "domain"]
ALLOWED_THREAT_LEVELS = ["high", "critical"]

# -------------------------
# LOAD FEEDS
# -------------------------
def load_feed(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# -------------------------
# NORMALIZATION
# -------------------------
def normalize_indicator(ind, source):

    if source == "VendorA":
        return {
            "id": ind["id"],
            "type": ind["type"],
            "value": ind["value"].strip(),
            "confidence": ind["confidence"],
            "threat_level": ind["threat"],
            "first_seen": ind["first_seen"],
            "sources": [source]
        }

    elif source == "VendorB":
        return {
            "id": ind["ioc_id"],
            "type": ind["indicator_type"],
            "value": ind["indicator_value"].strip(),
            "confidence": ind["score"],
            "threat_level": ind["severity"],
            "first_seen": ind["discovered"],
            "sources": [source]
        }

    elif source == "VendorC":
        return {
            "id": ind["threat_id"],
            "type": ind["category"],
            "value": ind["ioc"].strip(),
            "confidence": ind["reliability"],
            "threat_level": ind["risk"],
            "first_seen": ind["seen_at"],
            "sources": [source]
        }

# -------------------------
# VALIDATION
# -------------------------
def validate_indicators(indicators):

    valid = []
    errors = []
    allowed_types = {"ip", "domain", "hash", "url"}

    for ind in indicators:

        try:
            if not all(k in ind for k in ["id","type","value","confidence"]):
                raise ValueError("Missing required field")

            if not (0 <= ind["confidence"] <= 100):
                raise ValueError("Confidence out of range")

            if ind["type"] not in allowed_types:
                raise ValueError("Invalid type")

            if not isinstance(ind["value"], str) or not ind["value"].strip():
                raise ValueError("Invalid value")

            valid.append(ind)

        except Exception as e:
            errors.append(f"{ind.get('id','unknown')}: {str(e)}")

    return valid, len(errors), errors

# -------------------------
# DEDUPLICATION
# -------------------------
def deduplicate_indicators(indicators):

    deduped = {}
    duplicates = 0

    for ind in indicators:
        key = (ind["type"], ind["value"])

        if key not in deduped:
            deduped[key] = ind
        else:
            duplicates += 1

            existing = deduped[key]

            # keep highest confidence
            if ind["confidence"] > existing["confidence"]:
                existing = ind

            existing["sources"] = list(set(existing["sources"] + ind["sources"]))

            deduped[key] = existing

    return list(deduped.values()), duplicates

# -------------------------
# FILTERING
# -------------------------
def filter_indicators(indicators, min_conf, levels, types):

    filtered = [
        i for i in indicators
        if i["confidence"] >= min_conf
        and i["threat_level"] in levels
        and i["type"] in types
    ]

    return filtered

# -------------------------
# FIREWALL OUTPUT
# -------------------------
def transform_to_firewall(indicators):

    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_entries": len(indicators),
        "blocklist": [
            {
                "address": i["value"],
                "action": "block",
                "priority": i["threat_level"],
                "reason": f"Threat level: {i['threat_level']}, Confidence: {i['confidence']}%",
                "sources": i["sources"]
            }
            for i in indicators
        ]
    }

# -------------------------
# SIEM OUTPUT
# -------------------------
def transform_to_siem(indicators):

    return {
        "feed_version": "1.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "indicators": [
            {
                "indicator": i["value"],
                "type": "ipv4" if i["type"] == "ip" else i["type"],
                "confidence": i["confidence"],
                "severity": i["threat_level"],
                "sources": i["sources"],
                "first_seen": i["first_seen"] + "T00:00:00Z"
            }
            for i in indicators
        ]
    }

# -------------------------
# STATISTICS REPORT
# -------------------------
def generate_report(total_loaded, valid_count, error_count, unique_count,
                    duplicates, filtered_count, indicators):

    type_dist = Counter(i["type"] for i in indicators)
    sev_dist = Counter(i["threat_level"] for i in indicators)

    source_counter = Counter()
    for i in indicators:
        for s in i["sources"]:
            source_counter[s] += 1

    report = f"""
================================================================
THREAT INTELLIGENCE AGGREGATION REPORT
================================================================

INPUT SUMMARY
----------------------------------------------------------------
Feeds processed:         3
Total indicators loaded: {total_loaded}
Valid indicators:        {valid_count}
Validation errors:       {error_count}

DEDUPLICATION
----------------------------------------------------------------
Unique indicators:       {unique_count}
Duplicates removed:      {duplicates}

FILTERING
----------------------------------------------------------------
Confidence threshold:    >= {CONFIDENCE_THRESHOLD}
Threat levels:           {", ".join(ALLOWED_THREAT_LEVELS)}
Indicator types:         {", ".join(ALLOWED_TYPES)}
Indicators passing:      {filtered_count}

DISTRIBUTION BY TYPE
----------------------------------------------------------------
""" 

    for k,v in type_dist.items():
        report += f"{k.upper():15}: {v}\n"

    report += "\nDISTRIBUTION BY SEVERITY\n----------------------------------------------------------------\n"

    for k,v in sev_dist.items():
        report += f"{k.capitalize():15}: {v}\n"

    report += "\nTOP SOURCES\n----------------------------------------------------------------\n"

    for src,count in source_counter.most_common():
        report += f"{src:15}: {count}\n"

    return report

# -------------------------
# WRITE OUTPUT FILES
# -------------------------
def write_outputs(firewall, siem, report):

    with open("firewall_blocklist.json","w") as f:
        json.dump(firewall,f,indent=4)

    with open("siem_feed.json","w") as f:
        json.dump(siem,f,indent=4)

    with open("summary_report.txt","w") as f:
        f.write(report)

# -------------------------
# MAIN PIPELINE
# -------------------------
def main():

    feeds = [
        ("vendor_a.json","VendorA","indicators"),
        ("vendor_b.json","VendorB","data"),
        ("vendor_c.json","VendorC","threats")
    ]

    normalized = []
    total_loaded = 0

    for file,source,key in feeds:

        data = load_feed(file)

        for ind in data[key]:
            total_loaded += 1
            normalized.append(normalize_indicator(ind,source))

    valid, error_count, errors = validate_indicators(normalized)

    deduped, duplicates = deduplicate_indicators(valid)

    filtered = filter_indicators(
        deduped,
        CONFIDENCE_THRESHOLD,
        ALLOWED_THREAT_LEVELS,
        ALLOWED_TYPES
    )

    firewall = transform_to_firewall(filtered)
    siem = transform_to_siem(filtered)

    report = generate_report(
        total_loaded,
        len(valid),
        error_count,
        len(deduped),
        duplicates,
        len(filtered),
        filtered
    )

    write_outputs(firewall, siem, report)

    print("Aggregation Complete")
    print(report)


if __name__ == "__main__":
    main()