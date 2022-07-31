#----------------- DEPENDENCIES ------------------#
import serial
from time import sleep, time
import pandas as pd
import numpy as np
import os
#------------------------------------------------#

#----------------- FUNCTIONS ------------------#


def port_auto_detect():
    import warnings
    import serial
    import serial.tools.list_ports
    ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'CP2102' in p.description  # may need tweaking to match arduino
    ]
    if not ports:
        raise IOError("No Device found!")
    if len(ports) > 1:
        warnings.warn('Multiple Device found - using the first')
    return ports[0]


def compile_data(data, columnArray, label, path=''):
    df = pd.DataFrame(data, columns=columnArray)
    df.to_csv(path + label + '.csv', index=False)
    print("\nData Writing Done... shape: ", df.shape)
#-----------------------------------------------#


#------------------ SETTINGS -------------------#
columnName = ['timestamp', 'user_id',
              'flex_1', 'flex_2', 'flex_3', 'flex_4', 'flex_5',
              'Qw', 'Qx', 'Qy', 'Qz',
              'GYRx', 'GYRy', 'GYRz',
              'ACCx', 'ACCy', 'ACCz',
              'ACCx_body', 'ACCy_body', 'ACCz_body',
              'ACCx_world', 'ACCy_world', 'ACCz_world']

data = []

user_id = '007'  # input("Enter User ID: ")
gestureName = input("Enter Gesture Name: ").lower()
recorditeration = 10
segmentLength = 150
# try:
#     recorditeration = int(input("Enter #iteration_per_gesture: "))
# except ValueError:
#     print("#iteration_per_gesture must be an integer and greater than zero.")
# try:
#     segmentLength = int(input("Enter #datapoint_per_iteration: "))
# except ValueError:
#     print("#datapoint_per_iteration must be an integer and greater than zero.")

# Make a directory named 'Channels' in the 'storePath' if there is none already\n",
currentPath = os.getcwd()
store_path = os.path.join(currentPath, "data", user_id)
if not os.path.isdir(store_path):
    os.makedirs(store_path)

port = port_auto_detect()
# port = '/dev/ttyUSB0'
ser = serial.Serial(port=port,
                    baudrate=230400,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1,
                    xonxoff=0,
                    rtscts=0)

print("\nEstablishing Communication... Please Wait")

ser.dtr = False
sleep(1)
ser.reset_input_buffer()
ser.dtr = True
sleep(1)

#-------------------------------------------------#
#
#------------------ ITERATION SETTINGS -------------------#


count = 0
recordData = True
interruptToken = False
current_time = time()
prev_time = current_time
T = np.zeros(segmentLength, dtype=float)

#-------------------------------------------------#
#
#------------------ INITIALIZATION -------------------#


print("\nInitializing MPU6050 in ..", end='')

while True:
    try:
        ser.readline().decode('utf-8').rstrip().split(',')
        break
    except(ValueError):
        print('.')
val_discard = 500
for i in range(val_discard):
    values = ser.readline().decode('utf-8').rstrip().split(',')
    if (i % 100) == 0:
        print(int((val_discard-i) / 100))
print('\n')

#-------------------------------------------------#
#
#------------------ MAIN ITERATIONS -------------------#


while True:
    try:
        current_time = time()
        values = ser.readline().decode('utf-8').rstrip().split(',')
        values = list(map(float, values))
        values.insert(0, current_time)
        values.insert(1, user_id)
        print(values)

        # if(recordData == True):
        #     interruptToken = False
        #     data.append(values)
        #     print("\nData Received... index: ", len(data)-1, end='')
        #     T[(len(data)-1) % segmentLength] = current_time

        # if ((len(data) % segmentLength) == 0) and (recordData == True) and (interruptToken == False):
        #     if recordData == True:
        #         recordData = False
        #         interruptToken = True
        #         count += 1
        #         print('\tSegment - ', count, ' finished')
        #         f_s = 1 / np.diff(T)
        #         f_s = np.delete(f_s, 0)
        #         print('\nSampling Frequency:\t\tMean = {:.2f}Hz  |  Max = {:.2f}Hz  |  Min = {:.2f}Hz'.format(
        #             f_s.mean(), f_s.max(), f_s.min()))
        #     if count >= recorditeration:
        #         df = pd.DataFrame(data, columns=columnName)
        #         df.to_csv(store_path + '/' + gestureName + '.csv', index=False)
        #         print("\nData Writing Done... shape: ", df.shape)
        #         break

    # except(KeyboardInterrupt):
    #     if recordData == False:
    #         print("\n\nStart")
    #         ser.readline().decode('utf-8').rstrip().split(',')
    #         recordData = True

    except(ValueError):
        print(end='.')

    except Exception as e:
        print(e)
    # except:
    #     print("Something's Wrong... CHECK!!!")
