"""Independent literal SI-S01 E/F/S acceptance oracle: stdlib only, no project imports."""
from pathlib import Path
import datetime
import hashlib
import json

OWN=Path(__file__).resolve().parent
assert OWN.name.endswith("__CRITIC__si-s01-independent-efs-vectors__b3acdd")
PROTOCOL=Path("/home/lizening/research-notes/agent-logs/2026-10-26T100859Z__SOL__si-p3-persistent-launch-coordination__f1a52e8c/ADOPTED_SOURCE_ONLY_PROTOCOL.md")
PROTOCOL_SHA="daa1d787f9ef13f5927dcf696a2be4c6328dc159b3eb39b5f0f5f520582ebb72"
protocol_before=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
assert protocol_before==PROTOCOL_SHA
# These literals were copied from the adopted protocol, never imported from production.
FAMILIES=(
    "pick_and_place_simple",
    "pick_clean_then_place_in_recep",
    "pick_cool_then_place_in_recep",
    "pick_heat_then_place_in_recep",
    "pick_two_obj_and_place",
)
N=(35,26,16,9,10)
E_FLOOR=(22,17,10,6,7)
FS_FLOOR=(9,6,4,2,3)
NOT_FUTILE="SOURCE_UPPER_BOUNDS_NOT_FUTILE"
NO_GO="COMPLETE_SOURCE96_STRUCTURAL_NO_GO"
# E, F, S and every expected status/count below are independent hand-specified literals.
CASES=[
    dict(id="01_exact_E72_F24",E=[25,19,12,8,8],F=[9,6,4,2,3],S=[16,13,8,6,5],
         total_E=72,total_F=24,total_S=48,normal_successes=72,status=NOT_FUTILE,
         violations=[],generations=456,steps=432,environment_operations=528),
    dict(id="02_E_total71_only",E=[24,19,12,8,8],F=[9,6,4,2,3],S=[15,13,8,6,5],
         total_E=71,total_F=24,total_S=47,normal_successes=72,status=NO_GO,
         violations=["E_total_below_72"],generations=451,steps=427,environment_operations=523),
    dict(id="03_F_total23_with_necessary_family_deficit",E=[25,19,12,8,8],F=[8,6,4,2,3],S=[17,13,8,6,5],
         total_E=72,total_F=23,total_S=49,normal_successes=73,status=NO_GO,
         violations=["F_total_below_24","F_family:pick_and_place_simple"],generations=456,steps=433,environment_operations=529),
    dict(id="04_S_total23_with_necessary_family_deficit",E=[25,19,12,8,8],F=[17,13,8,6,5],S=[8,6,4,2,3],
         total_E=72,total_F=49,total_S=23,normal_successes=47,status=NO_GO,
         violations=["S_total_below_24","S_family:pick_and_place_simple"],generations=456,steps=407,environment_operations=503),
    dict(id="05_only_E_family_deficit",E=[21,22,12,8,9],F=[9,6,4,2,3],S=[12,16,8,6,6],
         total_E=72,total_F=24,total_S=48,normal_successes=72,status=NO_GO,
         violations=["E_family:pick_and_place_simple"],generations=456,steps=432,environment_operations=528),
    dict(id="06_only_F_family_deficit_total24",E=[25,19,12,8,8],F=[8,7,4,2,3],S=[17,12,8,6,5],
         total_E=72,total_F=24,total_S=48,normal_successes=72,status=NO_GO,
         violations=["F_family:pick_and_place_simple"],generations=456,steps=432,environment_operations=528),
    dict(id="07_only_S_family_deficit_total24",E=[25,19,12,8,8],F=[17,12,8,6,5],S=[8,7,4,2,3],
         total_E=72,total_F=48,total_S=24,normal_successes=48,status=NO_GO,
         violations=["S_family:pick_and_place_simple"],generations=456,steps=408,environment_operations=504),
]
MODE_SPEC={
    "N":{
        "name":"noneligible_normal_success_action1",
        "source_normal":True,"Y0":1,"E":False,
        "generation_attempts":1,"executed_actions":1,
        "terminal_after_action":1,"terminal_reward":1,
        "anchor":"NO_ELIGIBLE_STATE; normal terminal before action5",
        "state_after_action1":{"done":True,"truncated":False,"valid_actions":[]},
    },
    "S":{
        "name":"eligible_normal_success_action6",
        "source_normal":True,"Y0":1,"E":True,
        "generation_attempts":6,"executed_actions":6,
        "terminal_after_action":6,"terminal_reward":1,
        "state_after_action5":{"done":False,"truncated":False,"reward":0,"valid_actions_nonempty":True},
        "anchor":"Seal the real after-action5 state before generation6; action5 itself must not terminate",
        "state_after_action6":{"done":True,"truncated":False,"valid_actions":[]},
    },
    "F":{
        "name":"eligible_normal_actor_parse_failure_attempt6",
        "source_normal":True,"Y0":0,"E":True,
        "generation_attempts":6,"executed_actions":5,
        "terminal_after_action":None,"terminal_reward":0,
        "state_after_action5":{"done":False,"truncated":False,"reward":0,"valid_actions_nonempty":True},
        "anchor":"Seal after-action5 before attempt6; retain this valid S5 after parse failure",
        "attempt6":"A complete Generation envelope decoded to text rejected by the real frozen P0 parser; execute no sixth action",
        "source_termination":"invalid_actor (normal fail-closed, not a callback exception)",
    },
}
output_cases=[]
for c in CASES:
    assert len(c["E"])==len(c["F"])==len(c["S"])==5
    slots={}
    for i,f in enumerate(FAMILIES):
        e,fail,success=c["E"][i],c["F"][i],c["S"][i]
        assert type(e) is int and type(fail) is int and type(success) is int
        assert 0<=e<=N[i] and fail>=0 and success>=0 and fail+success==e
        # Character j explicitly supplies the synthetic mode for family-local index j.
        slots[f]="F"*fail+"S"*success+"N"*(N[i]-e)
        assert len(slots[f])==N[i]
    observed_F=[slots[f].count("F") for f in FAMILIES]
    observed_S=[slots[f].count("S") for f in FAMILIES]
    observed_E=[observed_F[i]+observed_S[i] for i in range(5)]
    assert observed_E==c["E"] and observed_F==c["F"] and observed_S==c["S"]
    assert (sum(observed_E),sum(observed_F),sum(observed_S))==(c["total_E"],c["total_F"],c["total_S"])
    violations=[]
    for name,total,floor in (("E",sum(observed_E),72),("F",sum(observed_F),24),("S",sum(observed_S),24)):
        if total<floor:violations.append(name+"_total_below_"+str(floor))
    for i,f in enumerate(FAMILIES):
        for name,observed,floors in (("E",observed_E,E_FLOOR),("F",observed_F,FS_FLOOR),("S",observed_S,FS_FLOOR)):
            if observed[i]<floors[i]:violations.append(name+"_family:"+f)
    assert violations==c["violations"]
    assert (NO_GO if violations else NOT_FUTILE)==c["status"]
    modes="".join(slots.values())
    assert len(modes)==96
    gen=sum(MODE_SPEC[m]["generation_attempts"] for m in modes)
    steps=sum(MODE_SPEC[m]["executed_actions"] for m in modes)
    successes=sum(MODE_SPEC[m]["Y0"] for m in modes)
    assert (gen,steps,steps+96,successes)==(c["generations"],c["steps"],c["environment_operations"],c["normal_successes"])
    output_cases.append({
        "id":c["id"],"slot_modes_by_family_local_index":slots,
        "expected":{
            "status":c["status"],"normal_sources":96,"source_phase_sealed":True,
            "YT_for_every_slot":None,"teacher_status":"TEACHER_NOT_AUTHORIZED_SOURCE_ONLY",
            "source_Y0":{"successes":c["normal_successes"],"failures":c["total_F"]},
            "upper_bounds":{"E":c["total_E"],"F":c["total_F"],"S":c["total_S"],
                "by_family":{f:{"E":c["E"][i],"F":c["F"][i],"S":c["S"][i]} for i,f in enumerate(FAMILIES)}},
            "violations_for_explanation_only":c["violations"],
            "synthetic_boundary_calls":{"model_load":1,"env_construct":96,"reset":96,
                "generation":c["generations"],"step":c["steps"],"env_close":96,
                "environment_operations":c["environment_operations"],
                "teacher_generation":0,"branch_reset":0,"replay_step":0},
        },
    })
