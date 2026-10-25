from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
f=ROOT/'src/self_improvement/si_p3/collector.py';s=f.read_text().replace('from env.base import InteractiveEnvironment','from env.base import InteractiveEnvironment\nfrom recovery.corpus import task_family_from_id');s=s.replace('require(task.task_id == self.slot.task_id and task.family == self.slot.family and task.split == "train",','require(task.task_id == self.slot.task_id and task_family_from_id(task.task_id) == self.slot.family and\n                task.family in (None, self.slot.family) and task.split == "train",');s=s.replace('PublicState(task.task_id, task.family, task.text, result.observation, tuple(result.valid_actions))','PublicState(task.task_id, self.slot.family, task.text, result.observation, tuple(result.valid_actions))');f.write_text(s)
f=ROOT/'src/self_improvement/si_p3/data.py';s=f.read_text();start=s.index('    require(all(set(x) == {"task_id", "family"}');end=s.index('    selected = []\n',start);block=s[start:end];s=s[:start]+'    validate_background_identities(expert_train_tasks, evidence_class=evidence_class)\n'+s[end:];insert=s.index('\ndef select_background(');helper='\n\ndef validate_background_identities(expert_train_tasks: Sequence[Mapping[str, str]], *, evidence_class: str) -> None:\n'+block.replace('    if evidence_class == "historical":','    require(evidence_class in ("historical", "synthetic"), "background evidence class")\n    if evidence_class == "historical":')+'\n';s=s[:insert]+helper+s[insert:];f.write_text(s)
f=ROOT/'tests/test_si_p3_learning.py';s=f.read_text();old=s.index('\ndef test_background_rejects_unbound_complete_historical_identity_set');s=s[:old]+r'''

def test_background_complete_historical_metadata_anchor_rejects_subset():
    from self_improvement.si_p3.data import validate_background_identities
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'configs/sft/sft_accepted_task_splits.json').read_text())
    tasks=[{'task_id':x['task_id'],'family':x['task_id'].split('-',1)[0]} for x in manifest['pools']['train'] if x['task_id'].split('-',1)[0] in FAMILIES]
    assert len(tasks)==895
    validate_background_identities(tasks,evidence_class='historical')
    with pytest.raises(ContractError,match='identity anchor'):
        validate_background_identities(tasks[1:],evidence_class='historical')
''';f.write_text(s)
f=ROOT/'tests/test_si_p3_collector.py';f.write_text(f.read_text()+r'''


def test_actual_normalized_P0_reset_family_None_is_derived_from_canonical_ID():
    from env.base import ResetResult,Task,Transition
    from self_improvement.si_p3.collector import EnvironmentAdapter
    slot=synthetic_plan()[0]
    class Boundary:
        def reset(self,*,seed):return ResetResult('public obs',Task(slot.task_id,'public goal','train'),('wait',))
        def step(self,command):return Transition('terminal public obs',1.0,True,False,())
    env=EnvironmentAdapter(Boundary(),slot,'synthetic-session')
    state=env.reset()
    assert state.family==slot.family
    terminal=env.step('wait')
    assert terminal.done and terminal.reward==1 and terminal.valid_actions==()


def test_missing_nonterminal_map_and_conflicting_family_fail_closed():
    from env.base import ResetResult,Task,Transition
    from self_improvement.si_p3.collector import EnvironmentAdapter
    slot=synthetic_plan()[0]
    class Boundary:
        def reset(self,*,seed):return ResetResult('public',Task(slot.task_id,'goal','train',slot.family),('wait',))
        def step(self,command):return Transition('public',0.0,False,False,None)
    env=EnvironmentAdapter(Boundary(),slot,'synthetic-session');env.reset()
    with pytest.raises(ContractError,match='full action map'):env.step('wait')
    class Conflict(Boundary):
        def reset(self,*,seed):return ResetResult('public',Task(slot.task_id,'goal','train','wrong'),('wait',))
    with pytest.raises(ContractError,match='identity drift'):EnvironmentAdapter(Conflict(),slot,'s').reset()
''')
f=ROOT/'docs/si_p3_engineering_v1.md';s=f.read_text().replace('`EnvironmentAdapter` uses the existing normalized environment interface.','`EnvironmentAdapter` uses the existing normalized P0 environment interface. The frozen wrapper leaves Task.family=None, so the new adapter derives it from the verified canonical task ID and rejects conflicting explicit family values. Empty terminal maps are supported; an unreported map (None) remains fail-closed rather than silently becoming a complete map. Actual terminal map availability remains unverified without future authorized execution.');f.write_text(s)
print('Closed Task.family=None production interface using frozen canonical parser; historical identity metadata guard tested directly.')
