

This threat intelligence aggregator takes threat indication data from multiple vendors in different json formats and converts it to one simple format for the rest of the script to process. After the json data is converted, it is then validated to make sure it has all the required data, any duplicates are removed, filters to only process data with a 85 confidence level or higher, only high and critical threats, and only ip and domain types. That processed data is then output into three different types of files. The first one is a json firewall blocklist file, the second is a json SIEM feed file, and the last one is a human readable text file. 


The script is simply run by being in the directory of where the python file is located (week 8), and running the script python threat_aggregator.py. After completion you should see the three reports created. 


Vendor A uses id, type, value, confidence, threat, and first_seen. Vendor B uses ioc_id, indicator_type, indicator_value, score, severity, and discovered. Vendor C used threat_id, category, ioc, reliability, risk, and seen_at. Each section is then converted to a simple format using id, type, value, confidence, threat_level, and first_seen.

Here is how I converted vendor C's data: 

elif source == "VendorC":
        return {
            "id": ind["threat_id"],
            "type": ind["category"],
            "value": ind["ioc"].strip(),
            "confidence": ind["reliability"],
            "threat_level": ind["risk"],
            "first_seen": ind["seen_at"],
            "sources": [source]




This script handles duplicates by deleting them in the DEDUPLICATION section of the script. When data from different or same vendors have the same type and value but different confidence levels, the higher confidence level is kept by:

# keep highest confidence
            if ind["confidence"] > existing["confidence"]:
                existing = ind


This script filters the threat indicators after detecting deduplication. At the top of the script, this is listed:
CONFIDENCE_THRESHOLD = 85
ALLOWED_TYPES = ["ip", "domain"]
ALLOWED_THREAT_LEVELS = ["high", "critical"] 

This ensures only data with at least a confidence level of 85 is scanned, type must match either ip or domain, and threat level must match either high or critical.




The first output, firewall blocklist, shows which ip addresses or domains should be blocked from the firewall. It also shows what the priority was, either critical or high, the reason for why it should be blocked, and from what vendor that ip or domain was found from. 

The second output, SIEM feed, shows the indicator, type, confidence level, severity, and sources of alerts that would appear in a SIEM dashboard. 

The third output, summary report, summarizes the total findings in a human readable format. It shows data like feeds processed, duplicates removed, filters set, etc.



The test feeds from the three different vendors include at least two duplicates, a confidence level of under 85, big mix of different IPs, domains, URLs and hashes, as well as high, critical, medium and low threat levels.


AI helped me to perfect my script, I ran into errors trying to set up my filtering but with the help of AI I was able to find a solution. I also had AI create the different test feeds for me to make sure I had a good mix of different data without making things too complicated. 


One thing that took a lot of thinking but ended up being very simple was how to convert the data from the different vendors to one simple format. I didn't even know where or how to start on this but I had AI give me some examples and I quickly found a solution. 

