"""Disabled clean-1 witness contract; no runtime or engine imports.

These are hypotheses for one self-authored development draft, not evidence
that a parser, renderer, or environment accepts them. Observations are limited
to selected facts and do not establish the complete environment state.
"""

PLAN = (
    ("go to source_zero", "gotolocation", {"a": "actor", "lstart": "process_location", "lend": "source_zero_location", "r": "source_zero"}),
    ("take alpha from source_zero", "pickupobject", {"a": "actor", "l": "source_zero_location", "o": "alpha", "r": "source_zero"}),
    ("go to processor", "gotolocation", {"a": "actor", "lstart": "source_zero_location", "lend": "process_location", "r": "processor"}),
    ("clean alpha with processor", "cleanobject", {"a": "actor", "l": "process_location", "o": "alpha", "r": "processor"}),
    ("go to destination_zero", "gotolocation", {"a": "actor", "lstart": "process_location", "lend": "destination_zero_location", "r": "destination_zero"}),
    ("move alpha to destination_zero", "putobject", {"a": "actor", "l": "destination_zero_location", "o": "alpha", "ot": "kind_alpha", "r": "destination_zero", "rt": "kind_destination_zero"}),
)


def _name(value):
    result = getattr(value, "name", None)
    if not isinstance(result, str) or not result:
        raise ValueError("invalid_name")
    return result


def _ground(value):
    name = _name(value)
    mapping = getattr(value, "mapping", None)
    if not isinstance(mapping, dict):
        raise ValueError("ground_mapping_invalid")
    pairs = []
    seen = set()
    for key, item in mapping.items():
        k, v = _name(key).casefold(), _name(item).casefold()
        if k in seen:
            raise ValueError("ground_mapping_duplicate_key")
        seen.add(k)
        pairs.append((k, v))
    return name.casefold(), dict(pairs)


def _actions(state):
    raw = state.get("_valid_commands")
    grounds = state.get("_valid_actions")
    public = state.get("admissible_commands")
    if (not isinstance(raw, list) or not raw or
            not all(isinstance(command, str) and command.strip() for command in raw) or
            len(set(raw)) != len(raw) or not isinstance(grounds, list) or
            len(raw) != len(grounds) or not isinstance(public, list) or
            not all(isinstance(command, str) for command in public) or
            public != sorted(set(raw))):
        raise ValueError("action_map_invalid")
    return raw, grounds, public


def select_ground(state, index):
    """Select the sole exact command with the complete expected grounding."""
    if type(index) is not int or not 0 <= index < len(PLAN):
        raise ValueError("step_index_invalid")
    raw, grounds, public = _actions(state)
    command, name, mapping = PLAN[index]
    if command not in public or raw.count(command) != 1:
        raise ValueError("planned_command_missing_or_ambiguous")
    selected = grounds[raw.index(command)]
    actual_name, actual_mapping = _ground(selected)
    if actual_name != name or actual_mapping != mapping:
        raise ValueError("ground_binding_invalid")
    return selected


def _facts(state):
    source = state.get("_facts")
    if not isinstance(source, list):
        raise ValueError("facts_missing")
    result = []
    for fact in source:
        name = _name(fact).casefold()
        arguments = getattr(fact, "arguments", None)
        if not isinstance(arguments, (list, tuple)):
            raise ValueError("fact_arguments_invalid")
        result.append((name, *(_name(argument).casefold() for argument in arguments)))
    return result


def check_facts(state, stage):
    """Validate stage 0 (reset) through 6 against selected local facts only."""
    if type(stage) is not int or not 0 <= stage <= len(PLAN):
        raise ValueError("fact_stage_invalid")
    location = ("process_location", "source_zero_location", "source_zero_location",
                "process_location", "process_location", "destination_zero_location",
                "destination_zero_location")[stage]
    expected = {("atlocation", "actor", location)}
    if stage < 2:
        expected.update({("inreceptacle", "alpha", "source_zero"),
                         ("objectatlocation", "alpha", "source_zero_location")})
    elif stage < 6:
        expected.update({("holds", "actor", "alpha"), ("holdsany", "actor")})
    else:
        expected.update({("inreceptacle", "alpha", "destination_zero"),
                         ("objectatlocation", "alpha", "destination_zero_location")})
    if stage >= 4:
        expected.add(("isclean", "alpha"))

    def local(fact):
        predicate, *args = fact
        if predicate == "atlocation":
            return bool(args) and args[0] == "actor"
        if predicate in ("inreceptacle", "objectatlocation", "isclean"):
            return bool(args) and args[0] == "alpha"
        if predicate == "holds":
            return bool(args) and (args[0] == "actor" or (len(args) > 1 and args[1] == "alpha"))
        if predicate == "holdsany":
            return bool(args) and args[0] == "actor"
        return False

    observed = set(filter(local, _facts(state)))
    if observed != expected:
        raise ValueError("selected_facts_mismatch")
    goals = {("isclean", "alpha"), ("inreceptacle", "alpha", "destination_zero")}
    if (goals <= observed) != (stage == 6):
        raise ValueError("two_goal_mismatch")
    return {"stage": stage, "selected_facts": sorted(observed),
            "both_goals": goals <= observed,
            "scope": "SELECTED_LOCAL_FACTS_ONLY"}


def observe(state):
    """Serialize relevant observations without importing an engine or retaining objects."""
    raw, grounds, public = _actions(state)
    fact_rows = _facts(state)
    serialized_grounds = []
    for ground in grounds:
        name, mapping = _ground(ground)
        serialized_grounds.append({"name": name, "mapping": mapping})
    last = state.get("_last_action")
    if last is not None:
        name, mapping = _ground(last)
        last = {"name": name, "mapping": mapping}
    feedback, won = state.get("feedback"), state.get("won")
    if not isinstance(feedback, str) or type(won) is not bool:
        raise ValueError("observation_invalid")
    return {"feedback": feedback, "won": won,
            "facts": [list(row) for row in sorted(fact_rows)],
            "raw_commands": list(raw), "public_commands": list(public),
            "groundings": serialized_grounds, "last_action": last}
