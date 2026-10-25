"""Freeze current SI-P2 audit evidence; only task-owned files are written."""
from audit_io import *
import shutil

report=OWN/'COMMON_QUALITY_AUDIT.md';before=report.read_text()
backup=OWN/'draft_v1/COMMON_QUALITY_AUDIT_before_editorial_clarification.md';assert not backup.exists();shutil.copy2(report,backup)
after=before.replace('legacy128行原件无认证共享event ID','Q_hist通过的legacy128行无认证共享event ID（原parent legacy合计132行）')
old='anchor key在打开parent结果前从无outcome的manifest写入anchor_keys_pre_outcome.json，使用真实LF'
new='anchor规则由任务单预先固定；正式审计进程在读取parent记录前由identity-only manifest写入anchor_keys_pre_outcome.json。此前字段形状probe已读取既有结果，因此这里不声称首次接触结果之前封存hash或人类盲法。实际anchor选择函数始终只接收质量及身份/目标摘要、无结果label，并在连接结果label划分B/C之前固定选择。key使用真实LF'
assert old in after;after=after.replace(old,new);assert after!=before;report.write_text(after)
record=OWN/'RECORD.md'
with record.open('a') as f:f.write('\n封存前编辑澄清：主报告中128指Q_hist通过的legacy行，原parent legacy为132；anchor规则由协调方事前固定，程序的先后顺序不代表人工首次接触结果前封存hash，字段probe已读既有结果。仅修正文义，不重跑审计或改任何集合/判据；编辑前主文原字节保留draft_v1/COMMON_QUALITY_AUDIT_before_editorial_clarification.md，最终主文hash由FROZEN_HANDOFF及FILE_HASHES绑定。pool_quality_audit.json为1.26MB，略高于建议<1MB，以保留171行完整布尔项与逐条原始locator；无全prompt、全action map或原raw复制。\n')
# Fresh input rehash; the only data operations are byte reads.
bindings=json.loads((OWN/'complete_input_bindings.json').read_bytes())
for x in bindings:assert sha(x['path'])==x['sha256_before']==x['sha256_after'],x['path']
output('final_input_immutability_receipt.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_input_paths_rehashed':len(bindings),'all_match_recorded_before_after':True,'scientific_calls_added':0})
receipts=['parent_inspection.receipt.json','r19_event_inspection.receipt.json','common_quality_audit.receipt.json','common_quality_final.receipt.json','document_completion.receipt.json']
for name in receipts:
 r=json.loads((OWN/name).read_bytes());assert r['returncode']==0;assert sha(r['combined_log_path'])==r['combined_log_sha256'];assert sha(r['argv'][-1])==r['script_sha256']
items=[]
for name in ['COMMON_QUALITY_AUDIT.md','pool_quality_audit.json','pipeline_counts.json','pool_sets.json','original_eleven_dispositions.json','complete_input_bindings.json','INPUT_HASHES.sha256','model_identity_bindings.json','static_contract_receipts.json','frozen_worktree_receipts.json','prior_p1_immutability_check.json','final_input_immutability_receipt.json','RECORD.md','common_quality_final.receipt.json','document_completion.receipt.json']:
 p=OWN/name;items.append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size})
output('FROZEN_HANDOFF.json',{'task':'SI-P2','directory':str(OWN),'state':'DEVELOPER_AUDIT_COMPLETE_AWAITING_INDEPENDENT_REVIEW','Q_hist':{'raw_rows':171,'raw_unique_tasks':169,'quality_PASS':164,'quality_HOLD':0,'quality_EXCLUDE':7,'final_unique_anchors':162,'B':95,'C':10,'B_minus_C':85,'harm':6,'failure':61},'Q_pin':{'quality_PASS':36,'quality_HOLD':128,'quality_EXCLUDE':7,'final_unique_anchors':36,'B':29,'C':1,'B_minus_C':28,'harm':2,'failure':5},'original_eleven':{'mechanically_supported':11,'unique_C_tasks_after_anchor':10,'excluded_by_quality':0,'one_nonminimum_prefix':'R10_OSR:R8-F23'},'DATA_FEASIBILITY':'NOT_READY','qualified_training_N':'NOT_ESTABLISHED','equal_budget_control':'NOT_ESTABLISHED','learning_gain':'NOT_PROVEN','scientific_calls_added':0,'science_authorization':'NOT_GRANTED','source_scientific_SHA':'2da980f631badc25086d12db60d128ff507d3ae6','analyzer_SHA':'85cbb92395e5e2420c2adeb1fa0634653e742910','historical_R19_cost_unchanged':{'model_generations':5142,'reset_inclusive_environment_operations':7949,'old_177_342_included':True},'all_primary_subprocess_returncodes':0,'artifacts':items,'raw_receipts':receipts,'publication':'Coordinator owned; no commit/push/shared INDEX modification','drafts_and_auxiliary_errors_retained':True})
print('frozen_handoff',sha(OWN/'FROZEN_HANDOFF.json'));print('main_report',sha(report));print('machine_audit',sha(OWN/'pool_quality_audit.json'));print('unchanged_inputs',len(bindings));print('primary_receipts_all_real_zero',len(receipts));print('science_increment',0)
