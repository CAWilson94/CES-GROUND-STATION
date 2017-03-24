from scheduler.models import TLE, AzEl, NextPass
import math, ephem, threading
from datetime import date, datetime, timedelta

class TLE_Services():

	def findTLEById(id):
		try:
			tleEntryId = TLE.objects.get(id = id)
		except TLE.DoesNotExist as e:
			tleEntryId = None
		return tleEntryId

	def findTLEByName(name):
		try:
			tleEntryName = TLE.objects.get(name = name)
		except TLE.DoesNotExist as e:
			tleEntryName = None
		return tleEntryName

	def saveTLE(TLEw):
		try: 
			TLEw.save()
			pass
		except TLE.DoesNotExist as e:
			print("Unable To Save")			

	def removeTLEById(id):
		try:
			TLE.objects.get(id = id).delete()
			pass
		except TLE.DoesNotExist as e:
			print ("Unable to remove from db") #TODO: raisemassive error

	