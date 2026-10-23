# R19-B1 G3 raw evidence bundle

Verify the bundle using `sha256sum r19_g3_complete_evidence.tar.gz` and the value in `archive_manifest.json`. List members using `tar -tzf r19_g3_complete_evidence.tar.gz`; restore the bundle with `tar -xzf r19_g3_complete_evidence.tar.gz`.

`archive_member_inventory.json` gives the exact original byte length and SHA-256 of every regular file included. `source_sha256.before.txt` and `source_sha256.after.txt` preserve identical pre/post source inventories. The independent member-by-member check confirmed all 15 members match their original local files.

This package is a lossless archive of the completed authorized G3 output and supervisor record. It is not a G4 report or statistical analysis.
