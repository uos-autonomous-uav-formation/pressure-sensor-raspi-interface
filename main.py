import busio
import board
import argparse
from src.aoa_sensor import AoaSensor
# Create test and debugging hints

REF_VOLTAGE = 5

parser = argparse.ArgumentParser(
    prog="Pressure sensor Raspberry Pi interface"
)
parser.add_argument("-p", "--plot", action="store_true", help="Opens a window to live plot the pressure data")
parser.add_argument("-r", "--record", action="store_true", help="Record data of a single pressure sensor")
args = parser.parse_args()


if args.plot:
    print("Initializing plotting")
    import src.plot.plotter

if args.record:
    from src.datalog.datalog import data_recording

    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    aoa_1 = AoaSensor(spi, board.D7, 3.3)

    data_recording(aoa_1)