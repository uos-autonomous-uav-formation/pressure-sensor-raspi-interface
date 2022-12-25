import busio
import digitalio
import board
import time
from src import AoaSensor
# Create test and debugging hints

REF_VOLTAGE = 5


# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Note we are not using the assigned GPIOs due to incompatibility with D8
# cs2 = digitalio.DigitalInOut(board.D20) 

aoa_1 = AoaSensor(spi, board.D7, 5)

while True:
    time.sleep(0.5)
    aoa_1.dbg()
