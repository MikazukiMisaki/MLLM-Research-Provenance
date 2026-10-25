from pathlib import Path
import json,hashlib,subprocess,datetime
r=Path(__file__).resolve().parent;assert 'si-p3-controlled-experience-design' in str(r);s=json.loads((r/'START_STATE.json').read_text());sdir=Path(s['directories']['sol']);ldir=Path(s['directories']['luna'])
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
for d,names in [(sdir,['FILE_HASHES.sha256','FIVE_FAMILY_ADDENDUM_HASHES.sha256','INPUT_HASHES.sha256']),(ldir,['FILE_HASHES.sha256','ADDENDUM_HASHES.sha256'])]:
 for name in names:
  count=0
  for line in (d/name).read_text().splitlines():
   if not line.strip():continue
   sha,p=line.split(maxsplit=1);p=p.removeprefix('*');fp=Path(p) if Path(p).is_absolute() else d/p
   assert fp.is_file(),str(fp);assert h(fp)==sha,(str(fp),h(fp),sha);count+=1
  checks.append({'manifest':str(d/name),'sha256':h(d/name),'entries':count,'all_match':True})
knownmeta=json.loads((ldir/'metadata_audit.json').read_text())
for p,b in knownmeta['inputs_before'].items():assert h(Path(p))==b['sha256']
for p,b in knownmeta['inputs_after'].items():assert h(Path(p))==b['sha256'] and b['unchanged']
freeze=json.loads((sdir/'FROZEN_HANDOFF.json').read_text())
for b in freeze['artifacts']:assert h(Path(b['path']))==b['sha256']
# Verify only preserved historical raw hashes; no project analyzer or task payload processing.
old=json.loads((r/'existing_g3_raw_hash_drift_check.json').read_text())
for b in old['files']:assert h(Path(b['path']))==b['sha256']
# Assert adopted final partition and resource/recipe arithmetic, independently checked scripts were real rc0.
for receipt in ['independent_design_math.receipt.json','verify_luna_metadata_proposal.receipt.json','verify_adopted_design.receipt.json','fixed_cutoff_budget_math.receipt.json']:
 d=json.loads((r/receipt).read_text());assert d['actual_returncode']==0
state=[]
for path,expected,branch in [('/home/lizening/wt-codex-r18c2','e537f441010077123a307e9d50ea40cf8dad8547','agent/codex-r18c2'),('/home/lizening/wt-r19-g4-consumer-contract-repair','85cbb92395e5e2420c2adeb1fa0634653e742910','codex/r19-g4-consumer-contract-repair'),('/home/lizening/wt-r19-recovery-duration-v1','2da980f631badc25086d12db60d128ff507d3ae6','')]:
 commands=[]
 for args in [['git','rev-parse','--show-toplevel'],['git','branch','--show-current'],['git','rev-parse','HEAD'],['git','status','--porcelain','--untracked-files=no']]:
  cp=subprocess.run(args,cwd=path,capture_output=True,text=True);assert cp.returncode==0;commands.append({'argv':args,'actual_returncode':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
 assert commands[0]['stdout'].strip()==path;assert commands[1]['stdout'].strip()==branch;assert commands[2]['stdout'].strip()==expected;assert commands[3]['stdout'].strip()==''
 state.append({'path':path,'expected_sha':expected,'commands':commands})
remote=['git','ls-remote','origin','refs/heads/codex/r19-g4-consumer-contract-repair','refs/heads/codex/r19-source-contract-review-fixes'];cp=subprocess.run(remote,cwd='/home/lizening/wt-r19-g4-consumer-contract-repair',capture_output=True,text=True);assert cp.returncode==0
remotevals={v.split()[1]:v.split()[0] for v in cp.stdout.splitlines()};assert remotevals['refs/heads/codex/r19-g4-consumer-contract-repair']=='85cbb92395e5e2420c2adeb1fa0634653e742910';assert remotevals['refs/heads/codex/r19-source-contract-review-fixes']=='2da980f631badc25086d12db60d128ff507d3ae6'
out={'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'DELIVERY_BYTES_METADATA_ARITHMETIC_AND_SCIENTIFIC_REF_DRIFT_CHECKED','author_manifests':checks,'sol_frozen_handoff_artifact_matches':len(freeze['artifacts']),'luna_actual_before_after_input_bindings_match':len(knownmeta['inputs_before']),'old_G3_raw_hashes_match':len(old['files']),'source_states':state,'scientific_remote':{'argv':remote,'actual_returncode':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr},'scientific_calls':{'models':0,'environment':0,'tokenizer':0,'training':0,'project_validator':0,'pytest':0,'preflight':0,'G2_G3_G4':0},'exception':'Luna shortened input-path fields and manually transcribed stdout are rejected as raw/bindings; corrected actual metadata/tool receipts independently matched and preserved separately.'}
(r/'delivery_and_source_drift_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'manifest_entries':[x['entries'] for x in checks],'actual_inputs':len(knownmeta['inputs_before']),'source_head_checks':len(state),'science_calls':out['scientific_calls']},indent=2))
