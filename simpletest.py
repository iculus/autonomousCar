import pickle as pickle
import datetime
import logging
import sys
import time

from Adafruit_BNO055 import BNO055


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

while True:
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno.get_calibration_status()
    # Print everything out.
    #print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(heading, roll, pitch, sys, gyro, accel, mag))
    # Other values you can optionally read:
    # Orientation as a quaternion:
    #x,y,z,w = bno.read_quaterion()
    # Sensor temperature in degrees Celsius:
    temp_c = bno.read_temp()
    #print('temp={0}'.format(temp_c))
    # Magnetometer data (in micro-Teslas):
    Mx,My,Mz = bno.read_magnetometer()
    #print('magX={0} \n magY={1} \n magZ={2}'.format(Mx,My,Mz))
    # Gyroscope data (in degrees per second):
    Gyrx,Gyry,Gyrz = bno.read_gyroscope()
    #print('gyroX={0} \n gyroY={1} \n gyroZ={2}'.format(Gyrx,Gyry,Gyrz))
    # Accelerometer data (in meters per second squared):
    Ax,Ay,Az = bno.read_accelerometer()
    #print('aForceX={0} \n aForceY={1} \n aForceZ={2}'.format(Ax,Ay,Az))
    # Linear acceleration data (i.e. acceleration from movement, not gravity--
    # returned in meters per second squared):
    LAx,LAy,LAz = bno.read_linear_acceleration()
    #print('linAForceX={0} \n linAForceY={1} \n linAForceZ={2}'.format(LAx,LAy,LAz))
    # Gravity acceleration data (i.e. acceleration just from gravity--returned
    # in meters per second squared):
    Gx,Gy,Gz = bno.read_gravity()
    #print('gForceX={0} \n gForceY={1} \n gForceZ{2}'.format(Gx,Gy,Gz))
    # Sleep for a second until the next reading.
    values = (heading, roll, pitch, gyro, accel, mag, temp_c, Mx,My,Mz, Gyrx, Gyry, Gyrz, Ax, Ay, Az, LAx, LAy, LAz, Gx, Gy, Gz)
    pickle.dump( values, open(filename, "ab"))
    time.sleep(0.01)
