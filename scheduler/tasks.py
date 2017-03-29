from celery.task.schedules import crontab
from celery import shared_task
from celery.decorators import periodic_task
from time import sleep
from scheduler.schedulerQueue import SchedulerQ
from random import randint
from django.db import models
#from scheduler.missionServices import mission_services as ms

#from scheduler.services import pollForNew

schedulerQ = SchedulerQ()


@shared_task()
def SchedulerThread():
	print ("Starting Scheduler") 
	while(1):
		print ( "Polling for new")
		try:
			mission_list = models.mission_list.objects.filter(status="New")
			for i in mission_list:
				i.status = ("Waiting")
				print("Count = %r" %i)
				pass
		except:
			print("Nope")	 
		sleep(2)
	print("Exiting Scheduler")
	


@shared_task()
def RotatorsThread(schedulerQ):
	print ("Starting Rotators") 
	while(1):
		item = schedulerQ.getItem()
		print("In Rotators thread - " + str(item))
		sleep(2)
	print("Exiting Rotators")


# @periodic_task(
# 	run_every=(crontab(minute='*/1')),
# 	name ="repeating_task",
# 	ignore_result=True)
@shared_task()
def repeatingTask():
	myId = randint(0, 10)
	print("Started task: " + str(myId))
	sleep(10)
	#tle = TLE.objects.all()
	#index = randint(0, len(tle))
	#print("Got TLE: " + tle[index].name)
	print("Ended task: " + str(myId))

@shared_task()
def setSchedulerQ(schedulerQueue):
	schedulerQ = schedulerQueue

@shared_task()
def getSchedulerQ():
	return schedulerQ
