from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
OWN=Path(__file__).resolve().parent;REPO=Path('/home/lizening/wt-si-p3-source-only-v2');SHA='d7a82acb510157ab7ba5439d790816c5c948439f';BASE='844cc4b78df1f83e29391ffd5ab861a2d0c0a3fd'
def read(p):return json.loads(Path(p).read_bytes())
def binding(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(name,value):
 with (OWN/name).open('x') as f:json.dump(value,f,indent=2);f.write('\n')
comparison=read(OWN/'SOFTWARE_COMPARISON_FINAL.json');remote=read(OWN/'REMOTE_EQUALITY.json');scope=read(OWN/'SOURCE_SCOPE_FINAL.json')
assert comparison['source_sha']==remote['source_sha']==scope['candidate_sha']==SHA and remote['live_remote_equals_clean_local_HEAD']
assert comparison['exact_historical80_ID_classification_phase_exception_types_equal'] and not comparison['new_problem_IDs']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()==SHA and not subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True)
for label in ('rt_final_compile','rt_final_diff_check','rt_final_path_credential_scan'):
 r=read(OWN/'receipts'/(label+'.json'));assert r['source_sha']==SHA and r['authentic_returncode']==r['expected_returncode'] and r['pre_status']==r['post_status']==''
initial=read(OWN/'INPUT_BINDINGS_FINALIZATION_INITIAL.json');rt=read(OWN/'INPUT_BINDINGS_RT_INITIAL.json');after=[binding(x['path']) for x in initial['files']];assert after==initial['files']==rt['files']
ruling=read(OWN/'RT_FIX_RULING_BINDING.json');assert binding(ruling['path'])['sha256']==ruling['sha256']
oldtree='/home/lizening/wt-si-e2-cuda-uuid-compat'
oldhead=subprocess.check_output(['git','rev-parse','HEAD'],cwd=oldtree,text=True).strip();oldstatus=subprocess.check_output(['git','status','--porcelain=v1'],cwd=oldtree,text=True);assert oldhead==BASE and oldstatus==''
write('INPUT_BINDINGS_AFTER.json',{'captured_utc':datetime.now(timezone.utc).isoformat(),'same_consumed_input_bytes_as_both_finalization_snapshots':True,'files':after,'RT_ruling':binding(ruling['path']),'original_frozen844_worktree_head':oldhead,'original_frozen844_worktree_status':oldstatus,'scientific_calls_added':0,'no_claim_of_rehashing_unconsumed_historical_raw_evidence':True})
for file in ('SYNTHETIC_EVIDENCE_RT_INDEX.json','RT_RELIABILITY_EVIDENCE_INDEX.json'):
 v=read(OWN/file)
 for row in v.get('published_compact_copies',v.get('copies',[])):assert binding(row['copy']['path'])==row['copy']
