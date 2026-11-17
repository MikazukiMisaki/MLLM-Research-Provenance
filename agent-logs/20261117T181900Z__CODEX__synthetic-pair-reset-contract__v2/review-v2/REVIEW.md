# Synthetic reset contract v2: independent CPU review

This is a fictional one-pair interface candidate, not scientific execution or
permission to run. No real task, environment, model, tokenizer or GPU was
invoked. The exact original `_NativeResetCapture` source SHA256 is
`1c2df60c671ab408dfd5738192edd0371db848191a904c77e695dc250ff7b00e`;
its `won` list/tuple is serialized into `won_batch` list and `won_batch_type`
string. Original episode SHA256 is
`06922aed662e84c1366624600c361f64ca7fba1ee93daccf83ff8de7a174a21b`;
it forwards that dictionary in reset evidence and checks false.

Candidate `bridge.py` SHA256
`4979a93508a40cc467e7d5a52dd508121cfa4f9af1b2fbbe6f7fbb4c67dd81ff`;
`fake_arm.py` SHA256
`fb298e4185adec47ee20275aba07f210c890312329f3bce3431a7a80ea277206`;
`test_pair.py` SHA256
`cd94236396ce81cc97db6a1c2bb68706931330155a6c10ffa3d076c2a847cadd`.
The candidate enforces exactly the two expected fields, one genuine boolean
false in the list, and `list`/`tuple` as source-type labels.

Independent pinned-interpreter run of the seven author tests: **7 passed,
exit 0**. `test-output.log` SHA256
`89deaa759ce606291f54da5ad8eebffd8f84c99ef6bf55bcba14f3cee543e528`.
Separately, `replay.py` SHA256
`a44b7ec2b9e82d1039a0e073edc6c3bd5de45d668417d46d50c74be8ba1a8247`
replayed two allowed and four invalid fictional shapes. Its output SHA256 is
`b4a0d34248be3d7b96265e2b5b6f7e4a0df03f44c3009ce142298882f4774276`.

List and tuple origin claims completed both fictional arms. B's integer zero,
true, extra metadata or missing type stopped the owner before B model-load
reservation, retaining one setup, both reset reservations and returns, and
the A model-load reservation. Each ledger ended aborted and reused output
was refused. The author's seven-test run used twelve fictional setups and
the independent six-case replay used six more; these 18 test setups are not
scientific materializations.

The results verify only specified synthetic protocol cases. They do not
authenticate the child's reset claims, establish hidden-state equality,
connect the real actor or StageBudgetChannel, verify native success or bind
the scientific roster, global physical costs, GPU controls or process cleanup.
No remaining confirmed defect was found within this narrow reset-shape scope.
