import requests
from scheduler.models import TLE
import ephem
import re

class services():

	
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
		
		checkedTLEArray = services.checkTLEFormat(tleArray)
		#checkedTLEArray = tleArray
		#call post in here?

		i=0
		while i != (len(checkedTLEArray)-3):
			name = services.adder(checkedTLEArray[i]).strip()
			try: 
				tleentry = TLE.objects.get(name=name)
				pass
			except TLE.DoesNotExist as e:
				#create new entry in db
				newTLE = TLE(name =name, line1 = checkedTLEArray[i+1], line2 = checkedTLEArray[i+2])
				newTLE.save()
			else:
				#update existing
				tleentry.line1 = checkedTLEArray[i+1]
				tleentry.line2 = checkedTLEArray[i+2]
				tleentry.save()
			i+=3	

	
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
		line1regex = '^1 ([0-9]{5}[A-Z]) ([0-9]{2}[0-9]{3}[A-Z]{1,3}) ? ? ([0-9]{5}.[0-9]{8}) (( |-).[0-9]{8})  ([0-9]{5}-[0-9]) ( |-)([0-9]{5}-[0-9]) (0)  ([0-9]{4})'
		line2regex = '^2 [0-9]{5}  ? ?[0-9]{1,3}.[0-9]{4}  ? ?[0-9]{1,3}.[0-9]{4} [0-9]{7}  ? ?[0-9]{1,3}.[0-9]{4}  ? ?[0-9]{1,3}.[0-9]{4}  ?[0-9]{1,2}.[0-9]{8} ? ? ? ?[0-9]{1,5}[0-9]'
		#use () for groups
		r1 = re.compile(line1regex)
		r2 = re.compile(line2regex)
		checkedTLEArray = []

		line1Right = False
		line2Right = False
		i=0
		while i != (len(tleArray)-3):
			line1Right =False
			line2Right =False
			if r1.match(tleArray[i+1]) is not None:
				#print ('TLE line 1 of Satellite: {0} has correct format'.format(tleArray[i]))
				#print (repr(tleArray[i+1]))
				line1Right = True
			if r2.match(tleArray[i+2]) is not None:
				#print ('TLE line 2 of Satellite: {0} has correct format'.format(tleArray[i]))
				#print (repr(tleArray[i+2]))
				line2Right = True
			if line1Right and line2Right:
				#no problem with this entry
				checkedTLEArray.append(tleArray[i])
				checkedTLEArray.append(tleArray[i+1])
				checkedTLEArray.append(tleArray[i+2])
			i+=3

		print (checkedTLEArray)
		return tleArray
