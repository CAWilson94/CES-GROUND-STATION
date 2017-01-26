import requests
from scheduler.RotatorServices import rotator_services as rs
from scheduler.models import TLE, AzEl, NextPass
import math, ephem, threading
from datetime import date, datetime, timedelta

class TLE_Services():

	def findTLEById(id):
		try:
			tleEntryFi = TLE.objects.get(id = id)
			print ("got it") 
			pass
		except TLE.DoesNotExist as e:
			print ("major error") 
		return tleEntryFi

	def findTLEByName(name):
		try:
			tleEntryF = TLE.objects.get(name = name)
			print ("got it")
			pass
		except TLE.DoesNotExist as e:
			print ("major error")
		return tleEntryF

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

	