#!/usr/bin/env python3
"""Parse only safetensors JSON headers; never map/read tensor payloads."""
import json,struct
from pathlib import Path
SNAP=Path('/home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218')
ADAPTER=Path('/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter/adapter_model.safetensors')
SIZES={'BOOL':1,'U8':1,'I8':1,'F8_E4M3':1,'F8_E5M2':1,'U16':2,'I16':2,'F16':2,'BF16':2,'U32':4,'I32':4,'F32':4,'U64':8,'I64':8,'F64':8}
def header(path):
 with path.open('rb') as f:
  nbuf=f.read(8)
  if len(nbuf)!=8: raise ValueError(f'bad safetensors header prefix: {path.name}')
  n=struct.unpack('<Q',nbuf)[0]
  raw=f.read(n)
  if len(raw)!=n: raise ValueError(f'truncated safetensors header: {path.name}')
 d=json.loads(raw)
 by_dtype={}; tensors=0; params=0; tensor_bytes=0
 for name,desc in d.items():
  if name=='__metadata__': continue
  dtype=desc['dtype']; shape=desc['shape']; count=1
  for dim in shape: count*=dim
  tensors+=1; params+=count; by_dtype[dtype]=by_dtype.get(dtype,0)+count
  tensor_bytes+=count*SIZES[dtype]
 return {'path':str(path),'header_bytes':n,'tensor_count':tensors,'parameter_elements':params,'elements_by_dtype':by_dtype,'tensor_payload_bytes_calculated':tensor_bytes}
base=[header(p) for p in sorted(SNAP.glob('*.safetensors'))]
adapter=header(ADAPTER)
out={'schema':'SI_E2_STATIC_WEIGHT_HEADER_SUMMARY_V1','method':'Read 8-byte safetensors header length and JSON header only; no tensor payload read, no safetensors library/model import/load.','base_revision':'b968826d9c46dd6066d109eabc6255188de91218','base_shards':base,'base_total_parameter_elements':sum(x['parameter_elements'] for x in base),'base_total_tensor_payload_bytes_calculated':sum(x['tensor_payload_bytes_calculated'] for x in base),'base_elements_by_dtype':{},'p0_adapter':adapter}
for x in base:
 for k,v in x['elements_by_dtype'].items(): out['base_elements_by_dtype'][k]=out['base_elements_by_dtype'].get(k,0)+v
print(json.dumps(out,sort_keys=True,separators=(',',':')))
