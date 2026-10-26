from pathlib import Path
import json,hashlib,subprocess,shutil,time
OWN=Path(__file__).resolve().parent;B=json.loads((OWN/'BINDING.json').read_text());TREE=Path(B['checkout']);OUT=Path(B['external']);DEST=OUT/'relocated_child_bytecode'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
tracked=set((OWN/'tracked_files.stdout').read_bytes().decode().split('\0')[:-1])
caches=[p for p in TREE.rglob('__pycache__') if '.git' not in p.parts]
rows=[]
for cache in sorted(caches):
 relative=cache.relative_to(TREE);files=sorted(p for p in cache.rglob('*') if p.is_file())
 assert all(str(p.relative_to(TREE)) not in tracked for p in files)
 check=subprocess.run(['git','check-ignore',str(relative)],cwd=TREE,capture_output=True)
 assert check.returncode==0,relative
 contents=[{'relative_file':str(p.relative_to(cache)),'size_bytes':p.stat().st_size,'sha256':sha(p)} for p in files]
 destination=DEST/relative;destination.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(cache),str(destination))
 after=[{'relative_file':str(p.relative_to(destination)),'size_bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(destination.rglob('*')) if p.is_file()]
 assert after==contents
 rows.append({'observed_checkout_relative_path':str(relative),'external_destination':str(destination),'git_check_ignore_returncode':check.returncode,'git_check_ignore_stdout':check.stdout.decode().strip(),'all_files_untracked':True,'file_count':len(contents),'size_bytes':sum(x['size_bytes'] for x in contents),'contents_pre_post_identical':True,'files':contents})
remaining=[str(p.relative_to(TREE)) for p in TREE.rglob('__pycache__') if '.git' not in p.parts]
status=subprocess.run(['git','status','--porcelain=v1','--untracked-files=all'],cwd=TREE,capture_output=True)
(OWN/'post_cache_relocation_git_status.stdout').write_bytes(status.stdout);(OWN/'post_cache_relocation_git_status.stderr').write_bytes(status.stderr)
record={'status':'DISCLOSED_TRANSIENT_IGNORED_CACHE_PLACEMENT_DEVIATION_RELOCATED_WITHOUT_RERUN','interpretation':'Main invocation used -I -B and explicit external pytest/cache/tmp roots. Existing isolated subprocesses nevertheless wrote ignored __pycache__ in the private temporary checkout. Never-written-to-checkout is NOT claimed. Only these ignored untracked bytecode caches were subsequently moved outside checkout; tracked source/test bytes and test-result artifacts were not edited. No tests were rerun.','cache_directory_count':len(rows),'cache_file_count':sum(r['file_count'] for r in rows),'cache_total_bytes':sum(r['size_bytes'] for r in rows),'entries':rows,'remaining_checkout_pycache_paths':remaining,'post_relocation_git_status_returncode':status.returncode,'post_relocation_git_status_clean':status.stdout==b''}
(OWN/'CACHE_PLACEMENT_DEVIATION.json').write_text(json.dumps(record,indent=2)+'\n')
summary=json.loads((OWN/'COMPARISON_SUMMARY.json').read_text());summary['cache_placement_deviation']={'record':'CACHE_PLACEMENT_DEVIATION.json','status':record['status'],'observed_directory_count':len(rows),'remaining_checkout_pycache_paths':remaining,'no_test_rerun':True,'post_relocation_git_status_clean':status.stdout==b''}
(OWN/'COMPARISON_SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
with (OWN/'RECORD.md').open('a') as f:f.write('\nCache placement deviation: despite main -I -B and external cache/temp controls, existing isolated subprocesses wrote10 ignored __pycache__ directories inside the private /tmp checkout. These untracked bytecode caches were moved to the external /tmp directory after capture, with file bytes verified unchanged. No tests were rerun. This restores an empty checkout cache set but does not establish that cache files were never transiently written into the checkout. See CACHE_PLACEMENT_DEVIATION.json.\n')
print(json.dumps({'cache_directory_count':len(rows),'cache_file_count':record['cache_file_count'],'cache_bytes':record['cache_total_bytes'],'remaining_checkout_pycache_paths':remaining,'post_relocation_git_status_clean':status.stdout==b''}))
