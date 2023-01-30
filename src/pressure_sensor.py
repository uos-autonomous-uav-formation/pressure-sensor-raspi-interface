from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_mcp3xxx.mcp3008 as MCP
from numbers import Number

# Implement a zeroing in startup (like with the airspeed sensor)

class PressureSensor:
    _min_voltage_check: float = 0.3 # When performing start up safety checks, 
    
    zero: int = None

    def __init__(self, mcp: MCP.MCP3008, channel: int, ref_voltage: Number):
        """ Interface for a MPXV7002DP pressure sensor via a MCP analogue to digital converter.
        
        """

        # Initialize connection
        self._input = AnalogIn(mcp, channel)
        self.channel = channel

        # Perform start up checks
        self._start_up_safety_checks()

        # Peform zeroing
        self._zero = self._raw_voltage


    def _start_up_safety_checks(self):
        if self._raw_voltage < self._min_voltage_check:
            raise ValueError(f"Voltage too low for {self.channel}. Check if sensor working and wiring connected.")
    
    @property
    def _raw_pressure(self):
        return (self._raw_voltage / (5 * 0.2)) - 0.5

    @property
    def _raw_voltage(self):
        return self._input.voltage

    @property
    def voltage(self):
        return self._raw_voltage - self._zero

    @property
    def theoretical_error(self):
        pass