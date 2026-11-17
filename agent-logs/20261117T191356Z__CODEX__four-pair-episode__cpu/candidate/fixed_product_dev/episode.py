"""Fixed DEV episode using the existing actor, parser and environment ports.

EOS or an ordinary unselected parse is a recorded policy failure for this DEV
protocol. Broken action mappings and other technical errors propagate instead.
The caller supplies an externally enforced controller and all real ports.
"""

import json


def run_episode(*, arm, controller, env_factory, load_producer, source_worker,
                projection, parser, parse_value, state_factory, expected_game,
                expected_eos, expected_pad, previous_initial=None):
    env = producer = None
    history = []
    steps = 0
    try:
        def construct_owned():
            nonlocal env
            env = env_factory()
            return env

        env = controller.effect("env_construct", construct_owned, lambda _: {"arm": arm})
        controller.effect("env_init", env.initialize, lambda _: {"arm": arm})
        reset = controller.effect("reset", env.reset, lambda x: {
            "arm": arm, "state": x[0].to_dict(), "gamefile": x[1],
            "candidate_native_reset": x[2].get("candidate_native_reset")
            if len(x) == 3 and type(x[2]) is dict else None})
        if type(reset) is not tuple or len(reset) != 3 or type(reset[2]) is not dict:
            raise ValueError("native reset unknown")
        state, game = reset[:2]
        native = reset[2].get("candidate_native_reset")
        if (type(native) is not dict or native.get("won_batch") != [False]
                or type(native["won_batch"][0]) is not bool):
            raise ValueError("native reset won unknown")
        if game != expected_game or state.ended:
            raise ValueError("evaluation game identity")
        initial = state.to_dict()
        if previous_initial is not None and json.dumps(
                initial, sort_keys=True, separators=(",", ":"), allow_nan=False) != json.dumps(
                    previous_initial, sort_keys=True, separators=(",", ":"), allow_nan=False):
            raise ValueError("public initial mismatch; hidden state unproven")

        def load_owned():
            nonlocal producer
            producer = load_producer(arm)
            return producer

        producer = controller.effect("model_load", load_owned, lambda _: {"arm": arm})
        token_eos = producer.tokenizer.eos_token_id
        token_pad = producer.tokenizer.pad_token_id
        if (type(token_eos) is not int or type(token_pad) is not int
                or token_eos == token_pad or token_pad != expected_pad
                or token_eos not in expected_eos):
            raise ValueError("tokenizer EOS/pad configuration incompatible")

        def known_result(result):
            # A cleanup failure must not erase an already observed result.
            controller.journal.emit("fixed_product_episode_outcome_known", result)
            return result

        while steps < 50:
            public = projection(state, history)
            valid = state.valid_actions
            mapping = public["action_map"]
            if not valid or len(set(valid)) != len(valid) or list(mapping.values()) != list(valid):
                raise ValueError("ambiguous action mapping")
            try:
                generated = source_worker._generation(producer, public, controller, expected_eos, expected_pad)
            except ValueError as error:
                # These two exact checks in the historical _generation occur
                # after its physical generation/sequence receipt is persisted.
                reasons = {"earlier EOS in output": "EARLIER_EOS",
                           "padding or ambiguous EOS/padding in output": "OUTPUT_PADDING"}
                if str(error) not in reasons:
                    raise
                return known_result({"arm": arm, "initial_public": initial, "won": False,
                                     "steps": steps, "termination": "POLICY_FAILURE",
                                     "failure_reason": reasons[str(error)]})
            selection = parse_value(parser(generated["raw"], valid))
            controller.journal.emit("dev_parser_returned", {
                "arm": arm, "index": steps, "result": selection,
                "eos_last": generated["eos_last"], "output_ids": generated["output_ids"],
                "raw": generated["raw"], "decoder_stop_reason": "NOT_OBSERVED"})
            if type(generated["eos_last"]) is not bool:
                raise ValueError("EOS status unknown")
            action = selection.get("action")
            action_id = selection.get("action_id")
            status = selection.get("selection_status")
            if status not in ("selected", "action_format_violation", "action_out_of_range"):
                raise ValueError("unknown or broken parser mapping")
            selected = status == "selected"
            if selected and (action_id not in mapping or mapping[action_id] != action):
                raise ValueError("selected action mapping mismatch")
            if not generated["eos_last"] or not selected:
                return known_result({"arm": arm, "initial_public": initial, "won": False,
                                     "steps": steps, "termination": "POLICY_FAILURE",
                                     "failure_reason": "MISSING_EOS" if not generated["eos_last"] else "UNSELECTED"})
            transition = controller.effect(
                "step", lambda: env.step(action),
                lambda t: {"arm": arm, "index": steps, "action_id": action_id,
                           "action": action, "transition": source_worker._transition_wire(t)})
            wire = source_worker._transition_wire(transition)
            steps += 1
            history.append((state.observation, action))
            controller.journal.emit("dev_decision_committed", {
                "arm": arm, "index": steps - 1, "action": action, "transition": wire})
            if wire["truncated"] or (wire["won"] and not wire["done"]):
                raise ValueError("unknown or inconsistent terminal")
            if wire["done"]:
                return known_result({"arm": arm, "initial_public": initial, "won": wire["won"],
                                     "steps": steps, "termination": "TERMINAL"})
            if wire["valid_actions"] is None:
                raise ValueError("missing next action map")
            state = state_factory(state, wire)
        return known_result({"arm": arm, "initial_public": initial, "won": False,
                             "steps": steps, "termination": "HORIZON"})
    finally:
        errors = []
        for name, obj in (("environment", env), ("producer", producer),
                          ("resource", getattr(producer, "resource", None))):
            if obj is None:
                continue
            try:
                controller.journal.emit(name + "_close_started", {"arm": arm})
            except BaseException as error:
                errors.append(error)
            try:
                obj.close()
                try:
                    controller.journal.emit(name + "_close_returned", {"arm": arm})
                except BaseException as error:
                    errors.append(error)
            except BaseException as error:
                errors.append(error)
                try:
                    controller.journal.emit(name + "_close_unknown", {"arm": arm})
                except BaseException:
                    pass
        if errors:
            raise RuntimeError("one or more cleanup operations UNKNOWN") from errors[0]
