"""Freeze local SI-P0 prose/evidence; no project imports or scientific checks."""
import datetime
import hashlib
import json
from pathlib import Path


def finalize(ns):
    own=ns['OWN'];digest=ns['digest'];inv=json.loads((own/'experience_inventory.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    check=[]
    for item in inv['input_bindings']:
        current=digest(Path(item['path']))
        check.append({'path':item['path'],'original_audit_sha256':item['sha256_before'],'at_delivery_sha256':current,'unchanged':current==item['sha256_before']})
    if not all(x['unchanged'] for x in check):raise RuntimeError('An original input changed; stop delivery')
    (own/'final_input_hash_check.json').write_text(json.dumps({'checked_at_utc':now,'mode':'file_hash_read_only_not_project_validator','input_count':len(check),'all_unchanged':True,'bindings':check},ensure_ascii=False,indent=2)+'\n')
    expected={'root_final_head.log':'e537f441010077123a307e9d50ea40cf8dad8547','frozen85_final_head.log':'85cbb92395e5e2420c2adeb1fa0634653e742910','executed2da_final_head.log':'2da980f631badc25086d12db60d128ff507d3ae6'}
    for filename,sha in expected.items():
        if (own/filename).read_text().strip()!=sha:raise RuntimeError('Identity changed '+filename)
    for filename in ['root_final_status.log','frozen85_final_status.log','executed2da_final_status.log']:
        if len((own/filename).read_text().splitlines())!=1:raise RuntimeError('Scientific tree has changes '+filename)
    receipts=[json.loads(line) for line in (own/'commands.log').read_text().splitlines() if line.strip()]
    # Real subprocess receipts are recorded by the wrapper, not inferred from text.
    if any(r['exit_code']!=0 for r in receipts):raise RuntimeError('Read command receipt needs explicit review')
    scope={'task_id':'SI-P0-SOL-b1c48c','state':'LOCAL_FROZEN_FOR_COORDINATOR_REVIEW','scientific_permission':'NOT_GRANTED','data_feasibility':'READY_FOR_PROTOCOL_DESIGN','training_data_ready':'NOT_READY','new_scientific_generations':0,'new_environment_operations':0,'new_training':0,'project_analyzer_validator_pytest_invocations':0,'new_policy_replay':0,'agents_spawned_or_messaged':0,'git_commit_push_or_staging':0,'shared_inventory_or_index_modified':False,'budget':'First-round cap 2 person-hours; no other agent work; initial recorded checks 05:46 UTC; finishing within cap','R19_ledger_unchanged':{'model_generations':5142,'reset_inclusive_environment_operations':7949,'includes_old':{'generations':177,'environment_operations':342}},'actual_subprocess_receipts_before_finalization':len(receipts),'receipt_exit_codes':sorted(set(r['exit_code'] for r in receipts)),'authoritative_scope_file':'/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/SOL_RESEARCH_TASK.md','authoritative_scope_sha256':'d7a42a134345b4262c497221cceb4a3ccb066b90f0fcd5e64fee94bd35e8f4af','not_review_pass_or_launch_clearance':True,'checked_at_utc':now}
    (own/'RESOURCE_AND_SCOPE_RECEIPT.json').write_text(json.dumps(scope,ensure_ascii=False,indent=2)+'\n')
    (own/'LITERATURE_READ_SCOPE.json').write_text(json.dumps({'read_date_utc':'2026-10-25','mode':'primary-source read only; no author code executed','sources':[{'url':'https://aclanthology.org/2024.emnlp-main.861/','full_text':'https://aclanthology.org/2024.emnlp-main.861.pdf','read_scope':'abstract, method self-training/reflection data flow and deployment setting'},{'url':'https://arxiv.org/abs/2605.20477','version':'v1','full_text':'https://arxiv.org/html/2605.20477v1','read_scope':'abstract, sections3/4, 5.1 partition and5.3 validation-selection limitation'},{'url':'https://arxiv.org/abs/2610.00372','version':'v1','full_text':'https://arxiv.org/html/2610.00372v1','read_scope':'abstract, controlled paired interventions and router method; not complete experiment reproduction'}],'novelty':'NOT_PROVEN; limited three-paper comparison; no exhaustive priority review'},ensure_ascii=False,indent=2)+'\n')
    exit_table='\n'.join(f"| `{Path(r['log']).stem}` | {r['exit_code']} | `{Path(r['log']).name}` / `.receipt.json` |" for r in receipts)
    md=f'''# SI-P0 RECORD — 本地审计/设计冻结交付

任务 `SI-P0-SOL-b1c48c`。唯一自有目录 `{own}`。协调方独立review未在本文件宣告；publication由协调方处理，当前LOCAL_ONLY。

## 授权与实际工作

唯一任务单SHA256 `d7a42a134345b4262c497221cceb4a3ccb066b90f0fcd5e64fee94bd35e8f4af`匹配。开始按任务核验根/branch/HEAD，随后只读历史report、manifest及已完成TRAIN source/branch；以纯stdlib流式重数既有二元终局、canonical去重、字段来源和哈希，生成不含训练prompt/target的审计索引。另读指定三篇primary论文，写一轮不可执行草案。

没有model/ALFWorld/训练/tokenizer/G2/G3/G4/preflight/policy replay/项目analyzer/项目validator/pytest调用；没有科学代码/测试/提示/协议/adapter变更，没有commit/push/stage、共享INDEX/rootinventory或其他agent文件改动，没有派agent/发线程消息。当前代码树clean，2da为detached HEAD原状，不切branch。本任务不是原36例detector审计的执行。

只在自有目录写stdlib审计脚本/文本/metadata。大raw、weights、adapter、cache、dataset未复制。`historical_paths.log`约1.10MB是早期rg路径元数据输出，超1MB偏好但不是raw树；可由协调方选择不发布该冗余草稿日志。严格≤1MB的`experience_inventory.json`为{(own/'experience_inventory.json').stat().st_size} bytes。其row hash覆盖原JSONL行及换行。

## 当前结论

DATA_FEASIBILITY=READY_FOR_PROTOCOL_DESIGN；TRAINING_DATA_READY=NOT_READY；科学执行NO_GO/NOT_GRANTED。跨已列异质处理的rescue并集17tasks/18states；post-SFT单动作共有经验仅11states/10tasks，light集中且缺clean/cool。普通source成功不等于rescue、多个treatment/K/alias不等于新任务。R19K2两次真实救回和两例CONTINUE本来成功的oracle-over-K2病例在主报告、inventory中分别列明。

未来最小A/B/C草案仅一轮；B/C同候选池/等训练预算，C额外检查paired增量；获取/验证费用分别报告，不能以训练token匹配冒称端到端成本公平。N、科学资源上限、训练配方和可执行命令均未批准或制定成可运行设置。当前不要求澄清才能完成SI-P0，但历史weights身份、旧transition语义、公共投影、独立新TRAIN身份与训练token可用性是未来阻断项。

## 来源与不可变性

完整{len(check)}个已读原件的path/size/before/after SHA在`experience_inventory.json.input_bindings`；交付前再次核对全部相同，见`final_input_hash_check.json`。这只是stdlib文件哈希，不是项目完整性validator。所读Sprint source/R1/R7/R14/正式R19 branches也与原manifest指向hash一致。

正式R19 summary `6ff56b7e9bc31c29bc9afd0c3ceea43c4fdf53b2addb29d3ce9f2c5e99b5d3c4`、opportunity report `92c066ad1c9c7f187430db82ad6285800e4f31005a1fd2933231d30d695df4bc`、独立验收 `7331b865778481ab4e1b10943eac0e4090ea004e214dbdfff283cfbe042833e6`均匹配任务提供值；原branches `eff9b5e74d3d5daa928cb662dcc59fc3f434f66796b673679d40b374f3c8636f`不变。未调用其main/statistics/report流水线。

旧失败run8个文件均哈希保留；其原RUNNING / in_progress元数据没有改成新失败。原完成G3所有已读事件/manifest/source/branches不改。R19campaign仍5142generations/7949 reset-inclusive ops，含旧177/342；此次增量0，不是全项目费用。

根HEAD `{expected['root_final_head.log']}`；analyzer `{expected['frozen85_final_head.log']}`；executedG3 `{expected['executed2da_final_head.log']}`。最终status/head的独立只读命令均有真实exit凭据。

## 真实执行凭据与审计草稿修正

`commands.log`是receipt wrapper追加的真实subprocess.returncode。下表在finalization开始时覆盖{len(receipts)}条记录，全部exit0；随后finalization自己的log/receipt由同wrapper追加。`FILE_HASHES.sha256`在最后这些append完成后才seal。

| 本轮只读/文档操作 | 实际exit | 原始日志与receipt |
|---|---:|---|
{exit_table}

核心历史重数以`inventory_audit_final.log/.receipt.json`为准；`inventory_summary_final.log`为精简视图。无pytest/test PASS可报告，因为未运行测试。

早期stdlib草稿探测曾把事件kind/嵌套generation/Stage2 map路径读错；原件未缺失，最终4926 action maps/4965 total generations已按真实schema纠正。保留各草稿原日志，详见`DRAFT_AUDIT_CORRECTIONS.md`。两个推测R18小写文件名检索由exec工具返回exit2后，改用真实大写路径成功；该辅助发现命令不在wrapper表内，不能把它伪记exit0。默认沙盒最初无法创建命名空间；本任务经自动批准的显式窄范围读取/自有目录写入才继续，无审批拒绝或绕过。

## 冻结、交接与资源

首条已记录检查约2026-10-25 05:46UTC；本记录准备于{now}，本轮仅此agent工作，首轮2人时上限内完成，未为凑positive延长采集。`RESOURCE_AND_SCOPE_RECEIPT.json`记录边界。指定三篇文献读范围见`LITERATURE_READ_SCOPE.json`；未复现论文、无创新首创/效能证明。

主要交付四份markdown及`experience_inventory.json`。`FROZEN_HANDOFF.json`列绝对path/size/SHA；`FILE_HASHES.sha256`覆盖封存时所有其他自有文件（不自哈希，亦不包含随后生成的`SEAL_CHECK.json`）；`SEAL_CHECK.json`绑定该manifest并记录逐文件读取核对结果。最后seal的真实退出由桌面exec返回，不是独立科研验收。

协调方可取原字节副本自行发布；本线程不触共享索引、不上传、不commit/push。下一步仅等待协调方独立审阅/明确新任务，不自行启动数据构建、实验、训练、统计或新复盘循环。
'''
    (own/'RECORD.md').write_text(md)
    print(json.dumps({'original_input_files':len(check),'unchanged':True,'receipt_count_before_this_wrapper_return':len(receipts),'data_feasibility':scope['data_feasibility'],'training_data_ready':scope['training_data_ready'],'scientific_permission':'NOT_GRANTED'},ensure_ascii=False))


def seal(ns):
    own=ns['OWN'];digest=ns['digest']
    # This mode is invoked directly only after wrapper appended finalization receipt.
    required=['SELF_EXPERIENCE_FEASIBILITY.md','experience_inventory.json','MINIMAL_SELF_IMPROVEMENT_PROTOCOL_DRAFT.md','INNOVATION_COMPARISON.md','RECORD.md','commands.log','INPUT_HASHES.sha256','final_input_hash_check.json','RESOURCE_AND_SCOPE_RECEIPT.json']
    required_rows=[{'path':str(own/name),'bytes':(own/name).stat().st_size,'sha256':digest(own/name)} for name in required]
    handoff={'task_id':'SI-P0-SOL-b1c48c','state':'LOCAL_FROZEN_FOR_COORDINATOR_INDEPENDENT_REVIEW','not_independent_review_pass':True,'scientific_permission':'NOT_GRANTED','data_feasibility':'READY_FOR_PROTOCOL_DESIGN','training_data_ready':'NOT_READY','root_head':'e537f441010077123a307e9d50ea40cf8dad8547','frozen_analyzer_head':'85cbb92395e5e2420c2adeb1fa0634653e742910','executed_G3_head':'2da980f631badc25086d12db60d128ff507d3ae6','R19_cost_unchanged':[5142,7949],'files':required_rows,'publication_owner':'coordinator; no commit/push/shared index mutation by this task','next_action':'wait for independent review and new explicit task'}
    (own/'FROZEN_HANDOFF.json').write_text(json.dumps(handoff,ensure_ascii=False,indent=2)+'\n')
    files=sorted(p for p in own.iterdir() if p.is_file() and p.name not in {'FILE_HASHES.sha256','SEAL_CHECK.json'})
    pairs=[(digest(p),p) for p in files]
    (own/'FILE_HASHES.sha256').write_text(''.join(h+'  '+str(p)+'\n' for h,p in pairs))
    if not all(digest(p)==h for h,p in pairs):raise RuntimeError('Own frozen file changed while sealing')
    seal={'manifest_path':str(own/'FILE_HASHES.sha256'),'manifest_sha256':digest(own/'FILE_HASHES.sha256'),'covered_files':len(pairs),'all_recorded_blobs_match':True,'scope':'Local stdlib file-byte comparison only; not scientific validator or independent review','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'FROZEN_HANDOFF_sha256':digest(own/'FROZEN_HANDOFF.json')}
    (own/'SEAL_CHECK.json').write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'seal':seal,'required_files':required_rows},ensure_ascii=False,indent=2))
