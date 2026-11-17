import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

source = '/home/lizening/research-notes/agent-logs/20261118__CODEX__fictional-final-checkpoint__private'
child = r'''
import os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import final_checkpoint as c
import torch
assert not torch.cuda.is_initialized()
target = Path(sys.argv[2])
cb = c.FictionalFinalCheckpoint(target)
values = {'fictional.weight': torch.tensor([1.0, 2.0], device='cpu')}
if sys.argv[3] == 'before_publish':
    cb(16, values, after_temp_sync=lambda: os._exit(23))
else:
    original = c.fsync_dir
    def exit_at_final_dir(path):
        if Path(path) == target:
            os._exit(24)
        return original(path)
    c.fsync_dir = exit_at_final_dir
    cb(16, values)
raise AssertionError('unexpected callback return')
'''
env = dict(os.environ, CUDA_VISIBLE_DEVICES='', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
with tempfile.TemporaryDirectory(prefix='fictional-checkpoint-review-') as tmp:
    root = Path(tmp)
    for mode, expected in [('before_publish', 23), ('after_receipt', 24)]:
        parent = root / mode
        parent.mkdir()
        target = parent / 'final'
        p = subprocess.run([sys.executable, '-I', '-B', '-c', child, source, str(target), mode], env=env, capture_output=True, text=True, timeout=30)
        assert p.returncode == expected, (mode, p.returncode, p.stderr)
        pending = list(parent.glob('.final.pending-*'))
        row = {'mode': mode, 'child_exit': p.returncode, 'callback_return_observed': False,
               'target_exists': target.exists(), 'pending_count': len(pending), 'classification': 'UNKNOWN'}
        if mode == 'before_publish':
            assert not target.exists() and len(pending) == 1
            row['pending_names'] = sorted(p.name for p in pending[0].iterdir())
        else:
            assert target.is_dir() and not pending
            receipt = json.loads((target / 'receipt.json').read_text())
            row['receipt'] = receipt
            row['artifact_sha256'] = hashlib.sha256((target / 'fictional.safetensors').read_bytes()).hexdigest()
            assert receipt['status'] == 'RELOAD_CHECKED_CALLBACK_RETURN_REQUIRED'
        print(json.dumps(row, sort_keys=True))
