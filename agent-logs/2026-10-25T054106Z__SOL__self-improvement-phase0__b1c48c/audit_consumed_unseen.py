"""Recount existing consumed unseen evidence only; no project runtime imports."""
import collections,hashlib,json
from pathlib import Path
r=Path("/home/lizening/Alfworld-Self-Improvement-Project")
own=Path(__file__).resolve().parent
names={"schedule":r/"configs/evaluation/sft_heldout_valid_unseen_schedule.json","raw":r/"artifacts/runtime/validation/sft-valid-unseen-g1-20260829T031028Z/trajectories.jsonl","development":r/"artifacts/runtime/sft-policy-bootstrap/online_evaluation/sft_trajectories.jsonl"}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs={k:{"path":str(p),"bytes":p.stat().st_size,"sha256_before":sha(p)} for k,p in names.items()}
scheduled=json.loads(names["schedule"].read_text())["episodes"]
rows=[json.loads(z) for z in names["raw"].open() if z.strip()]
ix={x["task_id"]:x for x in scheduled}
errors=[];successes=0;ids=set();families=collections.Counter()
for x in rows:
    t=x["task"]["task_id"];m=x["metadata"];ids.add(t);families[m["task_family"]]+=1
    success=any(bool((s["metadata"]["environment"]["alfworld_info"].get("won") or [False])[0]) for s in x["steps"]);successes+=success
    expected=ix.get(t)
    if expected is None:errors.append({"task":t,"error":"not_scheduled"});continue
    actual={"split":x["task"]["split"],"nominal_seed":m["nominal_seed"],"reset_order_position":m["reset_order_position"],"schedule_index":m["schedule_index"],"source_game_sha256":m["source_game_sha256"],"task_family":m["task_family"],"horizon":m["max_steps"]}
    for k,v in actual.items():
        if expected[k]!=v: errors.append({"task":t,"key":k,"expected":expected[k],"actual":v})
dev={json.loads(z)["task"]["task_id"] for z in names["development"].open() if z.strip()}
for k,p in names.items():inputs[k]["sha256_after"]=sha(p);inputs[k]["unchanged"]=inputs[k]["sha256_before"]==inputs[k]["sha256_after"]
out={"kind":"independent pure-stdlib consumed-record recount; no new outcomes","inputs":inputs,"rows":len(rows),"unique_task_ids":len(ids),"scheduled":len(scheduled),"raw_successes":successes,"families":dict(families),"schedule_binding_errors":errors,"missing_scheduled":sorted(set(ix)-ids),"development_id_intersection":sorted(ids&dev),"interpretation":"49/60 SFT single arm, no same-batch base comparison. Historical records, not newly independent heldout evidence or new science permission.","new_scientific_calls":0}
(own/"independent_unseen_recount.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
