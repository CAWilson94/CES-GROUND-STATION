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
		if len(tleArray)%3 !=0:
			print ("major error") #TODO: raisemassive error
		
		checkedTLEArray = services.checkTLEFormat(tleArray)

		#call post in here?

		i=0
		while i <= (len(checkedTLEArray)-3):
			name = services.adder(checkedTLEArray[i]).strip()
			try: 
				tleentry = TLE.objects.get(name=name)
				pass
			except TLE.DoesNotExist as e:
				#create new entry in db
				newTLE = TLE(name=name, line1=checkedTLEArray[i+1], line2=checkedTLEArray[i+2])
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
		i=0
		badEntriesArray = []# needs an iterator
		while i <= (len(tleArray)-3):
			try: 
				ephem.readtle(tleArray[i],tleArray[i+1],tleArray[i+2])
			except ValueError as e:
				badEntriesArray.append(tleArray[i])
				badEntriesArray.append(tleArray[i+1])
				badEntriesArray.append(tleArray[i+2])
				print(tleArray[i])
				print(tleArray[i+1])
				print(tleArray[i+2])
			i+=3

		goodEntriesArray = [entry for entry in tleArray if entry not in badEntriesArray]
		#print(goodEntriesArray)	
		return goodEntriesArray

