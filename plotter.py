import busio
import board
import numpy as np
from src import AoaSensor
from matplotlib import animation
from matplotlib import pyplot as plt

REF_VOLTAGE = 5


# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

aoa_1 = AoaSensor(spi, board.D7, 3.3)

fig, ax = plt.subplots()

max_x = 200
maxy = 4

x = np.arange(0, max_x)
ax.set_ylim(-2, 2)

data = {}

for i in [1, 2, 3, 4, 5]:
    data[i] = {}
    data[i]["ydata"] = [0] * len(x)
    data[i]["line"], = ax.plot(x, data[i]["ydata"], label=f"Pressure sensor {i}")


def update(a):
    for i in data.keys(): 
        data[i]["ydata"].pop(0)
        data[i]["ydata"].append(aoa_1.pressure_sensor_voltage(i))
        data[i]["line"].set_ydata(data[i]["ydata"])



ani = animation.FuncAnimation(fig, update)

plt.legend()
plt.show()

ani.save("test")