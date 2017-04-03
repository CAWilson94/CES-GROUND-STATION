from datetime import datetime, timedelta
from scheduler.MOT.ruleBased import MOTRuleBased
from scheduler.models import TLE, Mission, NextPass
from scheduler.MOT.GAScheduler import MOTGA


class SchedulerServices():

	def scheduleAndSavePasses(self, scheduler, usefulTime):
		missions = Mission.objects.all().exclude(status="PAUSED")
		print("Got missions, setting statuses...")
		for m in missions: 
			m.status = "SCHEDULING"
			m.save()
		print("Done.")
		print("Scheduling...")
		print("Removing previous passes...")
		passes = NextPass.objects.all()
		for p in passes:
			p.delete()
		print("Done.")		
		passes = scheduler.find(missions, usefulTime)
		print("Scheduled " + str(len(passes)) + " passes.")
		
		missions = Mission.objects.all()
		for p in passes:
			if(p.mission not in missions):
				p.delete()

		print("Scheduled " + str(len(passes)) + " passes.")
		
		print("Saving new passes...")
		for p in passes: 
			p.save()
		passes = []
		print("Done.")
		print("Got missions, setting statuses...")
		for m in Mission.objects.all().exclude(status="PAUSED"): 
			m.status = "SCHEDULED"
			m.save()
		print("Done.")

		return NextPass.objects.all().order_by("riseTime")