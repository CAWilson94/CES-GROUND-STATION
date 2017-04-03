from scheduler.schedulerHelper import SchedulerHelper
from scheduler.MOT.schedulerInterface import MOT
from . import GA as ga


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
        orderOfPasses = []
        passes = []
        print("HALLO-------------------------------------------")
        passes = SchedulerHelper.getPassesFromMissions(self, missions)
        untouchedChromosome = ga.nextPassChromosome(passes)
        print("\n" + str(untouchedChromosome.fitness))
        population = ga.generatePopulation(chromosome=untouchedChromosome)
        # ga.printPopulation(population)
        chromosomeWinner = ga.GA(population)
        ''' instead of chromosome object you want to return the satpasslist'''
        orderOfPasses = chromosomeWinner.satPassList
        return orderOfPasses
