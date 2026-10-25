"""Pure-stdlib SI-P0 evidence inspection; never imports project code.

This emits audit metadata/indexes, never prompts/targets or training JSONL.
"""
import collections
import csv
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True

OWN = Path(__file__).resolve().parent
PROJECT = Path('/home/lizening/Alfworld-Self-Improvement-Project')
FROZEN = Path('/home/lizening/wt-r19-g4-consumer-contract-repair')
RUNTIME = PROJECT / 'artifacts/runtime'
R19 = Path('/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z')

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def outline(value, depth=0):
    if depth >= 3:
        if isinstance(value, (list, dict)):
            return {'type': type(value).__name__, 'length': len(value)}
        return {'type': type(value).__name__}
    if isinstance(value, dict):
        return {key: outline(item, depth + 1) for key, item in value.items()}
    if isinstance(value, list):
        return {'length': len(value), 'first': outline(value[0], depth + 1) if value else None}
    if isinstance(value, (bool, int, float)) or value is None:
        return value
    return {'type': 'str', 'chars': len(value), 'value': value if depth < 2 and len(value) < 180 else None}

STAGES = {
    'SPRINT2C': RUNTIME / 'corpus/sprint2c-paired-20260820T143604Z/pairs.jsonl',
    'R4': RUNTIME / 'validation/sft-recovery-feasibility-r4-20260908T080000Z/pairs.jsonl',
    'R9_CONTINUE': RUNTIME / 'validation/persistent-recovery-replay-continue-r9-20260909T033000Z/continue_branches.jsonl',
    'R10_OSR': RUNTIME / 'validation/persistent-recovery-osr-control-r10-20260909T000000Z/osr_branches.jsonl',
    'R11_PBR': RUNTIME / 'validation/persistent-recovery-pbr-comparison-r11-20260909T000000Z/pbr_branches.jsonl',
    'R14_SOURCE': RUNTIME / 'validation/progress-aware-recovery-r14-20260910T000000Z/raw_trajectories.jsonl',
    'R15_CONTINUE': RUNTIME / 'validation/progress-aware-recovery-r15-b-20260910T000000Z/continue_ledger.jsonl',
    'R16_OSR': RUNTIME / 'validation/progress-aware-recovery-r16-osr-20260910T000000Z/osr_ledger.jsonl',
    'R17_PAR': RUNTIME / 'validation/progress-aware-recovery-r17-par-20260911T000000Z/par_ledger.jsonl',
    'R18_C1': RUNTIME / 'validation/progress-aware-r18-c1-20260911T000000Z/fact_text_branches.jsonl',
    'R18_C2': RUNTIME / 'validation/progress-aware-r18-c2-formal-aa9fa3c34520941e/card_v2_branches.jsonl',
    'R19_BRANCHES': R19 / 'branches.jsonl',
    'R19_SOURCE': R19 / 'source_trajectories.jsonl',
}

