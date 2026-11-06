# Independent arithmetic review of training contract

Scope: independently check the algebra in TRAINING_SEMANTICS_SPEC_V1, SHA256 2969f9c1812babbd8488d8c10246cc99cbe295d36ec4e266daacb763c2d977fa, using invented rational numbers only. No model, ALFWorld environment, tokenizer, training data or GPU was used.

For every M from 1 through 12 and K from 0 through M, an exact Fraction calculation checks that the proposed alpha=M/(M+3K), with target weight 4alpha and other weight alpha, has dataset sample mean one. When K=0 or K=M, the sole present weight is one. In three-example windows with active-token counts 1,2,4 and all eight target/non-target patterns, it checks that the sum of the proposed scaled native-mean contributions equals an independent weighted token sum divided by unweighted update tokens. Output is result.txt.

This checks the finite examples and algebraic identity, not data authenticity, actual model mean-loss implementation, gradient dynamics, batch/distributed behavior, trainability, resource limits or scientific effects. It does not decide whether sample normalization is optimal. The test does not establish real input availability. M,K in this note are hypothetical, not real dataset counts.
