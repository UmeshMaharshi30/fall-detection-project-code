import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from time import sleep
import serial

ser = serial.Serial('/dev/ttyACM0', baudrate=9600)

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

sleep(2)

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    # fetching data from sensor via arduino via serial/usb
    voltage = ser.readline()
    print(voltage)
    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(voltage)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Sensor data over Time')
    plt.ylabel('Voltage v')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1)
plt.show()
