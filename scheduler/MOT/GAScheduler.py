from random import randint
from datetime import timedelta
from scheduler.models import NextPass
from scheduler.schedulerHelper import SchedulerHelper
from scheduler.MOT.schedulerInterface import MOT
from . import GA as ga
from scheduler.models import Mission


class MOTRuleBased(MOT):

missions = Mission.objects.all()
        # Returns a list of passes with no conflicts
    def find(self, missions, usefulTime):
        """

        Find a list of passes with no conflicts
        """

        passes = SchedulerHelper.getPassesFromMissions(self, missions)
        print("Passes: " + str(len(passes)))

        return orderOfPasses

find(missions, 100)