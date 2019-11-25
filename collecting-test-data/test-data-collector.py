import os
from time import sleep
import datetime as dt
import serial
from timeit import default_timer as timer
from pynput.keyboard import Key, Listener

class SensorData:
    def __init__(self, t, volt):
        self.time = t
        self.voltage = volt

data_collection = "training"

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

def main_data_collection():
    try: 
        #print("Press 1 to start reading data and crtl + c to stop")
        #while not input() == "1":
        #    pass
        print("Pausing for 3 seconds to wait for stabilizng sensor data");
        sleep(3)
        for i in range(0, 10):
            print("starting to reading data in 1 seconds")
            fall_data_collected = []
            sleep(1)
            reading_count = 0;
            start = timer()
            ser = serial.Serial('COM4', baudrate=115200)
            while reading_count < 12000: 
                voltage = ser.readline()
                voltage= voltage.rstrip().decode('utf-8','ignore')
                #print(voltage.count('.'))
                try:
                    voltage = int(voltage)
                    if voltage > 500 or voltage < 100:
                        continue
                    reading_count = reading_count + 1
                    #fall_data_collected.append(SensorData( dt.datetime.now().strftime('%H:%M:%S.%f'), voltage))
                    fall_data_collected.append(str(voltage))
                except ValueError:
                    pass
            end = timer()
            print(end - start)
            #current_time = dt.datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.csv'
            current_time = "fall_5_" + str(i) + ".csv"
            file = data_collection + os.path.sep + current_time
            with open(file, 'w') as f:
                #f.write("[")
                for item in fall_data_collected:
                    #print(item.time + "," + str(item.voltage) + "\n")
                    #f.write("%s\n" % item)
                    #f.write(item.time + "," + str(item.voltage) + "\n")    
                    f.write(str(voltage) + "\n")    
            print("Sleeping for 5 seconds")
            sleep(5)
        ser.close()
            
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


main_data_collection()

# Collect events until released
#with Listener(
        #on_press=on_press,
        #on_release=on_release) as listener:
    #listener.join()