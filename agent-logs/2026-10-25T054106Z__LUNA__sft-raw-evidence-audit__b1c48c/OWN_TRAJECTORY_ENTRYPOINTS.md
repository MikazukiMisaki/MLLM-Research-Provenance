# 已有自身轨迹 / 恢复原件入口（只定位）

用途：供协调方后续判断“已有 agent 自身经验是否包含可验证增量”。本表只是文件入口盘点，没有筛选/重标学习样本、读取 held-out 未运行任务 outcome，或更改 R19/G3/G4 原件。路径在本地机器；JSON 中对应已观察文件的 size/SHA 见 `raw_artifact_inventory.json`。

| 原件 | 用途/边界 |
|---|---|
| `/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/sft-recovery-source-pool-r1-20260908T042933Z/trajectories.jsonl` | SFT actor source-pool 的原始 episode 入口；SHA `8a23c081e06d2f741fba9a5e0f7c3f15c7f73a696b74173748399f3785c6c59f`。不代表这些样本具有独立增益。 |
| `/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/persistent-recovery-source-pool-r7-20260909T000000Z/trajectories.jsonl` | 后续 actor source-pool 原始 episodes；SHA `780603bf96fc5ae5abdd4f588f76c7187dd191feabdb9a230e1e1c9c78eddac8`。 |
| `/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/sft-recovery-replay-continue-r3-20260908T055308Z/continue_branches.jsonl` | R3 paired continuation branches；SHA `eba101c0e8d6a894879548dc79aa93042d2a5e11b4659277fc1a5c3dd1bf0c13`。 |
| `/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/persistent-recovery-replay-continue-r9-20260909T033000Z/continue_branches.jsonl` | R9 paired continuation branches；SHA `b04ea7cbea1ddd5818a2875e6a806b468e6db03afed09cfeaa792f8a05af2e99`。 |
| `/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/source_trajectories.jsonl` | 唯一授权的 R19 G3 run `260422ac02bd42a8b2929d7ef240526b` source actor trajectories；campaign 原件，不在 SI-P0 重解读。 |
| `/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/branches.jsonl` | 同一 R19 run recovery branches；不得脱离 source/registry/events 单独视为独立训练案例。 |
| `/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/execution_events.jsonl` | 同一 R19 run 原始 event ledger，保持原件不变。 |
| `/home/lizening/research-notes/agent-logs/2026-10-23T024938Z__LUNA__r19-g3-raw-upload__2da980f/archive_manifest.json` | R19 原始证据上传 manifest，指向完整原始 G3 evidence archive；用于完整性与内容范围核对。 |

R19 物理成本仍按已独立核准的 `5,142 generations / 7,949 environment operations (resets included)` 报告；原始前驱 `177 / 342` 保留。这里没有从这些入口增加或推导新 episode 成本。它们未来若用于设计，必须同时看完整 paired counterfactual、任务身份重复、分支来源、成本、泄漏 exclusions 与 outcome 是否被用于既有设计；不能把“policy 生成过”或“轨迹成功”直接等同于“agent 从自身经验学习后改进”。
