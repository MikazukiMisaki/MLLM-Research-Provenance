# 澄清：本研究的裸编号参考与项目解析器

本研究的裸编号参考是**先对解码文本去除首尾空白，再检查完整 `A` 加三位数字，且编号存在本题映射**的研究指标。它不调用、不替代或完整模拟任何项目生产解析器。旧方案中“裸编号参考”的措辞不得理解成冻结 H4 基线的 parser。

核对 `reports/SPRINT_1_5_FINAL.md` 所记 H4 实现提交 `08bc212d7b2ed1e38665f4b3049638ffe3a60005`：该版本的 `src/models/action_parser.py` 中，`parse_action_id` 要求形如 `Action-ID: Axyz` 的唯一非空行并检查映射；其源文件 SHA-256 为 `0a1c668d590980d1d8cdd4104a2b3c9aa851037fc238a2c73c45b57ab4432fbe`。该实现的 `src/models/qwen.py` 在 indexed 决策中调用该解析器。实际任务还受采集器、生成和环境接口等条件约束；本研究未运行该冻结策略或验证其生产行为。

当前工作树 `src/recovery/two_stage_v2.py` 的 `parse_bare_stage_two_output` 则检查生成是否完成，并对未去首尾空白的 `generation.raw_output` 完整匹配裸编号后再查映射；被核查文件 SHA-256 为 `ed4fc18621eea343f40c216ff3b3c36c65deb817144a718df3bf75ada5ecdfb2`。这与本研究自行去空白的规则也不完全相同；本研究没有调用该阶段解析器或声称数值等价。

结果出现后，使用同一本机 tokenizer 将保存的输出 token 去除末尾 EOS，以 `skip_special_tokens=True` 解码，并在**不调用 `.strip()`** 的条件下检查。动作编号因子研究的 32 次中，32/32 的解码文本与其去首尾空白的形式相同，14 条形状是裸编号、18 条形状是方括号编号；进度规则探针 16/16 无首尾空白变化且全部为方括号形状。这只是对这 48 条保存 token 的同机核查，不证明其他输出没有空白，也不认证模型权重、物理执行或完整 parser 的效果。

可选 `audit_unstripped_tokens.py` 使用本地 tokenizer 对本包脱敏日志重新计算形状数；它需要 Transformers 和用户指定的本地 tokenizer 目录，但不加载模型权重或使用 GPU。标准库的正式 CPU 复算入口不依赖此可选核查。
