# Sol Research SI-E1实现任务

新的用户授权工程继续，阅读 /home/lizening/research-notes/agent-logs/2026-10-25T102943Z__SOL__si-e1-engineering-review__sie1_b8f6/COMMON_ENGINEERING_CONTRACT.md 及前SI-P3权威协议/独立review。你的provenance OWN=/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6。

请从exact85cbb923建立独立 /home/lizening/wt-si-p3-engineering-contracts，branch codex/si-p3-engineering-contracts；先核对若已存在不要覆盖，报告真实状态。不要在authoritative/rootreview/旧执行worktree开发；读AGENTS要求五份project文档。

最小实现目标（全纯新增为主，避免改旧冻结方法/fingerprints）：
1. versioned SI-P3工程协议与数据/边界schema，绑定最终五family、背景S新固定hash规则、caps/guards；标ENGINEERING_ONLY/NO_LIVE。禁止机器路径或凭证进科学commit。
2. single-K1 source→preassignedprefix→exactreplay→stage1/2首动作→**同env原地P0suffix**完整生产collector核心与显式runtime ports；复用真实P0公共prompt/parser/schema/producer适配，typed mapping contract，不再出现dict/object或operation name分歧。接journal+unit registry+physical成本上限/输入tokens预留+GPUallocated×monotonic预算合同；all96slots/无效/早终止/NA标签/Q/oldsource续段引用只记一次。无需本阶段live driver，但生产collector核心必须有非空集成，不只写dataclass或全mock逻辑。
3. 完整pool→共同Q/去重→一次B/C matched adoption→paired slots/collator/exposure/guard审计。真实新data没有，构造明确synthetic非空多family正向/负向fixture经生产函数走完，model/env生成边界才fake；不能mock collector/parser/journal/registry/quality或把validator改成总pass。动作前公开input禁止future/诊断泄漏；EOS/cap/fullmap/invalid/earlytermination覆盖。
4. 仅新增P0 continuation训练合同/受gate保护的最小loader/controller：生产路径必须PeftModel.from_pretrained(base,既有P0,is_trainable=True)，同初始化/仅LoRA/freshoptimizer/final18/固定paired order，拒绝freshget_peft_model替代warm-start、best-checkpoint/extraepoch/drop-last/独立shuffle、输出覆盖。CPU小型合成PEFT roundtrip及实际collator可验证软件，**不得加载实际8B或执行真实训练**；如不实现真实训练driver请明示缺口，不称runtime ready。
5. pinned /home/lizening/miniconda3/envs/alfworld-self-improve/bin/python 软件focused/fullsuite（历史base85的3fail+77errors不修；必须无NEW IDs）；保存actualraw receipts、compile/diff、非空integration artifacts；可读取Luna最后交付但不要改她文件。tokenizer可本地精确缓存文本编码；不读取新task正文。

请先回报边界/分解并直接实现，不需等我批准routine可逆工程选择。新的确认性统计reporter不在本阶段，保留未来验收spec即可。必要依赖method若必须改旧共享方法，先给具体repro和最小diff请求scope裁定，不自扩。完成freeze clean精确commit、push自己科学branch非force/live ls-remote核验，提供diff+完整methods/bindings/测试证据+HANDOFF与有限未证项。你无独立验收/launch权限。provenance不commit/不push/不INDEX。目标交付可review的最小真实合同包，不设计第二研究方法/架构。
