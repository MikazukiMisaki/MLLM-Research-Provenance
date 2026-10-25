"""Independent stdlib source hash/identity joins and historical cost field semantics."""
import hashlib,json,datetime
from pathlib import Path
OWN=Path(__file__).resolve().parent
P0=Path("/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__CODEX__self-experience-feasibility__b1c48c/experience_inventory.json")
cases_path=OWN/"FIXED_ELEVEN_CASES.json"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(P0)=="1b0b7766d5901894d71f635433b9055223648d07bf5bda4e648c1129403cd8c0"
x=json.loads(P0.read_text());fixed=json.loads(cases_path.read_text())["cases"]
bindings={r["path"]:r for r in x["input_bindings"]}
def canonical(s):
    z=str(s).replace("\\","/").rstrip("/").split("/")
    for j in range(len(z)-1,0,-1):
        if z[j].startswith("trial_"):return z[j-1]+"/"+z[j]
    return str(s)
stages=("R4","R10_OSR","R16_OSR","R17_PAR","R18_C1","R18_C2","R19_BRANCHES")
source_rows={};proofs={}
for stage in stages:
    p=Path(x["stage_summaries"][stage]["source_path"]);binding=bindings[str(p)];before=sha(p)
    rawlines={i:b for i,b in enumerate(p.open("rb"),1) if b.strip()}
    bad=[];units=[]
    for u in x["cohort_indices"][stage]:
        b=rawlines[u["source_line"]];r=json.loads(b);task=canonical(r.get("task_id",r.get("canonical_trial_id")))
        ok=hashlib.sha256(b).hexdigest()==u["source_row_sha256"] and task==u["canonical_task"] and r["prefix_id"]==u["prefix_id"]
        if not ok:bad.append(u["prefix_id"])
        units.append({"prefix_id":u["prefix_id"],"canonical_task":task,"source_line":u["source_line"],"source_row_sha256":hashlib.sha256(b).hexdigest(),"ok":ok})
    after=sha(p)
    proofs[stage]={"source_path":str(p),"full_file_sha256":before,"P0_full_file_sha256_before":binding["sha256_before"],"P0_full_file_sha256_after":binding["sha256_after"],"actual_sha_after":after,"full_hash_matches":before==after==binding["sha256_before"]==binding["sha256_after"],"cohort_rows":len(units),"unique_tasks":len({u["canonical_task"] for u in units}),"all_prefix_to_task_mappings_verified":not bad,"mismatched_prefix_ids":bad,"units":units}
    source_rows[stage]={u["prefix_id"]:u for u in units}
case_proofs=[]
for c in fixed:
    stage="R19_BRANCHES" if c["stage"]=="R19_K1" else c["stage"];u=source_rows[stage][c["prefix_id"]]
    case_proofs.append({"case_id":c["case_id"],"canonical_task":c["canonical_task"],"source_path":proofs[stage]["source_path"],"source_file_sha256":proofs[stage]["full_file_sha256"],"row_sha256":u["source_row_sha256"],"case_matches":u["canonical_task"]==c["canonical_task"] and u["source_row_sha256"]==c["source_row_sha256"]})
training=Path("/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/training_result.json")
t=json.loads(training.read_text())
out={"schema":"SI_P1_INDEPENDENT_METADATA_JOIN_V1","observed_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"P0_inventory":{"path":str(P0),"sha256":sha(P0)},"fixed_cases":{"path":str(cases_path),"sha256":sha(cases_path)},"stage_proofs":proofs,"fixed_11_case_proofs":case_proofs,"all_named_mappings_and_source_hashes_match":all(p["full_hash_matches"] and p["all_prefix_to_task_mappings_verified"] for p in proofs.values()) and all(c["case_matches"] for c in case_proofs),"scope":"existing consumed records only; identity and byte hashes, no new outcome policy analysis","historical_training_cost_fields":{"source_path":str(training),"source_sha256":sha(training),"optimizer_steps":t["optimizer_steps"],"wall_time_seconds":t["wall_time_seconds"],"input_tokens_seen_recorded":t["input_tokens_seen"],"gpu_device_seconds":"NOT_PROVEN_BY_WALL_TIME","padding_semantics":"retain original metric name; not independently established from this JSON alone","not_in_R19_campaign_total":True},"new_scientific_calls":0,"limit":"Named mappings are closed; global absence of unregistered historical viewing/usage or scene-level similarity remains unproven."}
assert out["all_named_mappings_and_source_hashes_match"],out
(OWN/"independent_source_hash_and_identity_join.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"all_named_mappings_and_source_hashes_match":True,"stages":{k:{"rows":v["cohort_rows"],"tasks":v["unique_tasks"]} for k,v in proofs.items()},"fixed_cases":len(case_proofs),"training_fields":out["historical_training_cost_fields"]},indent=2))
