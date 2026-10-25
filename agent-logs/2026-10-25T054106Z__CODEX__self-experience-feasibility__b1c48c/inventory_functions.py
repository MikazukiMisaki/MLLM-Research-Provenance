"""Audit-only helpers. Reads observed records; emits identifiers/counts, no targets."""
import collections
import hashlib
import json
from pathlib import Path
import re


def run_audit(ns):
    OWN, STAGES, META, FROZEN, RUNTIME, R19 = (ns[k] for k in ('OWN','STAGES','META','FROZEN','RUNTIME','R19'))
    digest=ns['digest']
    input_table={}
    def register(path):
        path=Path(path)
        if str(path) not in input_table:
            input_table[str(path)]={'path':str(path),'bytes':path.stat().st_size,'sha256_before':digest(path)}
        return path
    def readjson(path):return json.loads(register(path).read_text())
    def rows(path):
        path=register(path)
        with path.open('rb') as stream:
            for n,line in enumerate(stream,1):
                if line.strip():yield n,hashlib.sha256(line).hexdigest(),json.loads(line)
    def canonical(value):
        if not value:return None
        parts=str(value).replace('\\','/').rstrip('/').split('/')
        for j in range(len(parts)-1,0,-1):
            if parts[j].startswith('trial_'):return parts[j-1]+'/'+parts[j]
        return str(value)
    def md(step):return step.get('policy_metadata') or step.get('metadata',{}).get('policy') or step.get('metadata',{})
    def sel(step):return md(step).get('action_selection') or step.get('metadata',{}).get('action_selection',{})
    def bind(step):
        s=sel(step);am=s.get('id_to_command') or {}
        aid=step.get('action_id') or s.get('parsed_action_id')
        command=step.get('mapped_command') or step.get('action') or s.get('mapped_environment_command')
        return bool(am),bool(am and aid in am and am[aid]==command)
    def token_summary(values):
        values=sorted(x for x in values if isinstance(x,(int,float)))
        return {'recorded_count':len(values),'min':values[0] if values else None,'max':values[-1] if values else None,'median':values[len(values)//2] if values else None,'note':'Only pre-existing counts; no tokenizer; upper-middle order statistic for even count.'}
    def summ_units(units):
        tasks={u['canonical_task'] for u in units if u.get('canonical_task')}
        episodes={u['episode_key'] for u in units if u.get('episode_key')}
        return {'rows':len(units),'canonical_tasks':len(tasks),'episode_identity_keys':len(episodes),'families':dict(collections.Counter(u.get('family') for u in units))}
    def pair_label(c,t):
        if c not in (0,1,False,True) or t not in (0,1,False,True):return 'INCOMPLETE_OR_UNKNOWN'
        if not c and t:return 'ACTUAL_RESCUE'
        if c and not t:return 'HARM'
        return 'NEUTRAL_SUCCESS' if c else 'NEUTRAL_FAILURE'
    manifest_data={k:readjson(p) for k,p in META.items() if p.is_file()}
    manifest_rows={k:{r['prefix_id']:r for r in v.get('prefixes',[])} for k,v in manifest_data.items() if k.endswith('_PREFIX')}
    primary_paths={
      'R19_FORMAL_SUMMARY':Path('/home/lizening/research-notes/agent-logs/2026-10-23T043602Z__LUNA__r19-g4-readiness__85cbb923/future_g4_report/summary.json'),
      'R19_OPPORTUNITY':Path('/home/lizening/research-notes/agent-logs/2026-10-23T043602Z__LUNA__r19-g4-readiness__85cbb923/future_g4_report/R19_OPPORTUNITY_REPORT.md'),
      'R19_ACCEPTANCE':Path('/home/lizening/research-notes/agent-logs/2026-10-25T040304Z__SOL__r19-g4-independent-result-review__85cbb923_dffaf4/independent_G4_acceptance.json'),
      'TASK':Path('/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/SOL_RESEARCH_TASK.md'),
      'ALIGNMENT':Path('/home/lizening/research-notes/agent-logs/2026-10-25T053211Z__SOL__self-improvement-alignment__e9c877/SELF_IMPROVEMENT_ALIGNMENT_AND_INNOVATION.md'),
      'R19_PROTOCOL':FROZEN/'R19_PROTOCOL.md',
    }
    for path in primary_paths.values():register(path)
    for name in ['SPRINT_2C_PAIRED_CORPUS.md','SFT_RECOVERY_FEASIBILITY_RESULTS.md','PERSISTENT_RECOVERY_R12_MECHANISM_AUDIT.md','PROGRESS_AWARE_RECOVERY_OSR_R16.md','PROGRESS_AWARE_RECOVERY_PAR_R17.md','PROGRESS_AWARE_RECOVERY_FACT_TEXT_R18_C1.md','PROGRESS_AWARE_RECOVERY_CARD_V2_R18_C2.md','PROGRESS_AWARE_RECOVERY_R18_B_V2_TREATMENT_FREEZE.md','SFT_DATASET_AUDIT.md','SFT_POLICY_BOOTSTRAP.md']:
        register(FROZEN/'reports'/name)
    inventory={'schema':'SI_P0_EXISTING_RECORD_AUDIT_V1','task_id':'SI-P0-SOL-b1c48c','not_training_data':True,'scientific_execution_permission':'NOT_GRANTED','statuses':{'OBSERVED':'Direct fields or recount of completed historical records','INFERRED':'Interpretation or design constraint, not a new outcome','NOT_PROVEN':'Missing identity/causal/learning claim'},'stage_summaries':{},'cohort_indices':{},'ordinary_source_success_indices':{},'gaps':[]}
    stage_units={};source_sets={};positive_refs=[];fingerprint_maps={}
    for stage in ['SPRINT_SOURCE','R1_SOURCE','R7_SOURCE','R14_SOURCE','R19_SOURCE']:
        units=[];success_index=[];ev=collections.Counter();ins=[];outs=[];term=collections.Counter()
        for n,sha,r in rows(STAGES[stage]):
            steps=r.get('steps',[]);task=canonical(r.get('task',{}).get('task_id'));meta=r.get('metadata',{})
            success=bool(steps and steps[-1].get('done') and steps[-1].get('reward',0)>0)
            reason=meta.get('termination_reason','UNKNOWN');term[reason]+=1
            family=r.get('task',{}).get('family') or meta.get('task_family')
            u={'canonical_task':task,'family':family,'episode_key':r.get('trajectory_id'),'schedule_index':meta.get('schedule_index'),'nominal_seed':r.get('seed'),'success':int(success),'source_line':n,'source_row_sha256':sha,'steps':len(steps),'horizon':meta.get('max_steps'),'termination_reason':reason}
            units.append(u)
            if success:success_index.append(u)
            for step in steps:
                p=md(step);raw=step.get('model_output') or step.get('raw_output')
                ev['decisions']+=1;ev['prompt_present']+=bool(p.get('prompt'));ev['raw_output_present']+=bool(raw);ev['observation_present']+=bool(step.get('observation'));ev['result_observation_present']+=bool(step.get('result_observation'))
                present,ok=bind(step);ev['action_map_present']+=present;ev['selected_id_maps_to_executed_command']+=ok
                if not ok:ev['mapping_unbound_or_nonselected']+=1
                ts=step.get('token_statistics',{});ins.append(ts.get('input_tokens'));outs.append(ts.get('generated_tokens'))
            if not task:inventory['gaps'].append(stage+': missing canonical task at line '+str(n))
        stage_units[stage]=units;source_sets[stage]={u['canonical_task'] for u in units}
        inventory['ordinary_source_success_indices'][stage]=success_index
        inventory['stage_summaries'][stage]={**summ_units(units),'observed_source_successes':len(success_index),'observed_source_nonsuccesses':len(units)-len(success_index),'source_hash_ref':str(STAGES[stage]),'actor':'base H4' if stage=='SPRINT_SOURCE' else 'frozen SFT-P0','resolved_base_weights_revision':'b968826d9c46dd6066d109eabc6255188de91218' if stage=='R19_SOURCE' else 'UNKNOWN','adapter_sha256':None if stage=='SPRINT_SOURCE' else '6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11','structural_evidence':dict(ev),'recorded_input_tokens':token_summary(ins),'recorded_output_tokens':token_summary(outs),'termination_reasons':dict(term),'semantic_public_only_and_temporal_projection':'NOT_PROVEN_PER_TRAINING_ROW','scope':'completed historical TRAIN sources only; ordinary successes not paired rescue labels'}
    source_like={'R3_CONTINUE':('continue','success'),'R9_CONTINUE':(None,'continue_success'),'R15_CONTINUE':(None,'r_continue')}
    pair_stages=['SPRINT2C','R4','R9_CONTINUE','R10_OSR','R11_PBR','R15_CONTINUE','R16_OSR','R17_PAR','R18_C1','R18_C2']
    for stage in pair_stages:
        units=[];labels=collections.Counter();evidence=collections.Counter();ins=[];outs=[];positive=[];harmful=[]
        for n,sha,row in rows(STAGES[stage]):
            r=row.get('compact',row) if stage=='R11_PBR' else row
            pid=r.get('prefix_id');task=canonical(r.get('task_id'));family=r.get('task_family') or r.get('family');h=r.get('remaining_horizon');d=r.get('selected_decision_index');ph=None
            if stage=='SPRINT2C':
                c=int(r['continue']['success']);t=int(r['recover']['success']);d=r['action_count'];h=r['remaining_horizon'];ph=r['prefix_sha256'];s2=r['recovery'].get('stage_two',{});gen=s2;parsed=s2;steps=r['recover'].get('steps',[]);rep=bool(r['reconstruction_provenance'].get('continue_exact') and r['reconstruction_provenance'].get('recover_exact'));episode=r['episode_group_id']
                s1=r['recovery'].get('stage_one',{});s1valid=s1.get('status')=='valid'
            elif stage=='R4':
                c=int(r['continue']['success']);t=int(r['recover']['success']);d=r['selected_decision_index'];h=r['prefix_replay']['remaining_horizon'];ph=manifest_rows['R4_PREFIX'][pid]['complete_prefix_sha256'];sf=r['raw_generations']['recovery'].get('stage_two',{});gen=sf.get('generation',{});parsed=sf.get('parsed',{});steps=r['recover'].get('continuation',{}).get('steps',[]);rep=r['prefix_replay'].get('replay_match');episode=str(r.get('source_schedule_index'));s1valid=r['recover']['stage_one'].get('status')=='valid'
            elif stage in source_like:
                par,key=source_like[stage];v=r[par] if par else r;c=int(v[key]);t=None;gen={};parsed={};steps=v.get('steps',[]) if par else r.get('steps',r.get('continue_full',{}).get('steps',[]));rep=r.get('exact_suffix_match',r.get('suffix_exact',r.get('replay',{}).get('replay_match')));episode=str(r.get('schedule_index'));s1valid=None
            else:
                c=int(r['r_continue']);key={'R10_OSR':'r_osr','R11_PBR':'r_pbr','R16_OSR':'r_osr','R17_PAR':'r_par','R18_C1':'r_fact_text','R18_C2':'r_card_v2'}[stage];t=int(r[key]);episode=str(r.get('schedule_index'));s1valid=r.get('stage_one_valid',r.get('stage1_valid'))
                rf=row.get('recovery_full',{})
                if stage in ('R18_C1','R18_C2'):
                    rf=r['recovery'];gen=rf.get('stage_two_generation',{});parsed=rf.get('stage_two_parsed',{});steps=r.get('continuation',{}).get('steps',[]);rep=bool(r.get('replay',{}).get('replay_pass',all(r.get('replay',{}).get('checks',{}).values())));ph=r.get('replay',{}).get('complete_public_prefix_sha256')
                else:
                    sf=rf.get('stage_two',{});sf=sf[0] if isinstance(sf,list) and sf else sf;gen=sf.get('generation',{}) if isinstance(sf,dict) else {};parsed=sf.get('parsed',{}) if isinstance(sf,dict) else {};steps=row.get('continuation_full',{}).get('steps',[]);rep=row.get('replay_full',{}).get('replay_match',r.get('replay',{}).get('replay_match',True if stage=='R11_PBR' else None));ph=r.get('replay',{}).get('complete_public_prefix_sha256') or r.get('replay_identity',{}).get('complete_public_prefix_sha256') or row.get('replay_full',{}).get('source_complete_public_prefix_sha256')
            if stage in ('R9_CONTINUE','R10_OSR','R11_PBR'):
                m=manifest_rows['R12_PREFIX'].get(pid,{});ph=ph or m.get('complete_public_prefix_sha256');d=d if d is not None else m.get('selected_decision_index');h=h if h is not None else m.get('remaining_horizon');episode=m.get('deterministic_episode_hash',episode)
            if stage.startswith('R1') and stage not in ('R10_OSR','R11_PBR'):
                m=manifest_rows['R15_PREFIX'].get(pid,{})
                if m:d=m['selected_decision_index'];h=m['remaining_horizon'];episode=str(m['schedule_index'])
            label=pair_label(c,t) if t is not None else 'ORDINARY_CONTINUE_REFERENCE'
            labels[label]+=1
            amap=parsed.get('id_to_command',{});aid=parsed.get('action_id');cmd=parsed.get('action',parsed.get('mapped_command',r.get('recovery_mapped_command')))
            evidence['records']+=1;evidence['replay_recorded_exact']+=bool(rep);evidence['stage2_prompt_present']+=bool(gen.get('prompt'));evidence['stage2_raw_output_present']+=bool(gen.get('raw_output'));evidence['stage2_action_map_present']+=bool(amap);evidence['stage2_selected_id_binding']+=bool(amap and aid in amap and amap[aid]==cmd);evidence['stage1_valid']+=bool(s1valid)
            if gen:ins.append(gen.get('input_tokens'));outs.append(gen.get('generated_tokens'))
            evidence['continuation_decisions']+=len(steps)
            for st in steps:
                evidence['continuation_prompt_present']+=bool(st.get('prompt') or md(st).get('prompt'))
                present,ok=bind(st);evidence['continuation_map_present']+=present;evidence['continuation_id_binding']+=ok
            u={'prefix_id':pid,'canonical_task':task,'family':family,'episode_key':episode,'decision_index':d,'remaining_horizon':h,'prefix_hash':ph,'continue_success':c,'treatment_success':t,'label':label,'source_line':n,'source_row_sha256':sha,'stage1_valid_recorded':s1valid,'stage2_prompt_present':bool(gen.get('prompt')),'stage2_raw_present':bool(gen.get('raw_output')),'stage2_id_map_bound':bool(amap and aid in amap and amap[aid]==cmd),'replay_recorded_exact':bool(rep)}
            units.append(u)
            if label=='ACTUAL_RESCUE':positive.append(pid);positive_refs.append({'stage':stage,**u})
            if label=='HARM':harmful.append(pid)
        stage_units[stage]=units;source_sets[stage]={u['canonical_task'] for u in units if u.get('canonical_task')}
        fingerprint_maps[stage]={u['prefix_id']:u.get('prefix_hash') for u in units}
        inventory['cohort_indices'][stage]=units
        inventory['stage_summaries'][stage]={**summ_units(units),'labels':dict(labels),'continue_successes':sum(u['continue_success'] for u in units),'treatment_successes':sum(u['treatment_success'] for u in units if u['treatment_success'] is not None) if stage not in source_like else None,'actual_rescue_prefix_ids':positive,'harm_prefix_ids':harmful,'structural_evidence':dict(evidence),'stage2_recorded_input_tokens':token_summary(ins),'stage2_recorded_output_tokens':token_summary(outs),'resolved_base_weights_revision':'UNKNOWN','source_path':str(STAGES[stage]),'scope':'historical stratified TRAIN development, not new independent training data'}
    # R3 is a reference shard of the existing R4 comparison, not a fresh paired corpus.
    r3=[]
    for n,sha,r in rows(STAGES['R3_CONTINUE']):
        r3.append({'prefix_id':r['prefix_id'],'canonical_task':canonical(r['task_id']),'episode_key':str(r.get('source_schedule_index')),'family':r.get('task_family'),'continue_success':int(r['continue']['success'])})
    source_sets['R3_CONTINUE']={u['canonical_task'] for u in r3}
    inventory['stage_summaries']['R3_CONTINUE']={**summ_units(r3),'continue_successes':sum(u['continue_success'] for u in r3),'reused_as':'R4 CONTINUE reference; not independent of R4'}
    # R19 records already contain all observed arm outcomes; no detector/rule is applied here.
    units=[];eligible=[];arm_counts=collections.Counter();arm_labels={str(k):collections.Counter() for k in range(1,6)};aliases=collections.Counter();rescues={str(k):[] for k in range(1,6)};special=[];evidence_ids=set();recovery_ids=set();suffix_ids=set();suffix_shared=collections.Counter()
    for n,sha,r in rows(STAGES['R19_BRANCHES']):
        task=canonical(r['canonical_trial_id']);ks=r.get('k_results',{});c=int(r['continue_success'])
        u={'prefix_id':r['prefix_id'],'canonical_task':task,'family':r['task_family'],'episode_key':str(r['source_schedule_index']),'decision_index':r['decision_index'],'remaining_horizon':50-r['decision_index'],'continue_success':c,'eligible_primary':r['eligible_primary'],'eligibility_reason':r['eligibility_reason'],'k_success':{k:v.get('success') for k,v in ks.items()},'source_line':n,'source_row_sha256':sha,'aliases':{k:{'derived_identity_from':v.get('derived_identity_from'),'derived_source_event_id':v.get('derived_source_event_id'),'checkpoint':v.get('checkpoint'),'derived_evidence_from_checkpoint':v.get('derived_evidence_from_checkpoint')} for k,v in ks.items() if v.get('derived_identity_from') is not None or v.get('derived_source_event_id') is not None}}
        units.append(u)
        for k,v in ks.items():
            arm_counts[k]+=1
            refs=v.get('evidence_refs',{})
            for refkey,ids in refs.items():
                if isinstance(ids,list):
                    evidence_ids.update(ids)
                    if 'recovery' in refkey:recovery_ids.update(ids)
                    if 'sft' in refkey:suffix_ids.update(ids)
            suffix_shared[tuple(refs.get('sft_generation_event_ids',[]))]+=1
            if v.get('derived_identity_from') is not None or v.get('derived_source_event_id') is not None:aliases[k]+=1
            if r['eligible_primary']:
                label=pair_label(c,v.get('success'));arm_labels[k][label]+=1
                if label=='ACTUAL_RESCUE':rescues[k].append({'prefix_id':r['prefix_id'],'canonical_task':task,'family':r['task_family'],'source_line':n,'source_row_sha256':sha,'arm_event_id':v['arm_event_id'],'terminal':v.get('terminal'),'sft_terminal':v.get('sft_terminal'),'sft_termination_reason':v.get('sft_termination_reason'),'recovery_environment_actions':v.get('recovery_environment_actions'),'sft_environment_actions':v.get('sft_environment_actions'),'continue_success':c,'treatment_success':v.get('success')})
        if r['eligible_primary']:eligible.append(u)
        if r['prefix_id'].endswith(('8ec4fc037229710f8f13','bf448be94724da4562c0')):
            p=r.get('passive_stopping_estimate',{})
            special.append({'prefix_id':r['prefix_id'],'continue_success':c,'k_success':u['k_success'],'passive':{key:p.get(key) for key in ['coverage','status','selected_k','estimated_success','estimated_logical_cost','branch_mapping_exact']},'evaluations':p.get('evaluations_through_selected_checkpoint'),'note':'Observed oracle-over-K2 cases only; not rescue relative to CONTINUE; no new rule evaluated'})
    inventory['cohort_indices']['R19_BRANCHES']=units;source_sets['R19_BRANCHES']={u['canonical_task'] for u in units}
    inventory['stage_summaries']['R19_BRANCHES']={**summ_units(units),'eligible':summ_units(eligible),'ineligible_attempts':len(units)-len(eligible),'observed_arm_records':dict(arm_counts),'labels_vs_continue_in_eligible':{k:dict(v) for k,v in arm_labels.items()},'derived_alias_records':dict(aliases),'distinct_referenced_events':len(evidence_ids),'source_path':str(STAGES['R19_BRANCHES']),'actual_K2_rescues':rescues['2'],'rescue_prefix_ids_by_K':{k:[x['prefix_id'] for x in v] for k,v in rescues.items()},'oracle_over_K2_cases':special,'resolved_base_weights_revision':'b968826d9c46dd6066d109eabc6255188de91218','adapter_sha256':'6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11','note':'183 logical K arms and aliases are not 183 independent experiences; measured common-path/suffix refs, own per-K costs preserved'}
    # Audit actual completed event records for structural lineage only; no project validator.
    kinds=collections.Counter();g=collections.Counter();firstschema={};physical_gen_ids=set();event_ref_found=set();phase=collections.Counter();token_in=[];token_out=[]
    for n,sha,r in rows(R19/'execution_events.jsonl'):
        kind=r['kind'];kinds[kind]+=1;payload=r.get('payload',{});identity=r.get('identity',{})
        if r.get('event_id') in evidence_ids:event_ref_found.add(r['event_id'])
        if kind=='generation_completed':
            physical_gen_ids.add(r['event_id']);phase[identity.get('operation') or identity.get('component') or 'UNKNOWN']+=1
            if kind not in firstschema:firstschema[kind]={'identity':identity,'payload_keys':list(payload),'nested_keys':{k:list(v) for k,v in payload.items() if isinstance(v,dict)}}
            # producer records generation evidence under result; inspect keys and aggregate only.
            ev=payload.get('evidence',{})
            result=ev.get('generation',payload.get('generation',payload.get('result',{})))
            amap=ev.get('action_map') or ev.get('id_to_command') or {};pr=ev.get('parser_result',ev);aid=pr.get('action_id');cmd=pr.get('action') or pr.get('mapped_command') or pr.get('command')
            g['action_map_present']+=bool(amap)
            g['selected_action_map_binding']+=bool(amap and aid in amap and amap[aid]==cmd)
            if isinstance(result,dict):
                g['generations']+=1;g['prompt_or_prompt_hash_present']+=bool(result.get('prompt') or result.get('prompt_sha256') or result.get('rendered_prompt_sha256'));g['raw_output_present']+=bool(result.get('raw_output'));token_in.append(result.get('input_tokens'));token_out.append(result.get('generated_tokens'))
    inventory['r19_event_lineage']={'event_counts':dict(kinds),'generation_operations':dict(phase),'generation_payload_first_schema':firstschema,'generation_structural_counts':dict(g),'recorded_input_tokens':token_summary(token_in),'recorded_generated_tokens':token_summary(token_out),'referenced_event_ids':len(evidence_ids),'referenced_event_ids_found':len(event_ref_found),'historical_cryptographic_chain_revalidation':'NOT_PERFORMED; use original independent acceptance; this is metadata lineage only'}
    # Original failed run is immutable and incomplete, not a task-failure episode.
    failed=R19.parent/'r19_b1_g3_pilot_after_a0de515d7e104101bf8157175ea3d995_20261022T190221Z'
    fm=readjson(failed/'execution_manifest.json');fu=readjson(failed/'unit_registry.json')
    for path in failed.iterdir():
        if path.is_file():register(path)
    fc=collections.Counter();fops=collections.Counter()
    for n,sha,r in rows(failed/'execution_events.jsonl'):
        fc[r['kind']]+=1
        if r['kind']=='environment_operation_completed':fops[r.get('payload',{}).get('operation')]+=1
    register(failed/'branches.jsonl')
    inventory['old_failed_G3']={'run_id':fm.get('run_id'),'status':fm.get('status'),'source_sha':fm.get('implementation_sha'),'event_counts':dict(fc),'completed_environment_operations':dict(fops),'branches_bytes':(failed/'branches.jsonl').stat().st_size,'unit_registry_top_keys':list(fu),'units_metadata':fu.get('units'),'classification':'INCOMPLETE_SOURCE_UNIT_NOT_TASK_FAILURE','training_candidate':False}
    inventory['campaign_cost_boundary']={'R19_cumulative_generations':5142,'R19_cumulative_reset_inclusive_environment_operations':7949,'includes_prior_cost':{'generations':177,'environment_operations':342},'this_SI_P0_scientific_calls':0,'not_all_project_total':True,'successful_G3_manifest_physical_expenditure':{k:v for k,v in manifest_data['R19_EXECUTION'].get('physical_expenditure',{}).items() if k!='observed_canonical_trial_ids'}}
    # Canonical identity overlap is intentionally cross-policy as well as within-policy.
    overlap=[]
    names=list(source_sets)
    for i,a in enumerate(names):
        for b in names[i+1:]:
            common=source_sets[a]&source_sets[b]
            if common:overlap.append({'stage_a':a,'stage_b':b,'shared_canonical_tasks':len(common)})
    inventory['canonical_identity_overlap_nonzero']=overlap
    selected=['SPRINT2C','R4','R9_CONTINUE','R15_CONTINUE','R19_BRANCHES']
    inventory['deduplication']={'selected_cohort_groups':selected,'selected_cohort_state_rows':sum(len(inventory['cohort_indices'][k]) for k in selected),'canonical_tasks_union':len(set().union(*(source_sets[k] for k in selected))),'do_not_call_independent_training_N':True,'within_cohort_tasks_with_multiple_states':{k:sum(v>1 for v in collections.Counter(u['canonical_task'] for u in inventory['cohort_indices'][k]).values()) for k in selected},'R16_R17_R18_same_prefix_ids':all(set(fingerprint_maps['R15_CONTINUE'])==set(fingerprint_maps[k]) for k in ['R16_OSR','R17_PAR','R18_C1','R18_C2']),'R16_R17_R18_task_decision_pairs_equal':all({(u['canonical_task'],u['decision_index']) for u in stage_units['R15_CONTINUE']}=={(u['canonical_task'],u['decision_index']) for u in stage_units[k]} for k in ['R16_OSR','R17_PAR','R18_C1','R18_C2']),'R12':'mechanism audit of R9/R10/R11; zero newly collected episodes','seed_identity_rule':'different seed never implies fresh canonical game/trial'}
    sft_pools=manifest_data['SFT_ACCEPTED_IDENTITIES']['pools'];training={canonical(r['task_id']) for r in sft_pools['train']};val={canonical(r['task_id']) for r in sft_pools['validation']};online={canonical(r['task_id']) for r in sft_pools['online_evaluation']}
    inventory['metadata_only_expert_split_overlap']={k:{'sft_expert_train_overlap':len(ts&training),'sft_expert_validation_overlap':len(ts&val),'sft_reserved_online_overlap':len(ts&online)} for k,ts in source_sets.items()}
    inventory['sft_expert_origin']={'expert_train_tasks':len(training),'expert_validation_tasks':len(val),'reserved_online_metadata_tasks':len(online),'self_generated':False,'outcomes_or_training_contents_read':False,'not_self_experience_candidate':True,'note':'Only identity metadata from accepted splits; expert training raw delegated elsewhere by coordinator'}
    inventory['actual_rescue_index_historical_treatments']=positive_refs
    all_positive=positive_refs+[x for refs in rescues.values() for x in refs]
    inventory['deduplication']['historical_rescue_task_union_all_listed_treatments']=len({x['canonical_task'] for x in all_positive})
    inventory['deduplication']['historical_rescue_state_union_all_listed_treatments']=len({(x['canonical_task'],x.get('decision_index',next((u['decision_index'] for u in eligible if u['prefix_id']==x['prefix_id']),None))) for x in all_positive})
    fixed_single=[x for x in positive_refs if x['stage'] in ('R4','R10_OSR','R16_OSR')]+rescues['1']
    inventory['deduplication']['post_SFT_single_action_OSR_K1_rescue_task_union']=len({x['canonical_task'] for x in fixed_single})
    inventory['deduplication']['post_SFT_single_action_OSR_K1_rescue_state_rows']=len(fixed_single)
    inventory['deduplication']['post_SFT_single_action_OSR_K1_rescue_families']=dict(collections.Counter(x['family'] for x in fixed_single))
    inventory['deduplication']['rescue_union_warning']='Upper audit counts over already outcome-selected heterogeneous methods; not training-ready samples or protocol N.'
    inventory['source_manifest_hash_comparisons']={}
    for m,key,stage in [('SPRINT_MANIFEST','source_h4_trajectory_sha256','SPRINT_SOURCE'),('R4_MANIFEST','source_trajectory_sha256','R1_SOURCE'),('R7_MANIFEST','raw_trajectory_sha256','R7_SOURCE'),('R14_MANIFEST','raw_trajectory_sha256','R14_SOURCE'),('R19_EXECUTION','branches_sha256','R19_BRANCHES')]:
        expected=manifest_data[m].get(key);actual=input_table[str(STAGES[stage])]['sha256_before']
        inventory['source_manifest_hash_comparisons'][stage]={'expected':expected,'actual':actual,'match':actual==expected if expected else None}
        if expected and actual!=expected:inventory['gaps'].append(stage+': raw file hash differs from named manifest value; preserve and investigate before construction.')
    inventory['gaps'] += ['Historical base model cache/weights revision is UNKNOWN outside R19; code git revisions and model_id are not weight revisions.','Prompt/map/transition structural presence is not proof of each projected SFT row public-only inputs or causal temporal cutoff.','No training rows exported; recovery Stage2 prompts contain subgoal/treatment context different from SFT-P0.','New independent-task identity universe and valid new evaluation sample size are NOT_PROVEN by this inventory.','Rescue selection observes historical terminal outcomes; no inference-time selector is authorized.','Sparse rescues and repeated tasks/treatments do not establish generalizable learning gain or a powered N.']
    for key,expected in [('TASK','d7a42a134345b4262c497221cceb4a3ccb066b90f0fcd5e64fee94bd35e8f4af'),('R19_FORMAL_SUMMARY','6ff56b7e9bc31c29bc9afd0c3ceea43c4fdf53b2addb29d3ce9f2c5e99b5d3c4'),('R19_OPPORTUNITY','92c066ad1c9c7f187430db82ad6285800e4f31005a1fd2933231d30d695df4bc'),('R19_ACCEPTANCE','7331b865778481ab4e1b10943eac0e4090ea004e214dbdfff283cfbe042833e6')]:
        got=input_table[str(primary_paths[key])]['sha256_before']
        if got!=expected:raise RuntimeError('Authoritative input hash mismatch '+key+' '+got)
    for path,record in input_table.items():
        record['sha256_after']=digest(Path(path));record['unchanged']=record['sha256_before']==record['sha256_after']
        if not record['unchanged']:raise RuntimeError('Read input changed during audit '+path)
    inventory['input_bindings']=list(input_table.values())
    inventory['original_inputs_unchanged']=all(x['unchanged'] for x in input_table.values())
    out=json.dumps(inventory,ensure_ascii=False,indent=1)+'\n'
    if len(out.encode())>1000000:raise RuntimeError('inventory exceeds 1MB')
    (OWN/'experience_inventory.json').write_text(out)
    (OWN/'INPUT_HASHES.sha256').write_text(''.join(v['sha256_before']+'  '+k+'\n' for k,v in sorted(input_table.items())))
    print(json.dumps({'stages':inventory['stage_summaries'],'dedup':inventory['deduplication'],'r19_event_lineage':inventory['r19_event_lineage'],'inventory_bytes':len(out.encode()),'input_files':len(input_table),'all_inputs_unchanged':inventory['original_inputs_unchanged']},ensure_ascii=False,indent=2))
