from pathlib import Path
import json,hashlib
from self_improvement.si_p3.runtime_gate import file_hash
from self_improvement.si_p3.runtime_environment import historical_replay
from self_improvement.si_p3.contract import digest
OWN=Path(__file__).resolve().parent
assert OWN.name=="2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82"
root=Path("/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z")
trajectory=root/"source_trajectories.jsonl";events=root/"execution_events.jsonl"
before={str(p):file_hash(p) for p in (trajectory,events)}
with trajectory.open("rb") as f:first=f.readline()
row=json.loads(first);refs=row["metadata"]["r19_source_event_refs"]
needed={refs["source_episode_event_id"],refs["reset_event_id"],*refs["transition_event_ids"]}
selected=[]
with events.open("rb") as f:
 for line in f:
  if json.loads(line)["event_id"] in needed:selected.append(line)
assert len(selected)==len(needed)
evidence=historical_replay(first,b"".join(selected))
after={str(p):file_hash(p) for p in (trajectory,events)}
assert before==after
result={"status":"ACTUAL_ORIGINAL_WIRE_ADAPTER_READ_ONLY","first_source_only":True,"input_hashes_before":before,"input_hashes_after":after,
 "file_sizes":{str(p):p.stat().st_size for p in (trajectory,events)},"selected_ref_count":len(needed),
 "task_id":evidence.task_id,"seed":evidence.seed,"saved_commands":len(evidence.commands),"public_states":len(evidence.states),
 "normalized_reference_sha256":digest({"states":evidence.states,"commands":evidence.commands}),
 "interpretation":"original saved evidence binding only; no new replay, model, environment, statistics or report pipeline",
 "real_model_env_training_calls":0,"new_task_bodies_opened":0}
(OWN/"actual_original_source_wire_check.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result))
