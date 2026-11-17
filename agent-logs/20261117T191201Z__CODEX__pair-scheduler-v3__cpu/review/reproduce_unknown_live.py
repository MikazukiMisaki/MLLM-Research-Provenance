from pathlib import Path
import json, subprocess, sys, tempfile
root=Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-owned-scheduler-v3__private')
sys.path.insert(0,str(root))
import test_scheduler, scheduler_synthetic
real_popen=subprocess.Popen
children=[]
def fictional_spawn(*args, **kwargs):
    p=real_popen([sys.executable, '-c', 'import time; time.sleep(20)'],start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    children.append(p);return p
def capture_failure(proc):raise scheduler_synthetic.Stop('synthetic capture failure')
scheduler_synthetic.subprocess.Popen=fictional_spawn
scheduler_synthetic.capture_owned=capture_failure
try:
    with tempfile.TemporaryDirectory() as t:
        path=Path(t).resolve();inputs,setup,verify=test_scheduler.fixture(path)
        try:scheduler_synthetic.run_fixture(path/'run',path,inputs,setup,verify)
        except scheduler_synthetic.Stop as e:assert str(e)=='synthetic capture failure'
        else:raise AssertionError('no stop')
        rows=[json.loads(line) for line in (path/'run'/'owner'/'global.jsonl').read_text().splitlines()]
        cleanup=[r['payload'] for r in rows if r['event']=='synthetic_cleanup_after_abort']
        assert len(cleanup)==1 and cleanup[0]['cleanup_status']=='UNKNOWN_DIRECT_CHILD_STILL_UNREAPED'
        assert cleanup[0]['signal_sent'] is False and children[0].poll() is None
        assert any(r['event']=='aborted' for r in rows) and not any(r['event']=='synthetic_batch_complete' for r in rows)
        print('PASS: actual bounded wait timed out; child remained live; parent recorded UNKNOWN, no signal, batch stopped')
finally:
    for p in children:
        if p.poll() is None:p.terminate()
        p.wait(timeout=5)
    print('Review-owned fictional sleeper terminated and reaped by test harness')
