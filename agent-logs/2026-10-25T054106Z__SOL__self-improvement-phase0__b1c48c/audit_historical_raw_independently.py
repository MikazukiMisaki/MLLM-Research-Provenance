"""Independent stdlib-only recount of existing evidence. No project imports or new evaluation."""
import collections, datetime, hashlib, json
from pathlib import Path

OWN = Path(__file__).resolve().parent
ROOT = Path("/home/lizening/Alfworld-Self-Improvement-Project")
def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1048576), b""): h.update(b)
    return h.hexdigest()
def canonical(v):
    return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()
def read(path): return json.loads(path.read_text())
files = {}
def pin(path):
    files[str(path)] = {"bytes":path.stat().st_size,"sha256_before":sha(path)}
    return path
protocol=read(pin(ROOT/"configs/sft/sft_training_protocol.json"))
bindings={}
for key,name in (("split_manifest_sha256","sft_task_splits.json"),("exclusion_manifest_sha256","sft_task_exclusions.json"),("schema_sha256","sft_dataset_schema.json")):
    path=pin(ROOT/"configs/sft"/name); v=read(path)
    bindings[key]={"path":str(path),"declared":protocol["dataset"][key],"raw_sha256":sha(path),"canonical_sha256":canonical(v),"canonical_matches":canonical(v)==protocol["dataset"][key],"definition":"src/sft/protocol.py canonical_json ensure_ascii=True, sorted compact JSON; build_sft_protocol_assets.py uses sha256_value"}
evalroot=ROOT/"artifacts/runtime/sft-policy-bootstrap/online_evaluation"
arms={}
for arm in ("base","sft"):
    path=pin(evalroot/(arm+"_trajectories.jsonl"))
    rows=[json.loads(line) for line in path.open() if line.strip()]
    ix={}
    success={}
    details={}
    for r in rows:
        task=r["task"]["task_id"]; m=r["metadata"]; steps=r["steps"]
        won=lambda s: bool((s.get("metadata",{}).get("environment",{}).get("alfworld_info",{}).get("won") or [False])[0])
        anywin=any(won(s) for s in steps)
        lastwin=bool(steps and won(steps[-1]))
        ix[task]={"seed":r["seed"],"nominal_seed":m["nominal_seed"],"split":r["task"]["split"],"family":m["task_family"],"schedule_index":m["schedule_index"],"reset_order_position":m["reset_order_position"],"horizon":m["max_steps"],"initial_observation_sha256":hashlib.sha256(r["initial_observation"].encode()).hexdigest(),"reset_canonical_sha256":canonical(m["reset"]),"pipeline_version":m["pipeline_version"]}
        success[task]=anywin
        details[task]={"success_any_won":anywin,"success_last_won":lastwin,"steps":len(steps),"termination":m["termination_reason"],"truncated":r["truncated"]}
    arms[arm]={"path":str(path),"rows":len(rows),"unique_tasks":len(ix),"successes":sum(success.values()),"any_vs_last_success_disagreements":sum(x["success_any_won"]!=x["success_last_won"] for x in details.values()),"families":dict(collections.Counter(x["family"] for x in ix.values())),"index":ix,"success":success,"details":details}
base,sft=arms["base"],arms["sft"]; common=set(base["index"])&set(sft["index"])
mismatches={t:{k:[base["index"][t][k],sft["index"][t][k]] for k in base["index"][t] if base["index"][t][k]!=sft["index"][t][k]} for t in common}
mismatches={t:v for t,v in mismatches.items() if v}
pairs=collections.Counter(("win" if sft["success"][t] and not base["success"][t] else "loss" if base["success"][t] and not sft["success"][t] else "tie") for t in common)
dataset=pin(ROOT/"artifacts/runtime/sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl")
groups=collections.defaultdict(list)
for line in dataset.open():
    r=json.loads(line)
    groups[r["prompt_sha256"]].append({"task_id":r["task_id"],"step_index":r["step_index"],"family":r["task_family"],"split":r["dataset_split"],"target_action_id":r["target_action_id"],"target_command":r["target_command"],"trajectory_sha256":r["trajectory_sha256"]})
repeated={h:rs for h,rs in groups.items() if len(rs)>1}
conflicting={h:rs for h,rs in repeated.items() if len({(x["target_action_id"],x["target_command"]) for x in rs})>1}
duplicates={"retained_prompt_repeat_occurrences":sum(len(rs)-1 for rs in repeated.values()),"repeated_groups":len(repeated),"conflicting_target_groups":len(conflicting),"conflicting_rows":sum(map(len,conflicting.values())),"within_one_task_groups":sum(len({r["task_id"] for r in rs})==1 for rs in conflicting.values()),"cross_task_groups":sum(len({r["task_id"] for r in rs})>1 for rs in conflicting.values()),"within_one_trajectory_groups":sum(len({r["trajectory_sha256"] for r in rs})==1 for rs in conflicting.values()),"conflicting_rows_by_family":dict(collections.Counter(r["family"] for rs in conflicting.values() for r in rs)),"examples":[{"prompt_sha256":h,"rows":rs} for h,rs in sorted(conflicting.items())[:4]],"historical_counter_explanation":{"before_exact_dedup_reported":148,"exact_duplicates_removed_reported":21,"retained_repeat_occurrences":127,"arithmetic_reconciles":148-21==127,"code_reference":"src/sft/dataset.py:270 deduplicate_exact_rows increments prompt_counts before skipping exact duplicate rows","interpretation":"different stages of counting; no demonstrated report inconsistency"},"interpretation":"Identical observable prompts with different recorded expert targets; legality/hash consistency audited separately. Could reflect valid alternative actions or bounded observation aliasing; not proof of wrong labels, global insufficiency, or pick-two failure cause."}
for path,rec in files.items():
    rec["sha256_after"]=sha(Path(path));rec["unchanged"]=rec["sha256_after"]==rec["sha256_before"]
out={"audit_kind":"independent stdlib-only historical-record recount; not model/env/policy execution","observed_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"inputs":files,"canonical_bindings":bindings,"bootstrap":{"arms":{a:{k:v for k,v in r.items() if k not in ("index","success","details")} for a,r in arms.items()},"paired_identities":len(common),"pair_counts":dict(pairs),"pair_metadata_mismatches":mismatches,"limit":"Record-level agreement; absent contemporaneous launch/runtime receipts is not remedied by these matching fields."},"dataset_prompt_target_audit":duplicates,"new_science_calls":0}
(OWN/"independent_raw_recount.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(out,ensure_ascii=False,indent=2))
