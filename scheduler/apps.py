from django.apps import AppConfig


class SchedulerConfig(AppConfig):
	name = 'scheduler'
	#main tread executes as standard and other  threads are started here
	#might need to move this depending on how many times this module is used
	def ready(self):
		#from scheduler.tasks import schedulerThread as s
		pollForNew.delay()
		#thread1 = s(1, "Scheduler Thread", 1)
		#thread1.start()
		#print ("Apps works")
		


