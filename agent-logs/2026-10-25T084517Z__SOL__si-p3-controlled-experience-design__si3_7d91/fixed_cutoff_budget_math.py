from pathlib import Path
import json
OWN=Path(__file__).resolve().parent
assert "si-p3-controlled-experience-design" in str(OWN)
def cap(n):
 assert n%4==0
 cuts=[5,10,15,20];d_sum=n//4*sum(cuts)
 src=50*n;t=2*n;suffix=49*n-d_sum;gen=src+t+suffix;tok=16*(src+suffix)+56*n
 return {"N":n,"preassigned_decisions":cuts,"nominal_cutoff_counts":{str(d):n//4 for d in cuts},"sum_d":d_sum,"source_generations_max":src,"teacher_generations_max":t,"actor_suffix_generations_max":suffix,"all_generations_max":gen,"reset_max":2*n,"source_actions_max":50*n,"replay_actions_max":d_sum,"teacher_actions_max":n,"actor_suffix_actions_max":suffix,"nonreset_actions_max":100*n,"environment_operations_with_resets_max":102*n,"generated_tokens_max":tok,"input_tokens_max_at_guard8192":8192*gen}
acq=[cap(n) for n in [96,384,480]];full=cap(480)
combined={"new_generations_max":full["all_generations_max"]+90000,"new_environment_operations_with_resets_max":full["environment_operations_with_resets_max"]+91800,"new_generated_tokens_max":full["generated_tokens_max"]+1440000,"new_input_tokens_max_at_guard8192":full["input_tokens_max_at_guard8192"]+8192*90000,"software_dev_smoke_training_excluded":True}
out={"status":"PROPOSED_DESIGN_RULE_ARITHMETIC_NOT_EXECUTABLE","rule":"For fixed nominal source order before opening any outcomes, decision d cycles5,10,15,20 at nominal index modulo4. All source positions remain even if early terminal/invalid/unreachable; no choosing alternative d or using leftover call allowance. Exact task call order/seed/runtime still future non-executed attachments.","scope":"source H50 +once Stage1/2 +one teacher action +remaining P0; one replay with0 model calls; source CONTINUE reused","acquisition":acq,"combined_full_acquisition_plus_final600_three_actors":combined,"prior_R19_actual":{"generations":5142,"environment_operations":7949},"actual_new_science":0,"limits":"Input guard8192 is proposed cap below observed40960 model config, not proof all future prompts fit; no truncation. Hardware/device time cap and software-operation budgets must be frozen before release. This tighter budget relies on exact preassigned cutoff balance; prior101N universal caps retained only as conservative draft/reference."}
(OWN/"fixed_cutoff_budget_math.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
