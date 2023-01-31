import busio
import board
import numpy as np
from src.aoa_sensor import AoaSensor
import time



REF_VOLTAGE = 5
RECORD_TIME = 30 # in seconds

class SingleRecord:
    sum: float = 0.0
    num: int = 0

    def average(self) -> float:
        return self.sum/self.num
    

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
            data: dict[int, SingleRecord] = {k: SingleRecord() for k in [1, 2, 3, 4, 5]}
            t_start = time.time()

            while True:
                for key, record in data.items():
                    record.num += 1
                    record.sum += aoa_sensor.pressure_sensor_dvoltage(key)


                if time.time() - t_start > RECORD_TIME:
                    break

            with open("output.csv", "a") as file:
                file.write(f"{command}," + ",".join([str(data[i].average()) for i in [1, 2, 3, 4, 5]]) + "\n")
