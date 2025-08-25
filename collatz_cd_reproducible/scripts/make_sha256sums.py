#!/usr/bin/env python3
import hashlib, os
FILES=[
 "certificates/collatz_refined_R13_S4_summary.json",
 "certificates/collatz_refined_R13_S4_cycle_summary.csv",
 "certificates/collatz_refined_R13_S4_certificate.json",
 "verification/collatz_accel_verify_summary_1e6.json",
 "verification/collatz_accel_verify_top_1e6.csv",
]
def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
with open("SHA256SUMS.txt","w") as out:
    for p in FILES:
        if os.path.exists(p):
            out.write(f"{sha256(p)}  {p}\n")
print("Wrote SHA256SUMS.txt")
