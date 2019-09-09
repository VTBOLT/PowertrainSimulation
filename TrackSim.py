import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

MPHoRPM = 0.019337455  # MPH/RPM
MPSoRPM = 0.008644633  # meters/s/RPM
GearRatio = 4
WheelD = 0.6604  # Wheel diameter in meters

CurrentMotor = 120000
NewMotor = 120000
tolerance = 10

# laps = input("Number of laps: ")  # this can be included in csv file in the future if we find that easier

file_name = r'\NJMP6_first4lapstwice.csv'
file_path = r'C:\Users\sesch\Desktop\BOLT\Converted'
location = file_path + file_name

# create DataFrame
data = pd.read_csv(location, names=['time', 'throttle', 'motorRPM', '4', '5', '6'], header=0, low_memory=False)
data_df = pd.DataFrame(data)

# find race start time - needs to be more accurate
start_time = 0
for i in range(0, len(data['time'])):
    if data['5'][i] >= 10:
        start_time = i
        break

# drop unused indexes
data_trimmed = data_df.shift(-start_time)
data_trimmed = data_trimmed.dropna()

# initialize arrays for new speed and distance data
distance = np.ones(len(data_trimmed['time']), np.float64)
speed = np.ones(len(data_trimmed['time']), np.float64)
acceleration = np.ones(len(data_trimmed['time']))
accel_binary = np.ones(len(data_trimmed['time']))

# calculate 'instantaneous' speed
for i in range(start_time):
    speed.put([i], data_trimmed['motorRPM'][i] / 4 / 60 * WheelD * pi)  # speed in meters per second
data_trimmed['speed'] = speed  # add speed column to data frame

# calculate aggregated distance
# calculate 'instantaneous' acceleration
for i in range(0, len(data_trimmed['time'])):
    if i == 0:
        distance.put([0], data_trimmed['speed'][0] * data_trimmed['time'][0] - 1)
        acceleration.put([0], 0)
    else:
        distance.put([i], distance[i-1] + data_trimmed['speed'][i] * (data_trimmed['time'][i] - data_trimmed['time'][i-1]))
        acceleration.put([i], data_trimmed['speed'][i] - data_trimmed['speed'][i-1])
data_trimmed['distance'] = distance  # add distance column to data frame
data_trimmed['acceleration'] = acceleration  # add acceleration column to data frame

for i in range(0, len(data_trimmed['time'])):
    if i == 0:
        accel_binary.put([0], 0)
    else:
        if data_trimmed['speed'][i] > data_trimmed['speed'][i-1]:
            accel_binary.put([i], 1)
        else:
            accel_binary.put([i], 0)
data_trimmed['accel binary'] = accel_binary  # add binary acceleration column to data frame

# binary acceleration (and normal accel) graph is very jittery - this should smooth it out
kernel_size = 2
accel_smooth = np.ones(kernel_size)
for accel in range(0, len(data_trimmed['time'])-kernel_size, kernel_size-1):
    if data_trimmed['accel binary'][accel+kernel_size-1] is not None:
        for i in range(0, kernel_size-1):
            accel_smooth.put([i], data_trimmed['accel binary'][accel+i])
        smoothed = np.mean(accel_smooth)
        if smoothed >= 0.5:
            smoothed = 1
        else:
            smoothed = 0
        for smooth in range(0, kernel_size-1):
            data_trimmed['accel binary'][accel+smooth] = smoothed


print('total distance over given time interval: {}'.format(distance[len(distance)-1]))
print('All data:')
print('{}'.format(data_trimmed))

plt.plot(data_trimmed['time'], data_trimmed['accel binary'])

plt.ylabel('Accel')
plt.xlabel('Time')
plt.show()