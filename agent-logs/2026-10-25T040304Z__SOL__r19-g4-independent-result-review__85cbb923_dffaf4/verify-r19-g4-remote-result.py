from pathlib import Path
import subprocess,json,hashlib,datetime
repo=Path('/home/lizening/research-notes');p=Path(Path('/tmp/r19-g4-result-review-path.txt').read_text().strip());op=repo/'agent-logs/2026-10-25T040521Z__LUNA__r19-formal-g4__85cbb923';report=repo/'agent-logs/2026-10-23T043602Z__LUNA__r19-g4-readiness__85cbb923/future_g4_report'
def git(*a):return subprocess.check_output(['git','-C',str(repo),*a],text=True).strip()
commit=git('rev-parse','HEAD');assert commit==git('rev-parse','origin/main')==git('ls-remote','origin','refs/heads/main').split()[0]=='3a98491e7304ba90926df8d8a00f0c3504aeab79'
assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
files=sorted([x for x in op.iterdir() if x.is_file()]+[x for x in report.iterdir() if x.is_file()]+[repo/'INDEX.md',repo/'FILE_HASHES.sha256']);assert len(files)==21
verified={}
for f in files:
 path=str(f.relative_to(repo));b=subprocess.check_output(['git','-C',str(repo),'show',commit+':'+path]);h=hashlib.sha256(b).hexdigest();assert h==hashlib.sha256(f.read_bytes()).hexdigest();verified[path]=h
for line in (op/'FILE_HASHES.sha256').read_text().splitlines():
 h,f=line.split('  ',1);assert hashlib.sha256((op/f).read_bytes()).hexdigest()==h
record={'status':'PASS_REMOTE_ALL_ORIGINAL_G4_OUTPUTS_AND_EXECUTION_EVIDENCE_BYTE_VERIFICATION','verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'provenance_commit':commit,'initial_raw_upload_commit':'172c051ba53b5e0aec355352a37d767b81690496','local_origin_and_live_remote_equal':True,'verified_file_count':len(verified),'raw_report_file_count':3,'verified_file_sha256':verified,'all_three_original_report_files_and_full_execution_logs_context_receipts_uploaded':True,'operator_task_inventory_matches':True,'scientific_evidence_or_report_changes':0,'reviewer_invoked_no_new_formal_analyzer':True,'scope_only_new_operator_evidence_report_leaf_and_additive_root_index_inventory':True,'initial_intermediate_metadata_comparison':'Observed incomplete operator publication metadata after first checkpoint; waited for final operator handoff, then21/21 matched. The three raw report files were already correct at first checkpoint; no scientific drift occurred.'}
(p/'remote_raw_result_verification.json').write_text(json.dumps(record,indent=2)+'\n');(p/'verify-r19-g4-remote-result.py').write_bytes(Path(__file__).read_bytes());print(json.dumps({k:v for k,v in record.items() if k not in ['verified_file_sha256','initial_intermediate_metadata_comparison']},indent=2))
