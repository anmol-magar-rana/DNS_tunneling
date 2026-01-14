 ## Wireshark Analysis of DNS Tunneling upon running DNS Tunneling Traffic Generator (Lab Simulation).py

The screenshot 'Wireshark PCAP.png' shows DNS A-record queries with long, high-entropy subdomains
indicative of DNS tunneling activity.

Observations:
- Repeated DNS queries to the same domain
- Encoded Base32 payloads embedded in subdomains
- Traffic sent over UDP port 53
- Behavior consistent with DNS-based data exfiltration

All traffic was generated in a controlled lab environment using non-functional
domains (`example.com`).