"""Recompute descriptive context from immutable historical rows; no model fitting."""
from pathlib import Path
import json
import hashlib
from collections import Counter

ROOT = Path(r"D:\MLWork\tariff_scope_20261007")
OUT = ROOT / "revision_20261023"

def rows(path):
    return [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines() if s.strip()]

def counts(values):
    return dict(sorted(Counter(values).items()))

def norm_numeric(state):
    # Historical evaluator explicitly treats an inactive/unparsed numeric guard
    # as unknown for the numeric-component comparison, never as supported.
    return "unknown" if state == "not_parsed" else state

def main():
    bp = ROOT / "datasets/benchmark.jsonl"
    ep = ROOT / "revision_20261009/evidence_numeric/evidence_operational_reference.jsonl"
    np = ROOT / "revision_20261009/evidence_numeric/numeric_layer_predictions.jsonl"
    cases = {r["case_id"]: r for r in rows(bp)}
    refs = {r["case_id"]: r for r in rows(ep)}
    primary = [cases[k] for k in refs]
    exact = [r for r in primary if r["exact_code_match"]]
    removed = [r for r in primary if not r["exact_code_match"]]
    numeric = rows(np)
    cross = Counter((cases[k]["y"], r["operational_evidence_state"]) for k, r in refs.items())
    groups = Counter(cases[r["case_id"]]["group"] for r in numeric)
    match = Counter()
    for r in numeric:
        for layer, pred in r["layers"].items():
            match[layer] += norm_numeric(pred["state"]) == r["numeric_reference_state"]
    largest = groups.most_common(1)[0][0]
    reduced = [r for r in numeric if cases[r["case_id"]]["group"] != largest]
    reduced_match = Counter()
    for r in reduced:
        for layer, pred in r["layers"].items():
            reduced_match[layer] += norm_numeric(pred["state"]) == r["numeric_reference_state"]
    cross_numeric = Counter((r["numeric_reference_state"], refs[r["case_id"]]["operational_evidence_state"]) for r in numeric)
    def composition(rs):
        return {"n": len(rs), "source": counts(r["source"] for r in rs),
                "source_by_y": counts(f'{r["source"]}:y={r["y"]}' for r in rs),
                "groups": len(set(r["group"] for r in rs))}
    summary = {
        "scope": "Historical references, unchanged; not a new source audit or expert ground truth.",
        "primary": composition(primary), "exact_code": composition(exact), "removed": composition(removed),
        "removed_code_granularity": [{"case_id":r["case_id"],"date":r["date"],
            "product_codes":r["product_hts"],"candidate_codes":r["rule_hts"],
            "source":r["source"],"administrative_y":r["y"]} for r in removed],
        "removed_code_boundary":"All 13 have eight-digit product codes against ten-digit candidate statistical codes. Exact-string filtering changes source and class composition; this is not an isolated test of historical code certainty. No new historical statistical-code adjudication is claimed.",
        "old_states": counts(r["operational_evidence_state"] for r in refs.values()),
        "old_y_by_z": {f'y={y}:{z}':n for (y,z),n in sorted(cross.items())},
        "old_condition_records": sum(len(r["conditions"]) for r in refs.values()),
        "numeric": {"n":len(numeric), "groups":len(groups), "group_sizes":dict(groups),
            "largest_group":largest,"largest_group_n":groups[largest],
            "largest_group_fraction":groups[largest]/len(numeric),
            "matches":dict(match), "state_normalization":"not_parsed -> unknown, as explicitly specified in the historical component evaluator", "without_largest_group_n":len(reduced),
            "without_largest_group_matches":dict(reduced_match),
            "numeric_by_whole_evidence": {f'{n}:{z}':c for (n,z),c in sorted(cross_numeric.items())}},
        "guard_cost_example": {"n":73,"false_grants":5,"false_denials":10,"referrals":26,
            "cg":5,"cd":1,"cr":0.5,"loss_guard":(5*5+10+26*.5)/73,
            "loss_review_all":.5,"break_even_cr":(5*5+10)/47,
            "interpretation":"Hypothetical administrative-disagreement costs; not measured legal error or savings."},
        "five_refuted_class": {"one_case_recall_change":1/5,"one_case_macro_recall_change":1/15},
        "sources": [{"path":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in (bp,ep,np)]
    }
    target = OUT / "verification/historical_context.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:summary[k] for k in ("primary","exact_code","removed","old_states","old_y_by_z","old_condition_records","numeric","guard_cost_example")},ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
