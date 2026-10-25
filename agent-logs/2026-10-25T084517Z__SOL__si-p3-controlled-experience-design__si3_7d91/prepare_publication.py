from pathlib import Path
import subprocess,json,hashlib,re,datetime
OWN=Path(__file__).resolve().parent;assert 'si-p3-controlled-experience-design' in str(OWN)
BASE=Path('/home/lizening/research-notes');S=json.loads((OWN/'START_STATE.json').read_text());DIRS=[Path(v) for v in S['directories'].values()]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def cmd(args):
 p=subprocess.run(args,cwd=BASE,capture_output=True,text=True);assert p.returncode==0,(args,p.stdout,p.stderr);return p.stdout
assert cmd(['git','rev-parse','HEAD']).strip()==S['provenance_start']
assert cmd(['git','diff','--name-only']).strip()==''
assert cmd(['git','diff','--cached','--name-only']).strip()==''
files=sorted(p for d in DIRS for p in d.rglob('*') if p.is_file() and p.name!='post-push-receipt.json' and '__pycache__' not in p.parts)
assert all(p.stat().st_size<=1000000 for p in files)
patterns={'github_token':r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b','openai_key':r'\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b','private_key':r'-----BEGIN (?:OPENSSH |RSA |EC |DSA )?PRIVATE KEY-----'}
findings=[]
for p in files:
 text=p.read_text(errors='replace')
 for name,pat in patterns.items():
  if re.search(pat,text):findings.append({'path':str(p.relative_to(BASE)),'pattern':name})
assert not findings,findings
(OWN/'secret_scan.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'all intended new task files only; targeted credential/private key patterns; no claim exhaustive detection','patterns':list(patterns),'scanned_file_count':len(files),'matches':findings,'no_weight_adapter_cache_environment_task_payload_training_dataset_files':True},indent=2)+'\n')
(OWN/'COMPACT_PUBLICATION_SCOPE.md').write_text('''# Publication scope

Only the three SI-P3 task directories, their own three INDEX rows, and rolling root FILE_HASHES inventory are intended. Identity/hash/family partition metadata is included to audit isolation. It is not a training dataset and contains no task payload, observations, model prompts, generated training rows, raw G3 ledger, weights, adapters or cache. Each new file is below1MB. Original drafts/error receipts and append-only corrections are retained; source-root and path/receipt exceptions are explicitly adjudicated by the independent review. No unrelated untracked historical fixture is included.

Targeted credential scan is a limited pattern check, not a universal secrecy proof. Scientific Git trees/refs and four raw G3 hashes remain unchanged. FILE_HASHES is a rolling inventory; task author frozen inventories retain their historical byte bindings. Final exact remote verification is recorded in ignored post-push-receipt.json and user response.
''')
idx=BASE/'INDEX.md';old=idx.read_text();assert 'si-p3-controlled-experience-design__si3_7d91/RECORD.md' not in old
rows=[('SOL','SI-P3 controlled new-experience protocol and independent investment review','DESIGN_REVIEWED_WITH_LIMITS;96candidate only;fullcampaign NO_GO;0science;5142/7949unchanged',S['directories']['root']),('CODEX / Sol Research','SI-P3 common-pool learning dose and five-family amendment','DESIGN_ONLY;fivefamily96;24new+S120;18updates proposed;no science',S['directories']['sol']),('LUNA','SI-P3 identity partitions and physical budget design','METADATA_ONLY;1139identities;old draft/receipt/path exceptions preserved+coordinator corrected;no science',S['directories']['luna'])]
with idx.open('a') as f:
 for owner,title,status,path in rows:f.write(f'| 2026-10-25 08:45:17 | {owner} | {title} | {status} | analyzer85cbb923 / G3source2da980f unchanged | [RECORD.md]({Path(path).relative_to(BASE)}/RECORD.md) |\n')
# preparation describes paths only, not own hash; inventory subsequently binds every intended byte.
prep=OWN/'publication_preparation.json'
prep.write_text(json.dumps({'status':'PREPARED_NOT_YET_COMMITTED_OR_PUSHED','base_sha':S['provenance_start'],'directories':S['directories'],'intended_files':[],'tracked_shared_changes':['INDEX.md','FILE_HASHES.sha256']},indent=2)+'\n')
allnew=sorted(p for d in DIRS for p in d.rglob('*') if p.is_file() and p.name!='post-push-receipt.json' and '__pycache__' not in p.parts)
# Root task inventory includes its preparation/helper and all coordinator records, excludes itself only.
rootfiles=sorted(p for p in OWN.rglob('*') if p.is_file() and p.name not in ['FILE_HASHES.sha256','post-push-receipt.json'] and '__pycache__' not in p.parts)
(OWN/'FILE_HASHES.sha256').write_text(''.join(f'{sha(p)}  {p.relative_to(OWN)}\n' for p in rootfiles))
allnew=sorted(p for d in DIRS for p in d.rglob('*') if p.is_file() and p.name!='post-push-receipt.json' and '__pycache__' not in p.parts)
intended=sorted({str(p.relative_to(BASE)) for p in allnew}|{'INDEX.md','FILE_HASHES.sha256'})
q=json.loads(prep.read_text());q['intended_files']=intended;q['new_file_count']=len(allnew);q['new_bytes_before_inventories']=sum(p.stat().st_size for p in allnew);prep.write_text(json.dumps(q,indent=2)+'\n')
# preparation changed: refresh coordinator manifest once, then root rolling inventory.
rootfiles=sorted(p for p in OWN.rglob('*') if p.is_file() and p.name not in ['FILE_HASHES.sha256','post-push-receipt.json'] and '__pycache__' not in p.parts)
(OWN/'FILE_HASHES.sha256').write_text(''.join(f'{sha(p)}  {p.relative_to(OWN)}\n' for p in rootfiles))
tracked=cmd(['git','ls-files','-z']).split('\0');tracked={x for x in tracked if x};full=sorted((tracked|set(intended))-{'FILE_HASHES.sha256'})
assert all((BASE/x).is_file() for x in full)
(BASE/'FILE_HASHES.sha256').write_text(''.join(f'{sha(BASE/x)}  {x}\n' for x in full))
cp=subprocess.run(['git','check-ignore','--stdin'],cwd=BASE,input='\n'.join(intended)+'\n',capture_output=True,text=True);assert cp.returncode==1 and not cp.stdout,(cp.returncode,cp.stdout)
print(json.dumps({'new_files':len(allnew),'intended_paths':len(intended),'root_inventory_entries':len(full),'task_sizes_bytes':{str(d.relative_to(BASE)):sum(p.stat().st_size for p in d.rglob('*') if p.is_file() and p.name!='post-push-receipt.json') for d in DIRS},'secret_matches':findings,'publication':'NOT_YET_COMMITTED_OR_PUSHED'},indent=2))
