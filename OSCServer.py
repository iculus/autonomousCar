#!/usr/bin/env python3
import getIP
from OSC import OSCServer
import sys
from time import sleep
import numpy as np
import matplotlib.pyplot as plt

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
ax = fig.add_subplot(111)

# some X and Y data
x = np.arange(11)
y = np.random.randn(11)

li, = ax.plot(x, y)

# draw and show it
ax.relim() 
ax.autoscale_view(True,True,True)
#fig.canvas.draw()
plt.show(block=False)

storedData = np.array ([[0]*22], ndmin=1)

def user_callback(path, tags, args, source):
    global storedData
    newInput = np.array([args],ndmin=1)
    storedData = np.append(storedData[-10:,:],np.array([args],ndmin=1),axis=0)
    li.set_ydata(storedData[:,15])
    ax.set_ylim([-100,100])
    fig.canvas.draw()

def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

server.addMsgHandler( "/data", user_callback )
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
