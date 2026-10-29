import hashlib,json,os,pathlib,subprocess,datetime,time
P=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T143500Z__SOL__si-u1-final-construction-plan__616f1e4')
E=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T144500Z__SOL__si-u1-stage1-manifest__616f1e4')
A=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9')
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def write(p,x):
 with open(p,'x',encoding='utf-8') as f: json.dump(x,f,sort_keys=True,indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def verify(path,digest):
 p=pathlib.Path(path); assert p.is_file() and not p.is_symlink(), str(p)
 assert sha(p)==digest, str(p)
 return json.loads(p.read_text())
assert not (P/'stage1').exists() and not (P/'REFS_FROZEN.json').exists()
review=verify(A/'FINALIZER_BOOTSTRAP616_INDEPENDENT_REVIEW.json','63c33a8c92d3b236ff58a6e4109407feaaff02b4f1951e133e0268f3607f330f')
assert review['schema']=='ASTRA_FINALIZER_BOOTSTRAP_REVIEW_V1' and review['decision']=='PASS_CONSTRUCTION_SOFTWARE_ONLY_NOT_PREFLIGHT_OR_EVALUATION'
assert review['source_sha']=='616f1e4f977c471aab461691d750d8bab5b00464' and review['builder_source_sha']=='7b4cfbf358fcc24cfe350bcbee29a09e8a9475cd' and review['evaluation_source_sha']=='8532275932dabddc498c23a2b6d9a045647542f0'
verify(A/'FINALIZER7B4_INDEPENDENT_REVIEW.json','2b26ab2634be3b0d4a56e9c0bade1e67ad3d6d52ccc3ab3419cb6f5e779242fe')
refs=json.loads((P/'REFS_CANDIDATE_NOT_EXECUTABLE.json').read_text())['refs']
refs['c_review']={'path':str(A/'C_REVIEW_BINDING_9BBAA.json'),'sha256':'41068ca8574f2f76a7c0566799dbd78aa87635623cebc457cc4d39d5d9469fe9'}
assert set(refs)=={'b_accept','b_exit','b_manifest','b_result','byte','c_accept','c_exit','c_manifest','c_result','c_review','manifest_draft','plan_draft','runtime_draft','schedule','training'}
objs={k:verify(v['path'],v['sha256']) for k,v in refs.items()}
c=objs['c_accept']; b=objs['c_review']
assert c['schema']=='SI_U1_INDEPENDENT_C_REAL_ACCEPTANCE_V1' and c['decision']=='ACCEPT_C_FIXED_FINAL_CHECKPOINT_AND_EVALUATION_CONSTRUCTION_ONLY' and type(c['actual_launcher_worker_exit']) is int and c['actual_launcher_worker_exit']==0 and c['process_cleanup_established'] is True
assert b['schema']=='SI_U1_C_REVIEW_BINDING_V1' and b['decision']=='PASS_C_TRAINING_INDEPENDENT_ONLY' and b['acceptance_sha256']==refs['c_accept']['sha256']
assert b['final_adapter_sha256']==c['final_adapter_tree_sha256'] and b['training_result_sha256']==c['training_result_sha256']==refs['c_result']['sha256'] and b['supervisor_sha256']==c['supervisor_sha256']==refs['c_exit']['sha256'] and b['manifest_sha256']==refs['c_manifest']['sha256'] and b['source_sha']==c['source_sha']
assert sha('/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python3.10')=='560aa01150e792ac8efc5f0e55db51e7175623437a2c2d7e62b2ec2cd9973449'
assert sha('/home/lizening/wt-si-u1-finalizer-bootstrap/bootstrap.py')=='471d66fcb2b5d14b69eb11b0f2d45b635eab1bb7c0ea2da29164bb4177ea13d7'
write(P/'REFS_FROZEN.json',refs); os.chmod(P/'REFS_FROZEN.json',0o600)
refhash=sha(P/'REFS_FROZEN.json')
write(E/'INPUT_REVIEW.json',{'status':'INPUTS_HASH_VERIFIED_FOR_STAGE1_ONLY','inputs':{k:v['sha256'] for k,v in refs.items()},'refs_sha256':refhash,'review_sha256':'63c33a8c92d3b236ff58a6e4109407feaaff02b4f1951e133e0268f3607f330f','c_review_and_acceptance_consistent':True,'science_preflight_or_model_env_invoked':False})
cmd=['/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python3.10','-I','-S','/home/lizening/wt-si-u1-finalizer-bootstrap/bootstrap.py','--stage','one','--refs',str(P/'REFS_FROZEN.json'),'--refs-sha256',refhash,'--output-dir',str(P/'stage1')]
env={'PATH':'/usr/bin:/bin','HOME':'/home/lizening','LC_ALL':'C.UTF-8','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1'}
write(E/'ONE_SHOT_CLAIM.json',{'argv':cmd,'env':env,'cwd':'/home/lizening/wt-si-u1-finalizer-bootstrap','created':utc(),'retry_allowed':False})
start=utc(); t=time.monotonic(); error=None; rc=None; pid=None
try:
 with open(E/'stdout.log','xb') as out,open(E/'stderr.log','xb') as err:
  proc=subprocess.Popen(cmd,cwd='/home/lizening/wt-si-u1-finalizer-bootstrap',env=env,stdout=out,stderr=err); pid=proc.pid; rc=proc.wait()
except Exception as ex: error=repr(ex)
write(E/'PROCESS_RECEIPT.json',{'argv':cmd,'env':env,'cwd':'/home/lizening/wt-si-u1-finalizer-bootstrap','start_utc':start,'end_utc':utc(),'duration_seconds':time.monotonic()-t,'pid':pid,'returncode':rc,'launch_error':error,'retry':False,'refs_sha256':refhash})
print(json.dumps({'returncode':rc,'launch_error':error,'refs_sha256':refhash,'output_exists':(P/'stage1').exists()}))
if rc!=0: raise SystemExit(1)
