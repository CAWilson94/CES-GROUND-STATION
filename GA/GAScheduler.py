from random import randint
from datetime import timedelta
from scheduler.models import NextPass
from scheduler.schedulerHelper import SchedulerHelper
from scheduler.MOT.schedulerInterface import MOT
from scheduler import GA as ga


class MOTRuleBased(MOT):

        # Returns a list of passes with no conflicts
    def find(self, missions, usefulTime):

        return orderOfPasses
