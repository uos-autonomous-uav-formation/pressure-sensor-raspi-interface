import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Implement a zeroing in startup (like with the airspeed sensor)

class PressureSensor:
    zero: int = None

    def __init__(self, mcp, channel, ref_voltage):
        self.input = AnalogIn(mcp, channel)

    
    @property
    def pressure(self):
        return (self.input / (5 * 0.2)) - 0.5

    @property
    def theoretical_error(self):
        pass