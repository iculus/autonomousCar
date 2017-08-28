import pickle
import os
import operator

def checkEqual2(iterator):
	return len(set(iterator)) <= 1

filenames = []

for dirname,dirnames,filenamesIn in os.walk('.'):
	for filename in filenamesIn:
		if filename.endswith("-save.p"):
			filenames.append(filename)
	

years = []
months = []
days = []
hours = []
minutes = []
secs = []
names = []
for filen in filenames:
	year,month,day,hour,minute,sec,name = filen.split('-')
	years.append(year)
	months.append(month)
	days.append(day)
	hours.append(hour)
	minutes.append(minute)
	secs.append(sec)
	names.append(name)

def returnCorrectFilenameToOpen( theArray, selectionList):
	#set up empty variables
	maskArray = []
	duplicate = False
	modulefilename = 'null'
	continueCheck = True
	#sort the array in to a new array
	sortedArray = sorted(theArray, reverse=True)
	maxOfArray = sortedArray[0]
	newArrayLength = len(theArray)
	#make a masking array of all max values
	for i in range(newArrayLength):
		maskArray.append(maxOfArray)
	#check if the second value is equal to the first value
	print sortedArray
	if sortedArray[1] == maskArray[1]:
		duplicate = True
	
	#now it is known if their is a max value duplicate
	#retreive the filename if applicable
	if duplicate == False:
		#find the index of the single max value
		index,value=max(enumerate( theArray ), key=operator.itemgetter(1))
		modulefilename = filenames[index]
		continueCheck = False
	if duplicate == True:
		pass
	return modulefilename,continueCheck
		

continueS = True
if continueS == True: fileToexamine,found = returnCorrectFilenameToOpen(years,filenames)
if continueS == True: fileToExamine,continueS = returnCorrectFilenameToOpen(months,filenames)
if continueS == True: fileToExamine,continueS = returnCorrectFilenameToOpen(days,filenames)
if continueS == True: fileToExamine,continueS = returnCorrectFilenameToOpen(hours,filenames)
if continueS == True: fileToExamine,continueS = returnCorrectFilenameToOpen(minutes,filenames)

dataFromPickle = []
with (open(fileToExamine, "rb")) as openFile:
	while True:
		try:
			dataFromPickle.append(pickle.load(openFile))
		except EOFError:
			break
heading = []
roll = []
pitch = []
gyro = []
accel = []
mag = []
temp_c = []
Mx = []
My = []
Mz = []
Gyrx = []
Gyry = []
Gyrz = []
Ax = []
Ay = []
Az = []
LAx = []
LAy = []
LAz = []
Gx = []
Gy = []
Gz = []

for row in dataFromPickle:
	heading.append(row[0])
	roll.append(row[1])
	pitch.append(row[2])
	gyro.append(row[3])
	accel.append(row[4])
	mag.append(row[5])
	temp_c.append(row[6])
	Mx.append(row[7])
	My.append(row[8])
	Mz.append(row[9])
	Gyrx.append(row[10])
	Gyry.append(row[11])
	Gyrz.append(row[12])
	Ax.append(row[13])
	Ay.append(row[14])
	Az.append(row[15])
	LAx.append(row[16])
	LAy.append(row[17])
	LAz.append(row[18])
	Gx.append(row[19])
	Gy.append(row[20])
	Gz.append(row[21])

import matplotlib.pyplot as plt
f, (ax1,ax2,ax3,ax4,ax5,ax6) = plt.subplots(6, sharex=True)
ax1.plot(LAx)
ax1.set_ylabel('lin accel X')
ax2.plot(LAy)
ax2.set_ylabel('lin accel Y')
ax3.plot(LAz)
ax3.set_ylabel('lin accel Z')
ax4.plot(Gyrx)
ax4.set_ylabel('gyro X')
ax5.plot(Gyry)
ax5.set_ylabel('gyro Y')
ax6.plot(Gyrz)
ax6.set_ylabel('gyro Z')
plt.show()
