from morse.builder.creator import ActuatorCreator

class Head(ActuatorCreator):
    _classpath = "abe_sim.actuators.head.Head"
    _blendname = "head"

    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name)

