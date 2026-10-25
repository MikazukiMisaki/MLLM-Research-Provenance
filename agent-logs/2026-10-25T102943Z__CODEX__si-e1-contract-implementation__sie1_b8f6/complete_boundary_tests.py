from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
f=ROOT/'tests/test_si_p3_learning.py';f.write_text(f.read_text()+r'''


@pytest.mark.parametrize('neutral_count',[7,8])
def test_fixed_B_selected_neutral_exact_boundary_without_redraw(pipeline,neutral_count):
    pool,original=pipeline[4],pipeline[5]
    selected_neutral=[x.example.task_id for x in original.B if x.Y0==1]
    flip=set(selected_neutral[:len(selected_neutral)-neutral_count])
    rows=tuple(replace(x,Y0=0) if x.example.task_id in flip else x for x in pool.candidates)
    fixture=Pool(rows,pool.dispositions,pool.integrity)
    if neutral_count==7:
        with pytest.raises(ContractError,match='neutral<8'):adopt_once(fixture)
    else:
        accepted=adopt_once(fixture)
        assert accepted.audit['selected_B_neutral']==8 and accepted.audit['draws']==1
        assert accepted.audit['selected_B']==original.audit['selected_B']


def test_cumulative_prompt_ratio_rejects_consistently_encoded_new_inputs(pipeline):
    tok=pipeline[3];pairs=list(pipeline[10])
    for i in range(120,144):
        b,c=pairs[i]
        longer=encode_example(tok,task_id=b.task_id,family=b.family,public_prompt=b.public_prompt+'\nSynthetic public details'+' item'*100,
                              completion=b.completion,command=b.command,origin='new')
        assert longer.loss_tokens==c.loss_tokens
        pairs[i]=(longer,c)
    with pytest.raises(ContractError,match='new cumulative prompt ratio'):
        audit_exposure(pairs,CompletionCollator(tok.pad_token_id))
''')
f=ROOT/'docs/si_p3_engineering_v1.md';s=f.read_text().replace('fresh append-only fsynced hash chain.','fresh append-only fsynced hash chain with a unique run ID.').replace('`UnitRegistry` starts each physical identity once;','`UnitRegistry` checks run/task/seed/kind/index/start and referenced action receipts online, then starts each physical identity once;').replace('common mechanical Q and2048','common mechanical Q and2048');f.write_text(s)
print('Added selected-B neutral7/8 boundary and cumulative prompt ratio checks; current frozen actor/v2 semantics retained.')
