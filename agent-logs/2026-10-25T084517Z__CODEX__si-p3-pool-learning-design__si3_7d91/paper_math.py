"""Paper-only hypothetical binomial arithmetic, not data analysis or experiment code."""
from pathlib import Path
import math,json
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__CODEX__si-p3-pool-learning-design__si3_7d91')

def binomial(n,p):
 if p==0:return [1.0]+[0.0]*n
 if p==1:return [0.0]*n+[1.0]
 logs=[math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)+k*math.log(p)+(n-k)*math.log1p(-p) for k in range(n+1)]
 vals=[math.exp(x) for x in logs];assert abs(math.fsum(vals)-1)<1e-10
 return vals

def upper_critical(d,alpha):
 # Equal-tail exact two-sided McNemar conditional null, directional positive rejection.
 if d==0:return 1
 probs=binomial(d,.5);s=0.;lo=-1
 for k in range(d//2+1):
  s+=probs[k]
  if s<=alpha/2+1e-15:lo=k
  else:break
 return d-lo if lo>=0 else d+1
crit={alpha:[upper_critical(d,alpha) for d in range(601)] for alpha in (.025,.05)}

def power(n,delta,q):
 assert n==600 and q>=abs(delta)
 pwin=(q+delta)/2;ploss=(q-delta)/2;pd=binomial(n,q)
 result={k:0.0 for k in ['positive_reject_alpha_025','positive_reject_alpha_05','value_guard_probability','reject_025_and_value_guard','reject_05_and_value_guard']}
 min_net=math.ceil(.05*n);max_loss=math.floor(.05*n)
 for d,pdval in enumerate(pd):
  wdist=binomial(d,pwin/q);tails=[0.0]*(d+2)
  for k in range(d,-1,-1):tails[k]=tails[k+1]+wdist[k]
  guard=max(math.ceil((d+min_net)/2),d-max_loss,0)
  tail=lambda k:tails[k] if k<=d+1 else 0.0
  result['value_guard_probability']+=pdval*tail(guard)
  for alpha,label in [(.025,'025'),(.05,'05')]:
   c=crit[alpha][d]
   result['positive_reject_alpha_'+label]+=pdval*tail(c)
   result['reject_'+label+'_and_value_guard']+=pdval*tail(max(c,guard))
 return {'N_eval':n,'true_net_difference':delta,'discordance_probability':q,'true_win_probability':pwin,'true_loss_probability':ploss,'true_gross_harm_within_05':ploss<=.05+1e-12,**result}

def acquisition_cap(n):
 # Balanced d in {5,10,15,20}; paper count, not an executable schedule.
 assert n%24==0
 source=50*n;teacher=2*n;suffix=int((49-12.5)*n)
 return {'planned_tasks':n,'source_model_calls_max':source,'teacher_stage1_calls_max':n,'teacher_stage2_calls_max':n,'P0_suffix_model_calls_max':suffix,'all_model_calls_max':source+teacher+suffix,'source_actions_max':50*n,'prefix_replay_actions_max':int(12.5*n),'teacher_actions_max':n,'suffix_actions_max':suffix,'environment_resets_max':2*n,'reset_inclusive_env_operations_max':102*n,'generated_tokens_max':16*(source+suffix)+56*n}
scenarios=[power(600,d,q) for d,q in [(.05,.05),(.05,.10),(.05,.15),(.05,.20),(.05,.30),(.08,.14),(.10,.16)]]
cap96=acquisition_cap(96);cap480=acquisition_cap(480)
eval600={'tasks':600,'actors':3,'episodes_max':1800,'model_calls_max':90000,'reset_inclusive_env_operations_max':91800,'generated_tokens_max':1440000}
dev60={'tasks':60,'actors_assumed_for_lower_comparison':1,'model_calls_max':3000,'reset_inclusive_env_operations_max':3060}
obj={'scope':'HYPOTHETICAL_PAPER_MATH_ONLY_NO_DATA_OR_POLICY_EVALUATION','assumptions':'i.i.d hypothetical paired trinomial outcomes for a single fixed comparison; q and delta are scenarios, not estimates from R19 or historical rescue yield. Exact conditional equal-tail binomial test is integrated over hypothetical D. No joint A/B/C power claim.','acquisition_96':cap96,'acquisition_480':cap480,'evaluation_600_three_actors':eval600,'development_60_one_actor_if_later_executed':dev60,'480_plus_60dev_plus_600eval_one_dev_actor_upper_counts':{'model_calls_max':cap480['all_model_calls_max']+3000+90000,'reset_inclusive_env_operations_max':cap480['reset_inclusive_env_operations_max']+3060+91800},'hypothetical_single_pair_scenarios':scenarios,'training_count_only':{'new_unique_examples_per_arm':24,'background_unique_examples_per_arm':120,'examples_per_arm':144,'epochs':2,'effective_batch':16,'optimizer_updates_per_arm':18,'new_task_exposures_per_arm':48,'background_task_exposures_per_arm':240,'max_length':2048,'padded_sequence_token_slots_upper_per_arm':144*2*2048,'actual_completion_and_prompt_tokens':'NOT_MEASURED_NO_TOKENIZER'}}
p=OWN/'paper_math.json'
with p.open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
print(json.dumps(obj,indent=2))
