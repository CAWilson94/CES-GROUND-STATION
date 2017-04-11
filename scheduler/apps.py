from django.apps import AppConfig
#from scheduler.tasks import repeatingTask
#from cesGroundStation.celery import app


print("HELLO FROM APPS!")

class SchedulerConfig(AppConfig):
	name = 'scheduler'
	
	def ready(self):
		pass