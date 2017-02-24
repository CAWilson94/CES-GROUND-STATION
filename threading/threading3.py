"""
Description of code:

Starts main thread and starts 3 differet threads from this.
Exits main thread and runs other threads.
Subclass prints current time and depending on the thread name
calls glasgow() if 1, venus if 2, and mars if 3
"""

import ephem
import datetime
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("Starting " + self.name)
        print_time(self.name, self.counter, 5)
        print ("Exiting " + self.name)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        if (threadName == "Thread-1"):
            glasgow()
        elif (threadName == "Thread-2"):
            az_alt_venus()
        else:
            az_alt_mars()
        counter -= 1

def glasgow():
	glasgow = ephem.Observer()
	glasgow.lon = '-4.4333'  # + EAST ( gpredict defaults at WEST)
	glasgow.lat = '55.8667' # + NORTH
	glasgow.elevation = 0 # From elevationmap.net
	glasgow.date = datetime.datetime.now()
	line1 = "CANX-2"
	line2 = "1 32790U 08021H   17009.81203317  .00000243  00000-0  32442-4 0  9992"
	line3 = "2 32790  97.5788  39.6856 0013256 340.5856  19.4854 14.87512065471295"
	iss = ephem.readtle(line1, line2, line3)
	iss.compute(glasgow)
	print('%s' % (iss.az))
	print('%s' % (iss.alt))

def az_alt_venus():
	gatech = ephem.Observer()
	gatech.lon = '-84.39733'
	gatech.lat = '33.775867'
	gatech.elevation = 320
	gatech.date = '1984/5/30 16:22:56'
	v = ephem.Venus(gatech)
	print('%s %s' % (v.alt, v.az))

# Expected output: 	72:19:44.8 134:14:25.3


def az_alt_mars():
	gatech = ephem.Observer()
	gatech.lon = '-84.39733'
	gatech.lat = '33.775867'
	gatech.elevation = 320
	gatech.date = '1984/5/30 16:22:56'
	v = ephem.Mars(gatech)
	print('%s %s' % (v.alt, v.az))

# Expected output: -71:51:57.3 25:28:20.0

# need observer and thing looking at
def tle():
	gatech = ephem.Observer()
	gatech.lon = '-84.39733'
	gatech.lat = '33.775867'
	gatech.elevation = 320
	gatech.date = '2017/01/10 16:22:56'
	line1 = "ISS"
	line2 = "1 25544U 98067A   17006.57365116  .00016717  00000-0  10270-3 0  9005"
	line3 = "2 25544  51.6418 123.9690 0007015  56.3626 303.8195 15.54006317 36615"
	iss = ephem.readtle(line1, line2, line3)
	iss.compute(gatech)
	print('%s' % (iss.alt))
	# Expected output: -83:23:17.7
	print('%s' % (iss.az))
	# Expected output: 67:19:50.8

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)
thread3 = myThread(3, "Thread-3", 3)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
#thread1.join()
#thread2.join()
print ("Exiting Main Thread")
