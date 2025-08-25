#!/usr/bin/env python3
"""
Build the (R,S) = (13,4) residue-graph certificate for the accelerated Collatz map.
Outputs:
  - certificates/R13_S4/residue_graph_mod_2^17_R13.csv
  - certificates/R13_S4/cycle_summary.json
  - certificates/R13_S4/certificate_R13_S4.json
  - certificates/R13_S4/SHA256SUMS.txt
No external dependencies required.
"""
import json, hashlib, os, time

def v2(x: int) -> int: return (x & -x).bit_length() - 1
def idx_to_res(i): return (i<<1) | 1
def res_to_idx(a): return (a-1) >> 1

def build(R=13, S=4, outdir="certificates/R13_S4"):
    BITS = R+S; MOD = 1<<BITS; N = MOD//2
    taus = [0]*N; w = [0]*N; nxt = [0]*N; nxt_res = [0]*N; res = [0]*N
    for i in range(N):
        a = idx_to_res(i); res[i]=a
        t = v2(3*a+1); taus[i]=t; w[i]=min(t,R)
        nplus = ((3*a+1)>>t) % MOD
        if nplus % 2 == 0: nplus |= 1
        nxt_res[i]=nplus; nxt[i]=res_to_idx(nplus)

    # cycles and mu*
    seen=[False]*N; inc=[False]*N; mu=float("inf"); cycles=[]
    for s in range(N):
        if seen[s]: continue
        path=[]; i=s
        while not seen[i] and not inc[i]:
            inc[i]=True; path.append(i); i=nxt[i]
        if inc[i]:
            k=path.index(i); cyc=path[k:]
            mean=sum(w[x] for x in cyc)/len(cyc); cycles.append((cyc,mean))
            if mean < mu-1e-15: mu=mean
        for x in path: seen[x]=True; inc[x]=False

    # B (max prefix deficit mu*m - sum w) over all starts
    def compute_B(mu):
        maxB=0; worst=[]
        seen=[False]*N
        for s in range(N):
            if seen[s]: continue
            i=s; order=[]; loc={}
            pref=0.0; minpref=0.0
            while i not in loc:
                loc[i]=len(order); order.append(i)
                pref += (mu - w[i])
                if pref < minpref: minpref = pref
                i=nxt[i]
            cs=loc[i]; cyc=order[cs:]
            pref_entry = sum(mu - w[x] for x in order[:cs])
            pref2=0.0; minpref_cyc=0.0
            for x in cyc:
                pref2 += (mu - w[x])
                if pref2 < minpref_cyc: minpref_cyc = pref2
            min_total = min(minpref, pref_entry + minpref_cyc)
            Bstart = -min_total
            if Bstart > maxB + 1e-12: maxB=Bstart; worst=[(s,int(round(Bstart)))]
            elif abs(Bstart - maxB) <= 1e-12: worst.append((s,int(round(Bstart))))
            for x in order: seen[x]=True
        return int(round(maxB)), [(idx_to_res(i), b) for (i,b) in worst]

    B, worst = compute_B(mu)

    os.makedirs(outdir, exist_ok=True)
    csv=os.path.join(outdir, f"residue_graph_mod_2^{BITS}_R{R}.csv")
    with open(csv,"w") as f:
        f.write("residue,next_residue,weight_tau_capped_R,tau_exact,next_index\n")
        for i in range(N):
            f.write(f"{res[i]},{nxt_res[i]},{w[i]},{taus[i]},{nxt[i]}\n")

    cyc_sum=[]
    for cyc,mean in cycles:
        cyc_res = [idx_to_res(x) for x in cyc]
        cyc_sum.append({
            "length": len(cyc),
            "mean_weight": mean,
            "residues": cyc_res[:10] + (["..."] if len(cyc_res)>10 else []),
            "includes_1": 1 in cyc_res,
            "is_minimizer": abs(mean-mu) < 1e-15
        })
    csum=os.path.join(outdir,"cycle_summary.json"); json.dump(cyc_sum, open(csum,"w"), indent=2)

    cert = {
        "modulus_bits": R+S, "modulus": 1<<(R+S), "R": R, "S": S,
        "mu_star": mu, "B": B,
        "unique_min_cycle": sum(1 for _,m in cycles if abs(m-mu)<1e-15)==1,
        "min_cycle_is_fixed_1": any((1 in [idx_to_res(x) for x in cyc]) and abs(mean-mu)<1e-15 for cyc,mean in cycles),
        "worst_starts": [{"residue": r, "B_start": b} for (r,b) in worst],
        "csv_file": os.path.basename(csv),
        "cycle_summary_file": os.path.basename(csum),
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "generator": "build_certificate.py"
    }
    cjson=os.path.join(outdir,"certificate_R13_S4.json"); json.dump(cert, open(cjson,"w"), indent=2)

    def sha256(p):
        h=hashlib.sha256()
        with open(p,"rb") as f:
            for chunk in iter(lambda: f.read(1<<20), b""): h.update(chunk)
        return h.hexdigest()
    shas=os.path.join(outdir,"SHA256SUMS.txt")
    with open(shas,"w") as f:
        for p in [csv, csum, cjson]:
            f.write(f"{sha256(p)}  {os.path.basename(p)}\n")

if __name__ == "__main__":
    build()