def probe():
    output = {}
    for stage, path in STAGES.items():
        record = {'path': str(path), 'exists': path.is_file()}
        if path.is_file():
            record['bytes'] = path.stat().st_size
            with path.open() as stream:
                row = next((json.loads(line) for line in stream if line.strip()), None)
            record['first_row_schema'] = outline(row)
        output[stage] = record
    (OWN / 'schema_probe.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))

def compact():
    for stage, path in STAGES.items():
        with path.open() as stream:
            row = next(json.loads(line) for line in stream if line.strip())
        print(stage, path.stat().st_size)
        for key, val in row.items():
            if isinstance(val, dict):
                print(' ', key, 'DICT', list(val))
                for k, v in val.items():
                    if isinstance(v, dict):
                        print('   ', k, 'DICT', list(v))
                    elif isinstance(v, list) and v and isinstance(v[0], dict):
                        print('   ', k, 'LIST', len(v), list(v[0]))
            elif isinstance(val, list):
                print(' ', key, 'LIST', len(val), list(val[0]) if val and isinstance(val[0], dict) else '')
            elif isinstance(val, str):
                print(' ', key, val if len(val)<160 else '<long text>')
            else:
                print(' ', key, val)


STAGES.update({
 'SPRINT_SOURCE': RUNTIME/'corpus/sprint2c-h4-pool-20260820T124651Z/trajectory.jsonl',
 'R3_CONTINUE': RUNTIME/'validation/sft-recovery-replay-continue-r3-20260908T055308Z/continue_branches.jsonl',
 'R1_SOURCE': RUNTIME/'validation/sft-recovery-source-pool-r1-20260908T042933Z/trajectories.jsonl',
 'R7_SOURCE': RUNTIME/'validation/persistent-recovery-source-pool-r7-20260909T000000Z/trajectories.jsonl',
})
META = {
 'SPRINT_MANIFEST':STAGES['SPRINT2C'].parent/'run_manifest.json',
 'SPRINT_SOURCE_MANIFEST':STAGES['SPRINT_SOURCE'].parent/'run_manifest.json',
 'R4_MANIFEST':STAGES['R4'].parent/'run_manifest.json',
 'R1_MANIFEST':STAGES['R1_SOURCE'].parent/'run_manifest.json',
 'R7_MANIFEST':STAGES['R7_SOURCE'].parent/'run_manifest.json',
 'R10_MANIFEST':STAGES['R10_OSR'].parent/'run_manifest.json',
 'R11_MANIFEST':STAGES['R11_PBR'].parent/'run_manifest.json',
 'R14_MANIFEST':STAGES['R14_SOURCE'].parent/'run_manifest.json',
 'R16_MANIFEST':STAGES['R16_OSR'].parent/'run_manifest.json',
 'R17_MANIFEST':STAGES['R17_PAR'].parent/'run_manifest.json',
 'R18_C1_MANIFEST':STAGES['R18_C1'].parent/'run_manifest.json',
 'R18_C2_MANIFEST':STAGES['R18_C2'].parent/'run_manifest.json',
 'R19_RUNTIME':R19/'runtime_manifest.json',
 'R19_EXECUTION':R19/'execution_manifest.json',
 'SPRINT_PREFIX':FROZEN/'configs/corpus/sprint2c_paired_prefix_manifest.json',
 'R4_PREFIX':FROZEN/'reports/sft_recovery_prefix_manifest.json',
 'R12_PREFIX':FROZEN/'reports/persistent_recovery_prefix_manifest.json',
 'R15_PREFIX':FROZEN/'reports/progress_aware_r15_prefix_manifest.json',
 'SFT_ACCEPTED_IDENTITIES':FROZEN/'configs/sft/sft_accepted_task_splits.json',
 'PROGRESS_EXCLUSIONS':FROZEN/'configs/recovery/progress_aware_source_exclusions.json',
}

def identities(obj, prefix='', depth=0):
    out={}
    if isinstance(obj,dict):
        for k,v in obj.items():
            key=prefix+'.'+k if prefix else k
            if isinstance(v,(dict,list)):
                if depth<5 and not isinstance(v,list): out.update(identities(v,key,depth+1))
            elif any(t in k.lower() for t in ['model','adapter','revision','horizon','max_steps','max_new_tokens','thinking','decoding','sampling','condition','pipeline','operator']):
                out[key]=v
    return out

def metadata():
    result={}
    for label,path in META.items():
        if not path.is_file():
            result[label]={'missing':str(path)};continue
        obj=json.loads(path.read_text())
        result[label]={'path':str(path),'bytes':path.stat().st_size,'sha256':digest(path),'keys':list(obj) if isinstance(obj,dict) else ['list',len(obj)],'identity_fields':identities(obj)}
        if 'PREFIX' in label or 'IDENTITIES' in label or 'EXCLUSIONS' in label:
            result[label]['schema']=outline(obj)
    (OWN/'metadata_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    for label,val in result.items():
        print(label,json.dumps({k:v for k,v in val.items() if k!='schema'},ensure_ascii=False))
    for label in ['SPRINT_SOURCE','R7_SOURCE','R3_CONTINUE']:
        p=STAGES[label]
        with p.open() as stream:r=next(json.loads(l) for l in stream if l.strip())
        print(label,'TOP',list(r))
        for k,v in r.items():
            if isinstance(v,dict):print(' ',k,list(v))
            if isinstance(v,list) and v and isinstance(v[0],dict):print(' ',k,len(v),list(v[0]))
    for stage in ['SPRINT2C','R4','R16_OSR','R18_C2','R19_SOURCE']:
        with STAGES[stage].open() as stream:r=next(json.loads(l) for l in stream if l.strip())
        if stage=='SPRINT2C': probes={'step':r['continue']['steps'][0],'stage2':r['recovery']['stage_two']}
        elif stage=='R4': probes={'stage2gen':r['raw_generations']['recovery']['stage_two'],'continuation':r['raw_generations']['sft_continuation_steps'][0]}
        elif stage=='R16_OSR': probes={'stage2gen':r['recovery_full']['stage_two']['generation'],'sftstep':r['continuation_full']['steps'][0]}
        elif stage=='R18_C2': probes={'sftstep':r['continuation']['steps'][0]}
        else:probes={'step':r['steps'][0]}
        for k,v in probes.items():
            print(stage,k,'DETAIL',json.dumps(outline(v),ensure_ascii=False))
    eventfile=R19/'execution_events.jsonl'
    types=collections.Counter();samples={}
    with eventfile.open() as stream:
        for line in stream:
            if not line.strip():continue
            r=json.loads(line);t=r.get('kind') or r.get('event_type') or r.get('type');types[t]+=1
            if t not in samples and len(samples)<30:samples[t]=outline(r)
    (OWN/'r19_event_schema.json').write_text(json.dumps({'counts':dict(types),'samples':samples},indent=2)+'\n')
    print('R19_EVENTS',dict(types),'sample file r19_event_schema.json')

def detail():
    for label in ['SPRINT_PREFIX','R4_PREFIX','R12_PREFIX','R15_PREFIX','SFT_ACCEPTED_IDENTITIES']:
        obj=json.loads(META[label].read_text())
        if 'prefixes' in obj:
            print(label,json.dumps(outline(obj['prefixes'][0]),ensure_ascii=False))
        else:
            print(label,json.dumps(outline(obj['pools']),ensure_ascii=False))
    for stage in ['R19_BRANCHES','R19_SOURCE']:
        with STAGES[stage].open() as stream:
            r=next(json.loads(l) for l in stream if l.strip() and ('eligible_primary' not in l or json.loads(l).get('eligible_primary')))
        print(stage,json.dumps(outline(r),ensure_ascii=False))
    c=collections.Counter();samps={}
    with (R19/'execution_events.jsonl').open() as stream:
        for line in stream:
            if not line.strip():continue
            r=json.loads(line);k=r['kind'];c[k]+=1
            if k not in samps:
                samps[k]={'identity':r.get('identity'),'payload_schema':outline(r.get('payload',{}))}
    (OWN/'r19_event_kind_probe.json').write_text(json.dumps({'counts':dict(c),'samples':samps},indent=2)+'\n')
    print('EVENT_COUNTS',dict(c))
    for k,v in samps.items():
        if k in ['model_generation_completed','source_episode_completed','k_arm_completed','environment_operation_completed','recovery_step_completed']:
            print('EVENT_SCHEMA',k,json.dumps(v,ensure_ascii=False))

def summary():
    inv=json.loads((OWN/'experience_inventory.json').read_text())
    for stage,row in inv['stage_summaries'].items():
        print(stage,json.dumps({k:row[k] for k in ['rows','canonical_tasks','episode_identity_keys','continue_successes','treatment_successes','labels','actual_rescue_prefix_ids','harm_prefix_ids','observed_source_successes','ineligible_attempts','eligible','observed_arm_records','derived_alias_records'] if k in row},ensure_ascii=False))
    for key in ['deduplication','r19_event_lineage','metadata_only_expert_split_overlap','old_failed_G3','campaign_cost_boundary']:
        print(key,json.dumps(inv[key],ensure_ascii=False))
    print('K_LABELS',json.dumps(inv['stage_summaries']['R19_BRANCHES']['labels_vs_continue_in_eligible'],ensure_ascii=False))
    print('K2_RESCUES',json.dumps(inv['stage_summaries']['R19_BRANCHES']['actual_K2_rescues'],ensure_ascii=False))
    print('ORACLE_OVER_K2',json.dumps(inv['stage_summaries']['R19_BRANCHES']['oracle_over_K2_cases'],ensure_ascii=False))
    print('SOURCE_OVERLAP',json.dumps([x for x in inv['canonical_identity_overlap_nonzero'] if ('SOURCE' in x['stage_a'] and 'SOURCE' in x['stage_b']) or ('R19' in x['stage_b'] and 'SOURCE' not in x['stage_a'])],ensure_ascii=False))
    print('OWN_BYTES',(OWN/'experience_inventory.json').stat().st_size)
    obj=json.loads((OWN/'r19_event_kind_probe.json').read_text())
    print('GEN_SAMPLE',json.dumps(obj['samples']['generation_completed'],ensure_ascii=False))

def contracts():
    seen=set()
    with (R19/'execution_events.jsonl').open() as stream:
        for line in stream:
            r=json.loads(line)
            if r['kind']!='generation_completed':continue
            comp=r.get('identity',{}).get('component')
            if comp in seen:continue
            seen.add(comp)
            print('GENERATION_COMPONENT',comp,json.dumps({'identity':r['identity'],'payload':outline(r['payload'])},ensure_ascii=False))
    inv=json.loads((OWN/'experience_inventory.json').read_text())
    for key in ['source_manifest_hash_comparisons']:
        print(key,json.dumps(inv[key]))
    print('INPUT_BINDINGS',len(inv['input_bindings']),all(r['unchanged'] for r in inv['input_bindings']))
    print('SINGLE_ACTION_RESCUES')
    for x in inv['actual_rescue_index_historical_treatments']:
        if x['stage'] in ['R4','R10_OSR','R16_OSR']:
            print(json.dumps({k:x.get(k) for k in ['stage','prefix_id','canonical_task','family','decision_index','stage1_valid_recorded','stage2_id_map_bound','replay_recorded_exact']}))
    for n,line in enumerate(STAGES['R19_BRANCHES'].read_text().splitlines(),1):
        r=json.loads(line)
        if r['prefix_id'] in inv['stage_summaries']['R19_BRANCHES']['rescue_prefix_ids_by_K']['2']:
            print('K2_RESCUE_REFS',r['prefix_id'],json.dumps(r['k_results']['2']['evidence_refs']))

if __name__ == '__main__':
    mode=sys.argv[1:]
    if mode==['probe']:probe()
    elif mode==['compact']:compact()
    elif mode==['metadata']:metadata()
    elif mode==['detail']:detail()
    elif mode==['summary']:summary()
    elif mode==['contracts']:contracts()
    elif mode==['finalize']:
        from finalization_functions import finalize
        finalize(globals())
    elif mode==['seal']:
        from finalization_functions import seal
        seal(globals())
    elif mode==['documents']:
        from deliverable_functions import write_deliverables
        write_deliverables(globals())
    elif mode==['audit']:
        from inventory_functions import run_audit
        run_audit(globals())
    else:raise SystemExit('supported modes: probe, compact, metadata, detail, audit, summary, contracts, documents, finalize, seal')
