# SI-P0 Luna补充：未来任务identity可用性元数据盘点
用户授权的只读审计与设计，继承LUNA_TASK全部禁止边界；非新heldout授权，禁止读取未消费任务outcome/轨迹正文，不运行任何模型/环境/项目程序。首轮补充≤15分钟，提前完成即返回；无法闭合就INDETERMINATE，不无限扩查。
目录仍为你自有 /home/lizening/research-notes/agent-logs/2026-10-25T054106Z__LUNA__sft-raw-evidence-audit__b1c48c；不得改任何已冻结文件，新增AVAILABLE_IDENTITY_AUDIT.md/.json与独立hash清单/receipt。不要动旧FILE_HASHES、sharedINDEX，不commit/push。
目的：仅元数据判断现有split是否存在可用于未来独立验证的候选identity，不能用134-60直接当可用数。
允许：只读installed json_2.1.1/train、valid_seen、valid_unseen目录名（task/trial名，不读未来traj_data/game/outcome）；读取已消费的原schedule、accepted dataset task索引、exclusions、已有R4/R12/R14/R16–R19 identities与历史有效评估清单，按canonical task/trial去重。不要为了扫全局而读取未运行任务内容。若全局消费登记不全，明确“已知集合差集候选，污染状态未证实”，不得宣称干净heldout。
输出：每split目录身份数；已知用于专家training/validation、online-dev、recovery-dev、heldout已消费/已看outcome的交集及来源hash；已知未消费候选差集的count与仅ID/hash（不带任何新outcome）；canonical规范、无法闭合历史使用范围、未来评估只能在独立冻结协议中决定。不要修改exclusions或生成可运行schedule/argv。
原已消耗60 valid_unseen及140 valid_seen必须保留为used，不能重新称新heldout。R19 TRAIN127与其36prefix是不同层级，用同episode计一次。本补充不为任何新采集/训练/评估赋许可、不派其他agent、不据候选数承诺power。
