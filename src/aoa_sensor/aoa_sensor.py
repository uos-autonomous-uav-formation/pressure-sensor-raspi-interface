import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from .pressure_sensor import PressureSensor


class AoaSensor:
    id: int

    def __init__(self, id, spi, chip_select, ref_voltage, 
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
        self.id = id

    def _allocate_pressure_sensor(self, orientation):
        self._pressure_sensors: dict[int, PressureSensor] = {}
        
        for key, item in orientation.items():
            self._pressure_sensors[key] = PressureSensor(self._mcp, item, ref_voltage=self.ref_voltage)

    def dbg(self):
        for key, item in self._pressure_sensors.items():
            print(f"Probe location {key}, Channel {item.channel}, pressure sensor: {item.pressure} Voltage {item.voltage}")
        
        print("\n\n\n")

    def pressure_sensor_voltage(self, pressure_sensor: int) -> float:
        return self._pressure_sensors[pressure_sensor].voltage
    
    def pressure_sensor_dvoltage(self, pressure_sensor: int) -> float:
        return self._pressure_sensors[pressure_sensor].dvoltage

    def pressure_sensor_zero(self, pressure_sensor: int) -> float:
        return self._pressure_sensors[pressure_sensor]._zero

    def aoa_corr_pressure(self, pressure_sensor: int) -> float:
        Vdd = 3.3
        return 525*(np.sign((self._pressure_sensors[pressure_sensor].voltage/Vdd)-0.5))*(((self._pressure_sensors[pressure_sensor].voltage/(Vdd*0.4))-1.25)**2)


    def alpha_aoa1(self, pressure_sensor: int) -> float:    #gives AOA of Angle of attack sensor 1
        p_avg = (self.aoa_corr_pressure(1) + self.aoa_corr_pressure(2) + self.aoa_corr_pressure(3) + self.aoa_corr_pressure(4))/4
        cp_alpha = (self.aoa_corr_pressure(1) - self.aoa_corr_pressure(3)) / (self.aoa_corr_pressure(5) - self.p_avg)
        return (cp_alpha + 0.3630852)/-0.131146 # return aoa 1

    def alpha_aoa2(self, pressure_sensor: int) -> float:  #gives AOA of Angle of attack sensor 2
        p_avg = (self.aoa_corr_pressure(1) + self.aoa_corr_pressure(2) + self.aoa_corr_pressure(
            3) + self.aoa_corr_pressure(4)) / 4
        cp_alpha = (self.aoa_corr_pressure(1) - self.aoa_corr_pressure(3)) / (self.aoa_corr_pressure(5) - self.p_avg)
        return (cp_alpha + 0.1877579) / -0.13755193  # return aoa2







