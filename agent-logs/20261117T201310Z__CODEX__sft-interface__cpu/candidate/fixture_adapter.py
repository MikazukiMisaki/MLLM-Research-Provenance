"""Fixed fictional v7 fixture only. No production conversion or training entrypoint."""
import hashlib
import json

FIXTURE_SHA256='0fcb3fc579a256667ccb833e61e473615d9fd42415e549c57abac58862580d30'
EOS=151645
class Rejected(ValueError):pass

def _require(condition,message):
    if not condition:raise Rejected(message)
def _ids(value):return type(value) is list and bool(value) and all(type(x) is int and x>=0 for x in value)
def _project_fake(fixture):
    """Internal validator for the exact fake fixture; not a source authenticator."""
    _require(type(fixture) is dict and set(fixture)=={'fixture_scope','rows','objects'},'fixture shape')
    _require(fixture['fixture_scope']=='FICTIONAL_ONLY_NOT_AUTHENTICATED','not fictional scope')
    rows=fixture['rows'];objects=fixture['objects']
    _require(type(rows) is list and len(rows)==2 and type(objects) is dict,'fake roster')
    _require([r.get('group') for r in rows]==['target','control'],'fake groups')
    used_refs=set();used_decisions=set();result=[]
    for row in rows:
        _require(type(row) is dict and row.get('parent')=='FICTIONAL_PARENT' and row.get('episode_id')=='FICTIONAL_EPISODE','fake lineage')
        x=row.get('selection');_require(type(x) is dict,'selection')
        refs=x.get('refs');keys={'index','source_decision_id','prompt_ref','action_ref','label_ref','mask_ref'}
        _require(type(refs) is dict and set(refs)==keys and refs['index']==x.get('index'),'source refs')
        decision=refs['source_decision_id'];_require(type(decision) is str and decision.startswith('FAKE-DECISION-') and decision not in used_decisions,'decision alias')
        used_decisions.add(decision)
        names=[refs[k] for k in ('prompt_ref','action_ref','label_ref','mask_ref')]
        _require(all(type(n) is str and n in objects and n not in used_refs for n in names) and len(set(names))==4,'artifact alias')
        used_refs.update(names)
        prompt,action,label,mask=(objects[n] for n in names)
        _require(type(prompt) is dict and set(prompt)=={'text','input_ids'} and type(prompt['text']) is str and prompt['text'].startswith('FICTIONAL '),'prompt')
        _require(type(action) is dict and set(action)=={'mapping','selected_id','command'} and type(action['mapping']) is dict and action['mapping'].get(action['selected_id'])==action['command'] and x.get('action_id')==action['selected_id'] and x.get('command')==action['command'],'action')
        _require(type(label) is dict and set(label)=={'token_ids'} and type(mask) is dict and set(mask)=={'sequence_ids','loss_mask'},'tensor source')
        inp=prompt['input_ids'];out=label['token_ids'];seq=mask['sequence_ids'];lm=mask['loss_mask']
        _require(_ids(inp) and _ids(out) and len(out)<=16 and len(inp)+len(out)<=4096,'token bounds no truncation')
        _require(out[-1]==EOS and EOS not in out[:-1],'fake EOS')
        _require(type(lm) is list and all(type(v) is int for v in lm) and lm==[0]*len(inp)+[1]*len(out),'completion-only mask')
        _require(seq==inp+out and x.get('input_tokens')==len(inp) and x.get('label')==out and x.get('loss_mask')==lm,'selection mismatch')
        result.append({'group':row['group'],'prompt':list(inp),'generated':list(out),'input_ids':list(seq),'loss_mask':list(lm),
                       'labels':[-100 if m==0 else t for t,m in zip(seq,lm)],'source_decision_id':decision,'source_refs':names})
    return result

def convert_fixture(raw):
    """Only the immutable built-in test bytes; authenticated real input is not supported."""
    _require(type(raw) is bytes and hashlib.sha256(raw).hexdigest()==FIXTURE_SHA256,'not the pinned fictional fixture')
    try:fixture=json.loads(raw)
    except (ValueError,UnicodeDecodeError) as error:raise Rejected('bad fixture') from error
    projected=_project_fake(fixture)
    return {'schema':'SI_V7_FAKE_TOKEN_PREVIEW_V1','scope':'FICTIONAL_ONLY','source_identity':'UNAUTHENTICATED_FAKE',
            'trainer_compatible':False,'scientific_use':'HOLD','rows':projected}

def convert_for_training(*_args,**_kwargs):
    raise RuntimeError('RESEARCH_HOLD: no authenticated selection-to-trainer bridge exists')
