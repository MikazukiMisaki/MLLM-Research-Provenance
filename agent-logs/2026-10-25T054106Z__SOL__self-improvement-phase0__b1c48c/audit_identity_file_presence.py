"""Metadata-only file-existence refinement. Never opens unconsumed game/trajectory content."""
import collections,hashlib,json
from pathlib import Path
own=Path(__file__).resolve().parent
candidate_path=Path("/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__LUNA__sft-raw-evidence-audit__b1c48c/AVAILABLE_IDENTITY_CANDIDATES.json")
candidate=json.loads(candidate_path.read_text())
data=Path("/home/lizening/alfworld_data/json_2.1.1")
families={"look_at_obj_in_light","pick_and_place_simple","pick_clean_then_place_in_recep","pick_cool_then_place_in_recep","pick_heat_then_place_in_recep","pick_two_obj_and_place"}
out={"kind":"directory identity plus game-file existence only; no file payload/outcome read","candidate_input":{"path":str(candidate_path),"sha256":hashlib.sha256(candidate_path.read_bytes()).hexdigest()},"splits":{},"new_scientific_calls":0}
for split in ("train","valid_seen","valid_unseen"):
    root=data/split;dirs=[p for p in root.glob("*/trial_*") if p.is_dir()]
    allids={p.relative_to(root).as_posix() for p in dirs}
    gameids={p.relative_to(root).as_posix() for p in dirs if p.parent.name.split("-",1)[0] in families and (p/"game.tw-pddl").is_file()}
    requested={v["identity"] for v in candidate[split]}
    kept=sorted(requested & gameids)
    out["splits"][split]={"directory_identities":len(allids),"six_family_with_existing_game_file":len(gameids),"directory_difference_candidates":len(requested),"difference_candidate_without_supported_existing_game":len(requested-gameids),"file_presence_candidate_difference_count":len(kept),"candidate_ids_hash":hashlib.sha256(json.dumps(kept,sort_keys=True,separators=(",",":")).encode()).hexdigest(),"family_counts_with_existing_game":dict(collections.Counter(x.split("/",1)[0].split("-",1)[0] for x in gameids))}
out["interpretation"]="Luna enumerated all task/trial directories correctly but many lack ALFWorld game.tw-pddl or lie outside the six families. File existence reduces nominal directory differences; these are still only candidates under an incomplete known-use register, not certified clean heldout, runnable-configuration validation, power, schedule or execution permission."
(own/"independent_identity_file_presence.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
