from pathlib import Path
import subprocess,json,hashlib,ast
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
def git(*args):
 p=subprocess.run(['git',*args],cwd=ROOT,capture_output=True,text=True);assert p.returncode==0,p.stderr;return p.stdout
staged=git('diff','--cached','--name-status').splitlines();assert len(staged)==17 and all(x.startswith('A\t') for x in staged)
assert git('rev-parse','HEAD').strip()=='85cbb92395e5e2420c2adeb1fa0634653e742910'
assert not git('diff','--name-only')
files=[x.split('\t')[1] for x in staged]
for name in files:
 b=(ROOT/name).read_bytes()
 assert b'/home/' not in b and b'/tmp/' not in b, name
 if name.endswith('.py'):ast.parse(b)
 if name.endswith('.json'):json.loads(b)
report={'base_sha':git('rev-parse','HEAD').strip(),'only_additions':files,'old_tracked_changes':[], 'machine_paths_in_commit':False,'file_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in files},'independent_acceptance':'NOT_ISSUED','scientific_execution':'NOT_GRANTED'}
(OWN/'precommit_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