protocol_after=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest()
assert protocol_after==protocol_before
doc={
    "schema":"SI_S01_INDEPENDENT_LITERAL_EFS_VECTORS_V1",
    "status":"DESIGN_VECTORS_ONLY_NOT_SOFTWARE_PASS_NOT_RUNTIME_AUTHORIZATION",
    "generated_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "authority":{"protocol_path":str(PROTOCOL),"sha256_before":protocol_before,"sha256_after":protocol_after},
    "independence":{"project_imports":False,"production_threshold_constants_used":False,
        "project_runtime_model_env_tokenizer_cuda_tests_network_calls":0,
        "new_real_task_bodies_or_results_read":False,"future_real_schedule":False},
    "literal_protocol":{"family_order":list(FAMILIES),"N":list(N),"E_family_floor":list(E_FLOOR),
        "F_family_floor":list(FS_FLOOR),"S_family_floor":list(FS_FLOOR),
        "total_E_floor":72,"total_F_floor":24,"total_S_floor":24},
    "slot_index_convention":"For each family, character j in slot_modes_by_family_local_index is family-local index j (zero based) in the synthetic Plan order. No real identity or seed is supplied.",
    "mode_specification":MODE_SPEC,
    "essential_qualifications":[
        "S5 must be alive after action5. Mode S terminates at action6, never at action5.",
        "Each completed case has exactly96 normal sources; normal parse failure is Y0=0, not technical NA.",
        "Every teacher outcome remains NA; NOT_FUTILE is only a necessary source upper-bound result.",
        "Family F/S floors each sum to24, so Ftotal23 or Stotal23 cannot avoid at least one family deficit.",
        "Expected violation names are explanatory independent-oracle fields; production need not expose these names.",
        "Use production parser/collector/journal/auditor, replacing only the external synthetic model/environment boundaries. Never mock the auditor or force parser results.",
        "Token counts, prompt bodies, rendered inputs, task identities and hardware timing are not fabricated by these vectors.",
    ],
    "cases":output_cases,
}
out=OWN/"EFS_ACCEPTANCE_VECTORS.json"
assert not out.exists()
out.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
method="""# Independent SI-S01 source upper-bound acceptance vectors

This package is synthetic design material, not a software PASS or a scientific execution release. Only the adopted protocol was read. No project module, runtime, tokenizer, model, environment, CUDA, network or test runner was invoked.

The builder uses literal N=[35,26,16,9,10], E floors=[22,17,10,6,7], F/S floors=[9,6,4,2,3] and totals72/24/24. Each case has hand-specified E/F/S arrays and expected status. Its stdlib checks only establish internal arithmetic and constructibility, not production correctness.

For each family, character j in slot_modes_by_family_local_index gives the mode of zero-based family-local slot j in a later synthetic Plan. There are exactly96 slots per case. The adapter may supply fake canonical identities, but must not select real A96 identities or read new task bodies.

Modes:
- N: normal success at action1; no S5.
- S: first five actions are nonterminal, with a nonempty action map at S5; seal S5 before generation6; action6 succeeds and terminates. Terminating at action5 would be ineligible and is intentionally forbidden.
- F: first five actions produce a valid S5; seal it before generation6; the sixth generation is rejected by the real frozen P0 parser and executes no action. This is a normal source failure, not a technical exception. Keep the valid S5.

All YT are NA. An S outcome is source success, not teacher success. All cases complete96 normal source dispositions and may therefore be sealed before necessary-condition classification. Projected call counts refer only to later software fixtures, not calls performed in this task.

Seven cases test exact E72/F24 acceptance, E71, F23, S23, and separately sufficient totals with one E/F/S family deficit. F/S family minima each sum to24: the F23 and S23 cases necessarily also have a family deficit. Those two total checks cannot be isolated while preserving all family minima.

A later independent reviewer can load the JSON, construct the synthetic boundary behavior, run the real production collector/auditor, and compare the returned status, per-family E/F/S, normal_sources=96, source_phase_sealed=true, allYT=NA and physical call counts. No production import is required to read this oracle. Production need not return the explanatory violation labels.

The expected NOT_FUTILE result says only that source necessary upper bounds are not violated. It does not establish Q, C24, a constructible training recipe or learning efficacy. Real rendering/token counts and hardware timing require their own evidence and are deliberately unspecified here.
"""
(OWN/"METHOD.md").write_text(method,encoding="utf-8")
print(json.dumps({"status":"LITERAL_VECTOR_ARITHMETIC_AND_MODE_COUNTS_CONSISTENT",
    "case_count":7,"synthetic_slots_per_case":96,"project_or_runtime_calls":0,
    "output":str(out),"output_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),
    "protocol_unchanged":protocol_before==protocol_after},ensure_ascii=False))

