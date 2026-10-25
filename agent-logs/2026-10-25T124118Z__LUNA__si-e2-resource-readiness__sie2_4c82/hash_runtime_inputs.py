#!/usr/bin/env python3
"""Read-only SHA256/size inventory of pinned runtime and original G3 evidence."""
import hashlib, json, os
from pathlib import Path

PROJECT = Path('/home/lizening/Alfworld-Self-Improvement-Project')
G3 = Path('/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z')
SUP = Path('/home/lizening/research-notes/agent-logs/2026-10-23T002200Z__LUNA__r19-g3-live-successor__2da980f/supervisor_live')
SNAP = Path('/home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218')
ADAPTER = PROJECT / 'artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter'
GAME = Path('/home/lizening/alfworld_data/json_2.1.1/train/pick_and_place_simple-Pencil-None-GarbageCan-316/trial_T20190907_165839_449092/game.tw-pddl')
CONFIGS = [
    Path('/home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g2_alfworld.yaml'),
    Path('/home/lizening/wt-r19-recovery-duration-v1/configs/local/alfworld_base_a40.yaml'),
    Path('/home/lizening/wt-r19-recovery-duration-v1/configs/experiments/r19_recovery_duration_v1.json'),
    Path('/home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g3_gate_2da980f_phase1.json'),
    PROJECT / 'configs/model/qwen3_8b.yaml',
    PROJECT / 'configs/sft/sft_dataset_schema.json',
    PROJECT / 'configs/sft/sft_run_config.json',
    PROJECT / 'configs/sft/sft_training_protocol.json',
]
G3_NAMES = ['g3_gate_receipt.json','environment_manifest.json','source_trajectories.jsonl','unit_registry.json','execution_manifest.json','branches.jsonl','runtime_manifest_preload.json','execution_events.jsonl','runtime_manifest.json','source_restart_comparison.json']
SUP_NAMES = ['launch_context.json','runner.log','runner_exit.json','supervisor_status.json']

def sha_file(p):
    h=hashlib.sha256(); n=0
    with p.open('rb') as f:
        while True:
            b=f.read(8*1024*1024)
            if not b: break
            h.update(b); n+=len(b)
    return {'path':str(p),'exists':True,'bytes':n,'sha256':h.hexdigest(),'is_symlink':p.is_symlink(),'symlink_target':os.readlink(p) if p.is_symlink() else None}

def tree(root):
    if not root.exists(): return {'root':str(root),'exists':False,'files':[]}
    fs=sorted((p for p in root.rglob('*') if p.is_file()),key=lambda p:p.relative_to(root).as_posix())
    rows=[]
    for p in fs:
        item=sha_file(p); item['relative_path']=p.relative_to(root).as_posix(); rows.append(item)
    return {'root':str(root),'exists':True,'file_count':len(rows),'files':rows}

out={'schema':'SI_E2_RUNTIME_INPUT_HASHES_V1','cached_base_snapshot':tree(SNAP),'p0_final_adapter':tree(ADAPTER),'g3_output_files':[sha_file(G3/n) for n in G3_NAMES],'g3_supervisor_files':[sha_file(SUP/n) for n in SUP_NAMES],'fixed_game_file':sha_file(GAME),'bound_config_files':[sha_file(p) if p.exists() else {'path':str(p),'exists':False} for p in CONFIGS]}
print(json.dumps(out,sort_keys=True,separators=(',',':')))
