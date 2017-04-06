from scheduler.MOT.ruleBased import MOTRuleBased
from scheduler.models import Mission, NextPass
import time
from scheduler.MOT.testingSchedulers import test
from scheduler.MOT import GA as ga
from scheduler.MOT.GAScheduler import MOTGA


class SchedulerServices():


	#scheduler = MOTSimpleHC()
	#scheduler = MOTSteepestHC()
	#scheduler = MOTStochasticHC()
	#scheduler = MOTRandomRestartHC()
	#scheduler = MOTRuleBased()
	
	def scheduleAndSavePasses():
		start = time.clock()

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

		stop = time.clock()
		run_time = float(stop - start)
		print("RUN TIME: " + str(run_time) + "---------------------------")
		running_time_ga = scheduler.ga_runTime()
		test(NextPass.objects.all().order_by("riseTime"), running_time_ga)

		next_pass_test = ga.nextPassChromosome(
			NextPass.objects.all().order_by("riseTime"))
		
		ga.nextPass_fitnessVariety_sum(next_pass_test
									   )
		return NextPass.objects.all().order_by("riseTime")
