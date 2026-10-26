"""Prepared only: execute solely after root supplies a frozen exact SHA.

Six software observations for ENG-PC01/PC02/A01. No pytest runner is invoked.
The repository fixture supplies only raw model/tokenizer/OS/environment I/O fakes.
Production reader, permit, ledger, producer, shared core, parser and audit remain real.
"""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import argparse, hashlib, json, os, re, subprocess, sys, traceback

PIN = Path('/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python')

def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(',', ':'), allow_nan=False)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--expected-sha', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    tree, output = args.repository.resolve(), args.output.resolve()
    assert re.fullmatch('[0-9a-f]{40}', args.expected_sha)
    assert sys.flags.isolated and Path(sys.executable).resolve() == PIN.resolve()
    assert all(k not in os.environ for k in ('PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV'))
    assert os.environ.get('CUDA_VISIBLE_DEVICES') == ''
    assert all(os.environ.get(k) == '1' for k in
               ('PYTHONDONTWRITEBYTECODE', 'HF_HUB_OFFLINE', 'TRANSFORMERS_OFFLINE'))
    sys.dont_write_bytecode = True
    assert not output.exists() and not output.is_relative_to(tree)
    def git(*parts):
        return subprocess.check_output(['git', *parts], cwd=tree, text=True).strip()
    before = {'sha': git('rev-parse', 'HEAD'), 'tree': git('rev-parse', 'HEAD^{tree}'),
              'status': git('status', '--porcelain=v1', '--untracked-files=all'),
              'branch': git('rev-parse', '--abbrev-ref', 'HEAD')}
    assert before['sha'] == args.expected_sha and before['status'] == ''
    assert before['branch'] == 'HEAD', 'Use an independent detached worktree'
    output.mkdir(parents=False)
    sys.path[:0] = [str(tree/'src'), str(tree/'tests'), str(tree)]
    from pytest import MonkeyPatch
    from si_s01_engineering_support import fixture_setup
    from self_improvement.si_s01.contract import ContractError, P0_SHA256, projection, PublicState
    from self_improvement.si_s01.engineering_contract import SOFTWARE, RNG_STATUS
    from self_improvement.si_s01.engineering_evidence import EngineeringLedger
    from self_improvement.si_s01.engineering_runtime import (
        EngineeringRun, EngineeringProducer, real_environment, observed_public, compare_prepared)
    from self_improvement.si_s01.engineering_audit import audit_engineering
    from self_improvement.si_s01.evidence import read_events
    observations = []
    def rejection(operation, message_fragment):
        try:
            operation()
        except ContractError as error:
            assert message_fragment in str(error), (type(error).__name__, str(error))
            return {'exception_type': type(error).__module__+'.'+type(error).__qualname__,
                    'message': str(error)}
        raise AssertionError('Expected production ContractError was not raised')
    def fixture(name, patch):
        patch.setenv('ALFWORLD_DATA', 'independent-software-restore-marker')
        f = fixture_setup(output/name, patch)
        assert f.permit.evidence_class == SOFTWARE and f.permit.authorization['science_authorized'] is False
        fake = sys.modules['torch']
        assert fake._si_s01_software_boundary is True
        assert Path(fake.__file__).resolve().is_relative_to(output/name)
        return f
    class Clock:
        now = 0.0
        def __call__(self): return self.now
    def prime(f, name):
        clock = Clock()
        ledger = EngineeringLedger(output/name/'probe_events.jsonl', f.permit,
                                   started_at=0.0, clock=clock)
        box = {}
        def load():
            box['producer'] = EngineeringProducer.load(f.permit, ledger)
            return {'mode': 'P0', 'adapter_sha256': P0_SHA256}
        ledger.call('model_load', 0, load)
        def construct():
            box['env'] = real_environment(f.permit)
            env = box['env']
            return dict(env.initialize()) | {'package_origins': env.engineering_package_origins}
        ledger.call('env_construct', 0, construct,
                    request={'pool_seed': 42, 'historical_internal_rng': RNG_STATUS})
        state = ledger.call('reset', 0,
            lambda: observed_public(box['env'].reset(seed=30000), f.permit.history,
                                    reset=True, goal=''), request={'seed': 30000})['state']
        assert state == f.permit.history.states[0]
        prompt = projection(PublicState.from_dict(state), [])['public_prompt']
        prepared = box['producer'].prepare(prompt)
        compare_prepared(f.permit.history, prepared)
        refs = f.permit.history.row['metadata']['r19_source_event_refs']
        request = {'historical_reset_event_id': refs['reset_event_id'],
                   'historical_generation_event_id': refs['generation_event_ids'][0]}
        return ledger, box['producer'], box['env'], clock, prepared, request
    def close_prefix(ledger, env, label, exhausted=False):
        if exhausted:
            rejection(lambda: ledger.call('env_close', 0,
                      lambda: (env.close() or {'closed': True})), '600-second')
        else:
            ledger.call('env_close', 0, lambda: (env.close() or {'closed': True}))
        ledger.close({'independent_software_probe': label, 'expected_rejection': True})
    try:
        name = 'pc01_second_invocation'
        with MonkeyPatch.context() as patch:
            f = fixture(name, patch)
            ledger, producer, env, clock, prepared, request = prime(f, name)
            def twice():
                producer.generate(prepared)
                return producer.generate(prepared)
            error = rejection(lambda: ledger.call('generation', 0, twice,
                prepared=prepared.to_dict(), request=request), 'invocation already consumed')
            assert f.state.calls['generation'] == 1
            assert ledger.used['generation'] == 1 and ledger.used['generated_tokens'] == 16
            close_prefix(ledger, env, name)
            observations.append({'case': name, 'expected_raw_model_counter': 1,
                                 'raw_model_counter': f.state.calls['generation'], 'rejection': error})
        name = 'pc01_mutated_caller_prepared'
        with MonkeyPatch.context() as patch:
            f = fixture(name, patch)
            ledger, producer, env, clock, big, request = prime(f, name)
            small = producer.prepare('independent small reservation')
            caller_owned, frozen_small = small.to_dict(), deepcopy(small.to_dict())
            assert len(small.prepared.input_ids) < len(big.prepared.input_ids)
            def changed():
                # Mutate both the caller dictionary and its original nested list objects.
                caller_owned['prompt'] = big.prepared.prompt
                caller_owned['rendered_prompt'] = big.prepared.rendered_prompt
                caller_owned['input_ids'][:] = list(big.prepared.input_ids)
                caller_owned['attention_mask'][:] = list(big.attention_mask)
                return producer.generate(big)
            error = rejection(lambda: ledger.call('generation', 0, changed,
                prepared=caller_owned, request=request), 'must equal reserved unit')
            assert f.state.calls['generation'] == 0
            assert ledger.used['input_tokens'] == len(frozen_small['input_ids'])
            close_prefix(ledger, env, name)
            rows = read_events(output/name/'probe_events.jsonl')
            starts = [e for e in rows if e['kind']=='unit_started' and
                      e['payload']['identity']['kind']=='generation']
            assert len(starts) == 1 and starts[0]['payload']['prepared'] == frozen_small
            observations.append({'case': name, 'expected_raw_model_counter': 0,
                'raw_model_counter': f.state.calls['generation'], 'rejection': error,
                'durable_prepared_equals_original_reservation': True,
                'reserved_input_tokens': ledger.used['input_tokens']})
        for advance in ('resource', 'synchronize'):
            name = 'pc02_deadline_after_'+advance
            with MonkeyPatch.context() as patch:
                f = fixture(name, patch)
                ledger, producer, env, clock, prepared, request = prime(f, name)
                clock.now = 599.0
                if advance == 'resource':
                    original = producer.resource
                    def delayed_resource():
                        result = original()
                        clock.now = 601.0
                        return result
                    producer.resource = delayed_resource  # Explicit resource-I/O fake only.
                else:
                    producer.torch.cuda.synchronize = lambda: setattr(clock, 'now', 601.0)
                error = rejection(lambda: ledger.call('generation', 0,
                    lambda: producer.generate(prepared), prepared=prepared.to_dict(),
                    request=request), '600-second')
                assert f.state.calls['generation'] == 0 and ledger.used['generation'] == 1
                close_prefix(ledger, env, name, exhausted=True)
                assert f.state.calls['close'] == 0
                observations.append({'case': name, 'expected_raw_model_counter': 0,
                    'raw_model_counter': f.state.calls['generation'],
                    'fake_clock_seconds': clock.now, 'rejection': error,
                    'no_close_edge_after_budget': True})
        name = 'a01_positive_and_resealed_conflicts'
        with MonkeyPatch.context() as patch:
            f = fixture(name, patch)
            report = EngineeringRun(f.permit, f.permit.output).run()
            assert report['status'] == 'OBSERVED_PUBLIC_PATH_COMPATIBLE_NOT_RNG_RECONSTRUCTED'
            assert f.state.calls['generation'] == f.state.calls['reset'] == f.state.calls['close'] == 1
            assert f.state.calls['step'] == 6 and report['science_authorized'] is False
            original_path = f.permit.output/'engineering_events.jsonl'
            original = read_events(original_path)
            encoder = EngineeringProducer(f.state.tokenizer, None, evidence_class=SOFTWARE)
            assert audit_engineering(original_path, f.permit, encoder)['status'] == report['status']
            calls_before = dict(f.state.calls)
            for attack in ('raw_latency', 'sequence_prefix'):
                rows = deepcopy(original)
                targets = [e for e in rows if e['kind']=='runtime_evidence' and
                           e['payload']['kind']=='generation_returned']
                assert len(targets) == 1
                data = targets[0]['payload']['data']
                if attack == 'raw_latency':
                    # A valid raw scalar changes only in the saved return, not the completion.
                    data['raw']['latency_seconds'] += 0.125
                    fragment = 'durable returned raw'
                else:
                    data['observed_sequence'][0] += 1
                    fragment = 'observed sequence'
                mapping, previous = {}, None
                def remap(value):
                    if isinstance(value, str): return mapping.get(value, value)
                    if isinstance(value, list): return [remap(v) for v in value]
                    if isinstance(value, dict): return {k: remap(v) for k, v in value.items()}
                    return value
                for event in rows:
                    old = event['event_id']
                    event['payload'] = remap(event['payload'])
                    event['previous'] = previous
                    event['event_id'] = hashlib.sha256(canonical(
                        {k: v for k, v in event.items() if k!='event_id'}).encode()).hexdigest()
                    mapping[old], previous = event['event_id'], event['event_id']
                target = output/name/(attack+'.jsonl')
                target.write_text(''.join(canonical(e)+'\n' for e in rows))
                assert read_events(target) == rows  # Chain valid before semantic rejection.
                starts = {e['payload']['unit']: e['event_id'] for e in rows if e['kind']=='unit_started'}
                assert all(e['payload']['started_event']==starts[e['payload']['unit']]
                    for e in rows if e['kind'] in ('unit_completed', 'unit_failed'))
                error = rejection(lambda: audit_engineering(target, f.permit, encoder), fragment)
                assert dict(f.state.calls) == calls_before
                observations.append({'case': 'a01_'+attack, 'rejection': error,
                    'coherent_chain_and_start_refs_accepted': True,
                    'audit_added_external_calls': False, 'mutant_journal_sha256': sha(target)})
        after = {'sha': git('rev-parse', 'HEAD'), 'tree': git('rev-parse', 'HEAD^{tree}'),
                 'status': git('status', '--porcelain=v1', '--untracked-files=all'),
                 'branch': git('rev-parse', '--abbrev-ref', 'HEAD')}
        assert before == after
        origins = {}
        for module_name in ('self_improvement.si_s01.engineering_evidence',
            'self_improvement.si_s01.engineering_runtime', 'self_improvement.si_s01.runtime_core',
            'self_improvement.si_s01.engineering_audit', 'si_s01_engineering_support'):
            path = Path(sys.modules[module_name].__file__).resolve()
            assert path.is_relative_to(tree)
            origins[module_name] = {'path': str(path), 'sha256': sha(path)}
        result = {'status': 'EXPECTED_CLOSURE_OBSERVATIONS_SOFTWARE_ONLY',
            'exact_sha': args.expected_sha, 'script_sha256': sha(__file__),
            'source_before': before, 'source_after': after, 'origins': origins,
            'science_authorized': False, 'real_model_environment_or_device_calls': False,
            'scope': 'ENG-PC01/PC02/A01 only; no scientific or launch acceptance',
            'observations': observations}
        write(output/'probe_observations.json', result)
        print(json.dumps(result, indent=2))
        return 0
    except BaseException as error:
        failure = {'status': 'CLOSURE_PROBE_EXPECTATION_NOT_MET_SOFTWARE_ONLY',
            'exact_sha': args.expected_sha, 'observations': observations,
            'case_in_progress': locals().get('name'),
            'last_fixture_observed_boundary_counts': dict(getattr(
                getattr(locals().get('f'), 'state', None), 'calls', {})),
            'exception_type': type(error).__module__+'.'+type(error).__qualname__,
            'message': str(error), 'traceback': traceback.format_exc()}
        write(output/'probe_observations.json', failure)
        print(json.dumps(failure, indent=2))
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
