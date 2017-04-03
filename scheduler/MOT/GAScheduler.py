from random import randint
from datetime import timedelta
from scheduler.models import NextPass
from scheduler.schedulerHelper import SchedulerHelper
from scheduler.MOT.schedulerInterface import MOT
from . import GA as ga
from . GA import Chromosome, satPass
from scheduler.models import Mission


class MOTGA(MOT):
    """
       Returns a list of passes with no conflicts
       """

    def find(self, missions, usefulTime):
        """
        'Finds' a list of next passes for a certain amount of hours, 
        or days, for which conflicts have been either ignored or 
        resolved using a GA.
        """

        """ Getting aw those next passes"""
        passes = SchedulerHelper.getPassesFromMissions(self, missions)
        query = Mission.objects.all()
        

        #for item in passes:
         #   print(item.mission.name + " start time: " +
          #        str(item.riseTime) + " end time: " + str(item.setTime))

        """
        Need to get a population which is a list of chromosomes here
        the list of chromosomes has to be objects which have two attributes: 

        (1) list of sat passes 
        (2) fitness
        """
        untouchedChromosome = ga.nextPassChromosome(passes) 
        print ("\n"  + str(untouchedChromosome.fitness))



  #      ga.GA()

        # return orderOfPasses


missions = Mission.objects.all()
m = MOTGA()
m.find(missions=missions, usefulTime=5)
