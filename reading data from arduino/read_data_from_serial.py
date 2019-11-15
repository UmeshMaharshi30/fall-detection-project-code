from time import sleep
import serial

ser = serial.Serial('/dev/ttyACM0', baudrate=9600)

sleep(2)

try: 
    print("Starting to read data from serial")
    while True: # Run forever
        data = ser.readline()
        print(data)
        
            
            
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    print("Exiting program")
except Exception as e:
    print(e)
finally:
    ser.close()
    pass