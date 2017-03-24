#import requests
#from scheduler.RotatorServices import rotator_services as rs
from scheduler.models import TLE, AzEl, NextPass, Mission
import math, ephem, threading
from datetime import date, datetime, timedelta

""" 
Mission control code that allows searching for missiont by id,
name, TLE object, status priority, No. of passes and save or 
update, can also remove by name"
"""
class mission_services():

	def findMissionById(index):
		try:
			mission = Mission.objects.get(id=index)
		except Mission.DoesNotExist:
			mission = None
		return mission

	def findMissionByName(name):
		try:
			mission = Mission.objects.get(name=name) 
		except Mission.DoesNotExist:  
			mission = None
		return mission

	def findMissionsByTLE(TLE):
		try:
			mission_list = Mission.objects.filter(TLE=TLE)
		except Mission.DoesNotExist:
			mission_list = None
		return mission_list   
	
	def findMissionsByStatus(status):
		try:
			mission_list = Mission.objects.filter(status=status)
		except Mission.DoesNotExist as e:
			print("missio didnt work")
			mission_list = None
		return mission_list

	def findMissionsByPriority(priority):
		try:
			mission_list = Mission.objects.filter(priority=priority)
		except Mission.DoesNotExist:
			mission_list = None
		return mission_list    
	 
	def findMissionsByCurrentNumberOfPasses(current_num_passes):
		try:
			mission_list = Mission.objects.filter(current_num_passes=current_num_passes)
		except Mission.DoesNotExist:
			mission_list = None
		return mission_list

	def findMissionsByMaxNumberOfPasses(max_num_passes):
		try:
			mission_list = Mission.objects.filter(max_num_passes=max_num_passes)
		except Mission.DoesNotExist:
			mission_list = None
		return mission_list

	def saveOrUpdate(mission):
	 	try:
	 		Mission.objects.update_or_create(mission)
	 		return True
	 	except Mission.DoesNotExist:
	 		return False 

	def removeMissionByName(name):  
		try:
			Mission.objects.filter(name=name).delete()
			return True
		except Mission.DoesNotExist:
			return False
	