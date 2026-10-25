from pathlib import Path
import datetime,hashlib,json,subprocess
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts');SHA='a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3'
for name in ['PUBLICATION_MANIFEST.json','FILE_HASHES.sha256','FINAL_READ_ONLY_RECEIPTS.json','INPUT_BINDINGS_FINAL_CHECK.json']:assert not (OWN/name).exists(),name
receipts=[]
for args in [['git','rev-parse','HEAD'],['git','status','--porcelain=v1'],['git','rev-parse','origin/codex/si-p3-engineering-contracts'],['git','diff','--check','85cbb92395e5e2420c2adeb1fa0634653e742910',SHA]]:
 p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True);receipts.append({'argv':args,'cwd':str(ROOT),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0
assert receipts[0]['stdout'].strip()==receipts[2]['stdout'].strip()==SHA and not receipts[1]['stdout']
(OWN/'FINAL_READ_ONLY_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
inputs=json.loads((OWN/'INPUT_AND_FROZEN_SOURCE_BINDINGS.json').read_text())['bindings'];checks=[]
for item in inputs:
 p=Path(item['path']);observed=hashlib.sha256(p.read_bytes()).hexdigest();expected=item.get('current_sha256',item.get('sha256'))
 checks.append({'path':str(p),'before_sha256':expected,'final_sha256':observed,'same':observed==expected})
 assert observed==expected,p
for name,info in json.loads((OWN/'NEW_METHODS_AND_FILES.json').read_text())['only_added_files'].items():
 assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==info['sha256']
(OWN/'INPUT_BINDINGS_FINAL_CHECK.json').write_text(json.dumps({'all_same':True,'source_SHA':SHA,'inputs':checks},indent=2)+'\n')
# Include compact final receipts/probes/code writers and copied tiny software outputs.
# Preserve complete synthetic raw trees locally and bind their hashes in the full inventory.
raw_dirs={'synthetic_integration_v1','synthetic_integration_v2','synthetic_integration_v3','synthetic_integration_frozen'}
compact_final={'integrity.json','quality.json','adoption.json','exposure.json','software_invocation_context.json'}
all_files=sorted(p for p in OWN.rglob('*') if p.is_file() and not p.is_symlink())
selected=[];local=[]
for p in all_files:
 rel=p.relative_to(OWN)
 if rel.parts[0] in raw_dirs:
  chosen=rel.parts[0]=='synthetic_integration_frozen' and p.name in compact_final
 else:chosen=True
 item={'relative_path':str(rel),'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 (selected if chosen else local).append(item)
manifest={'schema':'SI_E1_PUBLICATION_SELECTION_V1','creation_status':'LOCAL_ONLY_COORDINATOR_PUBLICATION_PENDING','source_commit_SHA':SHA,'science_branch_pushed_non_force':True,'provenance_not_committed_or_pushed':True,'shared_INDEX_root_inventory_untouched':True,'selected_compact_files':selected,'raw_software_files_retained_local_only':local,'selected_files_do_not_include_this_manifest_or_FILE_HASHES_to_avoid_self_reference':True,'auxiliary_manifest_paths':[str(OWN/'PUBLICATION_MANIFEST.json'),str(OWN/'FILE_HASHES.sha256')],'independent_acceptance':'NOT_ISSUED_BY_DEVELOPER','scientific_execution':'NOT_GRANTED','sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(OWN/'PUBLICATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
all_files=sorted(p for p in OWN.rglob('*') if p.is_file() and not p.is_symlink() and p.name!='FILE_HASHES.sha256')
rows=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(OWN)) for p in all_files]
(OWN/'FILE_HASHES.sha256').write_text('\n'.join(rows)+'\n')
# Read-only recomputation after final write. No more own files are mutated afterward.
for row in rows:
 expected,name=row.split('  ',1);assert hashlib.sha256((OWN/name).read_bytes()).hexdigest()==expected
out={'frozen_source_SHA':SHA,'local_origin_live_remote_verified':True,'clean':True,'selected_compact_files':len(selected),'raw_software_files_local':len(local),'total_hashed_files_excluding_hash_manifest':len(rows),'HANDOFF':{'path':str(OWN/'HANDOFF.md'),'sha256':hashlib.sha256((OWN/'HANDOFF.md').read_bytes()).hexdigest()},'PUBLICATION_MANIFEST':{'path':str(OWN/'PUBLICATION_MANIFEST.json'),'sha256':hashlib.sha256((OWN/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest()},'FILE_HASHES':{'path':str(OWN/'FILE_HASHES.sha256'),'sha256':hashlib.sha256((OWN/'FILE_HASHES.sha256').read_bytes()).hexdigest()},'all_input_bindings_unchanged':True,'test_result':'focused343; full800+3historicalfail+77historicalerrors; same80IDs; noNEW','real_scientific_increment':0,'independent_acceptance':'NOT_ISSUED','next':'Sol independent exact-SHA review'}
print(json.dumps(out,indent=2))
