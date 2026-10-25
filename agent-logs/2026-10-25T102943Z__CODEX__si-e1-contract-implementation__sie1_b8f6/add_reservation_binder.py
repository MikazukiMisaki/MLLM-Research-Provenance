from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
f=ROOT/'src/self_improvement/si_p3/reservations.py';assert not f.exists();f.write_text(r'''"""Pure offline binder for the exact SI-P3 design reservation bytes.

No task body, schedule file, launch argv, tokenizer, environment or model is
opened/constructed. A caller must supply all seed metadata explicitly.
Generic freeze_plan remains useful for synthetic software fixtures only.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

from recovery.corpus import task_family_from_id

from .contract import FAMILIES, SOURCE_QUOTAS, Slot, freeze_plan, require

RESERVATIONS_SHA256 = "6ce8a32a2345b59ecdef9c28c3a341e9c0801b8105f79895f9b2cb9545a4937e"


def bind_reservations(reservations_bytes: bytes, seed_metadata: Sequence[Mapping[str, Any]], *,
                      evidence_class: str = "historical", synthetic_expected_sha256: str | None = None) -> tuple[Slot, ...]:
    require(evidence_class in ("historical", "synthetic"), "reservation evidence class")
    require(type(reservations_bytes) is bytes, "original reservation bytes required")
    if evidence_class == "historical":
        require(synthetic_expected_sha256 is None, "historical reservation digest cannot be overridden")
        expected = RESERVATIONS_SHA256
    else:
        require(type(synthetic_expected_sha256) is str and len(synthetic_expected_sha256) == 64,
                "explicit synthetic reservation digest")
        expected = synthetic_expected_sha256
    require(hashlib.sha256(reservations_bytes).hexdigest() == expected, "frozen reservation raw-byte SHA256")
    value = json.loads(reservations_bytes)
    require(value["status"] == "ADOPTED_DESIGN_METADATA_ONLY_NOT_EXECUTABLE_NOT_AUTHORIZED" and
            value["no_schedule_indices_seeds_cutoffs_or_argv_per_identity"] is True, "metadata-only reservation boundary")
    rows = value["rows"]
    require(type(rows) is list and len({r["identity"] for r in rows}) == len(rows), "reservation unique canonical identities")
    source = [r for r in rows if r["partition"] == "acquisition_feasibility_96"]
    require(len(source) == 96 and all(r["family"] in FAMILIES and task_family_from_id(r["identity"]) == r["family"]
                                     for r in source), "reserved A96 family/identity shape")
    require(all(sum(r["family"] == f for r in source) == q for f, q in SOURCE_QUOTAS.items()), "reserved A96 quotas")
    require(all(set(r) == {"task_id", "family", "seed"} for r in seed_metadata), "caller must explicitly supply only identity/family/seed")
    expected_identities = {(r["identity"], r["family"]) for r in source}
    observed_identities = {(r["task_id"], r["family"]) for r in seed_metadata}
    require(len(seed_metadata) == 96 and observed_identities == expected_identities, "exact reserved A96 identity/family set; no D48/E600 substitution")
    return freeze_plan(seed_metadata)
''')
f=ROOT/'tests/test_si_p3_reservations.py';assert not f.exists();f.write_text(r'''"""Portable synthetic wire fixtures; real metadata checks live in the handoff evidence."""
import hashlib
import json
import pytest

from self_improvement.si_p3.contract import ContractError
from self_improvement.si_p3.reservations import bind_reservations
from si_p3_support import synthetic_plan


def fixture_bytes():
    plan=synthetic_plan()
    metadata=[{'task_id':s.task_id,'family':s.family,'seed':s.seed} for s in plan]
    rows=[{'identity':s.task_id,'family':s.family,'partition':'acquisition_feasibility_96'} for s in plan]
    dev={'identity':plan[0].family+'-synthetic-D48/trial-D48','family':plan[0].family,'partition':'engineering_development_train'}
    value={'status':'ADOPTED_DESIGN_METADATA_ONLY_NOT_EXECUTABLE_NOT_AUTHORIZED','no_schedule_indices_seeds_cutoffs_or_argv_per_identity':True,'rows':rows+[dev]}
    payload=json.dumps(value).encode()
    return payload,metadata,dev


def test_explicit_synthetic_reservation_binding_and_caller_seeds():
    payload,metadata,_=fixture_bytes()
    plan=bind_reservations(payload,metadata,evidence_class='synthetic',synthetic_expected_sha256=hashlib.sha256(payload).hexdigest())
    assert plan==synthetic_plan() and len(plan)==96


def test_same_family_D48_substitution_cannot_pass_same_quotas():
    payload,metadata,dev=fixture_bytes()
    metadata[0]=metadata[0]|{'task_id':dev['identity']}
    with pytest.raises(ContractError,match='exact reserved A96'):
        bind_reservations(payload,metadata,evidence_class='synthetic',synthetic_expected_sha256=hashlib.sha256(payload).hexdigest())


@pytest.mark.parametrize('attack',['hash_override','self_reported_hash','altered_bytes','missing_seed'])
def test_historical_expected_digest_is_frozen_not_self_reported(attack):
    payload,metadata,_=fixture_bytes()
    if attack=='missing_seed':
        metadata[0].pop('seed')
        with pytest.raises(ContractError,match='explicitly supply'):
            bind_reservations(payload,metadata,evidence_class='synthetic',synthetic_expected_sha256=hashlib.sha256(payload).hexdigest())
        return
    if attack=='self_reported_hash':
        obj=json.loads(payload);obj['sha256']=hashlib.sha256(payload).hexdigest();payload=json.dumps(obj).encode()
    if attack=='altered_bytes':payload+=b'\n'
    with pytest.raises(ContractError,match='cannot be overridden' if attack=='hash_override' else 'raw-byte SHA256'):
        bind_reservations(payload,metadata,synthetic_expected_sha256=hashlib.sha256(payload).hexdigest() if attack=='hash_override' else None)
''')
f=ROOT/'docs/si_p3_engineering_v1.md';s=f.read_text().replace('It supplies no task body, launch config or reserved real-task manifest.','`reservations.bind_reservations` first authenticates caller-supplied original reservation bytes against frozen SHA2566ce8a32a2345b59ecdef9c28c3a341e9c0801b8105f79895f9b2cb9545a4937e, verifies the exact A96 identity/family set against explicit caller seed metadata, then invokes the same freeze_plan. A quota-preserving D48/E600 substitution fails. Historical expected digest cannot be overridden or replaced by a header claim. The returned typed slots stay in memory; this package writes no real-task schedule/argv or task body. Synthetic fixtures use an explicitly separate digest branch.');f.write_text(s)
print('Added pure offline fixed-SHA A96 identity binding and six portable positive/negative software tests.')
