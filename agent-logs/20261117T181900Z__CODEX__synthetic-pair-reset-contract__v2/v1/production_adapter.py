"""Test-only binding to pinned production port code with synthetic CASES.

This is deliberately not a real-run launcher or a production admission gate.
"""
import hashlib
import inspect
import os
from pathlib import Path
import stat
import sys
import types

SOURCE_SHA256 = 'a1c5d80d58d0b4219ed813f7d61e30fe0e1a02ddca273f93b6734799e491e20e'

class BindingError(ValueError):
    pass

def load_synthetic_bound(source_path, fixture_root, synthetic_cases, expected_sha=SOURCE_SHA256):
    """Execute exact checked source bytes; replace `forward_specs.CASES` for fixtures.

    No import of the real forward_specs. This synthetic-only binding never claims
    the real CASES registry, production roster, or genuine task assets were checked.
    """
    source_path=Path(source_path)
    fixture_root=Path(fixture_root).resolve(strict=True)
    if not source_path.is_absolute() or not fixture_root.is_dir() or not synthetic_cases:
        raise BindingError('fixture/source shape')
    fd=os.open(source_path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
    try:
        before=os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_size>1_000_000: raise BindingError('source shape')
        with os.fdopen(fd,'rb',closefd=False) as source: raw=source.read(1_000_001)
        after=os.fstat(fd)
        if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns):
            raise BindingError('source drift')
    finally: os.close(fd)
    if hashlib.sha256(raw).hexdigest()!=expected_sha or expected_sha != SOURCE_SHA256:
        raise BindingError('source hash mismatch')
    for key, spec in synthetic_cases.items():
        if not isinstance(key,str) or spec.get('family')!='two': raise BindingError('fixture case')
        for value in spec['inputs'].values():
            path=Path(value['path'])
            if not path.is_absolute() or '..' in path.parts or not path.resolve(strict=True).is_relative_to(fixture_root):
                raise BindingError('input outside fixture root')
    fake=types.ModuleType('forward_specs')
    fake.CASES=synthetic_cases
    module=types.ModuleType('eprime_ports_synthetic_bound')
    module.__file__=str(source_path)
    prior=sys.modules.get('forward_specs')
    try:
        sys.modules['forward_specs']=fake
        exec(compile(raw,str(source_path),'exec'),module.__dict__)
    finally:
        if prior is None: sys.modules.pop('forward_specs',None)
        else: sys.modules['forward_specs']=prior
    if (module.CASES is not synthetic_cases or module.materialize.__code__.co_filename != str(source_path) or
        module.verify_materialized.__code__.co_filename != str(source_path)):
        raise BindingError('wrong functions/registry')
    if str(inspect.signature(module.materialize)) != '(output, manifest, journal, *, family)':
        raise BindingError('materialize signature')
    if str(inspect.signature(module.verify_materialized)) != '(game, config_path, dataset, manifest, journal, phase)':
        raise BindingError('verify signature')

    def setup(output, inputs, journal, *, family):
        if inputs not in [spec['inputs'] for spec in synthetic_cases.values()]: raise BindingError('unregistered fixture')
        if not Path(output).resolve(strict=True).is_relative_to(fixture_root): raise BindingError('output outside fixture')
        return module.materialize(output, inputs, journal, family=family)

    def verify(game, config, dataset, inputs, journal, phase):
        if inputs not in [spec['inputs'] for spec in synthetic_cases.values()]: raise BindingError('unregistered fixture')
        return module.verify_materialized(game, config, dataset, inputs, journal, phase)

    return setup, verify, module
