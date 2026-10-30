from pathlib import Path
from collections import Counter
import hashlib,json
p=Path('/home/lizening/research-notes/agent-logs/2026-10-29T145200Z__LUNA__si-u1-production-preflight-proposal__853/run_parent/evaluation_c2356bbda2b44159a333e7c9d24fc2d4/evaluation/events.jsonl')
expected='6146bb79faeb572c3674ff9ba907fac4be25eff4c2bd161a3d7cf3156d81c96e'
h=hashlib.sha256();counts=Counter(); violations=Counter(); min_tokens=None;max_tokens=None
with p.open('rb') as f:
 for raw in f:
  h.update(raw);row=json.loads(raw);data=row.get('payload',{});ident=data.get('identity',{})
  if row.get('kind')!='unit_completed' or ident.get('op')!='generation':continue
  d=data['data'];arm=ident.get('arm');counts[arm]+=1
  for key,value in [('do_sample',False),('thinking',False),('max_new_tokens',16),('adapter_mode',arm)]:
   if type(d.get(key)) is not type(value) or d.get(key)!=value: violations[key]+=1
  n=d.get('generated_tokens')
  if type(n) is not int or not 0<=n<=16:violations['generated_tokens_range']+=1
  else:min_tokens=n if min_tokens is None else min(min_tokens,n);max_tokens=n if max_tokens is None else max(max_tokens,n)
sha=h.hexdigest();assert sha==expected,(sha,expected)
out={'ledger_sha256':sha,'expected_ledger_sha256':expected,'completed_generations_by_arm':dict(sorted(counts.items())),'total_completed_generations':sum(counts.values()),'violations':dict(violations),'generated_tokens_min':min_tokens,'generated_tokens_max':max_tokens,'scope':'Only event metadata/counts; no prompts, output strings, task identities or outcomes emitted; no model, CUDA or environment calls. Ledger hash matches previously independently accepted analysis. This checks recorded events, not unrecorded launches or GPU execution.','source_file':'approved SI-U1 fixed 82-task evaluation event ledger'}
Path('DECODE_METADATA.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k] for k in ('ledger_sha256','completed_generations_by_arm','total_completed_generations','violations','generated_tokens_min','generated_tokens_max')},sort_keys=True))
assert sum(counts.values())==5001 and not violations
