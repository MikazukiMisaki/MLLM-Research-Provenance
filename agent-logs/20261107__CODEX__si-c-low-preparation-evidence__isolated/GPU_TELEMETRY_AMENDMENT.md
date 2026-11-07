# Shared GPU telemetry amendment for the exploratory C-low attempt

This is a prospective amendment for one possible C-low continuation, written
after preflight and before any live launch. It supersedes the revision-2
proposal only where stated below. No training result or clearance is implied.

The originally proposed telemetry included bus-ID binding and periodic
device-wide free/used memory, temperature, power and utilization. The current
reviewed approach binds the device by its complete GPU UUID in both the
authorization and every admission/runtime observation. The admission samples
free memory and utilization. The proposed live guardian samples device-wide
free memory, verifies the returned UUID and stops when telemetry fails or free
memory is below 2 GiB for three consecutive checks. Its target query-start
interval is four seconds, and it stops when the recorded sample gap exceeds
five seconds. Monitoring can detect a gap only afterwards; delays, unobserved
spikes and physical tails remain UNKNOWN.

For this exploratory attempt, do not require live periodic bus ID, device-wide
used memory, temperature, power or utilization telemetry as a launch
prerequisite. UUID, not the PCI bus location, is the bound device identity.
The missing quantities and energy consumption are UNKNOWN, not zero, and
cannot be used for later attribution, a power-budget claim, or a comparison of
GPU efficiency. Device-wide free memory is a shared-resource observation, not a
measure of this process's usage or exclusive access. The retained free-memory
and telemetry-loss stops do not protect against every thermal, power, hardware,
or shared-load event. If the resource guard or telemetry reports an error,
stop the attempt and retain incomplete evidence.

Unchanged requirements include the recent one-minute admission thresholds,
one live attempt without retry, the 1,800-second outer timeout, the historical
inner GPU allocator policy and its recorded checks, startup storage floor,
sampled storage stop, exact input/preflight/clearance bindings and independent
review. The original worker checks and records PyTorch allocator statistics at
its own checkpoints; those checks are not continuous external monitoring.
No claim of a hard physical-I/O cap, exclusive GPU allocation, continuous
monitoring or complete descendant cleanup follows from this amendment.
