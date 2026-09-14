"""Read-only preflight. Import-safe, standard library only; never runs scientific code."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = Path('/home/lizening/Alfworld-Self-Improvement-Project')
SHA = 'aa9fa3c34520941e7e3be00294b111e8254fd65b'
PYTHON = Path('/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python')
RUNTIME = REPO / 'artifacts/runtime/validation/progress-aware-r18-c2-formal-aa9fa3c34520941e'
NOTES = Path('/home/lizening/research-notes')


@dataclass(frozen=True)
class Rules:
    repo: Path = REPO
    script: Path = REPO / 'scripts/run_progress_aware_card_v2_r18_c2.py'
    runtime: Path = RUNTIME
    tasks: Path = NOTES / 'agent-logs'
    external_lock: Path = NOTES / 'r18c2-launch-control/launcher.lock'
    # Explicit additional paths are only for synthetic tests, never CLI overrides.
    test_wrappers: tuple[Path, ...] = ()


@dataclass(frozen=True)
class Process:
    pid: int
    exe: str | None
    cwd: str | None
    argv: tuple[str, ...]
    start_ticks: int
    boot_id: str
    state: str = 'S'
    ppid: int = 0
    pgid: int = 0
    sid: int = 0
    error: str | None = None


def resolve(value: str | Path, cwd: str | Path) -> Path:
    path = Path(value)
    return (path if path.is_absolute() else Path(cwd) / path).resolve()


def python_script(argv: tuple[str, ...]) -> tuple[str, str | None, tuple[str, ...]]:
    """Identify Python's execution operand, never arbitrary later arguments."""
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == '--':
            i += 1
            return ('script', argv[i], argv[i + 1:]) if i < len(argv) else ('none', None, ())
        if arg == '-c' or arg.startswith('-c'):
            return 'command', None, ()
        if arg == '-m' or arg.startswith('-m'):
            module = argv[i + 1] if arg == '-m' and i + 1 < len(argv) else arg[2:]
            return 'module', module, ()
        if arg == '-':
            return 'stdin', None, ()
        if arg in ('-h', '-V', '--help', '--version', '--help-env', '--help-xoptions', '--help-all'):
            return 'information', None, ()
        if not arg.startswith('-'):
            return 'script', arg, argv[i + 1:]
        if arg in ('-W', '-X', '--check-hash-based-pycs'):
            i += 2
        elif arg.startswith(('-W', '-X', '--check-hash-based-pycs=')) or re.fullmatch(r'-[bBdEiIOqRsSuvx]+', arg):
            i += 1
        else:
            return 'unknown', None, argv[i:]
    return 'none', None, ()


def bash_script(argv: tuple[str, ...]) -> tuple[str, str | None, tuple[str, ...]]:
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == '--':
            i += 1
            return ('script', argv[i], argv[i + 1:]) if i < len(argv) else ('none', None, ())
        if arg == '-c' or (arg.startswith('-') and not arg.startswith('--') and 'c' in arg[1:]):
            return 'command', None, ()
        if arg.startswith('-') and not arg.startswith('--') and 's' in arg[1:]:
            return 'stdin', None, ()
        if arg in ('--help', '--version') or (arg.startswith('-') and not arg.startswith('--') and 'n' in arg[1:]):
            return 'information_or_syntax', None, ()
        if not arg.startswith('-'):
            return 'script', arg, argv[i + 1:]
        if arg in ('--noprofile', '--norc', '--posix', '--restricted', '--login') or re.fullmatch(r'-[abefhiklmpqrtuvxBCEHPT]+', arg):
            i += 1
        elif arg in ('-o', '+o', '-O', '+O'):
            if arg == '-o' and i + 1 < len(argv) and argv[i + 1] == 'noexec':
                return 'information_or_syntax', None, ()
            i += 2
        else:
            return 'unknown', None, argv[i:]
    return 'none', None, ()


def output_and_resume(args: tuple[str, ...], cwd: str, rules: Rules) -> bool:
    outputs, resumes = [], 0
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--output' and i + 1 < len(args):
            outputs.append(resolve(args[i + 1], cwd))
            i += 2
        elif arg.startswith('--output='):
            outputs.append(resolve(arg.split('=', 1)[1], cwd))
            i += 1
        elif arg == '--resume':
            resumes += 1
            i += 1
        else:
            return False
    return outputs == [rules.runtime.resolve()] and resumes == 1


def wrapper_path(path: Path, rules: Rules) -> bool:
    if path in tuple(p.resolve() for p in rules.test_wrappers):
        return True
    try:
        relative = path.relative_to(rules.tasks.resolve())
    except ValueError:
        return False
    return (
        len(relative.parts) == 2
        and bool(re.fullmatch(r'\d{4}-\d\d-\d\dT\d{6}Z__(?:ASTRA|GEMINI|LUNA)__r18c2-[A-Za-z0-9_-]+', relative.parts[0]))
        and relative.parts[1] in ('durable-wrapper.sh', 'durable-wrapper-v2.sh')
    )


