import busio
import board
import numpy as np
from src.aoa_sensor import AoaSensor
from matplotlib import animation
from matplotlib import pyplot as plt

REF_VOLTAGE = 5


# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

aoa = [AoaSensor(0, spi, board.D7, 5), AoaSensor(1, spi, board.D20, 5)]

fig, ax = plt.subplots(ncols=2)

max_x = 200

x = np.arange(0, max_x) 
ax[0].set_ylim(0, 3.3)
ax[1].set_ylim(0, 3.3)


data = {}

for aoa_sensor in aoa:
    data[aoa_sensor.id] = {}
    for i in [1, 2, 3, 4, 5]:
        data[aoa_sensor.id][i] = {}
        data[aoa_sensor.id][i]["ydata"] = [0] * len(x)
        ax[aoa_sensor.id].set_title(f"for aoa {aoa_sensor.id}")
        data[aoa_sensor.id][i]["line"], = ax[aoa_sensor.id].plot(x, data[aoa_sensor.id][i]["ydata"], label=f"Pressure sensor {i}")


def update(a):
    for aoa_sensor in aoa:
        for i in data[aoa_sensor.id].keys():
            data[aoa_sensor.id][i]["ydata"].pop(0)
            data[aoa_sensor.id][i]["ydata"].append(aoa_sensor.pressure_sensor_voltage(i))
            data[aoa_sensor.id][i]["line"].set_ydata(data[aoa_sensor.id][i]["ydata"])



ani = animation.FuncAnimation(fig, update)

plt.xlabel("data point")
plt.ylabel("Voltage (V)")
plt.legend()
plt.show()


# The following is for the animation to live long enough, it will cause an exception but this is on purpose.
# In theory plt.show() should handle this lifetime but it is not doing so.
try:
    ani.save("test.mp3")

except ValueError:
    pass

except Exception as e:
    print(e)
