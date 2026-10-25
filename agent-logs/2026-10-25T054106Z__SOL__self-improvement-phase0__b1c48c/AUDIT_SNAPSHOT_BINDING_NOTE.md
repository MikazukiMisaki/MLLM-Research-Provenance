# Independent audit snapshot identities
The final independent_historical_rescue_verification.json SHA bf3503774a81abfeb1dc11343f677dafccefabcae78fe38607b815b82f5f437a binds the frozen developer inventory 1b0b7766d5901894d71f635433b9055223648d07bf5bda4e648c1129403cd8c0. Sol Research cites exactly this path/hash in its final addendum. The earlier mutable-inventory snapshot (a40ebc6f...) remains with first_snapshot suffix; both independently verified the same 31 raw rescue references/outcomes.

During local packaging, a draft script incorrectly assumed the peer cited the earlier snapshot and renamed the files. Its hash assertion returned exit1 before any document edits. Inspection showed the peer had correctly cited the final inventory-bound result; the renames were reversed immediately and bf350377... was verified at its cited filename. Neither bytes of these results nor peer documents nor scientific raw evidence changed. This was a corrected packaging assumption, not a scientific failure or rerun.

Do not rerun historical scripts into a frozen task directory. The original/script/log/receipt evidence and first snapshot are all preserved.
