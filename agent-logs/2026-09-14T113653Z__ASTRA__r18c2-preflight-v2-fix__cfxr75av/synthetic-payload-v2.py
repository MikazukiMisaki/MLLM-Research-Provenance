"""Harmless stand-in: sleep and output identity; no scientific imports or actions."""
import argparse,json,os,sys,time
from pathlib import Path
from datetime import datetime,timezone
parser=argparse.ArgumentParser();parser.add_argument('--output');parser.add_argument('--resume',action='store_true');args=parser.parse_args()
assert args.resume and Path(args.output)==Path(__file__).resolve().parent/'synthetic-runtime'
assert os.readlink('/proc/self/fd/0')=='/dev/null'
assert os.environ['SYNTHETIC_SENTINEL']=='retained value $ ;'
for tick in range(4):
 print(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'pid':os.getpid(),'ppid':os.getppid(),'pgid':os.getpgid(0),'sid':os.getsid(0),'tick':tick}),flush=True)
 print('STDERR_TICK '+str(tick),file=sys.stderr,flush=True)
 time.sleep(5)
rc=int(os.environ['SYNTHETIC_EXIT'])
Path(os.environ['SYNTHETIC_JOB'],'payload.complete').write_text(json.dumps({'exit':rc,'natural_completion':True})+'\n')
sys.exit(rc)
