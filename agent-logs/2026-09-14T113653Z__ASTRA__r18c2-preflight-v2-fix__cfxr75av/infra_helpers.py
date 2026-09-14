from pathlib import Path
from datetime import datetime,timezone
import subprocess,shlex
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
REPO=Path('/home/lizening/Alfworld-Self-Improvement-Project')
def run(args,log='commands.log',cwd=P,env=None,timeout=60):
 r=subprocess.run(args,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
 msg='\nUTC '+datetime.now(timezone.utc).isoformat()+'\nCWD '+str(cwd)+'\n$ '+shlex.join(args)+'\n'+r.stdout+'\nEXIT '+str(r.returncode)+'\n'
 with (P/'commands.log').open('a') as f:f.write(msg)
 if log!='commands.log':
  with (P/log).open('a') as f:f.write(msg)
 return r
