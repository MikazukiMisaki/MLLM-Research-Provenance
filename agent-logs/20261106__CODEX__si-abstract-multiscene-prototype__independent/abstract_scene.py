"""DEVELOPMENT_ONLY: finite typed role-graph prototype, not ALFWorld tasks.

No I/O, RNG, model, environment, or public-domain parsing. Isomorphism is
exact only for this module's fixed graph schema; arbitrary graphs are rejected.
"""
from dataclasses import dataclass
from hashlib import sha256
from itertools import permutations
import json
import re
from typing import ClassVar

STATUS = 'DEVELOPMENT_ONLY'
FAMILIES = {'clean': 'isClean', 'heat': 'isHot'}
NAME = re.compile(r'[a-z][a-z0-9_]{0,31}\Z')

class InvalidScene(ValueError):
    pass


def _name(value):
    if type(value) is not str or NAME.fullmatch(value) is None:
        raise InvalidScene('invalid abstract role identifier')
    return value


def _mapping(value, expected_keys):
    if type(value) is not dict or set(value) != expected_keys:
        raise InvalidScene('incorrect or ambiguous structured fields')
    return value

@dataclass(frozen=True)
class Scene:
    status: ClassVar[str] = STATUS
    family: str
    targets: tuple[str, ...]
    sources: tuple[str, ...]
    destinations: tuple[str, ...]


def scene(family, targets, sources, destinations):
    if type(family) is not str or family not in FAMILIES:
        raise InvalidScene('unsupported family')
    if any(type(v) not in (tuple, list) for v in (targets, sources, destinations)):
        raise InvalidScene('role arrays must be explicit sequences')
    if not (1 <= len(targets) <= 5 and len(targets) == len(sources) == len(destinations)):
        raise InvalidScene('scene size or role-array length invalid')
    targets, sources, destinations = (tuple(_name(x) for x in v) for v in (targets, sources, destinations))
    if len(set(targets)) != len(targets):
        raise InvalidScene('duplicate target')
    groups = (set(targets), set(sources), set(destinations), {'actor', 'processor'})
    if any(groups[i] & groups[j] for i in range(len(groups)) for j in range(i+1, len(groups))):
        raise InvalidScene('role aliases across disjoint types')
    return Scene(family, targets, sources, destinations)


def _validated(value):
    if type(value) is not Scene:
        raise InvalidScene('expected Scene')
    return scene(value.family, value.targets, value.sources, value.destinations)


def _labels(values):
    seen = {}
    return tuple(seen.setdefault(v, len(seen)) for v in values)


def canonical(value, *, goal_blind=False):
    """Canonical quotient by simultaneous target renaming + independent bin renaming.

    This is complete for the fixed schema: every target has one source, one
    processor, and one destination; actor begins at processor, and typed source,
    processor, destination location sets are disjoint. Arbitrary facts, colors,
    locations, object types, initial states, or extra goal edges are not accepted.
    """
    s = _validated(value)
    if type(goal_blind) is not bool:
        raise InvalidScene('goal_blind must be bool')
    pairs = min((_labels(tuple(s.sources[i] for i in p)),
                 _labels(tuple(s.destinations[i] for i in p)))
                for p in permutations(range(len(s.targets))))
    result = {'status': STATUS, 'schema': 'abstract_scene_v1', 'n': len(s.targets),
              'source_partition': list(pairs[0]), 'destination_partition': list(pairs[1]),
              'family': None if goal_blind else s.family}
    return result


def canonical_sha256(value, *, goal_blind=False):
    encoded = json.dumps(canonical(value, goal_blind=goal_blind), sort_keys=True,
                         separators=(',', ':'), ensure_ascii=True).encode('ascii')
    return {'status': STATUS, 'sha256': sha256(encoded).hexdigest()}


def goal(value):
    s = _validated(value)
    return {'status': STATUS, 'atoms':
            ([{'predicate': FAMILIES[s.family], 'target': t} for t in s.targets] +
             [{'predicate': 'inReceptacle', 'target': t, 'destination': d}
              for t, d in zip(s.targets, s.destinations)])}


