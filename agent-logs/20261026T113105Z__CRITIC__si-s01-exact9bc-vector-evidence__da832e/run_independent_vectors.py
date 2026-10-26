"""Bounded independent exact9bc production-function vector evidence; external I/O fake."""
from pathlib import Path
import argparse,collections,hashlib,importlib.abc,json,os,shutil,sys,tarfile,time,traceback

EXACT="9bc15b593ec6144915762a2fb1b172e063fe2c48"
ORACLE_SHA="e6f7a7ccb12264c92a46c31c1b60856df151b447e40b03edd9db7edaacf35402"
ADAPTER_SHA="6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11"
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def check(value,message):
    if not value:raise AssertionError(message)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",required=True);parser.add_argument("--archive",required=True)
    parser.add_argument("--oracle",required=True);parser.add_argument("--runs",required=True)
    parser.add_argument("--own",required=True)
    a=parser.parse_args()
    source,archive,oracle,runs,own=map(Path,(a.source,a.archive,a.oracle,a.runs,a.own))
    check(sha(oracle)==ORACLE_SHA,"independent oracle changed")
    doc=json.loads(oracle.read_text())
    check(doc["status"]=="DESIGN_VECTORS_ONLY_NOT_SOFTWARE_PASS_NOT_RUNTIME_AUTHORIZATION","oracle scope")
    check(len(doc["cases"])==7,"exactly seven authorized cases")
    family_order=doc["literal_protocol"]["family_order"]
    literal_N=doc["literal_protocol"]["N"]
    # Verify the archived committed files against the isolated extraction; no git worktree mutates.
    files={};links={}
    with tarfile.open(archive,"r:") as tf:
        check(tf.pax_headers.get("comment")==EXACT,"git archive commit identity")
        for member in tf.getmembers():
            target=source/member.name
            check(target.is_relative_to(source),"archive path scope")
            if member.isfile():
                expected=hashlib.sha256(tf.extractfile(member).read()).hexdigest()
                check(target.is_file() and not target.is_symlink() and sha(target)==expected,"extraction differs: "+member.name)
                files[member.name]=expected
            elif member.issym():
                check(target.is_symlink() and os.readlink(target)==member.linkname,"archive link differs")
                links[member.name]=member.linkname
    save(own/"ARCHIVE_SOURCE_BINDING.json",{"exact_commit":EXACT,"archive_path":str(archive),"archive_sha256":sha(archive),
        "regular_file_count":len(files),"files":files,"symlinks":links,"checked_against_archive":True})
    blocked_imports=[];blocked_external=[]
    forbidden={"torch","transformers","peft","tokenizers","alfworld","textworld","gym","gymnasium","huggingface_hub","pytest"}
    class NoRealRuntime(importlib.abc.MetaPathFinder):
        def find_spec(self,fullname,path=None,target=None):
            if fullname.split(".",1)[0] in forbidden:
                blocked_imports.append(fullname)
                raise RuntimeError("forbidden real runtime import in software-vector harness: "+fullname)
            return None
    sys.meta_path.insert(0,NoRealRuntime())
    def boundary_guard(event,args):
        if event in {"subprocess.Popen","os.system","socket.connect","socket.bind"}:
            blocked_external.append(event)
            raise RuntimeError("forbidden external boundary in software-vector harness: "+event)
    sys.addaudithook(boundary_guard)
    sys.path[:0]=[str(source/"src"),str(source/"tests")]
    # Only these test helpers are reused. Their metadata/plan/constants are never used.
    from si_s01_support import Tokenizer,FakeEnv
    from self_improvement.si_s01.contract import bind_plan
    from self_improvement.si_s01.collector import Producer,Collector
    from self_improvement.si_s01.audit import audit,write_report
    from self_improvement.si_s01.evidence import Ledger,Journal
    from self_improvement.si_p3.collector import parse_generation
    import inspect
    function_origins={name:inspect.getsourcefile(obj) for name,obj in {
        "Producer":Producer,"Collector":Collector,"Ledger":Ledger,"Journal":Journal,
        "parser":parse_generation,"audit":audit,"write_report":write_report,
        "fake_tokenizer":Tokenizer,"fake_environment":FakeEnv}.items()}
    check(all(Path(p).is_relative_to(source) for p in function_origins.values()),"function came from outside exact archive")
    save(own/"CLEAN_EXECUTION_CONTEXT.json",{
        "python":sys.executable,"python_version":sys.version,"isolated":sys.flags.isolated,
        "dont_write_bytecode":sys.dont_write_bytecode,"sys_path":sys.path,
        "environment":dict(os.environ),"function_origins":function_origins,
        "evidence_class":"synthetic_software_fixture","real_runtime_import_guard":sorted(forbidden),
        "oracle_path":str(oracle),"oracle_sha256":sha(oracle),"exact_commit":EXACT,
    })
    metadata_rows=[]
    for family,n in zip(family_order,literal_N):
        for local in range(n):
            identity=family+"-IndependentOracle-None-Table-"+str(local)+"/trial_independent_"+str(local)
            metadata_rows.append({"identity":identity,"family":family,"partition":"acquisition_feasibility_96",
                "identity_sha256":hashlib.sha256(identity.encode()).hexdigest(),"partition_rank_sha256":"b"*64})
    metadata=json.dumps({"status":"ADOPTED_DESIGN_METADATA_ONLY_NOT_EXECUTABLE_NOT_AUTHORIZED",
        "no_schedule_indices_seeds_cutoffs_or_argv_per_identity":True,"rows":metadata_rows},
        ensure_ascii=True,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    plan=bind_plan(metadata,evidence_class="synthetic_software_fixture",synthetic_sha256=hashlib.sha256(metadata).hexdigest())
    check(len(plan.slots)==96,"producer plan does not contain96")
    check([sum(s.family==f for s in plan.slots) for f in family_order]==literal_N,"production quotas differ from independent oracle")
    reports=own/"case_reports";reports.mkdir()
    results=[];t0=time.monotonic()
    for case in doc["cases"]:
        case_id=case["id"];out=runs/case_id;expected=case["expected"]
        record={"case_id":case_id,"expected_status":expected["status"],"run_output":str(out)}
        case_start=time.monotonic()
        try:
            mode_by_task={}
            for family in family_order:
                group=[s for s in plan.slots if s.family==family]
                modes=case["slot_modes_by_family_local_index"][family]
                check(len(group)==len(modes),"family-local translation length")
                mode_by_task.update({slot.task_id:m for slot,m in zip(group,modes)})
            check(len(mode_by_task)==96,"mode map must have96 unique synthetic tasks")
            calls=[];seen={};load_calls=[]
            def raw(prepared,slot,index):
                mode=mode_by_task[slot.task_id]
                text="bad" if mode=="F" and index==5 else "A000"
                tokens=[ord(ch) for ch in text]+[1]
                value={
                    "prompt":prepared.prepared.prompt,"rendered_prompt":prepared.prepared.rendered_prompt,
                    "rendered_prompt_sha256":hashlib.sha256(prepared.prepared.rendered_prompt.encode()).hexdigest(),
                    "raw_output":text,"token_ids":tokens,
                    "token_ids_sha256":hashlib.sha256(json.dumps(tokens,separators=(",",":")).encode()).hexdigest(),
                    "input_tokens":len(prepared.prepared.input_ids),"generated_tokens":len(tokens),
                    "latency_seconds":0.0,"output_complete":True,"token_cap_reached":False,"max_new_tokens":16,
                    "do_sample":False,"thinking":False,"adapter_mode":"P0","adapter_sha256":ADAPTER_SHA,
                }
                calls.append({"task_id":slot.task_id,"index":index,"mode":mode})
                return {"raw":value,"runtime":{"synthetic_software_fixture":True}}
            producer=Producer(Tokenizer(),raw,evidence_class="synthetic_software_fixture")
            def factory(slot):
                mode=mode_by_task[slot.task_id]
                settings={"done_at":1,"empty_at":1} if mode=="N" else {"done_at":6,"empty_at":6} if mode=="S" else {"done_at":-1}
                env=FakeEnv(slot,settings);seen[slot.task_id]=env
                return env
            def loader(ledger):
                load_calls.append(True);return producer
            collector=Collector(plan,loader,factory,out,
                run_id=hashlib.sha256(("independent-"+EXACT+"-"+case_id).encode()).hexdigest()[:32],
                devices=0)
            _,stop=collector.run()
            record["collector_stop"]=stop
            check(stop is None,"collector stopped: "+repr(stop))
            observed=audit(out/"source_events.jsonl",out/"source_trajectories.jsonl",plan,producer)
            write_report(out,observed)
            trajectories=[json.loads(line) for line in (out/"source_trajectories.jsonl").read_text().splitlines()]
            events=[json.loads(line) for line in (out/"source_events.jsonl").read_text().splitlines()]
            check(observed["status"]==expected["status"],"status differs from independent literal")
            check(observed["upper_bounds"]==expected["upper_bounds"],"E/F/S total or family differs from independent literal")
            check(observed["normal_sources"]==96 and observed["source_phase_sealed"] is True,"96 normal sources were not sealed")
            check(len(trajectories)==96 and all(r["disposition"]=="NORMAL_SOURCE" and r["YT"] is None and r["teacher_status"]=="TEACHER_NOT_AUTHORIZED_SOURCE_ONLY" for r in trajectories),"normal96/YT NA contract")
            check(observed["all_YT"] is None and observed["teacher_status"]=="TEACHER_NOT_AUTHORIZED_SOURCE_ONLY","teacher measurement claim")
            check(not observed["physical"]["open_units"] and not observed["physical"]["failed_units"],"open or failed physical units")
            wanted=expected["synthetic_boundary_calls"]
            components=observed["physical"]["components"]
            check(components=={k:wanted[k] for k in ("model_load","env_construct","reset","generation","step","env_close")},"physical component counts differ from literal")
            check(observed["physical"]["completed"]["generations"]==wanted["generation"],"generation debit differs")
            check(observed["physical"]["completed"]["environment_operations"]==wanted["environment_operations"],"environment debit differs")
            check(len(calls)==wanted["generation"] and len(load_calls)==1 and len(seen)==96,"external fake boundary counts differ")
            check(all(env.resets==1 and env.closed for env in seen.values()),"fresh single-reset environment not closed")
            check(sum(r["Y0"] for r in trajectories)==expected["source_Y0"]["successes"],"normal source successes differ")
            check(sum(r["Y0"]==0 for r in trajectories)==expected["source_Y0"]["failures"],"normal source failures differ")
            allowed_kinds={"model_load","env_construct","reset","generation","step","env_close"}
            started=[e["payload"] for e in events if e["kind"]=="unit_started"]
            check(all(p["identity"]["phase"]=="source" and p["identity"]["kind"] in allowed_kinds for p in started),"non-source phase or operation")
            for row in trajectories:
                mode=mode_by_task[row["slot"]["task_id"]]
                spec=doc["mode_specification"][mode]
                check((len(row["source"]["steps"]),len(row["source"]["generations"]),row["Y0"])==
                    (spec["executed_actions"],spec["generation_attempts"],spec["Y0"]),"source mode translation incorrect")
            check(observed["science_acceptance"]=="NOT_LEARNING_OR_TEACHER_ACCEPTANCE","wrong scientific interpretation")
            check(observed["real_device_hours"]==0,"software fixture claimed real allocation")
            check("Necessary upper bounds do not establish recipe or learning efficacy." in (out/"SOURCE_REPORT.md").read_text(),"report lacks necessary-condition qualification")
            for name in ("source_report.json","SOURCE_REPORT.md"):
                shutil.copyfile(out/name,reports/(case_id+"."+name))
            record.update(outcome="MATCHED_INDEPENDENT_LITERAL_ORACLE",observed_status=observed["status"],
                observed_upper_bounds=observed["upper_bounds"],normal_sources=96,source_phase_sealed=True,
                all_YT_NA=True,open_units=0,failed_units=0,non_source_calls=0,
                physical=observed["physical"],real_device_hours=observed["real_device_hours"])
        except BaseException as error:
            record.update(outcome="FAILED_OR_INTERFACE_MISMATCH",exception=type(error).__name__,message=str(error))
            print("CASE_FAILURE "+case_id,flush=True);traceback.print_exc()
        record["wall_seconds"]=time.monotonic()-case_start
        record["raw_artifacts"]={name:{"path":str(out/name),"bytes":(out/name).stat().st_size,"sha256":sha(out/name)}
            for name in ("source_events.jsonl","source_trajectories.jsonl","source_report.json","SOURCE_REPORT.md") if (out/name).is_file()}
        results.append(record)
        save(own/"CASE_RESULTS.json",results)
        print(json.dumps({"case":case_id,"outcome":record["outcome"],"observed_status":record.get("observed_status"),
            "wall_seconds":record["wall_seconds"]}),flush=True)
    check(sha(oracle)==ORACLE_SHA,"oracle changed during software acceptance")
    unchanged=all(sha(source/name)==expected for name,expected in files.items()) and all(os.readlink(source/name)==target for name,target in links.items())
    check(unchanged,"isolated source archive was modified")
    loaded_forbidden=sorted(forbidden.intersection(sys.modules))
    check(not blocked_imports and not blocked_external and not loaded_forbidden,"real runtime or external boundary attempted")
    matched=sum(r["outcome"]=="MATCHED_INDEPENDENT_LITERAL_ORACLE" for r in results)
    summary={"status":"EXACT9BC_SOFTWARE_VECTOR_EVIDENCE","exact_commit":EXACT,
        "oracle_path":str(oracle),"oracle_sha256_before":ORACLE_SHA,"oracle_sha256_after":sha(oracle),
        "case_count":7,"matched_cases":matched,"failed_cases":7-matched,
        "normal_synthetic_sources_observed":sum(r.get("normal_sources",0) for r in results),
        "synthetic_completed":dict(sum((collections.Counter(r.get("physical",{}).get("completed",{})) for r in results),collections.Counter())),
        "all_YT_NA_in_matched_cases":all(r.get("all_YT_NA") is True for r in results if r["outcome"]=="MATCHED_INDEPENDENT_LITERAL_ORACLE"),
        "real_model_tokenizer_cuda_alfworld_ssh_preflight_calls":0,
        "blocked_real_import_attempts":blocked_imports,"blocked_external_attempts":blocked_external,
        "forbidden_runtime_modules_loaded":loaded_forbidden,
        "isolated_source_unchanged":unchanged,"archive_sha256":sha(archive),"run_root":str(runs),
        "wall_seconds":time.monotonic()-t0,"final_pass_or_launch_clearance":False}
    save(own/"SUMMARY.json",summary);print(json.dumps(summary),flush=True)
    return 0 if matched==7 else 1

if __name__=="__main__":
    raise SystemExit(main())

