"""
This file provides a controlled lab simulation of DNS tunneling
data reconstruction for defensive security research.

It demonstrates how an attacker / analyst could:
- Extract encoded data from observed DNS queries
- Reassemble fragmented subdomain payloads
- Restore Base32 padding
- Decode the original plaintext

This script performs no network activity and does not capture,
send, intercept, or transmit any real data.

All inputs are hardcoded example values, and execution is fully
local and self-contained.

This implementation is intentionally simplified and assumes
ordered input to highlight practical limitations of DNS-based
exfiltration.
"""

import base64               # base32 decoding used

received_chunks = []        # list to store all extracted subdomains in order
# since DNS is through UDP port 53, packets can be lost/not in order, resulting in corrupted data
# attackers may then use sequence numbers, timestamps, checksums, etc to try and mitigate this

# this function takes a list of encoded data and decodes them
def decode_chunks(chunks):
    joined = "".join(chunks)                # rebuild the string of data

    # padding was removed during the encoding process, so it has to be added back before decoding
    length = len(joined)                    # length of the Base32 string
    remainder = length % 8                  # find how far off the length is from a multiple of 8
    missing_padding = (8 - remainder) % 8   # calculate how many padding characters are needed
    padding = "=" * missing_padding         # create the padding string

    decoded = base64.b32decode(joined + padding)

    return decoded.decode()

# example captured DNS queries from PCAPs / Route 53 query logs / etc
queries = [
    "JVAVINCGF5ZGIX3Q.example.com",
    "MZUWYZLDOQQGS3TH.example.com"
]

# for each query, recover the subdomain which is the ciphertext/payload
for q in queries:
    chunk = q.split(".")[0]
    received_chunks.append(chunk)   # store all the plaintext in a list

# reassemble the plaintext
decoded_data = decode_chunks(received_chunks)
print("Reconstructed Data:", decoded_data)
