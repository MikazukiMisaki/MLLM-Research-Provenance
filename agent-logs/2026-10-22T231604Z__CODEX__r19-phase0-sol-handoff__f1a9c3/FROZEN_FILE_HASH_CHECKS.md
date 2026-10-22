# Direct frozen-file hash check — Phase0

Read-only SHA-256 results for the pinned local Qwen3-8B snapshot at `/home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218`. Hashing read bytes only; no model deserialization, tokenizer loading, or inference occurred. Every observed digest matches the corresponding file entry in `configs/experiments/r19_b1_baseline_manifest.json` and the retained model identity manifest.

| File | Observed SHA256 | Check |
|---|---|---|
| `model-00001-of-00005.safetensors` | `31d6a825ae35f11fb85b195b4c42c146c051e446433125a215336abdf95cbf5f` | MATCH |
| `model-00002-of-00005.safetensors` | `5991236cea6fe21f3d43cab0f0e84448734fbbe0789816202989f2ddc9d18282` | MATCH |
| `model-00003-of-00005.safetensors` | `c5185c4794be2d8a9784d5753c9922db38df478ce11f9ed0b415b7304d896836` | MATCH |
| `model-00004-of-00005.safetensors` | `b5ee7de71fbf17db3d5704e0c8f2bc7d005ca9e1d7ca2aeb19827b0cfcaa917a` | MATCH |
| `model-00005-of-00005.safetensors` | `20c2d6366ab85c90786ccdd829cd2b9e7d30ef3b2ebbb998280e7e4014b542ff` | MATCH |
| `config.json` | `f7c4eadfbbf522470667b797a3c89be2524832d2d599797248dc304fff447c30` | MATCH |
| `generation_config.json` | `2325da0f15bb848e018c5ae071b7943332e9f871d6b60e2ed22ca97d4cb993d2` | MATCH |
| `model.safetensors.index.json` | `f9fdbcb91c23971c13ec5d5f2573d2349e8f61f2f049371ec699281748fdb1bc` | MATCH |
| `tokenizer.json` | `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4` | MATCH |
| `tokenizer_config.json` | `d5d09f07b48c3086c508b30d1c9114bd1189145b74e982a265350c923acd8101` | MATCH |
| `vocab.json` | `ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910` | MATCH |
| `merges.txt` | `8831e4f1a044471340f7c0a83d7bd71306a5b867e95fd870f74d0c5308a904d5` | MATCH |

The SFT adapter directory was also streamed read-only using the repository's documented `directory_sha256` implementation (sorted relative paths plus file contents): 11 files, directory SHA256 `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11`, MATCH against the frozen baseline.

Other directly re-hashed frozen inputs: baseline manifest `d503f35ae913b137dfff091263bf29c38aa0ade2eea648dc45d7e6cf80da0973`; G2 amendment `f8a138045cde125f2c5e08a7d077f75e3838cc7f6d0c67703faffe1166099e49`; protocol `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122`; source schedule `0be460359fe43193e73f8cb55a8fb19fdba02ea70e3d0809ec5978fad21c8948`; exclusion manifest `70447bba1b2a944d52ab9b4041b2d6ff3d865f4f0abd55d655214c8060ff5367`; G3 authorization `89b887518c85d22d3176af0b50fb1861b58fb1c3b13a4ecc2b76485a66529b31`; entrypoint-repair authorization `026eb1f0b05bcc27a6c901c10d787110cbac0e329551051973dda93e907bdc71`; source-contract restart authorization `de634ba310e47d3d49838b8a73d9c6d87f7db87deed042311e3718061a7eb428`; source-contract repair amendment `62ff158f5739859266664b1db2e323dca6ea0ad3b8e84134ecbe5fd06c847372`; append-only resolution JSONL `58783ba60b076ee190dccb0875aac65891d7e1c811e00fbe6303ca65896369d9`; ALFWorld local config `e90f93eb4604a473b6eb4a259a19ef1ca3c296bba1771ba70a1c9b0edbc99700`.

These are host-local verification artifacts. No weights, adapter payload, tokenizer payload, data, cache, or credentials are copied into provenance.
