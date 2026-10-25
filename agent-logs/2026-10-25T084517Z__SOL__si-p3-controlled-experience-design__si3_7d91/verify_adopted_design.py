from pathlib import Path
import json,hashlib,collections,math
OWN=Path(__file__).resolve().parent
assert "si-p3-controlled-experience-design" in str(OWN)
a=json.loads((OWN/"ADOPTED_METADATA_RESERVATIONS.json").read_text());q=json.loads((OWN/"prospective_tranche_family_math.json").read_text())["first96_family_quota"]
l=OWN.parent/"2026-10-25T084517Z__LUNA__si-p3-isolation-budget-design__si3_7d91/partition_proposal_family_capacity_addendum.json"
p=json.loads(l.read_text());assert hashlib.sha256(l.read_bytes()).hexdigest()==a["derived_from_luna_proposal_sha256"]
parent={x["identity"]:x for x in p["rows"]};selected=set()
for f,n in q.items():
 pool=sorted([x for x in p["rows"] if x["family"]==f and x["partition"]=="acquisition_train"],key=lambda x:(x["partition_rank_sha256"],x["identity"]))
 selected|={x["identity"] for x in pool[:n]}
assert len(selected)==96
seen=set()
for x in a["rows"]:
 i=x["identity"];assert i not in seen;seen.add(i);y=parent[i]
 assert x["identity_sha256"]==y["identity_sha256"]==hashlib.sha256(i.encode()).hexdigest()
 assert x["family"]==y["family"] and x["partition_rank_sha256"]==y["partition_rank_sha256"]
 expected=y["partition"]
 if expected=="acquisition_train":expected="acquisition_feasibility_96" if i in selected else "unallocated_nonlight_reserve"
 assert x["partition"]==expected
assert seen==set(parent)
counts=dict(collections.Counter(x["partition"] for x in a["rows"]));assert counts==a["partition_counts"]
assert counts=={"final_evaluation_train":600,"engineering_development_train":48,"acquisition_feasibility_96":96,"unallocated_nonlight_reserve":395}
for key in ["final_evaluation_train","engineering_development_train"]:
 assert {x["identity"] for x in a["rows"] if x["partition"]==key}=={x["identity"] for x in p["rows"] if x["partition"]==key}
b=json.loads((OWN/"fixed_cutoff_budget_math.json").read_text())["acquisition"][0]
assert b["all_generations_max"]==8496 and b["environment_operations_with_resets_max"]==9792 and b["generated_tokens_max"]==138240
assert 4*24==96 and sum([5,10,15,20])*24==1200
assert 50*96+2*96+49*96-1200==8496
assert (24+120)*2//16==18 and (24+120)*2%16==0
assert 24*2==48
new_quotas={"pick_and_place_simple":9,"pick_clean_then_place_in_recep":6,"pick_cool_then_place_in_recep":4,"pick_heat_then_place_in_recep":2,"pick_two_obj_and_place":3}
assert sum(new_quotas.values())==24
for f,quota in new_quotas.items():assert 2*quota<=q[f]
# Count/slot feasibility is necessary only, not actual token/exposure or effect evidence.
out={"status":"DESIGN_ARITHMETIC_AND_IDENTITY_CONSTRAINTS_MATCH","adopted_counts":counts,"first96_family_counts":q,"new_training_quota24":new_quotas,"source_pair_min_quality_total":72,"family_Q_min":{f:math.ceil(.625*n) for f,n in q.items()},"selected_B_neutral_min_of24":8,"recipe_updates_per_arm":18,"each_new_task_max_exposure":2,"budget_math":b,"actual_new_model_environment_tokenizer_training_calls":0,"actual_loss_mask_token_matching":"NOT_RUN_BLOCKING","full_experiment_release":"NOT_AUTHORIZED"}
(OWN/"independent_adopted_design_verification.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
