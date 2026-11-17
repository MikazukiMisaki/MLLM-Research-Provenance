from pathlib import Path
import subprocess
import sys
import tempfile

root=Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-owned-scheduler-v2__private')
sys.path.insert(0,str(root))
import test_scheduler, scheduler_synthetic
real_popen=subprocess.Popen
children=[]
def fictional_spawn(*args, **kwargs):
    p=real_popen([sys.executable, '-c', 'import time; time.sleep(20)'],start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    children.append(p)
    return p
def unknown_identity(proc):
    raise scheduler_synthetic.Stop('synthetic capture failure')
scheduler_synthetic.subprocess.Popen=fictional_spawn
scheduler_synthetic.capture_owned=unknown_identity
try:
    with tempfile.TemporaryDirectory() as t:
        path=Path(t).resolve()
        inputs,setup,verify=test_scheduler.fixture(path)
        try:
            scheduler_synthetic.run_fixture(path/'run',path,inputs,setup,verify)
            raise AssertionError('failure not triggered')
        except scheduler_synthetic.Stop as exc:
            assert str(exc)=='synthetic capture failure'
        assert len(children)==1 and children[0].poll() is None
        print('CONFIRMED: scheduler failed stop but its direct child remained live after capture failure')
finally:
    for child in children:
        if child.poll() is None:child.terminate()
        child.wait(timeout=5)
    print('Review-owned fictional sleeper explicitly terminated and reaped')
