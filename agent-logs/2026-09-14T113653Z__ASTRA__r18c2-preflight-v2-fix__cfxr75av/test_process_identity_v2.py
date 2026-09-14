"""Synthetic identity inputs only: never execute the scientific script."""
import importlib.util
import json
import fcntl
import os
from pathlib import Path
import sys
import tempfile
import unittest
from dataclasses import replace

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('preflight_v2', HERE / 'future-preflight-v2.py')
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def process(argv=None, **kwargs):
    defaults = dict(pid=12345, exe=str(m.PYTHON.resolve()), cwd=str(m.REPO),
                    argv=tuple(argv or [str(m.PYTHON), str(m.Rules().script), '--output', str(m.RUNTIME), '--resume']),
                    start_ticks=987654, boot_id='synthetic-boot')
    defaults.update(kwargs)
    return m.Process(**defaults)


class DetectorTests(unittest.TestCase):
    def test_false_positive_matrix(self):
        script, wrapper = str(m.Rules().script), str(HERE / 'durable-wrapper-v2.sh')
        cases = [
            ('shell-text', '/usr/bin/bash', ['bash', '-c', 'echo ' + script]),
            ('shell-data-arg', '/usr/bin/bash', ['bash', '-c', 'sleep 1', script]),
            ('grep', '/usr/bin/grep', ['grep', script, 'log.txt']),
            ('python-command-data', str(m.PYTHON.resolve()), ['python', '-c', 'pass', script]),
            ('python-command-joined', str(m.PYTHON.resolve()), ['python', '-cpass', script]),
            ('python-module-data', str(m.PYTHON.resolve()), ['python', '-m', 'json.tool', script]),
            ('python-stdin-data', str(m.PYTHON.resolve()), ['python', '-', script]),
            ('wrong-script-path', str(m.PYTHON.resolve()), ['python', '/tmp/run_progress_aware_card_v2_r18_c2.py', '--output', str(m.RUNTIME), '--resume']),
            ('wrapper-text', '/usr/bin/bash', ['bash', '-c', 'echo durable-wrapper.sh', wrapper]),
            ('editor', '/usr/bin/node', ['node', '/editor.js', script]),
            ('language-server', '/usr/bin/node', ['node', '/language-server.js', wrapper]),
            ('task-manager', '/usr/bin/node', ['node', '/task-manager.js', script, wrapper]),
            ('ps', '/usr/bin/ps', ['ps', '-p', '123', script]),
            ('different-python-script', str(m.PYTHON.resolve()), ['python', '/tmp/diagnostic.py', script]),
            ('wrong-wrapper-path', '/usr/bin/bash', ['bash', '/tmp/durable-wrapper-v2.sh', wrapper]),
            ('wrapper-syntax-check', '/usr/bin/bash', ['bash', '-n', wrapper]),
            ('wrapper-noexec-check', '/usr/bin/bash', ['bash', '-o', 'noexec', wrapper]),
            ('wrapper-stdin-data', '/usr/bin/bash', ['bash', '-is', wrapper]),
            ('python-help-data', str(m.PYTHON.resolve()), ['python', '--help', script]),
        ]
        for name, exe, argv in cases:
            with self.subTest(name=name):
                self.assertEqual(m.classify(process(argv, exe=exe))['kind'], 'unrelated')

    def test_true_runner_forms(self):
        script = 'scripts/run_progress_aware_card_v2_r18_c2.py'
        output = str(m.RUNTIME.relative_to(m.REPO))
        for prefix in [[], ['-u'], ['-B', '-u'], ['-X', 'dev'], ['-Wignore'], ['--']]:
            with self.subTest(prefix=prefix):
                argv = ['python', *prefix, script, '--output', output, '--resume']
                self.assertEqual(m.classify(process(argv))['kind'], 'runner')
        self.assertEqual(m.classify(process(['python', script, '--resume', '--output=' + output]))['kind'], 'runner')

    def test_exact_script_unexpected_invocation_stops(self):
        base = process()
        cases = [replace(base, argv=base.argv[:-1]),
                 replace(base, argv=base.argv[:-2] + ('/tmp/other-runtime', '--resume')),
                 replace(base, cwd='/tmp'),
                 replace(base, argv=base.argv + ('--replay-only',)),
                 replace(base, exe='/usr/bin/python3'),
                 replace(base, exe=None, error='permission denied'),
                 replace(base, cwd=None, argv=('python', 'scripts/run_progress_aware_card_v2_r18_c2.py'))]
        for case in cases:
            with self.subTest(case=case):
                self.assertEqual(m.classify(case)['kind'], 'ambiguous')

    def test_exact_scientific_module_is_reviewable(self):
        proc = process(['python', '-m', 'scripts.run_progress_aware_card_v2_r18_c2'])
        self.assertEqual(m.classify(proc)['kind'], 'ambiguous')

    def test_wrapper_identity(self):
        argv = ['bash', '--noprofile', '--norc', str(HERE / 'durable-wrapper-v2.sh'),
                str(HERE), str(m.REPO), str(m.Rules().external_lock), *process().argv]
        proc = process(argv, exe='/usr/bin/bash')
        self.assertEqual(m.classify(proc)['kind'], 'wrapper')
        self.assertEqual(m.classify(replace(proc, argv=('bash', '-l', *proc.argv[3:])))['kind'], 'wrapper')
        argv[6] = '/tmp/another.lock'
        self.assertEqual(m.classify(process(argv, exe='/usr/bin/bash'))['kind'], 'ambiguous')

    def test_legacy_wrapper_is_still_protected(self):
        wrapper = HERE.parent / '2026-09-14T054711Z__ASTRA__r18c2-operational-forensics__nvrcqcpb/durable-wrapper.sh'
        argv = ['bash', str(wrapper), str(HERE), str(m.REPO), str(m.Rules().external_lock), *process().argv]
        self.assertEqual(m.classify(process(argv, exe='/usr/bin/bash'))['kind'], 'wrapper')

    def test_pid_birth_and_boot(self):
        proc = process()
        record = {'pid': proc.pid, 'start_ticks': proc.start_ticks, 'boot_id': proc.boot_id}
        self.assertEqual(m.recorded_identity(record, proc), 'active_recorded_identity')
        self.assertEqual(m.recorded_identity(record, replace(proc, start_ticks=proc.start_ticks + 1)), 'pid_reused')
        self.assertEqual(m.recorded_identity(record, replace(proc, boot_id='new-boot')), 'previous_boot')
        self.assertEqual(m.recorded_identity({**record, 'boot_id': None}, proc), 'ambiguous_legacy_identity')
        self.assertEqual(m.recorded_identity(record, None), 'inactive')
        self.assertEqual(m.recorded_identity(record, replace(proc, state='Z')), 'inactive')

    def test_no_exited_process_is_active(self):
        self.assertEqual(m.classify(process(state='Z'))['kind'], 'unrelated')

    def test_lock_probe_nontruncating_and_held_lock_stop(self):
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            lock = Path(directory) / 'fixture.lock'
            lock.write_bytes(b'preserve-me')
            self.assertIn('available', m.probe_lock(lock, required=True))
            with lock.open('r') as held:
                fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
                with self.assertRaisesRegex(RuntimeError, 'lock held'):
                    m.probe_lock(lock, required=True)
            self.assertEqual(lock.read_bytes(), b'preserve-me')
            absent = Path(directory) / 'missing.lock'
            self.assertIn('absent', m.probe_lock(absent, required=False))
            self.assertFalse(absent.exists())
            with self.assertRaisesRegex(RuntimeError, 'missing'):
                m.probe_lock(absent, required=True)

    def test_proc_fixture_and_recorded_scan(self):
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            root = Path(directory)
            procroot, tasks = root / 'proc', root / 'tasks'
            (procroot / 'sys/kernel/random').mkdir(parents=True)
            (procroot / 'sys/kernel/random/boot_id').write_text('fixture-boot')
            process_dir = procroot / '4321'
            process_dir.mkdir()
            fields = ['S', '1', '4321', '4321'] + ['0'] * 15 + ['999'] + ['0'] * 5
            (process_dir / 'stat').write_text('4321 (fixture (name)) ' + ' '.join(fields))
            (process_dir / 'cmdline').write_bytes(b'python\0-c\0pass\0')
            (process_dir / 'exe').symlink_to(m.PYTHON.resolve())
            (process_dir / 'cwd').symlink_to(root)
            identity_dir = tasks / '2026-09-14T000000Z__ASTRA__r18c2-test__fixture'
            identity_dir.mkdir(parents=True)
            identity = identity_dir / 'runner.identity'
            identity.write_text(json.dumps({'pid': 4321, 'start_ticks': 999, 'boot_id': 'fixture-boot'}))
            rules = replace(m.Rules(), tasks=tasks)
            scan = m.process_gate(rules, procroot)
            self.assertEqual(scan['blockers'][0]['kind'], 'active_recorded_identity')
            identity.write_text(json.dumps({'pid': 4321, 'start_ticks': 998, 'boot_id': 'fixture-boot'}))
            self.assertEqual(m.process_gate(rules, procroot)['blockers'], [])
            identity.write_text(json.dumps({'pid': 4321, 'start_ticks': 999, 'boot_id': 'previous-boot'}))
            self.assertEqual(m.process_gate(rules, procroot)['blockers'], [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
