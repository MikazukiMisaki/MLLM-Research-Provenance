"""Read only the201 manifest-selected files; emit locations/categories, never payloads."""
from pathlib import Path
from collections import Counter
import hashlib,json,re

OWN=Path(__file__).resolve().parent
ROOT=Path("/home/lizening/research-notes/agent-logs/2026-10-26T102514Z__CODEX__si-s01-source-only-implementation__f1a52e8c")
MANIFEST=ROOT/"PUBLICATION_MANIFEST.json"
EXPECTED_SHA="3b14c027fb95bd23a9e4acc7c8b5bb3f4393e26c1153a69b177e9dc1bd0c9eaa"
before=hashlib.sha256(MANIFEST.read_bytes()).hexdigest();assert before==EXPECTED_SHA
doc=json.loads(MANIFEST.read_bytes());selected=doc["files"]
assert len(selected)==201 and len({x["relative_path"] for x in selected})==201
patterns={
 "private_key_header":re.compile(r"-----BEGIN (?:OPENSSH |RSA |EC |DSA |ENCRYPTED )?PRIVATE KEY-----"),
 "openai_token":re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}\b"),
 "github_token":re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
 "aws_access_key":re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
 "google_api_key":re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
 "google_oauth_token":re.compile(r"\bya29\.[0-9A-Za-z._-]{20,}\b"),
 "slack_token":re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{20,}\b"),
 "bearer_value":re.compile(r"\bBearer[ \t]+[A-Za-z0-9_.+/=-]{16,}",re.I),
 "credential_url":re.compile(r"https?://[^\s/\"'<>:@]+:[^\s\"'<>@]+@",re.I),
 "secret_assignment":re.compile(r"\b(?:api_key|access_token|refresh_token|client_secret|password|passwd|HF_TOKEN|HUGGING_FACE_HUB_TOKEN|OPENAI_API_KEY|GITHUB_TOKEN)[\"']?\s*[:=]\s*[\"']?([^\"'\s,;}{]{8,})",re.I),
 "jwt_shape":re.compile(r"\beyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\b"),
}
forbidden_extensions={".safetensors",".bin",".pt",".pth",".ckpt",".onnx",".npy",".npz",".arrow",".parquet",".pkl",".pickle"}
sensitive_keys={"prompt","public_prompt","rendered_prompt","observation","result_observation","initial_observation","goal","task_text","raw_output"}
known_small={"A000","bad","look","public","goal","room","fixture","synthetic",""}
category_counts=Counter();records=[];credential_hits=[];payload_candidates=[];numeric_arrays=[]
def category(rel):
 p=Path(rel)
 if p.suffix==".jsonl":return "selected_synthetic_raw_examples"
 if p.suffix in {".patch",".stat"}:return "source_diff_or_diff_stat"
 if p.suffix==".py":return "provenance_software_tools"
 if p.suffix==".md":return "handoff_scope_or_report_narrative"
 if p.suffix in {".xml",".stdout",".stderr"} or "reports.json" in rel:return "software_test_capture"
 if p.suffix==".sha256" or any(t in p.name for t in ("INVENTORY","INDEX","HASHES","BINDINGS","COMPARISON","SCOPE","EQUALITY")):return "metadata_hash_inventory_or_binding"
 return "software_receipt_or_control_metadata"
def walk(obj,path,stats,rel):
 if isinstance(obj,dict):
  for key,value in obj.items():
   location=path+"."+key
   if isinstance(value,str) and key in sensitive_keys:
    stats["payload_named_string_fields"]+=1
    low=value.lower()
    if "synthetic" in low or "fixture" in low:
     stats["explicit_synthetic_payload_fields"]+=1
    elif value in known_small or len(value)<=12:
     stats["short_boundary_literals"]+=1
    else:
     payload_candidates.append({"path":rel,"json_key_location":location,"field":key,"characters":len(value),"value_redacted":True})
   walk(value,location,stats,rel)
 elif isinstance(obj,list):
  if len(obj)>4096 and all(type(x) in (int,float) for x in obj):
   numeric_arrays.append({"path":rel,"json_key_location":path,"length":len(obj)})
  for i,value in enumerate(obj):walk(value,path+"["+str(i)+"]",stats,rel)
