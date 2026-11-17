"""FICTIONAL CPU-only checkpoint callback; not a production trainer or sandbox."""
import ctypes
import errno
import hashlib
import json
import os
from pathlib import Path
import tempfile
import torch
from safetensors import safe_open
from safetensors.torch import save_file

SCOPE='FICTIONAL_CPU_ONLY_NOT_LORA_NOT_SCIENCE'
FINAL_STEP=16
class CheckpointRejected(ValueError):pass

def fsync_dir(path):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)
def fsync_file(path):
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)
def sha_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(65536),b''):h.update(block)
    return h.hexdigest()
def verify_reload(path,expected,step,expected_sha):
    if sha_file(path)!=expected_sha:raise RuntimeError('digest mismatch')
    with safe_open(str(path),framework='pt',device='cpu') as reader:
        if reader.metadata()!={'scope':SCOPE,'step':str(step)} or set(reader.keys())!=set(expected):
            raise RuntimeError('metadata or key mismatch')
        for name,want in expected.items():
            observed=reader.get_tensor(name)
            if (observed.dtype!=want.dtype or observed.shape!=want.shape or
                not torch.equal(observed.contiguous().view(torch.uint8),want.view(torch.uint8))):
                raise RuntimeError('reloaded tensor mismatch')
    if sha_file(path)!=expected_sha:raise RuntimeError('post-read digest mismatch')
def rename_noreplace(src,dst):
    libc=ctypes.CDLL(None,use_errno=True)
    if not hasattr(libc,'renameat2'):raise OSError(errno.ENOSYS,'renameat2 unavailable')
    fn=libc.renameat2;fn.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint]
    fn.restype=ctypes.c_int
    if fn(-100,os.fsencode(src),-100,os.fsencode(dst),1)!=0:
        code=ctypes.get_errno();raise OSError(code,os.strerror(code))

class FictionalFinalCheckpoint:
    def __init__(self,target):
        self.target=Path(target);self.attempted=False
        self.status='NOT_ATTEMPTED';self.temp_path=None;self.receipt=None
    def __call__(self,step,tensors,*,after_temp_sync=None):
        if self.attempted:raise CheckpointRejected('single use; no retry')
        self.attempted=True;self.status='REJECTED'
        if type(step) is not int or step!=FINAL_STEP:
            raise CheckpointRejected('not final step')
        if (not self.target.is_absolute() or self.target.parent.resolve(strict=True)!=self.target.parent or
            self.target.name in ('','.','..') or os.path.lexists(self.target)):
            raise CheckpointRejected('target exists or path invalid')
        if type(tensors) is not dict or not tensors:raise CheckpointRejected('empty fake tensors')
        frozen={}
        for name,value in tensors.items():
            if (type(name) is not str or not name.startswith('fictional.') or not isinstance(value,torch.Tensor) or
                value.device.type!='cpu' or value.dtype not in (torch.float32,torch.float64,torch.int64) or value.ndim<1 or
                not bool(torch.isfinite(value).all().item())):
                raise CheckpointRejected('fictional finite CPU tensors only')
            frozen[name]=value.detach().contiguous().clone()
        self.status='UNKNOWN'
        try:
            self.temp_path=Path(tempfile.mkdtemp(prefix='.'+self.target.name+'.pending-',dir=self.target.parent))
            fsync_dir(self.target.parent)
            weight=self.temp_path/'fictional.safetensors'
            save_file(frozen,str(weight),metadata={'scope':SCOPE,'step':str(step)})
            os.chmod(weight,0o400);fsync_file(weight)
            before=sha_file(weight);fsync_dir(self.temp_path);verify_reload(weight,frozen,step,before)
            if after_temp_sync is not None:after_temp_sync()
            rename_noreplace(self.temp_path,self.target);fsync_dir(self.target.parent)
            final_weight=self.target/'fictional.safetensors'
            verify_reload(final_weight,frozen,step,before)
            # On-disk receipt never claims final confirmation: a later fsync may
            # fail or the process may die before returning to its owning caller.
            receipt={'scope':SCOPE,'status':'RELOAD_CHECKED_CALLBACK_RETURN_REQUIRED','step':step,'sha256':before,
                     'keys':sorted(frozen),'format':'safetensors','scientific_use':'HOLD'}
            data=(json.dumps(receipt,sort_keys=True)+'\n').encode()
            fd=os.open(self.target/'receipt.json',os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o400)
            try:
                view=memoryview(data)
                while view:
                    n=os.write(fd,view)
                    if n<=0:raise OSError('short receipt write')
                    view=view[n:]
                os.fsync(fd)
            finally:os.close(fd)
            fsync_dir(self.target);fsync_dir(self.target.parent)
            self.receipt=receipt;self.status='CONFIRMED_FICTIONAL_ONLY'
            return dict(receipt,callback_status=self.status)
        except BaseException:
            self.status='UNKNOWN'
            raise
