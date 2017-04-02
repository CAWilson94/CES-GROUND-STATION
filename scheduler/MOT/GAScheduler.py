from random import randint
from datetime import timedelta
from scheduler.models import NextPass
from scheduler.schedulerHelper import SchedulerHelper
from scheduler.MOT.schedulerInterface import MOT
from . import GA as ga
from scheduler.models import Mission


class MOTGA(MOT):
    """
       Returns a list of passes with no conflicts
       """

    def find(self, missions, usefulTime):
        print("hello")


        passes = SchedulerHelper.getPassesFromMissions(self, missions)
        """
        Need the name, the start and end time of each sat.
        Missions model does not have start and end time
        but does have TLE data which can be used to get start
        and end time for each pass.
        .. so will need to start from there to create the pass objects you need.
        """
        query = Mission.objects.all()
        for item in passes:
        	print(item.mission.name + " start time: " + str(item.riseTime) + " end time: " + str(item.setTime))
        # print("Passes: " + str(len(passes)))

        # return orderOfPasses


missions = Mission.objects.all()
m = MOTGA()
m.find(missions=missions, usefulTime=5)
