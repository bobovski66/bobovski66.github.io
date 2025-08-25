#!/usr/bin/env python3
import argparse, json, csv
def v2(x: int) -> int:
    c=0
    while x%2==0:
        x//=2; c+=1
    return c
def accelerated_next(n:int)->int:
    t=v2(3*n+1)
    return (3*n+1)>>t
def verify_upto(N:int):
    cache={1:0}; max_steps=0; argmax=1; max_val=1; checked=0
    for n in range(1,N,2):
        if n in cache:
            checked+=1; continue
        seq=[]; x=n; steps=0
        while x not in cache:
            seq.append(x); x=accelerated_next(x); steps+=1
            if x>max_val: max_val=x
            if steps>10_000_000: raise RuntimeError("cap")
        total=cache[x]
        for y in reversed(seq):
            total+=1; cache[y]=total
        if total>max_steps: max_steps=total; argmax=n
        checked+=1
    return {"N":N,"tested_count_odd":checked,"all_reached_1":True,
            "max_steps":max_steps,"argmax_steps":argmax,"max_value_seen":max_val,
            "cache_size":len(cache)}, cache
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--N",type=int,default=1_000_000)
    ap.add_argument("--summary",required=True)
    ap.add_argument("--top",required=True)
    a=ap.parse_args()
    summary, cache = verify_upto(a.N)
    with open(a.summary,"w") as f: json.dump(summary,f,indent=2,sort_keys=True)
    top=sorted([(n,s) for n,s in cache.items() if n<a.N and n%2==1],
               key=lambda t:t[1], reverse=True)[:50]
    with open(a.top,"w",newline="") as f:
        wr=csv.writer(f); wr.writerow(["n_odd","accelerated_steps_to_1"]); wr.writerows(top)
    print("Done.", summary)
if __name__=="__main__": main()
