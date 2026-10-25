from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
FILES={}
FILES['tests/test_si_p3_collector.py']=r'''"""Production contract tests; only raw generation/environment I/O is synthetic."""
import copy
import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from self_improvement.si_p3.audit import audit_run
from self_improvement.si_p3.collector import Collector, Ports, ProducerAdapter
from self_improvement.si_p3.contract import (CAPS, CONTRACT_FILE_SHA256, FAMILIES, SOURCE_QUOTAS,
                                            ContractError, PublicState, cut_matrix, digest, freeze_plan, plan_hash, projection)
from self_improvement.si_p3.evidence import Budget, Caps, Journal, UnitRegistry, validate_journal
from si_p3_support import (RawBoundary, SyntheticTokenizer, collect_synthetic, rehash, synthetic_plan)


@pytest.fixture(scope="module")
def complete(tmp_path_factory):
    return collect_synthetic(tmp_path_factory.mktemp("si-p3-software-complete"))


def test_versioned_contract_and_frozen_boundaries():
    root = Path(__file__).resolve().parents[1]
    p = root / "configs/self_improvement/si_p3_engineering_v1.json"
    assert hashlib.sha256(p.read_bytes()).hexdigest() == CONTRACT_FILE_SHA256
    value = json.loads(p.read_text())
    assert value["execution"] is False
    assert value["population"]["source_quotas"] == SOURCE_QUOTAS
    assert value["guards"]["selected_B_neutral_min"] == 8
    assert value["model"]["caps"] == CAPS
    assert value["population"]["automatic_384"] is False
    assert value["budgets"]["generations"] == 8496


def test_all96_plan_is_outcome_blind_balanced_and_fixed():
    plan = synthetic_plan()
    matrix = cut_matrix()
    assert len(plan) == 96 and sum(s.cutoff for s in plan) == 1200
    assert sum(101 - s.cutoff for s in plan) == 8496
    assert sum(1640 - 16 * s.cutoff for s in plan) == 138240
    for d in (5, 10, 15, 20):
        assert sum(s.cutoff == d for s in plan) == 24
    for family in FAMILIES:
        counts = [sum(s.cutoff == d and s.family == family for s in plan) for d in (5, 10, 15, 20)]
        assert max(counts) - min(counts) <= 1
        assert counts == list(matrix[family].values())
    assert plan_hash(plan) == digest([asdict(s) for s in plan])
    changed = list(plan);changed[0] = replace(changed[0], cutoff=10 if changed[0].cutoff == 5 else 5)
    with pytest.raises(ContractError, match="changed"):
        plan_hash(changed)


@pytest.mark.parametrize("change", ["future", "duplicate", "light", "missing"])
def test_no_plan_outcome_fields_replacement_or_quota_transfer(change):
    ids = [{"task_id":s.task_id,"family":s.family,"seed":s.seed} for s in synthetic_plan()]
    if change == "future": ids[0]["Y0"] = 0
    if change == "duplicate": ids[0] = ids[1]
    if change == "light": ids[0]["family"] = "look_at_obj_in_light"
    if change == "missing": ids.pop()
    with pytest.raises(ContractError): freeze_plan(ids)


def test_production_nonempty_source_replay_teacher_suffix_integrity(complete):
    run, events, tok, raw, envs = complete
    result = audit_run(run, events, tok)
    assert result["slots"] == len(run["slots"]) == 96
    assert all(row["disposition"] == "PAIRED" for row in run["slots"])
    assert len(envs) == 192 and all(e.resets == 1 and e.closes == 1 for e in envs)
    assert len(raw.calls) == result["physical"]["generations"]
    assert result["components"]["stage_one:generation"] == 96
    assert result["components"]["stage_two:generation"] == 96
    assert result["components"]["replay:step"] == 1200
    assert result["physical"]["environment_operations"] == sum(len(e.actions) + e.resets for e in envs)
    assert not any("baseline" in k for k in result["components"])
    cap_eos = [e for e in events if e["kind"] == "unit_completed" and e["payload"]["identity"]["phase"] == "stage_one"]
    assert all(e["payload"]["data"]["raw"]["token_cap_reached"] is True for e in cap_eos)
    assert all(e["payload"]["data"]["parsed"]["status"] == "valid" for e in cap_eos)


def test_reference_only_continue_and_inplace_P0_restore(complete):
    run, events, _, raw, envs = complete
    index = {e["event_id"]:e for e in events}
    for row in run["slots"]:
        d = row["slot"]["cutoff"]
        branch = row["branch"]
        assert branch["source_suffix_step_refs"] == row["source"]["rollout"]["steps"][d:]
        assert branch["source_suffix_generation_refs"] == row["source"]["rollout"]["generations"][d:]
        teacher = index[branch["teacher_step"]]["payload"]["data"]
        suffix = index[branch["suffix"]["steps"][0]]["payload"]["data"]
        assert teacher["session"] == suffix["session"]
        assert teacher["after"] == suffix["before"]
        assert index[branch["suffix"]["generations"][0]]["payload"]["data"]["raw"]["adapter_mode"] == "P0"
        assert index[branch["stage_two"]]["payload"]["data"]["raw"]["adapter_mode"] == "BASE"
        assert "Frozen Stage-1" not in row["projection"]["public_prompt"]


@pytest.mark.parametrize("field", ["event_id", "previous", "identity", "action_id", "before", "adapter", "cost", "label", "projection", "suffix_ref"])
def test_tampered_receipt_mapping_label_or_future_input_is_rejected(complete, field):
    run, events, tok, *_ = copy.deepcopy(complete)
    row = run["slots"][0]
    if field in ("cost", "label", "projection", "suffix_ref"):
        if field == "cost": run["cost"]["completed"]["generations"] += 1
        elif field == "label": row["Y0"] = 1 - row["Y0"]
        elif field == "projection": row["projection"]["future_reward"] = 1
        else: row["branch"]["source_suffix_step_refs"] = []
    else:
        event = next(x for x in events if x["kind"] == "unit_completed" and x["payload"]["identity"]["operation"] == "step")
        if field == "event_id": event["event_id"] = "0"*64
        elif field == "previous": event["previous"] = None
        elif field == "identity": event["payload"]["identity"]["operation"] = "shadow_step"
        elif field == "action_id": event["payload"]["data"]["action_id"] = None
        elif field == "before": event["payload"]["data"]["before"]["valid_actions"] = []
        elif field == "adapter":
            event = next(x for x in events if x["kind"] == "unit_completed" and x["payload"]["identity"]["operation"] == "generation")
            event["payload"]["data"]["raw"]["adapter_mode"] = "BASE"
    with pytest.raises((ContractError, KeyError)):
        audit_run(run, events, tok)


def test_coherent_rehash_does_not_hide_missing_ActionID_receipt(complete):
    events = copy.deepcopy(complete[1])
    first = next(x for x in events if x["kind"] == "unit_completed" and x["payload"]["identity"]["operation"] == "step")
    first["payload"]["data"]["action_id"] = None
    rehash(events)
    # Cryptographic rehash authenticates bytes, not the source/branch semantic claim.
    validate_journal(events)
    with pytest.raises(ContractError): audit_run(complete[0], events, complete[2])


def test_journal_and_registry_refuse_existing_unit_or_output(tmp_path):
    journal = Journal(tmp_path/"j.jsonl", plan_sha256="a"*64, evidence_class="synthetic")
    reg = UnitRegistry(journal)
    identity = {"slot":"s","task_id":"t","phase":"source","index":0,"operation":"reset"}
    unit, started = reg.start(identity,{})
    reg.finish(identity,unit,started,{})
    with pytest.raises(ContractError, match="no retry"): reg.start(identity,{})
    journal.close()
    with pytest.raises(FileExistsError): Journal(tmp_path/"j.jsonl",plan_sha256="a"*64,evidence_class="synthetic")


def test_live_gate_rejects_before_any_boundary(tmp_path):
    class Forbidden:
        def __getattr__(self, name): raise AssertionError("boundary touched")
    with pytest.raises(ContractError,match="NOT_GRANTED"):
        Collector(synthetic_plan(),Ports(Forbidden(),lambda *_: (_ for _ in ()).throw(AssertionError()),"live"),tmp_path/"j")
    assert not (tmp_path/"j").exists()


@pytest.mark.parametrize("kind", ["drift", "producer_shape", "adapter", "input_cap", "physical_error"])
def test_technical_failure_stops_all_later_slots_without_retry(tmp_path,kind):
    options = {"drift":True} if kind == "drift" else None
    def mutate(raw, boundary):
        if len(boundary.calls) != 1:return raw
        if kind == "producer_shape": return dict(raw, operation="task_actor_generation")
        if kind == "adapter": return dict(raw,adapter_mode="BASE")
        if kind == "physical_error": raise RuntimeError("synthetic hardware fault")
        return raw
    budget = Budget(caps=Caps(per_call_input=1)) if kind=="input_cap" else None
    run,events,tok,raw,envs=collect_synthetic(tmp_path/kind,mutate=mutate,env_options=options,budget=budget)
    assert run["status"] == "STOPPED" and run["slots"][0]["YT"] is None
    assert run["slots"][0]["Y0"] is None  # no manufactured failed source unit
    assert all(r["disposition"]=="NOT_ATTEMPTED_AFTER_STOP" for r in run["slots"][1:])
    validate_journal(events)
    assert len(envs)<=2
    with pytest.raises(ContractError,match="complete software"): audit_run(run,events,tok)
    if kind in ("producer_shape","adapter","physical_error"):
        assert run["cost"]["reserved_or_spent"]["generations"] == 1
        assert run["cost"]["open_units"]  # unknown generation retained, never refunded/retried


@pytest.mark.parametrize("state_kind", ["early", "empty", "teacher_terminal", "invalid_stage_one", "invalid_stage_two", "truncated_stage_one"])
def test_early_invalid_terminal_NA_and_EOS_semantics(tmp_path,state_kind):
    first = synthetic_plan()[0].task_id
    def options(slot,phase):
        return {state_kind:True} if slot.task_id==first and state_kind in ("early","empty","teacher_terminal") else {}
    def mutate(raw,boundary):
        is_target = f"synthetic task {first.rsplit('/',1)[-1]}." in raw["prompt"] and first.split('/')[0] in raw["prompt"]
        phase1=raw["max_new_tokens"]==40
        phase2=raw["prompt"].startswith("Select the one currently available action")
        if is_target and ((state_kind=="invalid_stage_one" and phase1) or (state_kind=="invalid_stage_two" and phase2)):
            ids=boundary.tokenizer("bad")["input_ids"]+[1]
            raw.update(raw_output="bad",token_ids=ids,generated_tokens=len(ids),token_ids_sha256=hashlib.sha256(json.dumps(ids,separators=(',',':')).encode()).hexdigest(),token_cap_reached=False)
        if is_target and state_kind=="truncated_stage_one" and phase1:
            ids=raw["token_ids"][:-1]+[boundary.tokenizer.token(" ")]
            raw.update(token_ids=ids,token_ids_sha256=hashlib.sha256(json.dumps(ids,separators=(',',':')).encode()).hexdigest(),output_complete=False)
        return raw
    run,events,tok,_,envs=collect_synthetic(tmp_path/state_kind,mutate=mutate,env_options=options)
    assert run["status"]=="COMPLETE"
    row=run["slots"][0]
    audit_run(run,events,tok)
    if state_kind in ("early","empty"):
        assert row["disposition"]=="NO_ELIGIBLE_STATE" and row["YT"] is None and row["branch"] is None
    elif state_kind=="teacher_terminal":
        assert row["YT"]==1 and row["branch"]["suffix"]["generations"]==[]
    else:
        assert row["disposition"]=="INVALID_TEACHER" and row["YT"] is None
        assert row["branch"]["stage_one"] and row["branch"]["stage_two"] and row["branch"]["teacher_step"] is None


@pytest.mark.parametrize("key", ["generations","environment_operations","generated_tokens","input_tokens"])
def test_budgets_reserve_before_call_and_cannot_widen(key):
    with pytest.raises(ContractError): Caps(**{key:getattr(Caps(),key)+1})
    caps=Caps(**{key:1})
    b=Budget(caps=caps)
    if key=="environment_operations":
        b.reserve("a")
        with pytest.raises(ContractError,match="pre-call"): b.reserve("b")
    elif key=="generations":
        b.reserve("a",input_tokens=1,output_cap=1);b.complete("a",actual_output=1)
        with pytest.raises(ContractError,match="pre-call"):b.reserve("b",input_tokens=1,output_cap=1)
    else:
        with pytest.raises(ContractError,match="pre-call"):b.reserve("a",input_tokens=2,output_cap=2)


def test_GPUallocation_times_monotonic_and_clock_reversal():
    times=iter([100.0,100.0,7300.1])
    b=Budget(allocated_devices=2,monotonic=lambda:next(times))
    b.reserve("a")
    with pytest.raises(ContractError,match="device-hour"):b.complete("a")
    times=iter([100.0,99.0]);b=Budget(monotonic=lambda:next(times))
    with pytest.raises(ContractError,match="reversed"):b.reserve("x")


def test_public_state_whitelist_rejects_hidden_fields():
    value=PublicState("pick_and_place_simple/s","pick_and_place_simple","goal","obs",("wait",)).to_dict()
    value["future_reward"]=1
    with pytest.raises(ContractError,match="hidden/future"):PublicState.from_dict(value)
'''
FILES['tests/test_si_p3_learning.py']=r'''"""Full production pool/adoption/collator path and bounded CPU PEFT roundtrip."""
import copy
import hashlib
import json
from collections import Counter
from dataclasses import replace
from pathlib import Path

import pytest

from self_improvement.si_p3.contract import (ADOPTION_QUOTAS, BACKGROUND_QUOTAS, FAMILIES, ContractError, rank)
from self_improvement.si_p3.data import (CompletionCollator, Example, Pool, adopt_once, audit_exposure, build_pool,
                                         encode_example, fixed_schedule, paired_slots, select_background)
from self_improvement.si_p3.continuation import (RECIPE, Final18Controller, load_p0_continuation,
                                                parameter_fingerprint, require_cpu_toy, validate_recipe)
from sft.training import directory_sha256
from si_p3_support import collect_synthetic,synthetic_background


@pytest.fixture(scope="module")
def pipeline(tmp_path_factory):
    folder=tmp_path_factory.mktemp("si-p3-software-pool")
    run,events,tok,raw,envs=collect_synthetic(folder)
    pool=build_pool(run,events,tok)
    adoption=adopt_once(pool)
    bg,file,tasks,rows=synthetic_background(folder,tok)
    pairs=paired_slots(adoption,bg)
    exposure=audit_exposure(pairs,CompletionCollator(tok.pad_token_id))
    return folder,run,events,tok,pool,adoption,bg,file,tasks,rows,pairs,exposure


def test_nonempty_multifamily_production_quality_adoption_and_exposure(pipeline):
    _,run,events,tok,pool,adoption,bg,_,_,_,pairs,exposure=pipeline
    assert len(pool.dispositions)==len(pool.candidates)==96
    assert len(adoption.C)==len(adoption.B)==24
    assert Counter(x.example.family for x in adoption.C)==Counter(ADOPTION_QUOTAS)
    assert adoption.audit["selected_B_neutral"]>=8
    assert all(x.YT==1 for x in adoption.B)  # C remains eligible for B
    assert all(x.Y0==0 and x.YT==1 for x in adoption.C)
    assert len(bg)==120 and Counter(x.family for x in bg)==Counter(BACKGROUND_QUOTAS)
    assert len(pairs)==144 and exposure["optimizer_updates"]==18
    assert len(exposure["microbatch_loss_tokens"])==144
    assert all(b==c for b,c in exposure["microbatch_loss_tokens"])
    assert all(b==c for b,c in exposure["update_loss_tokens"])
    assert all(x<=1.05 for x in exposure["prompt_ratios"].values())


def test_actual_collator_preserves_EOS_when_PAD_equals_EOS(pipeline):
    tok=pipeline[3];pairs=pipeline[10]
    ex1,ex2=pairs[0][0],pairs[-1][0]
    batch=CompletionCollator(tok.eos_token_id)([ex1,ex2])
    for i,ex in enumerate([ex1,ex2]):
        assert batch["labels"][i,len(ex.input_ids)-1].item()==tok.eos_token_id
        assert all(x==-100 for x in batch["labels"][i,:ex.prompt_tokens].tolist())
        assert all(x==-100 for x in batch["labels"][i,len(ex.input_ids):].tolist())
        assert int((batch["labels"][i,1:]!=-100).sum())==ex.loss_tokens


def test_S_hash_rules_are_fixed_and_do_not_replace_bad_selected_task(pipeline,tmp_path):
    _,_,_,tok,_,_,bg,file,tasks,rows,*_=pipeline
    selected=bg[0].task_id
    altered=[r for r in rows if r["task_id"]!=selected]
    path=tmp_path/"missing.jsonl";path.write_text(''.join(json.dumps(r)+'\n' for r in altered))
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    with pytest.raises(ContractError,match="no replacement"):
        select_background(path,tok,tasks,evidence_class="synthetic",synthetic_sha256=sha)
    with pytest.raises(ContractError,match="file hash"):
        select_background(file,tok,tasks,evidence_class="historical")
    reverse=tmp_path/"reverse.jsonl";reverse.write_text(''.join(json.dumps(r)+'\n' for r in reversed(rows)))
    result=select_background(reverse,tok,list(reversed(tasks)),evidence_class="synthetic",synthetic_sha256=hashlib.sha256(reverse.read_bytes()).hexdigest())
    assert result==bg
    assert bg[0].task_id==min((t['task_id'] for t in tasks if t['family']==FAMILIES[0]),key=lambda t:(rank('SI-P3-S-v1',FAMILIES[0],t),t))


@pytest.mark.parametrize("failure",["Q","C","neutral","B_contrast","projections","length"])
def test_common_quality_and_fixed_draw_guards_do_not_redraw(pipeline,failure):
    pool=pipeline[4];rows=list(pool.candidates)
    if failure=="Q":rows=rows[:71]
    elif failure=="C":rows=[replace(x,Y0=1) for x in rows]
    elif failure=="neutral":rows=[replace(x,Y0=0) for x in rows]
    elif failure=="B_contrast":
        selected=set(pipeline[5].audit['selected_B'])
        rows=[replace(x,Y0=0) if x.example.task_id in selected else x for x in rows]
    elif failure=="projections":rows=[replace(x,example=replace(x.example,projection_sha256='same')) for x in rows]
    elif failure=="length":
        rows=[replace(x,example=replace(x.example,labels=x.example.labels+((1,) if x.Y0==0 else (1,1)))) for x in rows]
    changed=Pool(tuple(rows),pool.dispositions,pool.integrity)
    if failure=="length":
        # Matching may draw only C for those cells; neutral>=8 rejects without alternate C/B.
        with pytest.raises(ContractError):adopt_once(changed)
    else:
        with pytest.raises(ContractError):adopt_once(changed)


@pytest.mark.parametrize("change",["shuffle","drop_last","extra_epoch","duplicate_task","prompt_tokens","loss_tokens","S_change"])
def test_paired_exposure_guards_reject_mask_order_dose_or_resource_tamper(pipeline,change):
    pairs=list(pipeline[10]);schedule=fixed_schedule();collator=CompletionCollator(pipeline[3].pad_token_id)
    if change=="shuffle":schedule=(tuple(reversed(schedule[0])),schedule[1])
    elif change=="drop_last":schedule=(schedule[0][:-1],schedule[1])
    elif change=="extra_epoch":schedule=schedule+(schedule[0],)
    elif change=="duplicate_task":pairs[-1]=(pairs[-2][0],pairs[-1][1])
    elif change=="prompt_tokens":
        b,c=pairs[-1];pairs[-1]=(replace(b,prompt_tokens=b.prompt_tokens*50),c)
    elif change=="loss_tokens":
        b,c=pairs[-1];pairs[-1]=(replace(b,labels=b.labels[:-1]+(-100,)),c)
    else:
        b,c=pairs[0];pairs[0]=(b,replace(c,command='changed'))
    with pytest.raises(ContractError):audit_exposure(pairs,collator,schedule)


@pytest.mark.parametrize("key,value",[("epochs",3),("checkpoint","best_loss"),("warm_start","get_peft_model"),("drop_last",True),("independent_arm_shuffle",True),("updates",19)])
def test_recipe_rejects_search_fresh_lora_and_extra_training(key,value):
    cfg=dict(RECIPE);cfg[key]=value
    with pytest.raises(ContractError):validate_recipe(cfg)


def test_genuine_CPU_PEFT_warmstart_fresh_optimizer_final18_and_roundtrip(pipeline,tmp_path):
    import torch
    from peft import LoraConfig,TaskType,get_peft_model,PeftModel
    from transformers import LlamaConfig,LlamaForCausalLM
    torch.set_num_threads(1)
    torch.manual_seed(42)
    config=LlamaConfig(vocab_size=max(1024,len(pipeline[3].vocab)+16),hidden_size=16,intermediate_size=32,
                       num_hidden_layers=1,num_attention_heads=2,num_key_value_heads=2,
                       max_position_embeddings=2048,bos_token_id=2,eos_token_id=1,pad_token_id=1)
    base=LlamaForCausalLM(config)
    untouched=copy.deepcopy(base.state_dict())
    # Fixture construction only; production loader must never create a fresh adapter.
    expert=get_peft_model(base,LoraConfig(task_type=TaskType.CAUSAL_LM,r=32,lora_alpha=64,lora_dropout=.05,bias='none',target_modules='all-linear'))
    with torch.no_grad():
        for name,p in expert.named_parameters():
            if 'lora_B' in name:p.fill_(.005)
    adapter=tmp_path/'toy_original_adapter';expert.save_pretrained(adapter)
    expected=directory_sha256(adapter)
    models=[];receipts=[]
    for arm in ('B','C'):
        fresh=LlamaForCausalLM(config);fresh.load_state_dict(untouched)
        model,receipt=load_p0_continuation(fresh,adapter,evidence_class='cpu_toy_software',expected_adapter_sha256=expected)
        models.append(model);receipts.append(receipt)
    assert receipts[0]['initial_lora_parameters_sha256']==receipts[1]['initial_lora_parameters_sha256']
    assert receipts[0]['initial_frozen_parameters_sha256']==receipts[1]['initial_frozen_parameters_sha256']
    assert receipts[0]['actual_P0_verified'] is False
    for arm,model in zip(('B','C'),models):
        controller=Final18Controller(model,pipeline[10],CompletionCollator(1),tmp_path/arm,arm=arm,evidence_class='cpu_toy_software')
        assert not controller.optimizer.state
        with pytest.raises(ContractError,match='final18'):controller.finish()
        with pytest.raises(ContractError,match='slot order'):controller.consume([999,998])
        for slots in controller.microbatches:controller.consume(slots)
        result=controller.finish()
        assert result['updates']==18 and result['initial_lora_sha256']!=result['final_lora_sha256']
        assert result['real_training_performed'] is False
        assert parameter_fingerprint(model,lora=False)==controller.frozen_before
        with pytest.raises(ContractError):controller.consume(controller.microbatches[0])
        with pytest.raises(ContractError):controller.finish()
        fresh=LlamaForCausalLM(config);fresh.load_state_dict(untouched)
        reloaded=PeftModel.from_pretrained(fresh,tmp_path/arm/'final_update18_adapter',local_files_only=True)
        assert parameter_fingerprint(reloaded,lora=True)==result['final_lora_sha256']
        with pytest.raises(FileExistsError):Final18Controller(model,pipeline[10],CompletionCollator(1),tmp_path/arm,arm=arm,evidence_class='cpu_toy_software')
    with pytest.raises(ContractError,match='NOT_GRANTED'):
        load_p0_continuation(models[0],adapter,evidence_class='live',expected_adapter_sha256=expected)
    wrong=LlamaForCausalLM(config)
    with pytest.raises(ContractError,match='identity'):
        load_p0_continuation(wrong,adapter,evidence_class='cpu_toy_software',expected_adapter_sha256='0'*64)
'''
for name,body in FILES.items():
 p=ROOT/name;assert not p.exists();p.write_text(body);print(name)
