# DNS_tunneling
Exploration of how data can be exfiltrated using DNS tunneling from the attackers side and how to detect them from the defenders side.

This project is purely educational. It does not capture, send, or transmit any data. All code execution is local and fully contained within the files themselves.

This project contains three .py files:

1) dns_encoder.py (fake infected device)
- Encodes data
- Wraps it in DNS-like payload
- Sends via 'A' record lookup request

2) dns_decoder.py (attacker's fake dns server)          
- Listens on UDP
- Parses "query"
- Extracts encoded data

3) dns_tunnel_detection (SOC SIEM detection rule )
- Calculates entropy of subdomains
- Flags any high entropy subdomains
- Stops any suspicious queries from being sent out of the network

