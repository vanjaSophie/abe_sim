from morse.builder.creator import ActuatorCreator

class Base(ActuatorCreator):
    _classpath = "abe_sim.actuators.base.Base"
    _blendname = "base"

    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name)

