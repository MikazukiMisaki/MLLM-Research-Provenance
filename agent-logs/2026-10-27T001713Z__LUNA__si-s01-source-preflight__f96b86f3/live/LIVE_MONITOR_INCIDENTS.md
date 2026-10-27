# Live-run monitoring notes

The following were operator-side read-only monitoring mistakes, not production-run failures. They did not alter the source run, outputs, or schedule.

1. An initial path check omitted the random `_oxwwsyg4` suffix from `handoff.storage.output` and reported the wrong path absent. The exact handoff path was then used; the original path and open files were present. No signal, stop, or repair was issued. The mistaken alarm and correction were reported to Root.
2. One follow-up query omitted `agent-logs/` from the readiness-record path and returned `FileNotFoundError`. It did not start or affect any process; subsequent checks used the exact handoff path.

All subsequent live monitoring derives the output path mechanically from `SOURCE_EXECUTION_HANDOFF.json`. The actual run remained on the originally authorized supervisor/worker pair and completed normally.
