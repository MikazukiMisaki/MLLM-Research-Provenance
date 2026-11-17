"""Write only synthetic, no-op IPC exchange evidence to a fresh directory."""
import json
from pathlib import Path
import socket
import subprocess
import sys
import bridge
root=Path(__file__).parent/'synthetic-evidence'
root.mkdir(mode=0o700)
owner=bridge.Budget(root/'owner',{'model_load':2,'generation':2})
results=[]
for arm in ('A','B'):
    parent,child=socket.socketpair()
    log=root/('worker-'+arm+'.jsonl')
    proc=subprocess.Popen([sys.executable,'-I','-B',str(Path(__file__).parent/'fake_client.py'),str(child.fileno()),str(log),'normal'],pass_fds=(child.fileno(),))
    child.close()
    try:owner.serve(parent,arm,log)
    finally:parent.close()
    rc=proc.wait(timeout=8)
    results.append({'arm':arm,'synthetic_child_returncode':rc})
    if rc:raise SystemExit('synthetic child failed')
(root/'receipt.json').write_text(json.dumps({'scope':'synthetic-only no-op callbacks','children':results,'counts':owner.counts,'finished':owner.finished,'failed':owner.failed},sort_keys=True,indent=2)+'\n')
