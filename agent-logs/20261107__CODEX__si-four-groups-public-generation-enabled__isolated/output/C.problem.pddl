; DEVELOPMENT_ONLY STATIC FIXTURE
(define (problem dev_c_cool_pair)
  (:domain alfred)
  (:objects
    actor - agent
    loc_fridge_c loc_shelf_c loc_table_c - location
    fridge_c shelf_c table_c - receptacle
    apple_c pear_c - object
    FridgeType MicrowaveType rt_shelf_c rt_table_c SinkBasinType - rtype
    ButterKnifeType KnifeType ot_apple_c ot_pear_c - otype
  )
  (:init
    (atLocation actor loc_fridge_c)
    (canContain rt_shelf_c ot_apple_c)
    (canContain rt_shelf_c ot_pear_c)
    (coolable apple_c)
    (coolable pear_c)
    (inReceptacle apple_c table_c)
    (inReceptacle pear_c table_c)
    (objectAtLocation apple_c loc_table_c)
    (objectAtLocation pear_c loc_table_c)
    (objectType apple_c ot_apple_c)
    (objectType pear_c ot_pear_c)
    (pickupable apple_c)
    (pickupable pear_c)
    (receptacleAtLocation fridge_c loc_fridge_c)
    (receptacleAtLocation shelf_c loc_shelf_c)
    (receptacleAtLocation table_c loc_table_c)
    (receptacleType fridge_c FridgeType)
    (receptacleType shelf_c rt_shelf_c)
    (receptacleType table_c rt_table_c)
    (= (total-cost) 0)
  )
  (:goal (and (inReceptacle apple_c shelf_c) (inReceptacle pear_c shelf_c) (isCool apple_c) (isCool pear_c)))
  (:metric minimize (total-cost))
)
