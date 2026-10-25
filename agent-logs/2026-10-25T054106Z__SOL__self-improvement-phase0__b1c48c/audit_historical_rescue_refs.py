"""Independently check reported historical rescue refs against raw line bytes and outcome fields."""
import collections,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
inventory=Path("/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__CODEX__self-experience-feasibility__b1c48c/experience_inventory.json")
inv=json.loads(inventory.read_text());ix=inv["actual_rescue_index_historical_treatments"]
targets=collections.defaultdict(list)
for ref in ix:targets[inv["stage_summaries"][ref["stage"]]["source_path"]].append(ref)
errors=[];verified=[];sources={}
for path,refs in targets.items():
    p=Path(path); before=hashlib.sha256(p.read_bytes()).hexdigest(); wanted={r["source_line"] for r in refs}
    lines={n:b for n,b in enumerate(p.open("rb"),1) if n in wanted}
    for ref in refs:
        b=lines.get(ref["source_line"]);r=json.loads(b);stage=ref["stage"]
        if stage=="R11_PBR":r=r.get("compact",r)
        if stage in ("SPRINT2C","R4"): c,t=int(r["continue"]["success"]),int(r["recover"]["success"])
        else:
            c=int(r["r_continue"]);t=int(r[{"R10_OSR":"r_osr","R11_PBR":"r_pbr","R16_OSR":"r_osr","R17_PAR":"r_par","R18_C1":"r_fact_text","R18_C2":"r_card_v2"}[stage]])
        parts=str(r["task_id"]).replace("\\","/").rstrip("/").split("/")
        task="/".join(parts[-2:])
        checks={"line_raw_sha256":hashlib.sha256(b).hexdigest()==ref["source_row_sha256"],"prefix_id":r["prefix_id"]==ref["prefix_id"],"canonical_task":task==ref["canonical_task"],"continue_zero":c==0,"recovery_one":t==1}
        verified.append({"stage":stage,"prefix_id":ref["prefix_id"],"canonical_task":task,"source_line":ref["source_line"],"checks":checks})
        if not all(checks.values()):errors.append(verified[-1])
    sources[path]={"sha256_before":before,"sha256_after":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size}
out={"audit_kind":"independent raw outcome and line-ref verification of reported rescue inventory, not policy evaluation/training-row approval","candidate_inventory_path":str(inventory),"candidate_inventory_sha256":hashlib.sha256(inventory.read_bytes()).hexdigest(),"verified_refs":verified,"errors":errors,"historical_rescue_rows":len(verified),"historical_unique_tasks":len({r["canonical_task"] for r in verified}),"input_sources":sources,"limit":"Different stage/treatment rows are repeated observations, not independent training N. R19 separately counted in independent_r19_experience_recount.json. No causal learning utility inferred.","new_scientific_calls":0}
(ROOT/"independent_historical_rescue_verification.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k not in ("verified_refs","input_sources")},indent=2))
