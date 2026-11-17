"""Retain one four-pair fictional software transcript, not an experiment."""
import json
from pathlib import Path
from test_batch import fixture
from batch_synthetic import run_batch
root=Path(__file__).parent/'synthetic-evidence'
root.mkdir(mode=0o700)
inputs,setup,verify=fixture(root)
owner=run_batch(root/'run',inputs,setup,verify)
(root/'receipt.json').write_text(json.dumps({'scope':'four fictional pairs and fake child claims only',
 'counts':owner.counts,'finished':owner.finished,'closed':sorted(owner.closed),'failed':owner.failed},sort_keys=True,indent=2)+'\n')
