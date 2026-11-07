; DEVELOPMENT ONLY: independently authored diagnostic problem, not D
(define (problem dev_single_toggle_probe)
 (:domain alfred)
 (:objects
    probe_actor - agent
    probe_place - location
    probe_table - receptacle
    probe_switch - object
    MicrowaveType SinkBasinType FridgeType rt_probe_table - rtype
    KnifeType ButterKnifeType ot_probe_switch - otype)
 (:init
    (atLocation probe_actor probe_place)
    (receptacleAtLocation probe_table probe_place)
    (receptacleType probe_table rt_probe_table)
    (inReceptacle probe_switch probe_table)
    (objectAtLocation probe_switch probe_place)
    (objectType probe_switch ot_probe_switch)
    (toggleable probe_switch)
    (= (total-cost) 0))
 (:goal (and (isToggled probe_switch)))
 (:metric minimize (total-cost)))
