import pathlib,subprocess,hashlib,ast,json
p=pathlib.Path(pathlib.Path('/tmp/r19-g4-independent-review-path.txt').read_text().strip());root=pathlib.Path('/tmp/r19-g4-independent-review-85cbb923');base='2da980f631badc25086d12db60d128ff507d3ae6';cand='85cbb92395e5e2420c2adeb1fa0634653e742910';dev=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-23T035448Z__CODEX__r19-g4-c01-c02__implementation')
def git(*a):return subprocess.check_output(['git','-C',str(root),*a])
def old(f):return git('show',base+':'+f).decode()
def sha(b):return hashlib.sha256(b).hexdigest()
def methods(t):return {n.name:n for n in ast.parse(t).body if isinstance(n,ast.FunctionDef)}
f='scripts/analyze_r19_recovery_duration.py';o=old(f);n=(root/f).read_text();a=methods(o);b=methods(n);changed={k for k in a if ast.dump(a[k])!=ast.dump(b[k])};added=set(b)-set(a);assert changed=={'validate_live_execution_provenance','validate_live_exit_receipt'};assert added=={'_validate_local_inference_runtime','_supervisor_option','_read_supervisor_object','_validate_supervisor_launch_context'}
def remaining(t,allowed):return [ast.dump(node) for node in ast.parse(t).body if not(isinstance(node,ast.FunctionDef) and node.name in allowed)]
assert remaining(o,changed)==remaining(n,changed|added)
files=git('diff','--name-only',base,cand).decode().splitlines();assert set(files)=={'scripts/analyze_r19_recovery_duration.py','tests/test_r19_g3_authorization.py','tests/test_r19_g4_consumer_contracts.py','tests/test_r19_recovery_duration.py'}
auth=json.loads(old('configs/experiments/r19_b1_g3_authorization_v1.json'));amend=json.loads(old('configs/experiments/r19_b1_g3_source_contract_repair_amendment_v1.json'));expected=auth['scientific_execution_fingerprints'].copy();expected.update({k:v['new'] for k,v in amend['changed_method_fingerprints'].items()})
def hspan(text,obj):
 nodes=ast.parse(text).body
 for key in obj.split('.'):
  found=[x for x in nodes if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and x.name==key];assert len(found)==1;node=found[0];nodes=node.body
 return sha(ast.get_source_segment(text,node).encode())
for key,h in expected.items():
 path,obj=key.split('::');assert hspan(old(path),obj)==h
 if not key.endswith('::validate_live_exit_receipt'):assert hspan((root/path).read_text(),obj)==h
assert sha((dev/'HANDOFF.json').read_bytes())=='92c49f2d3fe4541563662b71a8187809ebf1e15fbb72a9729e6d29e0812797da';assert sha((dev/'RECORD.md').read_bytes())=='ed561d5c5654ab107261990e69debb6f72d185e07e203f1a1c55255039c92d2b'
freeze=json.loads((dev/'evidence/source_freeze.json').read_text());hashes={k:{'old':hspan(o,k) if k in a else None,'new':hspan(n,k)} for k in sorted(changed|added)};assert hashes==freeze['changed_production_methods'];delta=git('diff',base,cand);assert sha(delta)==freeze['diff_sha256']==sha((dev/'evidence/source_delta.patch').read_bytes());(p/'evidence/complete_reviewed_delta.patch').write_bytes(delta)
pub=json.loads((dev/'publication_manifest.json').read_text());inventory=json.loads((dev/'evidence_inventory.json').read_text());verified={}
for name in pub['files']:
 path=dev/name;h=sha(path.read_bytes())
 if name in inventory:assert h==inventory[name]['sha256'] and path.stat().st_size==inventory[name]['bytes']
 assert path.stat().st_size<10*1024**2;verified[name]=h
result={'scope':'STATIC_EXACT_SHA_DELTA_REVIEW_NOT_FORMAL_G4','source_sha':cand,'parent_executed_G3_sha':base,'changed_files':files,'two_existing_methods_changed':sorted(changed),'four_helpers_added':sorted(added),'all_other_analyzer_AST_including_imports_constants_control_flow_identical':True,'no_runtime_supervisor_protocol_cost_or_statistics_change':True,'historical_fingerprints_verified':len(expected),'current_unchanged_fingerprints_verified':39,'method_sha256':hashes,'complete_delta_sha256':sha(delta),'developer_selected_publication_files_verified':verified,'developer_publication_manifest_sha256':sha((dev/'publication_manifest.json').read_bytes()),'production_and_test_code_mutated_by_reviewer':False}
(p/'evidence/static_exact_sha_review.json').write_text(json.dumps(result,indent=2)+'\n');print('STATIC_SCOPE_AND_HASHES_PASS',len(verified))
