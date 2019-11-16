import os
from time import sleep
import datetime as dt
import serial
import struct
from pynput.keyboard import Key, Listener

class SensorData:
    def __init__(self, t, volt):
        self.time = t
        self.voltage = volt

ser = serial.Serial('/dev/ttyACM0', baudrate=9600)
data_collection = "training"

print("Pausing for 2 seconds to wait for stabilizng sensor data");

collect_date = False;

fall_data_collected = []
def on_press(key):
    print('{0} pressed'.format(key))

def on_release(key):
    # print('{0} release'.format(key))
    if key == Key.esc:
        print("Exiting program")
        return False
    if key == key.enter:
        collect_date = not collect_date;
        print("Data collection " + collect_date)

try: 
    print("Press 1 to start reading data and crtl + c to stop")
    while not input() == "1":
        pass
    print("starting to reading data")
    while True: # Run forever
        voltage = ser.readline()
        voltage= voltage.rstrip().decode('utf-8','ignore')
        #print(voltage.count('.'))
        if(len(voltage) == 0 or voltage.count('.') > 1 or float(voltage) > 4):
            continue
        fall_data_collected.append(SensorData( dt.datetime.now().strftime('%H:%M:%S.%f'), float(voltage)))
        #fall_data_collected.append({"time" : dt.datetime.now().strftime('%H:%M:%S.%f'), "voltage" : float(voltage)})
        #print("press 1 to start or stop collecting data")
        #if not collect_date:
        #    pass
        #else :
        #    while collect_date:
        #        fall_data_collected.push({'time' : dt.datetime.now().strftime('%H:%M:%S.%f'), 'voltage' :  ser.readline()})
        #   print(fall_data_collected)
        
            
except KeyboardInterrupt:
    userinp = input("\nto save press 1")
    if(userinp == "1"):
        current_time = dt.datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.csv'
        file = data_collection + os.path.sep + current_time
        with open(file, 'w') as f:
            #f.write("[")
            for item in fall_data_collected:
                print(item.time + "," + str(item.voltage) + "\n")
                #f.write("%s\n" % item)
                f.write(item.time + "," + str(item.voltage) + "\n")
            #f.write("]")
    #print(fall_data_collected)
            
except Exception as e:
    print(e)
finally:
    ser.close()
    pass

# Collect events until released
#with Listener(
        #on_press=on_press,
        #on_release=on_release) as listener:
    #listener.join()