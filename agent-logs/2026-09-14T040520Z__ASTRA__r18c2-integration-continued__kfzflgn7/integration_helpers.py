from pathlib import Path
import subprocess, json, shlex, os
P=Path(__file__).resolve().parent
S=json.loads((P/'state.json').read_text())
INTEGRATION='/home/lizening/wt-codex-r18c2'
AUTHORITATIVE='/home/lizening/Alfworld-Self-Improvement-Project'
ACCEPTED='5ebb7ff9a7b50b035e6871735bdfe3fa9d88ff39'
BASE='b06b1fb9ad31f54fb2b660a48ada707a4aeababe'
PYTHON='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'
def save():
 (P/'state.json').write_text(json.dumps(S,indent=2)+'\n')
def run(args,cwd=INTEGRATION,log=None,env=None,check=True):
 r=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env)
 e={'cwd':cwd,'command':shlex.join(args),'exit_code':r.returncode,'output':r.stdout}
 S['commands'].append(e)
 with (P/'commands.log').open('a') as f:f.write('\nCWD: '+cwd+'\n$ '+e['command']+'\n'+r.stdout+'\nEXIT: '+str(r.returncode)+'\n')
 if log:(P/log).write_text(r.stdout)
 save()
 if check and r.returncode:raise RuntimeError(e['command']+' failed: '+r.stdout)
 return r.stdout.strip()
def gate(ok,message):
 if not ok:raise RuntimeError(message)
def stop(exc):
 S['errors'].append(str(exc));S['status']='STOP';save();print('STOP: '+str(exc))
