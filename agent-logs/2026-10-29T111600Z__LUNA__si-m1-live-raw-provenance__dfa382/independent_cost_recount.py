"""Read-only stdlib count of immutable SI-M1 copied journal; not scientific validator."""
from collections import Counter
from pathlib import Path
import hashlib,json,math,sys
O=Path(__file__).resolve().parent;path=O/'raw/output/probe_events.jsonl';report=json.loads((O/'raw/output/probe_report.json').read_bytes());supervisor=json.loads((O/'raw/output/supervisor_exit.json').read_bytes());events=[];prev=None;last=-float('inf');complete_newline=False
with path.open('rb') as f:
 for line in f:
  complete_newline=line.endswith(b'\n');e=json.loads(line);payload={k:v for k,v in e.items() if k!='event_id'};raw=json.dumps(payload,ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False).encode();assert e['event_id']==hashlib.sha256(raw).hexdigest() and e['sequence']==len(events) and e['previous']==prev and math.isfinite(e['monotonic']) and e['monotonic']>=last;events.append(e);prev=e['event_id'];last=e['monotonic']
assert complete_newline and events[0]['kind']=='run_opened' and events[-1]['kind']=='run_closed'
started={};returned={};completed={};failed={};closed={};runtime=Counter()
for e in events:
 p=e['payload'];k=e['kind']
 if k=='unit_started':assert p['unit'] not in started;started[p['unit']]=p
 elif k=='unit_returned':assert p['unit'] in started and p['unit'] not in returned;returned[p['unit']]=p
 elif k=='unit_completed':assert p['unit'] in returned and p['unit'] not in completed and returned[p['unit']]['data']==p['data'];completed[p['unit']]=p
 elif k=='unit_failed':failed[p['unit']]=p
 elif k=='case_closed':assert p['case_id'] not in closed;closed[p['case_id']]=p
 elif k=='runtime_evidence':runtime[p['kind']]+=1
components=Counter(p['identity']['kind'] for p in completed.values());generations=sum(components[x] for x in ('stage_one','stage_two'));ops=sum(components[x] for x in ('reset','replay','teacher_step'));input_tokens=sum(len(started[u]['prepared']['input_ids']) for u,p in completed.items() if p['identity']['kind'] in ('stage_one','stage_two'));output_tokens=sum(p['data']['raw']['generated_tokens'] for p in completed.values() if p['identity']['kind'] in ('stage_one','stage_two'));actual={'generations':generations,'environment_operations':ops,'generated_tokens':output_tokens,'input_tokens':input_tokens};assert actual==report['physical']['completed'] and components==Counter(report['physical']['components']) and not failed and set(started)==set(completed) and len(closed)==5
for row in report['rows']:
 for key in ('Z_immediate','terminal_observed','P0_suffix','disposition'):assert closed[row['case_id']][key]==row[key]
assert supervisor['authentic_returncode']==0 and supervisor['execution_status']=='EXIT_RECORDED' and supervisor['cleanup_established'] and supervisor['within_time_cap']
r={'schema':'SI_M1_STDLIB_CHAIN_AND_COST_RECOUNT_V1','classification':'READ_ONLY_ACCOUNTING_NOT_FULL_SCIENTIFIC_AUDIT','event_count':len(events),'journal_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'chain_verified':True,'distinct_unit_starts':len(started),'completed_units':len(completed),'failed_units':len(failed),'open_units':len(set(started)-set(completed)),'runtime_generation_invocations':runtime['generation_invoked'],'runtime_generation_returns':runtime['generation_returned'],'components':dict(components),'physical':actual,'case_closures':len(closed),'report_accounting_and_closures_match':True,'device_hours':supervisor['allocated_device_hours'],'prior_generations':7101,'prior_environment_operations':10004,'cumulative_generations':7101+generations,'cumulative_environment_operations':10004+ops}
(O/'INDEPENDENT_COST_RECOUNT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
