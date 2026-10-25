"""Additive SI-P1 source/axis clarification. Reads records and source text only."""
from pathlib import Path
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import subprocess

OWN = Path('/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__CODEX__si-p1-eleven-targets__caae4c')
COORD = Path('/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c')
SRC = Path('/home/lizening/wt-r19-g4-consumer-contract-repair')
EXPECTED_MANIFEST = '14189f7752494eee84fdc6adad161957b0afe34b597f68fedce845d4d5976572'
EXPECTED_AUDIT = 'f8fe8141d2c431274082856105a2b8aa81c76b774fe624fe50c5d33bf77ba901'
EXPECTED_SOURCE = {
    'src/trajectory/trajectory.py': '31bbd35c7960ddcf87c6d1c38376d10aaf95e741f9dedecbe4f8e23a97fdb958',
    'src/env/alfworld.py': '086a4a6fc7aac6250230ceeb5f1fa2f198ef4d529bc5af6c476181cd1c7f959d',
    'scripts/run_r19_experiment.py': '06bb8e11c3cc9e9484b8d5731c86690b97a4c445a0e5aa16b72b912c6c14dd5c',
}
EXPECTED_AUTHORITY = {
    'SOL_RESEARCH_TASK.md': 'adcb03193e40baf839e14f9d521e3f7a309c28ce901d6a4dcf1d044660ec579b',
    'FIXED_ELEVEN_CASES.json': 'e5039568d8213fa5d879ffb2aec8c44e932fa99bc4de67bd527ebcae67ccb45b',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump_new(name, data):
    p = OWN / name
    with p.open('x', encoding='utf-8') as f:
        if isinstance(data, str):
            f.write(data)
        else:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write('\n')
    return {'path': str(p), 'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size}


def method(text, name):
    nodes = [n for n in ast.walk(ast.parse(text)) if isinstance(n, ast.FunctionDef) and n.name == name]
    assert len(nodes) == 1, (name, len(nodes))
    n = nodes[0]
    return {'method': name, 'line': n.lineno, 'end_line': n.end_lineno,
            'AST_sha256': sha(ast.dump(n, include_attributes=False).encode()),
            'source_text': ast.get_source_segment(text, n)}


manifest_path = OWN / 'FILE_HASHES.sha256'
manifest_bytes = manifest_path.read_bytes()
assert sha(manifest_bytes) == EXPECTED_MANIFEST
frozen_before = []
for line in manifest_bytes.decode().splitlines():
    expected, path = line.split('  ', 1)
    p = Path(path)
    assert p.parent == OWN
    observed = sha(p.read_bytes())
    assert observed == expected, path
    frozen_before.append({'path': str(p), 'expected_sha256': expected, 'sha256_before': observed})
assert len(frozen_before) == 51
for p in [manifest_path, OWN / 'SEAL_CHECK.json']:
    h = sha(p.read_bytes())
    frozen_before.append({'path': str(p), 'expected_sha256': h, 'sha256_before': h})

bindings = []
for name, expected in EXPECTED_AUTHORITY.items():
    p = COORD / name
    observed = sha(p.read_bytes())
    assert observed == expected
    bindings.append({'path': str(p), 'sha256_before': observed})
audit_path = OWN / 'eleven_target_audit.json'
audit_bytes = audit_path.read_bytes()
assert sha(audit_bytes) == EXPECTED_AUDIT
audit = json.loads(audit_bytes)
assert len(audit['cases']) == 11
assert len({c['canonical_task'] for c in audit['cases']}) == 10
historical_path = OWN / 'historical_contracts.json'
historical = json.loads(historical_path.read_bytes())
bindings.append({'path': str(historical_path), 'sha256_before': sha(historical_path.read_bytes())})
texts = {}
for rel, expected in EXPECTED_SOURCE.items():
    p = SRC / rel
    b = p.read_bytes()
    assert sha(b) == expected
    texts[rel] = b.decode()
    bindings.append({'path': str(p), 'sha256_before': expected})

current_methods = {
    'Trajectory.succeeded': method(texts['src/trajectory/trajectory.py'], 'succeeded'),
    'AlfWorldTextEnvironment.step': method(texts['src/env/alfworld.py'], 'step'),
    'R19.record_step': method(texts['scripts/run_r19_experiment.py'], 'record_step'),
    'R19.run_sft_suffix': method(texts['scripts/run_r19_experiment.py'], 'run_sft_suffix'),
}
assert 'self.steps[-1].done and self.steps[-1].reward > 0' in current_methods['Trajectory.succeeded']['source_text']
assert 'success = int(bool(transition.done and float(transition.reward) > 0))' in current_methods['R19.run_sft_suffix']['source_text']

# These are Git object reads, never imports or calls to any historical source.
source_reads = []
for stage, revision in [
    ('R4', '7a01a6107b4bc9c994893220aab078af39fe4fff'),
    ('R10_OSR', '8926d8fb10e634489031de3da910c572b50d8d44'),
    ('R16_OSR', 'd1ef841ea9dc7423177fb7647906e2e719f0fbe7'),
    ('R19_K1', '2da980f631badc25086d12db60d128ff507d3ae6'),
]:
    rel = 'src/trajectory/trajectory.py'
    argv = ['git', '-C', str(SRC), 'show', revision + ':' + rel]
    result = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    row = {'stage': stage, 'revision': revision, 'path': rel, 'argv': argv,
           'returncode': result.returncode, 'stdout_sha256': sha(result.stdout),
           'stderr': result.stderr.decode(errors='replace')}
    assert result.returncode == 0, row
    found = method(result.stdout.decode(), 'succeeded')
    row['historical_method'] = found
    row['matches_frozen85_AST'] = found['AST_sha256'] == current_methods['Trajectory.succeeded']['AST_sha256']
    assert row['matches_frozen85_AST'], stage
    source_reads.append(row)
rel = 'scripts/run_r19_experiment.py'
argv = ['git', '-C', str(SRC), 'show', '2da980f631badc25086d12db60d128ff507d3ae6:' + rel]
result = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
row = {'stage': 'R19_K1', 'revision': '2da980f631badc25086d12db60d128ff507d3ae6',
       'path': rel, 'argv': argv, 'returncode': result.returncode,
       'stdout_sha256': sha(result.stdout), 'stderr': result.stderr.decode(errors='replace'), 'methods': []}
assert result.returncode == 0, row
for label, name in [('R19.record_step', 'record_step'), ('R19.run_sft_suffix', 'run_sft_suffix')]:
    found = method(result.stdout.decode(), name)
    found['matches_frozen85_AST'] = found['AST_sha256'] == current_methods[label]['AST_sha256']
    assert found['matches_frozen85_AST']
    row['methods'].append(found)
source_reads.append(row)
wrapper_links = [c for c in historical['contracts'] if c['method'] == 'AlfWorldTextEnvironment.step']
assert len(wrapper_links) == 4 and all(c['method_AST_equal'] for c in wrapper_links)

rows = []
for index, c in enumerate(audit['cases']):
    assert c['checks'] and all(v is True for v in c['checks'].values())
    terminal = c['terminal_corroboration']
    recover = terminal['recovery_branch_terminal']
    control = terminal['CONTINUE_terminal']
    # Same original terminal predicate on already audited fields; no policy replay.
    rec_pred = int(bool(recover['done'] and float(recover['reward']) > 0))
    con_pred = int(bool(control['done'] and float(control['reward']) > 0))
    assert (con_pred, rec_pred) == (0, 1)
    raw_won = 'RAW_WON_EXPLICIT_TRUE' if recover['won_entries'] else 'RAW_WON_NOT_RECORDED'
    control_won = 'RAW_WON_EXPLICIT_FALSE' if control['won_entries'] else 'RAW_WON_NOT_RECORDED'
    if recover['won_entries']:
        assert all(e['value'] is True for e in recover['won_entries'])
    if control['won_entries']:
        assert all(e['value'] is False for e in control['won_entries'])
    rows.append({
        'case_id': c['case_id'], 'canonical_task': c['canonical_task'],
        'original_audit': {'path': str(audit_path), 'sha256': EXPECTED_AUDIT, 'pointer': '/cases/' + str(index)},
        'input_target_axis': 'INPUT_TARGET_LINEAGE_SUPPORTED',
        'basis': 'All original mechanical source/replay/public-input/ordered-map/first-target/execution checks are true; missing won is not a target invalidity.',
        'original_checks': c['checks'],
        'model_identity_axis': c['model_identity']['axis'],
        'terminal_corroboration_axis': {
            'original_success_predicate': 'terminal done && reward > 0',
            'historical_recover_success': 1, 'historical_CONTINUE_success': 0,
            'recorded_terminal_predicate_check': {'recover': rec_pred, 'CONTINUE': con_pred},
            'recover_raw_won_status': raw_won, 'CONTINUE_raw_won_status': control_won,
            'recover_terminal': recover, 'CONTINUE_terminal': control,
            'historical_success_labels_retained': True,
            'missing_won_is_new_G3_failure': False,
        },
        'old_combined_disposition_preserved_in_frozen_original': c['disposition'],
        'overall_training_eligibility': 'HOLD_NOT_READY',
        'training_row_approved': False, 'learning_gain': 'NOT_PROVEN',
        'teacher_target': 'Executed adapter-off first recovery action only; adapter-on suffix remains separate.',
    })
assert Counter(r['terminal_corroboration_axis']['recover_raw_won_status'] for r in rows) == {'RAW_WON_EXPLICIT_TRUE': 9, 'RAW_WON_NOT_RECORDED': 2}
assert Counter(r['model_identity_axis'] for r in rows) == {'MODEL_IDENTITY_PARTIAL': 10, 'MODEL_IDENTITY_PINNED': 1}

clarification = {
    'schema': 'SI_P1_SUCCESS_AXES_CLARIFICATION_V1', 'task_id': 'SI-P1-TARGET-caae4c',
    'scope': 'Additive reviewer clarification of frozen 11-case audit; no new case, raw relabel, policy evaluation or training dataset.',
    'scientific_permission': 'NOT_GRANTED', 'scientific_calls_added': 0,
    'frozen_original_audit_sha256': EXPECTED_AUDIT,
    'frozen_original_manifest_sha256': EXPECTED_MANIFEST,
    'summary': {'rows': 11, 'canonical_tasks': 10, 'input_target_lineage_supported': 11,
                'model_identity_partial': 10, 'model_identity_pinned': 1,
                'recover_RAW_WON_EXPLICIT_TRUE': 9, 'recover_RAW_WON_NOT_RECORDED': 2,
                'historical_CONTINUE0_recover1_retained': 11,
                'qualified_training_N': 'NOT_ESTABLISHED', 'DATA_FEASIBILITY': 'NOT_READY',
                'B_pool_ready': False, 'learning_gain': 'NOT_PROVEN'},
    'semantic_limit': 'Original repository success labels use done and positive terminal reward. Wrapper forwards underlying reward and done. Static source does not certify a historical installed-environment binary or a universal reward/won equivalence; absence of raw won remains a corroboration limit, not a replacement failure label.',
    'cases': rows,
}
outputs = [dump_new('eleven_axes_clarification.json', clarification)]
md = '''# SI-P1：原成功谓词与逐案独立轴澄清

本补充仅澄清已封存的11状态/10任务审计，原文件与原始证据保持不变。此前汇总的9项 `INPUT_TARGET_LINEAGE_SUPPORTED`、2项 `HOLD_EVIDENCE` 把终态 won 佐证缺口纳入了综合 disposition；该计数不能解释成仅9项机械目标有效。独立机械来源链结论为 **11/11 INPUT_TARGET_LINEAGE_SUPPORTED**，训练资格仍为 **NOT_READY / qualified N NOT_ESTABLISHED**。

原成功谓词经静态源码核对：

- `src/trajectory/trajectory.py:59–62` 的 `Trajectory.succeeded` 是最后一步 `done && reward>0`。R4、R10、R16、executed R19 的四个真实 Git 对象中，该方法 AST 均与冻结85版本一致；逐条真实 Git 返回码及文本哈希见源证据文件。
- `scripts/run_r19_experiment.py:2204–2277` 的实际方法名为 `run_sft_suffix`，2264行按 `done && reward>0` 写入 success；它消费原 Transition 对象。executed2da 与冻结85方法 AST 一致。
- `src/env/alfworld.py:58–72` 原 wrapper 将底层 rewards/dones 转成 float/bool，并把 info 放在 metadata。它没有以 won 替换 reward；前轮已封存的四个历史 wrapper 方法对照一致。
- `scripts/run_r19_experiment.py:1635–1663` 的 `record_step` 导出 observation、valid_actions、reward、done、truncated、executed_command，未导出 metadata/won；返回值仍含原 Transition 对象。executed2da 与85该方法 AST 一致。因此 R19 导出缺 won 与其既有成功契约兼容。

11例均保留历史 CONTINUE=0、recover=1；已封存终态字段也符合上述原谓词。9例 raw 中有 recovery done=true、reward=1、won=true；R4:R2-F01 与 R19 K1 例的 recovery 有 done=true、reward=1，won 标为 **RAW_WON_NOT_RECORDED**。R19 的 CONTINUE raw 也没有 won，不补造 won=false。R4 CONTINUE 则有显式 won=false。

缺 won 是原始字段佐证边界，不能作为新的机械非法目标、G3失败、旧成功标签撤销或新增追溯性验收门槛。本轮没有新增终局规则，没有依据 subgoal、teacher card、塑形奖励或未来 suffix 给第一动作发明局部成功标签。恢复分支最终成功不证明第一动作单独造成成功，更不证明该动作可被 P0 学到或提高泛化表现。

三轴逐例保留如下；L=INPUT_TARGET_LINEAGE_SUPPORTED，M=MODEL_IDENTITY_PARTIAL，P=MODEL_IDENTITY_PINNED：

| case | 输入→目标 | 模型身份 | recovery raw won | 历史 CONTINUE→recover |
|---|---|---|---|---|
'''
for r in rows:
    m = 'P' if r['model_identity_axis'] == 'MODEL_IDENTITY_PINNED' else 'M'
    won = r['terminal_corroboration_axis']['recover_raw_won_status']
    md += '| ' + r['case_id'] + ' | L | ' + m + ' | ' + won + ' | 0→1保留 |\n'
md += '''
机械轴依据原审计已核对的动作前公共输入、既有 replay、完整有序 map、原始第一动作输出及实际执行证据；模型身份轴仍为10 PARTIAL、1 PINNED。第三轴记录原终态谓词与 raw won 佐证程度。学习收益另列 NOT_PROVEN；不能由任一轴替代。

范围限制：这里只确立原仓库谓词与 wrapper 的透传关系，未重新认证历史安装的 ALFWorld/TextWorld 二进制，也未证明所有状态上 reward 与 won 普遍等价。已记录的 done/正奖励与原成功标签应如实保留；未知的额外原始佐证仍是未知。

11项仍是候选审计索引。原 adapter-off 第一 recovery 目标与 adapter-on suffix 分开；不增加 K2、不搬运 teacher subgoal/card、不改变公共输入。11状态中的同 task 两 prefix 仍计为一个任务；B_pool 尚未建立，不能把11个筛出的正例当可识别筛选增益的对照池。训练资格整体 HOLD_NOT_READY 反映数据/对照/身份等未决条件，不以缺 won 单独否定机械来源链。

本补充只读取本轮已封存 JSON、原源码及 Git 对象；未执行任何旧 P0/P1 脚本，未读取 Luna 未完成文件，未导出训练 prompt/JSONL，未运行项目 analyzer/validator、pytest、模型、环境、replay、训练、G3/G4或 preflight。科学增量0；R19历史累计5142 generations / 7949环境操作（含177/342）保持原样。本补充是开发侧审计澄清，独立审查与后续许可仍由协调方决定。
'''
outputs.append(dump_new('SUCCESS_PREDICATE_AND_AXES_ADDENDUM.md', md))

for item in frozen_before:
    item['sha256_after'] = sha(Path(item['path']).read_bytes())
    item['unchanged'] = item['sha256_before'] == item['sha256_after'] == item['expected_sha256']
assert all(i['unchanged'] for i in frozen_before)
for item in bindings:
    item['sha256_after'] = sha(Path(item['path']).read_bytes())
    item['unchanged'] = item['sha256_before'] == item['sha256_after']
assert all(i['unchanged'] for i in bindings)
evidence = {
    'created_at_UTC': datetime.now(timezone.utc).isoformat(),
    'operation': 'Static source and sealed-record clarification only',
    'original_manifest_entries_checked': 51,
    'original_manifest_and_seal_also_checked': True,
    'frozen_original_files_before_after': frozen_before,
    'current_source_and_authority_before_after': bindings,
    'current_static_methods': current_methods,
    'historical_source_object_reads_real_receipts': source_reads,
    'wrapper_historical_bindings_referenced_from_frozen_previous_audit': wrapper_links,
    'original_raw_hash_checks': {
        'path': str(OWN / 'final_input_hash_check.json'),
        'sha256': sha((OWN / 'final_input_hash_check.json').read_bytes()),
        'scope': 'Referenced existing 35-input pre/post receipt; not a new full raw rehash or analysis.'},
    'project_modules_imported_or_executed': False,
    'old_audit_scripts_executed': False,
    'new_policy_replay_or_scientific_calls': 0,
}
outputs.append(dump_new('success_axes_source_and_freeze_evidence.json', evidence))
record = '''# SI-P1 成功谓词澄清追加记录

任务 SI-P1-TARGET-caae4c。按协调方最新只读澄清，在唯一自有目录创建本补充；所有既有文件保持原字节。原 FILE_HASHES.sha256 的51条全部核对，manifest与SEAL_CHECK另核对；当前源码/任务单/固定case清单前后哈希一致。输入输出具体路径和SHA见 success_axes_source_and_freeze_evidence.json 与本补充单独hash清单。

新增程序 success_axes_clarification.py 仅使用stdlib读已封存JSON及源码文本，并通过 git show 读取固定历史 Git 对象；没有导入项目模块，没有执行任何旧脚本。5次源文件对象读取的真实argv、returncode、stdout hash、stderr及方法对照在源证据JSON。本追加程序本身的真实stdout/returncode由 success_axes_clarification.receipt.json 独立保存；成功执行不是科学/独立review PASS。

新建主文 SUCCESS_PREDICATE_AND_AXES_ADDENDUM.md；逐案数据 eleven_axes_clarification.json。旧审计的9/2综合disposition保留原样，新补充澄清机械输入目标轴为11/11来源链成立，原0→1标签全部保留；9例won显式一致、2例RAW_WON_NOT_RECORDED；10模型身份PARTIAL、1PINNED。训练N未建立，DATA_FEASIBILITY=NOT_READY，learning_gain=NOT_PROVEN，B_pool未就绪。

不修改科学树、原raw、任何其他agent文件、旧目录、sharedINDEX/rootinventory，不commit/push，不运行模型、环境、训练、tokenizer、项目analyzer/validator/pytest、source/replay/G2/G3/G4/preflight或policy评估。本补充科学调用0。后续独立审查/发布由协调方负责。
'''
outputs.append(dump_new('SUCCESS_AXES_ADDENDUM_RECORD.md', record))
print(json.dumps({'operation_completed': 'static_additive_clarification', 'case_rows': 11,
                  'mechanical_lineages_supported': 11, 'raw_won_missing_recovery_rows': 2,
                  'old_manifest_entries_unchanged': 51,
                  'historical_source_git_read_returncodes': [r['returncode'] for r in source_reads],
                  'science_calls_added': 0, 'outputs': outputs}, ensure_ascii=False, indent=2))
