from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path(__file__).resolve().parent
r=Path('/home/lizening/research-notes/agent-logs/2026-10-25T143804Z__LUNA__si-e2-context-inspection__cudafix_3a14')
d=json.loads((r/'INSPECTION_RECEIPT.json').read_bytes())
assert d['ssh_attempted'] and d['ssh_returncode']==255 and d['ssh_timeout'] is False
err=(r/'ssh.stderr.bin').read_text();assert 'Permission denied (publickey,password)' in err and (r/'ssh.stdout.bin').stat().st_size==0
assert 'BatchMode=yes' in d['ssh_argv'] and 'StrictHostKeyChecking=yes' in d['ssh_argv']
manifest=json.loads((r/'FINAL_PUBLICATION_MANIFEST.json').read_bytes());assert manifest['source_sha_observed']=='NOT_OBSERVED' and manifest['remote_host_identity_observed'] is False
result={'UTC':datetime.now(timezone.utc).isoformat(),'READ_ONLY_CONTEXT_AUDIT':'PASS_EVIDENCE_OF_UNAVAILABLE_EXISTING_AUTHENTICATED_ROUTE','GPU_RUNTIME_READINESS':'BLOCKED','existing_ssh_authentication':'FAILED_255','one_read_only_SSH_attempt':True,'timeout':False,'remote_execution_or_source_SHA':'NOT_OBSERVED','host_local_PID_binding':'NOT_PROVEN','config_keys_credentials_privileges_changed':False,'new_CUDA_model_environment_or_science_calls':0,'raw_error':err,'next_capability_needed':'Already authorized trusted host execution route or independently authenticated host/local PID mapping; never accept unknown PID by correlation','not_an_approval_request':True,'no_probe_retry_release':True,'evidence':{p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in (r/'INSPECTION_RECEIPT.json',r/'LOCAL_CAPABILITY_SNAPSHOT.json',r/'ssh.stdout.bin',r/'ssh.stderr.bin',r/'RECORD.md')}}
with (ROOT/'independent_context_inspection_review.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'status':result['READ_ONLY_CONTEXT_AUDIT'],'runtime':result['GPU_RUNTIME_READINESS'],'raw_ssh_exit':255}))
