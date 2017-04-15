from scheduler.models import Mission, NextPass
from scheduler.missionServices import missionServices

from scheduler.MOT.ruleBased import MOTRuleBased
from scheduler.MOT.GAScheduler import MOTGA
from scheduler.MOT.simpleHC import MOTSimpleHC
from scheduler.MOT.steepestHC import MOTSteepestHC
from scheduler.MOT.stochasticHC import MOTStochasticHC
from scheduler.MOT.randomRestartHC import MOTRandomRestartHC

# imports for comparison of schedulers
import time
from scheduler.MOT.testingSchedulers import test
from scheduler.MOT import GA as ga
from scheduler.MOT.testingSchedulers import stats_each_sat


class SchedulerServices():

    #scheduler = MOTSimpleHC()
    #scheduler = MOTSteepestHC()
    #scheduler = MOTStochasticHC()
    #scheduler = MOTRandomRestartHC()
    #scheduler = MOTRuleBased()
    #scheduler = MOTGA()


    def scheduleAndSavePasses():
        is_testing = False
        
        start = time.clock()

        scheduler = MOTRuleBased()

        missions = missionServices.findMissionsExcludingStatus("PAUSED")
        print("Got missions, setting statuses...")
        for m in missions:
            m.status = "SCHEDULING"
            m.save()
        print("Done.")

        print("Removing previous passes...")
        NextPass.objects.all().delete()
        print("Done.")

        print("Scheduling...")
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
        for m in missionServices.findMissionsExcludingStatus("PAUSED"):
            m.status = "SCHEDULED"
            m.save()
        print("Done.")


        stop = time.clock()
        run_time = float(stop - start)
        print("RUN TIME: " + str(run_time) + "---------------------------")
        if(isTesting):
            test(NextPass.objects.all().order_by("riseTime"), run_time)
            stats_each_sat(NextPass.objects.all().order_by("riseTime"))
        return NextPass.objects.all().order_by("riseTime")
