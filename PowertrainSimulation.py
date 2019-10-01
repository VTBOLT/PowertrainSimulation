"""
This document is going to become the main scrip that will analyze a powertrain.
This will likely need to be imported as if it were a library so parameters can be passed in. As a result, this script
will not be able to run by itself.
"""


# add motor/motor controller compatibility check?

def main(data_frame, max_torque, max_rpm_max_torque, min_torque, max_rpm, motor_mass, mc_mass, pack_cap_kwh,
         data_stripper, powertrain_id):
    import numpy as np
    import pandas as pd
    import math
    import os

    inputStrip = input("Enter a value for data stripper > 0 or type 'n' to use default")
    if inputStrip != 'n':
        data_stripper = inputStrip

    location = os.path.abspath(
        'OriginalBikeModelFiles\\EditedBOLT3Data.csv')  # csv file trimmed to only when the bike is racing

    # create DataFrame
    data = pd.read_csv(location, names=['time start', 'high low', 'distances', 'final speed'], header=0,
                       low_memory=False)
    data_df = pd.DataFrame(data)

    # Traction control for beginning of race
    #   extra weight from rider makes center of mass near 0.49-0.48L (L is distance between centers of wheels)
    # Traction control for rest of race
    #   rider moves forward so center of mass near .5L

    GearRatio = 4
    WheelR = 0.3302  # Wheel radius in meters
    BikeM = 200  # mass input from optimization program in kgs

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

    segment_times = np.zeros(data_df.shape[0])

    for i in range(0, data_df.shape[0]):
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

    print("Total time for powertrain {} is {}".format(powertrain_id, total_time))
    return total_time


main()
