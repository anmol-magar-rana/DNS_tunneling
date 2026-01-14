# DNS_tunneling Simulation and Detection Lab
## Important Disclaimer
This project / home lab is intended strictly for educational security research and defensive detection development. It includes a controlled simulation of DNS tunneling techniques for the purpose of understanding how such activity appears on the network and how it can be detected by SOC analysts.

The DNS tunneling components are proof-of-concept implementations and are not designed for real-world misuse. They do not include persistence, exploitation, privilege escalation, or command-and-control frameworks beyond basic DNS query generation.

This project should only be executed in isolated lab environments or against domains you own or are authorized to test. Use of this project is subject to the terms of the included MIT License.

## Overview
This project provides a controlled lab that demonstrates how DNS tunneling works, why it is fragile for attackers, and how Security Operations Centers can detect it in real environments.

The repository is intentionally split into four small components:

1. Data Exfiltration Simulation – how attackers abuse trusted DNS infrastructure to exfiltrate sensitive data

2. Data Reconstruction – how tunneled data is recovered and why it can fail

3. Detection Logic – one way how SOCs identify may suspicious DNS behavior

4. Wireshark PCAP - Live packets captured and documented on Wireshark upon carrying out the data exfiltration simulation.

All scripts are designed for educational and defensive research only. Guard rails are implemented in 'DNS Tunneling Traffic Generator (Lab Simulation).py' to prevent accidental misuse, and example domains and data are used throughout.

## 1. Data Fxfiltration Simulation - DNS Tunneling Traffic Generator (Lab Simulation).py

This file simulates the attacker-side behavior of DNS tunneling in a controlled lab environment.
Its purpose is to generate representative DNS traffic for analysis and detection testing.

Key defensive insights:
- DNS is often trusted and broadly allowed (UDP/53)
- encoded subdomains tend to have higher entropy than legitimate names
- DNS tunneling is noisy over time and leaves detectable artifacts

Safety controls:
- LAB_MODE must be explicitly enabled
- DRY_RUN is enabled by default to prevent live queries
- uses 'example.com', a domain reserved by IANA for testing and documentation

## 2. Data Reconstruction - dns_decoder.py
This file simulates the post-processing stage of DNS tunneling, where 
captured encoded data is reconstructed from observed DNS queries. 
This file performs no network activity and operates entirely on hardcoded example data.

Insights gained:
- understanding basic reconstruction logic
- partial detection can break attacker workflows
- missing even a single query can corrupt exfiltrated data
- DNS tunneling is fragile in real networks

Some limitations discovered:
- assumes queries arrive in order
- packet loss handling or retransmission has to be built in features as well, especially if using UDP

## 3. Detection Logic - dns_tunnel_detection.py
This file simulates a simple toy SIEM detection rule inspired by real world SOC practices.
This simplified rule exists to illustrate why DNS tunneling is detectable, not to serve as a production SIEM rule.

Overview of the rule:
- it uses Shannon entropy to score DNS subdomains
- this score is then used to try and identidy potential queries that resemble encoded data to be exfiltrated
- the threshold for detection can be changed according to risk tolerance

Insights gained:
- high-entropy subdomains are not automatically malicious — many legitimate services use encoded data in DNS.
- there is no perfect entropy threshold; some malicious traffic may evade detection.
- entropy is a signal, not a verdict. it indicates suspicion, not certainty.
- in real SOC environments, entropy is combined with additional context such as: 
    - baseline behavior
    - query length and frequency
    - NXDOMAIN ratios
    - domain reputation

## 4. Wireshark PCAP - Wireshark PCAP.md & Wireshark PCAP.png
Wireshark PCAP.png shows the screenshot of the captured packets in the network.
Wireshark PCAP.md goes into a little more details on this.