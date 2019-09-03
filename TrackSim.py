import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

MPHoRPM = 0.019337455
MPSoRPM = 0.008644633
GearRatio = 4

CurrentMotor = 120000
NewMotor = 120000
tolerance = 10

laps = input("Number of laps: ") # this can be included in csv file in the future if we find that easier

file_name = r'\NJMP6_first4lapstwice.csv'
file_path = r'C:\Users\sesch\Desktop\BOLT\Converted'
location = file_path + file_name

data = pd.read_csv(location, names=['time', 'throttle', 'motorRPM', '4', '5', '6'], header=0, low_memory=False)
data_df = pd.DataFrame(data)

speed = np.empty(2)

print(len(data['time']))

for i in range(0, len(data['time']-1)):
    speed = np.append(data['motorRPM'][i]/4, axis=0)[i] # add bike speed to array for every time instance
print(len(speed))
print(speed)
data['speed'] = speed # add new column to dataframe
"""
time_offset = []
for t in range(0, len(data)):
    if data['pack_current'][t] >= 10:
        start_time = t
        break
# print(len(data))
plt.plot(data['time'], data['pack_current'])

plt.ylabel('Pack Current')
plt.xlabel('Time')
plt.show()
"""