import gzip,hashlib,json,tarfile
from pathlib import Path
O=Path(__file__).resolve().parent;manifest=json.loads((O/'COPY_MANIFEST.json').read_bytes());rel=[r['path'] for r in manifest['files']]+['COPY_MANIFEST.json','INDEPENDENT_COST_RECOUNT.json','RECORD.md'];archive=O/'si_m1_live_raw.tar.gz'
def sha(b):return hashlib.sha256(b).hexdigest()
with archive.open('xb') as out:
 with gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0) as gz:
  with tarfile.open(fileobj=gz,mode='w',format=tarfile.PAX_FORMAT) as tar:
   for name in sorted(rel):
    path=O/name;info=tarfile.TarInfo(name);info.size=path.stat().st_size;info.mode=0o600;info.uid=info.gid=0;info.uname=info.gname='';info.mtime=0
    with path.open('rb') as source:tar.addfile(info,source)
rows=[]
with tarfile.open(archive,'r:gz') as tar:
 names=tar.getnames();assert names==sorted(rel)
 for member in tar.getmembers():
  data=tar.extractfile(member).read();local=(O/member.name).read_bytes();assert data==local
  rows.append({'path':member.name,'bytes':len(data),'sha256':sha(data)})
result={'schema':'SI_M1_RAW_ARCHIVE_VERIFICATION_V1','archive':'si_m1_live_raw.tar.gz','archive_bytes':archive.stat().st_size,'archive_sha256':sha(archive.read_bytes()),'members':rows,'member_count':len(rows),'all_member_bytes_match':True}
(O/'ARCHIVE_VERIFY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('archive','archive_bytes','archive_sha256','member_count','all_member_bytes_match')},sort_keys=True))
