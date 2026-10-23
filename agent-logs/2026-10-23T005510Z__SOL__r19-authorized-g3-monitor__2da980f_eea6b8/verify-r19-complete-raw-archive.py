import pathlib,subprocess,hashlib,json,tarfile,datetime,io
repo=pathlib.Path('/home/lizening/research-notes')
p=pathlib.Path(pathlib.Path('/tmp/r19-live-monitor-path.txt').read_text().strip())
raw=repo/'agent-logs/2026-10-23T024938Z__LUNA__r19-g3-raw-upload__2da980f'
source_root=pathlib.Path('/home/lizening/wt-r19-recovery-duration-v1')
def digest(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(repo),*args]).decode().strip()
commit=git('rev-parse','HEAD'); assert git('rev-parse','origin/main')==commit
assert git('ls-remote','origin','refs/heads/main').split()[0]==commit
manifest=json.loads((raw/'archive_manifest.json').read_text())
archive=raw/manifest['archive']; rel=str(archive.relative_to(repo))
remote=subprocess.check_output(['git','-C',str(repo),'show',f'{commit}:{rel}'])
assert digest(remote)==digest(archive.read_bytes())==manifest['archive_sha256']
inv=json.loads((raw/'archive_member_inventory.json').read_text()); expected={x['path']:x for x in inv['members']}
verified=[]
with tarfile.open(fileobj=io.BytesIO(remote),mode='r:gz') as tar:
 all_members=tar.getmembers(); assert all(x.isfile() or x.isdir() for x in all_members)
 for x in all_members: assert not pathlib.PurePosixPath(x.name).is_absolute() and '..' not in pathlib.PurePosixPath(x.name).parts
 members=[x for x in all_members if x.isfile()]
 assert {x.name for x in members}==set(expected)
 for member in members:
  assert not pathlib.PurePosixPath(member.name).is_absolute() and '..' not in pathlib.PurePosixPath(member.name).parts
  b=tar.extractfile(member).read(); e=expected[member.name]
  original=(source_root if member.name.startswith('artifacts/') else repo)/member.name
  assert len(b)==e['bytes'] and digest(b)==e['sha256']==digest(original.read_bytes())
  verified.append({'path':member.name,'bytes':len(b),'sha256':digest(b)})
output=source_root/'artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z'
expected_output_files={str(x.relative_to(source_root)) for x in output.rglob('*') if x.is_file()}
assert expected_output_files=={x for x in expected if x.startswith('artifacts/')}
assert (raw/'source_sha256.before.txt').read_bytes()==(raw/'source_sha256.after.txt').read_bytes()
metadata={}
for f in raw.rglob('*'):
 if not f.is_file() or f.name=='post-push-receipt.json':continue
 path=str(f.relative_to(repo)); b=subprocess.check_output(['git','-C',str(repo),'show',f'{commit}:{path}'])
 assert digest(b)==digest(f.read_bytes()); metadata[path]=digest(b)
result={'status':'PASS_INDEPENDENT_REMOTE_ARCHIVE_AND_ALL_ORIGINAL_MEMBERS_BYTE_VERIFICATION',
 'verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'provenance_commit':commit,
 'local_HEAD_equals_origin_and_live_remote_main':True,'archive_repository_path':rel,'archive_sha256':digest(remote),'archive_bytes':len(remote),
 'complete_original_scientific_output_file_count':len(expected_output_files),'archive_member_count':len(verified),
 'member_sha256_and_size_match_originals':True,'no_unsafe_paths_or_symlinks':True,'before_and_after_source_hash_lists_identical':True,
 'remote_addendum_file_sha256':metadata,'members':verified,'new_model_environment_preflight_G4_calls':0}
(p/'remote_raw_archive_independent_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('members','remote_addendum_file_sha256')},indent=2))
