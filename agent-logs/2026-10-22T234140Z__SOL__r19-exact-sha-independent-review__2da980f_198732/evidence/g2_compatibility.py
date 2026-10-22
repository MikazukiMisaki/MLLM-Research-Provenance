"""Read and re-evaluate preserved G2 evidence without loading models or environments."""
import json,sys
from pathlib import Path
from collections import Counter
root=Path('/tmp/r19-independent-review-2da980f')
sys.path[:0]=[str(root),str(root/'src')]
from scripts import run_r19_experiment as r
from scripts import analyze_r19_recovery_duration as a
original=Path('/home/lizening/wt-r19-recovery-duration-v1')
gate=json.loads((original/'configs/local/r19_b1_g3_gate_bf31f3.json').read_text())
auth,_=r._load_g3_authorization()
evidence=Path(gate['g2_carry_forward']['evidence_directory'])
for name,digest in auth['g2_carry_forward']['evidence_file_sha256'].items():
 assert r.sha256_file(evidence/name)==digest
manifest=json.loads((evidence/'execution_manifest.json').read_text())
events=r._read_jsonl(evidence/'execution_events.jsonl');branches=r._read_jsonl(evidence/'branches.jsonl')
physical=a.validate_event_ledger(events,expected_evidence_class='live')
r._verify_b1_smoke_raw_k3_signatures(branches,events)
baseline=json.loads(r.R19_B1_BASELINE.read_text())
bounds=r._compute_b1_smoke_bounds(baseline,json.loads(r.R8_PREFIX_MANIFEST.read_text()))
registry=json.loads((evidence/'unit_registry.json').read_text())
checks=r._evaluate_r19_b1_smoke(rows=branches,events=events,
 isolation=json.loads((evidence/'runtime_manifest.json').read_text())['model_adapter_isolation'],
 model_calls=physical['completed_physical_model_generations'],
 environment_operations=physical['physical_environment_operations']+physical['physical_environment_resets'],
 bounds=bounds,unit_registry_status_counts=dict(Counter(u['status'] for u in registry['units'].values())))
assert checks==json.loads((evidence/'smoke_checks.json').read_text())==manifest['execution']
assert manifest['implementation_sha']==r.R19_G2_EXECUTED_SHA
print(json.dumps({'class':'read_only_old_G2_evidence_not_new_smoke','raw_G2_recomputed':checks['status'],
 'g2_executed_sha':manifest['implementation_sha'],'g2_run_id':manifest['run_id'],
 'physical_generations':physical['completed_physical_model_generations'],
 'physical_environment_operations_including_resets':physical['physical_environment_operations']+physical['physical_environment_resets'],
 'bounds':bounds,'all_five_pinned_evidence_hashes_match':True,
 'no_G2_rerun':True,'new_SHA_carry_forward':'PENDING_SOL_REVIEW'},indent=2))
