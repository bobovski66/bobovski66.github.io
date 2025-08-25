# Collatz CD — Reproducible Certificates

This repository contains all code and data to reproduce the finite certificates used in the paper.

See `scripts/` for code, `certificates/` for lifted-residue certificate outputs, and `verification/` for the finite-check template.

Run:

```
python3 scripts/collatz_certificate.py --R 13 --S 4   --summary certificates/collatz_refined_R13_S4_summary.json   --cycles  certificates/collatz_refined_R13_S4_cycle_summary.csv   --cert    certificates/collatz_refined_R13_S4_certificate.json

python3 scripts/verify_accelerated.py --N 1000000   --summary verification/collatz_accel_verify_summary_1e6.json   --top     verification/collatz_accel_verify_top_1e6.csv

python3 scripts/make_sha256sums.py
```
