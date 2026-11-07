; DEVELOPMENT_ONLY STATIC FIXTURE
(define (problem dev_d_use_place)
  (:domain alfred)
  (:objects
    actor - agent
    loc_cabinet_d loc_table_d - location
    cabinet_d table_d - receptacle
    lamp_d mug_d - object
    FridgeType MicrowaveType rt_cabinet_d rt_table_d SinkBasinType - rtype
    ButterKnifeType KnifeType ot_lamp_d ot_mug_d - otype
  )
  (:init
    (atLocation actor loc_table_d)
    (canContain rt_cabinet_d ot_mug_d)
    (inReceptacle lamp_d table_d)
    (inReceptacle mug_d table_d)
    (objectAtLocation lamp_d loc_table_d)
    (objectAtLocation mug_d loc_table_d)
    (objectType lamp_d ot_lamp_d)
    (objectType mug_d ot_mug_d)
    (openable cabinet_d)
    (pickupable mug_d)
    (receptacleAtLocation cabinet_d loc_cabinet_d)
    (receptacleAtLocation table_d loc_table_d)
    (receptacleType cabinet_d rt_cabinet_d)
    (receptacleType table_d rt_table_d)
    (toggleable lamp_d)
    (= (total-cost) 0)
  )
  (:goal (and (inReceptacle mug_d cabinet_d) (isToggled lamp_d)))
  (:metric minimize (total-cost))
)
