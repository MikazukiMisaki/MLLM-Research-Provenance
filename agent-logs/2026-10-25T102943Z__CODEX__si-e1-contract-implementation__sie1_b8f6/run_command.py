"""SI-E1 provenance-only command recorder; never import old audit scripts."""
from pathlib import Path
import datetime,json,subprocess,sys,time
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
label,cwd,*argv=sys.argv[1:]
assert label.replace('_','').replace('-','').isalnum()
assert argv
folder=OWN/'receipts';folder.mkdir(exist_ok=True)
assert not (folder/(label+'.json')).exists(), 'never overwrite receipt'
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
p=subprocess.run(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(folder/(label+'.stdout')).write_bytes(p.stdout);(folder/(label+'.stderr')).write_bytes(p.stderr)
r={'argv':argv,'cwd':cwd,'started_utc':start,'elapsed_monotonic_seconds':time.monotonic()-t,'returncode':p.returncode,'stdout':str(folder/(label+'.stdout')),'stderr':str(folder/(label+'.stderr'))}
(folder/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r));sys.stdout.flush();sys.stdout.buffer.write(p.stdout);sys.stderr.buffer.write(p.stderr)
sys.exit(p.returncode)
