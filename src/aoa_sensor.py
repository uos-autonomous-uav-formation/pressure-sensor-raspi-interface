import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from .pressure_sensor import PressureSensor


class AoaSensor:
    
    def __init__(self, spi, chip_select, ref_voltage, 
    orientation: dict[int, int] = None):
        """
        Angle of attack sensor implementation using MCP3008.

        Args:
            spi: The SPI bus connecting to the MCP3008 chip.
            chip_select: The chipselect pin. For example board.D7
            ref_voltage: The refernce voltage the chip is connected to
            orientaion: The pin alloction of each probe hole. Key is the probe hole based on image, value is the pin (min 0, max 7)  Defaults to: {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}
        
        """

        if orientation is None:
            orientation = {
                1: 0,
                2: 1,
                3: 2,
                4: 3,
                5: 4
            }
        else:
            if max(orientation.values()) > 8:
                raise ValueError("Pin value too high for an MCP3008 chip, maximum value 7")
            if min(orientation.values()) < 0:
                raise ValueError("Pin value too low for an MCP3008 chip, minimum value 0")

        self._chip_select = digitalio.DigitalInOut(chip_select)
        self._mcp = MCP.MCP3008(spi, self._chip_select, ref_voltage=ref_voltage)
        self.ref_voltage = ref_voltage
        self._allocate_pressure_sensor(orientation)

    def _allocate_pressure_sensor(self, orientation):
        self._pressure_sensors = {}
        
        for key, item in orientation.items():
            self._pressure_sensors[key] = PressureSensor(self._mcp, item, ref_voltage=self.ref_voltage)

    def dbg(self):
        for key, item in self._pressure_sensors.items():
            print(f"Probe location {key}, Channel {item.channel}, pressure sensor: {item.pressure} Voltage {item.voltage}")
        
        print("\n\n\n")

    def pressure_sensor_voltage(self, pressure_sensor: int) -> float:
        return self._pressure_sensors[pressure_sensor].voltage
        
