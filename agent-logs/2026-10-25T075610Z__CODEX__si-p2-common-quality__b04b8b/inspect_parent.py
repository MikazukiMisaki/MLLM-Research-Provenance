from audit_io import *
from collections import Counter,defaultdict
m=authority();pr=parent_rows(m)
print('start_utc',datetime.datetime.now(datetime.timezone.utc).isoformat())
for st in SOURCES:
 print('FILE',st,SOURCES[st],register(SOURCES[st]).stat().st_size)
rows_out=[];shown=set()
for c,r in pr:
 st=c['stage']
 if st=='R4':
  gen=r.get('raw_generations',{}).get('recovery',{}).get('stage_two') or {};rec=r.get('recover',{});p=gen.get('parsed') or {};g=gen.get('generation') or {};s1=rec.get('stage_one',{});suf=rec.get('continuation') or {};label=rec.get('success');exe=rec.get('recovery_action_executed');tr=rec.get('recovery_transition');ct=r.get('continue',{}).get('success')
 elif st in ('R10_OSR','R16_OSR'):
  gen=r.get('recovery_full',{}).get('stage_two') or {};p=gen.get('parsed') or {};g=gen.get('generation') or {};s1=(r.get('recovery_full',{}).get('stage_one') or {}).get('parsed',{});suf=r.get('continuation_full') or {};label=r.get('r_osr');exe=r.get('recovery_action_executed');tr=r.get('recovery_transition');ct=r.get('r_continue',r.get('continue_success'))
 else:
  arm=r['k_results']['1'] or {};p={};g={};s1={};suf=arm;label=arm.get('success');exe=bool(arm.get('evidence_refs',{}).get('recovery_transition_event_ids'));tr=None;ct=r.get('continue_success')
 row={'case':c['case_id'],'continue':ct,'recover':label,'stage1':s1.get('status'),'stage2':p.get('status'),'generation_complete':g.get('output_complete'),'cap':g.get('token_cap_reached'),'executed':exe,'suffix_steps':len(suf.get('steps',[])),'stop':suf.get('termination_reason',suf.get('stop_reason')),'transition_keys':list(tr) if isinstance(tr,dict) else None}
 rows_out.append(row)
 key=(st,s1.get('status'),p.get('status'),exe,label, bool(suf.get('steps')))
 if key not in shown:
  shown.add(key);print('EXAMPLE',json.dumps(row));print('ROWKEYS',st,list(r));print('sufkeys',list(suf));print('stage1',str(s1)[:200]);print('parsed',str({k:v for k,v in p.items() if k not in ('id_to_command','valid_actions','prompt')})[:600]);print('rec_schema',json.dumps({k:list(v) if isinstance(v,dict) else type(v).__name__ for k,v in (r.get('recover') or r.get('recovery_full') or r['k_results']['1'] or {}).items()}))
print('COUNTS',json.dumps({st:dict(Counter(str((x['stage1'],x['stage2'],x['executed'],x['recover'],x['stop'])) for x in rows_out if x['case'].startswith(st+':'))) for st in SOURCES},ensure_ascii=False))
output('parent_shape_inspection.json',rows_out)
# Read only top-level runtime identity; no weights/tokenizer loaded.
for st in ['R4','R10_OSR','R16_OSR']:
 p=next(Path(c['source_path']).parent/'run_manifest.json' for c,r in pr if c['stage']==st)
 x=readjson(p);print('MANIFEST',st, json.dumps({k:v for k,v in x.items() if any(t in k for t in ['revision','model','adapter','isolation','horizon'])},ensure_ascii=False))
finish_bindings('inspection_input_bindings.json')
