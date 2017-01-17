import requests
from scheduler.models import TLE, AzEl
import math, ephem, datetime
from datetime import date, datetime, timedelta

class Services():
	
	def updateTLE():
		"""
		Retrieves TLE data from external source, checks format and places in db 
		"""
		requestsObject = requests.get("http://celestrak.com/NORAD/elements/cubesat.txt")
		tle=requestsObject.text
	
		#splits text into one list with format:
		#name, line1, line2, name, line1, line2
		tleArray = tle.split('\r\n')

		#remove errant empty entry
		if tleArray[len(tleArray)-1]=='':
		 	del tleArray[len(tleArray)-1]
		if len(tleArray)%3 !=0:
			print ("major error") #TODO: raisemassive error


		checkedTLEArray = _Helper.checkTLEFormat(tleArray)

		i=0
		while i <= (len(checkedTLEArray)-3):
			name = _Helper.adder(checkedTLEArray[i]).strip()
			try: 
				tleEntry = TLE.objects.get(name=name)
				pass #what does pass do?
			except TLE.DoesNotExist as e:
				#create new entry in db
				newTLE = TLE(name=name, line1=checkedTLEArray[i+1], line2=checkedTLEArray[i+2])
				newTLE.save()
			else:
				#update existing
				tleEntry.line1 = checkedTLEArray[i+1]
				tleEntry.line2 = checkedTLEArray[i+2]
				tleEntry.save()
			i+=3	

	def getAzElTLENow(self, tleEntry):

		#getObserver from where?
		observer = _Helper.getObserver(self, datetime.now());

		# try: 
		# 	tleEntry = TLE.objects.get(name=tleName)
		# except TLE.DoesNotExist:
		# 	return "Error" 

		try:
			sat = ephem.readtle(tleEntry.name,tleEntry.line1, tleEntry.line2) #necessary?
		except ValueError as e:
			return "format of db is incorrect TLE"

		sat.compute(observer)
		#AzEl = [sat.az,sat.alt]
		#return sat object?
		return	AzEl(0, sat.az,sat.alt)

	def getAzElTLE(self, tleEntry,dateTime):

		#getObserver from where?
		observer = _Helper.getObserver(self, dateTime);

		try:
			sat = ephem.readtle(tleEntry.name,tleEntry.line1, tleEntry.line2) #necessary?
		except ValueError as e:
			return "format of db is incorrect TLE"

		sat.compute(observer)
		#AzEl = [sat.az,sat.alt]
		#return sat object?
		return	AzEl(0, sat.az,sat.alt)

	def getAzElForPeriod(self, riseTime, setTime, period):
		i=0
		for timestamp in _Helper.datespan(riseTime,setTime, delta=timedelta(seconds=period)):
			azel = getAzElTLE(self,tleEntry,timestamp)
			i+=1
			#change azel id?
			azelProgress.append(azel)
		return azelProgress #return object to go in db that's related to list of next passes


	def makeNextPassDetails(self,tleEntry,increments,dateTime):
		#ask for hours increments,seconds increments etc or make it only seconds
		#get future passes of satellite
		
		#make list of Az El & range, footprint, where do we have that value?  
		#in range of rise time to set time with 30 increments

		nextPassObject = getNextPass(self,tleEntry,dateTime)   #object/model
		#from rise time info[0]
		#until set time info[4]
		azelProgress = []

		i=0
		for timestamp in _Helper.datespan(nextPassObject.riseTime, nextPassObject.setTime, delta=timedelta(seconds=increments)):
			azel = getAzElTLE(self, tleEntry,timestamp)
			i+=1
			azelProgress.append(azel)
			print(timestamp)
			#new progresssion object?
			#how important is accuracy? can it be ten secs out
			#return list of foreign key related models?
		return azelProgress #return object to go in db that's related to list of next passes
	
	def getNextPass(self, tleEntry, dateTime):
		observer = __Helper.getObserver(dateTime);
		sat = ephem.readtle(tleEntry.name,tleEntry.line1, tleEntry.line2)
		details = observer.next_pass(sat)
					
		riseTime = _Helper.roundMicrosecond(details[0])
		setTime = _Helper.roundMicrosecond(details[4])
		duration  = setTime - riseTime
				#riseTime, setTime, duration, maxElevation, riseAzimuth, setAzimuth
		#return NextPass(0,riseTime, settime, duration, details[3],details[1],details[5],tleEntry)
		
	# def makeListOfNextPasses(self, tleEntry, number):

	# 	observer = __Helper.getObserver(datetime.now());
	# 	sat = ephem.readtle(tleEntry.name,tleEntry.line1, tleEntry.line2)
	# 	listOfNextPasses = []

	# 	nextPass = self.getNextPass(self, tleEntry,datetime.now())

	# 	i=0
	# 	while i<number:
	# 		for nextPassDetails in listOfNextPasses
	# 									#riseTime, setTime, duration, maxElevation, riseAzimuth, setAzimuth
	# 			np = nextPass(tleEntry,nextPassDetails[0],nextPassDetails[4],duration,nextPassDetails[3],nextPassDetails[1],nextPassDetails[5])#.save()
	# 			listOfNextPasses.extend(np)

	# 		observer = self.getObserver(info[4].datetime());

	# 		nextPass = self.getNextPass(self,tleEntry,setTime)
	# 		i+=1

	# 	makeNextPassDetails(self,tleEntry)

	# def getListOfNextPasses(tleObject)
		#limit to ten

	#def getAzElTLEOnDate(tleName, date)

class _Helper():
	#Helper Functions
	def adder(stringsep):  #nicer way?
		"""
		Adds up the split strings of the satellite name
		"""
		string=""
		for x in stringsep:
			string = string+x
		return (string)


	def checkTLEFormat(tleArray):
		"""
		Checks the format of the each TLE line to make sure it is in the correct format
		"""
		i=0
		badEntriesArray = []# needs an iterator
		while i <= (len(tleArray)-3):
			try: 
				ephem.readtle(tleArray[i],tleArray[i+1],tleArray[i+2])
			except ValueError as e:
				badEntriesArray.append(tleArray[i])
				badEntriesArray.append(tleArray[i+1])
				badEntriesArray.append(tleArray[i+2])
			i+=3

		goodEntriesArray = [entry for entry in tleArray if entry not in badEntriesArray]
		return goodEntriesArray

	def getObserver(self,datetime):

		observer = ephem.Observer();
		observer.lat = math.radians(55.8667)
		observer.long = math.radians(-4.4333)
		observer.date = ephem.Date(datetime)
		return observer
	
	def datespan(startDate, endDate, delta=timedelta(days=1)):
		currentDate = startDate
		while currentDate < endDate:
			yield currentDate
			currentDate += delta
#from stackoverflow

	def roundMicrosecond(ephemDate):
		dateTime = ephemDate.datetime()
		ms = dateTime.microsecond/1000000
		msRound = int(round(ms,0))
		dateTime = dateTime + timedelta(seconds = msRound) - timedelta(microseconds = dateTime.microsecond)
		return dateTime
		


