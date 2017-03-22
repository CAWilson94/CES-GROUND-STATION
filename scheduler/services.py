import requests
from django.db.utils import OperationalError
from scheduler.missionServices import mission_services as ms
from scheduler.models import TLE, AzEl, NextPass, Mission
import math, ephem, threading
from datetime import date, datetime, timedelta

class rotatorThread (threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.couner = counter
	def run(self):
		print ("Starting " + self.name) 
		try:
		#rs.hi()
			Services.polling()
		#rs.get_position()
		except OperationalError:
			print("RotatorThread - Could not find table (try makemigrations and migrate again)")
		print("Exiting "+ self.name)

class schedulerThread (threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.couner = counter
	def run(self):
		print ("Starting " + self.name) 
		print("Polling for new now")
		try:
			Services.pollForNew()
		# ts.removeTLEById(180)

		except OperationalError:
			print("SchedulerThread - Could not find table (try makemigrations and migrate again)")
		print("Exiting "+ self.name)

class Services():

	def pollForNew():
		print ( "Polling for new")
		try:
			mission_list = ms.findMissionsByStatus("New")
			for i in mission_list:
				i.status = ("Waiting")
				print("Count = %r" %i)
				pass
		except TLE.DoesNotExist as e:
			print("Already exists")	 

	def pollQueue():
		count = 0
		while (count < 10):
			try:
				mission_list = ms.findMissionsByStatus("Ready")
				for i in mission_list:
					i.status = ("Tracked")
				print("Count = %r" %count)
				count+=1
				pass
			except TLE.DoesNotExist as e:
				print("Already exists")	 

	def getAzElTLE(self, tleEntry, dateTime):
		"""
		Returns an AzEl object calculated with one satellite and one instanteous measure
		of time 
		"""

		# getObserver preferences file AK
		observer = _Helper.getObserver(self, dateTime);

		try:
			sat = ephem.readtle(tleEntry.name, tleEntry.line1, tleEntry.line2)  # necessary?
		except ValueError:
			return "Format of TLEEntry is incorrect (getAzElTLE)"

		sat.compute(observer)
		return	AzEl(azimuth=sat.az,elevation=sat.alt)


	def getAzElTLENow(self, tleEntry):
		return Services.getAzElTLE(self, tleEntry, datetime.now())


	def getAzElForPeriod(self, tleEntry, riseTime, setTime, period):
		"""
		Returns a list of AzEl objects calculated during the period of timestamp
		with one satellite 
		"""
		azelProgress = []
		i = 0
		for timestamp in _Helper.timeSpan(riseTime, setTime, delta=timedelta(seconds=period)):
			azel = Services.getAzElTLE(self, tleEntry, timestamp)
			i += 1  # change azel id? AK
			azelProgress.append(azel)
		return azelProgress


	def getNextPass(self, tleEntry, dateTime):
		"""
		Returns a next pass object of the satellite after the date given
		"""
		observer = _Helper.getObserver(self, dateTime);
		try:
			sat = ephem.readtle(tleEntry.name, tleEntry.line1, tleEntry.line2)
		except ValueError:
			return "Format of TLEEntry is incorrect (getNextPass)"

		details = observer.next_pass(sat)

		riseTime = _Helper.roundMicrosecond(details[0])
		setTime = _Helper.roundMicrosecond(details[4])
		duration  = setTime - riseTime
				#riseTime, setTime, duration, maxElevation, riseAzimuth, setAzimuth
		return NextPass(riseTime=riseTime, setTime=setTime, duration=duration, maxElevation=details[3],riseAzimuth=details[1],setAzimuth=details[5])

	def makeMissions(chosenSatsList): #, priorityList
		"""
		Saves user chosen satellites in the mission object and then saves that in db
		"""
		print(chosenSatsList)
		for name in chosenSatsList:
			try:
				mission = Mission.objects.get(name=name)
			except Mission.DoesNotExist as e:
				try:
					tle = TLE.objects.get(name=name)
				except TLE.DoesNotExist as e:
					#print(e)
					print("Attempted to CubeSat '{}' but it does not exist in the DB".format(name))
					#somehow asked to schedule a satellite that isn't in the database
					return False
				newMission = Mission(name=name,TLE=tle,status="NEW",priority=1)
				newMission.save()
				return True
			else:
				pass
				#update status to "needs to be scheduler again"?
		return False
			#else:
			#	mission.priorty = newPriority

	def updateTLE():
		"""
		Retrieves TLE data from external source, checks format and places in db
		"""
		tle=[]
		try:
			requestsObject = requests.get("http://celestrak.com/NORAD/elements/cubesat.txt",timeout=5)
			tle = requestsObject.text
			#requests.exceptions.RequestException.
		# except requests.packages.urllib3.exceptions.NewConnectionError as e:
		# 	print("can't connect")
		# 	return
		except OSError as ex:
			print("Cannot connect to Internet or Celestrak is unreachable")
			return

		# splits text into one list with format:  AK
		# name, line1, line2, name, line1, line2
		tleArray = tle.split('\r\n')

		# remove errant empty entry
		if tleArray[len(tleArray) - 1] == '':
			del tleArray[len(tleArray) - 1]
		if len(tleArray) % 3 != 0:
			print("major error")  # TODO: raisemassive error AK
			# cause some entry(s) don't have three entries

		checkedTLEArray = _Helper.checkTLEFormat(tleArray)

		i = 0
		while i <= (len(checkedTLEArray) - 3):
			name = _Helper.adder(checkedTLEArray[i]).strip()
			try:
				tleEntry = TLE.objects.get(name=name)
			except TLE.DoesNotExist as e:
				# create new entry in db
				newTLE = TLE(name=name, line1=checkedTLEArray[i + 1], line2=checkedTLEArray[i + 2])
				newTLE.save()
			else:
				# update existing
				tleEntry.line1 = checkedTLEArray[i + 1]
				tleEntry.line2 = checkedTLEArray[i + 2]
				tleEntry.save()
			i += 3

class _Helper():
	# Helper Functions
	def adder(stringsep):  # nicer way? AK
		"""
		Adds up the split strings of the satellite name
		"""
		string = ""
		for x in stringsep:
			string = string + x
		return (string)


	def checkTLEFormat(tleArray):
		"""
		Checks the format of the each TLE line to make sure it is in the correct format
		"""
		i = 0
		badEntriesArray = []  # needs an iterator
		while i <= (len(tleArray) - 3):
			try:
				ephem.readtle(tleArray[i], tleArray[i + 1], tleArray[i + 2])
			except ValueError:
				# print ("Bad entry ",tleArray[i]) #put in log
				badEntriesArray.append(tleArray[i])
				badEntriesArray.append(tleArray[i + 1])
				badEntriesArray.append(tleArray[i + 2])
			i += 3

		goodEntriesArray = [entry for entry in tleArray if entry not in badEntriesArray]
		return goodEntriesArray

	def getObserver(self, datetime):
		"""
		Returns glasgow observer
		"""
		observer = ephem.Observer();
		observer.lat = math.radians(55.8667)
		observer.long = math.radians(-4.4333)
		observer.date = ephem.Date(datetime)
		return observer

	def timeSpan(startTime, endTime, delta):  # timedelta(days=1)):
		"""
		Returns (yields) an iterator of timestamps in from start to end 
		in delta increments
		"""
		currentTime = startTime
		while currentTime < endTime:
			yield currentTime
			currentTime += delta
			# from stackoverflow

	def roundMicrosecond(ephemDate):
		"""
		Takes in an ephemDate object, rounds down or up the microseconds to 
		an integer and returns a python datetime object
		"""
		dateTime = ephemDate.datetime()
		ms = dateTime.microsecond / 1000000
		msRound = int(round(ms, 0))
		dateTime = dateTime + timedelta(seconds=msRound) - timedelta(microseconds=dateTime.microsecond)
		return dateTime


