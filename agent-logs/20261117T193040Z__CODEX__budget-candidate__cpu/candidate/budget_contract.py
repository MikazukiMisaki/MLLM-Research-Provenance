"""Prospective arithmetic only. No ledger reads, execution, approval or launch."""
import re

class BudgetError(ValueError): pass

# Single prospective 4-pair bound only; not a claim of approved or available budget.
NEW_MAX={'generation':400,'step':400,'reset':8,'model_load':8,'env_construct':8,
         'env_init':8,'materialize':4,'input_tokens':400*4096,'output_tokens':400*16,
         'environment_operations':408}
METRICS=tuple(NEW_MAX)
UNMODELED=('training','device','time','io')

def _amounts(value,name):
    if type(value) is not dict or set(value)!=set(METRICS):raise BudgetError(name+' resource set')
    if any(type(x) is not int or x<0 for x in value.values()):raise BudgetError(name+' resource value')
    if value['environment_operations'] < value['reset']+value['step']:
        raise BudgetError(name+' environment total excludes reset/step')
    return value

def _historical(value,name):
    if type(value) is not dict or set(value)!={'ledger_sha256','amounts'}:raise BudgetError(name+' evidence shape')
    sha=value['ledger_sha256']
    if type(sha) is not str or re.fullmatch('[0-9a-f]{64}',sha) is None:raise BudgetError(name+' evidence digest')
    return _amounts(value['amounts'],name)

def validate_budget(value):
    if type(value) is not dict or set(value)!={'known_completed','unknown_reserved','new_limits','combined_ceiling','unmodeled'}:
        raise BudgetError('budget schema: explicitly report unknown reservations')
    known=_historical(value['known_completed'],'known_completed')
    unknown=_historical(value['unknown_reserved'],'unknown_reserved')
    new=_amounts(value['new_limits'],'new_limits')
    ceiling=_amounts(value['combined_ceiling'],'combined_ceiling')
    if new!=NEW_MAX:raise BudgetError('four-pair proposed maximum must be exact for every resource')
    # An unresolved generation has no trusted actual output; carry its full reservation.
    if (unknown['input_tokens'] < unknown['generation']*4096 or
        unknown['output_tokens'] < unknown['generation']*16):
        raise BudgetError('unknown generation reservation missing token allowance')
    if type(value['unmodeled']) is not dict or value['unmodeled']!={x:'NOT_MODELED' for x in UNMODELED}:
        raise BudgetError('unmodeled training/device/time/io must remain incomplete')
    required={k:known[k]+unknown[k]+new[k] for k in METRICS}
    if any(required[k]>ceiling[k] for k in METRICS):raise BudgetError('combined ceiling exceeded')
    return {'status':'BUDGET_INCOMPLETE','arithmetic':'CONSISTENT_CLAIMS_ONLY',
            'required_ceiling':required,'history_authenticated':False,
            'unknown_reservations_authenticated':False,'authorization':False,
            'unmodeled':dict(value['unmodeled'])}
