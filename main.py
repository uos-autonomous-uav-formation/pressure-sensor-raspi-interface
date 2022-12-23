import busio
import digitalio
import board
import time
from src.pressure_sensor import PressureSensor
# Create test and debugging hints

REF_VOLTAGE = 5


# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs1 = digitalio.DigitalInOut(board.D7)
cs2 = digitalio.DigitalInOut(board.D20) # Note we are not using the assigned GPIOs due to incompatibility with D8

# create the mcp object
mcp1 = MCP.MCP3008(spi, cs1, ref_voltage=REF_VOLTAGE)
mcp2 = MCP.MCP3008(spi, cs2, ref_voltage=REF_VOLTAGE)

# create an analog input channel on pin 0
channels1 = {
    0: {"mcp": MCP.P0},
    1: {"mcp": MCP.P1},
    2: {"mcp": MCP.P2},
    3: {"mcp": MCP.P3},
}

for i in channels1.keys():
    channels1[i]["input"] = AnalogIn(mcp1, channels1[i]["mcp"])

while True:
    time.sleep(0.5)

    for i in channels1.keys():
        temp_vals = 0

        for t in range(0, 100):
            temp_vals += channels1[i]["input"].voltage
        print(f'ADC Voltage in {i}: {str(temp_vals/100)}')

    print(" \n\n\n")