from pathlib import Path
import datetime,json,subprocess
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts');SHA='a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3';branch='codex/si-p3-engineering-contracts'
commands=[]
def run(args,cwd=ROOT):
 p=subprocess.run(args,cwd=cwd,capture_output=True,text=True);commands.append({'argv':args,'cwd':str(cwd),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0,p.stderr;return p.stdout
head=run(['git','rev-parse','HEAD']).strip();origin=run(['git','rev-parse','origin/'+branch]).strip();live=run(['git','ls-remote','--heads','origin','refs/heads/'+branch,'refs/heads/codex/r19-g4-consumer-contract-repair','refs/heads/codex/r19-source-contract-review-fixes'])
refs={line.split()[1]:line.split()[0] for line in live.splitlines()}
assert head==origin==refs['refs/heads/'+branch]==SHA
assert refs['refs/heads/codex/r19-g4-consumer-contract-repair']=='85cbb92395e5e2420c2adeb1fa0634653e742910'
assert refs['refs/heads/codex/r19-source-contract-review-fixes']=='2da980f631badc25086d12db60d128ff507d3ae6'
assert not run(['git','status','--porcelain=v1'])
result={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen_SHA':SHA,'branch':branch,'remote_ref':'refs/heads/'+branch,'local_HEAD_origin_live_remote_equal':True,'old85_2da_remote_refs_unchanged':True,'clean':True,'source_publication_only':'non-force own science branch; provenance not staged/committed/pushed','commands':commands}
(OWN/'LIVE_REMOTE_EQUALITY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='commands'},indent=2))
