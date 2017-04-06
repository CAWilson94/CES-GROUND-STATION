from datetime import datetime, timedelta
from scheduler.MOT.ruleBased import MOTRuleBased
from scheduler.models import TLE, Mission, NextPass

class SchedulerServices():


	#scheduler = MOTSimpleHC()
	#scheduler = MOTSteepestHC()
	#scheduler = MOTStochasticHC()
	#scheduler = MOTRandomRestartHC()
	#scheduler = MOTRuleBased()
	
	def scheduleAndSavePasses():
		scheduler = MOTRuleBased()
		usefulTime = 6
		
		missions = Mission.objects.all().exclude(status="PAUSED")
		print("Got missions, setting statuses...")
		for m in missions: 
			m.status = "SCHEDULING"
			m.save()
		print("Done.")

		print("Scheduling...")
		print("Removing previous passes...")
		NextPass.objects.all().delete()
		print("Done.")

		passes = scheduler.find(missions, usefulTime)
		print("Scheduled " + str(len(passes)) + " passes.")
		
		print("Saving new passes...")
		NextPass.objects.bulk_create(passes)
		passes = []
		print("Done.")

		print("Got missions, setting statuses...")
		for m in Mission.objects.all().exclude(status="PAUSED"): 
			m.status = "SCHEDULED"
			m.save()
		print("Done.")

		return NextPass.objects.all().order_by("riseTime")