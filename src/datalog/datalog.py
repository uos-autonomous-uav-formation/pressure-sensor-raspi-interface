import busio
import board
import numpy as np
from src.aoa_sensor import AoaSensor
import time

REF_VOLTAGE = 5
TIME_TO_AVERAGE = -1 # Time to do time averaging for in seconds (it considers a precision in nanoseconds)
NUM_RECORDS = 1000 # Number of datapoitns to record


class SingleRecord:
    sum: float = 0.0
    num: int = 0
    zero: int = 0

    def average(self) -> float:
        return self.sum/self.num
    
    def __str__(self):
        return f"{self.average()},{self.num},{self.zero}"
    

def __record_single(aoa_sensor: AoaSensor, command: str, number_identified: int | None):
    data: dict[int, SingleRecord] = {k: SingleRecord() for k in [1, 2, 3, 4, 5]}
    t_start = time.time_ns()

    while True:
        for key, record in data.items():
            record.num += 1
            record.sum += aoa_sensor.pressure_sensor_dvoltage(key)
            record.zero = aoa_sensor.pressure_sensor_zero(key)


        if time.time_ns() - t_start > TIME_TO_AVERAGE*1e9:
            break

    with open("output.csv", "a") as file:
        file.write(f"{command},{number_identified}," + 
                    ",".join([str(data[i].__str__()) for i in [1, 2, 3, 4, 5]]) + 
                    f",\n")


def __record_data(aoa_sensor: AoaSensor, command: str, iter: int):
    
    for i in range(0, iter):
        __record_single(aoa_sensor, command, i)
        time.sleep(0.01)

def data_recording(aoa_sensor: AoaSensor):

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
            __record_data(aoa_sensor, command, iter)
