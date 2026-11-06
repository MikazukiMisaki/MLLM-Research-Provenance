"""DEVELOPMENT_ONLY in-memory self-authored drafts + temporary dirs; no engine."""
import json
from pathlib import Path
import tempfile
import unittest
import generate_draft as g
import check_draft as c

class DraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.public=g.public_inputs()
    def render(self,case='clean-2'):
        p,t=g.render(case,self.public); return p.decode(),t.decode()
    def rejects(self,p,t):
        with self.assertRaises((c.Invalid,UnicodeError)): c.check(p.encode(),t.encode(),self.public)
    def test_all_four_fixed_drafts_replay_public_actions(self):
        for case in g.CASES:
            with self.subTest(case=case):
                p,t=g.render(case,self.public); out=c.check(p,t,self.public)
                self.assertEqual(out['status'],'DEVELOPMENT_ONLY_STATIC_PASS')
                self.assertEqual(out['target_count'],int(case[-1]))
                self.assertEqual(out['script_steps'],6*int(case[-1]))
                self.assertEqual(out['engine_grounding_rendering_physical_semantics_and_solvability'],'UNKNOWN')
    def test_goal_omission_extra_duplicate_wrong_family(self):
        p,t=self.render()
        variants=[p.replace('(isClean beta)','',1),p.replace('(isClean beta)','(isClean alpha)',1),
                  p.replace('(isClean beta)','(isHot beta)',1),
                  p.replace('(inReceptacle beta destination_one)','(inReceptacle beta destination_zero)',1)]
        for x in variants: self.rejects(x,t)
    def test_missing_and_conflicting_initial_facts(self):
        p,t=self.render()
        for x in [p.replace('(cleanable alpha)','',1),p.replace('(pickupable alpha)','',1),
                  p.replace('(canContain kind_destination_zero kind_alpha)','',1),
                  p.replace('(atLocation actor process_location)','(atLocation actor process_location)\n    (atLocation actor source_zero_location)',1),
                  p.replace('(inReceptacle alpha source_zero)','(inReceptacle alpha source_zero)\n    (isClean alpha)',1),
                  p.replace('(inReceptacle alpha source_zero)','(inReceptacle alpha source_zero)\n    (holdsAny actor)',1)]: self.rejects(x,t)
    def test_wrong_types_ambiguous_references_and_locations(self):
        p,t=self.render()
        for x in [p.replace('SinkBasinType','MicrowaveType'),
                  p.replace('alpha beta - object','alpha alpha - object'),
                  p.replace('(objectType alpha kind_alpha)','(objectType alpha kind_beta)',1),
                  p.replace('(objectType beta kind_beta)','(objectType beta kind_alpha)',1),
                  p.replace('(cleanable alpha)','(cleanable alpha)\n    (heatable alpha)',1),
                  p.replace('(receptacleAtLocation destination_one destination_one_location)','(receptacleAtLocation destination_one destination_zero_location)',1),
                  p.replace('(receptacleAtLocation source_zero source_zero_location)','',1),
                  p.replace('(inReceptacle beta source_zero)','(inReceptacle beta destination_zero)',1)]: self.rejects(x,t)
    def test_instruction_omission_wrong_pair_or_unapproved_grammar(self):
        p,t=self.render()
        for x in [t.replace('; clean beta and put it in destination_one','',1),
                  t.replace('clean beta and put it in destination_one','clean beta and put it in destination_zero',1),
                  t.replace('clean alpha and put it in destination_zero','heat alpha and put it in destination_zero',1),
                  t.replace('clean alpha and put it in destination_zero','clean alpha and put it in destination_zero; clean alpha and put it in destination_zero',1),
                  t.replace('TODO','MODIFIED',1)]: self.rejects(p,x)
    def test_domain_or_grammar_drift_rejected(self):
        p,t=self.render(); inp=dict(self.public); inp['alfred.pddl']+=b'\n'
        with self.assertRaises(c.Invalid): c.check(p.encode(),t.encode(),inp)
        inp=dict(self.public); inp['alfred.twl2']+=b'\n'
        with self.assertRaises(c.Invalid): c.check(p.encode(),t.encode(),inp)
    def test_unknown_sections_and_unbalanced(self):
        p,t=self.render()
        for x in [p.replace('  (:metric','  (:mystery (x))\n  (:metric'),p[:-4],p.replace('(:goal (and','(:goal (or',1)]: self.rejects(x,t)
    def test_output_is_exclusive_and_manifest_not_a_result(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'draft'; result=g.create('heat-2',out)
            self.assertEqual(result['status'],'DEVELOPMENT_ONLY_STATIC_DRAFT')
            self.assertEqual(result['runtime_solvability'],'UNKNOWN')
            self.assertEqual(result,json.loads((out/'manifest.json').read_text()))
            with self.assertRaises(FileExistsError): g.create('heat-2',out)
            self.assertEqual(c.check((out/'problem.pddl').read_bytes(),(out/'derived_grammar.twl2').read_bytes())['target_count'],2)
    def test_nonfixed_case_rejected(self):
        with self.assertRaises(ValueError): g.render('clean-3',self.public)

if __name__=='__main__': unittest.main(verbosity=2)
