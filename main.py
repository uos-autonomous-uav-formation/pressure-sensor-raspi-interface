import busio
import board
import argparse
from src import AoaSensor
# Create test and debugging hints

REF_VOLTAGE = 5

parser = argparse.ArgumentParser(
    prog="Pressure sensor Raspberry Pi interface"
)
parser.add_argument("-plot", action="store_true", help="Opens a window to live plot the pressure data")
args = parser.parse_args()


if args.plot:
    print("Initializing plotting")

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Note we are not using the assigned GPIOs due to incompatibility with D8
# cs2 = digitalio.DigitalInOut(board.D20) 

aoa_1 = AoaSensor(spi, board.D7, 3.3)

