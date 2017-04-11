from scheduler.models import Mission, NextPass

from scheduler.MOT.ruleBased import MOTRuleBased
from scheduler.MOT.GAScheduler import MOTGA
from scheduler.MOT.simpleHC import MOTSimpleHC
from scheduler.MOT.steepestHC import MOTSteepestHC
from scheduler.MOT.stochasticHC import MOTStochasticHC
from scheduler.MOT.randomRestartHC import MOTRandomRestartHC

## imports for comparison of schedulers
import time
from scheduler.MOT.testingSchedulers import test
from scheduler.MOT import GA as ga

class SchedulerServices():

	#scheduler = MOTSimpleHC()
	#scheduler = MOTSteepestHC()
	#scheduler = MOTStochasticHC()
	#scheduler = MOTRandomRestartHC()
	#scheduler = MOTRuleBased()
	
	def scheduleAndSavePasses():
		start = time.clock()

		scheduler = MOTRuleBased()
				
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

		start = time.clock()
		passes = scheduler.find(missions)
		stop = time.clock()

		run_time = float(stop - start)
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
		if(len(passes) > 0 ):
			test(NextPass.objects.all().order_by("riseTime"), run_time)

			next_pass_test = ga.nextPassChromosome(NextPass.objects.all().order_by("riseTime"))
		
			ga.nextPass_fitnessVariety_sum(next_pass_test)

		return NextPass.objects.all().order_by("riseTime")
