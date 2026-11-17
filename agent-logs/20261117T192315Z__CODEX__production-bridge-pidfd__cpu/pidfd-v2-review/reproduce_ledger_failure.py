import pathlib,sys,tempfile
from unittest.mock import patch
sys.path.insert(0,'/home/lizening/research-notes/agent-logs/20261118__CODEX__owned-child-pidfd-owner-v2__private')
from owner import Owner
with tempfile.TemporaryDirectory() as t:
    owner=Owner(pathlib.Path(t)/'owner')
    assert owner.launch([sys.executable,'-c','import time;time.sleep(.5)'])
    original=owner._record
    def record(state,**kw):
        if state=='UNKNOWN':raise OSError('fictional fsync failure')
        return original(state,**kw)
    def failed_open(pid):raise RuntimeError('fictional open failure')
    with patch.object(owner,'_record',side_effect=record):
        assert owner.terminate(open_pidfd=failed_open) is False
    assert owner.state=='UNKNOWN' and owner.durable is False and owner.child is not None
    text=owner.path.read_text()
    assert '"state": "UNKNOWN"' not in text
    print('PASS: failed UNKNOWN write -> durable=False; no false durable journal claim; direct child retained')
    assert owner.await_natural_exit(2)==0
    print('Reviewer-owned finite child reaped naturally')
