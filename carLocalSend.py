import pickle as pickle
import datetime
import logging
import sys
import time
from OSC import OSCClient, OSCMessage, OSCServer
from Adafruit_BNO055 import BNO055
import pygame as pg
import os


def play_music(music_file):
	'''
	stream music with mixer.music module in blocking manner
	this will stream the sound from disk while playing
	'''
	clock = pg.time.Clock()
	try: 
		pg.mixer.music.load(music_file)
		print("Music file {} loaded!".format(music_file))
	except pygame.error:
		print("File {} not found! {}".format(music_file, pg.get_error()))
		#return

	print music_file
	pg.mixer.music.play()

	# for x in range(0,100):
	#     pg.mixer.music.set_volume(float(x)/100.0)
	#     time.sleep(.0075)
	# # check if playback has finished
	while pg.mixer.music.get_busy():
		clock.tick(30)


freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 2048   # number of samples (experiment to get right sound)
pg.mixer.init(freq, bitsize, channels, buffer)
# optional volume 0 to 1.0
pg.mixer.music.set_volume(1.0)

mp3s = []
for file in os.listdir("/home/pi/AdamsCar"):
	if file.endswith(".mp3"):
		file = '/home/pi/AdamsCar/' + file
		print file
		mp3s.append(file)


run = True

client = OSCClient()
client.connect( ("192.168.42.11", 7110) )

#bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=17)
bno = BNO055.BNO055(serial_port='/dev/ttyS0', rst=17)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
	logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
	raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
	print('System error: {0}'.format(error))
	print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

print('Reading BNO055 data, press Ctrl-C to quit...')

year = datetime.datetime.now().strftime("%y")
month = datetime.datetime.now().strftime("%m")
day = datetime.datetime.now().strftime("%d")
hour = datetime.datetime.now().strftime("%H")
minute = datetime.datetime.now().strftime("%M")
secs = datetime.datetime.now().strftime("%S")
filename = year+'-'+month+'-'+day+'-'+hour+'-'+minute+'-'+secs+'-'+"save.p"

def checkThresh(arrayOfInterest, threshold, name, wait, orig):
	if abs (arrayOfInterest) > threshold and wait == False:
		print name, arrayOfInterest
		event = (name, arrayOfInterest)
		global timerDelay
		try: client.send( OSCMessage ("/event",event) )
		except: pass
		for x in mp3s:
			try: play_music(x) 
			except: pass
		return True, time.time()
	else:
		return wait, orig

timerDelay = True
import time
timeThen = time.time()
while run:
	# Read the Euler angles for heading, roll, pitch (all in degrees).
	heading, roll, pitch = bno.read_euler()
	# Read the calibration status, 0=uncalibrated and 3=fully calibrated.
	sys, gyro, accel, mag = bno.get_calibration_status()
	# Orientation as a quaternion:
	#x,y,z,w = bno.read_quaterion()
	# Sensor temperature in degrees Celsius:
	temp_c = bno.read_temp()
	# Magnetometer data (in micro-Teslas):
	Mx,My,Mz = bno.read_magnetometer()
	# Gyroscope data (in degrees per second):
	Gyrx,Gyry,Gyrz = bno.read_gyroscope()
	# Accelerometer data (in meters per second squared):
	Ax,Ay,Az = bno.read_accelerometer()
	# Linear acceleration data (i.e. acceleration from movement, not gravity--
	# returned in meters per second squared):
	LAx,LAy,LAz = bno.read_linear_acceleration()
	# Gravity acceleration data (i.e. acceleration just from gravity--returned
	# in meters per second squared):
	Gx,Gy,Gz = bno.read_gravity()
	values = (heading, roll, pitch, gyro, accel, mag, temp_c, Mx,My,Mz, Gyrx, Gyry, Gyrz, Ax, Ay, Az, LAx, LAy, LAz, Gx, Gy, Gz)

	timeNow = time.time()	

	if timeNow - timeThen > 4:
		timerDelay = False
	elif timeNow - timeThen <= 4:
		timerDelay = True

	if timerDelay == False:
		Xthresh = 3
		XGyrothresh = 10
		timerDelay,timeThen = checkThresh(LAx, Xthresh, 'x-event',timerDelay, timeThen)
		timerDelay,timeThen = checkThresh(LAy, Xthresh, 'y-event',timerDelay, timeThen)
		timerDelay,timeThen = checkThresh(LAz, Xthresh, 'z-event',timerDelay, timeThen)
    		#pickle.dump( values, open(filename, "ab"))
		try: client.send( OSCMessage ("/data", values) )
		except: pass
	#time.sleep(0.01)