def classify(proc: Process, rules: Rules = Rules()) -> dict:
    result = {'pid': proc.pid, 'kind': 'unrelated', 'reason': 'no executed R18-C2 script identity'}
    if proc.state in ('Z', 'X'):
        return {**result, 'reason': 'exited/zombie, not executing'}
    if not proc.argv:
        return result
    executable = Path((proc.exe or proc.argv[0]).removesuffix(' (deleted)')).name
    is_python = bool(re.fullmatch(r'python(?:\d+(?:\.\d+)*)?', executable))
    is_bash = executable == 'bash'
    cwd = proc.cwd or '/'
    mode, script, args = python_script(proc.argv) if is_python else bash_script(proc.argv) if is_bash else ('none', None, ())
    if is_python and mode == 'module' and script == 'scripts.run_progress_aware_card_v2_r18_c2':
        return {**result, 'kind': 'ambiguous', 'reason': 'scientific module invocation requires review'}
    if mode != 'script' or script is None:
        return result
    path = resolve(script, cwd)
    if is_python and proc.cwd is None and Path(script).name == rules.script.name:
        return {**result, 'kind': 'ambiguous', 'reason': 'executed scientific script candidate with unreadable cwd'}
    if is_python and path == rules.script.resolve():
        if not proc.exe or not proc.cwd or proc.error or Path(proc.exe).resolve() != PYTHON.resolve():
            return {**result, 'kind': 'ambiguous', 'reason': 'exact scientific script but incomplete /proc identity'}
        if Path(cwd).resolve() == rules.repo.resolve() and output_and_resume(args, cwd, rules):
            return {**result, 'kind': 'runner', 'reason': 'Python executable, exact script/cwd/output/resume'}
        return {**result, 'kind': 'ambiguous', 'reason': 'exact scientific script with unexpected cwd or invocation'}
    if is_bash and wrapper_path(path, rules):
        if not proc.exe or not proc.cwd or proc.error or Path(proc.exe).resolve() != Path('/usr/bin/bash').resolve() or len(args) < 5:
            return {**result, 'kind': 'ambiguous', 'reason': 'known wrapper execution with incomplete identity/arguments'}
        job, work, lock, *payload = args
        payload_process = Process(proc.pid, payload[0], cwd, tuple(payload), proc.start_ticks, proc.boot_id)
        valid_job = resolve(job, cwd).is_relative_to(rules.tasks.resolve())
        if (valid_job and Path(cwd).resolve() == rules.repo.resolve()
                and resolve(work, cwd) == rules.repo.resolve()
                and resolve(lock, cwd) == rules.external_lock.resolve()
                and classify(payload_process, rules)['kind'] == 'runner'):
            return {**result, 'kind': 'wrapper', 'reason': 'Bash executing exact task wrapper with exact payload/cwd/lock'}
        return {**result, 'kind': 'ambiguous', 'reason': 'known wrapper execution with unexpected payload/cwd/lock'}
    return result


def stat_fields(path: Path) -> list[str]:
    return path.read_text().rsplit(') ', 1)[1].split()


def read_process(pid: int, boot: str, proc_root: Path = Path('/proc')) -> Process | None:
    base = proc_root / str(pid)
    try:
        first = stat_fields(base / 'stat')
        argv = tuple(a.decode(errors='replace') for a in (base / 'cmdline').read_bytes().split(b'\0') if a)
        error = None
        try:
            exe, cwd = os.readlink(base / 'exe'), os.readlink(base / 'cwd')
        except PermissionError:
            exe = cwd = None
            error = 'permission denied resolving exe/cwd'
        last = stat_fields(base / 'stat')
        if first[19] != last[19]:
            return None  # PID changed during snapshot; never combine identities.
        return Process(pid, exe, cwd, argv, int(last[19]), boot, last[0], int(last[1]), int(last[2]), int(last[3]), error)
    except (FileNotFoundError, ProcessLookupError):
        return None


def recorded_identity(record: dict, current: Process | None) -> str:
    if current is None or current.state in ('Z', 'X'):
        return 'inactive'
    if int(record['pid']) != current.pid or int(record['start_ticks']) != current.start_ticks:
        return 'pid_reused'
    if not record.get('boot_id'):
        return 'ambiguous_legacy_identity'
    if record['boot_id'] != current.boot_id:
        return 'previous_boot'
    return 'active_recorded_identity'


