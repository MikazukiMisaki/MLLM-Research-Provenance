# Literature matrix clarification: training budgets and mixed trajectories

This additive note qualifies two entries in the previously published `RELATED_WORK_MATRIX.md` under `2026-10-30T010000Z__CODEX__si-stage-two-followup__76d9`; the earlier record remains unchanged.

Zhang et al., [Agent Learning via Early Experience](https://arxiv.org/html/2510.08558v3), describe a matched step budget in the main comparison. Appendix B.2 states that optimizer updates are matched for IWM and imitation learning, while it specifies matched epochs for SR. The wording in the earlier matrix can be read as independently establishing identical optimizer-update counts for every method. That stronger claim is not supported by the checked appendix; treat it as an author-reported main-text budget comparison with these distinctions, and do not infer equal data collection, tokens or total compute.

Lauffer et al., [Imitation Learning for Multi-turn LM Agents via On-policy Expert Corrections](https://arxiv.org/html/2512.14895v1), compare several construction strategies with success and repetition filtering. The inspected comparison includes additional expert data for the 7B groups; the 32B OEC curve mixes expert and corrected data and its endpoint changes the problem distribution. Do not portray the work as a pure source-only causal comparison, or matched total compute.

These clarifications do not change project outcomes or authorize any experiment. Independent reviews of the source text and introduction revisions are separately recorded.
