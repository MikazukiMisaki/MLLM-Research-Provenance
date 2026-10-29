import gzip,hashlib,io,json,os,re,tarfile
from pathlib import Path
ROOT=Path('/home/lizening/research-notes/agent-logs')
OUT=Path(__file__).parent
DIRS=['2026-10-29T231522Z__CODEX__si-next-data-isolation-readonly__f2a1','2026-10-29T231518Z__CODEX__si-u1-power-feasibility__independent','2026-10-29T232019Z__CODEX__si-u1-small-n-power__independent','2026-10-29T232200Z__CODEX__si-power-independent-critique','2026-10-29T233600Z__CODEX__si-small-n-independent-review','2026-10-29T233000Z__CODEX__si-pool-independent-critique','2026-10-29T231600Z__CODEX__si-next-readonly-budget']
def sha(data):return hashlib.sha256(data).hexdigest()
payload=[]
for d in DIRS:
 for p in sorted((ROOT/d).iterdir()):
  if not p.is_file() or p.is_symlink() or p.name.startswith('.'):continue
  data=p.read_bytes();payload.append((p, 'sources/'+d+'/'+p.name,data))
for rel,expect in [('2026-10-29T232200Z__CODEX__si-next-feasibility-decision/SI_NEXT_FEASIBILITY_DECISION.md','a31c23b0afea5804a68fb2eec2138e37979a4e30ed3d06b5cfbc2c4517367f4a'),('2026-10-29T234100Z__CODEX__si-feasibility-independent-acceptance/INDEPENDENT_ACCEPTANCE.json','201106e2573c154c67d783e863248149588716a7304c7076d732fe26016de2a5')]:
 p=ROOT/rel;data=p.read_bytes();assert sha(data)==expect;payload.append((p,'sources/'+rel,data))
assert len(payload)>40
# Reject likely credential material, without printing any matched bytes.
patterns=[re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),re.compile(rb'gh[pousr]_[A-Za-z0-9_]{30,}'),re.compile(rb'AKIA[0-9A-Z]{16}')]
hits=sum(bool(pat.search(data)) for _,_,data in payload for pat in patterns)
if hits:raise RuntimeError('credential pattern match in selected sources')
manifest={'schema':'SI_NEXT_PRIVATE_PUBLICATION_V1','privacy':'PRIVATE_REPOSITORY_ONLY; raw task identifiers included; no task payload, model weights, or environment data', 'note':'Copied exact bytes; original records remain unchanged; source byte hashes are as captured before archive and verified again after construction. Historical records and correction are additive.', 'source_files':[{'source':str(p),'member':name,'bytes':len(data),'sha256':sha(data)} for p,name,data in payload], 'secret_patterns_matches':0}
archive=OUT/'si_next_readonly_evidence_v2.tar.gz'
with archive.open('xb') as raw:
 with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0,filename='') as gz:
  with tarfile.open(fileobj=gz,mode='w|') as tar:
   for _,name,data in payload:
    info=tarfile.TarInfo(name);info.size=len(data);info.mode=0o600;info.mtime=0;info.uid=info.gid=0;info.uname=info.gname='';tar.addfile(info,io.BytesIO(data))
assert all(sha(p.read_bytes())==sha(data) for p,_,data in payload)
with tarfile.open(archive,'r:gz') as tar:
 members=tar.getmembers();assert len(members)==len(payload)
 for (_,name,data),m in zip(payload,members):
  assert m.isfile() and m.name==name and sha(tar.extractfile(m).read())==sha(data)
manifest['archive']={'path':archive.name,'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'members_verified':len(payload)}
mp=OUT/'PUBLICATION_MANIFEST_V2.json';mp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');os.chmod(mp,0o600);os.chmod(archive,0o600)
print(json.dumps({'members':len(payload),'archive_bytes':archive.stat().st_size,'archive_sha256':sha(archive.read_bytes()),'manifest_sha256':sha(mp.read_bytes()),'credential_pattern_matches':0},sort_keys=True))
