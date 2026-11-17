"""Persist successful and cleanup-failure fictional transcripts, no real inputs."""
import json
from pathlib import Path
from test_scheduler import fixture
from scheduler_synthetic import run_fixture
import global_owner
root=Path(__file__).parent/'synthetic-evidence'
root.mkdir(mode=0o700)
complete=root/'complete';complete.mkdir()
inputs,setup,verify=fixture(complete)
owner=run_fixture(complete/'run',complete,inputs,setup,verify)
(complete/'receipt.json').write_text(json.dumps({'scope':'fictional only','counts':owner.counts,
 'token_reservations':owner.tokens,'closed':sorted(owner.closed),'completed':owner.completed},sort_keys=True,indent=2)+'\n')
stopped=root/'stopped';stopped.mkdir()
inputs,setup,verify=fixture(stopped)
try:
    run_fixture(stopped/'run',stopped,inputs,setup,verify,linger_case=global_owner.SCHEDULE[1][0])
except Exception as error:
    (stopped/'receipt.json').write_text(json.dumps({'scope':'fictional only','status':'expected fail-stop',
      'exception_type':type(error).__name__,'message':str(error)},sort_keys=True,indent=2)+'\n')
else:raise SystemExit('cleanup failure did not stop')
