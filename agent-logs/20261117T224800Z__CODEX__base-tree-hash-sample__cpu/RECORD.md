# Single base-tree hash sample

The original local CPU-only measurement reads the 12-file base tree once and applies the production tree digest serialization. Result reports matched SHA, logical bytes and wall/CPU time; this is one cache/shared-filesystem observation, not physical I/O or a throughput guarantee. No model, GPU or environment was called. The original path-bearing measurement script remains private; its SHA256 is `761cf9f628068adc968cc77718f04e0d89e43b91b91b1586d52a930f8256b259`.
