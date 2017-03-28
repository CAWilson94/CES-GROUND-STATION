from datetime import datetime, timedelta
from scheduler.MOT.ruleBased import MOTRuleBased
from scheduler.models import TLE, Mission, NextPass

class SchedulerServices():

	def scheduleAndSavePasses(self, scheduler, usefulTime):
		missions = Mission.objects.all().exclude(status="PAUSED")

		passes = scheduler.find(missions, usefulTime)
		print("Scheduling " + str(len(passes)) + " passes.")
		print("Removing previous passes...")
		NextPass.objects.all().delete()
		print("Done. Saving new passes...")
		for p in passes: 
			p.save()
		passes = []
		print("Done.")

		return NextPass.objects.all()