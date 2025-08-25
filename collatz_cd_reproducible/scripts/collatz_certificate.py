#!/usr/bin/env python3
import argparse, json, csv
def v2(x: int) -> int:
    c = 0
    while x % 2 == 0:
        x //= 2
        c += 1
    return c
def build_graph(R: int, S: int):
    M = 1 << (R+S)
    vertices = list(range(1, M, 2))
    index = {a:i for i,a in enumerate(vertices)}
    succ = [0]*len(vertices); tau=[0]*len(vertices); w=[0]*len(vertices)
    for i,a in enumerate(vertices):
        t = v2(3*a + 1); tau[i]=t; w[i]=min(t,R)
        b = ((3*a + 1) >> t) % M; succ[i]=index[b]
    return M, vertices, succ, tau, w
def enumerate_cycles(succ):
    n=len(succ); visited=[0]*n; cycles=[]
    for i in range(n):
        if visited[i]: continue
        seen={}
        j=i
        while not visited[j]:
            visited[j]=1; seen[j]=True; j=succ[j]
        if j in seen:
            cyc=[]; k=j
            while True:
                cyc.append(k); k=succ[k]
                if k==j: break
            cycles.append(cyc)
    return cycles
def compute_mu_B(vertices, succ, w, cycles):
    mu_list=[(len(c), sum(w[i] for i in c)/len(c)) for c in cycles]
    mu_star=min(mu for _,mu in mu_list)
    n=len(vertices); on=[False]*n; L=[0]*n
    for c in cycles:
        l=len(c)
        for i in c: on[i]=True; L[i]=l
    B=0.0
    for s in range(n):
        x=s; ssum=0.0; min_s=0.0; seen=False; taken=0; l=0
        for _ in range(n+100):
            ssum += (w[x]-mu_star)
            if ssum < min_s: min_s = ssum
            if on[x]:
                if not seen: seen=True; l=L[x]
                taken += 1
                if taken >= l: break
            x = succ[x]
        if -min_s > B: B = -min_s
    return mu_star, B, mu_list
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=13)
    ap.add_argument("--S", type=int, default=4)
    ap.add_argument("--summary", required=True)
    ap.add_argument("--cycles", required=True)
    ap.add_argument("--cert", required=True)
    a=ap.parse_args()
    M,V,succ,tau,w = build_graph(a.R,a.S)
    cycles=enumerate_cycles(succ)
    mu_star,B,mu_list = compute_mu_B(V,succ,w,cycles)
    with open(a.summary,"w") as f:
        json.dump({"R":a.R,"S":a.S,"modulus":M,"num_vertices":len(V),
                   "num_cycles":len(cycles),"mu_star":mu_star}, f, indent=2, sort_keys=True)
    import csv as _csv
    with open(a.cycles,"w",newline="") as f:
        wr=_csv.writer(f); wr.writerow(["cycle_length","mean_trunc_tau"])
        for L,mu in sorted(mu_list, key=lambda t:(t[1],t[0])): wr.writerow([L,mu])
    with open(a.cert,"w") as f:
        json.dump({"R":a.R,"S":a.S,"modulus":M,"mu_star":mu_star,
                   "global_precycle_slack_B":B}, f, indent=2, sort_keys=True)
    print(f"mu_star={mu_star:.6f}, B={B:.1f}, cycles={len(cycles)}")
if __name__=="__main__": main()
