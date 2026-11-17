"""Direct-child-only synthetic cleanup observation; not host/GPU ownership proof."""
from dataclasses import dataclass
import os
from pathlib import Path
import subprocess

class CleanupUnknown(RuntimeError):pass

@dataclass(frozen=True)
class Receipt:
    pid:int
    start_tick:int
    process_group:int
    returncode:int
    visible_group_members:tuple
    scope:str='CURRENT_PROCFS_ONLY;HIDDEN_DESCENDANTS_AND_GPU_UNKNOWN'

def identity(pid):
    try:
        raw=(Path('/proc')/str(pid)/'stat').read_text()
        tail=raw[raw.rfind(')')+1:].split()
        return {'state':tail[0],'ppid':int(tail[1]),'pgid':int(tail[2]),'sid':int(tail[3]),'start':int(tail[19])}
    except (OSError,ValueError,IndexError) as error:raise CleanupUnknown('direct process identity unknown') from error

def capture_owned(proc):
    info=identity(proc.pid)
    if info['ppid']!=os.getpid() or info['pgid']!=proc.pid or info['sid']!=proc.pid:
        raise CleanupUnknown('not own direct session leader')
    return info

def members(pgid):
    found=[]
    for item in Path('/proc').iterdir():
        if not item.name.isdigit():continue
        try:
            raw=(item/'stat').read_text();tail=raw[raw.rfind(')')+1:].split()
            if int(tail[2])==pgid:found.append(int(item.name))
        except FileNotFoundError:continue
        except (OSError,ValueError,IndexError) as error:raise CleanupUnknown('procfs visibility incomplete') from error
    return tuple(sorted(found))

def stop_direct_if_same(proc, original):
    """Signal only our verified live direct child; never signal a group or other PID."""
    if proc.poll() is not None:return
    now=identity(proc.pid)
    if (now['ppid'],now['pgid'],now['sid'],now['start']) != (os.getpid(),original['pgid'],original['sid'],original['start']):
        raise CleanupUnknown('direct child identity changed; no signal sent')
    proc.terminate()
    try:proc.wait(timeout=2)
    except subprocess.TimeoutExpired:raise CleanupUnknown('own child termination unconfirmed')

def finish_owned(proc,original,timeout):
    try:rc=proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired as error:
        stop_direct_if_same(proc,original)
        raise CleanupUnknown('direct child exceeded deadline; batch must stop') from error
    if rc!=0:raise CleanupUnknown('direct child failed; batch must stop')
    visible=members(original['pgid'])
    if visible:raise CleanupUnknown('visible process-group member remains')
    return Receipt(proc.pid,original['start'],original['pgid'],rc,visible)
