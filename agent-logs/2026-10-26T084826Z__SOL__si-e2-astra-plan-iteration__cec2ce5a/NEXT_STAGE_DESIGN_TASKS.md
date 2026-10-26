# SI-P3 下一步设计交接：无运行授权

共同起点：工程SHA `844cc4b78df1f83e29391ffd5ab861a2d0c0a3fd`；冻结v1原件不改；当前采集/训练/评估NO_GO。先读同目录COORDINATOR_DECISION.md及Astra最终方案；保留所有原始现场。用户持续授权Sol Research、Luna与协调方分工，本交接仅延续设计和只读证据范围。

## Sol Research：版本化v2协议草案与静态影响分析

1. 仅新增自己唯一provenance目录的文档。以固定全96 d5、source-first及确定性futility作为候选；不覆盖v1、不生成可执行schedule/gate/argv、不修改科学源码或测试。
2. 明确E保守上界、d步后的snapshot与parser-stop边界，Y0与YT语义、unknown/technical/budget/structural STOP的区别；source96完整后才判断，teacher未测保持NA。完整上界、家族配额、共同Q、B_pool包含C、一次抽样和禁止top-up照原条件保留。此处是候选池包含关系；实际B24不必也不能在至少8neutral条件下包含全部C24，须如实报告B与C抽样交集。
3. 静态列出实际采集驱动、journal、evidence auditor、seed/counter/reset/replay需要变动的方法/事件和必要负向测试。当前逐slot synthetic collector不是live driver；设计如何先source96后branch，不能以全局reset顺序碰运气。只提范围，不实现、不测试。
4. 独立核对9,216/9,792/149,760完整帽与source-only4,800生成帽，16M输入/4device-hours不可承诺完成。单列C24/家族失败数量的未证明风险，不能通过降C、扩大N、额外selector或改变teacher来“修复”。
5. 写出研究归因：C-A是追加训练包，C-B是共同背景/匹配配方下的failure筛选差异；固定早期干预动作蒸馏不是adaptive stopping。区分RECIPE_CONSTRUCTIBLE和learning efficacy。
6. 返回草案SHA、静态证据、分歧/风险和RECORD；开发/采集/训练/评价均未放行。不要修改或stage共享INDEX/清单；交协调方统一发布。没有独立验收或launch权。

## Luna：队列可比性、预算与执行能力证据准备

1. 只读取已有登记/manifest/hash证据，不打开未使用task正文、不重新查询GPU/CUDA/模型/环境，不再SSH或重跑任何旧授权命令。
2. 用已有identity/hash清单说明旧127与新96的任务隔离、家族差异，以及旧127与S120/历史训练使用重合能否查清；只报告可证明的交集与unknown，不能把旧6/120失败率外推新96。不能修改分区或按旧结果另选新任务。
3. 从已有证据指出可信宿主/NVML到容器PID身份映射还缺什么、可使用哪条已存在且已认证的入口；若无新增能力就明确BLOCKED，不重复失败探针、不放宽guard、不索要或导出密钥。只给能力需求/静态方案。
4. 为待审v2写不可执行预算/停止说明，区分source-only、完整采集、工程CUDA成本、历史科学5142/7949、未来训练/评估；固定新输出identity仅作命名建议，不创建run/output/gate/clearance。
5. 返回独立目录RECORD及hash。不要修改/stage共享INDEX/inventory，协调方统一发布。无preflight、launcher、模型、环境、采集、训练、G4或评价执行。

## 验收与协调

只接受可核对的文档/静态结果，未运行项保持NOT_RUN/NOT_PROVEN。任何已存在证据不足均标unknown，不用合成数据填真实结论。协调方收齐后独立审查并与Astra收敛唯一候选；这不构成下一阶段运行授权。若该配方投入不值得，可以结束这条小剂量路线，不为获得正结果扩大范围。
