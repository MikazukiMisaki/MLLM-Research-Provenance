"""Actual subprocess receipts for SI-P1 read-only audit and own document writes."""
import datetime,json,subprocess,sys
from pathlib import Path
OWN=Path(__file__).resolve().parent
label,cwd,*argv=sys.argv[1:]
if not label.replace('_','').isalnum():raise SystemExit('bad label')
allowed={'git','rg','cat','sha256sum','ls','stat'}
if argv[0] not in allowed and not (argv[0]=='python' and Path(argv[1]).resolve()==OWN/'eleven_audit.py'):raise SystemExit('not allowed')
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(argv,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=OWN/(label+'.log');log.write_text(r.stdout)
receipt={'argv':argv,'cwd':cwd,'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_returncode':r.returncode,'returncode_source':'subprocess.returncode','log':str(log),'scope':'SI_P1_EXISTING_EVIDENCE_ONLY'}
(OWN/(label+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
with (OWN/'commands.log').open('a') as stream:stream.write(json.dumps(receipt)+'\n')
print(json.dumps(receipt));print(r.stdout[:24000]);raise SystemExit(r.returncode)
