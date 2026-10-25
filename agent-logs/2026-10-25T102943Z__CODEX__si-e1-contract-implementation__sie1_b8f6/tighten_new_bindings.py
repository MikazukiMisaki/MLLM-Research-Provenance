from pathlib import Path
import hashlib,json,sys
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
sys.path.insert(0,str(ROOT/'src'))
from self_improvement.si_p3.contract import FAMILIES,digest,CONTRACT_FILE_SHA256
manifest=ROOT/'configs/sft/sft_accepted_task_splits.json';b=manifest.read_bytes()
manifest_sha=hashlib.sha256(b).hexdigest();assert manifest_sha=='9c374fafdcc7d7db77e878d23e852a0ec55eedcc3886cb0cebe7491d67e564e5'
items=json.loads(b)['pools']['train']
metadata=sorted([{'task_id':x['task_id'],'family':x['task_id'].split('-',1)[0]} for x in items if x['task_id'].split('-',1)[0] in FAMILIES],key=lambda x:(x['family'],x['task_id']))
assert len(metadata)==895
identity_sha=digest(metadata)
f=ROOT/'src/self_improvement/si_p3/contract.py';s=f.read_text();s+=f'\nEXPERT_TRAIN_MANIFEST_SHA256 = "{manifest_sha}"\nEXPERT_TRAIN_FIVE_IDENTITY_SHA256 = "{identity_sha}"\n';f.write_text(s)
f=ROOT/'src/self_improvement/si_p3/data.py';s=f.read_text().replace('from .contract import (ADOPTION_QUOTAS,','from .contract import (EXPERT_TRAIN_FIVE_IDENTITY_SHA256, integer, ADOPTION_QUOTAS,');needle='    selected = []\n    for family in FAMILIES:';replacement='    if evidence_class == "historical":\n        require(digest(sorted(expert_train_tasks, key=lambda x: (x["family"], x["task_id"]))) ==\n                EXPERT_TRAIN_FIVE_IDENTITY_SHA256, "complete original expert_train identity anchor")\n    selected = []\n    for family in FAMILIES:';assert needle in s;s=s.replace(needle,replacement);s=s.replace('require(row["task_family"] == family, "background task family")','require(row["task_family"] == family and integer(row["step_index"]), "background task family/index")');f.write_text(s)
f=ROOT/'configs/self_improvement/si_p3_engineering_v1.json';v=json.loads(f.read_text());v['background']['expert_train_manifest_sha256']=manifest_sha;v['background']['five_family_expert_train_identity_sha256']=identity_sha;f.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');newsha=hashlib.sha256(f.read_bytes()).hexdigest()
f=ROOT/'src/self_improvement/si_p3/contract.py';s=f.read_text().replace(CONTRACT_FILE_SHA256,newsha);f.write_text(s)
f=ROOT/'src/self_improvement/si_p3/audit.py';s=f.read_text();old='"physical": dict(self.physical), "components": dict(self.components), "plan_sha256": run["plan_sha256"]}'
new='"physical": dict(self.physical), "components": dict(self.components), "plan_sha256": run["plan_sha256"],\n                "logical_prefix_comparisons": [logical_costs(row, self.index) for row in run["slots"]]}'
assert old in s;s=s.replace(old,new)
s+=r'''


def logical_costs(row: Mapping[str, Any], event_index: Mapping[str, Any]) -> dict[str, Any]:
    """Receipt cost algebra only; shared CONTINUE refs never incur another debit."""
    def cost(generations: list[str], steps: list[str]) -> dict[str, int]:
        raw = [event_index[e]["payload"]["data"]["raw"] for e in generations]
        return {"generations": len(raw), "environment_steps": len(steps),
                "input_tokens": sum(g["input_tokens"] for g in raw),
                "generated_tokens": sum(g["generated_tokens"] for g in raw)}
    branch = row.get("branch")
    if branch is None:
        return {"slot_key": row["slot_key"], "CONTINUE": None, "K1": None, "teacher_attempt": None}
    attempt = cost([branch["stage_one"], branch["stage_two"]],
                   [branch["teacher_step"]] if branch["teacher_step"] else [])
    policy = None
    if branch["teacher_step"] is not None:
        policy = cost([branch["stage_one"], branch["stage_two"]] + branch["suffix"]["generations"],
                      [branch["teacher_step"]] + branch["suffix"]["steps"])
    return {"slot_key": row["slot_key"],
            "CONTINUE": cost(branch["source_suffix_generation_refs"], branch["source_suffix_step_refs"]),
            "K1": policy, "teacher_attempt": attempt,
            "physical_debit_added_by_this_function": 0, "reset_and_prefix_replay_in_policy_cost": False}
''';f.write_text(s)
print(json.dumps({'historical_background_tasks':len(metadata),'metadata_sha256':identity_sha,'contract_sha256':newsha}))
