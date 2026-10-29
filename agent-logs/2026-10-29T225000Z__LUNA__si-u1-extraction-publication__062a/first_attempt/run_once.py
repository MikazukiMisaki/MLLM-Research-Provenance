import hashlib, json, os, subprocess, time
from pathlib import Path

HERE = Path(__file__).parent
ASTRA = Path('/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9')
SPEC = ASTRA / 'EXTRACTION_SPEC_C2356_CANDIDATE_V1.json'
APPROVAL = Path('/home/lizening/research-notes/agent-logs/2026-10-29T150100Z__CODEX__si-u1-eval-live-release__853/EXTRACTION_APPROVAL_C2356.json')
REVIEW = ASTRA / 'C2356_REAL_EVALUATION_OPERATIONAL_INDEPENDENT_REVIEW.json'
EXTRACTOR = Path('/home/lizening/wt-si-u1-result-extractor/si_u1_extract.py')
PYTHON = '/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python3.10'

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''): h.update(block)
    return h.hexdigest()

def snapshot(root):
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()}

expected = {str(SPEC):'6d5e1625a28c41651756de561d8a141df42d4398db3dcc9d0c9e6588b4de318d', str(APPROVAL):'6859dd5f7c6bb88ba8c749e882579daa3c472963f97591b98883116e00335e7d', str(REVIEW):'bbf43bd32f994eb948fc6cc02b4d6ff25e902d6fa2eab20524f562d0688d4600', str(EXTRACTOR):'c0827b923f518b5d8ddefb73974994d8a445f352fc8bc8b6e99abb88b3df0f7d'}
receipt = {'schema':'SI_U1_POSTRUN_EXTRACTION_PROCESS_V1','started_unix':time.time(),'attempted':False}
try:
    assert all(sha(Path(p)) == h for p,h in expected.items())
    spec = json.loads(SPEC.read_bytes())
    assert json.loads(REVIEW.read_bytes())['decision']=='ACCEPT_OPERATIONAL_COMPLETENESS_ELIGIBLE_FOR_APPROVED_PREREGISTERED_EXTRACTION_ONLY'
    for k in ('manifest','runtime_spec','plan','protocol','schedule','analysis','authorization','clearance','stats'):
        x=spec[k]; assert sha(Path(x['path']))==x['sha256']
    assert not Path(spec['analysis_output']).exists()
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=EXTRACTOR.parent,text=True).strip()=='b442aa811bcec2fa4eba2cfabb2ed28719cc38dc'
    assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=normal'],cwd=EXTRACTOR.parent,text=True).strip()
    root=Path(spec['run_output']); before=snapshot(root)
    (HERE/'original_before.json').write_text(json.dumps(before,sort_keys=True,indent=2)+'\n')
    argv=[PYTHON,'-I','-B',str(EXTRACTOR),'--spec',str(SPEC),'--spec-sha256',expected[str(SPEC)],'--approval',str(APPROVAL),'--approval-sha256',expected[str(APPROVAL)]]
    env={'PATH':'/usr/bin:/bin','HOME':'/home/lizening','HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','CUDA_VISIBLE_DEVICES':'','TOKENIZERS_PARALLELISM':'false'}
    receipt.update({'argv':argv,'cwd':str(EXTRACTOR.parent),'environment':env,'input_hashes':expected,'run_output':str(root),'attempted':True})
    with (HERE/'stdout').open('xb') as out, (HERE/'stderr').open('xb') as err:
        p=subprocess.Popen(argv,cwd=EXTRACTOR.parent,env=env,stdout=out,stderr=err)
        receipt['child_pid']=p.pid
        receipt['authentic_returncode']=p.wait()
    after=snapshot(root)
    (HERE/'original_after.json').write_text(json.dumps(after,sort_keys=True,indent=2)+'\n')
    receipt['original_evidence_unchanged']=(before==after)
    receipt['bound_inputs_unchanged']=all(sha(Path(p)) == h for p,h in expected.items()) and all(sha(Path(spec[k]['path']))==spec[k]['sha256'] for k in ('manifest','runtime_spec','plan','protocol','schedule','analysis','authorization','clearance','stats'))
    result=Path(spec['analysis_output'])
    receipt['analysis_exists']=result.is_file()
    if result.is_file(): receipt['analysis_sha256']=sha(result)
    receipt['closed_success']=receipt['authentic_returncode']==0 and receipt['original_evidence_unchanged'] and receipt['bound_inputs_unchanged'] and receipt['analysis_exists']
except BaseException as e:
    receipt['error']=repr(e)
    receipt['closed_success']=False
finally:
    receipt['ended_unix']=time.time()
    with (HERE/'PROCESS_RECEIPT.json').open('x') as f: json.dump(receipt,f,sort_keys=True,indent=2);f.write('\n')
if not receipt['closed_success']: raise SystemExit(1)
