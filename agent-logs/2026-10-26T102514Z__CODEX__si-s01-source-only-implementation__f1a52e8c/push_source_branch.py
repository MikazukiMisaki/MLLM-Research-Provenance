from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,time
OWN=Path(__file__).resolve().parent;REPO=Path('/home/lizening/wt-si-p3-source-only-v2');EXPECTED='d7a82acb510157ab7ba5439d790816c5c948439f';REF='refs/heads/codex/si-p3-source-only-v2';REMOTE='https://github.com/MikazukiMisaki/Alfworld-Self-Improvement-Project.git'
comparison=json.loads((OWN/'SOFTWARE_COMPARISON_FINAL.json').read_bytes());assert comparison['source_sha']==EXPECTED and not comparison['new_problem_IDs']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()==EXPECTED
assert not subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True)
assert subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()=='codex/si-p3-source-only-v2'
env=dict(os.environ);env.update(GIT_TERMINAL_PROMPT='0',GIT_ALLOW_PROTOCOL='https',GIT_SSH_COMMAND='false')
records=[]
def run(label,argv):
 at=time.monotonic();utc=datetime.now(timezone.utc).isoformat()
 with (OWN/'receipts'/(label+'.stdout')).open('xb') as out,(OWN/'receipts'/(label+'.stderr')).open('xb') as err:r=subprocess.run(argv,cwd=REPO,env=env,stdout=out,stderr=err)
 receipt={'argv':argv,'cwd':str(REPO),'source_sha':EXPECTED,'started_utc':utc,'authentic_returncode':r.returncode,'elapsed_seconds':time.monotonic()-at,'transport':'HTTPS_ONLY_SSH_DISABLED','force':False}
 for suffix in ('stdout','stderr'):
  p=OWN/'receipts'/(label+'.'+suffix);b=p.read_bytes();receipt[suffix]={'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 with (OWN/'receipts'/(label+'.json')).open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
 records.append(receipt);assert r.returncode==0,(label,r.returncode)
 return (OWN/'receipts'/(label+'.stdout')).read_text()
before=run('remote_before',['git','ls-remote','--heads',REMOTE,REF])
run('source_push',['git','push','--porcelain',REMOTE,'HEAD:'+REF])
after=run('remote_after',['git','ls-remote','--heads',REMOTE,REF])
assert after.strip()==EXPECTED+'\t'+REF,after
assert not subprocess.check_output(['git','status','--porcelain=v1'],cwd=REPO,text=True)
value={'repository':REMOTE,'ref':REF,'source_sha':EXPECTED,'remote_before_stdout':before,'live_remote_stdout':after,'live_remote_equals_clean_local_HEAD':True,'non_force_push':True,'HTTPS_only_no_host_SSH':True,'only_own_scientific_branch_updated':True,'provenance_commit_push_or_shared_inventory_mutation':False,'receipts':records}
with (OWN/'REMOTE_EQUALITY.json').open('x') as f:json.dump(value,f,indent=2);f.write('\n')
print(json.dumps({'source_sha':EXPECTED,'remote_ref':REF,'live_remote_equality':True}))
