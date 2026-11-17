#!/usr/bin/env python3
"""Unreleased design-v7 CPU prototype. Manifest claims are not authenticated provenance."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

LIMIT=2_000_000
COUNTS={'files_read':0,'bytes_read':0,'ledger_records':0}
BOUNDS={'files':0,'bytes':0,'ledger_records':0}
class Reject(Exception): pass
def require(ok,reason):
    if not ok:raise Reject(reason)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def exact_dict(value,keys,where):
    require(type(value) is dict and set(value)==set(keys),where+' fields')
def strings(value,where):
    require(type(value) is list and bool(value) and all(type(x) is str and x for x in value),where)
    require(len(set(value))==len(value),where+' duplicates')
def ids(value,where):
    require(type(value) is list and bool(value) and all(type(x) is int and x>=0 for x in value),where)

def read_file(root,rel,expected,*,with_identity=False):
    require(type(rel) is str and rel and not Path(rel).is_absolute() and '..' not in Path(rel).parts,'bad relative path')
    require(type(expected) is str and re.fullmatch('[0-9a-f]{64}',expected) is not None,'bad digest')
    path=root/rel
    require(path.resolve(strict=True)==path and path.is_relative_to(root),'unsafe path or symlink')
    require(COUNTS['files_read']<BOUNDS['files'],'file read ceiling')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
    try:
        COUNTS['files_read']+=1
        a=os.fstat(fd);require(stat.S_ISREG(a.st_mode) and a.st_size<=LIMIT,'file shape')
        require(a.st_size<=BOUNDS['bytes']-COUNTS['bytes_read'],'byte read ceiling')
        with os.fdopen(fd,'rb',closefd=False) as f:raw=f.read(a.st_size)
        COUNTS['bytes_read']+=len(raw)
        b=os.fstat(fd)
        require((a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==
                (b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns,b.st_ctime_ns),'file drift')
    finally:os.close(fd)
    require(len(raw)<=LIMIT and digest(raw)==expected,'bytes hash mismatch')
    return (raw,(a.st_dev,a.st_ino)) if with_identity else raw

def load_json(raw):
    try:
        def pairs(p):
            d={}
            for k,v in p:
                if k in d:raise ValueError('duplicate key')
                d[k]=v
            return d
        return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
    except (ValueError,UnicodeDecodeError) as e:raise Reject('invalid JSON') from e

def repeat(actions):
    if len(actions)<4:return False
    a,b,c,d=actions[-4:]
    return a==c=='look' and type(b) is str and b.startswith('examine ') and len(b)>8 and b==d

def build(manifest,root,ledger):
    exact_dict(manifest,('schema','files','train','evaluation','claimed_product_sha256'),'manifest')
    require(manifest['schema']=='SI_STATE_SELECTION_DEMO_V7','manifest schema')
    require(re.fullmatch('[0-9a-f]{64}',manifest['claimed_product_sha256'] or '') is not None,'product claim')
    files=manifest['files'];require(type(files) is dict and files,'file inventory')
    identities={}
    def get(ref):
        require(type(ref) is str and ref in files,'missing artifact ref')
        raw,identity=read_file(root,ref,files[ref],with_identity=True)
        if ref in identities:require(identities[ref]==identity,'artifact identity drift')
        identities[ref]=identity
        return load_json(raw)
    train=manifest['train'];evaluation=manifest['evaluation']
    require(type(train) is list and 1<=len(train)<=128 and type(evaluation) is list and len(evaluation)==16,'roster size')
    for arm,rows in [('train',train),('evaluation',evaluation)]:
        for row in rows:
            exact_dict(row,('parent','lineage','episode_ref') if arm=='train' else ('parent','lineage'),arm)
            require(type(row['parent']) is str and bool(row['parent']),'parent')
            strings(row['lineage'],'lineage')
        require(len({x['parent'] for x in rows})==len(rows),arm+' parent duplicate')
    require(not ({x['parent'] for x in train}&{x['parent'] for x in evaluation}),'parent overlap')
    train_lineage={i for x in train for i in x['lineage']};eval_lineage={i for x in evaluation for i in x['lineage']}
    require(not (train_lineage&eval_lineage),'declared lineage overlap')
    require(len(train)<=BOUNDS['ledger_records'],'ledger record ceiling')
    ledger.extend({'index':i,'parent':row['parent'],'episode_ref':row['episode_ref'],
                   'episode_sha256':files.get(row['episode_ref']),
                   'disposition':'NOT_SCANNED_AFTER_STOP','reason':'not reached','decisions':[]} for i,row in enumerate(train))
    COUNTS['ledger_records']=len(ledger)
    result=[];episode_ids=set();decision_ids=set();terminal_owners={};decision_owners={}
    for parent_index,item in enumerate(train):
        active_decision=None
        try:
            ep=get(item['episode_ref']);exact_dict(ep,('parent','lineage','episode_id','product_sha256','terminal_ref','decisions'),'episode')
            require(ep['parent']==item['parent'] and ep['lineage']==item['lineage'] and ep['product_sha256']==manifest['claimed_product_sha256'],'episode claims differ')
            require(type(ep['episode_id']) is str and ep['episode_id'],'episode identity')
            require(ep['episode_id'] not in episode_ids,'duplicate declared episode source identity')
            episode_ids.add(ep['episode_id'])
            terminal=get(ep['terminal_ref']);exact_dict(terminal,('complete','won'),'terminal')
            terminal_identity=identities[ep['terminal_ref']]
            require(terminal_identity not in terminal_owners or terminal_owners[terminal_identity]==item['parent'],'terminal receipt reused across parents')
            terminal_owners[terminal_identity]=item['parent']
            require(terminal['complete'] is True and type(terminal['won']) is bool,'completion or win UNKNOWN')
            if terminal['won'] is False:
                ledger[parent_index].update(disposition='REJECT',reason='complete known non-success')
                continue
            decisions=ep['decisions'];require(type(decisions) is list and decisions,'missing decisions')
            history=[];valid=[]
            for i,d in enumerate(decisions):
                require(COUNTS['ledger_records']<BOUNDS['ledger_records'],'ledger record ceiling')
                active_decision={'index':i,'disposition':'PENDING','reason':'being checked'}
                ledger[parent_index]['decisions'].append(active_decision);COUNTS['ledger_records']+=1
                exact_dict(d,('index','source_decision_id','prompt_ref','action_ref','label_ref','mask_ref'),'decision')
                require(type(d['index']) is int and d['index']==i,'decision order')
                require(type(d['source_decision_id']) is str and d['source_decision_id'],'decision source identity')
                require(d['source_decision_id'] not in decision_ids,'duplicate declared decision source identity')
                decision_ids.add(d['source_decision_id'])
                p,a,label,m=(get(d[key]) for key in ('prompt_ref','action_ref','label_ref','mask_ref'))
                source_refs=tuple(identities[d[key]] for key in ('prompt_ref','action_ref','label_ref','mask_ref'))
                require(source_refs not in decision_owners or decision_owners[source_refs]==item['parent'],'decision refs reused across parents')
                decision_owners[source_refs]=item['parent']
                exact_dict(p,('text','input_ids'),'prompt');exact_dict(a,('mapping','selected_id','command'),'action')
                exact_dict(label,('token_ids',),'label');exact_dict(m,('sequence_ids','loss_mask'),'mask')
                require(type(p['text']) is str and bool(p['text']),'empty prompt');ids(p['input_ids'],'prompt ids');ids(label['token_ids'],'label ids')
                require(len(label['token_ids'])<=16,'label cap');ids(m['sequence_ids'],'formatted sequence')
                require(m['sequence_ids']==p['input_ids']+label['token_ids'] and len(m['sequence_ids'])<=4096,'context or formatting')
                require(type(m['loss_mask']) is list and all(type(x) is int for x in m['loss_mask']) and
                        m['loss_mask']==[0]*len(p['input_ids'])+[1]*len(label['token_ids']),'loss mask')
                require(type(a['mapping']) is dict and a['mapping'] and all(type(k) is str and type(v) is str and v for k,v in a['mapping'].items()),'action mapping')
                require(len(set(a['mapping'].values()))==len(a['mapping']),'duplicate commands')
                require(type(a['selected_id']) is str and type(a['command']) is str and a['mapping'].get(a['selected_id'])==a['command'],'bad recorded action')
                is_loop=repeat(history);target=not a['command'].startswith(('look','examine'))
                valid.append({'index':i,'loop':is_loop,'eligible_action':target,'action_id':a['selected_id'],
                              'command':a['command'],'label':label['token_ids'],'loss_mask':m['loss_mask'],
                              'input_tokens':len(p['input_ids']),'refs':d})
                active_decision.update(disposition='TARGET_CANDIDATE' if is_loop and target else
                    'CONTROL_CANDIDATE' if not is_loop and target else 'KNOWN_NONMATCH',reason='verified claim')
                active_decision=None
                history.append(a['command'])
            pairs=[(t,c) for t in valid for c in valid if t['loop'] and not c['loop'] and t['eligible_action'] and c['eligible_action']
                   and (t['action_id'],t['command'],t['label'],t['loss_mask'])==(c['action_id'],c['command'],c['label'],c['loss_mask'])]
            if not pairs:
                ledger[parent_index].update(disposition='REJECT',reason='no matching pair')
                continue
            t,c=pairs[0];result.append({'parent':item['parent'],'episode_id':ep['episode_id'],'episode_ref':item['episode_ref'],
                                        'terminal_ref':ep['terminal_ref'],'target':t,'control':c})
            ledger[parent_index].update(disposition='ACCEPT',reason='first qualifying pair')
            if len(result)==16:
                for row in ledger[parent_index+1:]:row.update(disposition='NOT_SCANNED_AFTER_SELECTION',reason='16 selected')
                break
        except (Reject,OSError,TypeError,KeyError,ValueError) as exc:
            if active_decision is not None:active_decision.update(disposition='UNKNOWN',reason=str(exc))
            ledger[parent_index].update(disposition='UNKNOWN',reason=str(exc))
            raise
    if len(result)<16:return result,'INSUFFICIENT'
    target=sum(x['target']['input_tokens'] for x in result);control=sum(x['control']['input_tokens'] for x in result)
    require(abs(target-control)*100<=5*min(target,control),'input total mismatch >5 percent')
    return result,'SELECTED_UNVERIFIED_CLAIMS'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest',required=True);ap.add_argument('--manifest-sha256',required=True)
    ap.add_argument('--input-root',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--max-files',required=True,type=int);ap.add_argument('--max-bytes',required=True,type=int)
    ap.add_argument('--max-ledger-records',required=True,type=int);args=ap.parse_args()
    output=Path(args.output);output.mkdir(mode=0o700,parents=False,exist_ok=False)
    status={'status':'UNKNOWN','manifest_sha256':args.manifest_sha256,'source_identity':'UNKNOWN',
            'execution_identity':'UNKNOWN','lineage_authenticity':'UNKNOWN','scientific_use':'HOLD',
            'cpu_wall_memory_budget':'NOT_IMPLEMENTED','output_byte_budget':'NOT_IMPLEMENTED',
            'full_scan_budget':'UNKNOWN','parent_roster_ledger_complete':False}
    ledger=[]
    try:
        require(args.max_files>0 and args.max_bytes>0 and args.max_ledger_records>0,'positive read/ledger ceilings required')
        BOUNDS.update(files=args.max_files,bytes=args.max_bytes,ledger_records=args.max_ledger_records)
        root=Path(args.input_root).resolve(strict=True);path=Path(args.manifest).resolve(strict=True)
        require(path.parent==root,'manifest must be directly in input root')
        manifest=load_json(read_file(root,path.name,args.manifest_sha256));pairs,outcome=build(manifest,root,ledger)
        if outcome=='SELECTED_UNVERIFIED_CLAIMS':
            for group in ('target','control'):
                with (output/(group+'.jsonl')).open('x',encoding='utf-8') as f:
                    for p in pairs:
                        f.write(json.dumps({'parent':p['parent'],'episode_id':p['episode_id'],
                            'episode_ref':p['episode_ref'],'terminal_ref':p['terminal_ref'],'selection':p[group]},sort_keys=True)+'\n')
        status.update(status=outcome,selected_parents=len(pairs))
    except (Reject,OSError,TypeError,KeyError,ValueError) as e:
        status['reason']=str(e);status['error_type']=type(e).__name__
    if ledger:
        with (output/'ledger.jsonl').open('x',encoding='utf-8') as f:
            for row in ledger:f.write(json.dumps(row,sort_keys=True)+'\n')
        status['parent_roster_ledger_complete']=True
    status['counters']=dict(COUNTS);status['read_limits']=dict(BOUNDS)
    (output/'status.json').write_text(json.dumps(status,sort_keys=True,indent=2)+'\n')
    print(json.dumps(status,sort_keys=True));return 0 if status['status']=='SELECTED_UNVERIFIED_CLAIMS' else 1

if __name__=='__main__':sys.exit(main())
