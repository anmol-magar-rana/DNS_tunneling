"""
Important: this is not a malware, everything done is contained within a safe and controlled environment.

This file simulates what the attackes server that receieves the dns query does:
Extracting encoded data from all queries
Combine all the encoded data
Decode using Base32
Recover the original plaintext
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
print("[+] Reconstructed Data:", decoded_data)
