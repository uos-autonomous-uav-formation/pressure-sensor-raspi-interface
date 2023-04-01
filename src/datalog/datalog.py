import numpy as np
from src.aoa_sensor import AoaSensor
import time

REF_VOLTAGE = 5
NUM_RECORDS = 1000 # Number of datapoitns to record
    

def __record_single(aoa_sensor: AoaSensor, command: str, number_identified: int):
    data: dict[int, float] = {k: 0.0 for k in [1, 2, 3, 4, 5]}

    for key, value in data.items():
        data[key] = aoa_sensor.pressure_sensor_dvoltage(key)

    with open("output.csv", "a") as file:
        file.write(f"{command},{aoa_sensor.id},{number_identified}," + 
                    ",".join([f"{data[i]},{aoa_sensor.pressure_sensor_zero(i)}" for i in [1, 2, 3, 4, 5]]) + 
                    f",\n")


def __record_data(aoa_sensors: list[AoaSensor], command: str, iter: int):
    
    for i in range(0, iter):
        for sensor in aoa_sensors:
            __record_single(sensor, command, i)
        time.sleep(0.005)

def data_recording(aoa_sensors: list[AoaSensor]):

    while True:
        command = input("Write command (h for help):")

        if command == "q":
            break

        elif command == "h":
            print("Use q to exit")
            print("Use h for help")
            print("Write anything else as the tag to store data for")

        else:
            iter = int(input("Number of datapoints"))
            print()
            __record_data(aoa_sensors, command, iter)
