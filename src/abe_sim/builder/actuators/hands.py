from morse.builder.creator import ActuatorCreator

class Hands(ActuatorCreator):
    _classpath = "abe_sim.actuators.hands.Hands"
    _blendname = "hands"

    def __init__(self, name=None):
        ActuatorCreator.__init__(self, name)

