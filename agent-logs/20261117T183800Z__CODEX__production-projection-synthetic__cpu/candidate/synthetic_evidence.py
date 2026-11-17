"""Retain one fictional two-step pair; never use real task/model assets."""
import json
from pathlib import Path
from test_pair import fixture
from pair_synthetic import run_pair
root=Path(__file__).parent/'synthetic-evidence'
root.mkdir(mode=0o700)
inputs,setup,verify=fixture(root)
owner=run_pair(root/'run',inputs,setup,verify)
(root/'receipt.json').write_text(json.dumps({'scope':'fictional inputs, fake boundaries and child claims only',
  'counts':owner.counts,'finished':owner.finished,'closed':sorted(owner.closed),'failed':owner.failed},sort_keys=True,indent=2)+'\n')
