# collatz_cd_reproducible (bundle)

Reproducible residue-graph certificate for the accelerated Collatz map, matching the paper’s Section 5–6.

## Contents

- `certificates/R13_S4/`
  - `residue_graph_mod_2^17_R13.csv` — graph over odd residues mod 2^17, with capped weights w = min(τ, 13)
  - `cycle_summary.json` — cycles, lengths, mean weights, and whether they include 1
  - `certificate_R13_S4.json` — summary: mu_star, B, uniqueness of minimizer, worst starts
  - `SHA256SUMS.txt` — SHA-256 hashes for the above files
- `scripts/build_certificate.py` — regenerate all artifacts (no dependencies)
- `latex_patches/`
  - `prop_R13S4.tex` — drop-in LaTeX for the concrete certificate proposition
  - `section6_bootstrap.tex` — minimal bootstrap statement aligned with H1–H3

## Certificate summary (R=13, S=4, modulus 2^17)

- Minimum–mean cycle value: **mu_star = 2**
- Global precycle slack: **B = 16**
- Unique minimizer: the fixed point **{1}**

## SHA-256 checksums

```
1c348af0200dbd05e93f59923f77434db61a2eb9639b575ec60daac332d8e40a  residue_graph_mod_2^17_R13.csv
cc46d9f0218c6b2f13660e71919c16a8d56838c6551c1fde94fcaec7c3586356  cycle_summary.json
22992f0f72c72530696cbb9ffaf9d933e7fcb01a11203b6a12010fa9cec8d761  certificate_R13_S4.json
```

## Reproduce

```bash
python3 scripts/build_certificate.py
sha256sum certificates/R13_S4/*  # compare with SHA256SUMS.txt
```

Artifacts were generated on 2025-08-25 03:00:41.