def process_gate(rules: Rules = Rules(), proc_root: Path = Path('/proc')) -> dict:
    boot = (proc_root / 'sys/kernel/random/boot_id').read_text().strip()
    processes, denied = {}, []
    for directory in proc_root.glob('[0-9]*'):
        try:
            process = read_process(int(directory.name), boot, proc_root)
        except PermissionError:
            denied.append(int(directory.name))
            continue
        if process is not None:
            processes[process.pid] = process
    blockers = []
    for process in processes.values():
        verdict = classify(process, rules)
        if verdict['kind'] != 'unrelated':
            blockers.append({**verdict, 'identity': asdict(process)})
    for identity_file in sorted(rules.tasks.glob('*/*.identity')):
        if identity_file.name not in ('launcher.identity', 'runner.identity'):
            continue
        # Only R18-C2 task records belong to this experiment's PID evidence.
        if '__r18c2-' not in identity_file.parent.name:
            continue
        raw = identity_file.read_text().strip()
        try:
            if raw.startswith('{'):
                record = json.loads(raw)
            else:
                pid, ticks = raw.split()
                boot_file = identity_file.parent / 'boot-id.txt'
                record = {'pid': int(pid), 'start_ticks': int(ticks), 'boot_id': boot_file.read_text().strip() if boot_file.exists() else None}
            pid = int(record['pid'])
            if pid in denied:
                blockers.append({'kind': 'ambiguous', 'pid': pid, 'reason': 'recorded process cannot be inspected', 'record': str(identity_file)})
                continue
            verdict = recorded_identity(record, processes.get(pid))
            if verdict in ('active_recorded_identity', 'ambiguous_legacy_identity'):
                blockers.append({'kind': verdict, 'pid': pid, 'record': str(identity_file), 'identity': asdict(processes[pid])})
        except (ValueError, KeyError, TypeError) as exc:
            raise RuntimeError(f'malformed recorded identity {identity_file}: {type(exc).__name__}') from exc
    return {'blockers': blockers, 'processes_inspected': len(processes), 'unreadable_unattributed_pids': denied, 'boot_id': boot}


def probe_lock(path: Path, *, required: bool) -> str:
    try:
        fd = os.open(path, os.O_RDONLY)
    except FileNotFoundError:
        if required:
            raise RuntimeError(f'required lock missing: {path}')
        return 'absent (not created)'
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError(f'lock held: {path}') from exc
        fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)
    return 'available at probe time; immediately released'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def preflight() -> dict:
    def git(*args: str) -> str:
        return subprocess.check_output(['git', *args], cwd=REPO, text=True).strip()
    require(git('branch', '--show-current') == 'codex/progress-aware-recovery', 'scientific branch differs')
    require(git('rev-parse', 'HEAD') == SHA, 'scientific HEAD differs')
    require(git('rev-parse', 'origin/codex/progress-aware-recovery') == SHA, 'scientific remote differs; fetch before preflight')
    require(not git('status', '--porcelain=v1'), 'scientific worktree dirty')
    require(Path(sys.executable).resolve() == PYTHON.resolve(), 'wrong Python environment')
    expected = {'ALFWORLD_DATA': '/home/lizening/alfworld_data', 'ALFWORLD_CONFIG_PATH': str(REPO / 'configs/local/alfworld_base_university.yaml'), 'TOKENIZERS_PARALLELISM': 'false', 'PYTHONPATH': '.'}
    for key, value in expected.items():
        require(os.environ.get(key) == value, f'environment mismatch: {key}')
    require(Path(expected['ALFWORLD_DATA']).is_dir(), 'data directory missing')
    require(Path(expected['ALFWORLD_CONFIG_PATH']).is_file(), 'config missing')
    require((REPO / 'artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter').is_dir(), 'adapter missing')
    baseline = json.loads((HERE / 'baseline-runtime.json').read_text())
    files = {str(f.relative_to(RUNTIME)): hashlib.sha256(f.read_bytes()).hexdigest() for f in RUNTIME.rglob('*') if f.is_file()}
    require(files == {k: v['sha256'] for k, v in baseline['files'].items()}, 'runtime changed since audited baseline')
    manifest = json.loads((RUNTIME / 'run_manifest.json').read_text())
    require(manifest['status'] == 'initialized' and manifest['provenance']['implementation_commit'] == SHA, 'manifest state/provenance changed')
    for field in ('accepted_branches', 'completed_branch_reruns', 'incomplete_branch_retries', 'operational_interruptions'):
        require(manifest[field] == 0, f'manifest counter changed: {field}')
    for name in baseline['formal_reports']:
        require(not (REPO / 'reports' / name).exists(), f'formal report exists: {name}')
    control = REPO / 'artifacts/runtime/progress-aware-r18-c2-control'
    for name, evidence in baseline['control'].items():
        if isinstance(evidence, dict):
            path = control / name
            require(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == evidence['sha256'], f'control state changed: {name}')
    require(json.loads((control / 'experiment.json').read_text()) == {'project_root': str(REPO), 'runtime': str(RUNTIME)}, 'owner differs')
    scan = process_gate()
    require(not scan['blockers'], 'active/ambiguous R18-C2 identity: ' + json.dumps(scan['blockers']))
    locks = {'scientific': probe_lock(control / 'writer.lock', required=True), 'external': probe_lock(Rules().external_lock, required=False)}
    return {'preflight': 'PASS', 'sha': SHA, 'manifest_status': 'initialized', 'accepted_branches': 0, 'ledger_rows': 0, 'process_scan': scan, 'locks': locks, 'scientific_calls': 0}


if __name__ == '__main__':
    try:
        print(json.dumps(preflight(), indent=2))
    except (RuntimeError, OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print('STOP: ' + str(exc), file=sys.stderr)
        raise SystemExit(65)
