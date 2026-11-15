# Recovery handoff counterfactual: CPU review package

This local package contains eight hand-authored fictional scenarios and saved model responses from the mainline subgoal intervention. It is a data-and-calculation review aid, not evidence of an ALFWorld rollout, real task success, an authenticated model identity, or another-machine replication. No protected task or direction-2 restricted window material is included. This README does not authorize external distribution; review sharing separately.

`pairs.json` contains only the fictional paired prompts, four-option mappings, intended actions, recorded decoded IDs, generated token suffixes, and declared EOS IDs, plus source-log hashes. It intentionally excludes model/configuration paths and GPU identifiers. The original input-token prefixes and full logits are not included. Source hashes identify recorded bytes but do not establish provenance or physical execution; the export and original logs were prepared by the same operator.

From this directory, using the standard library (the documented local run used Python 3.13.13):

```sh
python -S -B recompute.py pairs.json
```

The program checks the eight planned keys, paired prompt differences, action mappings and saved EOS suffixes, then recomputes the observed action transitions. Expected: 8 valid pairs; baseline selects `take_second` 8 times; the injected-subgoal condition selects `undo_first` 7 times and `take_second` once; seven changes; each injected target ID appears twice. It trusts the stored decoded ID and cannot independently tokenize prompts, verify the meaning of each fictional task, authenticate the original run or prove environment effects. It requires no network, GPU or model, and does not read protected-task data.
