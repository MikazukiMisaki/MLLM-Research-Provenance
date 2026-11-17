import sys
sys.path.insert(0,'/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-owned-static-adapter__private')
import static_adapter as adapter
import test_static_adapter as fixtures
plan,raw,digest,kw=fixtures.example()
plan['budget']['proposed_additional']={k:0 for k in adapter.METRICS}
result=adapter.validate_plan(plan,raw,digest)
draft=adapter.draft_arm_config(plan,raw,digest,**kw)
assert result['status']=='DECLARATIONS_CONSISTENT_NOT_AUTHORIZED' and draft['draft_only'] is True
print('ACCEPTED: all proposed additional costs zero with 4-pair / 8-episode declared limits; status remains NOT_AUTHORIZED')
print('No actual product, task, model, or environment used')
