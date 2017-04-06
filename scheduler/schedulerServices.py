'''from scheduler.MOT.ruleBased import MOTRuleBased'''
from scheduler.models import Mission, NextPass
import time
from scheduler.MOT.testingSchedulers import test
from scheduler.MOT import GA as ga
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
        running_time_ga = scheduler.ga_runTime()
        test(NextPass.objects.all().order_by("riseTime"), running_time_ga)

        next_pass_test = ga.nextPassChromosome(
            NextPass.objects.all().order_by("riseTime"))
        
        ga.nextPass_fitnessVariety_sum(next_pass_test
                                       )
        return NextPass.objects.all().order_by("riseTime")
