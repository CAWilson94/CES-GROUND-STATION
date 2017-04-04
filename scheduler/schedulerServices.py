'''from scheduler.MOT.ruleBased import MOTRuleBased'''
from scheduler.models import Mission, NextPass
import time
'''from scheduler.MOT.GAScheduler import MOTGA'''


class SchedulerServices():

    def scheduleAndSavePasses(self, scheduler, usefulTime):
        start = time.clock()
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
        stop = time.clock()
        run_time = float(stop - start)
        print("RUN TIME: " + str(run_time) + "---------------------------")
        return NextPass.objects.all().order_by("riseTime")


    """
	RB: 1.7127233815239506
	GA: 1.6871933330716447

	GA find method:  0.2518261348916351
	Scheduler Services: 1.7049328682093812

	RB find method: 0.11253854936622965
	Scheduler Services: 1.5128780909893056

	GA find method: 0.29648409299975853
	Scheduler Services: 1.6948029395651751

	25 generations: 
	GA find method:  0.18515130466244667
	Scheduler Services: 1.564443788325366

	15 generations: 
	GA find method: 
	Scheduler Services: 

	To get output needed: 
	Need the rise time of the first sat in next passes table
	And the set time of last sat in next passes table 

	total duration = set - rise 

	contact time = summation of all durations for every pass in the table

	time not looking = total duration - contact time

	list of sats looked at 
	number time called for each sat looked at 
	summation of time looked at for each one
	average time per pass of look for each sat 

	
    """