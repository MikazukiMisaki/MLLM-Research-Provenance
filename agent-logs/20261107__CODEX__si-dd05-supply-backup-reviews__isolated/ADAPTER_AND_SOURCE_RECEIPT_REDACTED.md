> Redacted publication copy: owner-private Drive object identifiers removed. Original SHA-256: `8b71fb71c679bf257d2540862c1052207cd17edeacd39302b800815e7a6b4442`.

# Private C-low source and adapter backup receipt

The frozen production source snapshot for local commit `9bbaa12c2d8177a60ec5a74ed2f970ef29a57bce` was backed up as the original Git tree archive, not a Git history bundle. Drive file ID `[OWNER_PRIVATE_ID_REDACTED]`; 13,198,060 bytes; downloaded SHA-256 `818fbacba5c437be77fc267da288a2a6508c196778726b99a7d8da3fe040038e`, matching local. The source was not established to exist on a remote Git ref.

The original final adapter has tree SHA-256 `1cc6c153138e58ca1bda44c0682757d68649c11190258854e7ee2454df816669`. The three original files were packaged in an uncompressed deterministic tar: `README.md` SHA-256 `78d8b8d68dbab5ccb4c470d0d3eaa2ff313321f42ba8c9d0c826bf9c8fdc9a42`, `adapter_config.json` SHA-256 `955ef287f8f6bf9f0eece48d58b79c572f8ee9746e54b8a648a47e7614614ae8`, `adapter_model.safetensors` SHA-256 `cf30d97663c48c1d77a534443cd43f5f3dea3bb9912c742a4ebcc9718e3ffc3f`. Tar metadata was normalized while file bytes were preserved. The complete tar is 349,255,680 bytes, SHA-256 `bca919093e9b7b62ba5e30824bce435b30595f2902b025ae2e4b43b567d42c63`.

A single-upload 100 MiB connector limit required splitting the tar into four ordered segments. Each was uploaded to the owner-private folder ID `[OWNER_PRIVATE_ID_REDACTED]`, and each was downloaded and hashed. Concatenating all four downloaded segments in order yielded the exact complete tar hash above. Drive metadata reported `shared=false` and only the owner for the folder and all four segments.

| Order | Drive file ID | Bytes | Downloaded SHA-256 |
| --- | --- | ---: | --- |
| 00 | `[OWNER_PRIVATE_ID_REDACTED]` | 94,371,840 | `bb8deff73436db8f2e28e102b51277463c2808d0db67e517775aaaf8d945cb27` |
| 01 | `[OWNER_PRIVATE_ID_REDACTED]` | 94,371,840 | `08dadd059a13df89901e416d54046ceb6a7bcf3541ae656b01bab1e6288f0818` |
| 02 | `[OWNER_PRIVATE_ID_REDACTED]` | 94,371,840 | `8666aaaeb88d152870b96aea072f82423da0b899bdf6bec18aa21d06d2c3d448` |
| 03 | `[OWNER_PRIVATE_ID_REDACTED]` | 66,140,160 | `ecf7f625ddde0c176aedf685789b351053444985ab4932c994a074f965ebf999` |

This preserves the actual trained adapter, but does not change the `INNER_COMPLETED_OUTER_UNKNOWN_NO_RETRY` classification, establish future availability of the base model/dependencies, or establish success-rate improvement. Private source and model material must retain owner-only access.
