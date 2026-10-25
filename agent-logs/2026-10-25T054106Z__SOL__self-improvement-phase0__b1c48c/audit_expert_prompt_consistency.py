from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib,json
SOURCE=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl')
OUT=Path("/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c")/'independent_expert_dataset_check.json'
def file_sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
before=file_sha(SOURCE)
rows=0; split_rows=Counter(); split_tasks=defaultdict(set); source_splits=Counter(); families=defaultdict(set); prompt_counts=Counter(); prompt_targets=defaultdict(set); prompt_splits=defaultdict(set); errors=Counter(); lengths=[]
with SOURCE.open() as f:
 for line in f:
  r=json.loads(line); rows+=1
  sp=r['dataset_split']; task=r['task_id']; split_rows[sp]+=1; split_tasks[sp].add(task); source_splits[r['source_split']]+=1; families[r['task_family']].add(task)
  ph=r['prompt_sha256']; prompt_counts[ph]+=1; prompt_targets[ph].add((r['target_action_id'],r['target_command'])); prompt_splits[ph].add(sp)
  if hashlib.sha256(r['prompt'].encode()).hexdigest()!=ph:errors['rendered_prompt_hash_mismatch']+=1
  if r['indexed_action_map'].get(r['target_action_id'])!=r['target_command']:errors['target_id_command_map_mismatch']+=1
  if r['completion'].strip()!=r['target_action_id']:errors['completion_target_mismatch']+=1
  if not r['terminal_task_success']:errors['declared_source_not_successful']+=1
  lengths.append(r['tokenizer_length'])
after=file_sha(SOURCE)
splits=sorted(split_tasks)
out={'audit_kind':'stdlib-only existing expert dataset integrity and recorded-label consistency; not re-tokenization/raw expert trajectory validation/policy evaluation','observed_utc':datetime.now(timezone.utc).isoformat(),'source_path':str(SOURCE),'bytes':SOURCE.stat().st_size,'source_sha256_before':before,'source_sha256_after':after,'source_unchanged':before==after,'matches_reported_sha256':before=='c547e8f0c5988b29288f2a097169c7859741b7d4f53f222af31f5e2889d516cf','rows':rows,'rows_per_split':dict(split_rows),'exact_stored_task_ids_per_split':{k:len(v) for k,v in split_tasks.items()},'stored_task_id_intersections':{a+'__'+b:len(split_tasks[a]&split_tasks[b]) for i,a in enumerate(splits) for b in splits[i+1:]},'tasks_per_family':{k:len(v) for k,v in families.items()},'source_splits':dict(source_splits),'retained_repeated_prompt_occurrences':sum(v-1 for v in prompt_counts.values()),'repeated_prompt_groups':sum(v>1 for v in prompt_counts.values()),'prompt_groups_with_conflicting_targets':sum(len(v)>1 for v in prompt_targets.values()),'cross_split_prompt_hash_groups':sum(len(v)>1 for v in prompt_splits.values()),'recorded_tokenizer_length_min':min(lengths),'recorded_tokenizer_length_max':max(lengths),'field_errors':dict(errors),'limitations':['Expert-origin dataset, not own-experience learning data','Exact stored identity intersections only; canonical/global contamination audited separately','Zero target conflicts would not prove observable-state sufficiency or absence of distribution shift','Recorded tokenizer lengths only, no tokenizer/model loaded'],'new_model_environment_calls':0}
OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
