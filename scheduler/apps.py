from django.apps import AppConfig
#from scheduler.tasks import repeatingTask
#from cesGroundStation.celery import app


print("HELLO FROM APPS!")

class SchedulerConfig(AppConfig):
	name = 'scheduler'
	threadsStarted = False
	
	#main tread executes as standard and other  threads are started here
	#might need to move this depending on how many times this module is used
	def ready(self):
		if(not self.threadsStarted):
			self.threadsStarted = True
			#app.control.purge()
			#print("Starting repeating task")
			#repeatingTask.delay()
			# schedulerQ = SchedulerQ()
			# setSchedulerQ.delay(schedulerQ)
			# SchedulerThread.delay(schedulerQ)
			# RotatorsThread.delay(schedulerQ)
			# getSchedulerQ.delay()

			# thread1 = SchedulerRunnable(1, "Scheduler Thread", schedulerQ)
			# thread1.start()
			# thread2 = RotatorsRunnable(2, "Rotator Thread", schedulerQ)
			# thread2.start()
