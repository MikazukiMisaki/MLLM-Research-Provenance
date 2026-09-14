import os,sys,time,json,datetime
from pathlib import Path
job=Path(sys.argv[1]); rc=int(sys.argv[2])
assert os.environ['LAUNCH_TEST_SENTINEL']=='space and $literal; line\nsecond'
assert os.readlink('/proc/self/fd/0')=='/dev/null'
for i in range(7):
 row={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'ppid':os.getppid(),'pgid':os.getpgid(0),'sid':os.getsid(0),'tty':os.isatty(0),'tick':i,'env_preserved':True}
 print(json.dumps(row),flush=True)
 print('STDERR_TICK '+str(i),file=sys.stderr,flush=True)
 time.sleep(5)
(job/'payload.complete').write_text(json.dumps({'expected_exit':rc,'pid':os.getpid(),'natural_completion':True})+'\n')
print('PAYLOAD_NATURAL_COMPLETION',flush=True)
sys.exit(rc)
