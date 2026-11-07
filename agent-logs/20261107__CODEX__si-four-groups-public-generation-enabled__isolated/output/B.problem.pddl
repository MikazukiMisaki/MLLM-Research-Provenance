; DEVELOPMENT_ONLY STATIC FIXTURE
(define (problem dev_b_slice_tool)
  (:domain alfred)
  (:objects
    actor - agent
    loc_shelf_b loc_table_b - location
    shelf_b table_b - receptacle
    knife_b tomato_b - object
    FridgeType MicrowaveType rt_shelf_b rt_table_b SinkBasinType - rtype
    ButterKnifeType KnifeType ot_tomato_b - otype
  )
  (:init
    (atLocation actor loc_table_b)
    (canContain rt_shelf_b ot_tomato_b)
    (canContain rt_table_b KnifeType)
    (inReceptacle knife_b table_b)
    (inReceptacle tomato_b table_b)
    (objectAtLocation knife_b loc_table_b)
    (objectAtLocation tomato_b loc_table_b)
    (objectType knife_b KnifeType)
    (objectType tomato_b ot_tomato_b)
    (pickupable knife_b)
    (pickupable tomato_b)
    (receptacleAtLocation shelf_b loc_shelf_b)
    (receptacleAtLocation table_b loc_table_b)
    (receptacleType shelf_b rt_shelf_b)
    (receptacleType table_b rt_table_b)
    (sliceable tomato_b)
    (= (total-cost) 0)
  )
  (:goal (and (inReceptacle tomato_b shelf_b) (isSliced tomato_b)))
  (:metric minimize (total-cost))
)
