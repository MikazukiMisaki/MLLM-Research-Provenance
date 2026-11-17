"""Research coordination INTERFACE CANDIDATE; test-only adapters; never a launcher.

No production implementation is imported here. No authorization is provided.
"""
import hashlib
import json
import os
from pathlib import Path
import socket
import stat
import subprocess

# Fictitious fixed schedule. Production schedule binding is NOT implemented.
SCHEDULE = (('one', ('A','B')), ('two', ('B','A')),
            ('three', ('A','B')), ('four', ('B','A')))
PAIRS = tuple(pair for pair, _ in SCHEDULE)
GLOBAL_CAP = {'materialize': 4, 'env_construct': 8, 'env_init': 8, 'reset': 8,
              'model_load': 8, 'generation': 400, 'step': 400}
ARM_CAP = {'env_construct': 1, 'env_init': 1, 'reset': 1, 'model_load': 1,
           'generation': 50, 'step': 50}

class Stop(RuntimeError):
    pass

def wire(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def sha(data):
    return hashlib.sha256(data).hexdigest()

class Owner:
    """One lifetime, one journal, no crash recovery or retry."""
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        try:
            fd = os.open(self.root/'claim', os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW, 0o600)
        except FileExistsError as e:
            raise Stop('already claimed: no retry') from e
        try:
            os.write(fd, b'INTERFACE CANDIDATE; NO RESUME\n')
            os.fsync(fd)
        finally:
            os.close(fd)
        self._syncdir()
        self.log = self.root/'budget.jsonl'
        self.prev, self.seq = '0'*64, 0
        self.count = {k: 0 for k in GLOBAL_CAP}
        self.local = {}
        self.open = None
        self.used_setup = set()
        self.used_arm = set()
        self.returned_setup = set()
        self.prepared = set()
        self.states = {}
        self.returned_local = {}
        self.pair_index = 0
        self.finished = False
        self.failed = False

    def _syncdir(self):
        fd = os.open(self.root, os.O_RDONLY|os.O_DIRECTORY)
        try: os.fsync(fd)
        finally: os.close(fd)

    def write(self, typ, data):
        if self.finished or self.failed: raise Stop('closed or failed')
        if self.seq:
            parsed = inspect_log(self.log)
            if parsed['seq'] != self.seq or parsed['hash'] != self.prev:
                raise Stop('journal mismatch')
        elif self.log.exists(): raise Stop('unexpected prior log')
        item = {'seq': self.seq+1, 'previous': self.prev, 'type': typ, 'data': data}
        h = sha(wire(item)); line = wire(dict(item, hash=h)) + b'\n'
        fd = os.open(self.log, os.O_WRONLY|os.O_CREAT|os.O_APPEND|os.O_NOFOLLOW, 0o600)
        try:
            view = memoryview(line)
            while view:
                n = os.write(fd, view)
                if n <= 0: raise OSError('short write')
                view = view[n:]
            os.fsync(fd)
        finally: os.close(fd)
        self._syncdir(); self.seq += 1; self.prev = h

    def expected_pair(self):
        if self.pair_index >= len(SCHEDULE): raise Stop('schedule exhausted')
        return SCHEDULE[self.pair_index]

    def expected_arm(self):
        pair, order = self.expected_pair()
        if self.states.get((pair,order[0])) != 'closed': return pair, order[0]
        return pair, order[1]

    def reserve(self, pair, arm, kind):
        if (self.failed or self.finished or self.open is not None or pair not in PAIRS or kind not in GLOBAL_CAP or
            self.count[kind] >= GLOBAL_CAP[kind]): raise Stop('budget/ambiguous reservation')
        if kind == 'materialize':
            if arm is not None or pair in self.used_setup or pair != self.expected_pair()[0]: raise Stop('duplicate or out-of-order setup')
        else:
            if ((pair,arm) != self.expected_arm() or self.states.get((pair,arm)) != 'started' or
                arm not in ('A','B') or (pair, arm) not in self.used_arm): raise Stop('unbound or out-of-order arm')
            local = self.local[(pair,arm)]
            if local[kind] >= ARM_CAP[kind]: raise Stop('arm cap')
            returned = self.returned_local[(pair,arm)]
            required = {'env_init':'env_construct','reset':'env_init','model_load':'reset','generation':'model_load','step':'generation'}
            if kind in required and returned[required[kind]] < 1: raise Stop('lifecycle order')
        token = sha(os.urandom(32))
        item = {'pair':pair, 'arm':arm, 'kind':kind, 'token':token}
        self.write('reserve',item)
        self.count[kind] += 1
        if arm is None: self.used_setup.add(pair)
        else: self.local[(pair,arm)][kind] += 1
        self.open = item
        return token

    def returned(self, token, receipt):
        if self.open is None or self.open['token'] != token: raise Stop('unmatched return')
        self.write('return', dict(self.open, receipt=receipt))
        if self.open['kind'] == 'materialize': self.returned_setup.add(self.open['pair'])
        else: self.returned_local[(self.open['pair'],self.open['arm'])][self.open['kind']] += 1
        self.open = None

    def mark_pre(self, pair, arm):
        if (self.failed or self.finished or self.open is not None or pair not in self.returned_setup or
            (pair,arm) != self.expected_arm() or (pair,arm) in self.prepared):
            raise Stop('invalid pre-verification')
        self.write('arm_pre_verified', {'pair':pair,'arm':arm})
        self.prepared.add((pair,arm))

    def start_arm(self, pair, arm):
        if (self.failed or self.finished or self.open is not None or (pair,arm) != self.expected_arm() or
            (pair,arm) not in self.prepared or (pair,arm) in self.used_arm or arm not in ('A','B')):
            raise Stop('bad arm start')
        self.write('arm_start', {'pair':pair,'arm':arm})
        self.used_arm.add((pair,arm))
        self.local[(pair,arm)] = {k:0 for k in ARM_CAP}
        self.returned_local[(pair,arm)] = {k:0 for k in ARM_CAP}
        self.states[(pair,arm)] = 'started'

    def outcome(self, pair, arm, won):
        key=(pair,arm)
        if self.failed or self.finished or self.open is not None or self.states.get(key) != 'started' or type(won) is not bool:
            raise Stop('invalid outcome')
        returned=self.returned_local[key]
        if any(returned[k] != 1 for k in ('env_construct','env_init','reset','model_load')) or returned['generation'] < 1:
            raise Stop('required completed lifecycle missing')
        # step=0 is legitimate for a policy-format failure.
        self.write('arm_result', {'pair':pair,'arm':arm,'won':won})
        self.states[key]='outcome'

    def verified(self, pair, arm):
        key=(pair,arm)
        if self.states.get(key) != 'outcome' or self.open is not None: raise Stop('no outcome to verify')
        self.write('arm_post_verified', {'pair':pair,'arm':arm})
        self.states[key]='verified'

    def close_arm(self, pair, arm):
        key=(pair,arm)
        if self.states.get(key) != 'verified' or self.open is not None: raise Stop('arm not verified')
        self.write('arm_closed', {'pair':pair,'arm':arm})
        self.states[key]='closed'
        expected_pair, order = self.expected_pair()
        if pair == expected_pair and all(self.states.get((pair,a)) == 'closed' for a in order):
            self.pair_index += 1

    def abort(self, reason):
        if self.finished or self.failed: return
        try:
            self.write('batch_aborted', {'reason':reason,'open':self.open})
        except BaseException:
            pass
        finally:
            self.failed = True

    def complete(self):
        expected={(pair,arm) for pair in PAIRS for arm in ('A','B')}
        if (self.failed or self.finished or self.open is not None or self.pair_index != len(SCHEDULE) or self.returned_setup != set(PAIRS) or
            set(self.states) != expected or any(self.states[k] != 'closed' for k in expected)):
            raise Stop('batch incomplete or failed')
        self.write('complete', {'counts':self.count.copy()}); self.finished=True

def inspect_log(path):
    raw=Path(path).read_bytes()
    if not raw or not raw.endswith(b'\n'): raise Stop('truncated journal')
    prev='0'*64
    try:
        for seq,line in enumerate(raw.splitlines(),1):
            row=json.loads(line); h=row.pop('hash')
            if row['seq'] != seq or row['previous'] != prev or sha(wire(row)) != h: raise ValueError()
            prev=h
    except (ValueError,KeyError,TypeError,json.JSONDecodeError) as e: raise Stop('corrupt journal') from e
    return {'seq':seq,'hash':prev}

def file_identity(path, root):
    path=Path(path)
    if not path.is_absolute() or '..' in path.parts or '..' in root.parts or not path.is_relative_to(root): raise Stop('unbound path')
    # Refuse symlink at any component. This is not a race-free kernel isolation primitive.
    rel=path.relative_to(root); current=root
    if root.is_symlink(): raise Stop('symlink root')
    for component in rel.parts:
        current=current/component
        if current.is_symlink(): raise Stop('symlink component')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        st=os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_size>1_000_000: raise Stop('file shape')
        with os.fdopen(fd,'rb',closefd=False) as f: content=f.read(1_000_001)
        after=os.fstat(fd)
        if (st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns):
            raise Stop('file changed while reading')
        return {'path':str(path),'sha256':sha(content)}
    finally: os.close(fd)

def snapshot(paths, root):
    game, config, dataset = map(Path, paths)
    if not dataset.is_absolute() or '..' in dataset.parts or '..' in root.parts or not dataset.is_relative_to(root): raise Stop('dataset containment')
    if game != dataset/'authored-eprime-only'/'game.tw-pddl': raise Stop('game layout')
    if sorted(p.name for p in dataset.iterdir()) != ['authored-eprime-only'] or sorted(p.name for p in game.parent.iterdir()) != ['game.tw-pddl','traj_data.json']:
        raise Stop('dataset inventory')
    return [file_identity(p,root) for p in (game,game.parent/'traj_data.json',config)]

def _pair(owner, pair_id, order, inputs, setup, verify, spawn):
    """Callback interfaces mirror materialize/verify; spawn is deliberately abstract.

    setup(output, inputs, journal, family='two') -> (game,config,dataset).
    verify(game,config,dataset,inputs,journal,phase) -> None.
    spawn(pair,arm,paths,fd) -> a supervised child (Popen-compatible).
    Production resource and model bindings are NOT implemented.
    """
    if (pair_id, tuple(order)) != owner.expected_pair(): raise Stop('pair/order differs from frozen schedule')
    root=owner.root/('pair-'+pair_id); root.mkdir(mode=0o700)
    token=owner.reserve(pair_id,None,'materialize')
    def journal(event, payload): owner.write('setup_detail', {'event':event,'payload':payload})
    paths=setup(root,inputs,journal,family='two')
    if not isinstance(paths,tuple) or len(paths)!=3: raise Stop('setup receipt')
    bound=snapshot(paths,root)
    owner.returned(token,{'paths':bound})
    expected=None
    for arm in order:
        verify(*paths,inputs,journal,'pre')
        if snapshot(paths,root)!=bound: raise Stop('input mismatch before arm')
        owner.mark_pre(pair_id,arm)
        owner.start_arm(pair_id,arm)
        parent,child=socket.socketpair()
        proc=None
        initial=None
        try:
            parent.settimeout(10)
            proc=spawn(pair_id,arm,paths,child.fileno())
            child.close()
            with parent.makefile('rwb',buffering=0) as f:
                while True:
                    raw=f.readline(65537)
                    if not raw or len(raw)>65536: raise Stop('missing or oversized child receipt')
                    msg=json.loads(raw)
                    typ=msg.get('type')
                    if typ=='reserve':
                        kind=msg['kind']
                        if kind in ('model_load','generation','step') and initial is None:
                            raise Stop('public initial not verified')
                        reply={'token':owner.reserve(pair_id,arm,kind)}
                    elif typ=='return':
                        owner.returned(msg['token'],msg.get('receipt')); reply={'ok':True}
                    elif typ=='initial':
                        if initial is not None or owner.open is not None or owner.local[(pair_id,arm)]['reset']!=1:
                            raise Stop('invalid initial')
                        initial=msg['state']
                        if not isinstance(initial,dict) or (expected is not None and wire(initial)!=wire(expected)):
                            raise Stop('initial mismatch')
                        owner.write('initial',{'pair':pair_id,'arm':arm,'state':initial}); reply={'ok':True}
                    elif typ=='done':
                        if owner.open is not None or initial is None or not isinstance(msg.get('won'),bool): raise Stop('unknown outcome')
                        owner.outcome(pair_id,arm,msg['won']); reply={'ok':True}
                        f.write(wire(reply)+b'\n'); break
                    else: raise Stop('unknown child message')
                    f.write(wire(reply)+b'\n')
            if proc.wait(timeout=10)!=0: raise Stop('child exit failure')
        except BaseException:
            # Ownership and descendant cleanup are NOT implemented. Preserve unknown state.
            if proc is not None and proc.poll() is None:
                proc.terminate()
                try: proc.wait(timeout=3)
                except subprocess.TimeoutExpired: pass
            raise
        finally:
            parent.close(); child.close()
        verify(*paths,inputs,journal,'post')
        if snapshot(paths,root)!=bound: raise Stop('input mismatch after arm')
        owner.verified(pair_id,arm)
        owner.close_arm(pair_id,arm)
        if expected is None: expected=initial
    return bound


def pair(owner, pair_id, order, inputs, setup, verify, spawn):
    if owner.failed or owner.finished:
        raise Stop('owner cannot continue')
    try:
        return _pair(owner, pair_id, order, inputs, setup, verify, spawn)
    except BaseException as error:
        owner.abort(type(error).__name__)
        raise
