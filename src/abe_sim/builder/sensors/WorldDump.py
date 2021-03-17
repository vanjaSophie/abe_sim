from morse.builder.creator import SensorCreator

class WorldDump(SensorCreator):
    _classpath = "abe_sim.sensors.WorldDump.WorldDump"
    _blendname = "WorldDump"

    def __init__(self, name=None):
        SensorCreator.__init__(self, name)

