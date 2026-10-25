"""Additive CAP/role clarification; stdlib, sealed records only, no project calls."""
from pathlib import Path
import hashlib,json
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T075610Z__CODEX__si-p2-common-quality__b04b8b')
INTERPRETATION=OWN.parent/'2026-10-25T075610Z__SOL__si-p2-same-pool-review__b04b8b/CAP_AND_ROLE_INTERPRETATION.md'
EXPECTED_INTERPRETATION='964b5a31dcb78516c16c61780a91be677c55964a6c4e044c505b3d360349ee0c'
EXPECTED_MANIFEST='35119df7b4416cf870eea7c5d8d4e85ceafc0b8878f757afd48723bf75620553'
CASE='R19_K1:R19-random-control-47bcdcad9c56a38ac146'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def new(name,obj):
 p=OWN/name
 with p.open('x',encoding='utf-8') as f:
  if isinstance(obj,str):f.write(obj)
  else:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
 return {'path':str(p),'sha256':sha(p)}
assert sha(INTERPRETATION)==EXPECTED_INTERPRETATION
manifest=OWN/'FILE_HASHES.sha256';assert sha(manifest)==EXPECTED_MANIFEST
old=[]
for line in manifest.read_text().splitlines():
 expected,path=line.split('  ',1);p=Path(path);assert p.is_relative_to(OWN);assert sha(p)==expected
 old.append({'path':path,'sha256_before':expected})
assert len(old)==55
p=OWN/'pool_quality_audit.json';a=json.loads(p.read_bytes());c=next(x for x in a['cases'] if x['case_id']==CASE)
assert c['Q_hist']==c['Q_pin']=='PASS'
assert c['labels']['CONTINUE']==c['labels']['recover']==1
s1=c['recorded_inference_tokens']['stage1'];s2=c['recorded_inference_tokens']['stage2']
assert s1['output_complete'] is True and s1['token_cap_reached'] is True and s1['generated_tokens']==s1['max_new_tokens']==40
assert s2['output_complete'] is True and s2['token_cap_reached'] is False and s2['generated_tokens']==5 and s2['max_new_tokens']==16
assert c['r19_evidence']['initial_stage1']['event_id']=='0298b176cd2ecde03292a043a54f9e771f3f95f29073a0f71d49bc989259dd76'
assert c['r19_evidence']['initial_stage2']['event_id']=='760cd1fed1648e86389223beca3421be35f575d995675a1c25f675b7493f608f'
assert c['first_target']['stage1_status']=='valid' and c['first_target']['parser_status']=='selected' and c['first_target']['executed'] is True
for q in ('Q_hist','Q_pin'):
 sets=a['pool_sets'][q]['sets']
 assert CASE in sets['B']['case_ids'] and CASE in sets['B_minus_C']['case_ids'] and CASE not in sets['C']['case_ids']
md='''# SI-P2 CAP 与角色解释追加确认

已读取并核验协调方 CAP_AND_ROLE_INTERPRETATION.md，SHA256 964b5a31dcb78516c16c61780a91be677c55964a6c4e044c505b3d360349ee0c。解释适用于既有冻结契约，不增加质量规则或科学授权。

case R19_K1:R19-random-control-47bcdcad9c56a38ac146 在**已封存最终v2交付**中已为 Q_hist=PASS、Q_pin=PASS，两个口径均为最终anchor；CONTINUE=1、K1=1，属于B与B\\C，不属于C。第一Stage2完整、selected、原动作确实执行。

原Stage1的output_complete=true、token_cap_reached=true、generated_tokens=max_new_tokens=40、status=valid；按原生成器及parser契约，上限EOS可为完整输出，不能仅因cap=true判截断。最终v2已统一按output_complete解释该字段；初稿误排及其纠正过程原字节均已保留。本次不更改集合、anchor、原label、质量mask或任何旧交付，也不因该neutral-success增加rescue。

冻结计数保持：Q_hist 164 PASS/7 EXCLUDE，最终162任务，B95/C10/neutral85；Q_pin 36 PASS/128 HOLD/7 EXCLUDE，最终36任务，B29/C1/neutral28。原11项机械目标仍成立，训练N未建立、DATA_FEASIBILITY=NOT_READY、学习收益NOT_PROVEN。

分工解释也已接收：Luna的独立parent身份/标签、过滤前anchor计划和预算记录，其locator受限的局部核对数不能直接作为共同质量mask或共同质量后的容量。最终共同质量由完整source/replay审计与协调方独立原件检查交叉决定。本次未读取Luna未完成文件，未对其实际交付另作裁定或要求其扩查。

这份说明只绑定协调方新解释与既有封存记录。55项旧manifest目标与旧manifest保持原字节；新增文件使用独立CAP_ROLE_ADDENDUM_HASHES.sha256，不追加旧commands.log或重写FILE_HASHES。真实新增stdlib程序回执另存cap_role_addendum.receipt.json，新增科学调用0。无模型/环境/训练/tokenizer/旧脚本/项目analyzer或validator/pytest/replay/G3/G4/preflight，无科学代码、sharedINDEX、commit或push操作。不宣称独立review PASS。
'''
artifacts=[new('CAP_AND_ROLE_INTERPRETATION_ADDENDUM.md',md)]
for x in old:
 x['sha256_after']=sha(Path(x['path']));x['unchanged']=x['sha256_before']==x['sha256_after'];assert x['unchanged']
assert sha(manifest)==EXPECTED_MANIFEST and sha(INTERPRETATION)==EXPECTED_INTERPRETATION
artifacts.append(new('cap_role_addendum_evidence.json',{'interpretation':{'path':str(INTERPRETATION),'sha256':EXPECTED_INTERPRETATION},'frozen_original_manifest':{'path':str(manifest),'sha256':EXPECTED_MANIFEST},'frozen_machine_audit':{'path':str(p),'sha256':sha(p)},'case_id':CASE,'case_before_and_after_disposition':'UNCHANGED_PASS_B_MINUS_C_NOT_C','case_flags':{'stage1':s1,'stage2':s2},'original_event_references':c['r19_evidence'],'old_55_files':old,'no_other_agent_file_read':True,'scientific_calls_added':0}))
artifacts.append(new('CAP_ROLE_ADDENDUM_RECORD.md','''# CAP/role 追加记录

只使用新写cap_role_addendum.py（OWN由__file__绑定并校验）读取协调方指定解释及既有本轮封存JSON/manifest；没有执行任何旧脚本或项目模块。按原记录确认本case早已在最终v2为neutral-success并保留，两口径质量/集合不变。55项旧文件与旧manifest未改；真实子进程argv、stdout/returncode、程序hash见cap_role_addendum.receipt.json与同名log。新增独立hash清单绑定本追加6项文件，不覆盖旧FILE_HASHES/commands.log。科学增量0，训练N与收益未证明；不宣称独立review PASS。
'''))
print(json.dumps({'case_id':CASE,'already_retained_in_frozen_final_v2':True,'Q_hist':'PASS','Q_pin':'PASS','membership':'neutral-success, B_minus_C, not C','old_files_unchanged':55,'scientific_calls_added':0,'artifacts':artifacts},ensure_ascii=False,indent=2))
