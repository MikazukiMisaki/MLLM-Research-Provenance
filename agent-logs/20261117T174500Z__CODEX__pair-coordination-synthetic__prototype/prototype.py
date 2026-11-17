"""CPU-only synthetic coordinator: not connected to a scientific runtime."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

PAIRS = ('one', 'two', 'three', 'four')
LIMITS = {'setup': 4, 'arm': 8}

class Stop(Exception):
    pass

def encode(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def digest(x):
    return hashlib.sha256(x).hexdigest()

class Owner:
    def __init__(self, directory):
        self.root = Path(directory)
        self.root.mkdir(mode=0o700, parents=True, exist_ok=True)
        # A durable, exclusive, non-reusable claim prevents another owner and resume.
        try:
            fd = os.open(self.root / 'claim', os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
        except FileExistsError as exc:
            raise Stop('existing claim: no second owner or resume') from exc
        try:
            os.write(fd, b'CPU SYNTHETIC ONLY; DO NOT RESUME\n')
            os.fsync(fd)
        finally:
            os.close(fd)
        dfd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
        self.journal = self.root / 'ledger.jsonl'
        self.prev = '0' * 64
        self.seq = 0
        self.reserved = {}
        self.returned = set()
        self.closed = False

    def append(self, event, data):
        if self.seq:
            seen = audit(self.journal)
            if (seen['previous'] != self.prev or seen['seq'] != self.seq or
                seen['reserved'] != self.reserved or seen['returned'] != self.returned or seen['complete']):
                raise Stop('journal changed or became inconsistent')
        elif self.journal.exists():
            raise Stop('unexpected preexisting journal')
        row = {'seq': self.seq + 1, 'previous': self.prev, 'event': event, 'data': data}
        h = digest(encode(row))
        fd = os.open(self.journal, os.O_CREAT | os.O_APPEND | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
        try:
            view = memoryview(encode(dict(row, hash=h)) + b'\n')
            while view:
                n = os.write(fd, view)
                if n <= 0:
                    raise OSError('short write')
                view = view[n:]
            os.fsync(fd)
        finally:
            os.close(fd)
        dfd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
        self.seq += 1
        self.prev = h

    def reserve(self, kind, pair, arm=None):
        key = (kind, pair, arm)
        if (self.closed or kind not in LIMITS or pair not in PAIRS or
            (kind == 'setup' and arm is not None) or (kind == 'arm' and arm not in ('A', 'B')) or
            key in self.reserved or len(self.reserved.keys() - self.returned) or
            sum(k[0] == kind for k in self.reserved) >= LIMITS[kind] or
            (kind == 'arm' and ('setup', pair, None) not in self.returned)):
            raise Stop('invalid, duplicate, open or over-limit operation')
        token = digest(os.urandom(32))
        self.append('reserve', {'kind': kind, 'pair': pair, 'arm': arm, 'token': token})
        self.reserved[key] = token
        return token

    def returned_effect(self, kind, pair, arm, token, receipt):
        key = (kind, pair, arm)
        if key not in self.reserved or key in self.returned or self.reserved[key] != token:
            raise Stop('unmatched return')
        self.append('return', {'kind': kind, 'pair': pair, 'arm': arm, 'token': token, 'receipt': receipt})
        self.returned.add(key)

    def complete(self):
        if self.reserved.keys() - self.returned or len(self.returned) != 12:
            raise Stop('incomplete batch')
        self.append('complete', {})
        self.closed = True

def effect(owner, kind, pair, arm, task_hash, fail=False):
    token = owner.reserve(kind, pair, arm)  # fsynced before child starts
    cmd = [sys.executable, '-I', '-B', __file__, '--child', kind, pair, arm or '-', task_hash, 'fail' if fail else 'ok']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Stop('child unknown; reservation retained') from exc
    if result.returncode:
        raise Stop('child failed; reservation retained')
    try:
        receipt = json.loads(result.stdout)
        expected = {'kind': kind, 'pair': pair, 'arm': arm, 'task_hash': task_hash}
        if {k: receipt[k] for k in expected} != expected or type(receipt['pid']) is not int or set(receipt) != set(expected) | {'pid'}:
            raise ValueError('receipt mismatch')
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise Stop('invalid receipt; reservation retained') from exc
    owner.returned_effect(kind, pair, arm, token, receipt)
    return receipt

def run(root, fail_on=None):
    owner = Owner(root)
    for i, pair in enumerate(PAIRS):
        task_hash = digest(encode({'synthetic_pair': pair}))
        effect(owner, 'setup', pair, None, task_hash, fail_on == ('setup', pair, None))
        for arm in (('A', 'B') if i % 2 == 0 else ('B', 'A')):
            effect(owner, 'arm', pair, arm, task_hash, fail_on == ('arm', pair, arm))
    owner.complete()
    return owner

def audit(path):
    raw = Path(path).read_bytes()
    if not raw or not raw.endswith(b'\n'):
        raise Stop('incomplete ledger')
    previous = '0' * 64
    reserved, returned = {}, set()
    complete = False
    try:
        for seq, line in enumerate(raw.splitlines(), 1):
            row = json.loads(line)
            h = row.pop('hash')
            if row['seq'] != seq or row['previous'] != previous or digest(encode(row)) != h or complete:
                raise ValueError('hash chain or order')
            previous = h
            data, event = row['data'], row['event']
            if event == 'reserve':
                key = (data['kind'], data['pair'], data['arm'])
                if (key[0] not in LIMITS or key[1] not in PAIRS or key in reserved or reserved.keys() - returned or
                    sum(k[0] == key[0] for k in reserved) >= LIMITS[key[0]] or
                    (key[0] == 'setup' and key[2] is not None) or
                    (key[0] == 'arm' and (key[2] not in ('A','B') or ('setup', key[1], None) not in returned))):
                    raise ValueError('invalid reservation')
                reserved[key] = data['token']
            elif event == 'return':
                key = (data['kind'], data['pair'], data['arm'])
                if key not in reserved or key in returned or data['token'] != reserved[key] or not isinstance(data['receipt'], dict):
                    raise ValueError('invalid return')
                returned.add(key)
            elif event == 'complete':
                if reserved.keys() - returned or len(returned) != 12 or data != {}:
                    raise ValueError('invalid completion')
                complete = True
            else:
                raise ValueError('unknown event')
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise Stop('invalid ledger') from exc
    return {'reserved': reserved, 'returned': returned, 'complete': complete, 'previous': previous, 'seq': seq}

if __name__ == '__main__':
    if len(sys.argv) != 7 or sys.argv[1] != '--child':
        raise SystemExit('Only synthetic child invocation is supported.')
    kind, pair, arm, task_hash, mode = sys.argv[2:]
    if mode == 'fail':
        raise SystemExit(7)
    print(encode({'kind': kind, 'pair': pair, 'arm': None if arm == '-' else arm,
                  'task_hash': task_hash, 'pid': os.getpid()}).decode())
