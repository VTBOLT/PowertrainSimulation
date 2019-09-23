"""
This document is going to become the main scrip that will analyze a powertrain.
This will likely need to be imported as if it were a library so parameters can be passed in. As a result, this script
will not be able to run by itself.
"""


def main(data_frame, max_torque, max_rpm_of_max_torque, max_rpm, mass, pack_capacity_kWh, data_stripper):
    import numpy as np
    import pandas as pd
    import math
    import os

    #input data stripper variable to speed up program if desired

    # minimum inputs to calculate accel (I think): motor max torque and total bike mass

    GearRatio = 4
    WheelR = 0.3302  # Wheel diameter in nanometers
    BikeM = 200  # mass input from optimization program in kgs
    max_torque = 240  # max torque of bike motor in N*m

    location = os.path.abspath('CSVFiles\\EditedBOLT3Data.csv')  # csv file trimmed to only when the bike is racing

    # create DataFrame
    data = pd.read_csv(location, names=['time start', 'high low', 'distances', 'final speed'], header=0, low_memory=False)
    data_df = pd.DataFrame(data)

    # torque curve
    # input max rpm, power, and max torque
    # make torque curve
    # Make list of RPMs at each moment in time for each segment.
    # Make equation for acceleration.
    # Find velocity at each time point.
    # Calculate distance traveled.
    # If traveled enough distance, break.

    # torque = torque wheel = torque shaft * 4
    # f*r = torque
    # torque / r = f
    # f = m * a
    # torque_shaft * 4 / r / m = a

    max_accel = max_torque * GearRatio / WheelR / BikeM  # Some scaling factors definitely need to be added to this
    powertrain_ID = 1  # some input from Kristen's program to organize different powertrains?

    segment_times = np.zeros((len(data_df['time start'])))

    for i in range(0, len(data_df['time start'])):
        if i % 2 is 1:  # segments bike is braking
            time = (2 * data_df['distances'][i]) / (data_df['final speed'][i] + data_df['final speed'][i - 1])
            segment_times.put([i], time)
        else:  # segments bike is accelerating
            if i is 0:
                det = 2 * max_accel * data_df['distances'][i]
                time = math.sqrt(det) / max_accel
                segment_times.put([i], time)
            else:
                det = pow(data_df['final speed'][i - 1], 2) + 2 * max_accel * data_df['distances'][i]
                time = (math.sqrt(det) - data_df['final speed'][i - 1]) / max_accel
                segment_times.put([i], time)

    total_time = np.sum(segment_times)

    print("Total time for powertrain {} is {}".format(powertrain_ID, total_time))


main()
