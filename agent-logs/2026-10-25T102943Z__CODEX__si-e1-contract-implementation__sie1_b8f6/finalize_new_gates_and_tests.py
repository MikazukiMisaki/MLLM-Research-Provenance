from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
f=ROOT/'src/self_improvement/si_p3/collector.py';s=f.read_text();s=s.replace('def __init__(self, tokenizer: Any, producer: RawProducer) -> None:\n        self.tokenizer','def __init__(self, tokenizer: Any, producer: RawProducer, *, evidence_class: str = "disabled") -> None:\n        software_only(evidence_class)\n        self.tokenizer');s=s.replace('evidence_class: str = "synthetic"','evidence_class: str = "disabled"');f.write_text(s)
f=ROOT/'src/self_improvement/si_p3/audit.py';s=f.read_text().replace('ProducerAdapter(tokenizer, lambda *_: None)','ProducerAdapter(tokenizer, lambda *_: None, evidence_class="synthetic")');f.write_text(s)
f=ROOT/'tests/si_p3_support.py';s=f.read_text().replace('Ports(ProducerAdapter(tokenizer, raw), factory)','Ports(ProducerAdapter(tokenizer, raw, evidence_class="synthetic"), factory, "synthetic")');f.write_text(s)
f=ROOT/'tests/test_si_p3_collector.py';f.write_text(f.read_text()+r'''


def test_model_port_and_collector_default_disabled(tmp_path):
    class Forbidden:
        def __getattr__(self,name):raise AssertionError('touched boundary before gate')
    with pytest.raises(ContractError,match='NOT_GRANTED'):ProducerAdapter(Forbidden(),Forbidden())
    with pytest.raises(ContractError,match='NOT_GRANTED'):
        Collector(synthetic_plan(),Ports(Forbidden(),Forbidden()),tmp_path/'disabled')
    assert not (tmp_path/'disabled').exists()


def test_logical_CONTINUE_references_do_not_debit_physical_cost(complete):
    run,events,tok,*_=complete
    result=audit_run(run,events,tok)
    values=result['logical_prefix_comparisons']
    assert len(values)==96
    for row,logical in zip(run['slots'],values):
        assert logical['CONTINUE']['generations']==len(row['branch']['source_suffix_generation_refs'])
        assert logical['K1']['generations']==2+len(row['branch']['suffix']['generations'])
        assert logical['teacher_attempt']['generations']==2
        assert logical['physical_debit_added_by_this_function']==0
''')
f=ROOT/'tests/test_si_p3_learning.py';f.write_text(f.read_text()+r'''


def test_background_rejects_unbound_complete_historical_identity_set(pipeline):
    # File hash is checked before identities; monkeypatch no validator/function.
    from self_improvement.si_p3.contract import EXPERT_TRAIN_FIVE_IDENTITY_SHA256,digest
    assert digest(sorted(pipeline[8],key=lambda x:(x['family'],x['task_id'])))!=EXPERT_TRAIN_FIVE_IDENTITY_SHA256
    # Synthetic evidence remains explicitly distinct, and never attests to actual S readiness.
    assert all(x.origin=='background' for x in pipeline[6])
''')
# preserve failed v1 integration script and all outputs, create a new non-overwriting revision.
f=OWN/'synthetic_integration_v2.py';assert not f.exists();s=(OWN/'synthetic_integration.py').read_text().replace("folder=OWN/'synthetic_integration_v1'","folder=OWN/'synthetic_integration_v2'");f.write_text(s)
print('Disabled-by-default ports; only explicit synthetic port evidence accepted. Added logical-cost and gate tests.')
