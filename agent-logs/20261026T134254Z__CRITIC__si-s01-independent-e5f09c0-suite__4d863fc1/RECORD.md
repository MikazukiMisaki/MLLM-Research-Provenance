# Independent exact e5f09c0 full-suite software evidence

This capture binds only immutable Git commit e5f09c05824cb61cb35ccbbf4e189b04e8829cea. Developer final handoff was pending when this independent run was requested; adoption requires an identical final SHA. This is not experiment launch clearance.

The checkout is /tmp/si-s01-independent-e5f09c0-4d863fc1-7nai5h78/checkout. It is a separate detached local clone containing pinned d7 Git objects for parity tests. The runner bytes match the sealed d7 runner, and the base844 environment-contract bytes match. Invocation is not byte-identical: this run adds -B and redirects test evidence/cache/temp outputs outside the checkout.

Collect/full each ran exactly once. Counts and historical ID, phase, outcome, exception-type, prior-pass and skip comparisons are retained in COMPARISON_SUMMARY.json and COMPARISON_*.json. Historical 3 failed calls and77 setup errors were not repaired or omitted. No matching exception-key claim implies identical messages or underlying causes.

The suite contains existing real tiny CPU model/PEFT and training fixtures; it must not be described as creating zero model objects. Real Qwen3-8B/CUDA/ALFWorld/SSH/production preflight/science are outside scope.

The Git diff contains19 total files, of which18 arePython and1Markdown. All18 Python files were compiled once to explicit external bytecode destinations. Git diff --check was run once. Post-checkout status and all tracked-file pre/post byte hashes are retained. See summary for actual results, including any cache paths.

Cache placement deviation: despite main -I -B and external cache/temp controls, existing isolated subprocesses wrote10 ignored __pycache__ directories inside the private /tmp checkout. These untracked bytecode caches were moved to the external /tmp directory after capture, with file bytes verified unchanged. No tests were rerun. This restores an empty checkout cache set but does not establish that cache files were never transiently written into the checkout. See CACHE_PLACEMENT_DEVIATION.json.

Path-order diagnostic: script imports and pytest reorder/duplicate sys.path entries, so the diagnostic expecting the initial literal src/tests/root first-three order is false. The observed first-three order normalized to checkout matches both base844 and d7 at all four captures. All six captured project-module origins are inside the exact candidate checkout. Raw origins were preserved.
