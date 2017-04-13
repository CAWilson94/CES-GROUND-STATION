#from scheduler.schedulerHelper import SchedulerHelper
from scheduler.MOT._MOTHelper import _Helper
from scheduler.MOT.schedulerInterface import MOT
from . import GA as ga


class MOTGA(MOT):
    """
       Returns a list of passes with no conflicts
       """

    def find(self, missions):
        """
        'Finds' a list of next passes for a certain amount of hours,
        or days, for which conflicts have been either ignored or
        resolved using a GA.
        """
        orderOfPasses = []
        passes = []
        passes = _Helper.getPassesFromMissions(self, missions)
        untouchedChromosome = ga.nextPassChromosome(passes)
        population = ga.generatePopulation(chromosome=untouchedChromosome)
        chromosomeWinner = ga.GA(population)
        orderOfPasses = chromosomeWinner.satPassList
      
        return orderOfPasses

