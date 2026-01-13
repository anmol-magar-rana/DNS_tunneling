"""
This file aims to simulate a toy SIEM rule that flags potential DNS tunneling attempts

The rule implemented here scores DNS queries based on entropy and flags queries that look like encoded data.
This simulates real logic used in Splunk / Sentinel and other SIEMs
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
        #<quarantine query logic>
    else:
        print(f"[OK] {query}")



