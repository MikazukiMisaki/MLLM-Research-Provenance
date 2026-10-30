"""Count already observed R19 outcomes from hash-bound frozen branch rows; no experiment."""
import hashlib,json
from pathlib import Path
p=Path('/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/branches.jsonl')
raw=p.read_bytes(); sha=hashlib.sha256(raw).hexdigest();assert sha=='eff9b5e74d3d5daa928cb662dcc59fc3f434f66796b673679d40b374f3c8636f'
rows=[json.loads(s) for s in raw.splitlines()]; assert len(rows)==39
rows=[r for r in rows if r['eligible_primary'] is True];assert len(rows)==36
for r in rows:
 assert set(r['k_results'])==set('12345')
 assert r['continue_success'] in (0,1)
 assert all(r['k_results'][k]['success'] in (0,1) for k in '12345')
s=lambda r,k:bool(r['k_results'][str(k)]['success'])
totals={str(k):sum(s(r,k) for r in rows) for k in range(1,6)}
extra=[r for r in rows if not s(r,2) and any(s(r,k) for k in range(1,6))]
result={'branch_sha256':sha,'input_rows':39,'eligible_rows':len(rows),'k_success_totals':totals,'continue_success_total':sum(r['continue_success'] for r in rows),'oracle_over_k2':len(extra),'oracle_over_k2_with_continue_success':sum(r['continue_success'] for r in extra),'oracle_over_k2_successful_ks_per_case_anonymized':sorted([k for k in range(1,6) if s(r,k)] for r in extra),'oracle_any_k_success_total':sum(any(s(r,k) for k in range(1,6)) for r in rows),'k2_wins_over_continue':sum(s(r,2) and not r['continue_success'] for r in rows),'continue_wins_over_k2':sum(r['continue_success'] and not s(r,2) for r in rows),'input_unchanged_after':hashlib.sha256(p.read_bytes()).hexdigest()==sha,'scope':'raw persisted branch outcome fields; no G4/model/environment invocation and no private task identifiers emitted'}
assert result['input_unchanged_after'] and totals=={'1':29,'2':30,'3':28,'4':25,'5':24}
assert result['continue_success_total']==30 and result['oracle_any_k_success_total']==32 and result['oracle_over_k2']==result['oracle_over_k2_with_continue_success']==2
assert result['oracle_over_k2_successful_ks_per_case_anonymized']==[[1],[5]] and result['k2_wins_over_continue']==result['continue_wins_over_k2']==2
print(json.dumps(result,indent=2,sort_keys=True))
