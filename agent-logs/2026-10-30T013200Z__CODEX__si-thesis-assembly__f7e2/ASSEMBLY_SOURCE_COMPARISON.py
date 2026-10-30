"""Compare exact manuscript inputs and approved assembly changes, without mutating them."""
import hashlib,json,pathlib,re
P=pathlib.Path
paths={'intro':P('/home/lizening/research-notes/agent-logs/2026-10-30T012000Z__CODEX__si-thesis-review-update__50d8/THESIS_INTRODUCTION_REVISED.md'),'chapter':P('/home/lizening/research-notes/agent-logs/2026-10-30T010000Z__CODEX__si-stage-two-followup__76d9/THESIS_CHAPTER_REVISED.md'),'assembled':P('/home/lizening/research-notes/agent-logs/2026-10-30T013200Z__CODEX__si-thesis-assembly__f7e2/THESIS_ASSEMBLED_WORKING_DRAFT.md')}
expected={'intro':'71a1d937a77645e73e3050079f83845e7d6283fcf0aa86160881dfd92fac6a5c','chapter':'8c28cd16aa600664bdd18206466a12bf6a3168654c8b1085494d87ba3c654879','assembled':'20c01eb4e3d1960e315b181aa9c0b5ef2c69e2802ed0ca8b44e28b30047eefbc'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert {k:sha(p) for k,p in paths.items()}==expected
s={k:p.read_text() for k,p in paths.items()}
def block(text,start,end):return text.split(start,1)[1].split(end,1)[0].strip()
a=block(s['intro'],'## 1. Introduction','## References for this working draft')
b=block(s['assembled'],'## 1. Introduction','## Experimental setting')
a=a.replace('At selected states from an existing agent trajectory,','At selected states from existing agent trajectories,').replace('**A controlled empirical comparison from a common starting point.**','**A nonrandomized, paired empirical comparison from a common starting point.**')
assert a==b
src=s['chapter'];dst=s['assembled']
setting=block(src,'## Experimental setting and research questions','## Position in prior research').replace('Qwen3-8B [4] in ALFWorld [3]','Qwen3-8B [2] in ALFWorld [1]')
assert setting==block(dst,'## Experimental setting','## Supervised continuation comparison')
headings=['Supervised continuation comparison','Results of the self-improvement pilot','Descriptive failure analysis','Exploratory recovery-duration study','Discussion and limitations']
checks={}
for i,h in enumerate(headings):
 src_end='## '+(headings[i+1] if i+1<len(headings) else 'Working references');dst_end='## '+(headings[i+1] if i+1<len(headings) else 'Working appendix: evidence and confidentiality')
 original=block(src,'## '+h,src_end)
 if h=='Discussion and limitations':
  original=original.replace('a controlled, paired comparison of two continuation-data sources','a nonrandomized, paired comparison of two continuation-data procedures').replace('the present controlled comparison','the present paired comparison')
 checks[h]=original==block(dst,'## '+h,dst_end)
assert all(checks.values())
refs=dst.split('## References',1)[1];defined=re.findall(r'^\[(\d+)\]',refs,re.M);body=dst.split('## References',1)[0];used=set(re.findall(r'\[(\d+)\]',body));assert defined==list(map(str,range(1,10))) and used==set(defined)
titles={'1':'ALFWorld: Aligning','2':'Qwen3 Technical','3':'A Reduction of Imitation','4':'Language Models are Few-Shot Butlers','5':'Re-ReST: Reflection-Reinforced','6':'Self-Generated In-Context','7':'Imitation Learning for Multi-turn','8':'Agent Learning via Early Experience','9':'Deep Reinforcement Learning at the Edge'}
for n,title in titles.items():assert any(x.startswith(f'[{n}] ') and title in x for x in refs.splitlines())
assert 'Micheli and Fleuret [4]' in dst and 'Micheli and Fleuret [5]' in src
assert {k:sha(p) for k,p in paths.items()}==expected
print(json.dumps({'source_sha256':expected,'intro_after_two_explicit_changes_matches_assembly':True,'experimental_setting_after_citation_remap_matches':True,'chapter_sections_after_two_explicit_discussion_changes':checks,'removed_chapter_prior_work_is_represented_by_introduction':True,'micheli_chapter_old_5_to_assembled_4':True,'all_nine_citation_labels_defined_once_and_used':True,'reviewed_bytes_unchanged_after':True,'limitations':'Exact section text and citation-title identity checks do not independently validate scientific claims, full bibliography metadata or the new working appendix.'},indent=2,sort_keys=True))
