"""CPU-only synthetic interface reproducers; no real model or environment."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

candidate_root=Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-production-interface-candidate__private')
sys.path.insert(0,str(candidate_root))
import candidate as c
from test_candidate import setup, verify, spawn_for

fake='''import json,socket,sys
s=socket.socket(fileno=int(sys.argv[1])); f=s.makefile('rwb',buffering=0)
def send(x):
 f.write((json.dumps(x)+'\\n').encode()); return json.loads(f.readline())
t=send({'type':'reserve','kind':'reset'})['token'];send({'type':'return','token':t,'receipt':{'synthetic':True}})
send({'type':'initial','state':{'fake':1}});send({'type':'done','won':True})
'''

with tempfile.TemporaryDirectory(prefix='review-fake-success-') as d:
    root=Path(d);worker=root/'fake.py';worker.write_text(fake);owner=c.Owner(root/'owner')
    def spawn(pair,arm,paths,fd):
        return subprocess.Popen([sys.executable,'-I','-B',str(worker),str(fd)],pass_fds=(fd,),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    for pair in c.PAIRS:
        c.pair(owner,pair,('A','B'),{'case':pair},setup,verify,spawn)
    owner.complete()
    rows=[json.loads(line) for line in owner.log.read_text().splitlines()]
    print('FAKE_SUCCESS_WITHOUT_MODEL:',json.dumps({'last':rows[-1]['type'],'counts':owner.count,'arm_results':sum(r['type']=='arm_result' for r in rows)},sort_keys=True))

with tempfile.TemporaryDirectory(prefix='review-caught-stop-') as d:
    owner=c.Owner(Path(d)/'owner')
    for pair in c.PAIRS[:3]:
        c.pair(owner,pair,('A','B'),{'case':pair},setup,verify,spawn_for())
    try:
        c.pair(owner,'four',('A','B'),{'case':'four'},setup,verify,spawn_for('mismatch'))
    except c.Stop as e:
        error=str(e)
    owner.complete()
    rows=[json.loads(line) for line in owner.log.read_text().splitlines()]
    print('CAUGHT_STOP_ACCEPTED:',json.dumps({'error':error,'last':rows[-1]['type'],'counts':owner.count,'arm_results':sum(r['type']=='arm_result' for r in rows)},sort_keys=True))
