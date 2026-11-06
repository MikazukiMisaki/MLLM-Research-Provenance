; SELF_AUTHORED DEVELOPMENT_ONLY STATIC_DRAFT; NOT EVALUATION.
(define (problem dev_toggle_symbolic_01)
  (:domain alfred)
  (:objects
    actor - agent
    station_location - location
    station - receptacle
    toggle_device - object
    SinkBasinType MicrowaveType FridgeType station_kind - rtype
    KnifeType ButterKnifeType device_kind - otype
  )
  (:init
    (atLocation actor station_location)
    (receptacleAtLocation station station_location)
    (receptacleType station station_kind)
    (inReceptacle toggle_device station)
    (objectAtLocation toggle_device station_location)
    (objectType toggle_device device_kind)
    (toggleable toggle_device)
    (isOn toggle_device)
    (= (total-cost) 0)
  )
  (:goal (and (isToggled toggle_device)))
  (:metric minimize (total-cost))
)
