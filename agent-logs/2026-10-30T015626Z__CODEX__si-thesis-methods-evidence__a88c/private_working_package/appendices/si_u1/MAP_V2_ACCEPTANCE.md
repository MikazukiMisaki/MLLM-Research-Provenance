# SI-U1 附录证据地图 V2 验收

结论：`ACCEPT_MAP_V2_WITH_ORIGINAL_APPENDIX_AS_SCOPED_WORKING_BUNDLE`。

地图 V2 `/home/lizening/research-notes/agent-logs/2026-10-30T070200Z__SOL__si-u1-repro-map-v2__8be2/EVIDENCE_MAP_V2.md` SHA `3652dd509396809e71d8c4e26b599b44fb829a981e257e010ea96dd8404504d2` 已核对。

与原地图完整 diff 只有两项：补正 decoder RECORD 的 SHA；把新 checker/JSON 的“本目录”改为其真实原始目录绝对路径。从原文应用这两项替换得到 V2 完全相同字节，没有新增科学主张。地图中 15 个明确绝对路径/摘要对现全部匹配。指向原目录的 APPENDIX_LOCAL_CHECK.json、check_appendix_inputs.py 均存在且哈希与先前审阅不变。

原附录 exact SHA `7fd0db41d8223e70dfca0f9e45f68d4214e97458edc457b7c60c3e7470aab592` 不变；原地图、checker、结果 JSON 和原 FILE_HASHES 清单也均保持原先字节。因此现在接受的组合是“原附录正文＋新 V2 证据地图”，不是原错误地图已被改写，也不把原 FILE_HASHES 说成已覆盖新 V2。整合时应显式携带这个新地图版本或将其路径/摘要写入整合清单。

先前 INDEPENDENT_REVIEW.md 所述配套摘要错误已关闭；修复时点、普遍盲态不可证明、当前文件核验与历史过程的区别、远端元数据限制及成本口径建议均继续适用。不存在完整重跑或新样本独立性通过的结论。此次仅作文档与哈希核对，未执行 checker、模型、环境或科学分析。
