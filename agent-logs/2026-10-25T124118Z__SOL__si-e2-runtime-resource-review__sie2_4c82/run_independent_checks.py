"""Frozen-candidate independent checks; never invoke real runtime probe."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from xml.etree import ElementTree as ET

OWN=Path(__file__).resolve().parent
assert OWN.name=='2026-10-25T124118Z__SOL__si-e2-runtime-resource-review__sie2_4c82'
PY='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'

def run(name,argv,cwd,*,source_binding=False):
    dest=OWN/'independent_software'
    dest.mkdir(exist_ok=True)
    env=os.environ.copy()
    for k in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV'):
        env.pop(k,None)
    env.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
    if source_binding:
        env.update(PYTHONPATH=str(Path(cwd)/'src'),CUDA_VISIBLE_DEVICES='',PYTHONDONTWRITEBYTECODE='1')
    start=datetime.now(timezone.utc).isoformat()
    stamp=time.monotonic()
    with (dest/(name+'.stdout')).open('xb') as out, (dest/(name+'.stderr')).open('xb') as err:
        p=subprocess.run(argv,cwd=cwd,env=env,stdout=out,stderr=err)
    rec={'argv':argv,'cwd':str(cwd),'start_utc':start,'finish_utc':datetime.now(timezone.utc).isoformat(),
         'elapsed_seconds':time.monotonic()-stamp,'subprocess_returncode':p.returncode,
         'environment_exclusions':['PYTHONPATH','PYTHONHOME','VIRTUAL_ENV'],
         'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1',
         'controlled_software_source_binding':str(Path(cwd)/'src') if source_binding else None,
         'CUDA_VISIBLE_DEVICES':env.get('CUDA_VISIBLE_DEVICES'),
         'stdout_sha256':hashlib.sha256((dest/(name+'.stdout')).read_bytes()).hexdigest(),
         'stderr_sha256':hashlib.sha256((dest/(name+'.stderr')).read_bytes()).hexdigest()}
    (dest/(name+'.receipt.json')).write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps({'name':name,'subprocess_returncode':p.returncode,'elapsed_seconds':rec['elapsed_seconds']}),flush=True)
    return rec

def junit(path):
    root=ET.parse(path).getroot()
    cases={}
    for c in root.iter('testcase'):
        key=c.attrib.get('classname','')+'::'+c.attrib['name']
        assert key not in cases,key
        children=[v.tag for v in c if v.tag in ('failure','error','skipped')]
        cases[key]=children[0] if children else 'passed'
    return cases

if __name__=='__main__':
    checkout=Path(sys.argv[1]).resolve()
    expected=sys.argv[2]
    assert len(expected)==40
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=checkout,text=True).strip()==expected
    assert not subprocess.check_output(['git','status','--porcelain'],cwd=checkout,text=True).strip()
    mode=sys.argv[3]
    if mode in ('full','full_pinned_source'):
        dest=OWN/'independent_software'
        label='candidate_full' if mode=='full' else 'candidate_full_pinned_source'
        xml=dest/(label+'.xml')
        run(label,[PY,'-m','pytest','-q','-p','no:cacheprovider','--junitxml='+str(xml),
                   '--basetemp=/tmp/si-e2-independent-'+label+'-fixtures'],checkout,source_binding=(mode=='full_pinned_source'))
        baseline=Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__SOL__si-e1-engineering-review__sie1_b8f6/independent_software/candidate_full_a995.xml')
        old,new=junit(baseline),junit(xml)
        bad=lambda d:{k:v for k,v in d.items() if v in ('failure','error')}
        result={'schema':'SI_E2_INDEPENDENT_REGRESSION_V1','base_SHA':'a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3',
                'source_SHA':expected,'baseline_XML_sha256':hashlib.sha256(baseline.read_bytes()).hexdigest(),
                'candidate_XML_sha256':hashlib.sha256(xml.read_bytes()).hexdigest(),
                'base_counts':{s:list(old.values()).count(s) for s in set(old.values())},
                'candidate_counts':{s:list(new.values()).count(s) for s in set(new.values())},
                'exact_failure_error_sets_equal':bad(old)==bad(new),
                'new_failures_or_errors':{k:v for k,v in bad(new).items() if old.get(k)!=v},
                'missing_baseline_ids':sorted(set(old)-set(new)),
                'new_tests':{k:v for k,v in new.items() if k not in old}}
        output='independent_regression_comparison.json' if mode=='full' else 'independent_regression_comparison_pinned_source.json'
        (OWN/output).write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('source_SHA','base_counts','candidate_counts','exact_failure_error_sets_equal')} |
                         {'new_failure_error_count':len(result['new_failures_or_errors']),
                          'missing_baseline_count':len(result['missing_baseline_ids']),
                          'new_test_count':len(result['new_tests'])}),flush=True)
    elif mode=='compile':
        paths=subprocess.check_output(['git','diff','--name-only','a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3',expected],cwd=checkout,text=True).splitlines()
        run('compile',[PY,'-m','py_compile']+[p for p in paths if p.endswith('.py')],checkout)
        run('source_diff_check',['git','diff','--check','a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3',expected],checkout)
    else:
        raise SystemExit('unknown non-execution check mode')