counts=comparison['candidate_counts'];ref=remote['ref']
handoff=f'''# SI-S01 frozen engineering handoff

FROZEN_DEVELOPER_DELIVERY_PENDING_ROOT_EXACT_SHA_REVIEW. No independent acceptance, runtime readiness or launch clearance is claimed.

Source `{SHA}`; branch `{ref}`; worktree {REPO}. Non-force publication and live remote equality: REMOTE_EQUALITY.json. Final delta adds16files; all543original tracked Git entries remain identical to exact844. The old844worktree is clean and unchanged.

## Implemented path

New si_s01 namespace: authenticated A96 metadata/plan -> separate static gate and one-launch clearance -> own supervisor/worker -> actual runtime ports -> frozen P0 prompt/parser -> collector/journal/unit registry/trajectories -> independent raw auditor -> source JSON/Markdown report. The real backend has actual artifact/module/PEFT/UUID/PID-owner/full token-tensor checks; it does not reuse the old four-call orchestration. Runtime ports are implemented but actual Qwen/P0/world execution is unverified.

Original metadata6ce8a32a... and actual five-field reservation rows bind the fixed families35/26/16/9/10, reset42/pool42/d5, original rank order and H50. Live has no hash override. Synthetic identities cannot enter --live. No real acquisition manifest/configuration was created and no new task payload was opened.

S5 is durable immediately after actual step5, before generation6/source close. Terminal/truncated/empty-map/early stops remain explicit. ValidS5 plus sixth parser failure remains E. NormalY0 is done&&reward>0; technical/budget/integrity incompletes stay NA and sealed priorY0 is retained. All96slots receive dispositions; YT is always NA with TEACHER_NOT_AUTHORIZED_SOURCE_ONLY. Only complete normal96source seal permits total/family E/F/S necessary upper bounds. NOT_FUTILE establishes no teacher/Q/adoption/learning success. Teacher/stage1/stage2/replay/independent suffix/train/eval hard-reject before external work.

Caps remain4800generations/4896reset+step/76800output/16Minput/8192perinput/4allocated-device-hours. Full reservations precede calls; failed/incomplete reservations persist. Load/construct/close have separate receipts and zero reset/step debit. Raw generation returns are saved before post-resource failure. Audit reconstructs raw unit/map/action/public-prompt/token/reference/cost evidence independently of collector summaries and binds live plan/run/caps/device/start/PID/UID/context to external authority.

Preflight-only is separate authority. Real live launch additionally requires a successful zero-science preflight receipt, authentic exit0 execution receipt and fresh independently hash-bound one-launch clearance tied to exact source/review/proposal/plan/env/argv/UID/UTC/output. No real preflight or clearance was created/executed by the developer. Software fixtures are explicitly synthetic.

## RT01/02/03 bounded correction

All in-flight9bc tests finished first and are preserved. Ruling46f2df17... authorized the five-file incremental correction in RT_incremental.patch. Every worker wait, including after SIGKILL, is bounded by remaining absolute allocation time; unknown exit stays null with identity/error/elapsed/survivors and incomplete cleanup. Atomic exclusive durable worker_start publication prevents partial final JSON without changing PID/UID/tick/parent/hash checks. Source report hours explicitly stop at collector_run_closed and are a stage lower bound; authentic supervisor_exit allocated_device_hours is final cost authority. Overlapping values must not be added. RT_AST_SCOPE_VERIFICATION.json proves all auditor statements before its final return are identical to9bc.

## Actual software evidence

Pinned /home/lizening/miniconda3/envs/alfworld-self-improve/bin/python. Focused83pass/exit0: receipts/rt_focused.json and rt_focused.xml. Full{counts['passed']}pass/{counts['failed']}fail/{counts['errors']}errors, authentic exit1: comparable_rt/full.receipt.json, full.reports.json and baseline.junit.xml. Exact80historical ID/classification/phase/exception-type keys match root's independent844baseline7f6c762e...; all953old passing IDs remain passed; all83new IDs pass. No new failure/error/skip. This is baseline-relative software verification, not a globally green suite or independent acceptance.

The byte-identical parameterized baseline runner, same explicit environment contract, Python-I and src/tests/tree order were used. Project module origins stay inside this worktree and unchanged before/after; CUDA remains uninitialized. Tiny CPU PEFT/model/tokenizer fixtures execute as software, not real Qwen/P0 training. Compile15newPythonfiles exit0; diffcheck exit0; targeted machine-path/credential-literal scan exit1 with no matches. Raw receipts retain genuine exits.

Nonempty production-function fixtures cover all96/five families, NOT_FUTILE/structuralNO_GO/family floors, S5+sixth parser failure, terminal/truncated/empty/early states, original P0 EOS-incomplete selection, exact4800/4896/76800caps, partialNA, continuous simulated time, and returned raw evidence on post-resource failure. Fully resealed negative fixtures pass reference consistency before rejecting semantic tampering. CLI constructor/import sentinels prove software-preflight zero runtime construction. Real software children cover exit0/7/deadline. The unreap case is a simulated process edge, not an actual kernel hang; partial publication uses controlled real filesystem interleaving. Original-byte compact artifacts: evidence_rt. Full local raw fixture paths/hashes: SYNTHETIC_EVIDENCE_RT_INDEX.json and RT_RELIABILITY_EVIDENCE_INDEX.json. Prefix fragments are explicitly incomplete.

Original draft48pass/1fail UTC fixture failure, subsequent9bc79pass runs, both9bc full runs, assembly typo and quoting errors, and failed HTTPS authentication receipt remain recorded. They are not relabeled as final results. GitHub Git transport was used only for the explicitly authorized own science-branch publication; no execution-host SSH/resource inspection occurred. See PUBLICATION_TRANSPORT_NOTE.md.

## Remaining limits and authority

Actual Qwen tokenizer/8B/CUDA initialization/ALFWorld/execution-host SSH/production preflight/scientific collection/teacher/training/evaluation added0. Historical science5142generations/7949operations, including177/342, remains unchanged; old engineering costs/evidence are retained. Consumed protocol/metadata/design/review bytes match both finalization snapshots. Unconsumed old raw science was not rehashed or modified.

Real runtime remains BLOCKED_UNPROVEN_HOST_LOCAL_PID_MAPPING. No ownership/UUID/PID guard is relaxed. Software does not prove actual load/resource feasibility, fresh-task token usage, long-run/power-loss behavior, scientific yield or learning. Root must independently review this exactSHA and genuine runtime prerequisites before later real metadata preparation/preflight/clearance. No launch or independentPASS authority belongs to the developer. Teacher/learning/evaluation remain absent.

Provenance is LOCAL_ONLY_PENDING_COORDINATOR_PUBLICATION; no sharedINDEX/inventory, provenance commit/push, other worktree or old evidence was edited. Full bindings: ASSIGNMENT.json, INPUT_BINDINGS_AFTER.json, RT_FIX_RULING_BINDING.json. Full source/method delta: source_delta_final.patch, METHOD_HASHES_FINAL.json, SOURCE_SCOPE_FINAL.json. Tests: SOFTWARE_COMPARISON_FINAL.json. Publication: PUBLICATION_MANIFEST.json and FILE_HASHES.sha256.
'''
with (OWN/'HANDOFF.md').open('x') as f:f.write(handoff)
record=f'''# Record

UTC {datetime.now(timezone.utc).isoformat()}. Own SI-S01 engineering evidence; LOCAL_ONLY_PENDING_COORDINATOR_PUBLICATION. Source {SHA}; base{BASE}. Task5fd913a8..., protocol daa1d787... and bounded root ruling46f2df17... verified. Required project documents were read before source edits. Only a new isolated worktree/branch was developed; all543old Git blobs and the old844worktree remain unchanged.

Commits744b9e0/9bc15b5 introduced the source-only path. Authentic9bc tests finished before the bounded correction; finald7a82ac changes only five approved new files. Final focused83pass exit0, full{counts} authentic exit1, exact80historical keys unchanged. Raw logs, original failures, intermediate receipts, own assembly errors and genuine subprocess exits remain retained. No skipped tests/new expected regression IDs or fingerprint bypasses were added.

Compact artifacts are original-byte copies of synthetic output; complete raw trees stay local at bound paths. The final source branch was non-force published using the existing GitHub Git service after HTTPS authentication lacked a helper. No execution-host SSH or scientific runtime occurred. No provenance Git publication/sharedINDEX edits occurred. Historical science5142/7949 remains unchanged. Source/evidence freeze at this seal, pending root's independent review; coordinator publishes selected bytes.
'''
with (OWN/'RECORD.md').open('x') as f:f.write(record)
write('FROZEN_HANDOFF.json',{'status':'FROZEN_DEVELOPER_DELIVERY_PENDING_ROOT_EXACT_SHA_REVIEW','source_sha':SHA,'base_sha':BASE,'branch':ref,'worktree':str(REPO),'remote_equality':binding(OWN/'REMOTE_EQUALITY.json'),'test_comparison':binding(OWN/'SOFTWARE_COMPARISON_FINAL.json'),'handoff':binding(OWN/'HANDOFF.md'),'record':binding(OWN/'RECORD.md'),'focused_passed':83,'full_counts':counts,'no_new_failure_error_IDs_or_types':True,'all543_original_Git_entries_equal':True,'source_methods':binding(OWN/'METHOD_HASHES_FINAL.json'),'incremental_scope':binding(OWN/'RT_INCREMENTAL_SCOPE.json'),'actual_runtime':'BLOCKED_UNPROVEN_HOST_LOCAL_PID_MAPPING','developer_scientific_calls_added':0,'historical_science':{'model_generations':5142,'environment_operations':7949},'provenance_status':'LOCAL_ONLY_PENDING_COORDINATOR_PUBLICATION','independent_acceptance_or_launch_clearance':False,'publication_manifest_path':str(OWN/'PUBLICATION_MANIFEST.json')})
files=[p for p in OWN.rglob('*') if p.is_file() and not p.is_symlink() and 'pytest_cache' not in p.parts and '__pycache__' not in p.parts]
selected=[p for p in files if p.relative_to(OWN).parts[0]!='evidence'];excluded=[p for p in files if p not in selected]
write('LOCAL_INVENTORY.json',{'scope':'Own payload excluding transient caches and self-referential seal files. Outside /tmp raw trees are separately bound.','selected_for_publication':[binding(p)|{'relative_path':str(p.relative_to(OWN))} for p in sorted(selected)],'retained_local_not_selected':[binding(p)|{'relative_path':str(p.relative_to(OWN))} for p in sorted(excluded)]})
selected.append(OWN/'LOCAL_INVENTORY.json')
with (OWN/'FILE_HASHES.sha256').open('x') as f:
 for p in sorted(selected):f.write(binding(p)['sha256']+'  '+str(p.relative_to(OWN))+'\n')
selected.append(OWN/'FILE_HASHES.sha256')
write('PUBLICATION_MANIFEST.json',{'schema':'SI_S01_OWN_COMPACT_PUBLICATION_V1','status':'LOCAL_ONLY_PENDING_COORDINATOR_PUBLICATION','source_sha':SHA,'root':str(OWN),'no_self_hash_cycle':'Manifest excludes itself; FILE_HASHES excludes itself and manifest. Manifest hash returned externally.','files':[binding(p)|{'relative_path':str(p.relative_to(OWN))} for p in sorted(selected)],'retained_local_not_selected':[str(p.relative_to(OWN)) for p in sorted(excluded)],'not_published_by_developer':True,'shared_INDEX_or_root_inventory_touched':False})
print(json.dumps({'source_sha':SHA,'manifest':binding(OWN/'PUBLICATION_MANIFEST.json'),'selected_files':len(selected),'selected_bytes':sum(p.stat().st_size for p in selected),'handoff':binding(OWN/'HANDOFF.md'),'frozen_handoff':binding(OWN/'FROZEN_HANDOFF.json')}))
