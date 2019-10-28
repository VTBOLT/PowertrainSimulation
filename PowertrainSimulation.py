"""
This document is going to become the main scrip that will analyze a powertrain.
This will likely need to be imported as if it were a library so parameters can be passed in. As a result, this script
will not be able to run by itself.
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import OriginalBikeModel as obike

ampHoursPerCell = 2.6  # amp hours for one 18650
voltsPerCell = 4.2  # fully charged 18650
allBattConfigs = False


def main(data_df, specs, data_stripper, pTrainID, series, parallel):

    max_torque = specs[0]
    max_rpm_max_torque = specs[1]
    min_torque = specs[2]
    max_overall_rpm = specs[3]
    motor_mass = specs[4]
    motor_loss = specs[5]
    rated_power = specs[6]
    mc_mass = specs[7]
    mc_loss = specs[8]
    series = specs[9]
    parallel = specs[10]
    pack_loss = specs[11]

    lossCoeff = pack_loss + mc_loss + motor_loss

    def kw_race(rated_power, raceTime):
        kw_race = rated_power * raceTime * 3600  # race time must be in hours
        return kw_race

    def power_loss(totalPackkWh, lossCoeff, raceTime):
        losskWh = lossCoeff * totalPackkWh / (raceTime * 3600)  # calculates kWh losses based on known loss coefficient. Change race time from seconds to hours.
        return losskWh

    def pack_specs(parallel, series):
        totAmpHours = parallel * ampHoursPerCell
        voltage = series * voltsPerCell
        kWhs = voltage * totAmpHours  # in kWs
        return kWhs

    def can_finish(kWh, kW, completionTime):
        finish = False
        if kWh / kW * 3600 > completionTime:  # times measured in seconds
            finish = True
        return finish

    def get_race_time(data_stripper, data_df):
        segDist = 0
        totTime = 0
        timeInt = .01 * data_stripper  # Set time intervals for acceleration microSegments
        accelSpeeds = np.zeros(data_df.shape[0] + 1)  # array for final speeds of acceleration segments
        accelSpeeds[0] = 0

        for i in range(0, data_df['distances'].shape[0]):
            if i % 2 is 1:  # Segments bike is braking
                # Time taken to complete one segment
                segTime = (2 * data_df['distances'][i]) / abs(
                    accelSpeeds[i] - data_df['final speed'][i + 1])  # difference in speed during brake
                totTime = totTime + segTime
                accelSpeeds[i + 1] = 0  # pad array so it lines up properly with final speeds for each segment
            elif i % 2 is 0:  # segments bike is accelerating
                if i is 0:
                    start_speed = 0
                else:
                    start_speed = data_df['final speed'][i - 1]

                microSeg = 0
                while segDist < data_df['distances'][i]:
                    this_accel = get_accel(start_speed)  # Get acceleration based on current speed
                    microSegDist = start_speed * timeInt + 0.5 * this_accel * timeInt * timeInt  # Distance of this micro segment

                    # Final speed of this micro segment, which is also the start_speed for the next micro segment
                    start_speed = timeInt * this_accel + start_speed

                    # Add this interval's distance to the segment's distance
                    segDist = segDist + microSegDist
                    microSeg = microSeg + 1
                accelSpeeds[i + 1] = start_speed
                segTime = microSeg * timeInt  # How long it took to travel this segment
                totTime = totTime + segTime
        return totTime

    def get_accel(current_speed):
        # calculate RPM from speed
        current_RPM = current_speed / (wheel_r * 2 * math.pi) * 60

        # find accel for that RPM
        if current_RPM < max_rpm_max_torque / (increment * data_stripper):
            # Flat slope for torque curve
            accel = max_a
        else:
            # Slope of torque curve
            accel = (torque_slope * current_RPM + torque_b) * t_to_a
        return accel

    # if series is 0 or parallel is 0:  # indicates that user wants to run through all pack configurations
    #   allBattConfigs = True  # otherwise, use user's given configuration and don't loop through all possibilities
    # else:
    kWh = pack_specs(series, parallel)  # change to kWh

    def get_accel(current_speed):
        # calculate RPM from speed
        current_RPM = current_speed / (wheel_r * 2 * math.pi) * 60

        # find accel for that RPM
        if current_RPM < max_rpm_max_torque / (increment * data_stripper):
            # Flat slope for torque curve
            accel = max_a
        else:
            # Slope of torque curve
            accel = (torque_slope * current_RPM + torque_b) * t_to_a
        return accel

    # BOLT4 ratio and wheel radius
    gear_ratio = 4
    wheel_r = 0.3302  # Wheel radius in meters
    bike_mass = 200  # Mass of bike without any of the input components

    # Add mass of each different pack type
    total_mass = bike_mass + motor_mass + mc_mass

    # Equation for max acceleration
    max_accel = max_torque * gear_ratio / wheel_r / total_mass  # Some scaling factors definitely need to be added to this

    # Use equation for max acceleration to find proportion of torque to acceleration for the acceleration curve
    t_to_a = 4/(total_mass * wheel_r)

    # Make m and b values for y=mx+b
    torque_slope = (max_torque - min_torque) / (max_rpm_max_torque - max_overall_rpm)
    torque_b = max_torque - (torque_slope * max_rpm_max_torque)

    # Define max possible accel
    max_a = max_torque * t_to_a

    # Making torque curve for specific powertrain setup (this is only useful if you want to see how the curve looks)
    increment = 0.1

    # A few assumptions
    min_torque = 0
    min_rpm = 0

    # the six pairs of points required to create the simplified torque curve
    accels = np.array([t_to_a * max_torque, t_to_a * max_torque, min_torque])
    motorRPMs = np.array([min_rpm, max_rpm_max_torque, max_overall_rpm])

    plt.plot(motorRPMs, accels)
    plt.ylabel("Accel (m/s^2)")
    plt.xlabel("Motor RPM")
    plt.show()

    totTime = get_race_time(data_stripper, data_df)

    print("Total time for powertrain {} is {}".format(pTrainID, totTime))
    kWRace = kw_race(kWh, totTime)
    canFinish = can_finish(kWh, kWRace, totTime)
    powerLoss = power_loss(kWh, lossCoeff, totTime)
    return totTime, pTrainID, canFinish, powerLoss



if __name__ == '__main__':
    main()
