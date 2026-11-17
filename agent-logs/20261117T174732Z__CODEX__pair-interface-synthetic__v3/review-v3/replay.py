"""Independent v3 schedule replays, synthetic subprocesses and files only."""
import pathlib,sys,tempfile
target=pathlib.Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-interface-schedule-v3__private')
sys.path.insert(0,str(target))
import candidate as c
from test_candidate import setup,verify,spawn_for

with tempfile.TemporaryDirectory(prefix='independent-v3-review-') as d:
    root=pathlib.Path(d)
    for name,pair,order in [('wrong_pair','four',('B','A')),('wrong_order','one',('B','A'))]:
        owner=c.Owner(root/name);calls=[]
        def record(*a,**k):calls.append(1);return setup(*a,**k)
        try:c.pair(owner,pair,order,{'case':pair},record,verify,spawn_for())
        except c.Stop as e:print(name,'stop=',str(e),'setup_calls=',len(calls),'materialize_reserved=',owner.count['materialize'],'failed=',owner.failed)
        else:raise AssertionError('wrong schedule was not rejected')
        assert not calls and owner.count['materialize']==0 and owner.failed
    owner=c.Owner(root/'control');calls=[]
    def record(*a,**k):calls.append(1);return setup(*a,**k)
    c.pair(owner,'one',('A','B'),{'case':'one'},record,verify,spawn_for())
    print('normal_control','setup_calls=',len(calls),'materialize_reserved=',owner.count['materialize'],'next=',owner.expected_pair())
    assert len(calls)==owner.count['materialize']==1 and owner.expected_pair()==('two',('B','A'))
    owner=c.Owner(root/'mismatch')
    for pair,order in c.SCHEDULE[:3]:c.pair(owner,pair,order,{'case':pair},setup,verify,spawn_for())
    pair,order=c.SCHEDULE[3]
    try:c.pair(owner,pair,order,{'case':pair},setup,verify,spawn_for('mismatch_second_reversed'))
    except c.Stop as e:print('mismatch','stop=',str(e),'failed=',owner.failed,'closed=',sum(s=='closed' for s in owner.states.values()),'model_load=',owner.count['model_load'])
    else:raise AssertionError('mismatch was not rejected')
    assert owner.failed and sum(s=='closed' for s in owner.states.values())==7 and owner.count['model_load']==7
    try:owner.complete()
    except c.Stop as e:print('mismatch_complete','stop=',str(e))
    else:raise AssertionError('failed batch was accepted')
