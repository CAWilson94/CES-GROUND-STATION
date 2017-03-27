from django.apps import AppConfig
from scheduler.schedulerQueue import SchedulerQ
from scheduler.runnables import SchedulerRunnable, RotatorsRunnable
from scheduler.tasks import SchedulerThread, RotatorsThread, setSchedulerQ, getSchedulerQ, repeatingTask


class SchedulerConfig(AppConfig):
	name = 'scheduler'
	threadsStarted = False
	#main tread executes as standard and other  threads are started here
	#might need to move this depending on how many times this module is used
	def ready(self):
		#if(not self.threadsStarted):
		#	self.threadsStarted = True
			# schedulerQ = SchedulerQ()
			# setSchedulerQ.delay(schedulerQ)
			# SchedulerThread.delay(schedulerQ)
			# RotatorsThread.delay(schedulerQ)
			# getSchedulerQ.delay()
		print("Starting repeating task")
		repeatingTask.delay()

			# thread1 = SchedulerRunnable(1, "Scheduler Thread", schedulerQ)
			# thread1.start()
			# thread2 = RotatorsRunnable(2, "Rotator Thread", schedulerQ)
			# thread2.start()

		# print ("Apps works") # got to here
		# from scheduler.tasks import pollForNew as s
		# s.delay()
		#from scheduler.services import Services as m
		#m.test()
		#bob = m.run_once(my_function)
		#thread1 = s(1, "Scheduler Thread", 1)
		#thread1.start()
