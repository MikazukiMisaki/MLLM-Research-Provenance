"""Read-only independent R19 branch identity and rescue recount; no project imports."""
import collections,hashlib,json
from pathlib import Path
own=Path(__file__).resolve().parent
p=Path("/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/branches.jsonl")
before=hashlib.sha256(p.read_bytes()).hexdigest()
rows=[json.loads(s) for s in p.open() if s.strip()]
selected=[r for r in rows if r["eligible_primary"]]
counts={}
rescues={}
for k in range(1,6):
    key=str(k); cells=collections.Counter(); rr=[]
    for r in selected:
        v=r["k_results"][key]
        success=int(v["success"])
        outcome="rescue" if success and not r["continue_success"] else "harm" if r["continue_success"] and not success else "both_success" if success else "both_fail"
        cells[outcome]+=1
        if outcome=="rescue": rr.append({"prefix_id":r["prefix_id"],"canonical_trial_id":r["canonical_trial_id"],"source_schedule_index":r["source_schedule_index"],"decision_index":r["decision_index"],"stratum":r["stratum"],"task_family":r["task_family"]})
    counts[key]=dict(cells);rescues[key]=rr
out={"source_path":str(p),"bytes":p.stat().st_size,"sha256_before":before,"sha256_after":hashlib.sha256(p.read_bytes()).hexdigest(),"all_branch_rows":len(rows),"eligible_rows":len(selected),"eligible_unique_trials":len({r["canonical_trial_id"] for r in selected}),"eligible_unique_trajectory_hashes":len({r["trajectory_sha256"] for r in selected}),"strata":dict(collections.Counter(r["stratum"] for r in selected)),"fixed_k_vs_continue":counts,"rescue_candidates_by_k":rescues,"eligible_prefixes_rescued_by_any_k":len({r["prefix_id"] for rs in rescues.values() for r in rs}),"unique_trials_rescued_by_any_k":len({r["canonical_trial_id"] for rs in rescues.values() for r in rs}),"limits":["Historical paired outcome inventory only; K arms are dependent and cannot be counted as independent learning examples","Recovery targets may come from adapter-off base controller; later SFT suffix actor is a different policy. Preserve segment identities.","Does not prove training utility or independent new-task transfer"],"new_scientific_calls":0}
(own/"independent_r19_experience_recount.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(out,ensure_ascii=False,indent=2))
