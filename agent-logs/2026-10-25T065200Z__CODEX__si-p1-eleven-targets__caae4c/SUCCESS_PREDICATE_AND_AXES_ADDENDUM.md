# SI-P1：原成功谓词与逐案独立轴澄清

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
| R4:R2-F01 | L | M | RAW_WON_NOT_RECORDED | 0→1保留 |
| R10_OSR:R8-F02 | L | M | RAW_WON_EXPLICIT_TRUE | 0→1保留 |
| R10_OSR:R8-F20 | L | M | RAW_WON_EXPLICIT_TRUE | 0→1保留 |
| R10_OSR:R8-F21 | L | M | RAW_WON_EXPLICIT_TRUE | 0→1保留 |
| R10_OSR:R8-F22 | L | M | RAW_WON_EXPLICIT_TRUE | 0→1保留 |
| R10_OSR:R8-F23 | L | M | RAW_WON_EXPLICIT_TRUE | 0→1保留 |
| R16_OSR:R15-F01 | L | M | RAW_WON_EXPLICIT_TRUE | 0→1保留 |
| R16_OSR:R15-F22 | L | M | RAW_WON_EXPLICIT_TRUE | 0→1保留 |
| R16_OSR:R15-F23 | L | M | RAW_WON_EXPLICIT_TRUE | 0→1保留 |
| R16_OSR:R15-F25 | L | M | RAW_WON_EXPLICIT_TRUE | 0→1保留 |
| R19_K1:R19-failure-b3ab21b8e193f6adf6ff | L | P | RAW_WON_NOT_RECORDED | 0→1保留 |

机械轴依据原审计已核对的动作前公共输入、既有 replay、完整有序 map、原始第一动作输出及实际执行证据；模型身份轴仍为10 PARTIAL、1 PINNED。第三轴记录原终态谓词与 raw won 佐证程度。学习收益另列 NOT_PROVEN；不能由任一轴替代。

范围限制：这里只确立原仓库谓词与 wrapper 的透传关系，未重新认证历史安装的 ALFWorld/TextWorld 二进制，也未证明所有状态上 reward 与 won 普遍等价。已记录的 done/正奖励与原成功标签应如实保留；未知的额外原始佐证仍是未知。

11项仍是候选审计索引。原 adapter-off 第一 recovery 目标与 adapter-on suffix 分开；不增加 K2、不搬运 teacher subgoal/card、不改变公共输入。11状态中的同 task 两 prefix 仍计为一个任务；B_pool 尚未建立，不能把11个筛出的正例当可识别筛选增益的对照池。训练资格整体 HOLD_NOT_READY 反映数据/对照/身份等未决条件，不以缺 won 单独否定机械来源链。

本补充只读取本轮已封存 JSON、原源码及 Git 对象；未执行任何旧 P0/P1 脚本，未读取 Luna 未完成文件，未导出训练 prompt/JSONL，未运行项目 analyzer/validator、pytest、模型、环境、replay、训练、G3/G4或 preflight。科学增量0；R19历史累计5142 generations / 7949环境操作（含177/342）保持原样。本补充是开发侧审计澄清，独立审查与后续许可仍由协调方决定。
