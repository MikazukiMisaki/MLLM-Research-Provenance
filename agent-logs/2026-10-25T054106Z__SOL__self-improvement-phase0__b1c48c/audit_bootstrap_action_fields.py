import collections,hashlib,json
from pathlib import Path
root=Path("/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/sft-policy-bootstrap/online_evaluation")
out={"kind":"stdlib-only historical explicit action field recount, not semantic re-labeling","arms":{},"new_scientific_calls":0}
for arm in ("base","sft"):
    path=root/(arm+"_trajectories.jsonl");before=hashlib.sha256(path.read_bytes()).hexdigest()
    rows=[json.loads(s) for s in path.open() if s.strip()];steps=[s for r in rows for s in r["steps"]]
    out["arms"][arm]={"path":str(path),"sha256_before":before,"sha256_after":hashlib.sha256(path.read_bytes()).hexdigest(),"episodes":len(rows),"recorded_decisions":len(steps),"recorded_action_valid_true":sum(s["action_valid"] is True for s in steps),"recorded_action_valid_false":sum(s["action_valid"] is False for s in steps),"recorded_parser_status":dict(collections.Counter(s["parser_status"] for s in steps))}
out["interpretation"]="Only one invalid base decision is recorded; observed 45 paired task gains cannot all be attributed to fixing malformed output. This does not causally isolate planning, imitation, navigation, or other learned skills and does not prove self-improvement."
(Path(__file__).resolve().parent/"independent_action_contract_recount.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
