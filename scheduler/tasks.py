from celery.task.schedules import crontab
from celery import shared_task
from celery.decorators import periodic_task
from time import sleep
from scheduler.schedulerQueue import SchedulerQ


from random import randint

schedulerQ = SchedulerQ()

@shared_task()
def SchedulerThread(schedulerQ):
	print ("Starting Scheduler") 
	counter = 0
	while(1):
		counter += 1
		if(counter > 100):
			counter = 0
		schedulerQ.setItem(counter)
		print("In Scheduler thread - " + str(counter))
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
	print("Ended task: " + str(myId))

@shared_task()
def setSchedulerQ(schedulerQueue):
	schedulerQ = schedulerQueue

@shared_task()
def getSchedulerQ():
	return schedulerQ