def validate_goal_and_language(value, candidate_goal, language):
    """Validate explicitly structured goal and meaning clauses, not natural text."""
    s = _validated(value)
    if type(candidate_goal) is not list or type(language) is not list:
        raise InvalidScene('goal and language must be explicit lists')
    goal_set = set()
    for atom in candidate_goal:
        if type(atom) is not dict:
            raise InvalidScene('invalid goal atom')
        pred = atom.get('predicate')
        if pred == FAMILIES[s.family]:
            _mapping(atom, {'predicate', 'target'})
            key = (pred, _name(atom['target']), None)
        elif pred == 'inReceptacle':
            _mapping(atom, {'predicate', 'target', 'destination'})
            key = (pred, _name(atom['target']), _name(atom['destination']))
        else:
            raise InvalidScene('unsupported or conflicting goal predicate')
        if key in goal_set:
            raise InvalidScene('duplicate goal atom')
        goal_set.add(key)
    expected_goals = {(FAMILIES[s.family], t, None) for t in s.targets}
    expected_goals |= {('inReceptacle', t, d) for t, d in zip(s.targets, s.destinations)}
    if goal_set != expected_goals:
        raise InvalidScene('goal mismatch')
    clauses = set()
    for clause in language:
        _mapping(clause, {'operation', 'target', 'destination'})
        if type(clause['operation']) is not str:
            raise InvalidScene('invalid operation')
        key = (clause['operation'], _name(clause['target']), _name(clause['destination']))
        if key in clauses:
            raise InvalidScene('duplicate language clause')
        clauses.add(key)
    expected_clauses = {(s.family, t, d) for t, d in zip(s.targets, s.destinations)}
    if clauses != expected_clauses:
        raise InvalidScene('structured language/goal mismatch or ambiguity')
    return {'status': STATUS, 'structured_goal_matches_language': True}


def dependencies(value):
    """Required per-target partial order; one-hand resource is a constraint.

    Edges do not claim an ordering between different targets or navigation.
    """
    s = _validated(value)
    nodes = [(t, op) for t in s.targets for op in ('pickup', 'process', 'put')]
    edges = [((t, a), (t, b)) for t in s.targets
             for a, b in (('pickup', 'process'), ('process', 'put'))]
    return {'status': STATUS, 'nodes': nodes, 'edges': edges,
            'resource_constraints': ['single_hand'],
            'additional_navigation_and_runtime_dependencies': 'UNKNOWN'}


def role_graph(value):
    """Build the declared abstract graph in memory, never an environment task."""
    s = _validated(value)
    sources, destinations = sorted(set(s.sources)), sorted(set(s.destinations))
    nodes = [('agent', 'actor'), ('processor', 'processor'), ('processor_location', 'processor')]
    nodes += [('target', t) for t in s.targets]
    nodes += [(kind, x) for x in sources for kind in ('source', 'source_location')]
    nodes += [(kind, x) for x in destinations for kind in ('destination', 'destination_location')]
    edges = [('actor_at', ('agent', 'actor'), ('processor_location', 'processor')),
             ('processor_at', ('processor', 'processor'), ('processor_location', 'processor'))]
    edges += [('source_at', ('source', x), ('source_location', x)) for x in sources]
    edges += [('destination_at', ('destination', x), ('destination_location', x)) for x in destinations]
    edges += [('initially_in', ('target', t), ('source', x)) for t, x in zip(s.targets, s.sources)]
    edges += [('goal_destination', ('target', t), ('destination', x)) for t, x in zip(s.targets, s.destinations)]
    return {'status': STATUS, 'family': s.family, 'nodes': nodes, 'edges': edges,
            'goals': goal(s), 'initial_goal_predicates': 'ASSUMED_FALSE_NOT_ENGINE_CHECKED',
            'physical_and_runtime_feasibility': 'UNKNOWN'}
