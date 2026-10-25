# Luna SI-E1只读tokenizer/背景S/runtime审计任务

新的用户授权工程继续，阅读 /home/lizening/research-notes/agent-logs/2026-10-25T102943Z__SOL__si-e1-engineering-review__sie1_b8f6/COMMON_ENGINEERING_CONTRACT.md 及其权威前协议。OWN=/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__LUNA__si-e1-token-runtime-audit__sie1_b8f6；不改科学代码/tests/旧记录，不用developer worktree，不INDEX/provenancecommit/push。

允许**精确已缓存tokenizer本地文本编码/CPU collator检查**，不允许Qwen3-8B/P0模型加载/神经generate、实际训练、ALFWorld构造/reset/step、正式预检/supervisor、新task正文/结果、真实96采集/G4。原科学85/2da与provenance1962a074先核验，模型/tokenizer/adapter/config/data输入文件hash/包依赖只读。不能因本任务名runtime认作release。

1. 独立用common固定hash规则从原balanced expert dataset（路径/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/sft-policy-bootstrap/sft_expert_dataset_balanced.jsonl；expectedSHA c547e8f0...）及known-use expert_train身份冻结S120 compact manifest。每选task身份hash/rowstep+prompt/target/map hashes/labelbareID/actualtoken lengths/quality provenance，不写完整prompt/训练row/token IDs进provenance；完整本地审计量若必要local-only+size/hash。每task一row，数量44/32/20/11/13，确认与new96/dev48/eval600零task交叉。不能为fit或hash修旧数据、读取新任务或偷偷替换已选task。
2. 本地精确cached snapshot b968826d9c46dd6066d109eabc6255188de91218 与实际P0 final_adapter tokenizer分别hash/加载tokenizer ONLY（offline local_files_only、清除Python路径污染，禁止下载）。核对chat_template enable_thinking=False、renderedP0 public输入、ID+EOS、prompt-prefix匹配、2048no-truncation、真实labels≠−100及causal shift数。用实际production helper/installed collator验证CPU tensors：padding0attention, prompt/pad mask、PAD==EOS时真实EOS保留target；负向过长/截断/malformed，仅software。若snapshot vsadapter tokenizer有差异，给byte/encoding证据，不选择有利口径。
3. generation、training监督tokens、nonpad输入、padded slots分账；明确S120真实量能观测、futureB/C新pool量NOT_OBSERVED，不写成已完成两臂曝光PASS。记录tokenizer load次数、编码row数、CPUtoy/collator调用数，实际模型/环境/训练0。
4. 只读准备可执行性矩阵：依赖版本/缓存origins、拟议16Minput/4device-hour如何据实际allocatedGPU数量×monotonic计账（不是wall=GPU）、source8496/9792budget无额外replay。没有真实newruntime/8B加载/环境调用，绝不可claim actualruntime/preflight ready。只给未闭合证据和明确条件，不建gate/argv/科学schedule。

所有命令由subprocess真实capture/log/receipt，不手写stdout/exit；路径用Path actual.exists+sha序列化，别漏agent-logs；input before/afterhash。交付S_BACKGROUND_MANIFEST.json（compact非dataset）、TOKENIZER_MASK_AUDIT.md/json、READ_ONLY_READINESS.md、raw receipts/commands、inputbindings、RECORD及hash清单；异常STOP对应依赖并继续独立只读工作，不修科学源码/数据。冻结后返回具体原始证据，不自行PASS新实现/放行。
