; DEVELOPMENT_ONLY STATIC FIXTURE
(define (problem dev_a_clean_heat)
  (:domain alfred)
  (:objects
    actor - agent
    loc_cabinet_a loc_microwave_a loc_sink_a loc_table_a - location
    cabinet_a microwave_a sink_a table_a - receptacle
    apple_a - object
    FridgeType MicrowaveType rt_cabinet_a rt_table_a SinkBasinType - rtype
    ButterKnifeType KnifeType ot_apple_a - otype
  )
  (:init
    (atLocation actor loc_table_a)
    (canContain rt_cabinet_a ot_apple_a)
    (cleanable apple_a)
    (heatable apple_a)
    (inReceptacle apple_a table_a)
    (objectAtLocation apple_a loc_table_a)
    (objectType apple_a ot_apple_a)
    (openable cabinet_a)
    (pickupable apple_a)
    (receptacleAtLocation cabinet_a loc_cabinet_a)
    (receptacleAtLocation microwave_a loc_microwave_a)
    (receptacleAtLocation sink_a loc_sink_a)
    (receptacleAtLocation table_a loc_table_a)
    (receptacleType cabinet_a rt_cabinet_a)
    (receptacleType microwave_a MicrowaveType)
    (receptacleType sink_a SinkBasinType)
    (receptacleType table_a rt_table_a)
    (= (total-cost) 0)
  )
  (:goal (and (inReceptacle apple_a cabinet_a) (isClean apple_a) (isHot apple_a)))
  (:metric minimize (total-cost))
)
