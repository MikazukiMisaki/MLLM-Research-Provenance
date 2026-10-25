from pathlib import Path
import subprocess,json,hashlib,datetime,sys
OWN=Path(__file__).resolve().parent;assert 'si-p3-controlled-experience-design' in str(OWN)
BASE=Path('/home/lizening/research-notes');PREP=json.loads((OWN/'publication_preparation.json').read_text());receipt={'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':[],'status':'IN_PROGRESS'}
def run(args,ok=(0,)):
 p=subprocess.run(args,cwd=BASE,capture_output=True);r={'argv':args,'actual_returncode':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')};receipt['commands'].append(r)
 if p.returncode not in ok:raise RuntimeError(str(r))
 return p.stdout
sha=lambda b:hashlib.sha256(b).hexdigest()
try:
 intended=PREP['intended_files'];head=run(['git','rev-parse','HEAD']).decode().strip();assert head==PREP['base_sha']
 remote=run(['git','ls-remote','origin','refs/heads/main']).decode().split()[0];assert remote==head
 cached=set(run(['git','diff','--cached','--name-only','-z']).decode().rstrip('\0').split('\0'));assert cached==set(intended),(cached^set(intended))
 run(['git','diff','--cached','--check'])
 for rel in intended:assert sha(run(['git','show',':'+rel]))==sha((BASE/rel).read_bytes()),rel
 for line in (BASE/'FILE_HASHES.sha256').read_text().splitlines():
  h,rel=line.split(maxsplit=1);assert sha((BASE/rel).read_bytes())==h,rel
 run(['git','commit','-m','Document SI-P3 controlled-experience design and independent investment review'])
 commit=run(['git','rev-parse','HEAD']).decode().strip();run(['git','push','origin','main'])
 origin=run(['git','rev-parse','origin/main']).decode().strip();live=run(['git','ls-remote','origin','refs/heads/main']).decode().split()[0];assert commit==origin==live
 verified=[]
 for rel in intended:
  local=(BASE/rel).read_bytes();remote_bytes=run(['git','show','origin/main:'+rel]);assert sha(local)==sha(remote_bytes),rel;verified.append({'path':rel,'bytes':len(local),'sha256':sha(local)})
 assert run(['git','diff','--name-only']).decode().strip()=='';assert run(['git','diff','--cached','--name-only']).decode().strip()==''
 receipt.update({'status':'PUSHED_AND_REMOTE_BYTES_VERIFIED','finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commit':commit,'local_equals_origin_equals_live_remote':True,'remote_verified_intended_files':verified,'root_inventory_entries':len((BASE/'FILE_HASHES.sha256').read_text().splitlines())})
except Exception as e:
 receipt.update({'status':'FAILED_PRESERVED','error':str(e)});(OWN/'post-push-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');raise
(OWN/'post-push-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'commit':receipt['commit'],'remote_verified_intended_files':len(receipt['remote_verified_intended_files']),'root_inventory_entries':receipt['root_inventory_entries']},indent=2))
