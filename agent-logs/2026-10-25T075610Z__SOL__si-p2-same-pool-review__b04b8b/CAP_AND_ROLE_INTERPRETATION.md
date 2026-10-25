# SI-P2 共同规则解释：cap与完整性、身份审计与目标质量

协调方在同行交付冻结前的独立原件核对；不修改事前anchor、采纳条件或科学源码/原始证据。

## token cap标志不是截断结论

实际case `R19_K1:R19-random-control-47bcdcad9c56a38ac146`（原branch行39）：CONTINUE=1、K1=1。原Stage1 event `0298b176cd2ecde03292a043a54f9e771f3f95f29073a0f71d49bc989259dd76` 的status=valid、output_complete=true、token_cap_reached=true、generated_tokens=max_new_tokens=40；raw输出SHA256=`7fc2232e4a1cc7cf35d3897c391fe16ab8b4edef4c5004b96e5a0c774fd199c2`。第一Stage2 event `760cd1fed1648e86389223beca3421be35f575d995675a1c25f675b7493f608f` 为selected、complete=true、cap=false、generated_tokens=5/16，原动作确实执行。

冻结源码 `scripts/run_r19_experiment.py:1355–1356` 明确以达到cap且末token为EOS时仍complete=true；`src/recovery/two_stage.py:295–306` 的Stage1 parser只因output_complete=false判truncated_stage_one。达到上限并在上限处EOS，与被截断不同。当前不加载tokenizer或重新parse；只核对已有flags和冻结生产契约。

共同质量原意是Stage1合法、第一Stage2完整未截断；不能新增“任何cap=true即排除”。该neutral-success不应仅因Stage1 cap=true被标STAGE1_TRUNCATED。若有其他独立不合格证据可据原件列出。本解释同等适用于所有行，不为了保留C；本case并非rescue。不会改变旧G3/validator/成功标签，也不追认新科学运行。

## Luna的角色范围

Luna任务要求独立parent身份/标签、**过滤前**固定anchor计划和预算，不要求在缺少完整source定位时独立完成Sol的质量核验。仅凭branch摘要无法重构公共字段时应记“此次locator审计未闭合”，不能据此把原数据裁定为Q_hist失败，也不能将这种受限mask当共同质量后的容量。

共同质量最终mask由Sol Research完整source/replay审计与协调方独立原件检查交叉决定，再接入Luna的独立parent索引。Luna不需为此扩查、补source或重跑任何旧审计；若初稿已经把81/90等局部核对数称最终Q_hist，需保留原字节并以addendum限定其scope。

本记录只是消除既有字段语义和分工误解，不改变171行范围、quality/dedup/anchor顺序或任何科学授权。当前新科学调用0。
