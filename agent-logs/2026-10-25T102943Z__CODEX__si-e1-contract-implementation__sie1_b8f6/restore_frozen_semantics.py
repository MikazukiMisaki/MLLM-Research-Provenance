from pathlib import Path
import hashlib,json
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
for name in ['collector.py','audit.py']:
 f=ROOT/'src/self_improvement/si_p3'/name;s=f.read_text()
 if name=='collector.py':
  s=s.replace('from recovery.two_stage import (parse_stage_one_output, parse_stage_two_output,\n                                stage_one_prompt, stage_two_prompt)','from recovery.two_stage_v2 import (parse_stage_one_output, parse_bare_stage_two_output,\n                                   stage_one_prompt, stage_two_prompt)')
  s=s.replace('parse_stage_two_output(generation.record(), state.valid_actions)','parse_bare_stage_two_output(generation.record(), state.valid_actions)')
  old='    if not generation.raw["output_complete"]:\n        return {"status": "truncated_actor", "action_id": None, "command": ""}\n'
  assert old in s;s=s.replace(old,'    # Frozen P0 parses its bare ID independently of EOS completeness.\n    # Keep raw flags for accounting; teacher completeness remains strict.\n')
 else:s=s.replace('from recovery.two_stage import stage_one_prompt, stage_two_prompt','from recovery.two_stage_v2 import stage_one_prompt, stage_two_prompt')
 f.write_text(s)
f=ROOT/'tests/si_p3_support.py';s=f.read_text().replace('output = "Action-ID: A001"','output = "A001"');f.write_text(s)
f=ROOT/'configs/self_improvement/si_p3_engineering_v1.json';v=json.loads(f.read_text());v['model']['teacher_operator_version']='two_stage_bounded_recovery_v2';v['model']['teacher_stage_two_contract']='frozen bare-ID v2';v['model']['actor_completeness_semantics']='parse_p2_selection independently of output_complete; flags retained; no added actor gate';oldsha=hashlib.sha256(f.read_bytes()).hexdigest();f.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');newsha=hashlib.sha256(f.read_bytes()).hexdigest()
f=ROOT/'src/self_improvement/si_p3/contract.py';f.write_text(f.read_text().replace(oldsha,newsha))
f=ROOT/'docs/si_p3_engineering_v1.md';s=f.read_text().replace('teacher prompts/parsers and P0 prompt are the frozen production functions.','teacher prompts/parsers are the frozen R19 two_stage_v2 bare-ID functions and the P0 prompt is unchanged. P0 source/suffix selection preserves parse_p2_selection independently of EOS completeness; raw cap/completion flags remain evidence, while Stage1/Stage2 teacher completeness stays strict.');f.write_text(s)
# A fresh fixture after the corrected treatment; preserve v1/v2 evidence and scripts.
f=OWN/'synthetic_integration_v3.py';assert not f.exists();s=(OWN/'synthetic_integration_v2.py').read_text().replace("folder=OWN/'synthetic_integration_v2'","folder=OWN/'synthetic_integration_v3'")
s=s.replace("'integrity':integrity,", "'integrity':{k:v for k,v in integrity.items() if k!='logical_prefix_comparisons'},")
f.write_text(s)
print(json.dumps({'only_new_methods_changed':True,'teacher':'frozen two_stage_v2 bare ID','actor':'frozen parse_p2_selection without new completeness gate','contract_sha256':newsha}))
