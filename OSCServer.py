#/usr/bin/env python3
import pickle as pickle
import getIP
from OSC import OSCServer, OSCClient
import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime

year = datetime.datetime.now().strftime("%y")
month = datetime.datetime.now().strftime("%m")
day = datetime.datetime.now().strftime("%d")
hour = datetime.datetime.now().strftime("%H")
minute = datetime.datetime.now().strftime("%M")
secs = datetime.datetime.now().strftime("%S")
filename = year+'-'+month+'-'+day+'-'+hour+'-'+minute+'-'+secs+'-'+"save.p"

myIPwlan0 = getIP.get_ip_address("wlan0")

server = OSCServer( (myIPwlan0, 7110) )
server.timeout = 0
run = True

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is 
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
import types
server.handle_timeout = types.MethodType(handle_timeout, server)

fig = plt.figure()
ax = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

# some X and Y data
x = np.arange(11)
y = np.random.randn(11)

li, = ax.plot(x, y)
li2, = ax2.plot(x, y)
li3, = ax3.plot(x, y)

# draw and show it
ax.relim() 
ax2.relim() 
ax3.relim() 
ax.autoscale_view(True,True,True)
ax2.autoscale_view(True,True,True)
ax3.autoscale_view(True,True,True)

yScaleMin = -40
yScaleMax = 40

ax.set_ylim([yScaleMin,yScaleMax])
ax2.set_ylim([yScaleMin,yScaleMax])
ax3.set_ylim([yScaleMin,yScaleMax])
#fig.canvas.draw()
plt.show(block=False)

storedData = np.array ([[0]*22], ndmin=1)

def user_callback(path, tags, args, source):
	pickle.dump( args , open(filename, "ab"))
	global storedData
	newInput = np.array([args],ndmin=1)
	storedData = np.append(storedData[-10:,:],np.array([args],ndmin=1),axis=0)
	#print len(storedData[:,16]), len(x)
	#if len(storedData[:,16]) == len(x):
	#    li.set_ydata(storedData[:,16])
	#    li2.set_ydata(storedData[:,17])
	#    li3.set_ydata(storedData[:,18])
	#    fig.canvas.draw()

def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

def user_display(path, tags, args, source):
	print args

server.addMsgHandler( "/data", user_callback )
server.addMsgHandler( "/event", user_display )
server.addMsgHandler( "/quit", quit_callback )

# user script that's called by the game engine every frame
def each_frame():
    # clear timed_out flag
    server.timed_out = False
    # handle all pending requests then return
    while not server.timed_out:
        server.handle_request()

# simulate a "game engine"
while run:
    each_frame()

server.close()
