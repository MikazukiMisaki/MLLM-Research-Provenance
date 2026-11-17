import copy,sys
sys.path.insert(0,'/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-budget-completeness__private')
from budget_contract import NEW_MAX,validate_budget,BudgetError
from test_budget_contract import example,values
assert NEW_MAX=={'generation':8*50,'step':8*50,'reset':8,'model_load':8,'env_construct':8,'env_init':8,'materialize':4,'input_tokens':8*50*4096,'output_tokens':8*50*16,'environment_operations':8*50+8}
base=example(); result=validate_budget(base)
assert result['required_ceiling']=={k:base['known_completed']['amounts'][k]+base['unknown_reserved']['amounts'][k]+NEW_MAX[k] for k in NEW_MAX}
assert result['status']=='BUDGET_INCOMPLETE' and result['authorization'] is False and result['history_authenticated'] is False
for label,change in [('zero',lambda x:x.update(new_limits=values())),('unknown_input',lambda x:x['unknown_reserved']['amounts'].__setitem__('input_tokens',4095)),('unknown_output',lambda x:x['unknown_reserved']['amounts'].__setitem__('output_tokens',15))]:
    b=copy.deepcopy(base);change(b)
    try:validate_budget(b)
    except BudgetError:print(label,'rejected')
    else:raise AssertionError(label+' accepted')
print('PASS: exact per-resource addition and 4/8/400/408/1638400/6400 bounds; authenticated history remains false')
