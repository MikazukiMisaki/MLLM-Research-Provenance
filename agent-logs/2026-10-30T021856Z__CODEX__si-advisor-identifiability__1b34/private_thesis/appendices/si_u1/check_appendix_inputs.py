#!/usr/bin/env python3
"""Check bound inputs and local archive bytes without model or project-code imports."""
from pathlib import Path
import hashlib,json,tarfile,io
N=Path('/home/lizening/research-notes/agent-logs'); D=N/'2026-10-29T164000Z__LUNA__si-u1-evaluation-offline-audit__c2356'; runtime=N/'2026-10-29T144100Z__SOL__si-u1-stage2-plan__2060cc8/stage2/runtime.json';auth=Path('/home/lizening/wt-si-self-imitation-evaluator/configs/local/si_pilot82_evaluation_authorization_c2356bbda2b44159a333e7c9d24fc2d4.json'); inv=D/'RAW_EVIDENCE_INVENTORY_PRIVATE.json'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
d=json.loads(runtime.read_bytes());a=json.loads(auth.read_bytes());assert sha(runtime)==a['runtime_spec']['sha256']=='e307fa192371b5bf6c2b92dff6f543868e723eda12c5c5a8893ce01dc6aeecd5'
def check(records):
 n=0
 for item in records:
  p=Path(item['path']);assert p.is_file() and sha(p)==item['sha256'];n+=1
 return n
game=check([x[k] for x in d['games'] for k in ('game','traj_data')]);assert game==164
lineage=check(list(d['isolation_inputs'].values())+[v for arm in 'BC' for v in d['adapters'][arm]['training_evidence'].values()]);assert lineage==12
packages=check(list(d['packages'].values()));assert packages==8
manifest=(D/'RAW_PART_HASHES.sha256').read_text().splitlines();parts=[];joined=bytearray()
for row in manifest:
 want,name=row.split(None,1);p=D/name.strip();data=p.read_bytes();assert hashlib.sha256(data).hexdigest()==want;parts.append(p);joined.extend(data)
assert len(parts)==12 and len(joined)==46536262 and hashlib.sha256(joined).hexdigest()=='71eb69cf4422bdbefd19485cc4fc5b7d4618ce974013a5882f1334784e8779d3'
inventory=json.loads(inv.read_bytes());assert inventory['archive_sha256']=='71eb69cf4422bdbefd19485cc4fc5b7d4618ce974013a5882f1334784e8779d3'
seen={}
with tarfile.open(fileobj=io.BytesIO(joined),mode='r:gz') as t:
 for member in t:
  if not member.isfile():continue
  assert member.name in inventory['members'] and member.name not in seen
  stream=t.extractfile(member);assert stream is not None;h=hashlib.sha256();n=0
  for chunk in iter(lambda:stream.read(1048576),b''):h.update(chunk);n+=len(chunk)
  exp=inventory['members'][member.name];assert n==exp['bytes'] and h.hexdigest()==exp['sha256'];seen[member.name]=True
assert len(seen)==32 and set(seen)==set(inventory['members'])
L=N/'2026-10-29T225000Z__LUNA__si-u1-extraction-publication__062a';first=json.loads((L/'first_attempt/PROCESS_RECEIPT.json').read_bytes());second=json.loads((L/'second_attempt/PROCESS_RECEIPT.json').read_bytes());assert first['authentic_returncode']==1 and not first['analysis_exists'];assert second['authentic_returncode']==0 and second['analysis_sha256']=='4a3ea016d4c06022980482ac9dbc58155a68bbe20fbc723a68ce49c7c345ea9b'
assert sha(runtime)=='e307fa192371b5bf6c2b92dff6f543868e723eda12c5c5a8893ce01dc6aeecd5'
out={'status':'PASS_LOCAL_BOUND_BYTES_AND_ARCHIVE_CONTENT_ONLY','runtime_sha256':sha(runtime),'evaluation_game_and_trajectory_files_matched':game,'isolation_and_training_evidence_files_matched':lineage,'specified_package_entry_files_matched':packages,'archive_part_count':len(parts),'archive_total_bytes':len(joined),'reassembled_archive_sha256':hashlib.sha256(joined).hexdigest(),'archive_members_rehashed_against_inventory':len(seen),'first_extraction_recorded_returncode':first['authentic_returncode'],'second_extraction_recorded_returncode':second['authentic_returncode'],'second_analysis_sha256':second['analysis_sha256'],'limits':['Local hash audit only; full base and adapter trees rely on the earlier independent byte audit and are not rehashed here.','Archive member hashes are checked against a saved inventory; this step does not rerun scientific processing or prove independent external execution.','No remote full-content checks; model/data absent from archive despite local hash-matched inputs.','Does not output task IDs, prompts, outcomes or archive member names.']}
Path(__file__).with_name('APPENDIX_LOCAL_CHECK.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
