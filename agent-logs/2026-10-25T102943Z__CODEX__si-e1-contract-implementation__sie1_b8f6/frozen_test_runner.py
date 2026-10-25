from pathlib import Path
import subprocess,sys
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
mode=sys.argv[1];assert mode in ('focused','full')
files=sorted(str(p.relative_to(ROOT)) for p in ROOT.glob('tests/test_r19*.py'))+['tests/test_si_p3_collector.py','tests/test_si_p3_learning.py','tests/test_si_p3_reservations.py'] if mode=='focused' else []
assert mode=='full' or len(files)>3
label='frozen_focused_v2' if mode=='focused' else 'frozen_full'
cmd=[sys.executable,str(OWN/'run_command.py'),label,str(ROOT),'env','PYTHONPATH=src:tests','PYTHONDONTWRITEBYTECODE=1','CUDA_VISIBLE_DEVICES=','HF_HUB_OFFLINE=1','TRANSFORMERS_OFFLINE=1','/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python','-m','pytest','-p','no:cacheprovider',*files,'--basetemp=/tmp/si-e1-codex-'+label+'-b8f6','--junitxml='+str(OWN/(label+'.xml'))]
p=subprocess.run(cmd);sys.exit(p.returncode)
