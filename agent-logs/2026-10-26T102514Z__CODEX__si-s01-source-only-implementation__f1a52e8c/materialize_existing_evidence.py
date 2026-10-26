from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
OWN=Path(__file__).resolve().parent;RAW=Path('/tmp/si-s01-draft_v2');OUT=OWN/'evidence';OUT.mkdir(exist_ok=False)
def b(path):
 p=Path(path);v=p.read_bytes();return {'path':str(p),'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()}
selections={'all96_not_futile':'test_all96_five_family_product0/run','complete_structural_no_go':'test_complete_source_structura0/run','s5_then_parser_failure':'test_fifth_action_then_sixth_p0/run','family_floor':'test_family_failure_floor_is_s0/run','technical_partial':'test_partial_stops_keep_prior_0/run','integrity_partial':'test_partial_stops_keep_prior_1/run','budget_partial':'test_partial_stops_keep_prior_2/run','simulated_time_cap':'test_simulated_allocation_cloc0/run','full_horizon_exact_caps':'test_full_horizon_exact_caps_a0/run','step50_empty_horizon':'test_step50_nonterminal_empty_0/run','p0_incomplete_eos_kept':'test_p0_valid_id_eos_incomplet0/run','fifth_terminal':'test_terminal_truncated_empty_0/run','fifth_truncated':'test_terminal_truncated_empty_1/run','fifth_empty':'test_terminal_truncated_empty_2/run','early_terminal':'test_terminal_truncated_empty_3/run','initial_empty':'test_terminal_truncated_empty_4/run'}
local=[];copies=[];report_summaries=[]
for label,relative in selections.items():
 src=RAW/relative;dest=OUT/label;dest.mkdir()
 for file in sorted(src.iterdir()):
  if file.is_file():local.append({'case':label,**b(file)})
 for name in ('source_report.json','SOURCE_REPORT.md'):
  srcfile=src/name;target=dest/name;target.write_bytes(srcfile.read_bytes());copies.append({'source':b(srcfile),'copy':b(target),'byte_identical':srcfile.read_bytes()==target.read_bytes()})
 r=json.loads((src/'source_report.json').read_bytes());report_summaries.append({'case':label,'report':str(dest/'source_report.json'),'status':r['status'],'normal_sources':r['normal_sources'],'source_phase_sealed':r['source_phase_sealed'],'upper_bounds':r['upper_bounds'],'physical':r['physical'],'real_device_hours':r['real_device_hours']})
 if label=='all96_not_futile':
  target=dest/'source_trajectories.jsonl';target.write_bytes((src/'source_trajectories.jsonl').read_bytes());copies.append({'source':b(src/'source_trajectories.jsonl'),'copy':b(target),'byte_identical':True})
  lines=[]
  with (src/'source_events.jsonl').open('rb') as f:
   for line in f:
    lines.append(line)
    event=json.loads(line)
    if event['kind']=='unit_completed' and event['payload']['identity']['kind']=='env_close':break
  target=dest/'first_source_events_PREFIX_FRAGMENT.jsonl';target.write_bytes(b''.join(lines))
  copies.append({'source':b(src/'source_events.jsonl'),'copy':b(target),'byte_identical_contiguous_prefix':True,'fragment_only_not_complete_source96_audit':True})
for label,relative in {'post_return_resource_failure':'test_new_bridge_post_resource_0','cli_positive':'test_software_fixture_actual_c0','cli_constructor_sentinel':'test_preflight_software_sentin0','supervisor_exit0':'test_authentic_exit_and_own_fo0/run','supervisor_exit7':'test_authentic_exit_and_own_fo1/run','supervisor_deadline':'test_deadline_terminates_real_0/deadline'}.items():
 src=RAW/relative;dest=OUT/label;dest.mkdir()
 names=('events.jsonl',) if label=='post_return_resource_failure' else ('child.stdout','child.stderr','child_receipt.json','preflight_receipt.json') if label.startswith('cli_') else ('supervisor_exit.json','launch_context.json','worker_start.json','worker.stdout','worker.stderr')
 for name in names:
  file=src/name
  if not file.is_file():continue
  target=dest/name;target.write_bytes(file.read_bytes());copies.append({'source':b(file),'copy':b(target),'byte_identical':True})
 for file in src.rglob('*'):
  if file.is_file() and not file.is_symlink():local.append({'case':label,**b(file)})
value={'captured_utc':datetime.now(timezone.utc).isoformat(),'source_sha':'9bc15b593ec6144915762a2fb1b172e063fe2c48','evidence_class':'synthetic_software_fixture','origin_receipt':str(OWN/'receipts/draft_v2.json'),'scope':'Existing software-test output only; no project producer/auditor/model/env is called by this stdlib copy/hash script. Original full fixture trees retained under /tmp. Byte fragments explicitly marked.','local_raw_files':local,'published_compact_copies':copies,'reports':report_summaries}
with (OWN/'SYNTHETIC_EVIDENCE_INDEX.json').open('x') as f:json.dump(value,f,indent=2);f.write('\n')
print(json.dumps({'cases':len(selections),'compact_copies':len(copies),'local_raw_files':len(local),'published_bytes':sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())}))
