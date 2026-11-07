# Independent review: verified-source split entries

The prepare-only entry SHA256 `46d9bd47a504f015ca1cf1750edeb65d2daa340d22f15deff983ed89718bd78a` differs from independently reviewed base `a6f11fcabf134cb6ce27dba5f242ef9e5c267a4c6ecc816a31c774522f204f79` only by enabling PREPARE. The dispatch-only entry SHA256 `e46c002923435f5309cba39a12fe0f312e86e81a0f7e7699e50017bd84316067` differs only by enabling DISPATCH. The other stage remains disabled in each copy.

Three fake-only tests independently passed (raw log SHA256 `6cea88752b3e58ae5cee56ff3b1b13eab34117918d6bad9661194c031e2dc157`): exact one-flag comparisons and wrong-stage CLI rejection using nonexistent fake paths. No real preparation, dispatch, GPU, model, environment or training was invoked by this review.

Within prior reviewed limitations, this supports consideration of a single separately authorized model-free preparation that creates only a private binding/review package using fresh, genuine gate inputs and admission. The package must be independently read, revalidated and associated with a separately authenticated external review/pin before any live dispatch. This is not a claim that real preparation occurred, not a live-launch clearance, and not scientific evidence; process isolation, standard-library/scientific dependencies and resource tails remain subject to previously recorded limits.
