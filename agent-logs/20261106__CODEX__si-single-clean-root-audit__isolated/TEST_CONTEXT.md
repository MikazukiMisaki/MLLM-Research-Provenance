# Independent fake-test invocation context

The first local `unittest` invocation omitted the documented `PLAN_BINDING` environment variable and therefore exited 1 with `KeyError: 'PLAN_BINDING'` in one of 14 tests. This was an invocation error, not evidence of a scientific or environment failure. No real subprocess, engine, model or GPU was invoked. The initial error was observed in the tool output, but no separate raw log was captured.

A subsequent invocation supplied the README-documented binding. Its raw output and exit status are saved separately in `independent_test.log` and `independent_exit.txt`; it exited 0. This passing fake suite does not imply real-worker acceptance. All code and tests remain the originally frozen bytes.
