#from scheduler.schedulerHelper import SchedulerHelper
from scheduler.MOT._MOTHelper import _Helper
from scheduler.MOT.schedulerInterface import MOT
from . import GA as ga
import time


class MOTGA(MOT):
    """
       Returns a list of passes with no conflicts
       """

    run_time_glob = 0

    def find(self, missions):
        """
        'Finds' a list of next passes for a certain amount of hours,
        or days, for which conflicts have been either ignored or
        resolved using a GA.
        """
        start = time.clock()
        orderOfPasses = []
        passes = []
        print("--------GA STARTING --------")
        passes = _Helper.getPassesFromMissions(self, missions)
        untouchedChromosome = ga.nextPassChromosome(passes)
        print("\n" + str(untouchedChromosome.fitness))
        population = ga.generatePopulation(chromosome=untouchedChromosome)
        # ga.printPopulation(population)
        chromosomeWinner = ga.GA(population)
        ''' instead of chromosome object you want to return the satpasslist'''
        orderOfPasses = chromosomeWinner.satPassList
        stop = time.clock()
        run_time = float(stop - start)
        print("GA TIME: " + str(run_time) + " - -------------------")
        global run_time_glob
        run_time_glob = run_time
        return orderOfPasses

    def ga_runTime(self):
        return run_time_glob