for entry in selected:
 rel=entry["relative_path"];p=ROOT/rel
 assert str(p)==entry["path"] and p.resolve().is_relative_to(ROOT.resolve())
 assert p.is_file() and not p.is_symlink()
 b=p.read_bytes();assert len(b)==entry["bytes"] # Parent already independently verified all201 hashes.
 rec={"relative_path":rel,"bytes":len(b),"category":category(rel),"manifest_sha256":entry["sha256"]}
 category_counts[rec["category"]]+=1
 rec["model_or_cache_extension"]=p.suffix.lower() in forbidden_extensions
 rec["nul_bytes"]=b.count(b"\0")
 rec["binary_container_magic"]=any(b.startswith(m) for m in (b"PK\x03\x04",b"\x1f\x8b",b"\x80\x04",b"\x93NUMPY"))
 try:text=b.decode("utf-8");rec["strict_utf8"]=True
 except UnicodeDecodeError:rec["strict_utf8"]=False;text=""
 for name,pat in patterns.items():
  hits=list(pat.finditer(text))
  if hits:
   credential_hits.append({"path":rel,"pattern":name,"count":len(hits),"lines":sorted({text.count("\n",0,m.start())+1 for m in hits}),"matched_values_redacted":True})
 stats=Counter()
 if p.suffix==".json":
  try:walk(json.loads(text),"$",stats,rel);rec["json_valid"]=True
  except json.JSONDecodeError:rec["json_valid"]=False
 elif p.suffix==".jsonl":
  stats["jsonl_nonempty_rows"]=0
  for i,line in enumerate(text.splitlines(),1):
   if line.strip():walk(json.loads(line),"$line"+str(i),stats,rel);stats["jsonl_nonempty_rows"]+=1
 rec["structured_payload_statistics"]=dict(stats)
 records.append(rec)
after=hashlib.sha256(MANIFEST.read_bytes()).hexdigest();assert after==before
report={"mode":"READ_ONLY_SELECTED201_CONTENT_SCREEN_NOT_PROJECT_VALIDATOR","manifest_path":str(MANIFEST),
 "manifest_sha256_before":before,"manifest_sha256_after":after,"manifest_unchanged":after==before,
 "selected_count":len(records),"selected_declared_bytes":sum(r["bytes"] for r in records),
 "category_counts":dict(category_counts),"max_selected_file_bytes":max(r["bytes"] for r in records),
 "files_over_1MiB":[r["relative_path"] for r in records if r["bytes"]>1048576],
 "files_over_256KiB":[{"path":r["relative_path"],"bytes":r["bytes"]} for r in records if r["bytes"]>262144],
 "non_utf8_or_binary":[r["relative_path"] for r in records if not r["strict_utf8"] or r["nul_bytes"] or r["binary_container_magic"]],
 "selected_model_dataset_cache_extensions":[r["relative_path"] for r in records if r["model_or_cache_extension"]],
 "credential_pattern_findings":credential_hits,"ambiguous_structured_payload_fields":payload_candidates,
 "large_numeric_arrays":numeric_arrays,"selected_files":records,
 "unselected_fixture_content_opened":False,"hash_all_fixtures_repeated":False}
(OWN/"CONTENT_SCREEN.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:report[k] for k in ("selected_count","selected_declared_bytes","category_counts","max_selected_file_bytes","files_over_1MiB","files_over_256KiB","non_utf8_or_binary","selected_model_dataset_cache_extensions","credential_pattern_findings","ambiguous_structured_payload_fields","large_numeric_arrays")},ensure_ascii=False))

