"""Independent exact-SHA software acceptance; actual CUDA hidden, no runtime CLI."""
from pathlib import Path
from datetime import datetime,timezone
from xml.etree import ElementTree as ET
import hashlib,json,os,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
PY='/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python'
BASE='dfc00e49d1ef4d48453d2331507429f8a0c7bbc5'
BASE_XML=Path('/home/lizening/research-notes/agent-logs/2026-10-25T124118Z__SOL__si-e2-runtime-resource-review__sie2_4c82/independent_software/candidate_full_pinned_source.xml')
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fresh(p,x):
 with p.open('x') as f:json.dump(x,f,indent=2);f.write('\n')
def command(label,argv,cwd):
 env=os.environ.copy()
 for k in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV'):env.pop(k,None)
 env.update(PYTHONPATH=str(cwd/'src'),CUDA_VISIBLE_DEVICES='',PYTHONDONTWRITEBYTECODE='1',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
 started=time.monotonic();utc=datetime.now(timezone.utc).isoformat()
 with (ROOT/(label+'.stdout')).open('xb') as out,(ROOT/(label+'.stderr')).open('xb') as err:
  p=subprocess.run(argv,cwd=cwd,env=env,stdout=out,stderr=err)
 receipt={'argv':argv,'cwd':str(cwd),'start_UTC':utc,'finish_UTC':datetime.now(timezone.utc).isoformat(),'subprocess_returncode':p.returncode,'elapsed_seconds':time.monotonic()-started,'inherited_python_settings_removed':['PYTHONPATH','PYTHONHOME','VIRTUAL_ENV'],'controlled_software_PYTHONPATH':env['PYTHONPATH'],'CUDA_VISIBLE_DEVICES':'','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','stdout_sha256':H(ROOT/(label+'.stdout')),'stderr_sha256':H(ROOT/(label+'.stderr'))}
 fresh(ROOT/(label+'.receipt.json'),receipt);print(json.dumps({'label':label,'returncode':p.returncode,'elapsed_seconds':receipt['elapsed_seconds']}),flush=True)
 return p.returncode

def cases(p):
 d={}
 for c in ET.parse(p).getroot().iter('testcase'):
  key=c.attrib.get('classname','')+'::'+c.attrib['name'];assert key not in d
  kinds=[v.tag for v in c if v.tag in ('failure','error','skipped')];d[key]=kinds[0] if kinds else 'passed'
 return d
if __name__=='__main__':
 cwd=Path(sys.argv[1]).resolve();sha=sys.argv[2];assert len(sha)==40
 git=lambda *a:subprocess.check_output(['git',*a],cwd=cwd,text=True)
 assert git('rev-parse','HEAD').strip()==sha and not git('status','--porcelain','--untracked-files=all').strip()
 assert git('rev-parse',sha+'^').strip()==BASE
 changes=git('diff','--name-only',BASE,sha).splitlines()
 fresh(ROOT/'independent_source_files.json',{'source_SHA':sha,'base_SHA':BASE,'files':[{'path':p,'sha256':H(cwd/p),'bytes':(cwd/p).stat().st_size} for p in changes],'delta':git('diff','--stat',BASE,sha),'clean':True})
 (ROOT/'independent_source_delta.patch').write_text(git('diff','--binary',BASE,sha))
 assert command('compile',[PY,'-m','py_compile',*[p for p in changes if p.endswith('.py')]],cwd)==0
 assert command('diff_check',['git','diff','--check',BASE,sha],cwd)==0
 code=command('full_suite',[PY,'-m','pytest','-q','-p','no:cacheprovider','--junitxml='+str(ROOT/'full_suite.xml'),'--basetemp=/tmp/si-e2-uuid-root-full-'+sha[:8]],cwd)
 old,new=cases(BASE_XML),cases(ROOT/'full_suite.xml');bad=lambda d:{k:v for k,v in d.items() if v in ('failure','error')}
 counts=lambda d:{s:list(d.values()).count(s) for s in ('passed','failure','error','skipped')}
 result={'source_SHA':sha,'base_SHA':BASE,'baseline_XML_sha256':H(BASE_XML),'candidate_XML_sha256':H(ROOT/'full_suite.xml'),'baseline_counts':counts(old),'candidate_counts':counts(new),'authentic_returncode':code,'exact_failure_error_sets_equal':bad(old)==bad(new),'missing_baseline_IDs':sorted(set(old)-set(new)),'new_IDs':{k:v for k,v in new.items() if k not in old},'new_failure_error_IDs':{k:v for k,v in bad(new).items() if old.get(k)!=v},'source_clean_after':not git('status','--porcelain','--untracked-files=all').strip()}
 fresh(ROOT/'independent_regression_comparison.json',result)
 print(json.dumps({k:v for k,v in result.items() if k not in ('new_IDs',)}|{'new_tests':len(result['new_IDs'])}),flush=True)
 assert result['exact_failure_error_sets_equal'] and not result['missing_baseline_IDs'] and not result['new_failure_error_IDs'] and result['source_clean_after']
 assert all(s=='passed' for s in result['new_IDs'].values())
