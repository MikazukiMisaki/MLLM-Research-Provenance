from pathlib import Path
import json,hashlib,collections
OWN=Path(__file__).resolve().parent
assert "si-p3-controlled-experience-design" in str(OWN)
BASE=Path("/home/lizening/research-notes")
L=BASE/"agent-logs/2026-10-25T084517Z__LUNA__si-p3-isolation-budget-design__si3_7d91"
C=BASE/"agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/P0_SCOPE_INCIDENT_SNAPSHOT/SUPPORTED_IDENTITY_CANDIDATES.json"
P=json.loads((L/"partition_proposal_family_capacity_addendum.json").read_text())
parents=json.loads(C.read_text())["train"]
by={x["identity"]:x for x in parents}; remaining={i for i in by if not i.startswith("look_at_obj_in_light-")}
families=sorted(P["family_capacities"]);assert len(remaining)==1139
ordered={f:sorted([i for i in remaining if i.startswith(f+"-")],key=lambda i:(hashlib.sha256(("SI-P3-task-partition-v1\n"+f+"\n"+i+"\n").encode()).hexdigest(),i)) for f in families}
expected={};qall={}
for part,n in [("final_evaluation_train",600),("engineering_development_train",48),("acquisition_train",480)]:
 caps={f:len(ordered[f]) for f in families}; total=sum(caps.values());q={f:n*caps[f]//total for f in families};extra=n-sum(q.values())
 rank=sorted(families,key=lambda f:(-(n*caps[f]%total),f))
 for f in rank[:extra]:q[f]+=1
 qall[part]=q
 for f in families:
  for i in ordered[f][:q[f]]:expected[i]=part
  ordered[f]=ordered[f][q[f]:]
qall["unallocated_nonlight_reserve"]={f:len(ordered[f]) for f in families}
for f in families:
 for i in ordered[f]:expected[i]="unallocated_nonlight_reserve"
assert set(expected)==remaining
assert len(P["rows"])==len(remaining)
for row in P["rows"]:
 i=row["identity"];f=row["family"]
 assert row["identity_sha256"]==hashlib.sha256(i.encode()).hexdigest()==by[i]["identity_sha256"]
 assert row["partition_rank_sha256"]==hashlib.sha256(("SI-P3-task-partition-v1\n"+f+"\n"+i+"\n").encode()).hexdigest()
 assert row["partition"]==expected[i]
assert qall==P["family_quotas"]
counts=dict(collections.Counter(expected.values()));assert counts==P["partition_counts"]
assert {x["identity"] for x in P["excluded_light_candidates"]}==set(by)-remaining
root_budget=json.loads((OWN/"independent_budget_math.json").read_text());lb=json.loads((L/"budget_design.json").read_text())["aggregate_physical_caps"]
checks={}
for n in [96,384,480]:
 key={96:"acquisition_N96_initial_feasibility",384:"incremental_acquisition_384_after_96_if_separately_released",480:"acquisition_N480_total_reference_including_initial_96"}[n]
 b=lb[key];assert b["model_generations_max"]==101*n;assert b["reset_inclusive_environment_operations_max"]==102*n;assert b["output_tokens_max"]==1640*n;assert b["environment_resets_max"]==2*n
 checks[str(n)]=True
assert lb["evaluation_E600_three_arms_A_B_C_horizon50"]["model_generations_max"]==90000
assert lb["evaluation_E600_three_arms_A_B_C_horizon50"]["reset_inclusive_environment_operations_max"]==91800
out={"status":"INDEPENDENT_METADATA_AND_CAP_ARITHMETIC_MATCH","candidate_count":1141,"nonlight_count":1139,"exact_rows_reproduced":len(expected),"partition_counts":counts,"family_quotas":qall,"all_partition_task_intersections":0,"light_unused":2,"budget_checks":checks,"limits":["no payload/outcome read","not scientific validator/preflight/experiment","original 480/60/600 draft retained; only five-family addendum accepted","numeric folder suffix overlap remains; not held-out layout"]}
(OWN/"independent_luna_proposal_verification.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
