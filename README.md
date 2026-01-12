# DNS_tunneling
Exploration of how data can be exfiltrated using DNS tunneling and how to detect them

high level architecture of this project

Client (localhost)
  - Encodes data
  - Wraps it in DNS-like payload
  - Sends via UDP socket
          
Fake DNS Server (localhost)
  - Listens on UDP
  - Parses "query"
  - Extracts encoded data

notes:
No real DNS
No usage of udp port 53 (use e.g. 53535)
No internet traffic
