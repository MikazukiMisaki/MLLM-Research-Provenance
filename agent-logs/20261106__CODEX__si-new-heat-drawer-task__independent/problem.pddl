; SELF_AUTHORED DEVELOPMENT_ONLY; STATIC CANDIDATE; NOT HELD-OUT.
(define (problem development_heat_apple_drawer_nov06)
  (:domain alfred)
  (:objects
    actor - agent
    microwave_spot counter_spot drawer_spot - location
    microwave counter drawer - receptacle
    apple - object
    MicrowaveType SinkBasinType FridgeType drawer_kind - rtype
    KnifeType ButterKnifeType apple_kind - otype
  )
  (:init
    (atLocation actor microwave_spot)
    (receptacleAtLocation microwave microwave_spot)
    (receptacleAtLocation counter counter_spot)
    (receptacleAtLocation drawer drawer_spot)
    (receptacleType microwave MicrowaveType)
    (receptacleType drawer drawer_kind)
    (openable drawer)
    (inReceptacle apple counter)
    (objectAtLocation apple counter_spot)
    (pickupable apple)
    (heatable apple)
    (objectType apple apple_kind)
    (canContain drawer_kind apple_kind)
    (= (total-cost) 0)
  )
  (:goal (and (isHot apple) (inReceptacle apple drawer)))
  (:metric minimize (total-cost))
)
