from pathlib import Path,PurePosixPath
import json,hashlib,tarfile,re,time
root=Path(__file__).resolve().parent;luna=Path('/home/lizening/research-notes/agent-logs/2026-10-27T001713Z__LUNA__si-s01-source-preflight__f96b86f3/live');report=json.load(open(luna/'LIVE_RESULT.json'));manifest=json.load(open(luna/'RAW_ARCHIVE_MEMBERS.json'));archive=Path(report['raw_archive']['path']);a=json.load(open(root/'INDEPENDENT_RESULT_REVIEW.json'));ctx=json.load(open('/tmp/si-s01-independent-result-review-context.json'));rawroot=Path(ctx['source_output'])
def fh(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
assert archive.stat().st_size==17608129 and fh(archive)=='474a9264bc483b2c641842478f5dcd8287e8d01a60a764c8dd84d892a922ef0a';assert manifest['member_count']==len(manifest['members'])==41 and not manifest['input_dataset_payload_included'] and not manifest['model_weights_adapters_or_cache_included']
spec={r['archive_path']:r for r in manifest['members']};assert len(spec)==41;rows=[];hits=[];raw_names=set();patterns=[re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),re.compile(rb'\bgh[pousr]_[A-Za-z0-9]{30,}\b'),re.compile(rb'\bgithub_pat_[A-Za-z0-9_]{40,}\b'),re.compile(rb'\bhf_[A-Za-z0-9]{30,}\b'),re.compile(rb'\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b')]
with tarfile.open(archive,'r|gz') as tf:
 for m in tf:
  safe=PurePosixPath(m.name);assert m.isfile() and not safe.is_absolute() and '..' not in safe.parts and m.name in spec
  item=spec.pop(m.name);original=Path(item['original_path']);assert original.is_file() and not original.is_symlink();assert m.size==item['bytes'] and m.mtime==0 and m.uid==m.gid==0 and m.uname==m.gname==''
  if original.parent==rawroot:
   assert original.name in a['original_files_before'];expected=a['original_files_before'][original.name];assert item['sha256_before']==expected['sha256'] and m.size==expected['bytes'];raw_names.add(original.name)
  else:
   assert (original.is_relative_to(Path('/home/lizening/research-notes/agent-logs')) and m.size<2*1024**2) or original==rawroot.parent/'raw.launch_claim.json' or original==rawroot.parent/'control/source_preflight_receipt.json'
  assert original.name not in ('game.tw-pddl','traj_data.json') and original.suffix not in ('.safetensors','.pt','.pth','.ckpt')
  h=hashlib.sha256();n=0;tail=b''
  with tf.extractfile(m) as f:
   for b in iter(lambda:f.read(1024*1024),b''):
    h.update(b);n+=len(b);window=tail+b
    if any(p.search(window) for p in patterns):hits.append(m.name)
    tail=window[-256:]
  assert n==m.size and h.hexdigest()==item['sha256_before']==fh(original)
  rows.append({'member':m.name,'original_path':str(original),'bytes':n,'sha256':h.hexdigest(),'independent_streamed_roundtrip_matches':True})
assert not spec and not hits and len(rows)==41 and raw_names==set(a['original_files_before'])
with archive.open('rb') as f:header=f.read(10)
assert header[:3]==b'\x1f\x8b\x08' and int.from_bytes(header[4:8],'little')==0
result={'schema':'ROOT_INDEPENDENT_RAW_SOURCE_ARCHIVE_CONTENT_REVIEW_V1','decision':'PASS_COMPLETE_ORIGINAL_BYTES_SAFE_FOR_EXPLICIT_PUBLICATION','archive':{'path':str(archive),'bytes':archive.stat().st_size,'sha256':fh(archive)},'original_raw_output_files_covered':len(raw_names),'archive_members_streamed_and_rehashed':len(rows),'members':rows,'targeted_credential_pattern_matches':0,'dataset_input_or_model_weights_adapter_cache_payload_included':False,'regular_safe_relative_members_only':True,'normalized_tar_headers_and_gzip_timestamp_valid':True,'raw_hashes_match_prior_independent_result_audit':True,'publication_size_review':'17.6MB exceeds10MB automaticcommit threshold, so coordinator explicitly inspected content/memberpurpose/completebytes/credentialscan. This is compact lossless raw experimental evidence for authorized collection, below50MB; publish this one selected archive, not raw474MB or arbitrary files.','new_model_environment_CUDA_generation_calls':0}
(root/'RAW_ARCHIVE_INDEPENDENT_REVIEW.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'decision':result['decision'],'archive_bytes':archive.stat().st_size,'members_verified':len(rows),'all9raw_output_files_covered':len(raw_names),'credential_matches':len(hits),'originals_unchanged':True}))
