"""Capture an independent pinned-interpreter software check, with no hidden GPU."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

OWN = Path(__file__).resolve().parent
assert OWN.name == '2026-10-25T102943Z__SOL__si-e1-engineering-review__sie1_b8f6'
label, checkout, *arguments = sys.argv[1:]
assert label.replace('_', '').replace('-', '').isalnum() and arguments
checkout = Path(checkout).resolve()
assert str(checkout).startswith('/tmp/si-e1-independent-review-')
assert (checkout / '.git').exists()
directory = OWN / 'independent_software'
directory.mkdir(exist_ok=True)
assert not (directory / (label + '.receipt.json')).exists()
env = os.environ.copy()
for variable in ('PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV'):
    env.pop(variable, None)
env.update({'CUDA_VISIBLE_DEVICES': '', 'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1',
            'PYTHONDONTWRITEBYTECODE': '1', 'TOKENIZERS_PARALLELISM': 'false',
            'PYTHONNOUSERSITE': '1', 'PYTHONPATH': str(checkout / 'src')})
argv = ['/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'] + arguments
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
timer = time.monotonic()
completed = subprocess.run(argv, cwd=checkout, env=env, capture_output=True)
blobs = {}
for name, data in (('stdout', completed.stdout), ('stderr', completed.stderr)):
    path = directory / (label + '.' + name)
    path.write_bytes(data)
    blobs[name] = {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
receipt = {'argv': argv, 'cwd': str(checkout), 'started_utc': start,
           'elapsed_monotonic_seconds': time.monotonic() - timer,
           'returncode': completed.returncode, 'capture': blobs,
           'effective_overrides': {k: env[k] for k in ('CUDA_VISIBLE_DEVICES', 'HF_HUB_OFFLINE',
                                  'TRANSFORMERS_OFFLINE', 'PYTHONDONTWRITEBYTECODE', 'PYTHONPATH')},
           'classification': 'SOFTWARE_CHECK_ONLY; synthetic model/env edges and CPU toy may execute; no scientific runtime'}
(directory / (label + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
sys.stdout.flush()
sys.stdout.buffer.write(completed.stdout)
sys.stderr.buffer.write(completed.stderr)
sys.exit(completed.returncode)
