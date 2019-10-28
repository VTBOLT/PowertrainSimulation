"""
This program will ask for a csv of powertrain components to input and run them through PowertrainSimulation.py
"""

import numpy as np
import pandas as pd
import OriginalBikeModel as obike
import PowertrainSimulation as psim
import os


def main():
    # Create csv for all components with their specs then add to abspath line.
    # Create data frame with every possible combination of specs.
    # Call OriginalBikeModel.py to get data from bolt 3
    # Call PowertrainSimulation.py with inputs as bolt 3 data frame and data in a row from
    # data frame of every possible combination corresponding to the ID of the powertrain being simulated.
    # data_frame, max_torque, max_rpm_of_max_torque, max_rpm, mass, pack_capacity_kWh, data_stripper

    # create dataframes
    locationkWhs = os.path.abspath('Component Inputs\\pack.csv')
    locationMCs = os.path.abspath('Component Inputs\\motor controllers.csv')
    locationMotors = os.path.abspath('Component Inputs\\motors.csv')

    datakWhs = pd.read_csv(locationkWhs, names=['series', 'parallel', 'pack loss'], header=0, low_memory=False)
    dataMCs = pd.read_csv(locationMCs, names=['MCmass', 'mc loss'], header=0, low_memory=False)
    dataMotors = pd.read_csv(locationMotors, names=['max torque', 'max rpm max torque', 'rpm min torque',
                                                    'mass', ' motor loss', 'rated power'], header=0, low_memory=False)

    df_kWhs = pd.DataFrame(datakWhs)
    df_MCs = pd.DataFrame(dataMCs)
    df_Motors = pd.DataFrame(dataMotors)

    numkWh = datakWhs.shape[0]
    numMCs = dataMCs.shape[0]
    numMotors = dataMotors.shape[0]

    numperms = numkWh * numMCs * numMotors

    # arrays to store number of each type of component for use in permuting through combinations
    kWhs = np.zeros(numperms)
    mcs = np.zeros(numperms)
    motors = np.zeros(numperms)

    # initialize dataframe for every possible combination of components
    combinations_df = pd.DataFrame(columns=['motors', 'MCs', 'kWh'])

    kWhData_df = pd.DataFrame(index=range(0, numperms), columns=['kWh', 'pack loss'])
    mcData_df = pd.DataFrame(index=range(0, numperms), columns=['MCmass', 'mc loss'])
    motorData_df = pd.DataFrame(index=range(0, numperms), columns={'max torque', 'max rpm max torque', 'min torque',
                                                                   'rpm min torque', 'mass', 'motor loss'})

    # permute through combinations and add to data frame
    motorSeg = int(numperms / numMotors)
    mcSeg = int(motorSeg / numMCs)
    kWhSeg = int(mcSeg / numkWh)

    for i in range(0, numMotors):
        for n in range(0, motorSeg):
            motors[n + i * motorSeg] = i

    for k in range(0, numMotors):
        for i in range(0, numMCs):
            for n in range(0, mcSeg):
                mcs[n + i * mcSeg + k * motorSeg] = i

    for l in range(0, numMotors):
        for k in range(0, numMCs):
            for i in range(0, numkWh):
                for n in range(0, kWhSeg):
                    kWhs[n + i * kWhSeg + k * mcSeg + l * motorSeg] = i

    combinations_df['motors'] = motors
    combinations_df['MCs'] = mcs
    combinations_df['kWh'] = kWhs

    specs_df = pd.DataFrame()  # create data frame to combine everything in

    # replace names with list of specs (eg. all motor 1s become [130,7000,20,8000,8]
    for i in range(0, numperms):
        n = int(combinations_df.iloc[i][0])
        motorData_df.iloc[i] = df_Motors.iloc[n]

        n = int(combinations_df.iloc[i][1])
        mcData_df.iloc[i] = df_MCs.iloc[n]

        n = int(combinations_df.iloc[i][2])
        kWhData_df.iloc[i] = df_kWhs.iloc[n]

    specs_df_data = pd.concat([specs_df, motorData_df, mcData_df, kWhData_df], axis=1)

    bolt3_df = obike.main()  # call OriginalBikeModel.py

    # instantiate arrays to fill with PowertrainSimulation.py output
    times = np.zeros(specs_df.shape[0])
    ptrainIDs = np.zeros(specs_df.shape[0])
    finish = np.zeros(specs_df.shape[0])
    powerLoss = np.zeros(specs_df.shape[0])

    inputStrip = input("Enter a value for data stripper > 1 or type 'n' to use default")
    if inputStrip != 'n':
        if inputStrip < '1':
            inputStrip = 1
        data_stripper = inputStrip
    else:
        data_stripper = 1

    # giveBattConfig = input("Enter 'y' to input your own number of series and parallel batteries. Enter 'n' to calculate every possible combination of series and parallel (this takes a long time)")
    # if giveBattConfig != 'n':
    parallel, series = input("Enter number of batteries in parallel and number of super cells in series.")
    # else:
    #    series = 0
    #    parallel = 0

    # returns time of completion, ID, and whether the pack config will allow it to finish the race
    for i in range(0, specs_df.shape[0]):
        times[i], ptrainIDs[i], finish[i], powerLoss[i] = psim.main(bolt3_df, specs_df.iloc[i], data_stripper, i, series, parallel)  # call PowertrainSimulation.py



if __name__ == '__main__':
    main()
