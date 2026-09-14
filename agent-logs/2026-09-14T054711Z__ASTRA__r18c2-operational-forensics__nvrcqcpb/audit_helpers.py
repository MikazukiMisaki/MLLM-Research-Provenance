from pathlib import Path
import subprocess,shlex,json,datetime
P=Path(__file__).resolve().parent
REPO=Path('/home/lizening/Alfworld-Self-Improvement-Project')
RUNTIME=REPO/'artifacts/runtime/validation/progress-aware-r18-c2-formal-aa9fa3c34520941e'
def run(args,artifact=None,cwd=REPO,timeout=30):
 try:
  r=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
  output=r.stdout;rc=r.returncode
 except OSError as e:
  output=str(e)+'\n';rc=127
 except subprocess.TimeoutExpired as e:
  output=str(e.output or '')+'\nTIMEOUT';rc=124
 text='\nUTC: '+datetime.datetime.now(datetime.timezone.utc).isoformat()+'\nCWD: '+str(cwd)+'\n$ '+shlex.join(args)+'\n'+output+'\nEXIT: '+str(rc)+'\n'
 with (P/'commands.log').open('a') as f:f.write(text)
 if artifact:
  with (P/artifact).open('a') as f:f.write(text)
 return rc,output
