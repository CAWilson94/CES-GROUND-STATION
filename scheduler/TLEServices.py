from scheduler.models import TLE, AzEl, NextPass
import math, ephem, threading
from datetime import date, datetime, timedelta

class TLE_Services():

	def findTLEById(id):
		try:
			tleEntryId = TLE.objects.all() #get(id = id)
			print(repr(tleEntryId))
		except TLE.DoesNotExist as e:
			tleEntryId = None
		return tleEntryId

	def findTLEByName(name):
		tleEntryName = TLE.objects.get(name = name)
		print(repr(tleEntry))
		try:
			tleEntryName = TLE.objects.get(name = name)
			print("here" + repr(tleEntryName))
		except TLE.DoesNotExist as e:
			tleEntryName = None
		return tleEntryName

	def saveTLE(TLEw):
		try: 
			tleEntry = TLE.objects.get(name=name)
			pass #what does pass do?
		except TLE.DoesNotExist as e:
			print("Already exists")			
		else:
			newTLE = TLE(name=name, line1=line1, line2=line2)
			newTLE.save()

	def removeTLEByID(id):
		try:
			TLE.objects.get(id = id).delete()
			#tleEntryR.delete()
			print ("got it")
			pass
		except TLE.DoesNotExist as e:
			print ("major error") #TODO: raisemassive error

	