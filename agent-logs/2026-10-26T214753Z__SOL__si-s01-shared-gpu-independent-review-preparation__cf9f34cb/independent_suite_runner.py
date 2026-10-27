from pathlib import Path
import hashlib,importlib,json,os,sys,time
TREE=Path(sys.argv[1]).resolve();OWN=Path(sys.argv[2]).resolve();MODE=sys.argv[3]
assert MODE in ('collect','full')
sys.path[:0]=[str(TREE/'src'),str(TREE/'tests'),str(TREE)]
import pytest
PROJECT=['env.base','models.policy','sft.masking','sft.training','self_improvement.si_p3.collector','scripts.run_r19_experiment','self_improvement.si_s01.runtime_core','self_improvement.si_s01.shared_resource','self_improvement.si_s01.shared_resource_audit']
def origins(stage):
    data={'mode':MODE,'stage':stage,'executable':sys.executable,'sys_path':sys.path,'environment_presence':{k:k in os.environ for k in ('PYTHONPATH','PYTHONHOME','VIRTUAL_ENV')},'CUDA_VISIBLE_DEVICES':os.environ.get('CUDA_VISIBLE_DEVICES'),'PYTHONDONTWRITEBYTECODE':os.environ.get('PYTHONDONTWRITEBYTECODE'),'modules':{}}
    for name in PROJECT+['pytest']:
        module=importlib.import_module(name);path=Path(module.__file__).resolve()
        if name in PROJECT:assert path.is_relative_to(TREE), (name,str(path))
        data['modules'][name]={'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    torch=sys.modules.get('torch')
    data['torch_imported']=torch is not None
    data['torch_cuda_initialized']=bool(torch.cuda.is_initialized()) if torch is not None and hasattr(torch,'cuda') else False
    (OWN/(MODE+'.origins.'+stage+'.json')).write_text(json.dumps(data,indent=2)+'\n')
    return data
origins('before')
class Evidence:
    def __init__(self):self.ids=[];self.reports=[];self.collection_errors=[]
    def pytest_collection_finish(self,session):
        self.ids=[item.nodeid for item in session.items]
        (OWN/(MODE+'.collection_ids.json')).write_text(json.dumps(self.ids,indent=2)+'\n')
    def pytest_collectreport(self,report):
        if report.failed:self.collection_errors.append({'nodeid':report.nodeid,'longrepr':str(report.longrepr)})
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self,item,call):
        outcome=yield
        report=outcome.get_result()
        row={'nodeid':item.nodeid,'phase':report.when,'outcome':report.outcome,'duration':report.duration}
        if call.excinfo is not None:
            row['exception_type']=call.excinfo.type.__module__+'.'+call.excinfo.type.__qualname__
            row['exception_message']=str(call.excinfo.value)
        if report.failed:row['longrepr']=str(report.longrepr)
        self.reports.append(row)
evidence=Evidence()
args=['-o','cache_dir='+str(OWN/'pytest_cache')]
if MODE=='collect':args+=['--collect-only','-q']
else:args+=['--junitxml='+str(OWN/'baseline.junit.xml')]
(OWN/(MODE+'.pytest_arguments.json')).write_text(json.dumps({'pytest_main_arguments':args,'default_testpaths_preserved':True,'filters_or_deselections':False},indent=2)+'\n')
at=time.monotonic();code=pytest.main(args,plugins=[evidence]);elapsed=time.monotonic()-at
(OWN/(MODE+'.reports.json')).write_text(json.dumps({'pytest_returncode':int(code),'elapsed_seconds':elapsed,'collection_errors':evidence.collection_errors,'reports':evidence.reports},indent=2)+'\n')
origins('after')
print('INDEPENDENT_BASELINE_CAPTURE '+json.dumps({'mode':MODE,'pytest_returncode':int(code),'collected':len(evidence.ids),'report_count':len(evidence.reports),'elapsed_seconds':elapsed}),flush=True)
raise SystemExit(int(code))
