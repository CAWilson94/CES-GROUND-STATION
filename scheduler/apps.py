from django.apps import AppConfig


class SchedulerConfig(AppConfig):
	name = 'scheduler'
	#main tread executes as standard and other  threads are started here
	#might need to move this depending on how many times this module is used
	def ready(self):
		print ("Apps works") # got to here
		from scheduler.tasks import pollForNew as s
		s.delay()
		#thread1 = s(1, "Scheduler Thread", 1)
		#thread1.start()