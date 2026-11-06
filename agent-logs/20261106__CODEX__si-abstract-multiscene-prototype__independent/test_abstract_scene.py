"""DEVELOPMENT_ONLY: in-memory fake role graphs only; no engine or task data."""
import itertools
import unittest
import abstract_scene as a


def mk(family='clean', sources=('s0','s0','s1'), destinations=('d0','d1','d0')):
    return a.scene(family, tuple('t'+str(i) for i in range(len(sources))), sources, destinations)


def language(s):
    return [{'operation':s.family,'target':t,'destination':d} for t,d in zip(s.targets,s.destinations)]


def norm(v):
    d={}
    return tuple(d.setdefault(x,len(d)) for x in v)

class AbstractTests(unittest.TestCase):
    def test_status_and_graph_edges(self):
        s=mk(); graph=a.role_graph(s)
        self.assertEqual(s.status,'DEVELOPMENT_ONLY')
        self.assertEqual(a.canonical_sha256(s)['status'],'DEVELOPMENT_ONLY')
        self.assertEqual(graph['status'],'DEVELOPMENT_ONLY')
        self.assertEqual(len([x for x in graph['edges'] if x[0]=='initially_in']),3)
        self.assertEqual(len([x for x in graph['edges'] if x[0]=='goal_destination']),3)
        self.assertEqual(graph['goals']['status'],'DEVELOPMENT_ONLY')
        self.assertEqual(len(graph['goals']['atoms']),6)
        self.assertEqual(graph['physical_and_runtime_feasibility'],'UNKNOWN')

    def test_joint_rename_permutation_all_orders(self):
        s=mk()
        for perm in itertools.permutations(range(3)):
            renamed=a.scene('clean',[f'x{j}' for j in range(3)],
                ['left' if s.sources[i]=='s0' else 'right' for i in perm],
                ['one' if s.destinations[i]=='d0' else 'two' for i in perm])
            self.assertEqual(a.canonical(s),a.canonical(renamed))
            self.assertEqual(a.canonical_sha256(s),a.canonical_sha256(renamed))

    def test_distinguishes_source_destination_and_pairing(self):
        original=mk(sources=('s0','s0','s1','s1'),destinations=('d0','d0','d1','d1'))
        crossed=mk(sources=('s0','s0','s1','s1'),destinations=('d0','d1','d0','d1'))
        self.assertNotEqual(a.canonical(original),a.canonical(crossed))
        separate=mk(sources=('s0','s1','s2','s3'),destinations=('d0','d0','d1','d1'))
        self.assertNotEqual(a.canonical(original),a.canonical(separate))
        swapped=mk(sources=('s0','s0','s0','s1'),destinations=('d0','d0','d1','d1'))
        self.assertNotEqual(a.canonical(swapped),a.canonical(mk(sources=('s0','s0','s1','s1'),destinations=('d0','d0','d0','d1'))))

    def test_family_and_goal_blind(self):
        self.assertNotEqual(a.canonical(mk()),a.canonical(mk('heat')))
        self.assertEqual(a.canonical(mk(),goal_blind=True),a.canonical(mk('heat'),goal_blind=True))
        with self.assertRaises(a.InvalidScene): a.canonical(mk(),goal_blind=1)

    def test_exact_abstract_orbit_counts(self):
        counts=[]
        for n in range(1,6):
            partitions={norm(p) for p in itertools.product(range(n), repeat=n)}
            signatures=set()
            for src in partitions:
                for dst in partitions:
                    s=mk(sources=tuple('s'+str(x) for x in src),destinations=tuple('d'+str(x) for x in dst))
                    c=a.canonical(s)
                    signatures.add((tuple(c['source_partition']),tuple(c['destination_partition'])))
            counts.append(len(signatures))
        self.assertEqual(counts,[1,4,10,33,91])
        self.assertEqual(sum(counts),139)

    def test_canonical_against_independent_bipartite_isomorphism(self):
        # Independent oracle: adjacency multiplicities up to row/column permutations.
        # Exhaustive through n=4; no scene contents or runtime calls.
        for n in range(1,5):
            partitions={norm(p) for p in itertools.product(range(n), repeat=n)}
            forward={}; backward={}
            for src in partitions:
                for dst in partitions:
                    rows=range(max(src)+1); cols=range(max(dst)+1)
                    matrix=min(tuple(sum(x==r and y==c for x,y in zip(src,dst))
                                     for r in rp for c in cp)
                               for rp in itertools.permutations(rows)
                               for cp in itertools.permutations(cols))
                    oracle=(len(rows),len(cols),matrix)
                    s=mk(sources=tuple('s'+str(x) for x in src),
                         destinations=tuple('d'+str(x) for x in dst))
                    c=a.canonical(s)
                    key=(tuple(c['source_partition']),tuple(c['destination_partition']))
                    if key in forward: self.assertEqual(forward[key],oracle)
                    if oracle in backward: self.assertEqual(backward[oracle],key)
                    forward[key]=oracle; backward[oracle]=key

    def test_boundaries_and_aliases(self):
        for n in (1,5):
            self.assertEqual(a.canonical(mk(sources=tuple('s'+str(i) for i in range(n)),destinations=tuple('d'+str(i) for i in range(n))))['n'],n)
        bad=[('clean',[],[],[]),('clean',['a']*6,['s']*6,['d']*6),('bad',['a'],['s'],['d']),
             ('heat',['a','a'],['s','s'],['d','d']),('clean',['a'],['same'],['same']),
             ('clean',['actor'],['s'],['d']),('clean',['a'],['s'],[]),
             ('clean',[True],['s'],['d']),('clean',['a'],['source one'],['d'])]
        for args in bad:
            with self.subTest(args=args), self.assertRaises(a.InvalidScene): a.scene(*args)
        with self.assertRaises(a.InvalidScene): a.canonical(a.Scene('evil',('t',),('s',),('d',)))

    def test_structure_goal_language(self):
        for fam in ('clean','heat'):
            s=mk(fam); g=a.goal(s)['atoms']; lang=language(s)
            self.assertTrue(a.validate_goal_and_language(s,list(reversed(g)),list(reversed(lang)))['structured_goal_matches_language'])
            bad_goals=[g[:-1],g+[g[0]],g+[{'predicate':'isCool','target':s.targets[0]}],
                       [dict(x, extra='x') if i==0 else x for i,x in enumerate(g)],
                       [dict(x, destination='d99') if i==3 else x for i,x in enumerate(g)]]
            for bg in bad_goals:
                with self.assertRaises(a.InvalidScene): a.validate_goal_and_language(s,bg,lang)
            bad_lang=[lang[:-1],lang+[lang[0]], [dict(x,operation='heat' if fam=='clean' else 'clean') if i==0 else x for i,x in enumerate(lang)],
                      [dict(x,destination='d99') if i==0 else x for i,x in enumerate(lang)],
                      [dict(x,target='unknown') if i==0 else x for i,x in enumerate(lang)]]
            for bl in bad_lang:
                with self.assertRaises(a.InvalidScene): a.validate_goal_and_language(s,g,bl)

    def test_dependency_partial_order(self):
        s=mk(); dep=a.dependencies(s); nodes=set(dep['nodes']); edges=dep['edges']
        self.assertEqual(len(nodes),9); self.assertEqual(len(edges),6)
        self.assertEqual(dep['resource_constraints'],['single_hand'])
        for (t,src),(u,dst) in edges:
            self.assertEqual(t,u)
            self.assertIn((src,dst),[('pickup','process'),('process','put')])
        order=[]
        while nodes:
            ready=sorted(n for n in nodes if not any(v==n and u in nodes for u,v in edges))
            self.assertTrue(ready,'cycle')
            order.extend(ready); nodes.difference_update(ready)
        self.assertEqual(len(order),9)

if __name__=='__main__': unittest.main(verbosity=2)
