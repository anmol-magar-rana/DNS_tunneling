"""
This file provides a simplified, offline simulation of a DNS tunneling
detection technique commonly used in SIEM environments.

It demonstrates how DNS queries can be scored using Shannon entropy
to identify subdomains that resemble encoded or exfiltrated data.

This implementation is intentionally minimal and exists to illustrate
detection concepts rather than serve as a production-ready rule.

No network activity is performed. All DNS queries are hardcoded
examples, and execution is fully local and self-contained.

In real SOC environments, entropy-based detection is combined with
additional signals such as baselining, frequency analysis, domain
reputation, and protocol behavior.
"""

import math                             # using log2 to calculate entropy
from collections import Counter         # using counter to track frequencies of characters

# this function calculates the entropy of a subdomain using Shannon's entropy principle
def shannon(word):
    entropy = 0.0
    length = len(word)

    counts = Counter(word)

    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)

    return entropy

# some example queries outbound of the network
dns_queries = [
    "google.com",
    "cdn.cloudflare.com",
    "d2FzZGFzZGZhc2RmYXNk.example.com",
    "JVAVINCGF5ZGIX3QMZUWYZLDOQQGS3TH.example.com"
]

# check every single query
for query in dns_queries:
    subdomain = query.split(".")[0]
    entropy = shannon(subdomain)

    # set value of 4, changable according to risk tolerance
    if entropy > 4:
        print(f"[ALERT] Possible DNS tunneling: {query}")
        #<quarantine query logic here>
    else:
        print(f"[OK] {query}")



