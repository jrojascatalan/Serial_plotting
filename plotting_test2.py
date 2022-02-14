import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import serial
import struct
import time

#initialize serial port
ser=serial.Serial(port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
    )
FSR=24.576
plt.ion()

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [] #store trials here (n)
ys = [] #store relative frequency here
rs = [] #for theoretical probability
i=0
n=0
line1,=ax.plot(xs, ys, 'b-')
fig.canvas.draw() 
axbackground = fig.canvas.copy_from_bbox(ax.bbox)

plt.show(block=False)
t_start = time.time()
text = ax.text(0.8,0.5, "")
# This function is called periodically from FuncAnimation
for j in np.arange(1000):

    while n<150:
        s=ser.readline()
   
        if s[0:9]=="Received:":
            x=struct.unpack('>H'*(len(s[9:11])//2),s[9:11])
            voltage=(x[0]*375.0/1000000)-FSR/2
            i=i+1
            xs.append(i)
            ys.append(voltage)
            n=n+1
            
    n=0
    tx = 'Mean Frame Rate:\n {fps:.3f}FPS'.format(fps= ((j+1) / (time.time() - t_start)) )
    print(((j+1) / (time.time() - t_start)) )
    text.set_text(tx) 
    ax.clear()
    ax.plot(xs, ys, label="test")
    line1.set_xdata(xs)
    line1.set_ydata(ys)
    plt.axis([xs[0], None, -3, 3])

    fig.canvas.draw()
    #fig.canvas.restore_region(axbackground)
    ax.draw_artist(text)
    fig.canvas.blit(ax.bbox)

    fig.canvas.flush_events()
    xs=[]
    ys=[]
    # Draw x and y lists
       # ax.clear()
       # ax.plot(xs, ys, label="test")
   
  #plt.show()