"""Imaginary subprocess. Has no dependency on any model or environment."""
import json
import os
import socket
import sys

fd=int(sys.argv[1]); arm=sys.argv[2]; mode=sys.argv[3]
sock=socket.socket(fileno=fd)
with sock.makefile('rwb',buffering=0) as f:
    def send(message):
        f.write((json.dumps(message)+'\n').encode())
        line=f.readline()
        if not line: raise SystemExit(10)
        return json.loads(line)
    def effect(kind):
        token=send({'type':'reserve','kind':kind})['token']
        if mode=='open' and kind=='generation': raise SystemExit(4)
        send({'type':'return','token':token,'receipt':{'synthetic':True}})
    for op in ('env_construct','env_init','reset'): effect(op)
    send({'type':'initial','state':{'task':'fictional','x': 2 if ((mode=='mismatch' and arm=='B') or (mode=='mismatch_second_reversed' and arm=='A')) else 1}})
    if mode=='no_model':
        send({'type':'done','won':True})
        raise SystemExit(0)
    for op in (('model_load','generation') if mode=='zero_step' else ('model_load','generation','step')): effect(op)
    send({'type':'done','won':False})
