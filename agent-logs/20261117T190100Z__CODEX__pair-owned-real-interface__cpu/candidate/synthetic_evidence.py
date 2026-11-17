"""Retain one fake worker + real candidate stage/IPC transcript; no real task."""
import json
from pathlib import Path
import global_owner
from test_candidate import CandidateTest, fixture
root=Path(__file__).parent/'synthetic-evidence'
root.mkdir(mode=0o700)
t=CandidateTest(methodName='test_shared_paths_real_stage_protocol_and_token_full_debit')
t.root=root.resolve();t.inputs,t.setup,t.verify=fixture(t.root)
t.owner=global_owner.GlobalOwner(t.root/'global')
t.binding=t.owner.materialize_pair('eval-two-pair-a',t.inputs,t.setup,t.verify)
rc,stage,error,stderr,work=t.run_arm()
(root/'fake-worker-stderr.log').write_bytes(stderr)
(root/'parent-channel-claims.json').write_text(json.dumps(stage.journal.rows,sort_keys=True,indent=2)+'\n')
result={'scope':'synthetic cases and no-op boundaries only','fake_worker_returncode':rc,
        'channel_finished':stage.finished,'channel_error':None if error is None else str(error),
        'global_counts':t.owner.counts,'conservative_token_reservations':t.owner.tokens}
(root/'receipt.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
if rc!=0 or error is not None or stage.finished!='COMPLETED':raise SystemExit('synthetic transcript failure')
