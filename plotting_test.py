import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import serial
import struct


#initialize serial port
ser=serial.Serial(port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
    )
FSR=24.576

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [] #store trials here (n)
ys = [] #store relative frequency here
rs = [] #for theoretical probability
i=0

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    s=ser.readline()
    if s[0:9]=="Received:":
        x=struct.unpack('>H'*(len(s[9:11])//2),s[9:11])
        voltage=(x[0]*375.0/1000000)-FSR/2
        i=i+1
        #print(voltage)
        #print(i)
	
	# Add x and y to lists
        if i>30:
            xs.remove(xs[0])
            ys.remove(ys[0])

        xs.append(i)
        ys.append(voltage)

    # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys, label="test")
   
    # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.axis([xs[0], None, -3, 3]) #Use for arbitrary number of trials
    #plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs,ys), interval=30)
plt.show()