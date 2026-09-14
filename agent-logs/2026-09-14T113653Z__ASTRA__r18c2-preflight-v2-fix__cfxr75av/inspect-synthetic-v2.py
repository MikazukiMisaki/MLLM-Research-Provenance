import json,sys
from dataclasses import replace
from pathlib import Path
from test_process_identity_v2 import m
from infra_helpers import P,run
name=sys.argv[1];job=P/'synthetic-jobs'/name
boot=Path('/proc/sys/kernel/random/boot_id').read_text().strip()
proc=m.read_process(int((job/'launcher.pid').read_text()),boot)
assert proc is not None
rules=m.Rules(repo=P,script=P/'synthetic-payload-v2.py',runtime=P/'synthetic-runtime',tasks=P/'synthetic-jobs',external_lock=P/'synthetic-launch.lock',test_wrappers=(P/'durable-wrapper-v2.sh',))
verdict=m.classify(proc,rules);assert verdict['kind']=='wrapper',verdict
child=m.read_process(int((job/'runner.pid').read_text()),boot)
assert child is not None and m.classify(child,rules)['kind']=='runner'
for role,current in [('launcher',proc),('runner',child)]:
 record=json.loads((job/(role+'.identity')).read_text())
 assert m.recorded_identity(record,current)=='active_recorded_identity'
 assert m.recorded_identity(record,replace(current,start_ticks=current.start_ticks+1))=='pid_reused'
 assert m.recorded_identity(record,replace(current,boot_id='other-boot'))=='previous_boot'
assert not Path('/proc/'+(job/'dispatch-shell.pid').read_text().strip()).exists()
try:m.probe_lock(P/'synthetic-launch.lock',required=True)
except RuntimeError:pass
else:raise AssertionError('Synthetic external lock did not block')
result={'launcher':m.asdict(proc),'runner':m.asdict(child),'wrapper_verdict':verdict,'launch_shell_returned':True,'boot_and_start_identity':'PASS','lock_held':'PASS'}
(P/('synthetic-'+name+'-identity.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
