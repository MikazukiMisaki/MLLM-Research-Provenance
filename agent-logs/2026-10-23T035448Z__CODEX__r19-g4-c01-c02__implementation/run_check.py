"""Engineering subprocess receipts; never starts scientific execution."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
name, cwd, *command = sys.argv[1:]
environment = dict(os.environ)
for key in ('PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV'):
    environment.pop(key, None)
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
def git_state():
    head = subprocess.run(['git', '-C', cwd, 'rev-parse', 'HEAD'], text=True, capture_output=True)
    status = subprocess.run(['git', '-C', cwd, 'status', '--porcelain=v1'], text=True, capture_output=True)
    return {'head': head.stdout.strip(), 'status': status.stdout, 'git_exit': head.returncode}
before_git = git_state()
result = subprocess.run(command, cwd=cwd, env=environment, text=True, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
(root / 'evidence' / (name + '.log')).write_text(result.stdout)
receipt = {'argv': command, 'cwd': cwd, 'started_at': started,
           'git_before': before_git, 'git_after': git_state(),
           'completed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'exit_code': result.returncode, 'exit_code_source': 'subprocess.returncode',
           'environment_presence': {key: key in environment for key in
                                    ('PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV')},
           'environment_allowlist': {key: environment[key] for key in
                                    ('CONDA_PREFIX', 'HF_HUB_OFFLINE', 'TRANSFORMERS_OFFLINE')
                                    if key in environment}}
(root / 'evidence' / (name + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
print(result.stdout[-1800:])
sys.exit(result.returncode)
