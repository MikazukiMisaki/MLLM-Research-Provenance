"""SI-P0 audit process receipts. Not a scientific runner."""
import datetime
import json
from pathlib import Path
import subprocess
import sys

OWN = Path(__file__).resolve().parent
name, cwd, *argv = sys.argv[1:]
if not name.replace('_', '').replace('-', '').isalnum():
    raise ValueError('simple receipt name required')
allowed = {'git', 'rg', 'cat', 'ls', 'stat', 'sha256sum'}
if Path(argv[0]).name not in allowed:
    if len(argv) < 2 or Path(argv[1]).resolve() != OWN / 'si_p0_inventory_audit.py':
        raise ValueError('only basic read commands and own pure-stdlib audit script allowed')
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
result = subprocess.run(argv, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(OWN / (name + '.log')).write_text(result.stdout)
receipt = {'argv': argv, 'cwd': cwd, 'started_at_utc': started,
           'completed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'exit_code': result.returncode, 'exit_code_source': 'subprocess.returncode',
           'log': str(OWN / (name + '.log')), 'mode': 'SI_P0_EXISTING_RECORD_AUDIT_ONLY'}
(OWN / (name + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
with (OWN / 'commands.log').open('a') as stream:
    stream.write(json.dumps(receipt, sort_keys=True) + '\n')
print(json.dumps(receipt))
print(result.stdout[:17000])
sys.exit(result.returncode)
