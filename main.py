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
args = parser.parse_args()


if args.plot:
    print("Initializing plotting")
    import src.plot.plotter

