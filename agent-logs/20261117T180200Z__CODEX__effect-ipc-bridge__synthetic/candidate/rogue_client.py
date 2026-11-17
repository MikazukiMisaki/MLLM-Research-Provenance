"""Deliberately malformed synthetic protocol peer, never used for research."""
import json
import socket
import sys
sock=socket.socket(fileno=int(sys.argv[1]));mode=sys.argv[2]
with sock.makefile('rwb',buffering=0) as f:
    def write(x):f.write((json.dumps(x)+'\n').encode())
    if mode=='early_finish':write({'kind':'finished','seq':0,'status':'COMPLETED'})
    elif mode=='pipeline':
        first=json.dumps({'kind':'reserve','seq':0,'operation':'generation'})+'\n'
        second=json.dumps({'kind':'reserve','seq':1,'operation':'generation'})+'\n'
        f.write((first+second).encode())
    elif mode=='sequence':write({'kind':'reserve','seq':1,'operation':'generation'})
    elif mode=='duplicate':
        write({'kind':'reserve','seq':0,'operation':'generation'});f.readline()
        write({'kind':'reserve','seq':0,'operation':'generation'})
    elif mode=='unknown_kind':write({'kind':'invented','seq':0})
    elif mode=='bad_receipt':
        write({'kind':'reserve','seq':0,'operation':'generation'});f.readline()
        write({'kind':'returned','seq':0,'operation':'generation','receipt_sha256':'0'*64})
    try:f.readline()
    except (OSError,ConnectionError):pass
