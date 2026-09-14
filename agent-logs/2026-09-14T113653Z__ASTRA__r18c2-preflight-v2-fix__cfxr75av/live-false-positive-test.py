import os,sys,json,subprocess,time
from pathlib import Path
from test_process_identity_v2 import m
from infra_helpers import P,REPO,run
jobs=[]
try:
 specs=[['/usr/bin/bash','-c','exec sleep 8',str(m.Rules().script)],
        [str(m.PYTHON),'-c','import time; time.sleep(8)',str(m.Rules().script)],
        ['/usr/bin/grep',str(m.Rules().script)]]
 for args in specs:
  jobs.append(subprocess.Popen(args,cwd=P,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL))
 time.sleep(0.15)
 boot=Path('/proc/sys/kernel/random/boot_id').read_text().strip()
 identities=[]
 for job in jobs:
  proc=m.read_process(job.pid,boot)
  assert proc is not None
  verdict=m.classify(proc)
  assert verdict['kind']=='unrelated',verdict
  identities.append({'identity':m.asdict(proc),'verdict':verdict})
 env=os.environ.copy();env.update(ALFWORLD_DATA='/home/lizening/alfworld_data',ALFWORLD_CONFIG_PATH=str(REPO/'configs/local/alfworld_base_university.yaml'),TOKENIZERS_PARALLELISM='false',PYTHONPATH='.')
 result=run([str(m.PYTHON),str(P/'future-preflight-v2.py')],'real-server-preflight.log',cwd=REPO,env=env)
 (P/'live-false-positive-results.json').write_text(json.dumps({'identities':identities,'preflight_exit':result.returncode,'preflight_output':result.stdout},indent=2)+'\n')
 assert result.returncode==0,result.stdout
 print(json.dumps({'live_unrelated_processes':len(identities),'preflight':'PASS'},indent=2))
finally:
 for job in jobs:
  if job.stdin:job.stdin.close()
 for job in jobs:job.wait(timeout=15)
 print('All owned false-positive processes exited and were reaped.')
