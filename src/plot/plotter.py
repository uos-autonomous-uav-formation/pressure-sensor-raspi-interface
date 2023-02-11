import busio
import board
import numpy as np
from src.aoa_sensor import AoaSensor
from matplotlib import animation
from matplotlib import pyplot as plt

REF_VOLTAGE = 5


# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

aoa_1 = AoaSensor(spi, board.D7, 3.3)

fig, ax = plt.subplots()

max_x = 200

x = np.arange(0, max_x) 
ax.set_ylim(-0.5, 0.5)

data = {}

for i in [1, 2, 3, 4, 5]:
    data[i] = {}
    data[i]["ydata"] = [0] * len(x)
    data[i]["line"], = ax.plot(x, data[i]["ydata"], label=f"Pressure sensor {i}")


def update(a):
    for i in data.keys(): 
        data[i]["ydata"].pop(0)
        data[i]["ydata"].append(aoa_1.pressure_sensor_dvoltage(i))
        data[i]["line"].set_ydata(data[i]["ydata"])



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
