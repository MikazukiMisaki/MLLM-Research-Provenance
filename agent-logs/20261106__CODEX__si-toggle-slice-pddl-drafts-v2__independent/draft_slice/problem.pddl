; SELF_AUTHORED DEVELOPMENT_ONLY STATIC_DRAFT; NOT EVALUATION.
(define (problem dev_slice_symbolic_01)
  (:domain alfred)
  (:objects
    actor - agent
    station_location - location
    station - receptacle
    sample_object knife_tool - object
    SinkBasinType MicrowaveType FridgeType station_kind - rtype
    KnifeType ButterKnifeType sample_kind - otype
  )
  (:init
    (atLocation actor station_location)
    (receptacleAtLocation station station_location)
    (receptacleType station station_kind)
    (inReceptacle sample_object station)
    (objectAtLocation sample_object station_location)
    (objectType sample_object sample_kind)
    (objectType knife_tool KnifeType)
    (holds actor knife_tool)
    (holdsAny actor)
    (sliceable sample_object)
    (= (total-cost) 0)
  )
  (:goal (and (isSliced sample_object)))
  (:metric minimize (total-cost))
)
